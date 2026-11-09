#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { isDeepStrictEqual } from "node:util";
import { fileURLToPath } from "node:url";

import { fetchAndInstall } from "./fetch_cli_artifact.mjs";
import { AdapterError, handshake } from "./runtime_adapter.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

function value(argumentsList, flag) {
  const index = argumentsList.indexOf(flag);
  return index >= 0 ? argumentsList[index + 1] : undefined;
}

export function validateInstalledCapabilityManifest(runtimeManifest, packagedManifest) {
  if (!isDeepStrictEqual(runtimeManifest, packagedManifest)) {
    throw new AdapterError(
      "release_capability_manifest_mismatch",
      "installed binary capability handshake differs from its packaged manifest",
    );
  }
}

function parseVersion(version, field) {
  const match = typeof version === "string" ? version.match(SEMVER) : null;
  if (!match) {
    throw new AdapterError(
      "skill_capability_contract_invalid",
      `${field} must be a stable semantic version`,
      { field, value: version ?? null },
    );
  }
  return match.slice(1).map(Number);
}

function compareVersions(left, right) {
  for (let index = 0; index < 3; index += 1) {
    if (left[index] !== right[index]) return left[index] < right[index] ? -1 : 1;
  }
  return 0;
}

export function validateSkillCapabilityContract(runtimeManifest, skillsLock) {
  const source = skillsLock?.version === 1
    && Array.isArray(skillsLock.sources)
    && skillsLock.sources.length === 1
    ? skillsLock.sources[0]
    : null;
  if (!source || source.package !== "jianying-skills") {
    throw new AdapterError(
      "skill_capability_contract_invalid",
      "skills.lock.json must contain exactly one jianying-skills source",
    );
  }

  parseVersion(source.releaseVersion, "skills.releaseVersion");
  const minimumVersion = parseVersion(source.minimumCliVersion, "skills.minimumCliVersion");
  const runtimeVersion = parseVersion(runtimeManifest?.cli_version, "runtime.cli_version");
  const requiredCapabilities = source.minimumCapabilities;
  if (!Array.isArray(requiredCapabilities)
      || requiredCapabilities.length === 0
      || requiredCapabilities.some((capability) => (
        typeof capability !== "string" || capability.length === 0
      ))
      || new Set(requiredCapabilities).size !== requiredCapabilities.length) {
    throw new AdapterError(
      "skill_capability_contract_invalid",
      "jianying-skills minimumCapabilities must be a non-empty unique string array",
    );
  }

  const capabilityEntries = runtimeManifest?.capabilities;
  if (!Array.isArray(capabilityEntries)) {
    throw new AdapterError(
      "skill_capability_contract_invalid",
      "installed runtime manifest has no capability array",
    );
  }
  const capabilityMap = new Map();
  for (const entry of capabilityEntries) {
    if (typeof entry?.id !== "string" || capabilityMap.has(entry.id)) {
      throw new AdapterError(
        "skill_capability_contract_invalid",
        "installed runtime manifest capability IDs must be unique strings",
      );
    }
    capabilityMap.set(entry.id, entry.status);
  }

  const unsupported = requiredCapabilities
    .map((id) => ({ id, status: capabilityMap.get(id) ?? "missing" }))
    .filter(({ status }) => status !== "supported");
  const versionCompatible = compareVersions(runtimeVersion, minimumVersion) >= 0;
  if (!versionCompatible || unsupported.length > 0) {
    throw new AdapterError(
      "skill_capability_contract_incomplete",
      "installed CLI does not satisfy the locked jianying-skills runtime contract",
      {
        skillsVersion: source.releaseVersion,
        minimumCliVersion: source.minimumCliVersion,
        runtimeCliVersion: runtimeManifest.cli_version,
        versionCompatible,
        unsupported,
      },
      ["install a released CLI that supports every capability required by the locked skills"],
    );
  }

  return {
    skillsVersion: source.releaseVersion,
    minimumCliVersion: source.minimumCliVersion,
    requiredCapabilities: [...requiredCapabilities],
  };
}

export async function runReleaseInstallCanary({ lockPath, installRoot }) {
  const lock = JSON.parse(fs.readFileSync(lockPath, "utf8"));
  const installed = await fetchAndInstall({ lockPath, installRoot });
  const restrictedPath = process.platform === "win32"
    ? [process.env.SystemRoot, path.join(process.env.SystemRoot ?? "C:\\Windows", "System32")]
      .filter(Boolean).join(";")
    : "/usr/bin:/bin";
  const env = {
    ...process.env,
    HOME: installRoot,
    USERPROFILE: installRoot,
    PATH: restrictedPath,
    JIANYING_CLI_INSTALL_ROOT: installRoot,
  };
  const ready = handshake({ env, pluginRoot: ROOT });
  if (!ready.ready || ready.source !== "installed_fallback") {
    throw new AdapterError(
      "release_canary_not_ready",
      "fresh release install did not become the checksum-pinned fallback runtime",
    );
  }
  if (ready.manifest?.contract_state !== "released"
      || ready.manifest?.release_ref !== lock.releaseRef
      || ready.manifest?.source_commit !== lock.sourceCommit) {
    throw new AdapterError(
      "release_identity_mismatch",
      "installed binary handshake differs from the immutable release lock",
      {
        expected: {
          releaseRef: lock.releaseRef,
          sourceCommit: lock.sourceCommit,
          contractState: "released",
        },
        actual: {
          releaseRef: ready.manifest?.release_ref ?? null,
          sourceCommit: ready.manifest?.source_commit ?? null,
          contractState: ready.manifest?.contract_state ?? null,
        },
      },
    );
  }
  let packagedManifest;
  try {
    packagedManifest = JSON.parse(fs.readFileSync(installed.capabilityManifest, "utf8"));
  } catch (error) {
    throw new AdapterError(
      "release_capability_manifest_invalid",
      `installed capability manifest cannot be read: ${error.message}`,
      { path: installed.capabilityManifest },
    );
  }
  validateInstalledCapabilityManifest(ready.manifest, packagedManifest);
  let skillsLock;
  try {
    skillsLock = JSON.parse(fs.readFileSync(path.join(ROOT, "skills.lock.json"), "utf8"));
  } catch (error) {
    throw new AdapterError(
      "skill_capability_contract_invalid",
      `cannot read skills.lock.json: ${error.message}`,
    );
  }
  const skillContract = validateSkillCapabilityContract(ready.manifest, skillsLock);
  return {
    schema: "jianying-plugin-release-install-canary/v1",
    platform: process.platform,
    arch: process.arch,
    releaseRef: lock.releaseRef,
    sourceCommit: lock.sourceCommit,
    archiveSha256: installed.archiveSha256,
    binarySha256: ready.sha256,
    capabilityManifestSha256: installed.capabilityManifestSha256,
    sbomSha256: installed.sbomSha256,
    capabilityManifestMatchesRuntime: true,
    skillsVersion: skillContract.skillsVersion,
    skillMinimumCliVersion: skillContract.minimumCliVersion,
    skillRequiredCapabilities: skillContract.requiredCapabilities,
    skillCapabilitiesSupported: true,
    capabilitySchema: ready.capabilitySchema,
    jobSchema: ready.jobSchema,
    requiredCapabilities: ready.requiredCapabilities,
    source: ready.source,
    cargoAvailableInHandshakePath: false,
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const argumentsList = process.argv.slice(2);
  const lockPath = value(argumentsList, "--lock");
  const installRoot = value(argumentsList, "--install-root");
  const output = value(argumentsList, "--output");
  try {
    if (!lockPath || !installRoot) {
      throw new AdapterError(
        "usage_error",
        "usage: release_install_canary.mjs --lock FILE --install-root DIR [--output FILE]",
      );
    }
    const data = await runReleaseInstallCanary({
      lockPath: path.resolve(lockPath),
      installRoot: path.resolve(installRoot),
    });
    const rendered = `${JSON.stringify({ ok: true, data })}\n`;
    if (output) fs.writeFileSync(path.resolve(output), rendered);
    else process.stdout.write(rendered);
  } catch (error) {
    const failure = error instanceof AdapterError
      ? error
      : new AdapterError("release_canary_failed", error.message ?? String(error));
    const rendered = `${JSON.stringify({ ok: false, error: failure.toJSON() })}\n`;
    if (output) fs.writeFileSync(path.resolve(output), rendered);
    else process.stdout.write(rendered);
    process.exitCode = 1;
  }
}
