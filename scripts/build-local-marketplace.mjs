#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const target = path.join(root, "dist/local-marketplace");
const staging = `${target}.tmp`;
fs.rmSync(staging, { recursive: true, force: true });
fs.mkdirSync(staging, { recursive: true });
for (const relative of [".agents/plugins/marketplace.json", "marketplace.json", "kimi-marketplace.json"]) {
  fs.mkdirSync(path.dirname(path.join(staging, relative)), { recursive: true });
  fs.copyFileSync(path.join(root, relative), path.join(staging, relative));
}
const manifest = JSON.parse(fs.readFileSync(path.join(staging, ".agents/plugins/marketplace.json")));
const localNames = new Set(manifest.plugins.filter(plugin => plugin.source?.source === "local").map(plugin => plugin.name));
for (const plugin of manifest.plugins) {
  if (plugin.source?.source !== "local") continue;
  const relative = plugin.source.path;
  if (!/^\.\/plugins\/[a-z0-9-]+$/.test(relative)) throw new Error(`unsafe source path: ${relative}`);
  const source = path.join(root, relative);
  if (!fs.statSync(source).isDirectory()) throw new Error(`missing package: ${source}`);
  fs.cpSync(source, path.join(staging, relative), { recursive: true });
}
const zcodePath = path.join(staging, "marketplace.json");
const zcode = JSON.parse(fs.readFileSync(zcodePath, "utf8"));
for (const plugin of zcode.plugins) {
  if (localNames.has(plugin.name)) plugin.source = `./plugins/${plugin.name}`;
}
fs.writeFileSync(zcodePath, `${JSON.stringify(zcode, null, 2)}\n`);
fs.rmSync(target, { recursive: true, force: true });
fs.renameSync(staging, target);
console.log(`Built ${target} with ${manifest.plugins.filter(p => p.source?.source === "local").length} aggregated packages.`);
