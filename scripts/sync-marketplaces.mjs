#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { validatePortableMcp } from "./portable-mcp-config.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const workspace = path.resolve(root, "..", "full-aigc-plugins-repositories");
const catalog = JSON.parse(fs.readFileSync(path.join(root, "catalog.json"), "utf8"));
const mode = process.argv.includes("--write") ? "write" : "check";
const remoteMode = process.argv.includes("--remote");
const remotePluginIds = new Set(
  process.argv
    .filter((argument) => argument.startsWith("--plugin="))
    .map((argument) => argument.slice("--plugin=".length))
);
const filteredCandidateIds = new Set(
  process.argv
    .filter((argument) => argument.startsWith("--candidate="))
    .map((argument) => argument.slice("--candidate=".length))
);

const candidatePlugins = catalog.candidatePlugins ?? [];
const installableCandidates = candidatePlugins
  .filter((candidate) => candidate.status === "release_candidate_installable");
const isInstallableCandidate = (plugin) =>
  plugin.status === "release_candidate_installable";
const marketplacePlugins = [...catalog.plugins, ...installableCandidates]
  .sort((left, right) => left.displayName.localeCompare(right.displayName, "en", { sensitivity: "base" }));

const releaseRef = (plugin) => `v${plugin.version}`;

const rawLogo = (plugin) =>
  `https://cdn.jsdelivr.net/gh/${plugin.repository}@${releaseRef(plugin)}/${plugin.logo}`;

const githubReleaseSource = (plugin) =>
  `https://github.com/${plugin.repository}/releases/tag/${releaseRef(plugin)}`;

const marketplaceDisplayName = (plugin) =>
  isInstallableCandidate(plugin) ? `${plugin.displayName} (RC)` : plugin.displayName;

const marketplaceDescription = (plugin) =>
  isInstallableCandidate(plugin)
    ? `Release candidate for controlled testing; not production-ready. ${plugin.description}`
    : plugin.description;

const pinnedIcon = (plugin) => plugin.logo ? rawLogo(plugin) : undefined;

const codex = {
  name: catalog.name,
  description: catalog.description,
  owner: { name: "PartMe.AI", url: "https://github.com/partme-ai" },
  plugins: marketplacePlugins.map((plugin) => ({
    name: plugin.id,
    source: {
      source: "url",
      url: `https://github.com/${plugin.repository}.git`,
      ref: releaseRef(plugin)
    },
    policy: { installation: "AVAILABLE", authentication: "ON_USE" },
    category: plugin.category,
    version: plugin.version,
    description: marketplaceDescription(plugin),
    ...(pinnedIcon(plugin) ? { icon: pinnedIcon(plugin) } : {}),
    interface: {
      displayName: marketplaceDisplayName(plugin),
      shortDescription: plugin.shortDescription,
      ...(pinnedIcon(plugin) ? { logo: pinnedIcon(plugin) } : {})
    }
  })),
  interface: { displayName: catalog.displayName }
};

const zcode = {
  name: catalog.name,
  displayName: catalog.displayName,
  description: catalog.description,
  plugins: marketplacePlugins.map((plugin) => ({
    name: plugin.id,
    source: { source: "github", repo: plugin.repository, ref: releaseRef(plugin) },
    description: marketplaceDescription(plugin),
    version: plugin.version,
    category: plugin.category,
    tags: plugin.tags,
    ...(pinnedIcon(plugin) ? { icon: pinnedIcon(plugin) } : {}),
    strict: true
  }))
};

const kimi = {
  version: "2",
  displayName: catalog.displayName,
  plugins: marketplacePlugins.map((plugin) => ({
    id: plugin.id,
    displayName: marketplaceDisplayName(plugin),
    ...(pinnedIcon(plugin) ? { icon: pinnedIcon(plugin) } : {}),
    source: githubReleaseSource(plugin)
  }))
};

const outputs = new Map([
  [path.join(root, ".agents/plugins/marketplace.json"), codex],
  [path.join(root, "marketplace.json"), zcode],
  [path.join(root, "kimi-marketplace.json"), kimi]
]);

const errors = [];
const format = (value) => `${JSON.stringify(value, null, 2)}\n`;

if (remotePluginIds.size > 0 && filteredCandidateIds.size > 0) {
  errors.push("--plugin and --candidate cannot be combined");
}

if (filteredCandidateIds.size > 0) {
  const knownCandidateIds = new Set((catalog.candidatePlugins ?? []).map(candidate => candidate.id));
  for (const candidateId of filteredCandidateIds) {
    if (!knownCandidateIds.has(candidateId)) errors.push(`unknown --candidate id: ${candidateId}`);
  }
}

if (remotePluginIds.size > 0) {
  const knownPluginIds = new Set(catalog.plugins.map((plugin) => plugin.id));
  for (const pluginId of remotePluginIds) {
    if (!knownPluginIds.has(pluginId)) errors.push(`unknown --plugin id: ${pluginId}`);
  }
  for (const [file, generated] of outputs) {
    if (!fs.existsSync(file)) {
      errors.push(`${path.relative(root, file)} is required for filtered synchronization`);
      continue;
    }
    const current = JSON.parse(fs.readFileSync(file, "utf8"));
    const identityKey = path.basename(file) === "kimi-marketplace.json" ? "id" : "name";
    const replacements = new Map(
      generated.plugins
        .filter((entry) => remotePluginIds.has(entry[identityKey]))
        .map((entry) => [entry[identityKey], entry])
    );
    current.plugins = current.plugins.map((entry) =>
      replacements.get(entry[identityKey]) ?? entry
    );
    outputs.set(file, current);
  }
}

if (filteredCandidateIds.size > 0) {
  for (const [file, generated] of outputs) {
    if (!fs.existsSync(file)) {
      errors.push(`${path.relative(root, file)} is required for filtered candidate synchronization`);
      continue;
    }
    const current = JSON.parse(fs.readFileSync(file, "utf8"));
    const identityKey = path.basename(file) === "kimi-marketplace.json" ? "id" : "name";
    const selectedEntries = generated.plugins
      .filter((entry) => filteredCandidateIds.has(entry[identityKey]));
    const selectedIds = new Set(selectedEntries.map((entry) => entry[identityKey]));
    const order = new Map(
      generated.plugins.map((entry, index) => [entry[identityKey], index])
    );
    current.plugins = [
      ...current.plugins.filter((entry) => !filteredCandidateIds.has(entry[identityKey])),
      ...selectedEntries
    ].sort((left, right) =>
      (order.get(left[identityKey]) ?? Number.MAX_SAFE_INTEGER)
      - (order.get(right[identityKey]) ?? Number.MAX_SAFE_INTEGER));
    for (const candidateId of filteredCandidateIds) {
      const candidate = candidatePlugins.find((entry) => entry.id === candidateId);
      if (candidate?.status === "release_candidate_installable" && !selectedIds.has(candidateId)) {
        errors.push(`${candidateId}: installable candidate has no generated ${path.relative(root, file)} entry`);
      }
    }
    outputs.set(file, current);
  }
}

const validateRemoteRelease = (plugin, options = {}) => {
  if (!remoteMode) return;
  if (remotePluginIds.size > 0 && !remotePluginIds.has(plugin.id)) return;
  if (filteredCandidateIds.size > 0 && !filteredCandidateIds.has(plugin.id)) return;
  const ref = releaseRef(plugin);
  const repositoryUrl = `https://github.com/${plugin.repository}.git`;
  let output = "";
  try {
    output = execFileSync(
      "git",
      ["ls-remote", repositoryUrl, `refs/tags/${ref}`, `refs/tags/${ref}^{}`],
      { encoding: "utf8" }
    );
  } catch (error) {
    errors.push(`${plugin.id}: cannot resolve remote tag ${ref}: ${error.message}`);
    return;
  }
  const lines = output.trim().split("\n").filter(Boolean);
  const peeled = lines.find((line) => line.endsWith(`refs/tags/${ref}^{}`));
  const direct = lines.find((line) => line.endsWith(`refs/tags/${ref}`));
  const sha = (peeled ?? direct)?.split(/\s+/)[0];
  if (!sha) {
    errors.push(`${plugin.id}: missing remote tag ${ref}`);
    return;
  }
  if (options.expectedCommit && sha !== options.expectedCommit) {
    errors.push(`${plugin.id}: remote tag ${ref} resolves to ${sha}, expected ${options.expectedCommit}`);
  }
  try {
    const release = JSON.parse(execFileSync(
      "gh",
      ["api", `repos/${plugin.repository}/releases/tags/${ref}`],
      { encoding: "utf8" }
    ));
    if (release.tag_name !== ref) {
      errors.push(`${plugin.id}: GitHub Release tag ${release.tag_name || "<missing>"} differs from ${ref}`);
    }
    if (release.draft) {
      errors.push(`${plugin.id}: GitHub Release ${ref} is still a draft`);
    }
    if (typeof options.expectedPrerelease === "boolean"
        && release.prerelease !== options.expectedPrerelease) {
      errors.push(`${plugin.id}: GitHub Release ${ref} prerelease=${release.prerelease}, expected ${options.expectedPrerelease}`);
    }
  } catch (error) {
    errors.push(`${plugin.id}: missing published GitHub Release for ${ref}: ${error.message}`);
  }
};

const validateSkills = (plugin, repo) => {
  const skillsRoot = path.join(repo, "skills");
  if (!fs.existsSync(skillsRoot)) {
    errors.push(`${plugin.id}: missing skills directory`);
    return;
  }
  const skillDirectories = fs.readdirSync(skillsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
  if (skillDirectories.length === 0) errors.push(`${plugin.id}: skills directory is empty`);
  for (const skillName of skillDirectories) {
    const skillPath = path.join(skillsRoot, skillName, "SKILL.md");
    if (!fs.existsSync(skillPath)) {
      errors.push(`${plugin.id}: missing skills/${skillName}/SKILL.md`);
      continue;
    }
    const text = fs.readFileSync(skillPath, "utf8");
    const frontmatter = text.match(/^---\n([\s\S]*?)\n---\n/);
    if (!frontmatter) {
      errors.push(`${plugin.id}: invalid frontmatter in skills/${skillName}/SKILL.md`);
      continue;
    }
    const declaredName = frontmatter[1].match(/^name:\s*["']?([^"'\n]+)["']?\s*$/m)?.[1]?.trim();
    const description = frontmatter[1].match(/^description:\s*(.+)$/m)?.[1]?.trim();
    if (declaredName !== skillName) {
      errors.push(`${plugin.id}: skill name ${declaredName ?? "<missing>"} differs from directory ${skillName}`);
    }
    if (!description) errors.push(`${plugin.id}: skill ${skillName} has no description`);
  }
};

for (const planningRepo of filteredCandidateIds.size > 0 ? [] : (catalog.planningRepositories ?? [])) {
  const repo = path.join(workspace, planningRepo.localDirectory);
  if (!fs.existsSync(repo)) {
    errors.push(`${planningRepo.name}: missing planning repository ${repo}`);
    continue;
  }
  for (const moduleName of planningRepo.modules ?? []) {
    const specification = path.join(repo, moduleName, "docs/superpowers/specs/plugin-design.md");
    if (!fs.existsSync(specification)) {
      errors.push(`${planningRepo.name}: missing ${moduleName} plugin design specification`);
    }
  }
  for (const manifest of ["plugin.json", ".codex-plugin/plugin.json", ".zcode-plugin/plugin.json", "kimi.plugin.json"]) {
    if (fs.existsSync(path.join(repo, manifest))) {
      errors.push(`${planningRepo.name}: planning-only repository must not publish ${manifest}`);
    }
  }
}

const installablePluginIds = new Set(catalog.plugins.map(plugin => plugin.id));
const candidatePluginIds = new Set();
for (const candidate of candidatePlugins) {
  if (filteredCandidateIds.size > 0 && !filteredCandidateIds.has(candidate.id)) continue;
  const missingFields = ["id", "displayName", "repository", "localDirectory", "version", "status", "releaseGate"]
    .filter(field => typeof candidate[field] !== "string" || candidate[field].trim() === "");
  for (const field of missingFields) {
    errors.push(`${candidate.id ?? "<candidate>"}: candidate plugin is missing ${field}`);
  }
  if (missingFields.length > 0) continue;
  if (candidatePluginIds.has(candidate.id)) {
    errors.push(`${candidate.id}: duplicate candidate plugin id`);
  }
  candidatePluginIds.add(candidate.id);
  if (installablePluginIds.has(candidate.id)) {
    errors.push(`${candidate.id}: candidate must not also exist in the production plugins collection`);
  }
  if (!["release_candidate_blocked", "release_candidate_installable"].includes(candidate.status)) {
    errors.push(`${candidate.id}: unsupported candidate status ${candidate.status}`);
  }
  if (isInstallableCandidate(candidate)) {
    for (const field of ["shortDescription", "category"]) {
      if (typeof candidate[field] !== "string" || candidate[field].trim() === "") {
        errors.push(`${candidate.id}: installable candidate is missing ${field}`);
      }
    }
    if (!Array.isArray(candidate.tags) || candidate.tags.length === 0) {
      errors.push(`${candidate.id}: installable candidate must declare tags`);
    }
    if (!/^\d+\.\d+\.\d+-[0-9A-Za-z][0-9A-Za-z.-]*$/u.test(candidate.version)) {
      errors.push(`${candidate.id}: installable candidate version must be a semantic pre-release`);
    }
  }

  const repo = path.resolve(workspace, candidate.localDirectory);
  if (!repo.startsWith(`${workspace}${path.sep}`)) {
    errors.push(`${candidate.id}: candidate repository must stay inside the managed repositories directory`);
    continue;
  }
  if (!fs.existsSync(repo)) {
    errors.push(`${candidate.id}: missing candidate repository ${repo}`);
    continue;
  }

  for (const relative of [".codex-plugin/plugin.json", ".zcode-plugin/plugin.json", "kimi.plugin.json"]) {
    const manifestPath = path.join(repo, relative);
    if (!fs.existsSync(manifestPath)) {
      errors.push(`${candidate.id}: missing candidate ${relative}`);
    } else {
      const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
      if (manifest.name !== candidate.id) {
        errors.push(`${candidate.id}: candidate ${relative} name is ${manifest.name}`);
      }
      if (manifest.version !== candidate.version) {
        errors.push(`${candidate.id}: candidate ${relative} version ${manifest.version} differs from ${candidate.version}`);
      }
    }
  }
  if (isInstallableCandidate(candidate)) {
    validateSkills(candidate, repo);
    errors.push(...validatePortableMcp(repo).map(error => `${candidate.id}: ${error}`));
  }

  const releaseGatePath = path.resolve(repo, candidate.releaseGate);
  if (!releaseGatePath.startsWith(`${repo}${path.sep}`)) {
    errors.push(`${candidate.id}: release gate must stay inside the candidate repository`);
  } else if (!fs.existsSync(releaseGatePath)) {
    errors.push(`${candidate.id}: missing release gate ${candidate.releaseGate}`);
  } else {
    const releaseGate = JSON.parse(fs.readFileSync(releaseGatePath, "utf8"));
    if (releaseGate.releaseStatus !== "BLOCKED") {
      errors.push(`${candidate.id}: candidate release gate must remain BLOCKED until production promotion`);
    }
    if (releaseGate.currentVersion !== candidate.version) {
      errors.push(`${candidate.id}: release gate version ${releaseGate.currentVersion} differs from ${candidate.version}`);
    }
    if (releaseGate.releaseTag !== releaseRef(candidate)) {
      errors.push(`${candidate.id}: release gate tag ${releaseGate.releaseTag} differs from ${releaseRef(candidate)}`);
    }
    if (isInstallableCandidate(candidate)) {
      validateRemoteRelease(candidate, {
        expectedPrerelease: true,
        expectedCommit: releaseGate.releaseCommit
      });
    }
  }
}

for (const [file, value] of outputs) {
  if (filteredCandidateIds.size > 0) {
    if (!fs.existsSync(file)) {
      errors.push(`${path.relative(root, file)} is required for candidate validation`);
      continue;
    }
    if (mode === "write") {
      fs.writeFileSync(file, format(value));
      continue;
    }
    const current = JSON.parse(fs.readFileSync(file, "utf8"));
    const identityKey = path.basename(file) === "kimi-marketplace.json" ? "id" : "name";
    for (const candidateId of filteredCandidateIds) {
      const candidate = candidatePlugins.find((entry) => entry.id === candidateId);
      const expectedEntry = value.plugins.find((entry) => entry[identityKey] === candidateId);
      const currentEntry = current.plugins?.find((entry) => entry[identityKey] === candidateId);
      if (candidate?.status === "release_candidate_blocked") {
        if (currentEntry) errors.push(`${path.relative(root, file)} must exclude blocked candidate ${candidateId}`);
      } else if (!currentEntry) {
        errors.push(`${path.relative(root, file)} must include installable candidate ${candidateId}`);
      } else if (JSON.stringify(currentEntry) !== JSON.stringify(expectedEntry)) {
        errors.push(`${path.relative(root, file)} installable candidate ${candidateId} is not synchronized`);
      }
    }
    continue;
  }
  const expected = format(value);
  if (mode === "write") {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, expected);
  } else if (!fs.existsSync(file) || fs.readFileSync(file, "utf8") !== expected) {
    errors.push(`${path.relative(root, file)} is not synchronized; run: node scripts/sync-marketplaces.mjs --write`);
  }
}

for (let index = 0; index < catalog.plugins.length; index += 1) {
  const plugin = catalog.plugins[index];
  if (filteredCandidateIds.size > 0) continue;
  if (remotePluginIds.size > 0 && !remotePluginIds.has(plugin.id)) continue;
  const previous = catalog.plugins[index - 1];
  if (remotePluginIds.size === 0 && previous
      && previous.displayName.localeCompare(plugin.displayName, "en", { sensitivity: "base" }) > 0) {
    errors.push(`catalog order is not alphabetical: ${previous.displayName} before ${plugin.displayName}`);
  }

  const repo = path.join(workspace, plugin.localDirectory);
  const logo = path.join(repo, plugin.logo);
  if (!fs.existsSync(logo)) errors.push(`${plugin.id}: missing ${logo}`);
  validateSkills(plugin, repo);
  errors.push(...validatePortableMcp(repo).map(error => `${plugin.id}: ${error}`));
  validateRemoteRelease(plugin, { expectedPrerelease: false });

  const repositoryMarketplacePath = path.join(repo, ".agents/plugins/marketplace.json");
  if (!fs.existsSync(repositoryMarketplacePath)) {
    errors.push(`${plugin.id}: missing ${repositoryMarketplacePath}`);
  } else {
    const repositoryMarketplace = JSON.parse(fs.readFileSync(repositoryMarketplacePath, "utf8"));
    const entry = repositoryMarketplace.plugins?.[0];
    if (!entry || repositoryMarketplace.plugins.length !== 1) {
      errors.push(`${plugin.id}: repository marketplace must contain exactly one plugin`);
    } else {
      if (entry.name !== plugin.id) errors.push(`${plugin.id}: repository marketplace name is ${entry.name}`);
      if (entry.description !== plugin.description) errors.push(`${plugin.id}: repository marketplace description differs`);
      if (entry.version !== plugin.version) errors.push(`${plugin.id}: repository marketplace version differs`);
      if (entry.source?.ref !== `v${plugin.version}`) errors.push(`${plugin.id}: repository marketplace source is not pinned to v${plugin.version}`);
      const immutableLogoPrefix = `https://cdn.jsdelivr.net/gh/${plugin.repository}@v${plugin.version}/`;
      if (!entry.icon?.startsWith(immutableLogoPrefix)) errors.push(`${plugin.id}: repository marketplace icon is not release-pinned`);
      if (!entry.interface?.logo?.startsWith(immutableLogoPrefix)) errors.push(`${plugin.id}: repository marketplace logo is not release-pinned`);
      if (entry.interface?.displayName !== plugin.displayName) errors.push(`${plugin.id}: repository marketplace displayName differs`);
      if (entry.interface?.shortDescription !== plugin.shortDescription) errors.push(`${plugin.id}: repository marketplace shortDescription differs`);
      if (repositoryMarketplace.interface?.displayName !== plugin.displayName) errors.push(`${plugin.id}: marketplace displayName differs`);
    }
  }

  const codexManifestPath = path.join(repo, ".codex-plugin/plugin.json");
  const portableManifestPath = path.join(repo, "plugin.json");
  const codexManifest = fs.existsSync(codexManifestPath)
    ? JSON.parse(fs.readFileSync(codexManifestPath, "utf8"))
    : null;
  if (fs.existsSync(portableManifestPath)) {
    const portable = JSON.parse(fs.readFileSync(portableManifestPath, "utf8"));
    if (portable.$schema !== "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json") {
      errors.push(`${plugin.id}: plugin.json has an unsupported Agent Plugins schema`);
    }
    if (portable.name !== plugin.id) errors.push(`${plugin.id}: plugin.json name is ${portable.name}`);
    if (portable.version !== plugin.version) errors.push(`${plugin.id}: plugin.json version is ${portable.version}`);
    if (portable.description !== plugin.description) errors.push(`${plugin.id}: plugin.json description differs`);
    const portableDisplayName = portable.extensions?.["com.openai"]?.interface?.displayName;
    const fallbackDisplayName = codexManifest?.interface?.displayName;
    if ((portableDisplayName ?? fallbackDisplayName) !== plugin.displayName) {
      errors.push(`${plugin.id}: OpenAI displayName differs from catalog`);
    }
  }

  for (const relative of [".codex-plugin/plugin.json", ".zcode-plugin/plugin.json", "kimi.plugin.json"]) {
    const manifestPath = path.join(repo, relative);
    if (!fs.existsSync(manifestPath)) {
      errors.push(`${plugin.id}: missing ${manifestPath}`);
      continue;
    }
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    if (manifest.name !== plugin.id) errors.push(`${plugin.id}: ${relative} name is ${manifest.name}`);
    if (manifest.description !== plugin.description) errors.push(`${plugin.id}: ${relative} description differs`);
    if (relative === ".zcode-plugin/plugin.json" && manifest.displayName !== plugin.displayName) {
      errors.push(`${plugin.id}: ${relative} displayName is ${manifest.displayName}`);
    }
    if (relative === "kimi.plugin.json") {
      if (manifest.interface?.displayName !== plugin.displayName) {
        errors.push(`${plugin.id}: ${relative} interface.displayName is ${manifest.interface?.displayName}`);
      }
      for (const field of ["skills", "commands", "agents"]) {
        const values = Array.isArray(manifest[field]) ? manifest[field] : manifest[field] ? [manifest[field]] : [];
        for (const value of values) {
          if (typeof value !== "string" || !value.startsWith("./")) {
            errors.push(`${plugin.id}: ${relative} ${field} path must start with ./`);
          } else if (!fs.existsSync(path.join(repo, value))) {
            errors.push(`${plugin.id}: ${relative} ${field} path does not exist: ${value}`);
          }
        }
      }
      if (manifest.hooks && !Array.isArray(manifest.hooks)) {
        errors.push(`${plugin.id}: ${relative} hooks must be an array`);
      }
      for (const [serverName, server] of Object.entries(manifest.mcpServers ?? {})) {
        if (server.command?.startsWith("/")) {
          errors.push(`${plugin.id}: ${relative} MCP ${serverName} command must be on PATH or start with ./`);
        }
        if (server.cwd && !server.cwd.startsWith("./")) {
          errors.push(`${plugin.id}: ${relative} MCP ${serverName} cwd must start with ./`);
        }
      }
    }
    if (manifest.version !== plugin.version && !manifest.version.startsWith(`${plugin.version}+`)) {
      errors.push(`${plugin.id}: ${relative} version ${manifest.version} does not match ${plugin.version}`);
    }
  }
}

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}

const validatedPluginCount = filteredCandidateIds.size > 0
  ? 0
  : remotePluginIds.size > 0
  ? remotePluginIds.size
  : catalog.plugins.length;
const validatedCandidateCount = filteredCandidateIds.size > 0
  ? filteredCandidateIds.size
  : candidatePlugins.length;
const validatedInstallableCandidateCount = filteredCandidateIds.size > 0
  ? [...filteredCandidateIds].filter((id) =>
      candidatePlugins.some((candidate) => candidate.id === id && isInstallableCandidate(candidate))).length
  : installableCandidates.length;
const validatedPlanningCount = filteredCandidateIds.size > 0
  ? 0
  : (catalog.planningRepositories ?? []).length;
console.log(`${mode === "write" ? "Synchronized" : "Validated"} ${validatedPluginCount} production plugins, ${validatedInstallableCandidateCount} installable RC plugin, ${validatedCandidateCount - validatedInstallableCandidateCount} blocked candidate plugin, and ${validatedPlanningCount} planning repository for Codex, ZCode, and Kimi.`);
