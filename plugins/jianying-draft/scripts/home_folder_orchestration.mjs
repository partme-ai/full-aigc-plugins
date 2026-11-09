import path from "node:path";
import process from "node:process";

import { AdapterError, runJsonCommand } from "./runtime_adapter.mjs";

const SCHEMA = "jianying-home-folder-operation/v1";
const CAPABILITY = "home.folder_lifecycle";
const OPERATIONS = new Set(["list", "create", "recycle", "list_recycled", "restore"]);
const WRITE_OPERATIONS = new Set(["create", "recycle", "restore"]);

function fail(message, details = {}) {
  throw new AdapterError(
    "home_folder_request_invalid",
    message,
    details,
    ["use the strict jianying-home-folder-operation/v1 request contract"],
  );
}

function requireString(value, field) {
  if (typeof value !== "string" || value.trim() === "") fail(`${field} must be a non-empty string`);
  return value;
}

function appendCommonArgs(argv, request) {
  if (request.config_root !== undefined) {
    argv.push("--config-root", path.resolve(requireString(request.config_root, "config_root")));
  }
  if (request.at !== undefined) {
    if (typeof request.at !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/.test(request.at)) {
      fail("at must use YYYY-MM-DDTHH:MM:SS", { field: "at" });
    }
    argv.push("--at", request.at);
  }
}

function assertExactKeys(request, allowed) {
  const unknown = Object.keys(request).filter((key) => !allowed.has(key));
  if (unknown.length) {
    fail("request contains unknown fields", { unknown_fields: unknown.sort() });
  }
}

/**
 * 将首页文件夹请求编译为固定 Rust CLI argv，不执行 GUI 或直接写配置。
 */
export function buildHomeFolderPlan(request) {
  if (!request || typeof request !== "object" || Array.isArray(request)) fail("request must be an object");
  if (request.schema !== SCHEMA) fail(`schema must be ${SCHEMA}`);
  if (!OPERATIONS.has(request.operation)) fail("operation is not supported", { operation: request.operation });

  const common = new Set(["schema", "operation", "config_root"]);
  const write = WRITE_OPERATIONS.has(request.operation);
  if (write) {
    common.add("approved");
    common.add("at");
  }
  const argv = ["home", "folder"];
  let verify;
  switch (request.operation) {
    case "list":
      assertExactKeys(request, common);
      argv.push("list");
      verify = { operation: "list", match: "response_is_state" };
      break;
    case "list_recycled":
      assertExactKeys(request, common);
      argv.push("list-recycled");
      verify = { operation: "list_recycled", match: "response_is_state" };
      break;
    case "create":
      common.add("name");
      common.add("parent_id");
      assertExactKeys(request, common);
      argv.push("create", requireString(request.name, "name"));
      if (request.parent_id !== undefined) {
        if (typeof request.parent_id !== "string") fail("parent_id must be a string");
        argv.push("--parent-id", request.parent_id);
      }
      verify = { operation: "list", match: "result.folder.id" };
      break;
    case "recycle":
      common.add("folder_id");
      assertExactKeys(request, common);
      argv.push("recycle", requireString(request.folder_id, "folder_id"));
      verify = { operation: "list_recycled", match: "result.recycle_id", cross_check: "active_id_absent" };
      break;
    case "restore":
      common.add("recycle_id");
      assertExactKeys(request, common);
      argv.push("restore", requireString(request.recycle_id, "recycle_id"));
      verify = { operation: "list", match: "result.folder_id", cross_check: "recycle_id_absent" };
      break;
    default:
      fail("operation is not supported", { operation: request.operation });
  }
  appendCommonArgs(argv, request);
  if (request.operation === "recycle") argv.push("--yes");
  return {
    schema: "jianying-home-folder-plan/v1",
    operation: request.operation,
    access: write ? "write" : "read",
    required_capability: CAPABILITY,
    approval_required: write,
    approved: write ? request.approved === true : null,
    argv,
    verify,
    fallback: null,
  };
}

function invoke(args, options) {
  const invocation = runJsonCommand({
    args,
    requiredCapabilities: [CAPABILITY],
    env: options.env,
    pluginRoot: options.pluginRoot,
  });
  if (invocation.exitCode !== 0 || invocation.envelope?.ok !== true) {
    throw new AdapterError(
      "home_folder_cli_failed",
      "released Rust CLI rejected the homepage folder operation",
      { argv: args, response: invocation.envelope, exit_code: invocation.exitCode },
      ["inspect the structured CLI failure", "do not retry an ambiguous write automatically"],
    );
  }
  return invocation.envelope.data;
}

function readArgs(operation, request) {
  const args = ["home", "folder", operation === "list_recycled" ? "list-recycled" : "list"];
  if (request.config_root !== undefined) args.push("--config-root", path.resolve(request.config_root));
  return args;
}

function exactCount(values, predicate) {
  return Array.isArray(values) ? values.filter(predicate).length : 0;
}

/**
 * 通过校验过的发布 Rust CLI 执行文件夹原子操作，并按 ID 独立回读验证。
 */
export function executeHomeFolderOperation({
  request,
  env = process.env,
  pluginRoot,
}) {
  const plan = buildHomeFolderPlan(request);
  if (plan.approval_required && plan.approved !== true) {
    throw new AdapterError(
      "approval_required",
      `homepage folder ${plan.operation} requires explicit approval`,
      { operation: plan.operation, argv: plan.argv },
      ["review the exact ids and set approved=true", "plan again if the target state changed"],
    );
  }
  const options = { env, pluginRoot };
  const result = invoke(plan.argv, options);
  if (plan.access === "read") {
    return { schema: "jianying-home-folder-execution/v1", operation: plan.operation, verified: true,
      plan, result, readback: result, cross_check: null, snapshot_path: null };
  }
  if (typeof result.snapshot_path !== "string" || result.snapshot_path === "") {
    throw new AdapterError(
      "home_folder_verification_failed",
      "CLI write response did not include a recovery snapshot",
      { operation: plan.operation, result },
      ["stop the workflow", "inspect the CLI transaction state before any retry"],
    );
  }

  let readback;
  let crossCheck = null;
  let verified = false;
  if (plan.operation === "create") {
    readback = invoke(readArgs("list", request), options);
    const folderId = result.folder?.id;
    verified = typeof folderId === "string"
      && exactCount(readback.folders, (folder) => folder.id === folderId) === 1;
  } else if (plan.operation === "recycle") {
    readback = invoke(readArgs("list_recycled", request), options);
    crossCheck = invoke(readArgs("list", request), options);
    verified = result.folder_id === request.folder_id
      && typeof result.recycle_id === "string"
      && exactCount(readback.recycled_folders, (entry) => entry.recycle_id === result.recycle_id
        && entry.folder_info?.id === request.folder_id) === 1
      && exactCount(crossCheck.folders, (folder) => folder.id === request.folder_id) === 0;
  } else if (plan.operation === "restore") {
    readback = invoke(readArgs("list", request), options);
    crossCheck = invoke(readArgs("list_recycled", request), options);
    verified = typeof result.folder_id === "string"
      && result.recycle_id === request.recycle_id
      && exactCount(readback.folders, (folder) => folder.id === result.folder_id) === 1
      && exactCount(crossCheck.recycled_folders, (entry) => entry.recycle_id === request.recycle_id) === 0;
  }
  if (!verified) {
    throw new AdapterError(
      "home_folder_verification_failed",
      "CLI write completed but exact-id state readback did not prove the requested result",
      { operation: plan.operation, result, readback, cross_check: crossCheck,
        snapshot_path: result.snapshot_path },
      ["stop automatic execution", "retain and inspect snapshot_path", "do not retry the write silently"],
    );
  }
  return {
    schema: "jianying-home-folder-execution/v1",
    operation: plan.operation,
    verified: true,
    plan,
    result,
    readback,
    cross_check: crossCheck,
    snapshot_path: result.snapshot_path,
  };
}
