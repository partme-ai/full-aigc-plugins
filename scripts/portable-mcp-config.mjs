import fs from "node:fs";
import path from "node:path";
import net from "node:net";

const isObject = value => value !== null && typeof value === "object" && !Array.isArray(value);
const mcpSchema = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json";
const pluginSchema = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json";

/** 检查标准 MCP 文件及其宿主服务覆盖；不启动或连接服务。 */
export function validatePortableMcp(repo) {
  const errors = [];
  const nativeServers = new Set();
  let usesMcp = false;
  const root = fs.realpathSync(repo);
  const contained = file => {
    const relative = path.relative(root, fs.realpathSync(file));
    return relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
  };
  const read = relative => {
    try {
      const file = path.resolve(root, relative);
      if (!contained(file) || !fs.statSync(file).isFile()) throw new Error("not a package-contained regular file");
      return JSON.parse(fs.readFileSync(file, "utf8"));
    } catch (error) {
      errors.push(`${relative}: ${error.message}`);
      return undefined;
    }
  };
  const collect = value => {
    if (isObject(value)) {
      for (const name of Object.keys(value)) nativeServers.add(name);
      if (Object.keys(value).length > 0) usesMcp = true;
    }
  };
  for (const relative of [".codex-plugin/plugin.json", ".zcode-plugin/plugin.json", "kimi.plugin.json"]) {
    if (!fs.existsSync(path.join(root, relative))) continue;
    const declaration = read(relative)?.mcpServers;
    if (typeof declaration === "string" && declaration.length > 0) {
      usesMcp = true;
      if (!declaration.startsWith("./")) errors.push(`${relative}: MCP path must start with ./`);
      else collect(read(declaration)?.mcpServers);
    } else collect(declaration);
  }
  if (fs.existsSync(path.join(root, ".mcp.json"))) collect(read(".mcp.json")?.mcpServers);

  if (!fs.existsSync(path.join(root, "mcp.json"))) {
    if (usesMcp) errors.push("missing mcp.json for plugin declaring MCP servers");
    return errors;
  }
  const config = read("mcp.json");
  if (!isObject(config) || config.$schema !== mcpSchema || !isObject(config.mcpServers)
      || Object.keys(config).some(key => !["$schema", "mcpServers"].includes(key))) {
    errors.push("mcp.json: expected canonical $schema and mcpServers object only");
    return errors;
  }
  if (read("plugin.json")?.$schema !== pluginSchema) errors.push("plugin.json: schema must match MCP specification version 1.0.0");
  for (const name of nativeServers) {
    if (!Object.hasOwn(config.mcpServers, name)) errors.push(`mcp.json: missing native server ${name}`);
  }
  for (const [name, server] of Object.entries(config.mcpServers)) {
    const fail = message => errors.push(`mcp.json: ${name}: ${message}`);
    if (!isObject(server) || !["stdio", "streamable-http", "sse"].includes(server.type)) {
      fail("invalid server object or transport");
      continue;
    }
    const allowed = server.type === "stdio" ? ["type", "command", "args", "env", "cwd"] : ["type", "url", "headers"];
    if (Object.keys(server).some(key => !allowed.includes(key))) fail("unknown transport fields");
    if (server.type === "stdio") {
      const command = server.command;
      if (typeof command !== "string" || !command || /[\s\x00]/u.test(command)
          || (!command.startsWith("./") && /[\\/]/u.test(command)) || command.includes("${")) {
        fail("command must be one bare executable or ./ package path");
      } else if (command.startsWith("./")) {
        try { if (!contained(path.resolve(root, command))) fail("command escapes package"); }
        catch { fail("package command does not exist"); }
      }
      if ("args" in server && (!Array.isArray(server.args) || server.args.some(value => typeof value !== "string"))) fail("args must be strings");
      if ("env" in server && (!isObject(server.env) || Object.entries(server.env).some(([key, value]) =>
        ["PLUGIN_ROOT", "PLUGIN_DATA"].includes(key.toUpperCase()) || typeof value !== "string"))) fail("invalid env or reserved plugin variables");
      if ("cwd" in server) {
        if (typeof server.cwd !== "string" || !/^(?:\.\/|\$\{PLUGIN_ROOT\}(?:\/|$)|\$\{PLUGIN_DATA\}(?:\/|$))/u.test(server.cwd)) fail("invalid cwd");
        else if (!server.cwd.startsWith("${PLUGIN_DATA}")) {
          try {
            const cwd = server.cwd.replaceAll("${PLUGIN_ROOT}", root);
            const resolved = path.resolve(root, cwd);
            if (!contained(resolved) || !fs.statSync(resolved).isDirectory()) fail("cwd must stay inside package and be a directory");
          } catch { fail("cwd does not resolve to a package directory"); }
        } else {
          const suffix = server.cwd.slice("${PLUGIN_DATA}".length);
          const marker = path.resolve(root, "__plugin_data_boundary__");
          const relative = path.relative(marker, path.resolve(marker, `.${suffix}`));
          if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) fail("cwd escapes PLUGIN_DATA");
        }
      }
    } else {
      try {
        if (typeof server.url !== "string") throw new Error();
        const url = new URL(server.url);
        const host = url.hostname.replace(/^\[|\]$/gu, "");
        const loopback = host === "localhost" || host === "::1" || (net.isIP(host) === 4 && host.startsWith("127."));
        if (!["http:", "https:"].includes(url.protocol) || url.username || url.password || server.url.includes("#")
            || (url.protocol === "http:" && !loopback)) fail("invalid remote URL");
      } catch { fail("invalid remote URL"); }
      if ("headers" in server) {
        if (!isObject(server.headers)) fail("headers must be an object");
        else {
          const names = new Set();
          for (const [key, value] of Object.entries(server.headers)) {
            if (!/^[!#$%&'*+.^_`|~0-9A-Za-z-]+$/u.test(key) || typeof value !== "string" || /[\r\n\x00]/u.test(value)) fail("invalid header");
            if (names.has(key.toLowerCase())) fail("duplicate header name");
            names.add(key.toLowerCase());
          }
        }
      }
    }
  }
  return errors;
}
