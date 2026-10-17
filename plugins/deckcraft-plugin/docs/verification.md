# 验证矩阵

> 2026-10-09。本地候选包已创建；静态、宿主和真实文稿分层验证。

| 层 | 范围 | 所需证据 | 当前 |
|---|---|---|---|
| 文档 | 双语入口、链接、状态和架构名称 | 本仓文件检查 | 本轮通过 |
| 包结构 | plugin.json、一个 Skill、mcp.json、包内路径 | 本地字段、路径与隔离安装；官方 Schema 另验 | LOCAL_PASS / SCHEMA_NOT_RUN |
| 客户端 | 插件加载、Skills 发现、可选扩展 | 目标客户端精确版本与运行记录 | NOT_RUN |
| MCP | DeckCraft stdio 握手、工具列表和调用 | 固定源码临时构建；目标客户端另验 | 直接 MCP PASS；宿主 NOT_RUN |
| 引擎 | 建稿、inspect、render、导出重开 | 当前 DeckCraft 版本的真实文稿 | 两页建稿、保存重开、PNG PASS；其余 NOT_RUN |
| 格式 | 外部 PPTX、PDF、PNG | 内容保留/丢失与视觉差异 | PNG 签名 PASS；外部语料 NOT_RUN |

当前本地检查覆盖根 JSON 字段、MCP 命令、技能快照相等、隔离复制与空白；官方 JSON Schema 未用验证器执行。所有文件仍未跟踪，`git diff --check` 不覆盖其内容。静态结构通过不证明宿主加载或 MCP 调用。

固定上游 `d0e57d7e25f9852179cc66be12dd6188f1c05535` 的 `deckcraft-cli 0.3.0` 在仓外 `/tmp` 临时构建成功。单个 headless MCP PID 22468 完成初始化、25 工具发现、命令查询、两页建稿、保存、同进程重开、标题回读和 PNG 导出；原生文稿 4450 字节、PNG 79479 字节且签名正确，退出后清理。初次比较整个 `inspect_document` 回复失败，因为重开后回复不完全相同；改为核对标题保留后通过，未声称完整文档等价。临时产物已删除；目标宿主未加载本地插件，PATH 中也没有安装全局 CLI。

上游 DeckCraft 的外部 PPTX 测试在 `DECKCRAFT_PPTX_IN` 未设置时跳过，不以普通单测成功代替真实语料。[上游测试](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/crates/pptx/tests/sample.rs)
