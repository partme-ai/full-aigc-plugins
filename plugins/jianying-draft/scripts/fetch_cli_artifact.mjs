#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { installBundle, upgradeBundle } from "./install_cli_bundle.mjs";
import { AdapterError, sha256File } from "./runtime_adapter.mjs";

const REPOSITORY = "full-aigc-plugins/jianying-draft";
const MAX_ARCHIVE_BYTES = 256 * 1024 * 1024;
const SUPPORTED = new Set(["darwin-arm64", "darwin-x64", "win32-x64"]);

function platformKey(platform, arch) {
  return `${platform}-${arch}`;
}

function loadArtifact(lockPath, platform, arch) {
  const lock = JSON.parse(fs.readFileSync(lockPath, "utf8"));
  const key = platformKey(platform, arch);
  if (!SUPPORTED.has(key)) {
    throw new AdapterError("unsupported_platform", `no release artifact for ${key}`);
  }
  const expectedRef = `v${lock.resolvedVersion}`;
  if (lock.repository !== REPOSITORY || lock.releaseRef !== expectedRef) {
    throw new AdapterError(
      "release_lock_invalid",
      "CLI lock is not bound to the canonical repository and immutable version ref",
    );
  }
  if (!/^[a-f0-9]{40}$/i.test(lock.sourceCommit ?? "")
      || lock.capabilitySchema !== "jianying-capabilities/v1") {
    throw new AdapterError(
      "release_lock_invalid",
      "CLI lock lacks an immutable source commit or supported capability schema",
    );
  }
  const artifact = lock.artifacts?.[key];
  if (!artifact) {
    throw new AdapterError("release_lock_incomplete", `CLI lock has no artifact for ${key}`);
  }
  const extension = key.startsWith("win32") ? ".zip" : ".tar.gz";
  const archiveName = `jianying-cli-${lock.resolvedVersion}-${key}${extension}`;
  const expectedUrl = `https://github.com/${REPOSITORY}/releases/download/${expectedRef}/${archiveName}`;
  if (artifact.url !== expectedUrl) {
    throw new AdapterError(
      "release_lock_invalid",
      `${key} artifact URL does not match the canonical release asset`,
      { expected: expectedUrl, actual: artifact.url ?? null },
    );
  }
  for (const field of [
    "archiveSha256", "binarySha256", "capabilityManifestSha256", "sbomSha256",
  ]) {
    if (!/^[a-f0-9]{64}$/i.test(artifact[field] ?? "")) {
      throw new AdapterError("release_lock_invalid", `${key}.${field} is not a SHA-256 digest`);
    }
  }
  return { artifact, archiveName, key, lock };
}

async function downloadArchive(url, output, expectedSha256, fetchImpl) {
  const response = await fetchImpl(url, { redirect: "follow" });
  if (!response.ok) {
    throw new AdapterError(
      "artifact_download_failed",
      `artifact download failed with HTTP ${response.status}`,
      { url, status: response.status },
    );
  }
  const declaredLength = Number(response.headers.get("content-length") ?? 0);
  if (declaredLength > MAX_ARCHIVE_BYTES) {
    throw new AdapterError("artifact_too_large", "artifact exceeds the download size limit");
  }
  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.byteLength === 0 || bytes.byteLength > MAX_ARCHIVE_BYTES) {
    throw new AdapterError("artifact_size_invalid", "artifact download has an invalid size");
  }
  fs.writeFileSync(output, bytes);
  const actual = sha256File(output);
  if (actual !== expectedSha256.toLowerCase()) {
    throw new AdapterError(
      "archive_checksum_mismatch",
      "downloaded archive checksum does not match the release lock",
      { expected: expectedSha256.toLowerCase(), actual },
    );
  }
}

function assertSafeExtractedTree(root) {
  const visit = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const candidate = path.join(directory, entry.name);
      const metadata = fs.lstatSync(candidate);
      if (metadata.isSymbolicLink()) {
        throw new AdapterError(
          "archive_member_unsafe",
          `release archive contains a symbolic link: ${path.relative(root, candidate)}`,
        );
      }
      if (metadata.isDirectory()) visit(candidate);
    }
  };
  visit(root);
}

export function validateArchiveMemberPaths(listing) {
  const members = listing.split(/\r?\n/).filter((entry) => entry.length > 0);
  if (members.length === 0) {
    throw new AdapterError("artifact_layout_invalid", "release archive has no members");
  }
  const roots = new Set();
  for (const original of members) {
    const member = original.replaceAll("\\", "/").replace(/\/$/, "");
    if (!member || member.includes("\0") || member.startsWith("/")
        || /^[A-Za-z]:\//.test(member)) {
      throw new AdapterError(
        "archive_member_unsafe",
        `release archive contains an absolute or empty member path: ${original}`,
      );
    }
    const segments = member.split("/");
    if (segments.some((segment) => !segment || segment === "." || segment === "..")) {
      throw new AdapterError(
        "archive_member_unsafe",
        `release archive member escapes its bundle root: ${original}`,
      );
    }
    roots.add(segments[0]);
  }
  if (roots.size !== 1) {
    throw new AdapterError(
      "artifact_layout_invalid",
      "release archive must contain exactly one declared bundle root",
    );
  }
  return [...roots][0];
}

export function validateArchiveMemberTypes(listing) {
  const members = listing.split(/\r?\n/).filter((entry) => entry.length > 0);
  if (members.length === 0) {
    throw new AdapterError("artifact_layout_invalid", "release archive has no typed members");
  }
  for (const member of members) {
    const type = member[0];
    if (type !== "-" && type !== "d") {
      throw new AdapterError(
        "archive_member_unsafe",
        "release archive may contain only regular files and directories",
        { memberType: type },
      );
    }
  }
}

function extractArchive(archive, destination, tarCommand) {
  const listing = spawnSync(tarCommand, ["-tf", archive], {
    encoding: "utf8",
    windowsHide: true,
  });
  if (listing.error || listing.status !== 0) {
    throw new AdapterError(
      "artifact_inspect_failed",
      "could not inspect the verified CLI archive before extraction",
      { error: listing.error?.message ?? null, exitCode: listing.status, stderr: listing.stderr },
    );
  }
  const declaredRoot = validateArchiveMemberPaths(listing.stdout);
  const typedListing = spawnSync(tarCommand, ["-tvf", archive], {
    encoding: "utf8",
    windowsHide: true,
  });
  if (typedListing.error || typedListing.status !== 0) {
    throw new AdapterError(
      "artifact_inspect_failed",
      "could not inspect verified CLI archive member types before extraction",
      {
        error: typedListing.error?.message ?? null,
        exitCode: typedListing.status,
        stderr: typedListing.stderr,
      },
    );
  }
  validateArchiveMemberTypes(typedListing.stdout);
  const result = spawnSync(tarCommand, ["-xf", archive, "-C", destination], {
    encoding: "utf8",
    windowsHide: true,
  });
  if (result.error || result.status !== 0) {
    throw new AdapterError(
      "artifact_extract_failed",
      "could not extract the verified CLI archive",
      { error: result.error?.message ?? null, exitCode: result.status, stderr: result.stderr },
    );
  }
  assertSafeExtractedTree(destination);
  const entries = fs.readdirSync(destination, { withFileTypes: true });
  if (entries.length !== 1 || !entries[0].isDirectory() || entries[0].name !== declaredRoot) {
    throw new AdapterError("artifact_layout_invalid", "release archive must contain one bundle directory");
  }
  return path.join(destination, entries[0].name);
}

export function validateLockedCapabilityIdentity(capability, lock) {
  const expected = {
    schema: lock.capabilitySchema,
    cli_version: lock.resolvedVersion,
    contract_state: "released",
    release_ref: lock.releaseRef,
    source_commit: lock.sourceCommit,
  };
  const actual = Object.fromEntries(
    Object.keys(expected).map((field) => [field, capability?.[field] ?? null]),
  );
  if (Object.entries(expected).some(([field, value]) => actual[field] !== value)) {
    throw new AdapterError(
      "release_capability_identity_mismatch",
      "bundle capability identity differs from the immutable release lock",
      { expected, actual },
    );
  }
}

function verifyLockedMembers(bundleRoot, artifact, key, lock) {
  const manifest = JSON.parse(fs.readFileSync(path.join(bundleRoot, "manifest.json"), "utf8"));
  if (manifest.platform !== key || manifest.version !== lock.resolvedVersion) {
    throw new AdapterError(
      "release_platform_mismatch",
      "bundle platform or version differs from release lock",
      {
        expected: { platform: key, version: lock.resolvedVersion },
        actual: { platform: manifest.platform ?? null, version: manifest.version ?? null },
      },
    );
  }
  const executable = key.startsWith("win32") ? "jianying.exe" : "jianying";
  const checks = [
    [executable, artifact.binarySha256],
    [manifest.capabilityManifest, artifact.capabilityManifestSha256],
    ["SBOM.spdx.json", artifact.sbomSha256],
  ];
  for (const [relative, expected] of checks) {
    const candidate = path.resolve(bundleRoot, relative);
    if (!candidate.startsWith(`${path.resolve(bundleRoot)}${path.sep}`)
        || !fs.statSync(candidate).isFile() || sha256File(candidate) !== expected.toLowerCase()) {
      throw new AdapterError(
        "release_member_checksum_mismatch",
        `release member does not match the lock: ${relative}`,
      );
    }
  }
  const capability = JSON.parse(
    fs.readFileSync(path.resolve(bundleRoot, manifest.capabilityManifest), "utf8"),
  );
  validateLockedCapabilityIdentity(capability, lock);
}

export async function fetchAndInstall({
  lockPath,
  installRoot,
  action = "install",
  platform = process.platform,
  arch = process.arch,
  fetchImpl = globalThis.fetch,
  tarCommand = process.platform === "win32" ? "tar.exe" : "tar",
}) {
  if (!["install", "upgrade"].includes(action)) {
    throw new AdapterError("usage_error", "fetch action must be install or upgrade");
  }
  if (typeof fetchImpl !== "function") {
    throw new AdapterError("download_unavailable", "this Node runtime does not provide fetch");
  }
  const selected = loadArtifact(path.resolve(lockPath), platform, arch);
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-cli-fetch-"));
  try {
    const archive = path.join(temporary, selected.archiveName);
    await downloadArchive(
      selected.artifact.url,
      archive,
      selected.artifact.archiveSha256,
      fetchImpl,
    );
    const extracted = path.join(temporary, "extracted");
    fs.mkdirSync(extracted);
    const bundleRoot = extractArchive(archive, extracted, tarCommand);
    verifyLockedMembers(bundleRoot, selected.artifact, selected.key, selected.lock);
    const installed = action === "upgrade"
      ? upgradeBundle({ bundleRoot, installRoot })
      : installBundle({ bundleRoot, installRoot });
    return {
      ...installed,
      sourceUrl: selected.artifact.url,
      archiveSha256: selected.artifact.archiveSha256,
      capabilityManifestSha256: selected.artifact.capabilityManifestSha256,
      sbomSha256: selected.artifact.sbomSha256,
    };
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}

function value(argumentsList, flag) {
  const index = argumentsList.indexOf(flag);
  return index >= 0 ? argumentsList[index + 1] : undefined;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const argumentsList = process.argv.slice(2);
    const action = argumentsList[0] ?? "install";
    const lockPath = value(argumentsList, "--lock");
    const installRoot = value(argumentsList, "--install-root");
    if (!lockPath || !installRoot) {
      throw new AdapterError(
        "usage_error",
        "usage: fetch_cli_artifact.mjs install|upgrade --lock FILE --install-root DIR",
      );
    }
    const data = await fetchAndInstall({ lockPath, installRoot, action });
    console.log(JSON.stringify({ ok: true, data }));
  } catch (error) {
    const failure = error instanceof AdapterError
      ? error
      : new AdapterError("artifact_install_failed", error.message ?? String(error));
    console.log(JSON.stringify({ ok: false, error: failure.toJSON() }));
    process.exitCode = 1;
  }
}
