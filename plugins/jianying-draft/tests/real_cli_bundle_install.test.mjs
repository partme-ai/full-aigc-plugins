import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { installBundle } from "../scripts/install_cli_bundle.mjs";
import { handshake, runJsonCommand } from "../scripts/runtime_adapter.mjs";
import { acquireOfficialResource } from "../scripts/native_resource_acquisition.mjs";
import { compileNativeControlPlan, probeNativeControlContracts } from "../scripts/native_control_orchestration.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const BUNDLE_ROOT = process.env.JIANYING_CLI_BUNDLE_ROOT;

test("a real release-layout bundle installs and handshakes without Cargo", {
  skip: !BUNDLE_ROOT,
}, () => {
  const installRoot = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-bundle-install-"));
  try {
    const installed = installBundle({ bundleRoot: BUNDLE_ROOT, installRoot });
    const env = {
      HOME: installRoot,
      PATH: "/usr/bin:/bin",
      JIANYING_CLI_INSTALL_ROOT: installRoot,
    };
    const ready = handshake({ env, pluginRoot: ROOT });
    const releaseManifest = JSON.parse(
      fs.readFileSync(path.join(BUNDLE_ROOT, "manifest.json"), "utf8"),
    );
    const packagedCapabilities = JSON.parse(
      fs.readFileSync(path.join(BUNDLE_ROOT, releaseManifest.capabilityManifest), "utf8"),
    );

    assert.equal(ready.ready, true);
    assert.equal(ready.source, "installed_fallback");
    assert.equal(ready.path, installed.executable);
    assert.equal(ready.sha256, installed.sha256);
    assert.equal(ready.version, installed.version);
    assert.equal(ready.capabilitySchema, "jianying-capabilities/v1");
    assert.equal(ready.jobSchema, "jianying-job/v2");
    assert.deepEqual(ready.requiredCapabilities, [
      "capabilities",
      "schema.job_v2",
      "job.run",
    ]);
    assert.deepEqual(ready.manifest, packagedCapabilities);
    const statuses = Object.fromEntries(
      ready.manifest.capabilities.map((capability) => [capability.id, capability.status]),
    );
    assert.equal(statuses["schema.compile_v1_compat"], "supported");
    assert.equal(statuses["project.compile"], "supported");
    assert.equal(statuses["media.audio"], "supported");
    assert.equal(statuses["timeline.quantization_report"], "supported");
    assert.equal(statuses["media.asr_whisper_cpp"], "supported");
    assert.equal(statuses["runtime.discovery"], "supported");

    const renderHelp = spawnSync(installed.executable, ["render", "--help"], {
      encoding: "utf8",
      env,
    });
    assert.equal(renderHelp.status, 0, renderHelp.stderr);
    assert.match(renderHelp.stdout, /\bnative-task\b/);

    const ttsHelp = spawnSync(installed.executable, ["media", "tts", "--help"], {
      encoding: "utf8",
      env,
    });
    assert.equal(ttsHelp.status, 0, ttsHelp.stderr);
    for (const provider of [
      "local-command",
      "system-macos",
      "system-windows",
      "local-http",
      "local-process",
      "edge-tts",
      "xiaomi-mimo",
      "volcengine",
      "aliyun-bailian",
      "baidu",
      "tencent-cloud",
      "minimax",
      "zhipu-glm",
    ]) {
      assert.match(ttsHelp.stdout, new RegExp(`\\b${provider}\\b`));
    }
    for (const option of [
      "--approval-id",
      "--approval-root",
      "--tts-state-root",
      "--resource-id",
      "--uid",
    ]) {
      assert.match(ttsHelp.stdout, new RegExp(`\\b${option.slice(2)}\\b`));
    }

    const transcribeHelp = spawnSync(installed.executable, ["media", "transcribe", "--help"], {
      encoding: "utf8",
      env,
    });
    assert.equal(transcribeHelp.status, 0, transcribeHelp.stderr);
    for (const option of [
      "--out",
      "--executable",
      "--model",
      "--model-id",
      "--format",
      "--language",
      "--translate",
      "--segment-timestamps",
      "--task-id",
      "--state-root",
      "--plan",
      "--retry",
    ]) {
      assert.match(transcribeHelp.stdout, new RegExp(`\\b${option.slice(2)}\\b`));
    }

    const discoveryHelp = spawnSync(installed.executable, ["runtime", "discover", "--help"], {
      encoding: "utf8",
      env,
    });
    assert.equal(discoveryHelp.status, 0, discoveryHelp.stderr);
    for (const option of ["--search-root", "--home", "--local-app-data"]) {
      assert.match(discoveryHelp.stdout, new RegExp(`\\b${option.slice(2)}\\b`));
    }
    const discovery = spawnSync(installed.executable, ["runtime", "discover", "--json"], {
      encoding: "utf8",
      env,
    });
    assert.equal(discovery.status, 0, discovery.stderr);
    const discoveryEnvelope = JSON.parse(discovery.stdout);
    assert.equal(discoveryEnvelope.data.automatic_routing, false);
    assert.equal(discoveryEnvelope.data.support_status, "unverified");

    const quantization = spawnSync(installed.executable, [
      "timeline",
      "quantization-report",
      "10ms",
      "50ms",
      "--fps-numerator",
      "30",
      "--maximum-drift",
      "30ms",
      "--json",
    ], { encoding: "utf8", env });
    assert.equal(quantization.status, 0, quantization.stderr);
    const quantizationEnvelope = JSON.parse(quantization.stdout);
    assert.equal(quantizationEnvelope.data.quantized.start_us, 0);
    assert.equal(quantizationEnvelope.data.quantized.duration_us, 66_666);

    const cloudDraft = path.join(installRoot, "cloud-plan-draft");
    fs.mkdirSync(cloudDraft);
    const cloudPlan = spawnSync(installed.executable, [
      "media",
      "tts",
      cloudDraft,
      "--provider",
      "minimax",
      "--text",
      "bundle secret-free plan",
      "--format",
      "mp3",
      "--model",
      "speech-2.8-hd",
      "--voice",
      "male-qn-qingse",
      "--credential-env",
      "ABSENT_BUNDLE_TEST_SECRET",
      "--task-id",
      "bundle-cloud-plan",
      "--max-cost-microunits",
      "50000",
      "--plan",
      "--json",
    ], { encoding: "utf8", env });
    assert.equal(cloudPlan.status, 0, cloudPlan.stderr);
    const cloudEnvelope = JSON.parse(cloudPlan.stdout);
    assert.equal(cloudEnvelope.data.state, "approval_required");
    assert.equal(cloudEnvelope.data.provider, "minimax");
    assert.equal(cloudEnvelope.data.approval_binding.command, "tts.cloud.submit");
    assert.doesNotMatch(cloudPlan.stdout, /bundle secret-free plan/);
    assert.equal(fs.existsSync(path.join(cloudDraft, "draft_content.json")), false);

    const volcPlan = spawnSync(installed.executable, [
      "media",
      "tts",
      cloudDraft,
      "--provider",
      "volcengine",
      "--text",
      "bundle volcengine v3 plan",
      "--format",
      "mp3",
      "--voice",
      "zh_female_fixture",
      "--resource-id",
      "seed-tts-2.0",
      "--uid",
      "bundle-user",
      "--credential-env",
      "ABSENT_BUNDLE_TEST_SECRET",
      "--task-id",
      "bundle-volcengine-plan",
      "--max-cost-microunits",
      "50000",
      "--plan",
      "--json",
    ], { encoding: "utf8", env });
    assert.equal(volcPlan.status, 0, volcPlan.stderr);
    const volcEnvelope = JSON.parse(volcPlan.stdout);
    assert.equal(volcEnvelope.data.provider, "volcengine");
    assert.equal(
      volcEnvelope.data.endpoint,
      "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse",
    );
    assert.doesNotMatch(volcPlan.stdout, /bundle volcengine v3 plan/);

    const expectedState = process.env.JIANYING_EXPECT_BUNDLE_STATE;
    if (expectedState) {
      assert.equal(ready.manifest.contract_state, expectedState);
    }
  } finally {
    fs.rmSync(installRoot, { recursive: true, force: true });
  }
});

test("a not-downloaded official resource crosses Fake GUI into the released Rust CLI", {
  skip: !BUNDLE_ROOT,
}, async (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-resource-acquisition-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installRoot = path.join(root, "runtime");
  installBundle({ bundleRoot: BUNDLE_ROOT, installRoot });
  const env = { HOME: root, PATH: "/usr/bin:/bin", JIANYING_CLI_INSTALL_ROOT: installRoot };
  const entitlementPath = path.join(root, "entitlement.json");
  fs.writeFileSync(entitlementPath, JSON.stringify({
    schema_version: "jianying-entitlement/v1", edition: "professional", status: "active", source: "gui_observed",
    observed_at_epoch_seconds: 1_795_000_000, expires_at_epoch_seconds: 1_796_000_000,
    capabilities: ["official_assets.professional"],
  }));
  const mediaPath = path.join(root, "travel-music.m4a");
  let inspected = false;
  const adapter = {
    identity: { kind: "fake_gui", editor_bundle: "com.lemon.lvpro", editor_version: "11.5.13243", adapter_version: "1" },
    async search() { return [{ schema: "jianying-resource-candidate/v1", candidate_id: "music-travel-release",
      domain: "music", title: "旅行轻快发布包", provider: "jianying_official", resource_id: "jy-music-travel-release",
      edition: "professional", download_state: "not_downloaded", styles: ["vlog"], moods: ["happy"], tempos: ["upbeat"],
      aspect_ratios: ["16:9"], channels: ["douyin"], allowed_usages: ["personal"], cost_microunits: 0,
      terms_reference: "jianying://terms/music/jy-music-travel-release", restrictions: [], preview_only: false, rank: 1,
      duration_ms: 90_000 }]; },
    async triggerDownload() { return { request_id: "release-download" }; },
    async inspectResource(value) { inspected = true; fs.writeFileSync(mediaPath, "released-cli-official-resource");
      return { ...value, download_state: "downloaded", local_path: mediaPath }; },
    async collectEvidence(value) { return { resource_id: value.resource_id, surface_id: "music.recommended",
      entitlement_marker: "professional", observed_at: "2026-11-14T22:13:20.000Z" }; },
  };
  const query = { schema: "jianying-native-resource-query/v1", request_id: "vlog-release-resource", domain: "music",
    keywords: ["旅行"], filters: { styles: ["vlog"], moods: ["happy"], tempos: ["upbeat"], aspect_ratios: ["16:9"],
      edition: "professional", usage: "personal", channel: "douyin", minimum_duration_ms: 10_000,
      maximum_duration_ms: 180_000, maximum_cost_microunits: 0, at_epoch_seconds: 1_795_000_000 },
    selection: { strategy: "ranked", maximum_candidates: 10 } };
  const result = await acquireOfficialResource({ query, adapter, entitlementPath, stateRoot: path.join(root, "state"),
    atEpochSeconds: 1_795_000_000, poll: { maximum_attempts: 2, interval_ms: 0 },
    cliRunner: (request) => runJsonCommand({ ...request, env, pluginRoot: ROOT }) });
  assert.equal(inspected, true);
  assert.equal(result.state, "ready");
  assert.equal(result.cli.register.status, "registered");
  assert.equal(result.cli.preflight.status, "ready");
});

test("basic, professional, limited-free and usage-conflict resource gates form a released CLI matrix", {
  skip: !BUNDLE_ROOT,
}, async (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-resource-matrix-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installRoot = path.join(root, "runtime");
  installBundle({ bundleRoot: BUNDLE_ROOT, installRoot });
  const env = { HOME: root, PATH: "/usr/bin:/bin", JIANYING_CLI_INSTALL_ROOT: installRoot };
  const makeCandidate = (name, overrides = {}) => ({ schema: "jianying-resource-candidate/v1",
    candidate_id: name, domain: "music", title: name, provider: "jianying_official", resource_id: `jy-${name}`,
    edition: "basic", download_state: "not_downloaded", styles: ["vlog"], moods: ["happy"], tempos: ["upbeat"],
    aspect_ratios: ["9:16"], channels: ["douyin"], allowed_usages: ["personal"], cost_microunits: 0,
    terms_reference: `jianying://terms/music/jy-${name}`, restrictions: [], preview_only: false, rank: 1,
    duration_ms: 30_000, ...overrides });
  const makeQuery = (name, edition, usage = "personal") => ({ schema: "jianying-native-resource-query/v1",
    request_id: `matrix-${name}`, domain: "music", keywords: [name], filters: { styles: ["vlog"], moods: ["happy"],
      tempos: ["upbeat"], aspect_ratios: ["9:16"], edition, usage, channel: "douyin",
      minimum_duration_ms: 1_000, maximum_duration_ms: 60_000, maximum_cost_microunits: 0,
      at_epoch_seconds: 1_795_000_000 }, selection: { strategy: "ranked", maximum_candidates: 2 } });
  const acquire = async (name, edition) => {
    const candidate = makeCandidate(name, { edition });
    const entitlementPath = path.join(root, `${name}-entitlement.json`);
    fs.writeFileSync(entitlementPath, JSON.stringify({ schema_version: "jianying-entitlement/v1", edition,
      status: "active", source: "gui_observed", observed_at_epoch_seconds: 1_795_000_000,
      expires_at_epoch_seconds: 1_796_000_000, capabilities: [`official_assets.${edition}`] }));
    const mediaPath = path.join(root, `${name}.m4a`);
    const adapter = { identity: { kind: "fake_gui", editor_bundle: "com.lemon.lvpro",
      editor_version: "11.5.13243", adapter_version: "1" }, async search() { return [candidate]; },
      async triggerDownload() { return { request_id: `download-${name}` }; }, async inspectResource(value) {
        fs.writeFileSync(mediaPath, name); return { ...value, download_state: "downloaded", local_path: mediaPath }; },
      async collectEvidence(value) { return { resource_id: value.resource_id, entitlement_marker: edition,
        observed_at: "2026-11-14T22:13:20.000Z" }; } };
    return acquireOfficialResource({ query: makeQuery(name, edition), adapter, entitlementPath,
      stateRoot: path.join(root, "state"), atEpochSeconds: 1_795_000_000,
      poll: { maximum_attempts: 2, interval_ms: 0 },
      cliRunner: request => runJsonCommand({ ...request, env, pluginRoot: ROOT }) });
  };
  const basic = await acquire("basic", "basic");
  const professional = await acquire("professional", "professional");
  assert.deepEqual([basic.cli.preflight.status, professional.cli.preflight.status], ["ready", "ready"]);

  let blockedCliCalls = 0;
  const rejected = async (name, candidate, query) => {
    const adapter = { identity: { kind: "fake_gui", editor_bundle: "com.lemon.lvpro",
      editor_version: "11.5.13243", adapter_version: "1" }, async search() { return [candidate]; },
      async triggerDownload() { throw new Error("blocked resource must not download"); },
      async inspectResource(value) { return value; }, async collectEvidence() { return {}; } };
    await assert.rejects(() => acquireOfficialResource({ query, adapter, entitlementPath: path.join(root, `${name}.json`),
      stateRoot: path.join(root, "blocked"), atEpochSeconds: 1_795_000_000,
      cliRunner: () => { blockedCliCalls += 1; } }), error => error.code === "resource_candidate_unavailable");
  };
  await rejected("expired", makeCandidate("expired", { limited_free_until_epoch_seconds: 1_794_999_999 }),
    makeQuery("expired", "basic"));
  await rejected("usage-conflict", makeCandidate("usage-conflict"), makeQuery("usage-conflict", "basic", "commercial"));
  await rejected("unknown-edition", makeCandidate("unknown-edition", { edition: "unknown" }),
    makeQuery("unknown-edition", "any"));
  await rejected("preview-only", makeCandidate("preview-only", { preview_only: true }),
    makeQuery("preview-only", "basic"));

  const failedDownload = makeCandidate("download-failed");
  const failedAdapter = { identity: { kind: "fake_gui", editor_bundle: "com.lemon.lvpro",
    editor_version: "11.5.13243", adapter_version: "1" }, async search() { return [failedDownload]; },
    async triggerDownload() { return { request_id: "download-failed" }; }, async inspectResource(value) {
      return { ...value, download_state: "failed", failure_code: "network_unavailable" }; },
    async collectEvidence() { throw new Error("failed download must not collect evidence"); } };
  await assert.rejects(() => acquireOfficialResource({ query: makeQuery("download-failed", "basic"),
    adapter: failedAdapter, entitlementPath: path.join(root, "download-failed.json"), stateRoot: path.join(root, "blocked"),
    poll: { maximum_attempts: 1, interval_ms: 0 }, cliRunner: () => { blockedCliCalls += 1; } }),
  error => error.code === "resource_download_failed");

  const expiredAccountPath = path.join(root, "expired-account-entitlement.json");
  fs.writeFileSync(expiredAccountPath, JSON.stringify({ schema_version: "jianying-entitlement/v1", edition: "basic",
    status: "active", source: "gui_observed", observed_at_epoch_seconds: 1_794_000_000,
    expires_at_epoch_seconds: 1_794_999_999, capabilities: ["official_assets.basic"] }));
  const expiredMedia = path.join(root, "expired-account.m4a");
  fs.writeFileSync(expiredMedia, "expired account fixture");
  const expiredCandidate = makeCandidate("expired-account", { download_state: "downloaded", local_path: expiredMedia });
  const expiredAdapter = { identity: { kind: "fake_gui", editor_bundle: "com.lemon.lvpro",
    editor_version: "11.5.13243", adapter_version: "1" }, async search() { return [expiredCandidate]; },
    async triggerDownload() { throw new Error("already downloaded"); }, async inspectResource(value) { return value; },
    async collectEvidence(value) { return { resource_id: value.resource_id, entitlement_marker: "basic",
      observed_at: "2026-11-14T22:13:20.000Z" }; } };
  await assert.rejects(() => acquireOfficialResource({ query: makeQuery("expired-account", "basic"),
    adapter: expiredAdapter, entitlementPath: expiredAccountPath, stateRoot: path.join(root, "expired-account-state"),
    atEpochSeconds: 1_795_000_000, poll: { maximum_attempts: 1, interval_ms: 0 },
    cliRunner: request => runJsonCommand({ ...request, env, pluginRoot: ROOT }) }), error => {
    assert.equal(error.code, "official_resource_cli_failed");
    assert.equal(error.details.response.error.type, "entitlement_expired");
    return true;
  });
  assert.equal(blockedCliCalls, 0);
});

test("an embedded official effect crosses Fake GUI into the released Rust CLI as a draft resource", {
  skip: !BUNDLE_ROOT,
}, async (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-draft-resource-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installRoot = path.join(root, "runtime");
  installBundle({ bundleRoot: BUNDLE_ROOT, installRoot });
  const env = { HOME: root, PATH: "/usr/bin:/bin", JIANYING_CLI_INSTALL_ROOT: installRoot };
  const entitlementPath = path.join(root, "entitlement.json");
  fs.writeFileSync(entitlementPath, JSON.stringify({ schema_version: "jianying-entitlement/v1",
    edition: "professional", status: "active", source: "gui_observed", observed_at_epoch_seconds: 1_795_000_000,
    expires_at_epoch_seconds: 1_796_000_000, capabilities: ["official_assets.professional"] }));
  const draft = path.join(root, "draft");
  fs.mkdirSync(draft, { recursive: true });
  fs.writeFileSync(path.join(draft, "draft_content.json"), JSON.stringify({ materials: { video_effects: [
    { id: "effect-node-1", name: "科技感", resource_id: "remote-effect" },
  ] }, tracks: [] }));
  const candidate = { schema: "jianying-resource-candidate/v1", candidate_id: "effect-release",
    domain: "effect", title: "科技感", provider: "jianying_official", resource_id: "jy-effect-release",
    edition: "professional", download_state: "downloaded", styles: [], moods: [], tempos: [], aspect_ratios: [],
    channels: ["douyin"], allowed_usages: ["personal"], cost_microunits: 0,
    terms_reference: "jianying://terms/effect/jy-effect-release", restrictions: [], preview_only: false, rank: 1,
    draft_path: draft, draft_resource_id: "effect-node-1" };
  const adapter = { identity: { kind: "fake_gui", editor_bundle: "com.lemon.lvpro",
    editor_version: "11.5.13243", adapter_version: "1" }, async search() { return [candidate]; },
    async triggerDownload() { throw new Error("already materialized in the isolated draft"); },
    async inspectResource(value) { return value; }, async collectEvidence(value) { return {
      resource_id: value.resource_id, surface_id: "effects.hot", entitlement_marker: "professional",
      observed_at: "2026-11-14T22:13:20.000Z" }; } };
  const query = { schema: "jianying-native-resource-query/v1", request_id: "effect-release-resource", domain: "effect",
    keywords: ["科技"], filters: { styles: [], moods: [], tempos: [], aspect_ratios: [], edition: "professional",
      usage: "personal", channel: "douyin", maximum_cost_microunits: 0, at_epoch_seconds: 1_795_000_000 },
    selection: { strategy: "ranked", maximum_candidates: 10 } };
  const result = await acquireOfficialResource({ query, adapter, entitlementPath, stateRoot: path.join(root, "state"),
    atEpochSeconds: 1_795_000_000, poll: { maximum_attempts: 1, interval_ms: 0 },
    cliRunner: request => runJsonCommand({ ...request, env, pluginRoot: ROOT }) });
  assert.equal(result.receipt.identity.kind, "draft_resource");
  assert.equal(result.receipt.identity.resource_id, "effect-node-1");
  assert.equal(result.cli.register.status, "registered");
  assert.equal(result.cli.preflight.status, "ready");
});

test("the released Rust CLI surface inventory compiles semantic timeline operations without coordinates", {
  skip: !BUNDLE_ROOT,
}, async (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-real-control-catalog-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installRoot = path.join(root, "runtime");
  installBundle({ bundleRoot: BUNDLE_ROOT, installRoot });
  const env = { HOME: root, PATH: "/usr/bin:/bin", JIANYING_CLI_INSTALL_ROOT: installRoot };
  const probed = await probeNativeControlContracts({ cliRunner: (request) => runJsonCommand({
    ...request, env, pluginRoot: ROOT,
  }) });
  assert.equal(probed.validation.surface_count, 50);
  assert.equal(probed.validation.unresolved_surface_ids.length, 5);
  assert.equal(probed.coverage.can_claim_complete, false);
  const plan = compileNativeControlPlan({ catalog: probed.catalog, inventory: probed.inventory,
    adapters: { draft_protocol: true }, requests: [{ request_id: "release-split",
      semantic_id: "timeline.segment.split", arguments: { draft: path.join(root, "draft"),
        segment_id: "segment-1", at: "1s" } }] });
  assert.deepEqual(plan.steps[0].cli.args.slice(0, 2), ["timeline", "split"]);
  assert.equal(plan.steps[0].route, "draft_protocol");
  assert.ok(plan.steps[0].surface_ids.includes("edit.split"));
  assert.ok(plan.steps[0].surface_ids.includes("canvas.segment.split") === false);
  assert.doesNotMatch(JSON.stringify(plan), /screen_coordinate|coordinates|"x"|"y"/);
});
