import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { fetchAndInstall } from "../scripts/fetch_cli_artifact.mjs";
import { handshake } from "../scripts/runtime_adapter.mjs";

const ARCHIVE = process.env.JIANYING_CLI_ARCHIVE_PATH;
const BUNDLE_ROOT = process.env.JIANYING_CLI_BUNDLE_ROOT;

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

test("a pinned archive downloads, extracts, installs and handshakes without Cargo", {
  skip: !ARCHIVE || !BUNDLE_ROOT,
}, async () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(BUNDLE_ROOT, "manifest.json"), "utf8"));
  const capabilities = JSON.parse(
    fs.readFileSync(path.join(BUNDLE_ROOT, manifest.capabilityManifest), "utf8"),
  );
  const platform = manifest.platform;
  const executable = platform.startsWith("win32") ? "jianying.exe" : "jianying";
  const releaseRef = `v${manifest.version}`;
  const archiveName = path.basename(ARCHIVE);
  const url = `https://github.com/full-aigc-plugins/jianying-draft/releases/download/${releaseRef}/${archiveName}`;
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-archive-fetch-"));
  const lockPath = path.join(root, "lock.json");
  const installRoot = path.join(root, "runtime");
  fs.writeFileSync(lockPath, JSON.stringify({
    resolvedVersion: manifest.version,
    releaseRef,
    repository: "full-aigc-plugins/jianying-draft",
    sourceCommit: capabilities.source_commit,
    capabilitySchema: capabilities.schema,
    artifacts: {
      [platform]: {
        url,
        archiveSha256: sha256(ARCHIVE),
        binarySha256: sha256(path.join(BUNDLE_ROOT, executable)),
        capabilityManifestSha256: sha256(path.join(BUNDLE_ROOT, manifest.capabilityManifest)),
        sbomSha256: sha256(path.join(BUNDLE_ROOT, "SBOM.spdx.json")),
      },
    },
  }));
  try {
    const data = await fetchAndInstall({
      lockPath,
      installRoot,
      platform: platform.startsWith("win32") ? "win32" : "darwin",
      arch: platform.endsWith("arm64") ? "arm64" : "x64",
      fetchImpl: async (requested) => {
        assert.equal(requested, url);
        const bytes = fs.readFileSync(ARCHIVE);
        return new Response(bytes, {
          status: 200,
          headers: { "content-length": String(bytes.length) },
        });
      },
    });
    assert.equal(data.archiveSha256, sha256(ARCHIVE));
    const ready = handshake({
      env: { HOME: root, PATH: "/usr/bin:/bin", JIANYING_CLI_INSTALL_ROOT: installRoot },
      platform: "darwin",
      arch: "arm64",
    });
    assert.equal(ready.source, "installed_fallback");
    assert.deepEqual(ready.manifest, capabilities);
    const statuses = Object.fromEntries(
      ready.manifest.capabilities.map((capability) => [capability.id, capability.status]),
    );
    assert.equal(statuses["schema.compile_v1_compat"], "supported");
    assert.equal(statuses["project.compile"], "supported");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
