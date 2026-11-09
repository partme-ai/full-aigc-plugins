import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(fs.readFileSync(path.join(root, "catalog.json"), "utf8"));
const marketplace = JSON.parse(fs.readFileSync(path.join(root, ".agents/plugins/marketplace.json"), "utf8"));

test("Codex cards use the Chinese display copy from the catalog", () => {
  const entries = new Map(marketplace.plugins.map((plugin) => [plugin.name, plugin]));
  const plugins = [
    ...catalog.plugins,
    ...(catalog.candidatePlugins ?? []).filter((plugin) => plugin.status === "release_candidate_installable"),
  ];
  for (const plugin of plugins) {
    const entry = entries.get(plugin.id);
    assert.ok(entry, `${plugin.id}: missing Codex marketplace entry`);
    const zh = plugin.localizations?.["zh-CN"] ?? {};
    assert.equal(entry.interface.displayName, zh.displayName ?? plugin.displayName, `${plugin.id}: displayName`);
    assert.equal(entry.interface.shortDescription, zh.shortDescription ?? plugin.shortDescription, `${plugin.id}: shortDescription`);
    assert.equal(entry.description, zh.description ?? plugin.description, `${plugin.id}: description`);
    assert.equal(entry.version, plugin.version, `${plugin.id}: version`);
  }
});

test("local Codex packages display the same names and descriptions as ZCode", () => {
  const zcode = JSON.parse(fs.readFileSync(path.join(root, "marketplace.json"), "utf8"));
  const zcodeEntries = new Map(zcode.plugins.map((plugin) => [plugin.name, plugin]));
  for (const entry of marketplace.plugins) {
    if (entry.source.source !== "local") continue;
    const packageRoot = path.resolve(root, entry.source.path);
    assert.ok(packageRoot.startsWith(`${path.join(root, "plugins")}${path.sep}`), `${entry.name}: local path`);
    const zcodeEntry = zcodeEntries.get(entry.name);
    assert.ok(zcodeEntry, `${entry.name}: missing ZCode entry`);
    for (const relative of ["plugin.json", ".codex-plugin/plugin.json"]) {
      const manifest = JSON.parse(fs.readFileSync(path.join(packageRoot, relative), "utf8"));
      const interfaceCopy = relative === "plugin.json"
        ? manifest.extensions?.["com.openai"]?.interface
        : manifest.interface;
      assert.equal(interfaceCopy?.displayName, zcodeEntry.displayName, `${entry.name}: ${relative} displayName`);
      assert.equal(interfaceCopy?.shortDescription, zcodeEntry.description, `${entry.name}: ${relative} shortDescription`);
      assert.equal(manifest.description, zcodeEntry.description, `${entry.name}: ${relative} description`);
    }
  }
});
