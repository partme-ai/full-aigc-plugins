# Tasks: 最小 Craft 插件

- [x] 补充 Windows CI 的完整包校验、含中文空格路径安装及原生宿主 MCP 启动回归；取得 Windows runner 结果后确认通过。

- [x] 在 Windows runner 验证 13 个原生 Craft CLI 创建、编辑、保存与新进程重开，并修复兼容问题。

- [x] 核对十仓真实 Git 根、工作区修改、Agent Plugins 1.0.0 组件和已有基础包；记录 DeckCraft 是唯一缺根包的仓库。
- [x] 在 DeckCraft 技能源与插件仓放入同一份 `deckcraft-use`，创建根 `plugin.json` 和连接现有 CLI 的 `mcp.json`，不增加 Harness 或本地执行器。
- [x] 核对十个包的 manifest、技能 frontmatter、包内路径和现有静态验证；修复基础包缺陷，并同步与实际状态冲突的文档。十仓基础结构核对通过；九仓现有验证入口通过（LightCraft 需提供其既有技能源路径）；DeckCraft 本地字段、MCP、技能快照、隔离复制、链接与空白检查通过。官方 JSON Schema 验证器未运行。
- [ ] 验证 13 个 Craft 插件在 Codex、ZCode、Kimi 的真实宿主调用和内嵌编辑同步；修复宿主能力声明与画面同步问题，外部环境阻塞如实记录，不用 SDK 调用代替。
- [x] 复核各仓已有高级任务：五个 `establish-v1-plugin` 长任务表补充分界；DesignCraft、LightCraft、PrintCraft 的现有 harden/extend 变更继续独立开放；CADCraft 无此类变更。未删改原任务和证据，Harness 的用途另行讨论。

- [x] 将13个开发候选以固定标签和校验和发行资源接入三宿主市场，验证干净Git安装、首次启动和真实Codex MCP调用；保留稳定发布及未验收能力的限制。

- [ ] 以固定发行提交生成13个Codex市场内薄包快照，验证安装前官方图标路径、实际安装/MCP与发布后市场发现，保留独立源码仓及其他宿主发行。
