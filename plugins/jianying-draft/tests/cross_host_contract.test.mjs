import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { Harness } from "../scripts/harness.mjs";
import { AdapterError, runJsonCommand } from "../scripts/runtime_adapter.mjs";
import { qualityContractDigest } from "../scripts/quality_contracts.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const FIXTURE = JSON.parse(
  fs.readFileSync(path.join(ROOT, "tests", "fixtures", "host_contract_rust.json"), "utf8"),
);

function fixtureCli({ recoverable = false } = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-host-contract-"));
  const cli = path.join(root, "jianying");
  const capabilities = ["capabilities", "schema.job_v2", "job.run"];
  fs.writeFileSync(cli, `#!/usr/bin/env node
const args = process.argv.slice(2).filter(value => value !== "--json");
if (args.includes("--version")) { console.log("jianying 1.6.19"); process.exit(0); }
if (args[0] === "capabilities") {
  console.log(JSON.stringify({ok:true,data:{schema:"jianying-capabilities/v1",cli_version:"1.6.19",capabilities:${JSON.stringify(capabilities)}.map(id=>({id,status:"supported"}))}}));
  process.exit(0);
}
if (args[0] === "probe") {
  console.log(JSON.stringify({ok:true,data:{path:args[1],duration_us:1000000,width:1920,height:1080,streams:["video"]}}));
  process.exit(0);
}
if (args[0] === "job" && args[1] === "run") {
  const response = ${recoverable
    ? '{ok:false,error:{type:"recoverable",message:"fixture interruption",details:{task_id:"host-task"},recovery:["retry"]}}'
    : '{ok:true,data:{operation:"create",task_id:"host-task"}}'};
  console.log(JSON.stringify(response));
  process.exit(${recoverable ? 75 : 0});
}
console.log(JSON.stringify({ok:false,error:{type:"unexpected",message:args.join(" "),details:{},recovery:[]}}));
process.exit(1);
`, { mode: 0o755 });
  const sha256 = crypto.createHash("sha256").update(fs.readFileSync(cli)).digest("hex");
  return { root, env: { JIANYING_CLI_PATH: cli, JIANYING_CLI_SHA256: sha256 } };
}

function request(root) {
  const media = path.join(root, "clip.mp4");
  fs.writeFileSync(media, "fixture-media");
  return {
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "cross-host-contract",
        canvas: { width: 1920, height: 1080, fps: 30 },
        tracks: [{ type: "video", name: "video", segments: [{ source: media, start_us: 0, duration_us: 1000000 }] }],
      },
    },
    mediaPaths: [media],
    outputPath: path.join(root, "draft"),
    evidenceLevel: "editable_draft",
  };
}

function normalizedState(state) {
  return {
    taskId: state.taskId,
    stage: state.stage,
    terminalState: state.terminalState,
    evidenceLevel: state.evidenceLevel,
    cliTaskId: state.cliTaskId,
    errorType: state.lastResult?.error?.type ?? null,
    recovery: state.lastResult?.error?.recovery ?? [],
  };
}

function runSuccessfulWorkflow(host, sharedRequest, cli) {
  const harness = new Harness({
    stateRoot: path.join(cli.root, "states", host.id),
    env: cli.env,
    pluginRoot: ROOT,
  });
  const started = harness.start(sharedRequest);
  const binding = harness.binding(started);

  assert.throws(
    () => harness.approve(started.taskId, {
      ...binding,
      target: `${binding.target}-wrong`,
      expiresAt: new Date(Date.now() + 60000).toISOString(),
    }),
    (error) => error instanceof AdapterError && error.code === "approval_scope_mismatch",
    `${host.id} must reject an approval bound to another target`,
  );

  harness.approve(started.taskId, {
    ...binding,
    expiresAt: new Date(Date.now() + 60000).toISOString(),
  });
  return normalizedState(harness.execute(started.taskId));
}

function runRecoverableWorkflow(host, sharedRequest, cli) {
  const harness = new Harness({
    stateRoot: path.join(cli.root, "recoverable-states", host.id),
    env: cli.env,
    pluginRoot: ROOT,
  });
  const started = harness.start(sharedRequest);
  harness.approve(started.taskId, {
    ...harness.binding(started),
    expiresAt: new Date(Date.now() + 60000).toISOString(),
  });
  const failed = harness.execute(started.taskId);
  const retried = harness.retry(started.taskId);
  return { failed: normalizedState(failed), retried: normalizedState(retried) };
}

test("Codex, ZCode, and Kimi manifests resolve the shared Rust Harness contract", () => {
  assert.equal(FIXTURE.schema, "jianying-plugin-host-contract-fixture/v2");
  assert.deepEqual(FIXTURE.hosts.map((host) => host.id), ["codex", "zcode", "kimi"]);
  for (const host of FIXTURE.hosts) {
    const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, host.manifest), "utf8"));
    assert.equal(manifest.name, "jianying-draft", host.id);
    assert.match(manifest.description, /Rust/, host.id);
    assert.equal(manifest.skills, "./skills/", host.id);
    assert.ok(fs.existsSync(path.join(ROOT, host.entry)), host.id);
    if (host.commands) assert.ok(fs.statSync(path.join(ROOT, host.commands)).isDirectory(), host.id);
    if (host.session_hook) {
      const hooks = fs.readFileSync(path.join(ROOT, host.session_hook), "utf8");
      assert.match(hooks, /scripts\/harness\.mjs[^\n]*doctor/, host.id);
    }
  }
});

test("the same workflow and approval fixture is semantically equivalent on all hosts", () => {
  const cli = fixtureCli();
  const sharedRequest = request(cli.root);
  const results = FIXTURE.hosts.map((host) => runSuccessfulWorkflow(host, sharedRequest, cli));
  assert.deepEqual(results.slice(1), [results[0], results[0]]);
  assert.deepEqual(results[0], {
    taskId: results[0].taskId,
    stage: "deliver",
    terminalState: "completed",
    evidenceLevel: "editable_draft",
    cliTaskId: "host-task",
    errorType: null,
    recovery: [],
  });
});

test("missing capabilities fail with the same structured error on all hosts", () => {
  const cli = fixtureCli();
  const results = FIXTURE.hosts.map((host) => {
    try {
      runJsonCommand({
        args: ["runtime", "export", `/draft/${host.id}`],
        requiredCapabilities: ["render.native"],
        env: cli.env,
        pluginRoot: ROOT,
      });
      assert.fail("missing capability must fail closed");
    } catch (error) {
      assert.ok(error instanceof AdapterError);
      return { code: error.code, details: error.details, recovery: error.recovery };
    }
  });
  assert.deepEqual(results.slice(1), [results[0], results[0]]);
  assert.equal(results[0].code, "missing_capability");
  assert.equal(results[0].details.capability, "render.native");
});

test("recoverable failures and retry checkpoints are equivalent on all hosts", () => {
  const cli = fixtureCli({ recoverable: true });
  const sharedRequest = request(cli.root);
  const results = FIXTURE.hosts.map((host) => runRecoverableWorkflow(host, sharedRequest, cli));
  assert.deepEqual(results.slice(1), [results[0], results[0]]);
  assert.equal(results[0].failed.terminalState, "recoverable");
  assert.equal(results[0].failed.errorType, "recoverable");
  assert.deepEqual(results[0].failed.recovery, ["retry"]);
  assert.equal(results[0].retried.stage, "approve");
  assert.equal(results[0].retried.terminalState, null);
});

test("quality contracts canonicalize identically for Codex, ZCode, and Kimi", () => {
  const contracts = JSON.parse(fs.readFileSync(path.join(ROOT,"tests/fixtures/quality-loop/contracts.json"),"utf8"));
  const reordered = Object.fromEntries(Object.entries(contracts.creative_target).reverse());
  const results = FIXTURE.hosts.map((host) => {
    const manifest = JSON.parse(fs.readFileSync(path.join(ROOT,host.manifest),"utf8"));
    assert.ok(fs.existsSync(path.join(ROOT,host.entry)),host.id);
    return {host:host.id,digest:qualityContractDigest(reordered),unicode:reordered.narrative_goal};
  });
  assert.deepEqual(results.map(item=>item.digest),Array(3).fill(qualityContractDigest(contracts.creative_target)));
  assert.deepEqual(results.map(item=>item.unicode),Array(3).fill("记录周末露营从出发到日落的真实变化"));
});
