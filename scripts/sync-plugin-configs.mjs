#!/usr/bin/env node
// 渠道单语：--locale=en 生成 GitHub 英文产物；--locale=zh-CN 生成 AtomGit 中文产物。
// catalog.json 是唯一双语源；产物里的 displayName / shortDescription / description
// 只保留当前渠道语言，displayName_i18n / description_i18n 也只写当前语言。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const option = (name, fallback) => {
  const prefix = `--${name}=`;
  const found = args.find((value) => value.startsWith(prefix));
  return found ? found.slice(prefix.length) : fallback;
};
const locale = option("locale", "en");
if (!["en", "zh-CN"].includes(locale)) {
  throw new Error(`unsupported --locale=${locale}; use en or zh-CN`);
}
const workspace = path.resolve(option(
  "workspace",
  path.resolve(root, "..", "full-aigc-plugins-repositories")
));
const catalog = JSON.parse(fs.readFileSync(path.join(root, "catalog.json"), "utf8"));
const format = (value) => `${JSON.stringify(value, null, 2)}\n`;
const selectedIds = new Set(args.filter((a) => a.startsWith("--plugin=")).map((a) => a.slice("--plugin=".length)));
const includeCandidates = args.includes("--include-candidates");
const writeVersion = !args.includes("--no-version");

const pool = [
  ...catalog.plugins,
  ...(includeCandidates
    ? (catalog.candidatePlugins ?? []).filter((candidate) => candidate.status === "release_candidate_installable")
    : []),
];
const known = new Set(pool.map((plugin) => plugin.id));
for (const id of selectedIds) if (!known.has(id)) throw new Error(`unknown --plugin id: ${id}`);

// 只取当前渠道语言；缺中文时显式报错，避免悄悄回退英文。
const pick = (plugin, field) => {
  if (locale === "en") return plugin[field];
  const value = plugin.localizations?.[locale]?.[field];
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`${plugin.id}: missing ${locale} ${field}`);
  }
  return value;
};
const i18n = (plugin, field) => ({ [locale]: pick(plugin, field) });

// UI 面板标题需要同时支持宿主的中英文界面；展示名仍按渠道单语。
const allDisplayNames = (plugin) => ({
  "en-US": plugin.displayName,
  "zh-CN": plugin.localizations?.["zh-CN"]?.displayName ?? plugin.displayName
});

const openCommand = (plugin, commandLocale) => {
  const name = commandLocale === "zh-CN"
    ? (plugin.localizations?.["zh-CN"]?.displayName ?? plugin.displayName)
    : plugin.displayName;
  if (commandLocale === "zh-CN") {
    return [
      "---",
      `description: 打开 ${name}，可同时打开工作区文件`,
      "---",
      "",
      `打开 ${name}，需要时同时打开工作区文件。`,
      "",
      `调用 ${name} 的 \`open_editor\` MCP 工具。若 \`$ARGUMENTS\` 指定文件，把工作区相对路径作为 \`path\` 传入；否则省略 \`path\`。面板提供交互式编辑；仅仅打开面板不算完成编辑。面板就绪后，通过本插件的 MCP 工具检查和修改同一份文档。导入与保存使用工作区路径；手动导出使用宿主的“另存为”。检查每次工具结果和已保存文件；不要自动重试超时的编辑。`,
      ""
    ].join("\n");
  }
  return [
    "---",
    `description: Open ${name} and optionally a workspace file`,
    "---",
    "",
    `Open ${name} using its \`open_editor\` MCP tool. If \`$ARGUMENTS\` names a file, pass it as \`path\`, relative to the current workspace. Otherwise omit \`path\`. The panel provides interactive editing; do not claim to have edited a document merely by opening it. After the panel is ready, use this plugin's MCP tools to inspect and edit the same document. Use workspace paths for imports and saves; manual exports use the host Save As dialog. Check every tool result and saved file; do not automatically retry a timed-out edit.`,
    ""
  ].join("\n");
};

let written = 0;
for (const plugin of pool) {
  if (selectedIds.size && !selectedIds.has(plugin.id)) continue;
  const repo = path.join(workspace, plugin.localDirectory);
  const files = {
    marketplace: path.join(repo, ".agents/plugins/marketplace.json"),
    codex: path.join(repo, ".codex-plugin/plugin.json"),
    zcode: path.join(repo, ".zcode-plugin/plugin.json"),
    kimi: path.join(repo, "kimi.plugin.json")
  };
  for (const [kind, file] of Object.entries(files)) {
    if (!fs.existsSync(file)) throw new Error(`${plugin.id}: missing ${kind} config: ${file}`);
  }

  const releaseRef = `v${plugin.version}`;
  const repositoryUrl = `https://github.com/${plugin.repository}`;
  const logoUrl = `https://cdn.jsdelivr.net/gh/${plugin.repository}@${releaseRef}/${plugin.logo}`;

  const displayName = pick(plugin, "displayName");
  const shortDescription = pick(plugin, "shortDescription");
  const description = pick(plugin, "description");

  const marketplace = JSON.parse(fs.readFileSync(files.marketplace, "utf8"));
  const entry = marketplace.plugins?.[0];
  if (!entry || marketplace.plugins.length !== 1) {
    throw new Error(`${plugin.id}: repository marketplace must contain exactly one plugin`);
  }
  marketplace.interface ??= {};
  marketplace.interface.displayName = displayName;
  entry.name = plugin.id;
  if (writeVersion) {
    entry.source = { source: "url", url: `${repositoryUrl}.git`, ref: releaseRef };
    entry.version = plugin.version;
    entry.icon = logoUrl;
  }
  entry.policy = { installation: "AVAILABLE", authentication: "ON_USE" };
  entry.category = plugin.category;
  entry.line = plugin.line;
  if (plugin.componentTypes) entry.componentTypes = plugin.componentTypes;
  entry.description = description;
  entry.interface ??= {};
  entry.interface.displayName = displayName;
  entry.interface.shortDescription = shortDescription;
  if (writeVersion) entry.interface.logo = logoUrl;

  const codex = JSON.parse(fs.readFileSync(files.codex, "utf8"));
  codex.name = plugin.id;
  codex.description = description;
  if (writeVersion) codex.version = plugin.version;
  if ("homepage" in codex) codex.homepage = repositoryUrl;
  if ("repository" in codex) codex.repository = repositoryUrl;
  codex.interface ??= {};
  codex.interface.displayName = displayName;
  codex.interface.shortDescription = shortDescription;
  if (writeVersion) {
    codex.interface.logo = `./${plugin.logo}`;
    codex.interface.logoDark = `./${plugin.logo}`;
    codex.interface.composerIcon = `./${plugin.logo}`;
    codex.interface.composerIconDark = `./${plugin.logo}`;
  }
  if ("websiteURL" in codex.interface) codex.interface.websiteURL = repositoryUrl;
  if ("privacyPolicyURL" in codex.interface) codex.interface.privacyPolicyURL = `${repositoryUrl}/blob/main/PRIVACY.md`;
  if ("termsOfServiceURL" in codex.interface) codex.interface.termsOfServiceURL = `${repositoryUrl}/blob/main/TERMS.md`;

  const zcode = JSON.parse(fs.readFileSync(files.zcode, "utf8"));
  zcode.name = plugin.id;
  zcode.displayName = displayName;
  zcode.displayName_i18n = i18n(plugin, "displayName");
  zcode.description = description;
  if (zcode.description_i18n) zcode.description_i18n = i18n(plugin, "description");
  if (writeVersion) zcode.version = plugin.version;
  if ("homepage" in zcode) zcode.homepage = repositoryUrl;
  if ("repository" in zcode) zcode.repository = repositoryUrl;

  if (plugin.ui) {
    const surfaceId = plugin.ui.surface ?? "editor";
    const serverName = `${plugin.id}-editor`;
    zcode.ui = {
      surfaces: [{
        id: surfaceId,
        title: allDisplayNames(plugin),
        icon: plugin.ui.icon ?? "image",
        server: serverName,
        resourceUri: `ui://${plugin.id}/panel.html`,
        availability: plugin.ui.availability ?? "session"
      }]
    };
    zcode.commands = "commands";
    zcode.mcpServers = {
      [serverName]: {
        type: "stdio",
        command: "node",
        args: ["${ZCODE_PLUGIN_ROOT}/ui/bootstrap.mjs"],
        cwd: "${ZCODE_PROJECT_DIR}",
        env: {
          CRAFT_PANEL_METADATA_FILE: "${ZCODE_PLUGIN_ROOT}/.zcode-plugin/panel-meta.json",
          CRAFT_WORKSPACE_ROOT: "${ZCODE_PROJECT_DIR}"
        }
      }
    };
    const commandsDir = path.join(repo, "commands");
    fs.mkdirSync(commandsDir, { recursive: true });
    fs.writeFileSync(path.join(commandsDir, "open.md"), openCommand(plugin, locale));
    written += 1;
  }

  const kimi = JSON.parse(fs.readFileSync(files.kimi, "utf8"));
  kimi.name = plugin.id;
  kimi.description = description;
  if (writeVersion) kimi.version = plugin.version;
  if ("homepage" in kimi) kimi.homepage = repositoryUrl;
  kimi.interface ??= {};
  kimi.interface.displayName = displayName;
  kimi.interface.shortDescription = shortDescription;
  if ("websiteURL" in kimi.interface) kimi.interface.websiteURL = repositoryUrl;

  for (const [kind, file] of Object.entries(files)) {
    fs.writeFileSync(file, format({ marketplace, codex, zcode, kimi }[kind]));
    written += 1;
  }

  for (const relative of ["plugin.json", ".claude-plugin/plugin.json"]) {
    const file = path.join(repo, relative);
    if (!fs.existsSync(file)) continue;
    const value = JSON.parse(fs.readFileSync(file, "utf8"));
    if (writeVersion) value.version = plugin.version;
    if ("description" in value) value.description = description;
    if (relative === "plugin.json") {
      value.extensions ??= {};
      value.extensions["com.openai"] ??= {};
      value.extensions["com.openai"].interface = codex.interface;
    }
    fs.writeFileSync(file, format(value));
    written += 1;
  }
}

console.log(`Synchronized ${written} plugin configuration files (${locale}).`);
