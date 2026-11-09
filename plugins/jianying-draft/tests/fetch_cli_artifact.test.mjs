import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  fetchAndInstall,
  validateArchiveMemberPaths,
  validateArchiveMemberTypes,
  validateLockedCapabilityIdentity,
} from "../scripts/fetch_cli_artifact.mjs";
import { AdapterError } from "../scripts/runtime_adapter.mjs";

function fixtureLock() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-fetch-lock-"));
  const lockPath = path.join(root, "lock.json");
  const archiveName = "jianying-cli-1.6.0-darwin-arm64.tar.gz";
  const url = `https://github.com/full-aigc-plugins/jianying-draft/releases/download/v1.6.0/${archiveName}`;
  const artifact = {
    url,
    archiveSha256: "1".repeat(64),
    binarySha256: "2".repeat(64),
    capabilityManifestSha256: "3".repeat(64),
    sbomSha256: "4".repeat(64),
  };
  const lock = {
    resolvedVersion: "1.6.0",
    releaseRef: "v1.6.0",
    repository: "full-aigc-plugins/jianying-draft",
    sourceCommit: "a".repeat(40),
    capabilitySchema: "jianying-capabilities/v1",
    artifacts: { "darwin-arm64": artifact },
  };
  fs.writeFileSync(lockPath, JSON.stringify(lock));
  return { root, lockPath, lock, artifact };
}

test("fetcher refuses a lock redirected to another repository before network access", async () => {
  const fixture = fixtureLock();
  fixture.lock.artifacts["darwin-arm64"].url =
    "https://github.com/attacker/jianying-cli/releases/download/v1.6.0/jianying-cli-1.6.0-darwin-arm64.tar.gz";
  fs.writeFileSync(fixture.lockPath, JSON.stringify(fixture.lock));
  let fetched = false;
  await assert.rejects(
    fetchAndInstall({
      lockPath: fixture.lockPath,
      installRoot: path.join(fixture.root, "runtime"),
      platform: "darwin",
      arch: "arm64",
      fetchImpl: async () => {
        fetched = true;
        return new Response();
      },
    }),
    (error) => error instanceof AdapterError && error.code === "release_lock_invalid",
  );
  assert.equal(fetched, false);
});

test("fetcher rejects an incomplete immutable identity before network access", async () => {
  for (const mutate of [
    (lock) => { delete lock.sourceCommit; },
    (lock) => { delete lock.capabilitySchema; },
  ]) {
    const fixture = fixtureLock();
    fixture.lock.sourceCommit = "a".repeat(40);
    fixture.lock.capabilitySchema = "jianying-capabilities/v1";
    mutate(fixture.lock);
    fs.writeFileSync(fixture.lockPath, JSON.stringify(fixture.lock));
    let fetched = false;
    await assert.rejects(
      fetchAndInstall({
        lockPath: fixture.lockPath,
        installRoot: path.join(fixture.root, "runtime"),
        platform: "darwin",
        arch: "arm64",
        fetchImpl: async () => {
          fetched = true;
          return new Response();
        },
      }),
      (error) => error instanceof AdapterError && error.code === "release_lock_invalid",
    );
    assert.equal(fetched, false);
  }
});

test("fetcher rejects a tampered archive without creating an active runtime", async () => {
  const fixture = fixtureLock();
  const installRoot = path.join(fixture.root, "runtime");
  await assert.rejects(
    fetchAndInstall({
      lockPath: fixture.lockPath,
      installRoot,
      platform: "darwin",
      arch: "arm64",
      fetchImpl: async () => new Response("tampered", { status: 200 }),
    }),
    (error) => error instanceof AdapterError && error.code === "archive_checksum_mismatch",
  );
  assert.equal(fs.existsSync(path.join(installRoot, "darwin-arm64")), false);
});

test("locked capability identity must match the immutable release lock", () => {
  const lock = {
    resolvedVersion: "1.6.0",
    releaseRef: "v1.6.0",
    sourceCommit: "a".repeat(40),
    capabilitySchema: "jianying-capabilities/v1",
  };
  const capability = {
    schema: "jianying-capabilities/v1",
    cli_version: "1.6.0",
    contract_state: "released",
    release_ref: "v1.6.0",
    source_commit: "a".repeat(40),
  };
  validateLockedCapabilityIdentity(capability, lock);

  for (const [field, value] of [
    ["cli_version", "1.6.1"],
    ["contract_state", "committed_unreleased"],
    ["release_ref", "v1.5.0"],
    ["source_commit", "b".repeat(40)],
    ["schema", "jianying-capabilities/v2"],
  ]) {
    assert.throws(
      () => validateLockedCapabilityIdentity({ ...capability, [field]: value }, lock),
      (error) => error instanceof AdapterError
        && error.code === "release_capability_identity_mismatch",
      field,
    );
  }
});

test("archive member preflight rejects traversal, absolute paths and split roots", () => {
  assert.equal(
    validateArchiveMemberPaths("jianying-cli-1.6.0/LICENSE\njianying-cli-1.6.0/jianying\n"),
    "jianying-cli-1.6.0",
  );
  for (const listing of [
    "../escape\n",
    "bundle/../../escape\n",
    "/tmp/escape\n",
    "C:\\temp\\escape\n",
    "bundle/file\nother/file\n",
    "bundle//file\n",
  ]) {
    assert.throws(
      () => validateArchiveMemberPaths(listing),
      (error) => error instanceof AdapterError
        && ["archive_member_unsafe", "artifact_layout_invalid"].includes(error.code),
    );
  }
});

test("archive member preflight rejects links and special files before extraction", () => {
  validateArchiveMemberTypes(
    "drwxr-xr-x user/group 0 2026-09-20 00:00 bundle/\n"
      + "-rwxr-xr-x user/group 1 2026-09-20 00:00 bundle/jianying\n",
  );
  for (const type of ["l", "h", "b", "c", "p", "s"]) {
    assert.throws(
      () => validateArchiveMemberTypes(`${type}rwxr-xr-x unsafe-member\n`),
      (error) => error instanceof AdapterError && error.code === "archive_member_unsafe",
    );
  }
});
