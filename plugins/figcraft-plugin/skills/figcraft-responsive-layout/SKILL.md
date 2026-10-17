---
name: figcraft-responsive-layout
description: 当需要用 FigCraft 做移动端、平板、桌面适配，处理自动布局、换行或内容溢出时使用。
license: Apache-2.0
---

# 响应式布局


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 连接与执行

先检查当前 MCP 的工具列表和 `editor_status`。有 `create_node`、`run_command`、`inspect_document` 时，使用实际工具 JSON schema；不猜测参数。通过 `list_commands` 找到本场景需要的命令及参数，再执行。

增强 Web 的 MCP 操作必须发生在已打开且就绪的同一页面。官方原版 Web 0.6.0 只有交互画面，文件服务尚未实现；没有这些 MCP 工具时不得假装已编辑或保存。独立原生 `figcraft-cli mcp` 是另一会话，切换必须明确告知。CLI 可用时用 `figcraft-cli commands --json` 检查命令；不自行安装缺失工具。

参考：[FigCraft v0.6.0 MCP](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)、[CLI](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)。命令以当前加载版本为准。

## 工作步骤

1. 检查现有 frame、容器层级及主要内容宽度，确认哪些模块应换行、折叠或隐藏。
2. 通过 list_commands 查询 layout.add 等实际命令，将相关容器转为横向、纵向或 grid；用 gap、padding、sizingH、sizingV 表达布局意图，避免同时用绝对 x/y 固定流内子项。
3. 建立 390×884、768×1024、1280×1024 三种 frame；重要组件保留同一套内容与语义顺序。
4. 检查 Hug 与 Fill 的父子约束、长标题、空内容、较多列表项；对每种尺寸分别截图和读取 absoluteBounds，识别出界节点。
5. 保存可编辑工程并重开；导出三种尺寸图，说明断点行为及仍需真实前端验证的交互。
