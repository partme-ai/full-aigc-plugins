# Craft 内嵌编辑器与场景技能

## Why

已有插件主要提供原生命令知识；用户需要在 ZCode、Codex 内看到实际编辑器，并用老照片修复等场景完成可编辑交付。

## What Changes

- 为已有九种 ZCode Craft Web 制品增加可移植 MCP Apps 接入，以及连接同一 MCP 进程的宿主浏览器页面。
- 单独补齐 EffectCraft、FilmCraft、LightCraft 的 Web 接入，不将启动原生窗口算作内嵌。
- 新建 SoundCraft、GridCraft、WordCraft 插件；PrintCraft 延续现有身份，对应上游 PdfCraft，不重复维护产品。
- 增加具体场景技能，保留既有锁定技能快照；新技能在独立技能源维护，本地候选明确标注。

## Non-goals

不改宿主源码，不新建 Agent Runtime，不提交推送或全局安装，不把浏览器适配验收冒充原生 MCP Apps 面板验收。

## Impact

涉及十二个插件、对应技能源和市场目录的开发文档。现有发行包与用户修改保留。
