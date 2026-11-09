import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { Harness } from "../scripts/harness.mjs";
import { AdapterError, runJsonCommand } from "../scripts/runtime_adapter.mjs";

const enabled = Boolean(process.env.JIANYING_CLI_PATH && process.env.JIANYING_CLI_SHA256);

test("real Rust CLI accepts the Harness Job v2 and creates a verified editable draft", { skip: !enabled }, () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-cli-harness-"));
  const media = path.join(root, "clip.mp4");
  const generated = spawnSync(
    "ffmpeg",
    [
      "-hide_banner", "-loglevel", "error", "-y",
      "-f", "lavfi", "-i", "color=c=blue:s=320x240:d=1:r=30",
      "-c:v", "libx264", "-pix_fmt", "yuv420p", media,
    ],
    { encoding: "utf8" },
  );
  assert.equal(generated.status, 0, generated.stderr);
  const audio = path.join(root, "voice.wav");
  const generatedAudio = spawnSync(
    "ffmpeg",
    [
      "-hide_banner", "-loglevel", "error", "-y",
      "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
      "-c:a", "pcm_s16le", audio,
    ],
    { encoding: "utf8" },
  );
  assert.equal(generatedAudio.status, 0, generatedAudio.stderr);

  const harness = new Harness({
    stateRoot: path.join(root, "state"),
    env: process.env,
  });
  assert.equal(harness.doctor().checks.cli.ready, true);
  const started = harness.start({
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "real-cli-harness",
        canvas: { width: 320, height: 240, fps: 30 },
        tracks: [{
          type: "video",
          name: "main",
          segments: [{ source: media, start_us: 0, duration_us: 1_000_000 }],
        }, {
          type: "audio",
          name: "voice",
          segments: [{ source: audio, start_us: 0, duration_us: 1_000_000 }],
        }],
      },
    },
    mediaPaths: [media, audio],
    outputPath: path.join(root, "draft"),
  });
  const binding = harness.binding(started);
  assert.throws(
    () => harness.approve(started.taskId, {
      ...binding,
      target: `${binding.target}-wrong`,
      expiresAt: new Date(Date.now() + 60_000).toISOString(),
    }),
    (error) => error instanceof AdapterError && error.code === "approval_scope_mismatch",
  );
  harness.approve(started.taskId, {
    ...binding,
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
  });

  const completed = harness.execute(started.taskId);
  assert.equal(completed.terminalState, "completed", JSON.stringify(completed.lastResult));
  assert.equal(completed.lastResult?.ok, true);
  assert.equal(completed.lastResult?.data?.verification?.ok, true);
  assert.ok(fs.statSync(path.join(completed.outputPath, "draft_content.json")).isFile());
  assert.ok(fs.statSync(path.join(completed.outputPath, "draft_meta_info.json")).isFile());
  const completedHistoryLength = harness.audit(started.taskId).history.length;
  assert.equal(harness.resume(started.taskId).terminalState, "completed");
  assert.equal(harness.audit(started.taskId).history.length, completedHistoryLength);
  assert.equal(harness.audit(started.taskId).approvals[0].used, true);

  const srt = path.join(root, "captions.srt");
  fs.writeFileSync(srt, "1\n00:00:00,000 --> 00:00:00,800\nReal CLI caption\n", "utf8");
  const captions = runJsonCommand({
    args: ["captions", "import-srt", completed.outputPath, srt, "--track", "captions"],
    requiredCapabilities: ["captions.import"],
    env: process.env,
  });
  assert.equal(captions.envelope?.ok, true, JSON.stringify(captions.envelope));

  const withCaptions = JSON.parse(fs.readFileSync(path.join(completed.outputPath, "draft_content.json"), "utf8"));
  const audioSegmentId = withCaptions.tracks
    .find((track) => track.type === "audio")
    .segments[0].id;
  const transactionRoot = path.join(root, ".jianying-transactions");
  const beforeVolume = new Set(fs.readdirSync(transactionRoot));
  const volume = runJsonCommand({
    args: ["timeline", "volume", completed.outputPath, audioSegmentId, "0.35"],
    requiredCapabilities: ["timeline.volume"],
    env: process.env,
  });
  assert.equal(volume.envelope?.ok, true, JSON.stringify(volume.envelope));
  const volumeTransaction = fs.readdirSync(transactionRoot)
    .find((entry) => !beforeVolume.has(entry));
  assert.ok(volumeTransaction, "volume mutation must create a restorable transaction snapshot");

  const restored = runJsonCommand({
    args: [
      "store", "restore-snapshot",
      "--snapshot", path.join(transactionRoot, volumeTransaction, "snapshot"),
      "--target", completed.outputPath,
    ],
    requiredCapabilities: ["store.restore"],
    env: process.env,
  });
  assert.equal(restored.envelope?.ok, true, JSON.stringify(restored.envelope));

  const proxy = path.join(root, "preview.mp4");
  const rendered = runJsonCommand({
    args: ["render", "proxy", completed.outputPath, "--out", proxy],
    requiredCapabilities: ["render.proxy"],
    env: process.env,
  });
  assert.equal(rendered.envelope?.ok, true, JSON.stringify(rendered.envelope));
  assert.ok(fs.statSync(proxy).size > 0);

  const childJob = JSON.parse(fs.readFileSync(started.jobPath, "utf8"));
  const batchJob = path.join(root, "batch.json");
  fs.writeFileSync(batchJob, JSON.stringify({
    schema: "jianying-job/v2",
    operation: "batch",
    jobs: [childJob, childJob],
  }));
  const batchOutput = path.join(root, "batch-drafts");
  const batch = runJsonCommand({
    args: [
      "job", "batch", batchJob,
      "--out", batchOutput,
      "--state-root", path.join(root, "cli-job-state"),
    ],
    requiredCapabilities: ["job.batch"],
    env: process.env,
  });
  assert.equal(batch.envelope?.ok, true, JSON.stringify(batch.envelope));
  assert.equal(batch.envelope?.data?.result?.count ?? batch.envelope?.data?.count, 2);
  assert.ok(fs.statSync(path.join(batchOutput, "0000", "draft_content.json")).isFile());
  assert.ok(fs.statSync(path.join(batchOutput, "0001", "draft_content.json")).isFile());

  const sourceContentPath = path.join(completed.outputPath, "draft_content.json");
  const sourceBefore = fs.readFileSync(sourceContentPath);
  const sourceTimeline = JSON.parse(sourceBefore);
  const segmentId = sourceTimeline.tracks[0].segments[0].id;
  const editedOutput = path.join(root, "edited-draft");
  const editStarted = harness.start({
    intent: {
      operation: "edit",
      sourcePath: completed.outputPath,
      operations: [{
        operation: "move_segment",
        segment_id: segmentId,
        target: { start_us: 0, duration_us: 750_000 },
      }],
    },
    mediaPaths: [],
    outputPath: editedOutput,
  });
  assert.equal(harness.binding(editStarted).command, "job.run.edit");
  harness.approve(editStarted.taskId, {
    ...harness.binding(editStarted),
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
  });
  const editCompleted = harness.execute(editStarted.taskId);
  assert.equal(editCompleted.terminalState, "completed", JSON.stringify(editCompleted.lastResult));
  assert.equal(editCompleted.lastResult?.data?.operation, "edit");
  assert.equal(editCompleted.lastResult?.data?.isolation?.source_unchanged, true);
  assert.equal(
    crypto.createHash("sha256").update(fs.readFileSync(sourceContentPath)).digest("hex"),
    crypto.createHash("sha256").update(sourceBefore).digest("hex"),
  );
  const editedTimeline = JSON.parse(fs.readFileSync(path.join(editedOutput, "draft_content.json"), "utf8"));
  assert.equal(editedTimeline.tracks[0].segments[0].target_timerange.start, 0);
  assert.equal(editedTimeline.tracks[0].segments[0].target_timerange.duration, 750_000);

  const blockedOutput = path.join(root, "blocked-draft");
  fs.mkdirSync(blockedOutput);
  const interrupted = harness.start({
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "real-cli-retry",
        canvas: { width: 320, height: 240, fps: 30 },
        tracks: [{
          type: "video",
          name: "main",
          segments: [{ source: media, start_us: 0, duration_us: 1_000_000 }],
        }],
      },
    },
    mediaPaths: [media],
    outputPath: blockedOutput,
  });
  harness.approve(interrupted.taskId, {
    ...harness.binding(interrupted),
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
  });
  const failed = harness.execute(interrupted.taskId);
  assert.equal(failed.terminalState, "failed");
  assert.equal(failed.approvals[0].used, true);

  const retried = harness.retry(interrupted.taskId);
  assert.equal(retried.stage, "approve");
  assert.deepEqual(retried.approvals, []);
  assert.deepEqual(retried.verifiedStages, ["intake", "inventory", "plan"]);
  assert.equal(retried.inventory[0].sha256, interrupted.inventory[0].sha256);
  fs.rmdirSync(blockedOutput);
  harness.approve(retried.taskId, {
    ...harness.binding(retried),
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
  });
  assert.equal(harness.execute(retried.taskId).terminalState, "completed");
});
