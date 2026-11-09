import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";
import test from "node:test";

const configuredRoots = process.env.JIANYING_HOST_PLUGIN_ROOTS;
const enabled = Boolean(
  configuredRoots
  && process.env.JIANYING_CLI_PATH
  && process.env.JIANYING_CLI_SHA256,
);

test("real Codex, ZCode, and Kimi installs execute one Job with equivalent semantics", { skip: !enabled }, async () => {
  const pluginRoots = JSON.parse(configuredRoots);
  assert.deepEqual(Object.keys(pluginRoots), ["codex", "zcode", "kimi"]);
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-cross-host-"));
  const media = path.join(root, "clip.mp4");
  const outputPath = path.join(root, "shared-draft");
  const generated = spawnSync(
    "ffmpeg",
    [
      "-hide_banner", "-loglevel", "error", "-y",
      "-f", "lavfi", "-i", "color=c=green:s=320x240:d=1:r=30",
      "-c:v", "libx264", "-pix_fmt", "yuv420p", media,
    ],
    { encoding: "utf8" },
  );
  assert.equal(generated.status, 0, generated.stderr);

  const request = {
    intent: {
      plan: {
        schema: "jianying-cli-plan/v1",
        name: "real-cross-host",
        canvas: { width: 320, height: 240, fps: 30 },
        tracks: [{
          type: "video",
          name: "main",
          segments: [{ source: media, start_us: 0, duration_us: 1_000_000 }],
        }],
      },
    },
    mediaPaths: [media],
    outputPath,
  };
  const evidence = [];
  for (const [host, pluginRoot] of Object.entries(pluginRoots)) {
    const moduleUrl = pathToFileURL(path.join(pluginRoot, "scripts", "harness.mjs")).href;
    const { Harness } = await import(`${moduleUrl}?host=${host}`);
    const harness = new Harness({
      stateRoot: path.join(root, "states", host),
      env: process.env,
      pluginRoot,
    });
    assert.equal(harness.doctor().checks.cli.ready, true, host);
    const started = harness.start(request);
    const job = JSON.parse(fs.readFileSync(started.jobPath, "utf8"));
    harness.approve(started.taskId, {
      ...harness.binding(started),
      expiresAt: new Date(Date.now() + 60_000).toISOString(),
    });
    const completed = harness.execute(started.taskId);
    assert.equal(completed.terminalState, "completed", host);
    evidence.push({
      host,
      taskId: completed.taskId,
      jobSchema: job.schema,
      operation: completed.lastResult?.data?.operation,
      verificationOk: completed.lastResult?.data?.verification?.ok,
      evidenceLevel: completed.evidenceLevel,
      verifiedStages: completed.verifiedStages,
    });
    fs.rmSync(outputPath, { recursive: true });
  }

  const expected = { ...evidence[0] };
  delete expected.host;
  for (const item of evidence) {
    const normalized = { ...item };
    delete normalized.host;
    assert.deepEqual(normalized, expected, item.host);
  }
  assert.equal(expected.jobSchema, "jianying-job/v2");
  assert.equal(expected.operation, "create");
  assert.equal(expected.verificationOk, true);
  assert.equal(expected.evidenceLevel, "editable_draft");
});
