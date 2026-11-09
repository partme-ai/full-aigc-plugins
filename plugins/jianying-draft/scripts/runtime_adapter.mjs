#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const PLUGIN_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export class AdapterError extends Error {
  constructor(code, message, details = {}, recovery = []) {
    super(message);
    this.name = "AdapterError";
    this.code = code;
    this.details = details;
    this.recovery = recovery;
  }

  toJSON() {
    return {
      type: this.code,
      message: this.message,
      details: this.details,
      recovery: this.recovery,
    };
  }
}

export function sha256File(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

export function locateCli(options = {}) {
  const env = options.env ?? process.env;
  const pluginRoot = options.pluginRoot ?? PLUGIN_ROOT;
  const platform = options.platform ?? process.platform;
  const arch = options.arch ?? process.arch;
  const lock = loadLock(pluginRoot);
  const override = env.JIANYING_CLI_PATH;
  if (override) {
    return verifyCandidate(
      path.resolve(override),
      env.JIANYING_CLI_SHA256,
      "development_override",
    );
  }

  const executable = platform === "win32" ? "jianying.exe" : "jianying";
  const artifactKey = `${platform}-${arch}`;
  const supportedPlatforms = new Set(["darwin-arm64", "darwin-x64", "win32-x64"]);
  if (!supportedPlatforms.has(artifactKey)) {
    throw new AdapterError(
      "unsupported_platform",
      `jianying runtime is not distributed for ${artifactKey}`,
      { platform, arch, supported: [...supportedPlatforms] },
      ["use a supported macOS or Windows host", "do not build from source during plugin execution"],
    );
  }
  const bundled = path.join(pluginRoot, "bin", artifactKey, executable);
  if (isFile(bundled)) {
    return verifyCandidate(
      bundled,
      lock.artifacts?.[artifactKey]?.sha256,
      "bundled_artifact",
    );
  }

  const installRoot = resolveInstallRoot(env, platform);
  const installedFallback = path.join(installRoot, artifactKey, executable);
  if (isFile(installedFallback)) {
    const checksumPath = path.join(path.dirname(installedFallback), `${executable}.sha256`);
    return verifyCandidate(
      installedFallback,
      readChecksum(checksumPath),
      "installed_fallback",
    );
  }

  const installed = findOnPath(executable, env);
  if (installed) {
    return verifyCandidate(installed, env.JIANYING_CLI_SHA256, "installed_path");
  }
  throw new AdapterError(
    "cli_not_found",
    `jianying CLI is not available for ${artifactKey}`,
    { platform, arch },
    [
      "install a verified jianying-cli artifact",
      "for development set JIANYING_CLI_PATH and JIANYING_CLI_SHA256",
    ],
  );
}

function resolveInstallRoot(env, platform) {
  if (env.JIANYING_CLI_INSTALL_ROOT) return path.resolve(env.JIANYING_CLI_INSTALL_ROOT);
  const home = env.HOME || env.USERPROFILE || os.homedir();
  if (platform === "darwin") {
    return path.join(home, "Library", "Application Support", "PartMe", "jianying-draft", "runtime");
  }
  if (platform === "win32") {
    const localAppData = env.LOCALAPPDATA || path.join(home, "AppData", "Local");
    return path.join(localAppData, "PartMe", "jianying-draft", "runtime");
  }
  return path.join(env.XDG_DATA_HOME || path.join(home, ".local", "share"), "partme", "jianying-draft", "runtime");
}

function readChecksum(checksumPath) {
  try {
    const token = fs.readFileSync(checksumPath, "utf8").trim().split(/\s+/)[0];
    return token;
  } catch {
    return undefined;
  }
}

export function handshake(options = {}) {
  const pluginRoot = options.pluginRoot ?? PLUGIN_ROOT;
  const lock = loadLock(pluginRoot);
  const located = locateCli({ ...options, pluginRoot });
  const versionResult = spawn(located.path, ["--version"], options.env);
  if (versionResult.exitCode !== 0) {
    throw new AdapterError(
      "version_probe_failed",
      "jianying --version failed",
      { exitCode: versionResult.exitCode, stderr: versionResult.stderr },
      ["run the verified CLI manually with --version"],
    );
  }
  const version = parseVersion(versionResult.stdout);
  if (compareVersions(version, lock.minimumVersion) < 0) {
    throw new AdapterError(
      "version_too_old",
      `jianying CLI ${version} is older than ${lock.minimumVersion}`,
      { actual: version, minimum: lock.minimumVersion },
      [`upgrade jianying-cli to ${lock.minimumVersion} or newer`],
    );
  }

  const capabilities = invokeJson(located.path, ["capabilities", "--json"], options.env);
  if (capabilities.exitCode !== 0 || capabilities.envelope?.ok !== true) {
    throw new AdapterError(
      "capability_probe_failed",
      "jianying capabilities --json failed",
      {
        exitCode: capabilities.exitCode,
        stderr: capabilities.stderr,
        response: capabilities.envelope,
      },
      ["run jianying capabilities --json and inspect its structured error"],
    );
  }
  const manifest = capabilities.envelope.data;
  if (manifest?.schema !== lock.capabilitySchema) {
    throw new AdapterError(
      "schema_incompatible",
      `capability schema ${manifest?.schema ?? "missing"} is not supported`,
      { actual: manifest?.schema ?? null, expected: lock.capabilitySchema },
      [`install a CLI exposing ${lock.capabilitySchema}`],
    );
  }
  if (manifest.cli_version !== version) {
    throw new AdapterError(
      "version_mismatch",
      "--version and capability manifest report different CLI versions",
      { executableVersion: version, manifestVersion: manifest.cli_version ?? null },
      ["replace the CLI with an internally consistent verified artifact"],
    );
  }
  requireCapabilities(manifest, lock.requiredCapabilities, lock.minimumVersion);
  return {
    ready: true,
    path: located.path,
    source: located.source,
    sha256: located.sha256,
    version,
    capabilitySchema: lock.capabilitySchema,
    jobSchema: lock.jobSchema,
    requiredCapabilities: [...lock.requiredCapabilities],
    manifest,
  };
}

export function runJob({ jobPath, outputPath, env = process.env, pluginRoot = PLUGIN_ROOT }) {
  const ready = handshake({ env, pluginRoot });
  const absoluteJobPath = path.resolve(jobPath);
  let operation;
  try {
    operation = JSON.parse(fs.readFileSync(absoluteJobPath, "utf8")).operation;
  } catch (error) {
    throw new AdapterError(
      "job_invalid",
      `cannot read Job v2 document: ${error.message}`,
      { jobPath: absoluteJobPath },
    );
  }
  const args = ["job", "run", absoluteJobPath];
  if (outputPath && ["create", "batch"].includes(operation)) {
    args.push("--out", path.resolve(outputPath));
  }
  args.push("--json");
  const invocation = invokeJson(ready.path, args, env);
  const error = invocation.envelope?.ok === false ? invocation.envelope.error : null;
  const taskId = invocation.envelope?.data?.task_id
    ?? error?.details?.task_id
    ?? null;
  return {
    ...invocation,
    taskId,
    error,
    recovery: error?.recovery ?? [],
  };
}

export function runJsonCommand({
  args,
  requiredCapabilities = [],
  env = process.env,
  pluginRoot = PLUGIN_ROOT,
}) {
  const ready = handshake({ env, pluginRoot });
  requireCapabilities(ready.manifest, requiredCapabilities, ready.version);
  const invocation = invokeJson(ready.path, [...args, "--json"], env);
  return { ...invocation, ready };
}

export function requireCapabilities(manifest, requiredCapabilities, minimumVersion = null) {
  const supported = new Set(
    (manifest?.capabilities ?? [])
      .filter((entry) => entry.status === "supported")
      .map((entry) => entry.id),
  );
  for (const capability of requiredCapabilities) {
    if (!supported.has(capability)) {
      throw new AdapterError(
        "missing_capability",
        `required capability ${capability} is not supported`,
        { capability, minimumVersion },
        [
          `install a compatible CLI with ${capability}`,
          "do not fall back to Python or an external headless checkout",
        ],
      );
    }
  }
}

function verifyCandidate(candidate, expectedSha256, source) {
  if (!isFile(candidate)) {
    throw new AdapterError(
      "cli_not_found",
      `jianying CLI does not exist at ${candidate}`,
      { path: candidate, source },
      ["correct the configured CLI path"],
    );
  }
  if (!expectedSha256 || !/^[a-f0-9]{64}$/i.test(expectedSha256)) {
    throw new AdapterError(
      "checksum_required",
      `no valid SHA-256 is configured for ${candidate}`,
      { path: candidate, source },
      ["set JIANYING_CLI_SHA256 or install an artifact listed in the CLI lock"],
    );
  }
  const actual = sha256File(candidate);
  if (actual.toLowerCase() !== expectedSha256.toLowerCase()) {
    throw new AdapterError(
      "checksum_mismatch",
      `jianying CLI checksum does not match for ${candidate}`,
      { path: candidate, expected: expectedSha256, actual },
      ["replace the CLI with the verified artifact; do not execute this file"],
    );
  }
  return { path: candidate, source, sha256: actual };
}

function loadLock(pluginRoot) {
  const lockPath = path.join(pluginRoot, "runtime", "jianying-cli.lock.json");
  try {
    return JSON.parse(fs.readFileSync(lockPath, "utf8"));
  } catch (error) {
    throw new AdapterError(
      "lock_invalid",
      `cannot read CLI lock: ${error.message}`,
      { path: lockPath },
      ["restore runtime/jianying-cli.lock.json from the plugin release"],
    );
  }
}

function findOnPath(executable, env) {
  const pathValue = env.PATH ?? "";
  for (const directory of pathValue.split(path.delimiter).filter(Boolean)) {
    const candidate = path.join(directory, executable);
    if (isFile(candidate)) return candidate;
  }
  return null;
}

function isFile(candidate) {
  try {
    return fs.statSync(candidate).isFile();
  } catch {
    return false;
  }
}

function spawn(executable, args, env = process.env) {
  const result = spawnSync(executable, args, {
    encoding: "utf8",
    env: { ...process.env, ...env },
    maxBuffer: 16 * 1024 * 1024,
  });
  if (result.error) {
    throw new AdapterError(
      "cli_spawn_failed",
      result.error.message,
      { executable, args },
      ["verify that the CLI is executable on this platform"],
    );
  }
  return {
    exitCode: result.status ?? 1,
    stdout: result.stdout ?? "",
    stderr: result.stderr ?? "",
  };
}

function invokeJson(executable, args, env) {
  const result = spawn(executable, args, env);
  let envelope;
  try {
    envelope = JSON.parse(result.stdout.trim());
  } catch (error) {
    throw new AdapterError(
      "invalid_json_response",
      `CLI stdout is not one JSON document: ${error.message}`,
      { exitCode: result.exitCode, stdout: result.stdout, stderr: result.stderr },
      ["rerun the CLI with --json and verify stdout contains only the envelope"],
    );
  }
  return { ...result, envelope };
}

function parseVersion(output) {
  const match = output.trim().match(/(?:^|\s)(\d+\.\d+\.\d+)(?:\s|$)/);
  if (!match) {
    throw new AdapterError(
      "version_invalid",
      `cannot parse CLI version from ${JSON.stringify(output.trim())}`,
      { output },
      ["install a standard jianying-cli release artifact"],
    );
  }
  return match[1];
}

function compareVersions(left, right) {
  const a = left.split(".").map(Number);
  const b = right.split(".").map(Number);
  for (let index = 0; index < 3; index += 1) {
    if (a[index] !== b[index]) return a[index] < b[index] ? -1 : 1;
  }
  return 0;
}

async function main() {
  const [command, ...args] = process.argv.slice(2);
  if (command === "handshake" || command === "doctor") {
    console.log(JSON.stringify({ ok: true, data: handshake() }));
    return;
  }
  if (command === "job" && args[0] === "run" && args[1]) {
    const outIndex = args.indexOf("--out");
    const result = runJob({
      jobPath: args[1],
      outputPath: outIndex >= 0 ? args[outIndex + 1] : undefined,
    });
    console.log(JSON.stringify(result.envelope));
    process.exitCode = result.exitCode;
    return;
  }
  if (command === "run" && args.length > 0) {
    const requiredCapabilities = [];
    const invocationArgs = [];
    for (let index = 0; index < args.length; index += 1) {
      if (args[index] === "--require") {
        if (!args[index + 1]) throw new AdapterError("usage_error", "--require needs a capability ID");
        requiredCapabilities.push(args[index + 1]);
        index += 1;
      } else {
        invocationArgs.push(args[index]);
      }
    }
    const result = runJsonCommand({ args: invocationArgs, requiredCapabilities });
    console.log(JSON.stringify(result.envelope));
    process.exitCode = result.exitCode;
    return;
  }
  throw new AdapterError(
    "usage_error",
    "usage: runtime_adapter.mjs handshake|doctor|job run JOB [--out DIR]|run COMMAND... [--require CAPABILITY]",
  );
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    const adapterError = error instanceof AdapterError
      ? error
      : new AdapterError("adapter_failed", error.message ?? String(error));
    console.log(JSON.stringify({ ok: false, error: adapterError.toJSON() }));
    process.exitCode = 1;
  });
}
