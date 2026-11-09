import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { importReleaseIndex } from "../scripts/import_cli_release_index.mjs";
import { AdapterError } from "../scripts/runtime_adapter.mjs";

const digest = "a".repeat(64);

function fixture(platforms) {
  return {
    schema: "jianying-cli-release-index/v1",
    version: "1.6.0",
    releaseRef: "v1.6.0",
    repository: "full-aigc-plugins/jianying-draft",
    capabilitySchema: "jianying-capabilities/v1",
    sourceCommit: "b".repeat(40),
    artifacts: Object.fromEntries(platforms.map((platform) => [platform, {
      url: `https://github.com/full-aigc-plugins/jianying-draft/releases/download/v1.6.0/${platform}.zip`,
      archiveSha256: digest,
      binarySha256: digest,
      capabilityManifestSha256: digest,
      sbomSha256: digest,
    }])),
  };
}

function files(index) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-release-index-"));
  const indexPath = path.join(root, "index.json");
  const lockPath = path.join(root, "lock.json");
  fs.writeFileSync(indexPath, JSON.stringify(index));
  fs.writeFileSync(lockPath, JSON.stringify({
    schema: "jianying-plugin-cli-lock/v1",
    minimumVersion: "1.6.0",
    capabilitySchema: "jianying-capabilities/v1",
    artifacts: {},
  }));
  const acceptancePath = path.join(root, "host-acceptance.json");
  fs.writeFileSync(acceptancePath, JSON.stringify({
    schema: "jianying-host-release-acceptance/v1",
    status: "passed",
    pluginVersion: "0.17.2",
    cliVersion: "1.5.0",
    skillsVersion: "2.0.3",
    jobSchema: "jianying-job/v2",
    hosts: [{ host: "fixture" }],
  }));
  return { indexPath, lockPath, acceptancePath };
}

test("refuses to populate a lock from an incomplete platform index", () => {
  const paths = files(fixture(["darwin-arm64"]));
  assert.throws(
    () => importReleaseIndex(paths),
    (error) => error instanceof AdapterError && error.code === "release_index_incomplete",
  );
  assert.deepEqual(JSON.parse(fs.readFileSync(paths.lockPath)).artifacts, {});
});

test("refuses an index without an immutable source commit", () => {
  const index = fixture(["darwin-arm64", "darwin-x64", "win32-x64"]);
  index.sourceCommit = null;
  const paths = files(index);
  assert.throws(
    () => importReleaseIndex(paths),
    (error) => error instanceof AdapterError && error.code === "release_index_invalid",
  );
  assert.deepEqual(JSON.parse(fs.readFileSync(paths.lockPath)).artifacts, {});
});

test("refuses a checksum-valid index pointing at another repository or tag", () => {
  const index = fixture(["darwin-arm64", "darwin-x64", "win32-x64"]);
  index.artifacts["darwin-arm64"].url =
    "https://github.com/attacker/jianying-cli/releases/download/v1.6.0/darwin-arm64.zip";
  const paths = files(index);
  assert.throws(
    () => importReleaseIndex(paths),
    (error) => error instanceof AdapterError && error.code === "release_index_invalid",
  );
  assert.deepEqual(JSON.parse(fs.readFileSync(paths.lockPath)).artifacts, {});
});

test("atomically imports all three checksum-pinned platform artifacts", () => {
  const paths = files(fixture(["darwin-arm64", "darwin-x64", "win32-x64"]));
  const result = importReleaseIndex(paths);
  const lock = JSON.parse(fs.readFileSync(paths.lockPath));
  assert.equal(result.platforms.length, 3);
  assert.equal(lock.resolvedVersion, "1.6.0");
  assert.equal(lock.releaseRef, "v1.6.0");
  assert.equal(lock.repository, "full-aigc-plugins/jianying-draft");
  assert.equal(lock.sourceCommit, "b".repeat(40));
  assert.equal(lock.artifacts["win32-x64"].sha256, digest);
  const acceptance = JSON.parse(fs.readFileSync(paths.acceptancePath));
  assert.equal(acceptance.status, "pending");
  assert.equal(acceptance.cliVersion, "1.6.0");
  assert.deepEqual(acceptance.hosts, []);
});
