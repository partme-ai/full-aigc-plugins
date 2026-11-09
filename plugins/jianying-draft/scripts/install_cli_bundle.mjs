#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { AdapterError } from "./runtime_adapter.mjs";

const SUPPORTED_PLATFORMS = new Set(["darwin-arm64", "darwin-x64", "win32-x64"]);
const REQUIRED_CONTRACT_MEMBERS = [
  "LICENSE",
  "THIRD_PARTY_NOTICES.md",
  "SBOM.spdx.json",
  "schemas/jianying-job-v2.schema.json",
];

function sha256File(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function readManifest(bundleRoot) {
  const manifestPath = path.join(bundleRoot, "manifest.json");
  try {
    return JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  } catch (error) {
    throw new AdapterError(
      "release_manifest_invalid",
      `cannot read release manifest: ${error.message}`,
      { path: manifestPath },
      ["download and extract the release artifact again"],
    );
  }
}

function resolveMember(bundleRoot, relative) {
  if (typeof relative !== "string" || relative.length === 0 || path.isAbsolute(relative)) {
    throw new AdapterError("release_path_invalid", "release manifest contains an invalid path", { path: relative });
  }
  const resolved = path.resolve(bundleRoot, relative);
  const prefix = `${path.resolve(bundleRoot)}${path.sep}`;
  if (!resolved.startsWith(prefix)) {
    throw new AdapterError("release_path_invalid", "release manifest path escapes the bundle", { path: relative });
  }
  return resolved;
}

function readContractJson(file, label) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (error) {
    throw new AdapterError(
      "release_contract_invalid",
      `${label} is not valid JSON: ${error.message}`,
      { path: file, label },
    );
  }
}

function verifyBundle(bundleRoot) {
  const sourceRoot = path.resolve(bundleRoot);
  const manifest = readManifest(sourceRoot);
  if (manifest.schema !== "jianying-cli-release/v1") {
    throw new AdapterError(
      "release_schema_incompatible",
      `unsupported release schema ${manifest.schema ?? "missing"}`,
      { expected: "jianying-cli-release/v1", actual: manifest.schema ?? null },
    );
  }
  if (!SUPPORTED_PLATFORMS.has(manifest.platform)) {
    throw new AdapterError(
      "release_platform_unsupported",
      `unsupported release platform ${manifest.platform ?? "missing"}`,
      { supported: [...SUPPORTED_PLATFORMS] },
    );
  }
  if (!Array.isArray(manifest.files) || manifest.files.length === 0) {
    throw new AdapterError("release_manifest_invalid", "release manifest has no files");
  }
  const declared = new Map();
  for (const entry of manifest.files) {
    if (declared.has(entry.path)) {
      throw new AdapterError(
        "release_manifest_invalid",
        `release manifest declares a duplicate path: ${entry.path}`,
      );
    }
    const source = resolveMember(sourceRoot, entry.path);
    let stat;
    try {
      stat = fs.statSync(source);
    } catch {
      stat = null;
    }
    if (!stat?.isFile()) {
      throw new AdapterError("release_file_missing", `release file is missing: ${entry.path}`);
    }
    const actual = sha256File(source);
    if (!/^[a-f0-9]{64}$/i.test(entry.sha256) || actual !== entry.sha256.toLowerCase()) {
      throw new AdapterError(
        "release_checksum_mismatch",
        `release checksum mismatch: ${entry.path}`,
        { expected: entry.sha256 ?? null, actual },
      );
    }
    if (Number(entry.size) !== stat.size) {
      throw new AdapterError("release_size_mismatch", `release size mismatch: ${entry.path}`);
    }
    declared.set(entry.path, { source, sha256: actual });
  }
  const executable = manifest.platform.startsWith("win32") ? "jianying.exe" : "jianying";
  const binary = declared.get(executable);
  const missing = [
    executable,
    manifest.capabilityManifest,
    ...REQUIRED_CONTRACT_MEMBERS,
  ].filter((relative) => typeof relative !== "string" || !declared.has(relative));
  if (!binary || missing.length > 0) {
    throw new AdapterError(
      "release_contract_incomplete",
      "release must declare its executable, schema, capability, SBOM and license materials",
      { executable, capabilityManifest: manifest.capabilityManifest ?? null, missing },
    );
  }
  const capability = readContractJson(
    declared.get(manifest.capabilityManifest).source,
    "capability manifest",
  );
  if (capability.schema !== "jianying-capabilities/v1") {
    throw new AdapterError(
      "release_contract_invalid",
      "release capability manifest schema is incompatible",
      { actual: capability.schema ?? null, expected: "jianying-capabilities/v1" },
    );
  }
  const jobSchema = readContractJson(
    declared.get("schemas/jianying-job-v2.schema.json").source,
    "jianying-job/v2 schema",
  );
  if (jobSchema["$schema"] !== "https://json-schema.org/draft/2020-12/schema"
      || !jobSchema["$id"]?.endsWith("/jianying-job-v2.schema.json")
      || !["schema", "operation"].every((field) => jobSchema.required?.includes(field))) {
    throw new AdapterError(
      "release_contract_invalid",
      "release does not contain the expected jianying-job/v2 JSON Schema",
    );
  }
  const sbom = readContractJson(declared.get("SBOM.spdx.json").source, "SPDX SBOM");
  if (sbom.spdxVersion !== "SPDX-2.3" || sbom.dataLicense !== "CC0-1.0"
      || !Array.isArray(sbom.packages) || sbom.packages.length === 0
      || sbom.packages.some((item) => !item.licenseDeclared || item.licenseDeclared === "NOASSERTION")) {
    throw new AdapterError(
      "release_contract_invalid",
      "release SBOM must be SPDX-2.3 and declare package licenses",
    );
  }
  return { sourceRoot, manifest, declared, executable, binary };
}

function writeInstallation(verified, destinationRoot) {
  const { manifest, declared, executable, binary } = verified;
  fs.mkdirSync(destinationRoot, { recursive: true });
  const destination = path.join(destinationRoot, manifest.platform);
  if (fs.existsSync(destination)) {
    throw new AdapterError(
      "install_exists",
      `runtime already exists at ${destination}`,
      { destination },
      ["use the explicit upgrade or rollback flow; do not overwrite an active runtime"],
    );
  }
  const staging = path.join(destinationRoot, `.${manifest.platform}-${process.pid}.staging`);
  try {
    fs.mkdirSync(staging);
    for (const [relative, entry] of declared) {
      const target = resolveMember(staging, relative);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.copyFileSync(entry.source, target);
    }
    if (!manifest.platform.startsWith("win32")) fs.chmodSync(path.join(staging, executable), 0o755);
    fs.writeFileSync(
      path.join(staging, `${executable}.sha256`),
      `${binary.sha256}  ${executable}\n`,
      "utf8",
    );
    fs.renameSync(staging, destination);
  } catch (error) {
    fs.rmSync(staging, { recursive: true, force: true });
    if (error instanceof AdapterError) throw error;
    throw new AdapterError("install_failed", error.message, { destination });
  }
  return {
    schema: manifest.schema,
    version: manifest.version,
    platform: manifest.platform,
    destination,
    executable: path.join(destination, executable),
    capabilityManifest: path.join(destination, manifest.capabilityManifest),
    sha256: binary.sha256,
  };
}

export function installBundle({ bundleRoot, installRoot }) {
  return writeInstallation(verifyBundle(bundleRoot), path.resolve(installRoot));
}

function installedChecksum(destination, executable) {
  const checksumFile = path.join(destination, `${executable}.sha256`);
  const checksum = fs.readFileSync(checksumFile, "utf8").trim().split(/\s+/)[0];
  if (!/^[a-f0-9]{64}$/i.test(checksum)) {
    throw new AdapterError("installed_checksum_invalid", `invalid installed checksum at ${checksumFile}`);
  }
  return checksum.toLowerCase();
}

export function upgradeBundle({ bundleRoot, installRoot }) {
  const verified = verifyBundle(bundleRoot);
  const destinationRoot = path.resolve(installRoot);
  const destination = path.join(destinationRoot, verified.manifest.platform);
  if (!fs.existsSync(destination)) return installBundle({ bundleRoot, installRoot });
  const previousSha256 = installedChecksum(destination, verified.executable);
  const rollback = path.join(
    destinationRoot,
    ".rollback",
    verified.manifest.platform,
    previousSha256,
  );
  if (fs.existsSync(rollback)) {
    throw new AdapterError("rollback_exists", `rollback slot already exists at ${rollback}`);
  }
  fs.mkdirSync(path.dirname(rollback), { recursive: true });
  fs.renameSync(destination, rollback);
  try {
    const installed = writeInstallation(verified, destinationRoot);
    return { ...installed, previousSha256, rollback };
  } catch (error) {
    if (!fs.existsSync(destination) && fs.existsSync(rollback)) fs.renameSync(rollback, destination);
    throw error;
  }
}

export function rollbackBundle({ installRoot, platform, sha256 }) {
  if (!SUPPORTED_PLATFORMS.has(platform) || !/^[a-f0-9]{64}$/i.test(sha256)) {
    throw new AdapterError("rollback_target_invalid", "rollback requires a supported platform and SHA-256");
  }
  const destinationRoot = path.resolve(installRoot);
  const executable = platform.startsWith("win32") ? "jianying.exe" : "jianying";
  const destination = path.join(destinationRoot, platform);
  const rollback = path.join(destinationRoot, ".rollback", platform, sha256.toLowerCase());
  if (!fs.existsSync(destination) || !fs.existsSync(rollback)) {
    throw new AdapterError(
      "rollback_not_found",
      "active runtime or requested rollback slot is missing",
      { destination, rollback },
    );
  }
  const currentSha256 = installedChecksum(destination, executable);
  const swap = path.join(destinationRoot, `.rollback-swap-${platform}-${process.pid}`);
  fs.renameSync(destination, swap);
  try {
    fs.renameSync(rollback, destination);
    fs.renameSync(swap, path.join(destinationRoot, ".rollback", platform, currentSha256));
  } catch (error) {
    if (!fs.existsSync(destination) && fs.existsSync(swap)) fs.renameSync(swap, destination);
    throw new AdapterError("rollback_failed", error.message, { destination, rollback });
  }
  return {
    platform,
    destination,
    restoredSha256: installedChecksum(destination, executable),
    previousSha256: currentSha256,
  };
}

function parseArguments(args) {
  const value = (flag) => {
    const index = args.indexOf(flag);
    return index >= 0 ? args[index + 1] : undefined;
  };
  return {
    action: args[0]?.startsWith("--") ? "install" : (args[0] ?? "install"),
    bundleRoot: value("--bundle"),
    installRoot: value("--install-root"),
    platform: value("--platform"),
    sha256: value("--sha256"),
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const options = parseArguments(process.argv.slice(2));
    if (!options.installRoot) {
      throw new AdapterError(
        "usage_error",
        "usage: install_cli_bundle.mjs install|upgrade --bundle DIR --install-root DIR | rollback --install-root DIR --platform PLATFORM --sha256 SHA256",
      );
    }
    let data;
    if (options.action === "rollback") {
      if (!options.platform || !options.sha256) throw new AdapterError("usage_error", "rollback target is required");
      data = rollbackBundle(options);
    } else if (options.action === "install" || options.action === "upgrade") {
      if (!options.bundleRoot) throw new AdapterError("usage_error", "release bundle is required");
      data = options.action === "upgrade" ? upgradeBundle(options) : installBundle(options);
    } else {
      throw new AdapterError("usage_error", `unknown install action ${options.action}`);
    }
    console.log(JSON.stringify({ ok: true, data }));
  } catch (error) {
    const failure = error instanceof AdapterError
      ? error
      : new AdapterError("install_failed", error.message ?? String(error));
    console.log(JSON.stringify({ ok: false, error: failure.toJSON() }));
    process.exitCode = 1;
  }
}
