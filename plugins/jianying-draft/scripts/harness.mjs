#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import os from "node:os";
import { fileURLToPath } from "node:url";

import { AdapterError, handshake, runJob, runJsonCommand, sha256File } from "./runtime_adapter.mjs";
import { loadPlanningData, planVideo } from "./video_planner.mjs";
import { loadOpenCatalog, readCreativeBrief, routeWorkflow } from "./open_workflow.mjs";
import { buildWorkflowPlan } from "./workflow_plan.mjs";
import { compileWorkflow } from "./workflow_compiler.mjs";
import { WorkflowRuntime, verifyDraftArtifact } from "./workflow_runtime.mjs";
import { collectMediaQualityEvidence, collectProxyEvidence } from "./quality_proxy_evidence.mjs";
import { buildEvidenceBundle } from "./quality_evidence.mjs";
import { createManualEvaluator, createTechnicalEvaluator, runEvaluator } from "./quality_evaluator.mjs";
import { createRemoteModelEvaluator } from "./remote_quality_evaluator.mjs";
import {
  applyRetargetProposal,
  buildComparativeEvaluationContext,
  buildMacroRevisionRequest,
  buildRetargetProposal,
  buildVisualReferenceSet,
} from "./quality_iteration.mjs";
import { compileNativeControlPlan, probeNativeControlContracts } from "./native_control_orchestration.mjs";
import { routeNativeResourceQuery } from "./native_resource_acquisition.mjs";
import { buildHomeFolderPlan, executeHomeFolderOperation } from "./home_folder_orchestration.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CONTRACT = JSON.parse(fs.readFileSync(path.join(ROOT, "runtime", "harness_contract.json"), "utf8"));
const EVIDENCE_LEVELS = CONTRACT.resultContract.evidenceLevels;
const CREATE_EVIDENCE_LEVELS = new Set(["structural", "editable_draft"]);
const OPEN_WORKFLOW_ROLLBACK_COMMANDS = new Set([
  "workflow-plan", "workflow-check", "workflow-compile", "workflow-start",
  "workflow-approve", "workflow-execute", "workflow-resume", "workflow-confirm-cancelled",
]);

function digest(value) {
  return crypto.createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

function atomicJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  fs.renameSync(temporary, file);
}

function record(state, event, details = {}) {
  state.history ??= [];
  state.history.push({ sequence: state.history.length + 1, event, stage: state.stage, details });
}

function filesUnder(root) {
  const files = [];
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const candidate = path.join(root, entry.name);
    if (entry.isDirectory()) files.push(...filesUnder(candidate));
    if (entry.isFile()) files.push(candidate);
  }
  return files.sort();
}

function skillDigest(skillRoot) {
  const hash = crypto.createHash("sha256");
  for (const file of filesUnder(skillRoot)) {
    hash.update(path.relative(skillRoot, file).split(path.sep).join("/"));
    hash.update("\0");
    hash.update(sha256File(file));
    hash.update("\n");
  }
  return hash.digest("hex");
}

export function riskFor(operation) {
  for (const [level, policy] of Object.entries(CONTRACT.riskLevels)) {
    if (policy.operations.includes(operation)) return { level, ...policy };
  }
  throw new AdapterError("risk_unclassified", `operation ${operation} has no risk classification`);
}

function requireEvidenceLevel(level, allowed = EVIDENCE_LEVELS) {
  const supported = allowed instanceof Set ? allowed.has(level) : allowed.includes(level);
  if (!supported) {
    throw new AdapterError(
      "evidence_level_invalid",
      `evidence level ${level} is not valid for this workflow`,
      { actual: level, allowed: [...allowed] },
      ["request an evidence level produced by the selected CLI operation"],
    );
  }
}

export function inventoryMedia({ mediaPaths, env = process.env, pluginRoot = ROOT }) {
  return mediaPaths.map((mediaPath) => {
    const absolute = path.resolve(mediaPath);
    if (!fs.statSync(absolute).isFile()) {
      throw new AdapterError("media_missing", `media file does not exist: ${absolute}`);
    }
    const result = runJsonCommand({ args: ["probe", absolute], env, pluginRoot });
    if (result.exitCode !== 0 || result.envelope?.ok !== true) {
      throw new AdapterError("probe_failed", `media probe failed: ${absolute}`, { response: result.envelope });
    }
    return { path: absolute, sha256: sha256File(absolute), facts: result.envelope.data };
  });
}

function planToProject(plan) {
  const materials = [];
  const tracks = (plan.tracks ?? []).map((track, trackIndex) => {
    const kind = track.type ?? track.kind;
    if (!kind) {
      throw new AdapterError("plan_invalid", `track ${trackIndex} is missing type`);
    }
    if (track.kind !== undefined) {
      track.type = kind;
      delete track.kind;
    }
    const segments = (track.segments ?? []).map((segment, segmentIndex) => {
      const id = `segment-${trackIndex}-${segmentIndex}`;
      const range = { start_us: segment.start_us, duration_us: segment.duration_us };
      if (kind === "video" || kind === "audio") {
        if (!segment.source) {
          throw new AdapterError("plan_invalid", `track ${trackIndex} segment ${segmentIndex} is missing source`);
        }
        const materialId = `material-${trackIndex}-${segmentIndex}`;
        materials.push({
          type: kind === "video" && segment.photo ? "image" : kind,
          id: materialId,
          path: segment.source,
        });
        return {
          type: kind,
          id,
          range,
          material_id: materialId,
          source_range: {
            start_us: segment.source_start_us ?? 0,
            duration_us: segment.source_duration_us ?? segment.duration_us,
          },
          // 与 Rust domain_compat::from_v1_plan 的构造器默认值保持一致；
          // v1 的完整速度和音量语义由 compatibility payload 无损承载。
          speed: 1,
          volume: 1,
        };
      }
      if (kind === "text") return { type: kind, id, range, text: segment.text ?? "" };
      if (kind === "sticker") {
        return { type: kind, id, range, resource_id: segment.resource_id ?? "" };
      }
      if (kind === "filter") {
        const filter = segment.filters?.[0];
        if (!filter) {
          throw new AdapterError("plan_invalid", `track ${trackIndex} segment ${segmentIndex} is missing filters[0]`);
        }
        return {
          type: kind,
          id,
          range,
          resource_id: filter.name,
          intensity: segment.intensity ?? filter.intensity ?? 100,
        };
      }
      if (kind === "effect") {
        const effect = segment.effects?.[0];
        if (!effect) {
          throw new AdapterError("plan_invalid", `track ${trackIndex} segment ${segmentIndex} is missing effects[0]`);
        }
        return {
          type: kind,
          id,
          range,
          resource_id: effect.name,
          parameters: segment.params ?? effect.params ?? {},
        };
      }
      throw new AdapterError("plan_invalid", `unsupported track type ${kind}`);
    });
    return {
      id: track.name ? `${track.name}-${trackIndex}` : `${kind}-${trackIndex}`,
      kind,
      segments,
    };
  });
  return {
    name: plan.name,
    width: plan.canvas?.width,
    height: plan.canvas?.height,
    frame_rate: { numerator: plan.canvas?.fps, denominator: 1 },
    timeline: { tracks },
    materials,
  };
}

function validatePlanShape(plan) {
  if (plan?.schema !== "jianying-cli-plan/v1") {
    throw new AdapterError("plan_invalid", "intent.plan.schema must be jianying-cli-plan/v1");
  }
  if (typeof plan.name !== "string" || plan.name.trim() === "") {
    throw new AdapterError("plan_invalid", "intent.plan.name must not be blank");
  }
  const { width, height, fps } = plan.canvas ?? {};
  if (![width, height, fps].every(Number.isInteger)) {
    throw new AdapterError("plan_invalid", "intent.plan.canvas requires integer width, height, and fps");
  }
  if (!Array.isArray(plan.tracks) || plan.tracks.length === 0) {
    throw new AdapterError("plan_invalid", "intent.plan.tracks must not be empty");
  }
  for (const [trackIndex, track] of plan.tracks.entries()) {
    if (!Array.isArray(track.segments) || track.segments.length === 0) {
      throw new AdapterError("plan_invalid", `track ${trackIndex} segments must not be empty`);
    }
    for (const [segmentIndex, segment] of track.segments.entries()) {
      if (!Number.isInteger(segment.start_us) || !Number.isInteger(segment.duration_us) || segment.start_us < 0 || segment.duration_us <= 0) {
        throw new AdapterError(
          "plan_invalid",
          `track ${trackIndex} segment ${segmentIndex} requires a non-negative integer start_us and positive integer duration_us`,
        );
      }
    }
  }
}

export function compileJob({ intent, inventory, outputPath }) {
  const operation = intent.operation ?? "create";
  if (operation === "edit") {
    return compileEditJob(intent, outputPath);
  }
  if (operation !== "create") {
    throw new AdapterError("operation_invalid", `unsupported Harness operation: ${operation}`);
  }
  const known = new Set(inventory.map((item) => item.path));
  const plan = structuredClone(intent.plan);
  validatePlanShape(plan);
  for (const track of plan.tracks ?? []) {
    for (const segment of track.segments ?? []) {
      if (segment.source) {
        segment.source = path.resolve(segment.source);
        if (!known.has(segment.source)) {
          throw new AdapterError("material_not_in_inventory", `material was not probed: ${segment.source}`);
        }
      }
    }
  }
  return {
    schema: "jianying-job/v2",
    operation: "create",
    project: { type: "new", project: planToProject(plan) },
    compatibility: { schema: "jianying-cli-plan/v1", payload: plan },
  };
}

function compileEditJob(intent, outputPath) {
  if (typeof intent.sourcePath !== "string" || intent.sourcePath.trim() === "") {
    throw new AdapterError("edit_invalid", "edit intent.sourcePath must not be blank");
  }
  const source = path.resolve(intent.sourcePath);
  const output = typeof outputPath === "string" && outputPath.trim() !== ""
    ? path.resolve(outputPath)
    : null;
  if (!output) {
    throw new AdapterError("edit_invalid", "edit outputPath must not be blank");
  }
  if (source === output) {
    throw new AdapterError("edit_invalid", "edit sourcePath and outputPath must be distinct");
  }
  if (!fs.existsSync(source) || !fs.statSync(source).isDirectory()) {
    throw new AdapterError("edit_source_missing", `edit source draft does not exist: ${source}`);
  }
  if (!Array.isArray(intent.operations) || intent.operations.length === 0) {
    throw new AdapterError("edit_invalid", "edit intent.operations must not be empty");
  }
  const operations = structuredClone(intent.operations);
  for (const [index, edit] of operations.entries()) {
    if (["add_material", "add_segment"].includes(edit?.operation)) {
      throw new AdapterError(
        "edit_operation_not_supported",
        `edit operation ${edit.operation} is not yet supported by the locked Rust CLI`,
        { index, operation: edit.operation },
        ["use replace_text, move_segment, or remove_segment"],
      );
    }
    if (!["replace_text", "move_segment", "remove_segment"].includes(edit?.operation)) {
      throw new AdapterError("edit_invalid", `unknown edit operation at index ${index}`);
    }
    if (typeof edit.segment_id !== "string" || edit.segment_id.trim() === "") {
      throw new AdapterError("edit_invalid", `edit operation ${index} requires segment_id`);
    }
    if (edit.operation === "replace_text"
      && (typeof edit.text !== "string" || edit.text.trim() === "")) {
      throw new AdapterError("edit_invalid", `replace_text operation ${index} requires non-blank text`);
    }
    if (edit.operation === "move_segment") {
      const { start_us: startUs, duration_us: durationUs } = edit.target ?? {};
      if (!Number.isInteger(startUs) || startUs < 0
        || !Number.isInteger(durationUs) || durationUs <= 0) {
        throw new AdapterError(
          "edit_invalid",
          `move_segment operation ${index} requires a non-negative integer start_us and positive integer duration_us`,
        );
      }
    }
  }
  return {
    schema: "jianying-job/v2",
    operation: "edit",
    project: { type: "existing", source, output },
    operations,
  };
}

export class Harness {
  constructor({ stateRoot, env = process.env, pluginRoot = ROOT }) {
    this.stateRoot = path.resolve(stateRoot);
    this.env = env;
    this.pluginRoot = pluginRoot;
  }

  sessionCheck() {
    // SessionStart hook entry: package integrity only, never exits non-zero.
    // External CLI / media tools / credentials are first-use setup owned by
    // the jianying-setup and jianying-use skills, so they are not checked here.
    let problems = [];
    try {
      const skillLock = JSON.parse(fs.readFileSync(path.join(this.pluginRoot, "skills.lock.json"), "utf8"));
      for (const source of skillLock.sources ?? []) {
        for (const skill of source.skills ?? []) {
          const skillRoot = path.join(this.pluginRoot, source.dest, skill);
          const actual = fs.existsSync(skillRoot) ? skillDigest(skillRoot) : null;
          if (actual !== source.sha256?.[skill]) {
            problems.push(`skill ${skill} 摘要不匹配（包不完整，建议重装插件）`);
          }
        }
      }
    } catch (error) {
      problems.push(`skills.lock.json 不可读：${error.message ?? String(error)}`);
    }
    if (problems.length > 0) {
      console.log(`剪映编辑环境告警：${problems.join("；")}`);
    }
    return { ready: problems.length === 0, problems };
  }

  doctor() {
    const result = runJsonCommand({ args: ["doctor"], env: this.env, pluginRoot: this.pluginRoot });
    const cliReady = result.exitCode === 0 && result.envelope?.ok === true;
    const skillLock = JSON.parse(fs.readFileSync(path.join(this.pluginRoot, "skills.lock.json"), "utf8"));
    const skillChecks = [];
    for (const source of skillLock.sources ?? []) {
      for (const skill of source.skills ?? []) {
        const skillRoot = path.join(this.pluginRoot, source.dest, skill);
        const actual = fs.existsSync(skillRoot) ? skillDigest(skillRoot) : null;
        skillChecks.push({ skill, ready: actual === source.sha256?.[skill], actual });
      }
    }
    const data = result.envelope?.data ?? {};
    const checks = {
      cli: { ready: cliReady, version: result.ready?.version, schema: result.ready?.capabilitySchema },
      skills: { ready: skillChecks.every((item) => item.ready), items: skillChecks },
      mediaTools: { ready: Boolean(data.ffprobe && data.ffmpeg), ffprobe: data.ffprobe, ffmpeg: data.ffmpeg },
      draftRoots: { ready: Array.isArray(data.draft_roots), items: data.draft_roots ?? [] },
      runtimeProfile: { ready: Array.isArray(data.editors_running), editorsRunning: data.editors_running ?? [] },
    };
    return {
      ready: Object.values(checks).every((check) => check.ready),
      checks,
      result: result.envelope,
    };
  }

  start({ intent, mediaPaths = [], outputPath, evidenceLevel = "editable_draft" }) {
    requireEvidenceLevel(evidenceLevel, CREATE_EVIDENCE_LEVELS);
    const operation = intent.operation ?? "create";
    const inventory = operation === "edit"
      ? []
      : inventoryMedia({ mediaPaths, env: this.env, pluginRoot: this.pluginRoot });
    const job = compileJob({ intent, inventory, outputPath });
    const taskId = `jy-${digest({ intent, inventory, outputPath }).slice(0, 20)}`;
    const taskRoot = path.join(this.stateRoot, taskId);
    const jobPath = path.join(taskRoot, "job.json");
    atomicJson(jobPath, job);
    const state = {
      schema: "jianying-harness-task/v1",
      taskId,
      stage: "approve",
      terminalState: null,
      inputDigest: digest(intent),
      operation,
      sourcePath: operation === "edit" ? path.resolve(intent.sourcePath) : null,
      inventory,
      jobPath,
      outputPath: path.resolve(outputPath),
      cliTaskId: null,
      approvals: [],
      evidenceLevel,
      verifiedStages: ["intake", "inventory", "plan"],
      lastResult: null,
      history: [],
    };
    record(state, "task.started", { inputDigest: state.inputDigest });
    this.save(state);
    return state;
  }

  approve(taskId, approval) {
    const state = this.load(taskId);
    const expected = this.binding(state);
    for (const key of ["command", "argumentsDigest", "cwd", "target", "taskId"]) {
      if (approval[key] !== expected[key]) {
        throw new AdapterError("approval_scope_mismatch", `approval ${key} does not match the task`);
      }
    }
    if (Date.parse(approval.expiresAt) <= Date.now()) {
      throw new AdapterError("approval_expired", "approval has expired");
    }
    state.approvals.push({ ...approval, used: false });
    state.stage = "execute";
    record(state, "approval.granted", { command: approval.command, target: approval.target });
    this.save(state);
    return state;
  }

  binding(state) {
    return {
      command: `job.run.${state.operation ?? "create"}`,
      argumentsDigest: digest({
        jobSha256: sha256File(state.jobPath),
        sourcePath: state.sourcePath,
        outputPath: state.outputPath,
      }),
      cwd: path.dirname(state.jobPath),
      target: state.outputPath,
      taskId: state.taskId,
    };
  }

  execute(taskId) {
    const state = this.load(taskId);
    const risk = riskFor(`job.run.${state.operation ?? "create"}`);
    if (risk.approval !== "none") {
      const approval = state.approvals.find((item) => !item.used && Date.parse(item.expiresAt) > Date.now());
      if (!approval) throw new AdapterError("approval_required", "a task-scoped approval is required");
      approval.used = true;
    }
    const result = runJob({
      jobPath: state.jobPath,
      outputPath: state.outputPath,
      env: this.env,
      pluginRoot: this.pluginRoot,
    });
    state.cliTaskId = result.taskId;
    state.lastResult = result.envelope;
    if (result.exitCode === 0 && result.envelope?.ok === true) {
      state.stage = "deliver";
      state.terminalState = "completed";
      state.verifiedStages = [...new Set([...state.verifiedStages, "approve", "execute", "verify", "deliver"])];
      record(state, "task.completed", { cliTaskId: state.cliTaskId, evidenceLevel: state.evidenceLevel });
    } else {
      state.stage = "execute";
      state.terminalState = result.error?.type === "recoverable" ? "recoverable" : "failed";
      record(state, "task.execution_failed", { terminalState: state.terminalState, cliTaskId: state.cliTaskId });
    }
    this.save(state);
    return state;
  }

  resume(taskId) {
    const state = this.load(taskId);
    if (state.terminalState === "completed") return state;
    if (state.verifiedStages.includes("execute")) return state;
    return this.execute(taskId);
  }

  list() {
    if (!fs.existsSync(this.stateRoot)) return [];
    return fs.readdirSync(this.stateRoot, { withFileTypes: true })
      .filter((entry) => entry.isDirectory() && fs.existsSync(path.join(this.stateRoot, entry.name, "state.json")))
      .map((entry) => this.load(entry.name))
      .map((state) => ({
        taskId: state.taskId,
        stage: state.stage,
        terminalState: state.terminalState,
        evidenceLevel: state.evidenceLevel,
        cliTaskId: state.cliTaskId,
      }));
  }

  show(taskId) {
    return this.load(taskId);
  }

  cancel(taskId) {
    const state = this.load(taskId);
    if (state.terminalState === "completed") {
      throw new AdapterError("task_terminal", "a completed task cannot be cancelled");
    }
    state.terminalState = "cancelled";
    record(state, "task.cancelled");
    this.save(state);
    return state;
  }

  retry(taskId) {
    const state = this.load(taskId);
    if (!["recoverable", "failed"].includes(state.terminalState)) {
      throw new AdapterError("task_not_retryable", "only failed or recoverable tasks can be retried");
    }
    state.terminalState = null;
    state.stage = "approve";
    state.approvals = [];
    record(state, "task.retry_requested", { preservedStages: state.verifiedStages });
    this.save(state);
    return state;
  }

  audit(taskId) {
    const state = this.load(taskId);
    return {
      taskId: state.taskId,
      inputDigest: state.inputDigest,
      inventory: state.inventory.map((item) => ({ sha256: item.sha256, facts: item.facts })),
      cliTaskId: state.cliTaskId,
      approvals: state.approvals.map((item) => ({
        command: item.command,
        argumentsDigest: item.argumentsDigest,
        target: item.target,
        expiresAt: item.expiresAt,
        used: item.used,
      })),
      history: state.history ?? [],
      terminalState: state.terminalState,
      evidenceLevel: state.evidenceLevel,
    };
  }

  assessDelivery(taskId, requestedLevel) {
    const state = this.load(taskId);
    requireEvidenceLevel(requestedLevel);
    requireEvidenceLevel(state.evidenceLevel);
    const levels = EVIDENCE_LEVELS;
    const actual = state.terminalState === "completed" ? state.evidenceLevel : "structural";
    return {
      taskId,
      requestedLevel,
      actualLevel: actual,
      satisfied: levels.indexOf(actual) >= levels.indexOf(requestedLevel),
      terminalState: state.terminalState,
    };
  }

  load(taskId) {
    return JSON.parse(fs.readFileSync(path.join(this.stateRoot, taskId, "state.json"), "utf8"));
  }

  save(state) {
    atomicJson(path.join(this.stateRoot, state.taskId, "state.json"), state);
  }
}

function parseCli(argv) {
  const argumentsList = [...argv];
  const stateIndex = argumentsList.indexOf("--state-root");
  let stateRoot = process.env.JIANYING_PLUGIN_STATE_ROOT;
  if (stateIndex >= 0) {
    stateRoot = argumentsList[stateIndex + 1];
    argumentsList.splice(stateIndex, 2);
  }
  return {
    command: argumentsList.shift(),
    argumentsList,
    stateRoot: stateRoot
      ? path.resolve(stateRoot)
      : path.join(os.homedir(), ".partme", "jianying-draft", "tasks"),
  };
}

function readJsonFile(file) {
  return JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
}

async function main() {
  const { command, argumentsList, stateRoot } = parseCli(process.argv.slice(2));
  if (process.env.JIANYING_OPEN_WORKFLOW_DISABLED === "1" && OPEN_WORKFLOW_ROLLBACK_COMMANDS.has(command)) {
    throw new AdapterError("open_workflow_disabled", "Open workflow entry is disabled for rollback; preserve existing state for reconciliation");
  }
  const harness = new Harness({ stateRoot });
  const workflowRuntime = new WorkflowRuntime({ stateRoot,
    executor: (bindings, state) => ({ ok: true, artifacts: bindings.map((binding) => {
      const jobPath = path.join(stateRoot, state.run_id, `${binding.output_id}.job.json`);
      atomicJson(jobPath, binding.job);
      const result = runJob({ jobPath, outputPath: binding.output_path });
      if (result.exitCode !== 0 || result.envelope?.ok !== true) {
        const error = new AdapterError("workflow_job_failed", `Job failed for ${binding.output_id}`, { result });
        if (result.taskId && result.error?.type === "recoverable") error.outcome = "unknown";
        throw error;
      }
      return { output_id: binding.output_id, path: binding.output_path, task_id: result.taskId,
        result_digest: digest(result.envelope) };
    }) }),
    verifier: (artifacts, state) => {
      const evidence = []; const issues = [];
      for (const artifact of artifacts) {
        const binding = state.compilation.job_bindings.find((item) => item.output_id === artifact.output_id);
        const segments = binding.job.project.project.timeline.tracks.flatMap((track) => track.segments ?? []);
        const duration = segments.reduce((maximum, segment) =>
          Math.max(maximum, segment.range.start_us + segment.range.duration_us), 0);
        const result = verifyDraftArtifact(artifact.path, { duration_us: duration });
        evidence.push(...result.evidence.map((item) => ({ output_id: artifact.output_id, level: "structural", ...item })));
        issues.push(...result.issues.map((item) => ({ output_id: artifact.output_id, ...item })));
      }
      return { ok: issues.length === 0, evidence, issues };
    } });
  let data;
  switch (command) {
    case "quality-evidence": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-evidence requires REQUEST.json");
      }
      const request = readJsonFile(argumentsList[0]);
      const options = { proxyPath: request.proxyPath, workflowId: request.workflowId, revision: request.revision,
        outputId: request.outputId, observedAt: request.observedAt };
      const proxy = collectProxyEvidence(options);
      const media = collectMediaQualityEvidence(options);
      data = { artifact: proxy.artifact, probe: proxy.probe, media: media.analysis,
        evaluation_evidence: [proxy.evidence, media.evidence, ...(media.audio_evidence?[media.audio_evidence]:[])],
        bundle: buildEvidenceBundle({ workflowId: request.workflowId, revision: request.revision,
          outputId: request.outputId, artifactDigest: proxy.artifact.digest,
          items: [...proxy.bundle_items, media.bundle_item],
          requiredTypes: ["structural", "technical", "creative"] }) };
      break;
    }
    case "quality-evaluate": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-evaluate requires REQUEST.json");
      }
      const request = readJsonFile(argumentsList[0]);
      const adapter = request.kind === "technical"
        ? createTechnicalEvaluator({ version: "1" })
        : createManualEvaluator({ reviewerId: request.reviewerId, version: request.version ?? "1" });
      data = runEvaluator({ adapter, input: request.input, profile: request.profile,
        comparativeContext: request.comparativeContext, context: request.context ?? {} });
      break;
    }
    case "quality-reference-set": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-reference-set requires REQUEST.json");
      }
      data = buildVisualReferenceSet(readJsonFile(argumentsList[0]));
      break;
    }
    case "quality-comparison-context": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-comparison-context requires REQUEST.json");
      }
      data = buildComparativeEvaluationContext(readJsonFile(argumentsList[0]));
      break;
    }
    case "quality-macro-revision": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-macro-revision requires REQUEST.json");
      }
      data = buildMacroRevisionRequest(readJsonFile(argumentsList[0]));
      break;
    }
    case "quality-retarget-propose": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-retarget-propose requires REQUEST.json");
      }
      data = buildRetargetProposal(readJsonFile(argumentsList[0]));
      break;
    }
    case "quality-retarget-apply": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-retarget-apply requires REQUEST.json");
      }
      data = applyRetargetProposal(readJsonFile(argumentsList[0]));
      break;
    }
    case "quality-evaluate-remote": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "quality-evaluate-remote requires REQUEST.json");
      }
      const request = readJsonFile(argumentsList[0]);
      const credential = process.env[request.credentialEnv];
      if (!credential) throw new AdapterError("credential_missing", "remote evaluator credential environment variable is missing");
      const maxUploadBytes = request.maxUploadBytes === undefined
        ? undefined
        : Math.min(request.maxUploadBytes, 7 * 1024 * 1024);
      const adapter = createRemoteModelEvaluator({ provider: request.provider, model: request.model, version: request.version,
        endpoint: request.endpoint, credential, stateRoot: path.join(stateRoot, "remote-evaluation"),
        timeoutMs: request.timeoutMs, maxResponseBytes: request.maxResponseBytes, maxUploadBytes });
      data = await adapter.evaluate({ input: request.input, profile: request.profile, approval: request.approval,
        budget: request.budget, resources: request.resources });
      break;
    }
    case "workflow-plan": {
      if (!argumentsList[0] || argumentsList[0].startsWith("--")) {
        throw new AdapterError("usage_error", "workflow-plan requires BRIEF.json");
      }
      const options = {};
      for (let i = 1; i < argumentsList.length; i += 2) {
        const flag = argumentsList[i];
        if (!["--development-skill-root", "--cursor"].includes(flag) ||
            !argumentsList[i + 1] || argumentsList[i + 1].startsWith("--") || Object.hasOwn(options, flag)) {
          throw new AdapterError("usage_error", "invalid or duplicate workflow-plan option");
        }
        options[flag] = argumentsList[i + 1];
      }
      const catalog = loadOpenCatalog({ developmentSkillRoot: options["--development-skill-root"] });
      const brief = readCreativeBrief(argumentsList[0]);
      data = routeWorkflow(brief, catalog, { cursor: options["--cursor"] });
      if (data.selected_scenes.length) data.workflow_plan = buildWorkflowPlan(brief, data);
      break;
    }
    case "workflow-check": {
      if (!argumentsList[0] || !argumentsList[1] || ![2, 4].includes(argumentsList.length) ||
          (argumentsList.length === 4 && (argumentsList[2] !== "--resources" || !argumentsList[3]))) {
        throw new AdapterError("usage_error", "workflow-check requires PLAN.json ASSET_LEDGER.json [--resources ACQUISITIONS.json]");
      }
      const ready = handshake();
      const plan = readJsonFile(argumentsList[0]);
      data = compileWorkflow({ plan, assetLedger: readJsonFile(argumentsList[1]), decisions: [],
        resourceAcquisitions: argumentsList[3] ? readJsonFile(argumentsList[3]) : [],
        cliIdentity: { version: ready.version, sha256: ready.sha256, jobSchema: ready.jobSchema,
          capabilities: ready.manifest.capabilities } });
      data.cli_identity = { version: ready.version, sha256: ready.sha256, source: ready.source };
      break;
    }
    case "workflow-compile": {
      if (!argumentsList[0] || !argumentsList[1] || !argumentsList[2]) {
        throw new AdapterError("usage_error", "workflow-compile requires PLAN.json ASSET_LEDGER.json DECISIONS.json --out DIR [--resources ACQUISITIONS.json]");
      }
      const outIndex = argumentsList.indexOf("--out");
      const resourcesIndex = argumentsList.indexOf("--resources");
      if (outIndex !== 3 || !argumentsList[4] || ![5, 7].includes(argumentsList.length) ||
          (argumentsList.length === 7 && (resourcesIndex !== 5 || !argumentsList[6]))) {
        throw new AdapterError("usage_error", "workflow-compile requires exactly one --out DIR and optional --resources ACQUISITIONS.json");
      }
      const ready = handshake();
      const outputRoot = path.resolve(argumentsList[4]);
      data = compileWorkflow({ plan: readJsonFile(argumentsList[0]), assetLedger: readJsonFile(argumentsList[1]),
        decisions: readJsonFile(argumentsList[2]), outputRoot,
        resourceAcquisitions: resourcesIndex===5?readJsonFile(argumentsList[6]):[],
        cliIdentity: { version: ready.version, sha256: ready.sha256, jobSchema: ready.jobSchema,
          capabilities: ready.manifest.capabilities } });
      if (data.can_compile) {
        fs.mkdirSync(outputRoot, { recursive: true });
        for (const binding of data.job_bindings) atomicJson(path.join(outputRoot, `${binding.output_id}.job.json`), binding.job);
        atomicJson(path.join(outputRoot, "compilation-receipt.json"), data.receipt);
        atomicJson(path.join(outputRoot, "workflow-compilation.json"), data);
      }
      break;
    }
    case "native-controls-inspect": {
      if (argumentsList.length > 2 || (argumentsList.length === 2 && (argumentsList[0] !== "--out" || !argumentsList[1]))) {
        throw new AdapterError("usage_error", "native-controls-inspect accepts only optional --out REPORT.json");
      }
      data = await probeNativeControlContracts();
      if (argumentsList[1]) atomicJson(path.resolve(argumentsList[1]), data);
      break;
    }
    case "native-controls-plan": {
      if (!argumentsList[0]) {
        throw new AdapterError("usage_error", "native-controls-plan requires REQUESTS.json [--canary CANARY.json] [--out PLAN.json]");
      }
      const canaryIndex = argumentsList.indexOf("--canary");
      const outIndex = argumentsList.indexOf("--out");
      if ((canaryIndex >= 0 && !argumentsList[canaryIndex + 1]) || (outIndex >= 0 && !argumentsList[outIndex + 1])) {
        throw new AdapterError("usage_error", "--canary and --out require a file path");
      }
      const unexpected = argumentsList.filter((value,index)=>index>0 &&
        ![canaryIndex,canaryIndex+1,outIndex,outIndex+1].includes(index));
      if (unexpected.length) throw new AdapterError("usage_error", `unknown native-controls-plan arguments: ${unexpected.join(" ")}`);
      const probed = await probeNativeControlContracts();
      const canary = canaryIndex >= 0 ? readJsonFile(argumentsList[canaryIndex + 1]) : null;
      const adapters = { draft_protocol: true, runtime_native: false, accessibility_adapter: false, visual_fallback: false };
      if (canary?.adapter?.kind && Object.hasOwn(adapters,canary.adapter.kind)) adapters[canary.adapter.kind] = true;
      data = compileNativeControlPlan({ requests: readJsonFile(argumentsList[0]), catalog: probed.catalog,
        inventory: probed.inventory, canary, adapters });
      if (outIndex >= 0) atomicJson(path.resolve(argumentsList[outIndex + 1]), data);
      break;
    }
    case "native-resource-route": {
      if (!argumentsList[0] || !argumentsList[1] || argumentsList.length !== 2) {
        throw new AdapterError("usage_error", "native-resource-route requires QUERY.json EDITION_OBSERVATION.json");
      }
      data = routeNativeResourceQuery(readJsonFile(argumentsList[0]), readJsonFile(argumentsList[1]));
      break;
    }
    case "home-folder-plan": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "home-folder-plan requires REQUEST.json");
      }
      data = buildHomeFolderPlan(readJsonFile(argumentsList[0]));
      break;
    }
    case "home-folder-execute": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "home-folder-execute requires REQUEST.json");
      }
      data = executeHomeFolderOperation({ request: readJsonFile(argumentsList[0]), pluginRoot: ROOT });
      break;
    }
    case "workflow-start": {
      if (!argumentsList[0] || argumentsList.length !== 1) {
        throw new AdapterError("usage_error", "workflow-start requires COMPILATION.json");
      }
      data = workflowRuntime.start({ compilation: readJsonFile(argumentsList[0]), revision: 1,
        budget: { currency: "CNY", maximum: 0 } });
      break;
    }
    case "workflow-approval-binding":
      data = workflowRuntime.approvalBinding(argumentsList[0]);
      break;
    case "workflow-approve":
      if (!argumentsList[0] || !argumentsList[1]) {
        throw new AdapterError("usage_error", "workflow-approve requires RUN_ID APPROVAL.json");
      }
      data = workflowRuntime.approve(argumentsList[0], readJsonFile(argumentsList[1]));
      break;
    case "workflow-execute":
      data = workflowRuntime.execute(argumentsList[0]);
      break;
    case "workflow-resume":
      data = workflowRuntime.resume(argumentsList[0]);
      break;
    case "workflow-cancel":
      data = workflowRuntime.cancel(argumentsList[0]);
      break;
    case "workflow-confirm-cancelled":
      data = workflowRuntime.confirmCancelled(argumentsList[0]);
      break;
    case "plan-video": {
      if (!argumentsList[0]) throw new AdapterError("usage_error", "plan-video requires INTENT.json");
      const devIndex = argumentsList.indexOf("--development-skill-root");
      if (devIndex >= 0 && !argumentsList[devIndex + 1]) {
        throw new AdapterError("usage_error", "--development-skill-root requires a path");
      }
      const intent = readJsonFile(argumentsList[0]);
      const planningData = loadPlanningData({
        developmentSkillRoot: devIndex >= 0 ? argumentsList[devIndex + 1] : undefined,
      });
      const manifest = (intent.delivery ?? "plan") === "plan" ? undefined : handshake().manifest;
      data = planVideo(intent, planningData, manifest);
      break;
    }
    case "session-check":
      // Advisory SessionStart hook: sessionCheck() prints a warning line
      // itself only when package integrity fails. The JSON envelope is
      // deliberately omitted so a healthy plugin stays completely silent in
      // session context, and the hook can never block session start.
      harness.sessionCheck();
      return;
    case "doctor":
      data = harness.doctor();
      break;
    case "start":
      if (!argumentsList[0]) throw new AdapterError("usage_error", "start requires REQUEST.json");
      data = harness.start(readJsonFile(argumentsList[0]));
      break;
    case "approve":
      if (!argumentsList[0] || !argumentsList[1]) {
        throw new AdapterError("usage_error", "approve requires TASK_ID APPROVAL.json");
      }
      data = harness.approve(argumentsList[0], readJsonFile(argumentsList[1]));
      break;
    case "execute":
      data = harness.execute(argumentsList[0]);
      break;
    case "resume":
      data = harness.resume(argumentsList[0]);
      break;
    case "list":
      data = harness.list();
      break;
    case "show":
      data = harness.show(argumentsList[0]);
      break;
    case "cancel":
      data = harness.cancel(argumentsList[0]);
      break;
    case "retry":
      data = harness.retry(argumentsList[0]);
      break;
    case "audit":
      data = harness.audit(argumentsList[0]);
      break;
    case "delivery":
      data = harness.assessDelivery(argumentsList[0], argumentsList[1]);
      break;
    default:
      throw new AdapterError(
        "usage_error",
        "usage: harness.mjs quality-evidence|quality-evaluate|quality-evaluate-remote|quality-reference-set|quality-comparison-context|quality-macro-revision|quality-retarget-propose|quality-retarget-apply|workflow-plan|workflow-check|workflow-compile|native-controls-inspect|native-controls-plan|native-resource-route|home-folder-plan|home-folder-execute|workflow-start|workflow-approval-binding|workflow-approve|workflow-execute|workflow-resume|workflow-cancel|workflow-confirm-cancelled|plan-video|doctor|start|approve|execute|resume|list|show|cancel|retry|audit|delivery [--state-root DIR]",
      );
  }
  console.log(JSON.stringify({ ok: true, data }));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    const adapted = error instanceof AdapterError
      ? error
      : new AdapterError("harness_failed", error.message ?? String(error));
    console.log(JSON.stringify({ ok: false, error: adapted.toJSON() }));
    process.exitCode = 1;
  });
}
