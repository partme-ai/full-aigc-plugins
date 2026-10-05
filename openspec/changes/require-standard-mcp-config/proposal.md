# Proposal

## Why

当前市场检查宿主 manifest，但不会拒绝只有宿主 MCP 配置、缺少标准 `mcp.json` 的插件。使用 MCP 的插件必须具有 Agent Plugins 1.0.0 标准配置；不使用 MCP 的插件可以不提供该文件。

## What Changes

- 对正式插件和可安装 RC 校验标准 MCP 配置。
- 已声明的宿主 MCP 服务必须在标准配置中存在；无 MCP 插件无需添加空配置。
- 拒绝缺失、无法解析、Schema 标识错误或服务配置无效的标准 MCP 文件。
- 保留宿主原生适配，不改变插件版本、供应商调用或发布门禁。

## Capabilities

### New Capabilities

- `portable-mcp-configuration`: 使用 MCP 的插件必须同时提供有效的标准 MCP 配置。

### Modified Capabilities

无。

## Impact

影响市场校验脚本及其测试。当前三个 MCP 插件已经包含标准文件，其他九个插件无须增加配置。此变更不发布或更新插件制品。
