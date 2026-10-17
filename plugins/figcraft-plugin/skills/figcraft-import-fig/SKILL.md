---
name: figcraft-import-fig
description: 当需要把 Figma .fig、REST 文件 JSON 或 SVG 导入 FigCraft，并检查字体、图片、组件与布局损失时使用。
license: Apache-2.0
---

# 设计稿迁移


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 连接与执行

先检查当前 MCP 的工具列表和 `editor_status`。有 `create_node`、`run_command`、`inspect_document` 时，使用实际工具 JSON schema；不猜测参数。通过 `list_commands` 找到本场景需要的命令及参数，再执行。

增强 Web 的 MCP 操作必须发生在已打开且就绪的同一页面。官方原版 Web 0.6.0 只有交互画面，文件服务尚未实现；没有这些 MCP 工具时不得假装已编辑或保存。独立原生 `figcraft-cli mcp` 是另一会话，切换必须明确告知。CLI 可用时用 `figcraft-cli commands --json` 检查命令；不自行安装缺失工具。

参考：[FigCraft v0.6.0 MCP](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)、[CLI](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)。命令以当前加载版本为准。

## 工作步骤

1. 保留输入原件。列出文件格式、关联图片与字体，确认目标工程的新路径；REST JSON 的图片放在其相邻 images 目录。
2. 使用 open_file 或已存在的 figcraft-cli convert 导入；.fig 是尽力兼容，读取实际返回警告，不宣称像素完全一致。
3. 通过 inspect_document 核对页面数、顶层 frame、组件实例、变量及原型；缺失图片、字体替代和不支持效果逐项记录。
4. 对关键页面截图与原稿对照，优先修复布局、文案和主视觉；可编辑结构优先，必要栅格化必须明确告知。
5. 保存新 .figcraft 文件，重开和导出 PNG；交付迁移工程、预览和损失清单，避免覆盖输入 .fig。
