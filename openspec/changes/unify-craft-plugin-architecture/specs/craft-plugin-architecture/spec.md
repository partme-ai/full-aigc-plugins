## ADDED Requirements

### Requirement: Minimal Craft package

每个基础可用的 Craft 插件 MUST 有 Agent Plugins 1.0.0 根 `plugin.json`，并提供至少一个本项目选择的可发现领域技能。只有实际使用原生 MCP 的插件才添加根 `mcp.json`。客户端命令和钩子不属于可移植核心。

#### Scenario: Client discovers the package
- **WHEN** 支持 Agent Plugins 1.0.0 的客户端加载包
- **THEN** 它可以按固定路径发现合法技能以及存在时的 MCP 配置，不依赖开发仓库中的外部路径

### Requirement: Upstream remains the execution source

技能 MUST 调用或指导调用实际存在的上游 CLI/MCP，不得为基础插件复制原生命令执行器或虚构工具。不可用命令和缺失前置条件 MUST 如实报告。

#### Scenario: DeckCraft command is unavailable
- **WHEN** 宿主未连接 DeckCraft MCP 且找不到 `deckcraft-cli`
- **THEN** 技能说明缺少的前置条件，不声称已完成文稿操作

### Requirement: Basic completion is separate from advanced work

基础插件检查 MUST 分别记录包结构、独立技能、宿主加载和真实上游调用。未执行的层 MUST 标为 NOT_RUN。Harness、全部原生命令、创作质量与多平台发行 MUST NOT 成为基础包结构通过的前置条件，也不得因基础包通过被标为完成。

#### Scenario: Static package passes while runtime is unavailable
- **WHEN** manifest 和技能通过本地检查但目标 CLI 或宿主未就绪
- **THEN** 仅报告静态包通过，宿主及真实调用保持 NOT_RUN
