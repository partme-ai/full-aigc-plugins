---
name: figcraft-dev-handoff
description: 当需要用 FigCraft 交付可编辑 UI 设计、标注、切图、CSS 或 React 等开发参考代码时使用。
license: Apache-2.0
---

# 开发交付


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 连接与执行

先检查当前 MCP 的工具列表和 `editor_status`。有 `create_node`、`run_command`、`inspect_document` 时，使用实际工具 JSON schema；不猜测参数。通过 `list_commands` 找到本场景需要的命令及参数，再执行。

增强 Web 的 MCP 操作必须发生在已打开且就绪的同一页面。官方原版 Web 0.6.0 只有交互画面，文件服务尚未实现；没有这些 MCP 工具时不得假装已编辑或保存。独立原生 `figcraft-cli mcp` 是另一会话，切换必须明确告知。CLI 可用时用 `figcraft-cli commands --json` 检查命令；不自行安装缺失工具。

参考：[FigCraft v0.6.0 MCP](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)、[CLI](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)。命令以当前加载版本为准。

## 工作步骤

1. 检查页面尺寸、组件状态、命名与图片版权来源，确认开发端所需格式和倍率。
2. 用 list_commands 查询 inspect.properties、inspect.assets、inspect.code；按当前 schema 获取实际布局、文字、颜色和组件属性。
3. 选取需要开发的 frame 和组件，分别生成目标平台代码参考；注明这是设计导出的参考代码，尚未在应用项目中编译运行。
4. 导出图标 SVG、栅格图 PNG/WebP 和页面预览；读取实际文件，检查透明背景、尺寸、倍率与命名，避免将截图作为可编辑源文件。
5. 保存并重开 .figcraft；交付工程、资源列表、组件状态说明和代码参考。只报告实际生成的产物，未执行前端集成需明确。
