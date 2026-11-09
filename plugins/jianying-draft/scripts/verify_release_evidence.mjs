#!/usr/bin/env node
import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { AdapterError } from "./runtime_adapter.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const EXPECTED_PLATFORMS = new Set(["darwin-arm64", "darwin-x64", "win32-x64"]);
const EXPECTED_READINESS_CHECKS = new Set([
  "plugin.version_matrix",
  "cli.platform_artifacts",
  "cli.immutable_identity",
  "cli.artifact_integrity",
  "skills.immutable_release",
  "skills.content_digests",
  "hosts.release_acceptance",
  "matrix.cli_skill_compatibility",
  "distribution.legal_materials",
  "runtime.legacy_engines_removed",
  "runtime.release_surface_rust_only",
]);
const SHA256 = /^[0-9a-f]{64}$/;
const COMMIT = /^[0-9a-f]{40}$/;

function platformKey(record) {
  return `${record.platform}-${record.arch}`;
}

function sameOrderedStrings(left, right) {
  return Array.isArray(left)
    && Array.isArray(right)
    && left.length === right.length
    && left.every((value, index) => value === right[index]);
}

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

export function verifyReleaseEvidence({
  evidenceRoot,
  lockPath,
  pluginRoot = ROOT,
  allowCutoverPending = false,
  pluginSourceCommit,
}) {
  const resolvedEvidenceRoot = path.resolve(evidenceRoot);
  const resolvedLockPath = path.resolve(lockPath);
  const lock = JSON.parse(fs.readFileSync(resolvedLockPath, "utf8"));
  const skillsLock = JSON.parse(
    fs.readFileSync(path.join(pluginRoot, "skills.lock.json"), "utf8"),
  );
  const skillSource = skillsLock.sources?.length === 1 ? skillsLock.sources[0] : null;
  // 归档与安装证据都包含插件本地技能，
  // 所以期望数 = 上游 vendored + localSkills。
  const localSkillCount = Array.isArray(skillsLock.localSkills) ? skillsLock.localSkills.length : 0;
  const expectedSkillCount = (Array.isArray(skillSource?.skills) ? skillSource.skills.length : 0)
    + localSkillCount;
  if (!lock.releaseRef || !COMMIT.test(lock.sourceCommit ?? "")) {
    throw new AdapterError("release_evidence_lock_invalid", "CLI lock has no immutable release identity");
  }
  const files = fs.readdirSync(resolvedEvidenceRoot)
    .filter((name) => name.endsWith(".json")
      && path.resolve(resolvedEvidenceRoot, name) !== resolvedLockPath)
    .sort();
  const records = files.map((name) => ({
    name,
    value: JSON.parse(fs.readFileSync(path.join(resolvedEvidenceRoot, name), "utf8")),
  }));
  const readiness = records.filter(
    ({ value }) => value.schema === "jianying-plugin-release-readiness/v1",
  );
  const canaries = records.filter(
    ({ value }) => value?.data?.schema === "jianying-plugin-release-install-canary/v1",
  );
  const archiveAudits = records.filter(
    ({ value }) => value?.schema === "jianying-plugin-archive-audit/v1",
  );
  const verifications = records.filter(
    ({ value }) => value?.data?.schema
      === "jianying-plugin-release-evidence-verification/v1",
  );
  const recognized = new Set(
    [...readiness, ...canaries, ...archiveAudits, ...verifications].map(({ name }) => name),
  );
  const unknown = records
    .map(({ name }) => name)
    .filter((name) => !recognized.has(name));
  if (unknown.length > 0 || verifications.length > 1) {
    throw new AdapterError(
      "release_evidence_asset_set_invalid",
      "release evidence contains unexpected JSON evidence assets",
      { unknown, verificationCount: verifications.length },
    );
  }
  if (archiveAudits.length !== 1) {
    throw new AdapterError(
      "release_archive_evidence_incomplete",
      "release evidence requires exactly one plugin archive audit",
      { archiveAuditCount: archiveAudits.length },
    );
  }
  const archiveAudit = archiveAudits[0].value;
  if (archiveAudit.status !== "passed"
      || !Number.isInteger(archiveAudit.fileCount)
      || archiveAudit.fileCount <= 0
      || expectedSkillCount <= 0
      || archiveAudit.skillCount !== expectedSkillCount
      || archiveAudit.rustOnlyRuntime !== true
      || archiveAudit.externalHeadlessRuntime !== false
      || archiveAudit.pythonDraftEngine !== false
      || !SHA256.test(archiveAudit.archiveSha256 ?? "")
      || !COMMIT.test(archiveAudit.pluginSourceCommit ?? "")
      || typeof archiveAudit.archive !== "string"
      || archiveAudit.archive.length === 0) {
    throw new AdapterError(
      "release_archive_evidence_invalid",
      "plugin archive audit does not prove one complete Rust-only distribution",
    );
  }
  if (pluginSourceCommit !== undefined
      && (pluginSourceCommit !== archiveAudit.pluginSourceCommit
        || !COMMIT.test(pluginSourceCommit))) {
    throw new AdapterError(
      "release_archive_identity_mismatch",
      "plugin archive audit source commit differs from the release checkout",
    );
  }
  const archivePath = path.resolve(resolvedEvidenceRoot, archiveAudit.archive);
  if (path.dirname(archivePath) !== resolvedEvidenceRoot
      || !fs.lstatSync(archivePath, { throwIfNoEntry: false })?.isFile()
      || sha256(archivePath) !== archiveAudit.archiveSha256) {
    throw new AdapterError(
      "release_archive_digest_mismatch",
      "plugin archive is missing, escapes the evidence root, or differs from its audit digest",
    );
  }
  const lockInsideEvidence = path.dirname(resolvedLockPath) === resolvedEvidenceRoot
    ? path.basename(resolvedLockPath)
    : null;
  const evidenceFiles = fs.readdirSync(resolvedEvidenceRoot, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name !== lockInsideEvidence)
    .map((entry) => entry.name)
    .sort();
  const recognizedFiles = new Set([...recognized, archiveAudit.archive]);
  const unexpectedFiles = evidenceFiles.filter((name) => !recognizedFiles.has(name));
  if (unexpectedFiles.length > 0) {
    throw new AdapterError(
      "release_evidence_asset_set_invalid",
      "release evidence contains unexpected non-JSON assets",
      { unknown: unexpectedFiles },
    );
  }
  const readinessReport = readiness.length === 1 ? readiness[0].value : null;
  const blocked = Array.isArray(readinessReport?.blocked) ? readinessReport.blocked : [];
  const releaseReady = readinessReport?.ready === true && blocked.length === 0;
  const cutoverPending = allowCutoverPending
    && readinessReport?.ready === false
    && blocked.length === 1
    && blocked[0] === "runtime.release_surface_rust_only";
  if (!releaseReady && !cutoverPending) {
    if (allowCutoverPending && readinessReport !== null) {
      throw new AdapterError(
        "release_readiness_evidence_invalid",
        "cutover evidence may only defer the final Rust-only release surface",
        { blocked },
      );
    }
    throw new AdapterError(
      "release_readiness_evidence_invalid",
      "release evidence requires exactly one all-green readiness report",
    );
  }
  const checks = Array.isArray(readinessReport.checks) ? readinessReport.checks : [];
  const checkIds = checks.map((check) => check?.id);
  const checkMap = new Map(checks.map((check) => [check?.id, check]));
  const plugin = JSON.parse(
    fs.readFileSync(path.join(pluginRoot, ".codex-plugin", "plugin.json"), "utf8"),
  );
  if (archiveAudit.pluginVersion !== plugin.version) {
    throw new AdapterError(
      "release_archive_identity_mismatch",
      "plugin archive version differs from the release manifest",
    );
  }
  const cliEvidence = checkMap.get("cli.immutable_identity")?.evidence;
  const skillEvidence = checkMap.get("skills.immutable_release")?.evidence;
  const readinessValid = (
    checkIds.length === EXPECTED_READINESS_CHECKS.size
    && new Set(checkIds).size === EXPECTED_READINESS_CHECKS.size
    && checkIds.every((id) => EXPECTED_READINESS_CHECKS.has(id))
    && checks.every((check) => check.status === (
      cutoverPending && check.id === "runtime.release_surface_rust_only"
        ? "blocked"
        : "ready"
    ))
    && readinessReport.plugin_version === plugin.version
    && cliEvidence?.version === lock.resolvedVersion
    && cliEvidence?.release_ref === lock.releaseRef
    && cliEvidence?.source_commit === lock.sourceCommit
    && skillSource !== null
    && skillSource.package === "jianying-skills"
    && Array.isArray(skillSource.minimumCapabilities)
    && skillSource.minimumCapabilities.length > 0
    && skillEvidence?.version === skillSource.releaseVersion
    && skillEvidence?.ref === skillSource.ref
    && skillEvidence?.commit === skillSource.sha
  );
  if (!readinessValid) {
    throw new AdapterError(
      "release_readiness_evidence_invalid",
      "readiness report is incomplete or not bound to this release",
    );
  }
  if (canaries.length !== 3) {
    throw new AdapterError(
      "release_canary_evidence_incomplete",
      "release evidence requires exactly three platform canaries",
    );
  }
  const observed = new Set();
  for (const { name, value } of canaries) {
    if (value.ok !== true) {
      throw new AdapterError("release_canary_evidence_invalid", `${name}: canary did not succeed`);
    }
    const canary = value.data;
    const platform = platformKey(canary);
    if (!EXPECTED_PLATFORMS.has(platform) || observed.has(platform)) {
      throw new AdapterError(
        "release_canary_evidence_invalid",
        `${name}: unexpected or duplicate platform ${platform}`,
      );
    }
    observed.add(platform);
    if (canary.releaseRef !== lock.releaseRef || canary.sourceCommit !== lock.sourceCommit) {
      throw new AdapterError(
        "release_canary_identity_mismatch",
        `${name}: canary identity differs from the CLI lock`,
      );
    }
    const digestFields = [
      "archiveSha256",
      "binarySha256",
      "capabilityManifestSha256",
      "sbomSha256",
    ];
    if (digestFields.some((field) => !SHA256.test(canary[field] ?? ""))) {
      throw new AdapterError(
        "release_canary_evidence_invalid",
        `${name}: canary digests are invalid`,
      );
    }
    const artifact = lock.artifacts?.[platform];
    if (!artifact || digestFields.some((field) => canary[field] !== artifact[field])) {
      throw new AdapterError(
        "release_canary_digest_mismatch",
        `${name}: canary artifact digests differ from the CLI lock`,
      );
    }
    if (canary.capabilityManifestMatchesRuntime !== true) {
      throw new AdapterError(
        "release_canary_contract_mismatch",
        `${name}: capability manifest was not proven equal to the binary handshake`,
      );
    }
    if (canary.skillsVersion !== skillSource.releaseVersion
        || canary.skillMinimumCliVersion !== skillSource.minimumCliVersion
        || !sameOrderedStrings(
          canary.skillRequiredCapabilities,
          skillSource.minimumCapabilities,
        )
        || canary.skillCapabilitiesSupported !== true) {
      throw new AdapterError(
        "release_canary_skill_contract_mismatch",
        `${name}: canary does not prove the locked Skills capability contract`,
      );
    }
    if (!Array.isArray(canary.requiredCapabilities)
        || !Array.isArray(lock.requiredCapabilities)
        || canary.requiredCapabilities.length !== lock.requiredCapabilities.length
        || canary.requiredCapabilities.some(
          (capability, index) => capability !== lock.requiredCapabilities[index]
        )) {
      throw new AdapterError(
        "release_canary_contract_mismatch",
        `${name}: canary required capabilities differ from the plugin lock`,
      );
    }
    if (canary.capabilitySchema !== lock.capabilitySchema
        || canary.jobSchema !== lock.jobSchema
        || canary.source !== "installed_fallback"
        || canary.cargoAvailableInHandshakePath !== false) {
      throw new AdapterError(
        "release_canary_contract_mismatch",
        `${name}: canary runtime contract differs from the plugin lock`,
      );
    }
  }
  const platforms = [...observed].sort();
  const baseFiles = [...readiness, ...canaries, ...archiveAudits]
    .map(({ name }) => name)
    .concat(archiveAudit.archive)
    .sort();
  const archiveAuditEvidence = {
    archive: archiveAudit.archive,
    archiveSha256: archiveAudit.archiveSha256,
    fileCount: archiveAudit.fileCount,
    pluginVersion: archiveAudit.pluginVersion,
    pluginSourceCommit: archiveAudit.pluginSourceCommit,
    skillCount: archiveAudit.skillCount,
    rustOnlyRuntime: archiveAudit.rustOnlyRuntime,
  };
  if (verifications.length === 1) {
    const stored = verifications[0].value;
    const expected = {
      schema: "jianying-plugin-release-evidence-verification/v1",
      ready: true,
      releaseRef: lock.releaseRef,
      sourceCommit: lock.sourceCommit,
      skillsVersion: skillSource.releaseVersion,
      skillMinimumCliVersion: skillSource.minimumCliVersion,
      skillRequiredCapabilities: skillSource.minimumCapabilities,
      archiveAudit: archiveAuditEvidence,
      platforms,
      files: baseFiles,
    };
    if (cutoverPending) expected.cutoverPending = true;
    if (stored.ok !== true || JSON.stringify(stored.data) !== JSON.stringify(expected)) {
      throw new AdapterError(
        "release_evidence_verification_stale",
        "verification artifact differs from the current evidence set",
      );
    }
  }
  const result = {
    schema: "jianying-plugin-release-evidence-verification/v1",
    ready: true,
    releaseRef: lock.releaseRef,
    sourceCommit: lock.sourceCommit,
    skillsVersion: skillSource.releaseVersion,
    skillMinimumCliVersion: skillSource.minimumCliVersion,
    skillRequiredCapabilities: skillSource.minimumCapabilities,
    archiveAudit: archiveAuditEvidence,
    platforms,
    files: baseFiles,
  };
  if (cutoverPending) result.cutoverPending = true;
  return result;
}

function value(argumentsList, flag) {
  const index = argumentsList.indexOf(flag);
  return index >= 0 ? argumentsList[index + 1] : undefined;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const argumentsList = process.argv.slice(2);
    const evidenceRoot = value(argumentsList, "--evidence-root");
    const lockPath = value(argumentsList, "--lock");
    const output = value(argumentsList, "--output");
    const pluginSourceCommit = value(argumentsList, "--plugin-source-commit");
    if (!evidenceRoot || !lockPath) {
      throw new AdapterError(
        "usage_error",
        "usage: verify_release_evidence.mjs --evidence-root DIR --lock FILE "
          + "[--plugin-source-commit SHA] [--allow-cutover-pending] [--output FILE]",
      );
    }
    const data = verifyReleaseEvidence({
      evidenceRoot: path.resolve(evidenceRoot),
      lockPath: path.resolve(lockPath),
      allowCutoverPending: argumentsList.includes("--allow-cutover-pending"),
      pluginSourceCommit,
    });
    const rendered = `${JSON.stringify({ ok: true, data })}\n`;
    if (output) fs.writeFileSync(path.resolve(output), rendered, "utf8");
    else process.stdout.write(rendered);
  } catch (error) {
    const failure = error instanceof AdapterError
      ? error
      : new AdapterError("release_evidence_invalid", error.message ?? String(error));
    const rendered = `${JSON.stringify({ ok: false, error: failure.toJSON() })}\n`;
    const output = value(process.argv.slice(2), "--output");
    if (output) fs.writeFileSync(path.resolve(output), rendered, "utf8");
    else process.stdout.write(rendered);
    process.exitCode = 1;
  }
}
