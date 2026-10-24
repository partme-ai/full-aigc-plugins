import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const readJson = relative => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));

test("Content Factory RC is visible and test-installable without becoming a production plugin", () => {
  const catalog = readJson("catalog.json");
  const candidate = catalog.candidatePlugins?.find(entry => entry.id === "content-factory");

  assert.ok(candidate, "content-factory must be present in catalog.candidatePlugins");
  assert.equal(candidate.status, "release_candidate_installable");
  assert.equal(candidate.version, "1.0.0-rc.2");
  assert.equal(candidate.releaseGate, "docs/verification/release-candidate.json");
  assert.equal(catalog.plugins.some(entry => entry.id === "content-factory"), false);

  const codex = readJson(".agents/plugins/marketplace.json").plugins
    .find(entry => entry.name === "content-factory");
  assert.ok(codex, "Codex marketplace must expose content-factory RC");
  assert.equal(codex.version, "1.0.0-rc.2");
  assert.equal(codex.source.ref, "v1.0.0-rc.2");
  assert.equal(codex.policy.installation, "AVAILABLE");
  assert.equal(codex.interface.displayName, candidate.displayName);
  assert.ok(codex.description.length > 0);

  const zcode = readJson("marketplace.json").plugins
    .find(entry => entry.name === "content-factory");
  assert.ok(zcode, "ZCode marketplace must expose content-factory RC");
  assert.equal(zcode.version, "1.0.0-rc.2");
  assert.equal(zcode.source.ref, "v1.0.0-rc.2");
  assert.ok(zcode.description.length > 0);

  const kimi = readJson("kimi-marketplace.json").plugins
    .find(entry => entry.id === "content-factory");
  assert.ok(kimi, "Kimi marketplace must expose content-factory RC");
  assert.equal(kimi.displayName, candidate.displayName);
  assert.equal(
    kimi.source,
    "https://github.com/full-aigc-plugins/content-factory-plugin/releases/tag/v1.0.0-rc.2"
  );

  const validation = spawnSync(
    process.execPath,
    [path.join(root, "scripts", "sync-marketplaces.mjs"), "--candidate=content-factory"],
    { cwd: root, encoding: "utf8" }
  );
  assert.equal(validation.status, 0, `${validation.stdout}\n${validation.stderr}`);
});
