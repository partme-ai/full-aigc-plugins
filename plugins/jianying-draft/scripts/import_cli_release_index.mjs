#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { AdapterError } from "./runtime_adapter.mjs";

const PLATFORMS = ["darwin-arm64", "darwin-x64", "win32-x64"];
const REPOSITORY = "full-aigc-plugins/jianying-draft";
const SHA256 = /^[a-f0-9]{64}$/i;
const COMMIT = /^[a-f0-9]{40}$/i;

function compareVersions(left, right) {
  const a = left.split(".").map(Number);
  const b = right.split(".").map(Number);
  for (let index = 0; index < 3; index += 1) {
    if (!Number.isInteger(a[index]) || !Number.isInteger(b[index])) return Number.NaN;
    if (a[index] !== b[index]) return a[index] < b[index] ? -1 : 1;
  }
  return 0;
}

export function importReleaseIndex({ indexPath, lockPath }) {
  const index = JSON.parse(fs.readFileSync(indexPath, "utf8"));
  if (index.schema !== "jianying-cli-release-index/v1") {
    throw new AdapterError("release_index_schema_invalid", "unsupported CLI release index schema");
  }
  if (!COMMIT.test(index.sourceCommit ?? "")) {
    throw new AdapterError("release_index_invalid", "release index sourceCommit is invalid");
  }
  const expectedRef = `v${index.version}`;
  if (index.repository !== REPOSITORY || index.releaseRef !== expectedRef) {
    throw new AdapterError(
      "release_index_invalid",
      "release index repository/ref identity is invalid",
      { repository: index.repository ?? null, releaseRef: index.releaseRef ?? null },
    );
  }
  const releasePrefix = `https://github.com/${REPOSITORY}/releases/download/${expectedRef}/`;
  const artifacts = {};
  for (const platform of PLATFORMS) {
    const entry = index.artifacts?.[platform];
    if (!entry) throw new AdapterError("release_index_incomplete", `release index is missing ${platform}`);
    for (const field of ["url", "archiveSha256", "binarySha256", "capabilityManifestSha256", "sbomSha256"]) {
      if (!entry[field] || (field !== "url" && !SHA256.test(entry[field]))) {
        throw new AdapterError("release_index_invalid", `${platform}.${field} is invalid`);
      }
    }
    const archiveName = entry.url.startsWith(releasePrefix)
      ? entry.url.slice(releasePrefix.length)
      : "";
    if (!archiveName || archiveName.includes("/") || archiveName.includes("\\")) {
      throw new AdapterError(
        "release_index_invalid",
        `${platform}.url must belong to ${REPOSITORY} ${expectedRef}`,
      );
    }
    artifacts[platform] = { ...entry, sha256: entry.binarySha256 };
  }
  const lock = JSON.parse(fs.readFileSync(lockPath, "utf8"));
  const versionOrder = compareVersions(index.version, lock.minimumVersion);
  if (Number.isNaN(versionOrder) || versionOrder < 0
      || index.capabilitySchema !== lock.capabilitySchema) {
    throw new AdapterError("release_index_incompatible", "release index does not satisfy the plugin lock");
  }
  const updated = {
    ...lock,
    resolvedVersion: index.version,
    releaseRef: index.releaseRef,
    repository: index.repository,
    sourceCommit: index.sourceCommit,
    artifacts,
  };
  const acceptancePath = path.join(path.dirname(lockPath), "host-acceptance.json");
  if (!fs.existsSync(acceptancePath)) {
    throw new AdapterError(
      "host_acceptance_missing",
      "CLI release import requires runtime/host-acceptance.json",
    );
  }
  const acceptance = JSON.parse(fs.readFileSync(acceptancePath, "utf8"));
  if (acceptance.schema !== "jianying-host-release-acceptance/v1") {
    throw new AdapterError("host_acceptance_invalid", "unsupported host acceptance schema");
  }
  const resetAcceptance = {
    ...acceptance,
    status: "pending",
    cliVersion: index.version,
    hosts: [],
  };
  const temporary = `${lockPath}.${process.pid}.tmp`;
  const acceptanceTemporary = `${acceptancePath}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, `${JSON.stringify(updated, null, 2)}\n`, "utf8");
  fs.writeFileSync(
    acceptanceTemporary,
    `${JSON.stringify(resetAcceptance, null, 2)}\n`,
    "utf8",
  );
  // 先失效宿主证据，再激活新 CLI 锁；中断时最多保持 fail-closed 的 pending 状态。
  fs.renameSync(acceptanceTemporary, acceptancePath);
  fs.renameSync(temporary, lockPath);
  return { version: index.version, platforms: PLATFORMS, lockPath, acceptancePath };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2);
    const value = (flag) => args[args.indexOf(flag) + 1];
    const data = importReleaseIndex({ indexPath: value("--index"), lockPath: value("--lock") });
    console.log(JSON.stringify({ ok: true, data }));
  } catch (error) {
    const failure = error instanceof AdapterError ? error : new AdapterError("release_index_import_failed", error.message);
    console.log(JSON.stringify({ ok: false, error: failure.toJSON() }));
    process.exitCode = 1;
  }
}
