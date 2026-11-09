import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { verifyReleaseEvidence } from "../scripts/verify_release_evidence.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const releaseRef = "v1.6.0";
const sourceCommit = "a".repeat(40);
const readinessChecks = [
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
];

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-release-evidence-"));
  const lockPath = path.join(root, "lock.json");
  const requiredCapabilities = ["capabilities", "schema.job_v2", "job.run"];
  const artifacts = Object.fromEntries([
    "darwin-arm64",
    "darwin-x64",
    "win32-x64",
  ].map((platform) => [platform, {
    archiveSha256: "1".repeat(64),
    binarySha256: "2".repeat(64),
    capabilityManifestSha256: "3".repeat(64),
    sbomSha256: "4".repeat(64),
  }]));
  fs.writeFileSync(lockPath, JSON.stringify({
    resolvedVersion: "1.6.0",
    releaseRef,
    sourceCommit,
    capabilitySchema: "jianying-capabilities/v1",
    jobSchema: "jianying-job/v2",
    requiredCapabilities,
    artifacts,
  }));
  const pluginVersion = JSON.parse(
    fs.readFileSync(path.join(ROOT, ".codex-plugin", "plugin.json"), "utf8"),
  ).version;
  const skillsLock = JSON.parse(
    fs.readFileSync(path.join(ROOT, "skills.lock.json"), "utf8"),
  );
  const skillSource = skillsLock.sources[0];
  const archiveName = "jianying-draft-plugin-source.tar.gz";
  const archivePath = path.join(root, archiveName);
  fs.writeFileSync(archivePath, "audited plugin archive fixture");
  const archiveSha256 = crypto.createHash("sha256")
    .update(fs.readFileSync(archivePath))
    .digest("hex");
  const checks = readinessChecks.map((id) => ({ id, status: "ready", evidence: [] }));
  checks.find((check) => check.id === "cli.immutable_identity").evidence = {
    version: "1.6.0",
    release_ref: releaseRef,
    source_commit: sourceCommit,
  };
  checks.find((check) => check.id === "skills.immutable_release").evidence = {
    version: skillSource.releaseVersion,
    ref: skillSource.ref,
    commit: skillSource.sha,
  };
  fs.writeFileSync(path.join(root, "readiness.json"), JSON.stringify({
    schema: "jianying-plugin-release-readiness/v1",
    ready: true,
    plugin_version: pluginVersion,
    checks,
    blocked: [],
  }));
  fs.writeFileSync(path.join(root, "plugin-archive-audit.json"), JSON.stringify({
    schema: "jianying-plugin-archive-audit/v1",
    status: "passed",
    archive: archiveName,
    archiveSha256,
    pluginVersion,
    pluginSourceCommit: sourceCommit,
    fileCount: 212,
    // 归档技能数 = vendored + localSkills
  skillCount: skillSource.skills.length + (skillsLock.localSkills?.length ?? 0),
    rustOnlyRuntime: true,
    externalHeadlessRuntime: false,
    pythonDraftEngine: false,
  }));
  for (const [platform, arch] of [
    ["darwin", "arm64"],
    ["darwin", "x64"],
    ["win32", "x64"],
  ]) {
    fs.writeFileSync(path.join(root, `canary-${platform}-${arch}.json`), JSON.stringify({
      ok: true,
      data: {
        schema: "jianying-plugin-release-install-canary/v1",
        platform,
        arch,
        releaseRef,
        sourceCommit,
        archiveSha256: "1".repeat(64),
        binarySha256: "2".repeat(64),
        capabilityManifestSha256: "3".repeat(64),
        sbomSha256: "4".repeat(64),
        capabilityManifestMatchesRuntime: true,
        skillsVersion: skillSource.releaseVersion,
        skillMinimumCliVersion: skillSource.minimumCliVersion,
        skillRequiredCapabilities: skillSource.minimumCapabilities,
        skillCapabilitiesSupported: true,
        capabilitySchema: "jianying-capabilities/v1",
        jobSchema: "jianying-job/v2",
        requiredCapabilities,
        source: "installed_fallback",
        cargoAvailableInHandshakePath: false,
      },
    }));
  }
  return { root, lockPath };
}

test("accepts one all-green readiness report and three unique release canaries", () => {
  const paths = fixture();
  try {
    const result = verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath });
    assert.equal(result.ready, true);
    assert.deepEqual(result.platforms, ["darwin-arm64", "darwin-x64", "win32-x64"]);
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("CLI writes one reusable verification artifact for workflow dispatch", () => {
  const paths = fixture();
  try {
    const output = path.join(paths.root, "verification.json");
    const result = spawnSync(process.execPath, [
      path.join(ROOT, "scripts", "verify_release_evidence.mjs"),
      "--evidence-root",
      paths.root,
      "--lock",
      paths.lockPath,
      "--output",
      output,
    ], { encoding: "utf8" });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout, "");
    const record = JSON.parse(fs.readFileSync(output, "utf8"));
    assert.equal(record.ok, true);
    assert.equal(record.data.ready, true);
    assert.deepEqual(record.data.platforms, ["darwin-arm64", "darwin-x64", "win32-x64"]);
    assert.equal(
      verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }).ready,
      true,
    );

    record.data.sourceCommit = "b".repeat(40);
    fs.writeFileSync(output, JSON.stringify(record));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /verification artifact differs from the current evidence set/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("CLI writes structured failure evidence when upstream platform artifacts are missing", () => {
  const paths = fixture();
  try {
    for (const name of fs.readdirSync(paths.root)) {
      if (![
        path.basename(paths.lockPath),
        "plugin-archive-audit.json",
        "jianying-draft-plugin-source.tar.gz",
      ].includes(name)) {
        fs.rmSync(path.join(paths.root, name), { force: true });
      }
    }
    const output = path.join(paths.root, "verification.json");
    const result = spawnSync(process.execPath, [
      path.join(ROOT, "scripts", "verify_release_evidence.mjs"),
      "--evidence-root",
      paths.root,
      "--lock",
      paths.lockPath,
      "--output",
      output,
    ], { encoding: "utf8" });

    assert.equal(result.status, 1);
    assert.equal(result.stdout, "");
    const record = JSON.parse(fs.readFileSync(output, "utf8"));
    assert.equal(record.ok, false);
    assert.equal(record.error.type, "release_readiness_evidence_invalid");
    assert.match(record.error.message, /exactly one all-green readiness report/);
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("cutover evidence accepts only the final Rust-only surface as explicitly pending", () => {
  const paths = fixture();
  try {
    const readinessPath = path.join(paths.root, "readiness.json");
    const readiness = JSON.parse(fs.readFileSync(readinessPath, "utf8"));
    readiness.ready = false;
    readiness.blocked = ["runtime.release_surface_rust_only"];
    readiness.checks.find(
      (check) => check.id === "runtime.release_surface_rust_only",
    ).status = "blocked";
    fs.writeFileSync(readinessPath, JSON.stringify(readiness));

    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /exactly one all-green readiness report/,
    );
    const result = verifyReleaseEvidence({
      evidenceRoot: paths.root,
      lockPath: paths.lockPath,
      allowCutoverPending: true,
    });
    assert.equal(result.ready, true);
    assert.equal(result.cutoverPending, true);
    const cliResult = spawnSync(process.execPath, [
      path.join(ROOT, "scripts", "verify_release_evidence.mjs"),
      "--evidence-root",
      paths.root,
      "--lock",
      paths.lockPath,
      "--allow-cutover-pending",
    ], { encoding: "utf8" });
    assert.equal(cliResult.status, 0, cliResult.stderr);
    assert.equal(JSON.parse(cliResult.stdout).data.cutoverPending, true);

    readiness.blocked.push("hosts.release_acceptance");
    readiness.checks.find(
      (check) => check.id === "hosts.release_acceptance",
    ).status = "blocked";
    fs.writeFileSync(readinessPath, JSON.stringify(readiness));
    assert.throws(
      () => verifyReleaseEvidence({
        evidenceRoot: paths.root,
        lockPath: paths.lockPath,
        allowCutoverPending: true,
      }),
      /cutover evidence may only defer the final Rust-only release surface/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects unknown JSON mixed into the release evidence asset set", () => {
  const paths = fixture();
  try {
    fs.writeFileSync(path.join(paths.root, "unrelated.json"), JSON.stringify({ ok: true }));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /unexpected JSON evidence assets/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects unknown non-JSON assets mixed into the release evidence set", () => {
  const paths = fixture();
  try {
    fs.writeFileSync(path.join(paths.root, "unrelated.bin"), "unexpected");
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /unexpected non-JSON assets/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("requires exactly one successful Rust-only plugin archive audit", () => {
  const missing = fixture();
  try {
    fs.rmSync(path.join(missing.root, "plugin-archive-audit.json"));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: missing.root, lockPath: missing.lockPath }),
      /exactly one plugin archive audit/,
    );
  } finally {
    fs.rmSync(missing.root, { recursive: true, force: true });
  }

  for (const mutate of [
    (audit) => { audit.status = "failed"; },
    (audit) => { audit.skillCount = 12; },
    (audit) => { audit.rustOnlyRuntime = false; },
    (audit) => { audit.externalHeadlessRuntime = true; },
    (audit) => { audit.pythonDraftEngine = true; },
  ]) {
    const paths = fixture();
    try {
      const auditPath = path.join(paths.root, "plugin-archive-audit.json");
      const audit = JSON.parse(fs.readFileSync(auditPath, "utf8"));
      mutate(audit);
      fs.writeFileSync(auditPath, JSON.stringify(audit));
      assert.throws(
        () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
        /does not prove one complete Rust-only distribution/,
      );
    } finally {
      fs.rmSync(paths.root, { recursive: true, force: true });
    }
  }
});

test("binds the exact plugin archive bytes, version, and release checkout commit", () => {
  const tampered = fixture();
  try {
    fs.appendFileSync(
      path.join(tampered.root, "jianying-draft-plugin-source.tar.gz"),
      "tampered",
    );
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: tampered.root, lockPath: tampered.lockPath }),
      /differs from its audit digest/,
    );
  } finally {
    fs.rmSync(tampered.root, { recursive: true, force: true });
  }

  const versionDrift = fixture();
  try {
    const auditPath = path.join(versionDrift.root, "plugin-archive-audit.json");
    const audit = JSON.parse(fs.readFileSync(auditPath, "utf8"));
    audit.pluginVersion = "99.0.0";
    fs.writeFileSync(auditPath, JSON.stringify(audit));
    assert.throws(
      () => verifyReleaseEvidence({
        evidenceRoot: versionDrift.root,
        lockPath: versionDrift.lockPath,
      }),
      /archive version differs from the release manifest/,
    );
  } finally {
    fs.rmSync(versionDrift.root, { recursive: true, force: true });
  }

  const commitDrift = fixture();
  try {
    assert.throws(
      () => verifyReleaseEvidence({
        evidenceRoot: commitDrift.root,
        lockPath: commitDrift.lockPath,
        pluginSourceCommit: "b".repeat(40),
      }),
      /source commit differs from the release checkout/,
    );
  } finally {
    fs.rmSync(commitDrift.root, { recursive: true, force: true });
  }
});

test("rejects an all-green readiness shell that omits required checks", () => {
  const paths = fixture();
  try {
    const readinessPath = path.join(paths.root, "readiness.json");
    const readiness = JSON.parse(fs.readFileSync(readinessPath, "utf8"));
    readiness.checks.pop();
    fs.writeFileSync(readinessPath, JSON.stringify(readiness));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /readiness report is incomplete or not bound to this release/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects readiness identities that drift from plugin, CLI, or Skills locks", () => {
  const mutations = [
    (report) => { report.plugin_version = "99.0.0"; },
    (report) => {
      report.checks.find((check) => check.id === "cli.immutable_identity")
        .evidence.source_commit = "b".repeat(40);
    },
    (report) => {
      report.checks.find((check) => check.id === "skills.immutable_release")
        .evidence.commit = "c".repeat(40);
    },
    (report) => { report.checks[0].id = report.checks[1].id; },
  ];
  for (const mutate of mutations) {
    const paths = fixture();
    try {
      const readinessPath = path.join(paths.root, "readiness.json");
      const readiness = JSON.parse(fs.readFileSync(readinessPath, "utf8"));
      mutate(readiness);
      fs.writeFileSync(readinessPath, JSON.stringify(readiness));
      assert.throws(
        () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
        /readiness report is incomplete or not bound to this release/,
      );
    } finally {
      fs.rmSync(paths.root, { recursive: true, force: true });
    }
  }
});

test("rejects duplicate platforms and identity drift", () => {
  const paths = fixture();
  try {
    const win = path.join(paths.root, "canary-win32-x64.json");
    const record = JSON.parse(fs.readFileSync(win, "utf8"));
    record.data.platform = "darwin";
    fs.writeFileSync(win, JSON.stringify(record));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /unexpected or duplicate platform/,
    );

    record.data.platform = "win32";
    record.data.sourceCommit = "b".repeat(40);
    fs.writeFileSync(win, JSON.stringify(record));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /identity differs from the CLI lock/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects valid-looking digests that differ from the platform lock", () => {
  const paths = fixture();
  try {
    const arm = path.join(paths.root, "canary-darwin-arm64.json");
    const record = JSON.parse(fs.readFileSync(arm, "utf8"));
    record.data.archiveSha256 = "3".repeat(64);
    fs.writeFileSync(arm, JSON.stringify(record));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /artifact digests differ from the CLI lock/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects capability manifest or SBOM evidence that differs from the platform lock", () => {
  for (const field of ["capabilityManifestSha256", "sbomSha256"]) {
    const paths = fixture();
    try {
      const arm = path.join(paths.root, "canary-darwin-arm64.json");
      const record = JSON.parse(fs.readFileSync(arm, "utf8"));
      record.data[field] = "5".repeat(64);
      fs.writeFileSync(arm, JSON.stringify(record));
      assert.throws(
        () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
        /canary artifact digests differ from the CLI lock/,
      );
    } finally {
      fs.rmSync(paths.root, { recursive: true, force: true });
    }
  }
});

test("rejects a canary without explicit binary-to-manifest equality evidence", () => {
  const paths = fixture();
  try {
    const arm = path.join(paths.root, "canary-darwin-arm64.json");
    const record = JSON.parse(fs.readFileSync(arm, "utf8"));
    record.data.capabilityManifestMatchesRuntime = false;
    fs.writeFileSync(arm, JSON.stringify(record));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /capability manifest was not proven equal to the binary handshake/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects a canary that omits a lock-required capability", () => {
  const paths = fixture();
  try {
    const arm = path.join(paths.root, "canary-darwin-arm64.json");
    const record = JSON.parse(fs.readFileSync(arm, "utf8"));
    record.data.requiredCapabilities.pop();
    fs.writeFileSync(arm, JSON.stringify(record));
    assert.throws(
      () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
      /required capabilities differ from the plugin lock/,
    );
  } finally {
    fs.rmSync(paths.root, { recursive: true, force: true });
  }
});

test("rejects canary evidence that is not bound to the locked Skills contract", () => {
  const mutations = [
    (canary) => { canary.skillsVersion = "99.0.0"; },
    (canary) => { canary.skillMinimumCliVersion = "99.0.0"; },
    (canary) => { canary.skillRequiredCapabilities.pop(); },
    (canary) => { canary.skillCapabilitiesSupported = false; },
  ];
  for (const mutate of mutations) {
    const paths = fixture();
    try {
      const arm = path.join(paths.root, "canary-darwin-arm64.json");
      const record = JSON.parse(fs.readFileSync(arm, "utf8"));
      mutate(record.data);
      fs.writeFileSync(arm, JSON.stringify(record));
      assert.throws(
        () => verifyReleaseEvidence({ evidenceRoot: paths.root, lockPath: paths.lockPath }),
        /locked Skills capability contract/,
      );
    } finally {
      fs.rmSync(paths.root, { recursive: true, force: true });
    }
  }
});
