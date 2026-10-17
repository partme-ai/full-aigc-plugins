## Why
当前编辑器包含有特定宿主命名及本机 MCP 配置，不能作为可搬迁的插件安装交付。

## What Changes
- 插件通过标准入口与 Codex、Claude Code 专用入口安装，启动不依赖开发机路径。
- 产品代码、技能和当前文档使用自身命名；停止分发旧宿主清单与专用更新通道。
- 保留第三方许可及来源声明，历史验收记录不改写。
- 当前聚焦插件宿主，WorkBuddy 的手写 MCP 配置不作为安装交付。

## Capabilities
### New Capabilities
### Modified Capabilities
- `craft-editor-scenes`: 可搬迁的插件安装与中性宿主接入。

## Impact
13 个插件、配套入口技能、构建和分发脚本。保持同会话编辑及工作区读写行为。
