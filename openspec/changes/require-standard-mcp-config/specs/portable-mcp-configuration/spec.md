## ADDED Requirements

### Requirement: MCP plugins provide portable configuration

市场 MUST 对正式插件和可安装 RC 执行标准 MCP 配置校验。宿主 manifest 的非空 `mcpServers` 声明或根 `.mcp.json` 的非空服务集合表明插件使用 MCP，此时 MUST 提供根 `mcp.json`；其中 MUST 覆盖宿主声明的服务名称。不使用 MCP 的插件 MAY 省略 `mcp.json`。

#### Scenario: A plugin declares native MCP without portable configuration
- **WHEN** 插件声明宿主 MCP 服务但缺少根 `mcp.json`
- **THEN** 市场检查失败并指出插件及缺失文件

#### Scenario: A skills-only plugin omits MCP configuration
- **WHEN** 插件没有 MCP 声明且不存在 `mcp.json`
- **THEN** MCP 配置检查通过且不创建空文件

#### Scenario: An empty portable file hides a native service
- **WHEN** 宿主声明服务但标准配置没有包含该服务名称
- **THEN** 市场检查失败并指出缺失的服务

### Requirement: Present portable MCP configurations are validated

已提供的 `mcp.json` MUST 为 JSON 对象，仅包含必需的 `$schema` 和 `mcpServers`；Schema MUST 为 Agent Plugins 1.0.0 canonical MCP 标识，根 `plugin.json` MUST 声明匹配版本。每个服务 MUST 使用标准传输类型及其允许字段。标准包路径 MUST 在真实路径解析后保持包内。市场校验 MUST 汇总错误而不是因单个无效文件崩溃。

#### Scenario: A portable configuration is malformed
- **WHEN** `mcp.json` JSON、字段、Schema 或服务配置无效
- **THEN** 市场检查失败并报告文件或服务错误

#### Scenario: A portable MCP configuration is valid
- **WHEN** 标准配置有效且覆盖所有宿主声明服务
- **THEN** MCP 静态检查通过但不声称握手、授权或业务调用成功
