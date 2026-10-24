#!/usr/bin/env node
// 校验全球（GitHub/英文）与国内（Gitee/中文）两个渠道的插件身份完全一致。
// 只允许展示文案与代码托管地址不同；id、version、ref 必须逐项相等。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (rel) => JSON.parse(fs.readFileSync(path.join(root, rel), "utf8"));
const identity = (file, key) => {
  const value = read(file);
  const map = new Map();
  for (const entry of value.plugins ?? []) {
    const id = entry[key];
    if (!id) throw new Error(`${file}: entry without ${key}`);
    map.set(id, { version: entry.version ?? null, ref: entry.source?.ref ?? null, displayName: entry.displayName ?? entry.interface?.displayName ?? null });
  }
  return map;
};

const pairs = [
  ["marketplace.json", "cn-marketplace/marketplace.json", "name"],
  ["kimi-marketplace.json", "cn-marketplace/kimi-marketplace.json", "id"],
  [".agents/plugins/marketplace.json", "cn-marketplace/.agents/plugins/marketplace.json", "name"]
];

const errors = [];
for (const [globalFile, cnFile, key] of pairs) {
  const left = identity(globalFile, key);
  const right = identity(cnFile, key);
  for (const id of left.keys()) if (!right.has(id)) errors.push(`${id}: missing from ${cnFile}`);
  for (const id of right.keys()) if (!left.has(id)) errors.push(`${id}: missing from ${globalFile}`);
  for (const [id, a] of left) {
    const b = right.get(id);
    if (!b) continue;
    if (a.version !== b.version) errors.push(`${id}: version ${a.version} != ${b.version}`);
    // 本地快照或 ZIP 源没有 ref，此时以 version 为身份；两边都有 ref 时必须相等。
    if (a.ref && b.ref && a.ref !== b.ref) errors.push(`${id}: ref ${a.ref} != ${b.ref}`);
    if (!a.displayName) errors.push(`${id}: ${globalFile} entry has no displayName`);
    if (!b.displayName) errors.push(`${id}: ${cnFile} entry has no displayName`);
    if (String(a.displayName).includes("(RC)") || String(b.displayName).includes("(RC)")) {
      errors.push(`${id}: displayName still carries an RC marker`);
    }
  }
}

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log("Channel parity OK: ids, versions and refs match across global and cn marketplaces.");
