#!/usr/bin/env node
// 生成国内（Gitee）渠道的中文市场产物。
// 与 sync-marketplaces.mjs 共用 catalog.json 单一事实源，只替换语言与代码托管地址。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(fs.readFileSync(path.join(root, "catalog.json"), "utf8"));
const args = process.argv.slice(2);
const option = (name, fallback) => {
  const prefix = `--${name}=`;
  const found = args.find((value) => value.startsWith(prefix));
  return found ? found.slice(prefix.length) : fallback;
};
const channelName = option("channel", "cn");
const channel = JSON.parse(fs.readFileSync(path.join(root, "channels", `${channelName}.json`), "utf8"));
const mode = args.includes("--write") ? "write" : "check";

const locale = channel.locale;
const localized = (plugin, field) =>
  plugin.localizations?.[locale]?.[field] ?? plugin[field];

const installableCandidates = (catalog.candidatePlugins ?? [])
  .filter((candidate) => candidate.status === "release_candidate_installable");
const plugins = [...catalog.plugins, ...installableCandidates]
  .sort((left, right) => left.id.localeCompare(right.id, "en"));

const repoPath = (plugin) => {
  const [org, name] = plugin.repository.split("/");
  if (channel.repositoryOrg) return `${channel.repositoryOrg}/${name}`;
  return `${channel.orgMap?.[org] ?? org}/${name}`;
};
const ref = (plugin) => `v${plugin.version}`;
const gitUrl = (plugin) => `${channel.codeHost}/${repoPath(plugin)}.git`;
const releaseUrl = (plugin) =>
  `${channel.codeHost}/${repoPath(plugin)}${channel.releaseTagPath}${ref(plugin)}`;
const assetUrl = (plugin) =>
  `${channel.assetBase}/${repoPath(plugin)}/raw/${ref(plugin)}/${plugin.logo}`;

const codex = {
  name: channel.marketplaceName,
  description: channel.description,
  owner: { name: "PartMe.AI", url: "https://github.com/partme-ai" },
  plugins: plugins.map((plugin) => ({
    name: plugin.id,
    source: { source: "url", url: gitUrl(plugin), ref: ref(plugin) },
    policy: { installation: "AVAILABLE", authentication: "ON_USE" },
    category: plugin.category,
    line: plugin.line,
    ...(plugin.componentTypes ? { componentTypes: plugin.componentTypes } : {}),
    version: plugin.version,
    description: localized(plugin, "description"),
    icon: assetUrl(plugin),
    interface: {
      displayName: localized(plugin, "displayName"),
      shortDescription: localized(plugin, "shortDescription"),
      logo: assetUrl(plugin)
    }
  })),
  interface: { displayName: channel.displayName }
};

const zcode = {
  name: channel.marketplaceName,
  displayName: channel.displayName,
  description: channel.description,
  plugins: plugins.map((plugin) => ({
    name: plugin.id,
    source: { source: "url", url: gitUrl(plugin), ref: ref(plugin) },
    displayName: localized(plugin, "displayName"),
    description: localized(plugin, "description"),
    version: plugin.version,
    category: plugin.category,
    line: plugin.line,
    ...(plugin.componentTypes ? { componentTypes: plugin.componentTypes } : {}),
    tags: plugin.tags,
    icon: assetUrl(plugin),
    strict: true
  }))
};

const kimi = {
  version: "2",
  displayName: channel.displayName,
  plugins: plugins.map((plugin) => ({
    id: plugin.id,
    displayName: localized(plugin, "displayName"),
    icon: assetUrl(plugin),
    source: releaseUrl(plugin)
  }))
};

const outDir = path.join(root, channel.output);
const outputs = new Map([
  [path.join(outDir, ".agents/plugins/marketplace.json"), codex],
  [path.join(outDir, "marketplace.json"), zcode],
  [path.join(outDir, "kimi-marketplace.json"), kimi]
]);

const errors = [];
const format = (value) => `${JSON.stringify(value, null, 2)}\n`;

for (const [file, value] of outputs) {
  const expected = format(value);
  if (mode === "write") {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, expected);
  } else if (!fs.existsSync(file) || fs.readFileSync(file, "utf8") !== expected) {
    errors.push(`${path.relative(root, file)} is not synchronized; run: node scripts/sync-cn-marketplace.mjs --write`);
  }
}

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log(`${mode === "write" ? "Synchronized" : "Validated"} ${plugins.length} ${locale} plugins for the ${channelName} channel.`);
