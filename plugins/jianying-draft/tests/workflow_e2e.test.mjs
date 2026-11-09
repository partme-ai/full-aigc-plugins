import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { runJob, runJsonCommand } from "../scripts/runtime_adapter.mjs";


function workflowCli() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-workflows-"));
  const cli = path.join(root, "jianying");
  const capabilities = [
    "capabilities", "schema.job_v2", "job.run", "job.batch", "job.retry",
    "project.edit_isolated", "captions.import", "timeline.volume", "render.proxy",
    "store.restore",
  ];
  fs.writeFileSync(cli, `#!/usr/bin/env node
const fs = require("node:fs");
const args = process.argv.slice(2).filter(value => value !== "--json");
if (args.includes("--version")) { console.log("jianying 1.6.19"); process.exit(0); }
if (args[0] === "capabilities") {
  console.log(JSON.stringify({ok:true,data:{schema:"jianying-capabilities/v1",cli_version:"1.6.19",capabilities:${JSON.stringify(capabilities)}.map(id=>({id,status:"supported"}))}}));
  process.exit(0);
}
const operation = args[0] === "job" && args[1] === "run" ? JSON.parse(fs.readFileSync(args[2], "utf8")).operation : args.slice(0, 2).join(".");
console.log(JSON.stringify({ok:true,data:{operation,task_id:"workflow-task",args}}));
`, { mode: 0o755 });
  const sha256 = crypto.createHash("sha256").update(fs.readFileSync(cli)).digest("hex");
  return { root, cli, env: { JIANYING_CLI_PATH: cli, JIANYING_CLI_SHA256: sha256 } };
}

function writeJob(root, operation, extra = {}) {
  const file = path.join(root, `${operation}.json`);
  fs.writeFileSync(file, JSON.stringify({ schema: "jianying-job/v2", operation, ...extra }));
  return file;
}

test("create and isolated edit Jobs share the Runtime Adapter", () => {
  const fixture = workflowCli();
  for (const operation of ["create", "edit"]) {
    const result = runJob({
      jobPath: writeJob(fixture.root, operation),
      outputPath: path.join(fixture.root, `${operation}-out`),
      env: fixture.env,
    });
    assert.equal(result.envelope.ok, true);
    assert.equal(result.envelope.data.operation, operation);
    assert.equal(result.taskId, "workflow-task");
  }
});

test("caption, audio, batch, recovery, and proxy workflows require their own capabilities", () => {
  const fixture = workflowCli();
  const cases = [
    { args: ["captions", "import-srt", "/draft", "/subs.srt"], capability: "captions.import" },
    { args: ["timeline", "volume", "/draft", "segment", "0.8"], capability: "timeline.volume" },
    { args: ["job", "batch", "/batch.json"], capability: "job.batch" },
    { args: ["job", "retry", "task-1"], capability: "job.retry" },
    { args: ["store", "restore-snapshot", "--snapshot", "/snapshot", "--target", "/draft"], capability: "store.restore" },
    { args: ["render", "proxy", "/draft"], capability: "render.proxy" },
  ];
  for (const item of cases) {
    const result = runJsonCommand({
      args: item.args,
      requiredCapabilities: [item.capability],
      env: fixture.env,
    });
    assert.equal(result.envelope.ok, true, item.capability);
  }
});

test("native export remains blocked without a supported native capability", () => {
  const fixture = workflowCli();
  assert.throws(
    () => runJsonCommand({
      args: ["runtime", "export", "/draft"],
      requiredCapabilities: ["render.native"],
      env: fixture.env,
    }),
    (error) => error.code === "missing_capability" && error.details.capability === "render.native",
  );
});
