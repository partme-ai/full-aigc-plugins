import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  buildHomeFolderPlan,
  executeHomeFolderOperation,
} from "../scripts/home_folder_orchestration.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function fakeCli(homeCapabilityStatus = "supported", breakReadback = false) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-home-folder-plugin-"));
  const executable = path.join(root, "jianying");
  const stateFile = path.join(root, "state.json");
  fs.writeFileSync(stateFile, JSON.stringify({
    folders: [{ id: "folder-one", name: "新建文件夹", parentId: "" }],
    recycled_folders: [],
  }));
  const lock = JSON.parse(fs.readFileSync(path.join(ROOT, "runtime", "jianying-cli.lock.json"), "utf8"));
  const capabilities = lock.requiredCapabilities.map((id) => ({ id, status: "supported" }));
  capabilities.push({ id: "home.folder_lifecycle", status: homeCapabilityStatus });
  fs.writeFileSync(executable, `#!/usr/bin/env node
const fs = require("node:fs");
const args = process.argv.slice(2).filter((value) => value !== "--json");
const stateFile = ${JSON.stringify(stateFile)};
const capabilities = ${JSON.stringify(capabilities)};
const breakReadback = ${JSON.stringify(breakReadback)};
const version = ${JSON.stringify(lock.minimumVersion)};
const read = () => JSON.parse(fs.readFileSync(stateFile, "utf8"));
const write = (value) => fs.writeFileSync(stateFile, JSON.stringify(value));
const ok = (data) => { console.log(JSON.stringify({ok:true,data})); process.exit(0); };
if (args.includes("--version")) { console.log("jianying " + version); process.exit(0); }
if (args[0] === "capabilities") ok({schema:"jianying-capabilities/v1",cli_version:version,capabilities});
const op = args.slice(0, 3).join(" ");
const state = read();
if (op === "home folder list") ok({folders:state.folders,count:state.folders.length});
if (op === "home folder list-recycled") {
  const values = breakReadback ? [] : state.recycled_folders;
  ok({recycled_folders:values,count:values.length});
}
if (op === "home folder create") {
  const folder = {id:"created-id",name:args[3],parentId:args[args.indexOf("--parent-id")+1] || ""};
  state.folders.push(folder); write(state); ok({status:"created",folder,snapshot_path:"/snapshot/create"});
}
if (op === "home folder recycle") {
  const folderId = args[3]; const index = state.folders.findIndex((item) => item.id === folderId);
  const folder = state.folders.splice(index, 1)[0];
  state.recycled_folders.push({recycle_id:"{recycle-one}",folder_info:folder,drafts:[],sub_folders:[]});
  write(state); ok({status:"recycled",folder_id:folderId,recycle_id:"{recycle-one}",snapshot_path:"/snapshot/recycle"});
}
if (op === "home folder restore") {
  const recycleId = args[3]; const index = state.recycled_folders.findIndex((item) => item.recycle_id === recycleId);
  const entry = state.recycled_folders.splice(index, 1)[0]; state.folders.push(entry.folder_info);
  write(state); ok({status:"restored",folder_id:entry.folder_info.id,recycle_id:recycleId,snapshot_path:"/snapshot/restore"});
}
console.log(JSON.stringify({ok:false,error:{type:"unexpected_args",details:{args}}})); process.exit(1);
`, { mode: 0o755 });
  const sha256 = crypto.createHash("sha256").update(fs.readFileSync(executable)).digest("hex");
  return {
    root,
    stateFile,
    env: { JIANYING_CLI_PATH: executable, JIANYING_CLI_SHA256: sha256 },
  };
}

test("folder requests compile to fixed Rust argv and reject arbitrary GUI fields", () => {
  const list = buildHomeFolderPlan({
    schema: "jianying-home-folder-operation/v1",
    operation: "list",
    config_root: "/tmp/config",
  });
  assert.deepEqual(list.argv, ["home", "folder", "list", "--config-root", "/tmp/config"]);
  assert.equal(list.access, "read");
  assert.equal(list.required_capability, "home.folder_lifecycle");

  const recycle = buildHomeFolderPlan({
    schema: "jianying-home-folder-operation/v1",
    operation: "recycle",
    folder_id: "folder-one",
    config_root: "/tmp/config",
    approved: true,
  });
  assert.deepEqual(recycle.argv, [
    "home", "folder", "recycle", "folder-one", "--config-root", "/tmp/config", "--yes",
  ]);
  assert.equal(recycle.access, "write");
  assert.equal(recycle.verify.operation, "list_recycled");

  assert.throws(
    () => buildHomeFolderPlan({
      schema: "jianying-home-folder-operation/v1",
      operation: "list",
      x: 10,
      y: 20,
    }),
    (error) => error.code === "home_folder_request_invalid",
  );
});

test("partial released capability blocks before mutation without GUI fallback", () => {
  const fixture = fakeCli("partial");
  const before = fs.readFileSync(fixture.stateFile, "utf8");
  assert.throws(
    () => executeHomeFolderOperation({
      request: {
        schema: "jianying-home-folder-operation/v1",
        operation: "recycle",
        folder_id: "folder-one",
        approved: true,
      },
      env: fixture.env,
      pluginRoot: ROOT,
    }),
    (error) => error.code === "missing_capability"
      && error.details.capability === "home.folder_lifecycle",
  );
  assert.equal(fs.readFileSync(fixture.stateFile, "utf8"), before);
  fs.rmSync(fixture.root, { recursive: true, force: true });
});

test("supported released CLI recycle and restore are independently read back by exact ids", () => {
  const fixture = fakeCli();
  const recycled = executeHomeFolderOperation({
    request: {
      schema: "jianying-home-folder-operation/v1",
      operation: "recycle",
      folder_id: "folder-one",
      approved: true,
    },
    env: fixture.env,
    pluginRoot: ROOT,
  });
  assert.equal(recycled.verified, true);
  assert.equal(recycled.result.folder_id, "folder-one");
  assert.equal(recycled.result.recycle_id, "{recycle-one}");
  assert.equal(recycled.readback.recycled_folders[0].folder_info.id, "folder-one");
  assert.equal(recycled.snapshot_path, "/snapshot/recycle");

  const restored = executeHomeFolderOperation({
    request: {
      schema: "jianying-home-folder-operation/v1",
      operation: "restore",
      recycle_id: "{recycle-one}",
      approved: true,
    },
    env: fixture.env,
    pluginRoot: ROOT,
  });
  assert.equal(restored.verified, true);
  assert.equal(restored.result.folder_id, "folder-one");
  assert.equal(restored.readback.folders[0].id, "folder-one");
  fs.rmSync(fixture.root, { recursive: true, force: true });
});

test("an ambiguous CLI success stops at readback and retains the recovery snapshot", () => {
  const fixture = fakeCli("supported", true);
  assert.throws(
    () => executeHomeFolderOperation({
      request: {
        schema: "jianying-home-folder-operation/v1",
        operation: "recycle",
        folder_id: "folder-one",
        approved: true,
      },
      env: fixture.env,
      pluginRoot: ROOT,
    }),
    (error) => error.code === "home_folder_verification_failed"
      && error.details.snapshot_path === "/snapshot/recycle",
  );
  fs.rmSync(fixture.root, { recursive: true, force: true });
});

test("harness planning is CLI-free and exposes no GUI fallback", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "jianying-home-folder-plan-"));
  const request = path.join(root, "request.json");
  fs.writeFileSync(request, JSON.stringify({
    schema: "jianying-home-folder-operation/v1",
    operation: "restore",
    recycle_id: "{recycle-one}",
    approved: true,
  }));
  const result = spawnSync(process.execPath, [path.join(ROOT, "scripts", "harness.mjs"), "home-folder-plan", request], {
    encoding: "utf8",
    env: { ...process.env, PATH: "/nonexistent", JIANYING_CLI_PATH: "/nonexistent" },
  });
  assert.equal(result.status, 0, result.stdout + result.stderr);
  const envelope = JSON.parse(result.stdout);
  assert.equal(envelope.ok, true);
  assert.equal(envelope.data.required_capability, "home.folder_lifecycle");
  assert.equal(envelope.data.fallback, null);
  assert.deepEqual(envelope.data.argv, ["home", "folder", "restore", "{recycle-one}"]);
  fs.rmSync(root, { recursive: true, force: true });
});
