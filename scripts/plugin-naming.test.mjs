import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(fs.readFileSync(path.join(root, "catalog.json"), "utf8"));
const plugins = [
  ...catalog.plugins,
  ...(catalog.candidatePlugins ?? []).filter((candidate) => candidate.status === "release_candidate_installable"),
];

test("every plugin has English base text and Chinese localization", () => {
  for (const plugin of plugins) {
    for (const field of ["displayName", "shortDescription", "description"]) {
      assert.equal(typeof plugin[field], "string", `${plugin.id}: missing ${field}`);
      assert.ok(plugin[field].trim().length > 0, `${plugin.id}: empty ${field}`);
      assert.equal(typeof plugin.localizations?.["zh-CN"]?.[field], "string", `${plugin.id}: missing zh-CN ${field}`);
      assert.ok(plugin.localizations["zh-CN"][field].trim().length > 0, `${plugin.id}: empty zh-CN ${field}`);
    }
  }
});

test("English base fields are monolingual", () => {
  const cjk = /[\u3400-\u9fff]/;
  for (const plugin of plugins) {
    for (const field of ["displayName", "shortDescription", "description"]) {
      assert.ok(!cjk.test(plugin[field]), `${plugin.id}: English ${field} contains CJK: ${plugin[field]}`);
      assert.ok(!plugin[field].includes(" / "), `${plugin.id}: English ${field} looks bilingual`);
    }
  }
});

test("Chinese localization is monolingual and complete", () => {
  const cjk = /[\u3400-\u9fff]/;
  for (const plugin of plugins) {
    const zh = plugin.localizations["zh-CN"];
    for (const field of ["displayName", "shortDescription", "description"]) {
      assert.ok(cjk.test(zh[field]), `${plugin.id}: Chinese ${field} has no CJK`);
      assert.ok(!zh[field].includes(" / "), `${plugin.id}: Chinese ${field} looks bilingual`);
    }
  }
});

test("short and full descriptions keep separate roles", () => {
  for (const plugin of plugins) {
    for (const [locale, value] of [["en", plugin], ["zh-CN", plugin.localizations["zh-CN"]]]) {
      assert.ok(!/[\r\n]/.test(value.shortDescription), `${plugin.id}: ${locale} shortDescription contains a newline`);
      assert.ok(!/[\r\n]/.test(value.description), `${plugin.id}: ${locale} description contains a newline`);
      assert.ok(value.description.length > value.shortDescription.length, `${plugin.id}: ${locale} description is not longer than shortDescription`);
      assert.ok(value.shortDescription.length <= 120, `${plugin.id}: ${locale} shortDescription is too long`);
    }
  }
});

test("display names follow '<product>（<domain>）' with no Use/RC/benchmark suffix", () => {
  for (const plugin of plugins) {
    for (const [locale, label] of [["en", "English"], ["zh-CN", "Chinese"]]) {
      const name = locale === "en" ? plugin.displayName : plugin.localizations["zh-CN"].displayName;
      const match = locale === "en" ? name.match(/^(.+) \((.+)\)$/) : name.match(/^(.+)（(.+)）$/);
      assert.ok(match, `${plugin.id}: ${label} displayName must be '<product>（<domain>）': ${name}`);
      const [, code, domain] = match;
      assert.ok(/[A-Za-z]/.test(code), `${plugin.id}: ${label} displayName must start with the code name: ${name}`);
      assert.ok(!/\s+(Design|Factory)$/.test(code), `${plugin.id}: ${label} code name still has Design/Factory: ${name}`);
      assert.ok(!name.includes("对标"), `${plugin.id}: ${label} displayName still contains a benchmark: ${name}`);
      assert.ok(!/alternative/i.test(name), `${plugin.id}: ${label} displayName still contains an alternative marker: ${name}`);
      if (locale === "zh-CN") assert.ok(/[\u4e00-\u9fa5]/.test(domain), `${plugin.id}: ${label} domain has no Chinese: ${name}`);
      assert.ok(!/\bUse\b/.test(name), `${plugin.id}: ${label} displayName still contains "Use"`);
      assert.ok(!/\bRC\b/.test(name), `${plugin.id}: ${label} displayName still contains an RC marker`);
      assert.ok(!name.includes("类）"), `${plugin.id}: ${label} displayName uses the rejected 类 marker`);
      assert.ok(name.length <= 60, `${plugin.id}: ${label} displayName is too long (${name.length})`);
    }
    assert.ok(/[\u4e00-\u9fa5]/.test(plugin.localizations["zh-CN"].displayName), `${plugin.id}: Chinese displayName has no Chinese`);
    assert.notEqual(plugin.displayName, plugin.localizations["zh-CN"].displayName, `${plugin.id}: en and zh display names are identical`);
  }
});

test("every plugin declares its product line", () => {
  for (const plugin of plugins) {
    assert.ok(["full-aigc", "full-stack"].includes(plugin.line), `${plugin.id}: missing or invalid line`);
  }
});

test("UI plugins declare a ZCode surface and open command", () => {
  const uiPlugins = plugins.filter((plugin) => plugin.componentTypes?.includes("ui"));
  const expectedUi = [
    "cadcraft", "deckcraft", "designcraft", "effectcraft", "figcraft", "filmcraft",
    "gridcraft", "lightcraft", "photocraft", "pdfcraft", "soundcraft", "vectorcraft", "wordcraft"
  ];
  assert.deepEqual(uiPlugins.map((plugin) => plugin.id).sort(), expectedUi.sort(), "unexpected UI plugin set");
  for (const plugin of uiPlugins) {
    assert.equal(plugin.line, "full-aigc", `${plugin.id}: UI plugin is outside the content line`);
    assert.equal(plugin.ui?.surface, "editor", `${plugin.id}: missing ui.surface`);
    const repo = path.resolve(root, "..", "full-aigc-plugins-repositories", plugin.localDirectory);
    // CI only checks out this repository; the per-plugin clones are local-only.
    if (!fs.existsSync(repo)) continue;
    const manifest = JSON.parse(fs.readFileSync(path.join(repo, ".zcode-plugin/plugin.json"), "utf8"));
    const surface = manifest.ui?.surfaces?.[0];
    assert.ok(surface, `${plugin.id}: missing ui.surfaces`);
    assert.equal(surface.id, "editor", `${plugin.id}: unexpected surface id`);
    assert.equal(surface.server, `${plugin.id}-editor`, `${plugin.id}: surface server mismatch`);
    assert.equal(surface.resourceUri, `ui://${plugin.id}/panel.html`, `${plugin.id}: surface resource mismatch`);
    assert.equal(surface.availability, "session", `${plugin.id}: surface availability mismatch`);
    assert.ok(manifest.mcpServers?.[surface.server], `${plugin.id}: missing matching mcpServers entry`);
    assert.equal(manifest.commands, "commands", `${plugin.id}: missing commands declaration`);
    assert.ok(fs.existsSync(path.join(repo, "commands/open.md")), `${plugin.id}: missing commands/open.md`);
  }
});

test("global and cn marketplaces stay in sync", () => {
  execFileSync(process.execPath, [path.join(root, "scripts/verify-channel-parity.mjs")], { encoding: "utf8", stdio: "pipe" });
});
