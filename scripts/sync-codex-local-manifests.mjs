#!/usr/bin/env node
// Codex 的 local 来源直接读取包内清单；让包内文案与 Codex 卡片保持一致。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const write = process.argv.includes("--write");
const codex = JSON.parse(fs.readFileSync(path.join(root, ".agents/plugins/marketplace.json"), "utf8"));
const pluginsRoot = path.join(root, "plugins");
let checked = 0;

for (const entry of codex.plugins) {
  if (entry.source.source !== "local") continue;
  const packageRoot = path.resolve(root, entry.source.path);
  if (!packageRoot.startsWith(`${pluginsRoot}${path.sep}`)) {
    throw new Error(`${entry.name}: local package path escapes plugins/`);
  }
  for (const relative of ["plugin.json", ".codex-plugin/plugin.json"]) {
    const file = path.join(packageRoot, relative);
    const original = fs.readFileSync(file, "utf8");
    const manifest = JSON.parse(original);
    const interfaceCopy = relative === "plugin.json"
      ? manifest.extensions?.["com.openai"]?.interface
      : manifest.interface;
    if (!interfaceCopy) throw new Error(`${entry.name}: missing ${relative} interface`);
    manifest.description = entry.description;
    interfaceCopy.displayName = entry.interface.displayName;
    interfaceCopy.shortDescription = entry.interface.shortDescription;
    const expected = `${JSON.stringify(manifest, null, 2)}\n`;
    if (write) {
      if (original !== expected) fs.writeFileSync(file, expected);
    } else if (original !== expected) {
      throw new Error(`${entry.name}: ${relative} Codex display copy is stale; run with --write`);
    }
    checked += 1;
  }
}

console.log(`${write ? "Synchronized" : "Validated"} ${checked} local Codex manifests against Codex card copy.`);
