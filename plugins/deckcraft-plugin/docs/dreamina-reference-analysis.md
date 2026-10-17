# Dreamina 借鉴与 DeckCraft 适配

> 2026-10-09。固定源码对照；本轮未运行 Dreamina 或 DeckCraft。Dreamina 两仓 CodeGraph 未初始化，采用源码直读。

| 参考 | 来源 | 借鉴内容 |
|---|---|---|
| dreamina-skills | [README](https://github.com/full-aigc-skills/dreamina-skills/blob/42f0e38ab114d271e2f999483ef83a6ebbddc4f3/README.md) | 少量可发现入口、按需参考、双语导航 |
| dreamina-canvas-plugin | [README](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/README.md)、[固定技能来源](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/skills.lock.json) | 插件包内技能、来源版本与文件摘要 |
| DeckCraft | [CLI](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/apps/deckcraft-cli/src/main.rs)、[MCP](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/crates/mcp/src/server.rs) | 已有命令和 MCP 服务，无需再实现一套 |
| Agent Plugins | [正式规范](https://agent-plugins.org/specification) | 根 manifest、Skills 和 MCP 固定发现位置 |

## 应保留的能力

技能触发与操作参考、运行时命令发现、来源固定、单独安装、建稿后的 inspect/render/export 回读，以及文档、静态检查、实际宿主和真实产物的分层证据。
命令与 Hooks 要按具体客户端扩展使用。插件内技能必须完整打包，安装后不能借用相邻技能库路径。

## 不直接移植的设计

Dreamina 的 quote/token/credits、付费审批、持久预算、提交状态机、上传器和视觉多轮控制器服务于付费云生成；DeckCraft 的初期插件是本地命令与现有 MCP 的组合。这些功能不进入基础架构。需要某项功能时先给具体场景、已有工具缺口、最小实现和回归。
DeckCraft Remote 在通信错误后可能重发修改请求，[源码](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/crates/mcp/src/backend.rs) 对此提供静态证据；未做故障注入，不能承诺或否认真实重复执行。初期选择适合的上游模式，遇到不确定结果先回读并说明边界。

## Dreamina 文档本身可改进之处

[skills 英文 README](https://github.com/full-aigc-skills/dreamina-skills/blob/42f0e38ab114d271e2f999483ef83a6ebbddc4f3/README.md) 含中文 Canvas 小节，双语内容可更一致；[2026-10-08 回归记录](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/docs/verification/round-safety-2026-10-08.md) 保留了当时的“本地候选/未发布”事实，阅读时应结合后续发布证据。插件锁定的技能来源可能早于技能仓当前版本，只有逐技能摘要与兼容说明能支持这种差异。历史付费、Windows 和宿主记录不能证明后续版本当前验收。

## 当前优先级

| 优先级 | 技能库 | 插件 |
|---|---|---|
| P0 | SKILL.md、触发与资源、运行时命令参考 | plugin.json、包内技能、mcp.json、规范校验 |
| P1 | 审查、导出和错误场景 | 宿主加载、MCP 握手、真实文稿闭环 |
| P2 | 更多媒体、图表和复杂格式案例 | 经证实有需要的客户端命令或 Hooks |
