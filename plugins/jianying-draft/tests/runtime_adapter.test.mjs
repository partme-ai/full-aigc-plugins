import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  AdapterError,
  handshake,
  locateCli,
  runJsonCommand,
  runJob,
} from "../scripts/runtime_adapter.mjs";
import {
  installBundle,
  rollbackBundle,
  upgradeBundle,
} from "../scripts/install_cli_bundle.mjs";
import { Harness, compileJob, inventoryMedia } from "../scripts/harness.mjs";
import { spawnSync } from "node:child_process";

function fakeCli(config = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-adapter-"));
  const cli = path.join(root, "jianying");
  const settings = {
    version: "1.6.19",
    capabilitySchema: "jianying-capabilities/v1",
    capabilities: ["capabilities", "schema.job_v2", "job.run"],
    jobExit: 0,
    jobStderr: "",
    jobEnvelope: { ok: true, data: { operation: "create", task_id: "task-ok" } },
    responses: {},
    ...config,
  };
  fs.writeFileSync(
    cli,
    `#!/usr/bin/env node
const settings = ${JSON.stringify(settings)};
const args = process.argv.slice(2);
if (args.includes("--version")) {
  console.log("jianying " + settings.version);
  process.exit(0);
}
if (args[0] === "capabilities") {
  console.log(JSON.stringify({ok:true,data:{
    schema:settings.capabilitySchema,
    cli_version:settings.version,
    capabilities:settings.capabilities.map(id => ({id,status:"supported"}))
  }}));
  process.exit(0);
}
if (args[0] === "probe") {
  console.log(JSON.stringify({ok:true,data:{path:args[1],duration_us:1000000,width:1920,height:1080,streams:["video"]}}));
  process.exit(0);
}
if (args[0] === "doctor") {
  console.log(JSON.stringify({ok:true,data:{version:settings.version,ffprobe:"fixture",ffmpeg:"fixture",draft_roots:[],editors_running:[]}}));
  process.exit(0);
}
if (args[0] === "job" && args[1] === "run") {
  if (settings.jobStderr) process.stderr.write(settings.jobStderr);
  const job = JSON.parse(require("node:fs").readFileSync(args[2], "utf8"));
  const response = settings.jobEnvelope ?? {ok:true,data:{operation:job.operation,task_id:"task-ok",args}};
  console.log(JSON.stringify(response));
  process.exit(settings.jobExit);
}
const responseKey = args.filter(value => value !== "--json").slice(0, 2).join(" ");
if (settings.responses[responseKey]) {
  console.log(JSON.stringify(settings.responses[responseKey]));
  process.exit(0);
}
console.log(JSON.stringify({ok:false,error:{type:"unexpected",message:args.join(" "),details:{},recovery:[]}}));
process.exit(1);
`,
    { mode: 0o755 },
  );
  const sha256 = crypto.createHash("sha256").update(fs.readFileSync(cli)).digest("hex");
  return { root, cli, sha256, version: settings.version };
}

function adapterEnv(fake, extra = {}) {
  return {
    JIANYING_CLI_PATH: fake.cli,
    JIANYING_CLI_SHA256: fake.sha256,
    ...extra,
  };
}

function releaseBundle(fake, platform = "darwin-arm64") {
  const bundle = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-bundle-"));
  const executable = platform.startsWith("win32") ? "jianying.exe" : "jianying";
  const capabilityDir = path.join(bundle, "provenance");
  fs.mkdirSync(capabilityDir);
  fs.copyFileSync(fake.cli, path.join(bundle, executable));
  fs.chmodSync(path.join(bundle, executable), 0o755);
  fs.writeFileSync(
    path.join(capabilityDir, "CAPABILITIES.json"),
    JSON.stringify({ schema: "jianying-capabilities/v1" }),
  );
  fs.mkdirSync(path.join(bundle, "schemas"));
  fs.writeFileSync(path.join(bundle, "LICENSE"), "fixture license\n");
  fs.writeFileSync(path.join(bundle, "THIRD_PARTY_NOTICES.md"), "fixture notices\n");
  fs.writeFileSync(path.join(bundle, "SBOM.spdx.json"), JSON.stringify({
    spdxVersion: "SPDX-2.3",
    dataLicense: "CC0-1.0",
    packages: [{
      name: "jianying-cli",
      versionInfo: fake.version ?? "1.6.19",
      licenseDeclared: "Apache-2.0",
    }],
  }));
  fs.writeFileSync(
    path.join(bundle, "schemas", "jianying-job-v2.schema.json"),
    JSON.stringify({
      $schema: "https://json-schema.org/draft/2020-12/schema",
      $id: "https://partme-ai.github.io/jianying-cli/schemas/jianying-job-v2.schema.json",
      required: ["schema", "operation"],
    }),
  );
  const files = [
    executable,
    "provenance/CAPABILITIES.json",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "SBOM.spdx.json",
    "schemas/jianying-job-v2.schema.json",
  ].map((relative) => {
    const content = fs.readFileSync(path.join(bundle, relative));
    return {
      path: relative,
      sha256: crypto.createHash("sha256").update(content).digest("hex"),
      size: content.length,
    };
  });
  fs.writeFileSync(
    path.join(bundle, "manifest.json"),
    JSON.stringify({
      schema: "jianying-cli-release/v1",
      version: fake.version ?? "1.6.19",
      platform,
      capabilityManifest: "provenance/CAPABILITIES.json",
      files,
    }),
  );
  return bundle;
}

test("locates an explicitly pinned development CLI", () => {
  const fake = fakeCli();
  const located = locateCli({ env: adapterEnv(fake) });
  assert.equal(located.path, fake.cli);
  assert.equal(located.sha256, fake.sha256);
  assert.equal(located.source, "development_override");
});

test("reports missing CLI and checksum mismatch with stable error codes", () => {
  assert.throws(
    () => locateCli({
      env: { PATH: "" },
      platform: "darwin",
      arch: "arm64",
    }),
    (error) => error instanceof AdapterError && error.code === "cli_not_found",
  );
  const fake = fakeCli();
  assert.throws(
    () => locateCli({ env: adapterEnv(fake, { JIANYING_CLI_SHA256: "0".repeat(64) }) }),
    (error) => error instanceof AdapterError && error.code === "checksum_mismatch",
  );
});

test("uses a checksum-pinned installed fallback on supported platforms", () => {
  const fake = fakeCli();
  const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-install-"));
  const installedDir = path.join(installRoot, "darwin-arm64");
  fs.mkdirSync(installedDir, { recursive: true });
  const installedCli = path.join(installedDir, "jianying");
  fs.copyFileSync(fake.cli, installedCli);
  fs.chmodSync(installedCli, 0o755);
  fs.writeFileSync(path.join(installedDir, "jianying.sha256"), `${fake.sha256}  jianying\n`);

  const located = locateCli({
    env: { PATH: "", JIANYING_CLI_INSTALL_ROOT: installRoot },
    platform: "darwin",
    arch: "arm64",
  });
  assert.equal(located.path, installedCli);
  assert.equal(located.source, "installed_fallback");
});

test("installs a verified extracted release bundle for a clean handshake", () => {
  const fake = fakeCli();
  const bundle = releaseBundle(fake);
  const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-clean-install-"));
  const installed = installBundle({ bundleRoot: bundle, installRoot });
  assert.equal(installed.platform, "darwin-arm64");
  const result = handshake({
    env: { PATH: path.dirname(process.execPath), JIANYING_CLI_INSTALL_ROOT: installRoot },
    platform: "darwin",
    arch: "arm64",
  });
  assert.equal(result.ready, true);
  assert.equal(result.source, "installed_fallback");
});

test("rejects a tampered extracted release bundle before installation", () => {
  const bundle = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-tampered-bundle-"));
  fs.writeFileSync(path.join(bundle, "jianying"), "tampered");
  fs.mkdirSync(path.join(bundle, "provenance"));
  fs.writeFileSync(path.join(bundle, "provenance", "CAPABILITIES.json"), "{}");
  fs.writeFileSync(
    path.join(bundle, "manifest.json"),
    JSON.stringify({
      schema: "jianying-cli-release/v1",
      version: "1.6.19",
      platform: "darwin-arm64",
      capabilityManifest: "provenance/CAPABILITIES.json",
      files: [
        { path: "jianying", sha256: "0".repeat(64), size: 8 },
        {
          path: "provenance/CAPABILITIES.json",
          sha256: crypto.createHash("sha256").update("{}").digest("hex"),
          size: 2,
        },
      ],
    }),
  );
  assert.throws(
    () => installBundle({
      bundleRoot: bundle,
      installRoot: fs.mkdtempSync(path.join(os.tmpdir(), "jianying-rejected-install-")),
    }),
    (error) => error instanceof AdapterError && error.code === "release_checksum_mismatch",
  );
});

test("rejects a checksum-valid bundle that omits mandatory legal or schema material", () => {
  const fake = fakeCli();
  const bundle = releaseBundle(fake);
  const manifestPath = path.join(bundle, "manifest.json");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  manifest.files = manifest.files.filter((entry) => entry.path !== "SBOM.spdx.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest));

  assert.throws(
    () => installBundle({
      bundleRoot: bundle,
      installRoot: fs.mkdtempSync(path.join(os.tmpdir(), "jianying-incomplete-contract-")),
    }),
    (error) => error instanceof AdapterError
      && error.code === "release_contract_incomplete"
      && error.details.missing.includes("SBOM.spdx.json"),
  );
});

test("rejects a checksum-valid placeholder SBOM", () => {
  const fake = fakeCli();
  const bundle = releaseBundle(fake);
  const sbomPath = path.join(bundle, "SBOM.spdx.json");
  fs.writeFileSync(sbomPath, "{}");
  const manifestPath = path.join(bundle, "manifest.json");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const entry = manifest.files.find((candidate) => candidate.path === "SBOM.spdx.json");
  entry.sha256 = crypto.createHash("sha256").update("{}").digest("hex");
  entry.size = 2;
  fs.writeFileSync(manifestPath, JSON.stringify(manifest));

  assert.throws(
    () => installBundle({
      bundleRoot: bundle,
      installRoot: fs.mkdtempSync(path.join(os.tmpdir(), "jianying-placeholder-sbom-")),
    }),
    (error) => error instanceof AdapterError && error.code === "release_contract_invalid",
  );
});

test("an interrupted bundle leaves the active offline runtime untouched", () => {
  const active = fakeCli({ version: "1.6.19" });
  const incomplete = fakeCli({ version: "1.7.0" });
  const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-interrupted-install-"));
  installBundle({ bundleRoot: releaseBundle(active), installRoot });
  const bundle = releaseBundle(incomplete);
  fs.unlinkSync(path.join(bundle, "provenance", "CAPABILITIES.json"));
  assert.throws(
    () => upgradeBundle({ bundleRoot: bundle, installRoot }),
    (error) => error instanceof AdapterError && error.code === "release_file_missing",
  );
  const result = handshake({
    env: { PATH: path.dirname(process.execPath), JIANYING_CLI_INSTALL_ROOT: installRoot },
    platform: "darwin",
    arch: "arm64",
  });
  assert.equal(result.version, "1.6.19");
});

test("upgrades and rolls back only between checksum-verified Rust runtimes", () => {
  const oldCli = fakeCli({ version: "1.6.19" });
  const newCli = fakeCli({ version: "1.7.0" });
  const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-rollback-install-"));
  const original = installBundle({ bundleRoot: releaseBundle(oldCli), installRoot });
  const upgraded = upgradeBundle({ bundleRoot: releaseBundle(newCli), installRoot });
  assert.equal(upgraded.previousSha256, original.sha256);
  const restored = rollbackBundle({
    installRoot,
    platform: "darwin-arm64",
    sha256: original.sha256,
  });
  assert.equal(restored.restoredSha256, original.sha256);
  const result = handshake({
    env: { PATH: path.dirname(process.execPath), JIANYING_CLI_INSTALL_ROOT: installRoot },
    platform: "darwin",
    arch: "arm64",
  });
  assert.equal(result.version, "1.6.19");
  const installedFiles = fs.readdirSync(restored.destination, { recursive: true })
    .map(String);
  assert.equal(installedFiles.some((entry) => /(?:\.py$|pyJianYingDraft|headless)/i.test(entry)), false);
});

test("unsupported platforms and incomplete installs are deterministically not-ready", () => {
  assert.throws(
    () => locateCli({ env: { PATH: "" }, platform: "linux", arch: "x64" }),
    (error) => error instanceof AdapterError && error.code === "unsupported_platform",
  );

  const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-incomplete-"));
  const installedDir = path.join(installRoot, "win32-x64");
  fs.mkdirSync(installedDir, { recursive: true });
  fs.writeFileSync(path.join(installedDir, "jianying.exe"), "not verified");
  assert.throws(
    () => locateCli({
      env: { PATH: "", JIANYING_CLI_INSTALL_ROOT: installRoot },
      platform: "win32",
      arch: "x64",
    }),
    (error) => error instanceof AdapterError && error.code === "checksum_required",
  );
});

test("handshake verifies version, capability schema, and required capabilities", () => {
  const fake = fakeCli();
  const result = handshake({ env: adapterEnv(fake) });
  assert.equal(result.ready, true);
  assert.equal(result.version, "1.6.19");
  assert.equal(result.jobSchema, "jianying-job/v2");
  assert.deepEqual(result.requiredCapabilities, [
    "capabilities",
    "schema.job_v2",
    "job.run",
  ]);
});

test("handshake rejects old version, incompatible schema, and missing capability", () => {
  const old = fakeCli({ version: "1.5.0" });
  assert.throws(
    () => handshake({ env: adapterEnv(old) }),
    (error) => error instanceof AdapterError && error.code === "version_too_old",
  );

  const schema = fakeCli({ capabilitySchema: "jianying-capabilities/v2" });
  assert.throws(
    () => handshake({ env: adapterEnv(schema) }),
    (error) => error instanceof AdapterError && error.code === "schema_incompatible",
  );

  const missing = fakeCli({ capabilities: ["capabilities", "schema.job_v2"] });
  assert.throws(
    () => handshake({ env: adapterEnv(missing) }),
    (error) =>
      error instanceof AdapterError
      && error.code === "missing_capability"
      && error.details.capability === "job.run"
      && error.recovery.length > 0,
  );
});

test("operation calls fail closed when their requested capability is not supported", () => {
  const fake = fakeCli();
  assert.throws(
    () => runJsonCommand({
      args: ["captions", "list", "/draft"],
      requiredCapabilities: ["captions.list"],
      env: adapterEnv(fake),
    }),
    (error) => error instanceof AdapterError
      && error.code === "missing_capability"
      && error.details.capability === "captions.list",
  );
});

test("job invocation preserves structured recoverable failure evidence", () => {
  const fake = fakeCli({
    jobExit: 1,
    jobStderr: "diagnostic only\n",
    jobEnvelope: {
      ok: false,
      error: {
        type: "recoverable",
        message: "resume required",
        details: { task_id: "task-42", checkpoint: "verify" },
        recovery: ["jianying job retry task-42"],
      },
    },
  });
  fs.writeFileSync(
    path.join(fake.root, "job.json"),
    JSON.stringify({ schema: "jianying-job/v2", operation: "create" }),
  );
  const result = runJob({
    jobPath: path.join(fake.root, "job.json"),
    outputPath: path.join(fake.root, "draft"),
    env: adapterEnv(fake),
  });
  assert.equal(result.exitCode, 1);
  assert.equal(result.stderr, "diagnostic only\n");
  assert.equal(result.error.type, "recoverable");
  assert.equal(result.taskId, "task-42");
  assert.deepEqual(result.recovery, ["jianying job retry task-42"]);
});

test("Harness inventories before compiling and enforces exact approval bindings", () => {
  const fake = fakeCli();
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-harness-"));
  const media = path.join(root, "clip.mp4");
  fs.writeFileSync(media, "fixture-media");
  const env = adapterEnv(fake, { PATH: path.dirname(process.execPath), PYTHONPATH: "" });
  const inventory = inventoryMedia({ mediaPaths: [media], env });
  assert.equal(inventory[0].facts.duration_us, 1000000);
  assert.throws(
    () => compileJob({
      intent: {
        plan: {
          schema: "jianying-cli-plan/v1",
          name: "unknown-material",
          canvas: { width: 1920, height: 1080, fps: 30 },
          tracks: [{ type: "video", segments: [{ source: path.join(root, "unknown.mp4"), start_us: 0, duration_us: 1000000 }] }],
        },
      },
      inventory,
    }),
    (error) => error instanceof AdapterError && error.code === "material_not_in_inventory",
  );
  assert.throws(
    () => compileJob({ intent: { plan: { schema: "jianying-cli-plan/v1" } }, inventory }),
    (error) => error instanceof AdapterError && error.code === "plan_invalid",
  );

  const compiled = compileJob({
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "strong-project",
        canvas: { width: 1920, height: 1080, fps: 30 },
        tracks: [{ type: "video", name: "main", segments: [{ source: media, start_us: 0, duration_us: 1000000 }] }],
      },
    },
    inventory,
  });
  assert.deepEqual(compiled.project.project, {
    name: "strong-project",
    width: 1920,
    height: 1080,
    frame_rate: { numerator: 30, denominator: 1 },
    timeline: {
      tracks: [{
        id: "main-0",
        kind: "video",
        segments: [{
          type: "video",
          id: "segment-0-0",
          range: { start_us: 0, duration_us: 1000000 },
          material_id: "material-0-0",
          source_range: { start_us: 0, duration_us: 1000000 },
          speed: 1,
          volume: 1,
        }],
      }],
    },
    materials: [{ type: "video", id: "material-0-0", path: media }],
  });

  const stateRoot = path.join(root, "state");
  const harness = new Harness({ stateRoot, env });
  const doctor = harness.doctor();
  assert.equal(doctor.ready, true);
  assert.equal(doctor.checks.skills.ready, true);
  assert.equal(doctor.checks.mediaTools.ready, true);
  assert.equal(doctor.checks.runtimeProfile.ready, true);
  assert.equal(fs.existsSync(stateRoot), false, "read-only doctor must not create or repair state");
  const state = harness.start({
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "fixture",
        canvas: { width: 1920, height: 1080, fps: 30 },
        tracks: [{ type: "video", segments: [{ source: media, start_us: 0, duration_us: 1000000 }] }],
      },
    },
    mediaPaths: [media],
    outputPath: path.join(root, "draft"),
  });
  assert.deepEqual(state.verifiedStages, ["intake", "inventory", "plan"]);
  assert.equal(harness.list()[0].taskId, state.taskId);
  assert.equal(harness.show(state.taskId).inputDigest, state.inputDigest);
  assert.throws(
    () => harness.execute(state.taskId),
    (error) => error instanceof AdapterError && error.code === "approval_required",
  );
  const binding = harness.binding(state);
  assert.throws(
    () => harness.approve(state.taskId, { ...binding, target: `${binding.target}-wrong`, expiresAt: new Date(Date.now() + 60000).toISOString() }),
    (error) => error instanceof AdapterError && error.code === "approval_scope_mismatch",
  );
  harness.approve(state.taskId, { ...binding, expiresAt: new Date(Date.now() + 60000).toISOString() });
  const completed = harness.execute(state.taskId);
  assert.equal(completed.terminalState, "completed");
  assert.equal(harness.assessDelivery(state.taskId, "editable_draft").satisfied, true);
  assert.equal(harness.assessDelivery(state.taskId, "native_export").satisfied, false);
  assert.equal(harness.resume(state.taskId).terminalState, "completed");
  assert.equal(harness.audit(state.taskId).history.at(-1).event, "task.completed");
  assert.throws(
    () => harness.cancel(state.taskId),
    (error) => error instanceof AdapterError && error.code === "task_terminal",
  );

  const retryState = structuredClone(completed);
  retryState.taskId = `${completed.taskId}-retry`;
  retryState.terminalState = "recoverable";
  retryState.stage = "execute";
  retryState.verifiedStages = ["intake", "inventory", "plan"];
  retryState.approvals = [];
  harness.save(retryState);
  const retried = harness.retry(retryState.taskId);
  assert.equal(retried.stage, "approve");
  assert.deepEqual(retried.verifiedStages, ["intake", "inventory", "plan"]);
  assert.equal(retried.inventory[0].sha256, state.inventory[0].sha256);
  assert.equal(harness.cancel(retryState.taskId).terminalState, "cancelled");
});

test("Harness compiles a real isolated edit Job with a target-bound approval", () => {
  const fake = fakeCli({ jobEnvelope: null });
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-edit-harness-"));
  const source = path.join(root, "source");
  const output = path.join(root, "edited");
  fs.mkdirSync(source);
  const intent = {
    operation: "edit",
    sourcePath: source,
    operations: [
      { operation: "replace_text", segment_id: "caption-1", text: "新字幕" },
      { operation: "move_segment", segment_id: "caption-1", target: { start_us: 1_000_000, duration_us: 2_000_000 } },
      { operation: "remove_segment", segment_id: "caption-2" },
    ],
  };
  const compiled = compileJob({ intent, inventory: [], outputPath: output });
  assert.deepEqual(compiled, {
    schema: "jianying-job/v2",
    operation: "edit",
    project: { type: "existing", source, output },
    operations: intent.operations,
  });
  assert.throws(
    () => compileJob({
      intent: {
        operation: "edit",
        sourcePath: source,
        operations: [{ operation: "add_material", material: { type: "video", id: "m1", path: "/clip.mp4" } }],
      },
      inventory: [],
      outputPath: output,
    }),
    (error) => error instanceof AdapterError && error.code === "edit_operation_not_supported",
  );

  const harness = new Harness({
    stateRoot: path.join(root, "state"),
    env: adapterEnv(fake),
  });
  const started = harness.start({ intent, mediaPaths: [], outputPath: output });
  assert.equal(started.operation, "edit");
  assert.equal(started.sourcePath, source);
  const binding = harness.binding(started);
  assert.equal(binding.command, "job.run.edit");
  assert.equal(binding.target, output);
  harness.approve(started.taskId, {
    ...binding,
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
  });
  const completed = harness.execute(started.taskId);
  assert.equal(completed.terminalState, "completed");
  assert.equal(completed.lastResult.data.operation, "edit");
  assert.equal(completed.lastResult.data.args.includes("--out"), false);
});

test("Harness cannot promote draft or proxy evidence to a native export", () => {
  const fake = fakeCli();
  const media = path.join(fake.root, "evidence.mp4");
  fs.writeFileSync(media, "evidence");
  const harness = new Harness({
    stateRoot: path.join(fake.root, "evidence-state"),
    env: adapterEnv(fake),
  });
  const base = {
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "evidence-level",
        canvas: { width: 1920, height: 1080, fps: 30 },
        tracks: [{ type: "video", segments: [{ source: media, start_us: 0, duration_us: 1000000 }] }],
      },
    },
    mediaPaths: [media],
    outputPath: path.join(fake.root, "evidence-output"),
  };

  assert.throws(
    () => harness.start({ ...base, evidenceLevel: "native_export" }),
    (error) => error instanceof AdapterError && error.code === "evidence_level_invalid",
  );
  assert.throws(
    () => harness.start({ ...base, evidenceLevel: "proxy_preview" }),
    (error) => error instanceof AdapterError && error.code === "evidence_level_invalid",
  );

  const state = harness.start({ ...base, evidenceLevel: "structural" });
  assert.throws(
    () => harness.assessDelivery(state.taskId, "unknown-level"),
    (error) => error instanceof AdapterError && error.code === "evidence_level_invalid",
  );
  const native = harness.assessDelivery(state.taskId, "native_export");
  assert.equal(native.satisfied, false);
  assert.equal(native.actualLevel, "structural");
});

test("the executable Harness doctor routes through the Rust Runtime Adapter", () => {
  const fake = fakeCli();
  const result = spawnSync(
    process.execPath,
    [path.join(process.cwd(), "scripts", "harness.mjs"), "doctor"],
    { encoding: "utf8", env: { ...process.env, ...adapterEnv(fake) } },
  );
  assert.equal(result.status, 0, result.stderr);
  const envelope = JSON.parse(result.stdout);
  assert.equal(envelope.ok, true);
  assert.equal(envelope.data.checks.cli.ready, true);
  assert.equal(envelope.data.checks.skills.ready, true);
});
