# Proposal: 十个 Craft 插件的最小可安装包

## Why

现有计划把插件包装、原生产品全功能验收与可选执行治理混在一起，使普通插件也按大型运行时开发。变更前九个仓库已有根 manifest 和技能，DeckCraft 尚缺实际包。本变更把“插件已开发”的基础门槛收敛到 Agent Plugins 1.0.0 可移植组件及一条真实使用路径。

## What Changes

- 十仓仅按根 `plugin.json`、可发现的技能和确有上游 MCP 时的根 `mcp.json` 核对；命令和钩子按目标宿主需要选用。
- 补齐 DeckCraft 的最小包和单一入口技能，复用上游 `deckcraft-cli mcp`，不另建执行器。
- 将包结构、技能独立安装、宿主加载、真实上游调用分层报告；基础插件完成不等待创作质量全覆盖或高级治理功能。

## Scope

PhotoCraft、DeckCraft、CADCraft、ArtCraft、EffectCraft、DesignCraft、LightCraft、FilmCraft、PrintCraft、VectorCraft 插件包。独立技能源仅在缺少本轮必需技能时修改；`research/storytold` 只读。

## Non-goals

本变更不开发、移除或重新定义 Harness，不建立共享插件运行时，不重写上游 CLI/MCP，不把全部命令、格式、平台及创作验收设为基础插件完成门槛。已有高级 OpenSpec 任务保持开放，但不阻止基础包的独立验收。
