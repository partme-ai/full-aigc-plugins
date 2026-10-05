import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { validatePortableMcp } from "./portable-mcp-config.mjs";

const schema = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json";
const document = (mcpServers = {}) => ({ $schema: schema, mcpServers });
const service = { type: "stdio", command: "node", args: [], cwd: "./" };

function fixture(t, files = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "portable-mcp-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  files = {
    "plugin.json": { $schema: "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", name: "fixture" },
    ...files,
  };
  for (const [name, value] of Object.entries(files)) {
    const file = path.join(root, name);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, typeof value === "string" ? value : JSON.stringify(value));
  }
  return root;
}

test("skills-only plugins may omit mcp.json", t => {
  assert.deepEqual(validatePortableMcp(fixture(t)), []);
});

test("host declarations require mcp.json across all supported hosts", t => {
  for (const file of [".codex-plugin/plugin.json", ".zcode-plugin/plugin.json", "kimi.plugin.json"]) {
    const root = fixture(t, { [file]: { mcpServers: { local: service } } });
    assert.match(validatePortableMcp(root).join("\n"), /missing mcp.json/);
  }
});

test("native MCP config and string references require portable configuration", t => {
  assert.match(validatePortableMcp(fixture(t, { ".mcp.json": { mcpServers: { local: service } } })).join("\n"), /missing mcp.json/);
  assert.match(validatePortableMcp(fixture(t, { ".codex-plugin/plugin.json": { mcpServers: "./native.json" }, "native.json": { mcpServers: { local: service } } })).join("\n"), /missing mcp.json/);
});

test("portable services cover host declarations without requiring identical native fields", t => {
  const root = fixture(t, {
    ".mcp.json": { mcpServers: { local: { ...service, startup_timeout_sec: 30 } } },
    "mcp.json": document({ local: service }),
  });
  assert.deepEqual(validatePortableMcp(root), []);
});

test("empty portable configuration cannot hide native services", t => {
  const root = fixture(t, { ".mcp.json": { mcpServers: { local: service } }, "mcp.json": document() });
  assert.match(validatePortableMcp(root).join("\n"), /missing native server local/);
});

test("malformed documents and nonstandard transports fail without throwing", t => {
  for (const value of ["{", { mcpServers: {} }, document([]), document({ local: { type: "http", url: "https://example.com/mcp" } }), document({ local: { ...service, startup_timeout_sec: 30 } })]) {
    assert.ok(validatePortableMcp(fixture(t, { "mcp.json": value })).length > 0);
  }
});

test("invalid command, cwd and reserved environment names are rejected", t => {
  for (const local of [{ ...service, command: "node script.js" }, { ...service, cwd: "../" }, { ...service, env: { PLUGIN_ROOT: "override" } }]) {
    assert.ok(validatePortableMcp(fixture(t, { "mcp.json": document({ local }) })).length > 0);
  }
});

test("remote endpoints require secure URLs and valid header fields", t => {
  assert.deepEqual(validatePortableMcp(fixture(t, { "mcp.json": document({ remote: { type: "streamable-http", url: "https://example.com/mcp" } }) })), []);
  for (const url of ["http://example.com/mcp", "https://user:pass@example.com/mcp", "https://example.com/mcp#fragment"]) {
    assert.ok(validatePortableMcp(fixture(t, { "mcp.json": document({ remote: { type: "streamable-http", url } }) })).length > 0);
  }
  for (const headers of [{ "X-Test": "bad\r\nvalue" }, { "X-Test": "one", "x-test": "two" }]) {
    assert.ok(validatePortableMcp(fixture(t, { "mcp.json": document({ remote: { type: "streamable-http", url: "https://example.com/mcp", headers } }) })).length > 0);
  }
});

test("MCP and plugin schema versions must match", t => {
  const root = fixture(t, { "plugin.json": { $schema: "unsupported", name: "fixture" }, "mcp.json": document() });
  assert.match(validatePortableMcp(root).join("\n"), /schema must match/);
});
