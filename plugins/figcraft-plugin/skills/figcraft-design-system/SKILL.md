---
name: figcraft-design-system
description: 当需要用 FigCraft 创建组件库、按钮状态、颜色与字体变量、明暗主题或统一设计规范时使用。
license: Apache-2.0
---

# 组件与设计系统


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 连接与执行

先检查当前 MCP 的工具列表和 `editor_status`。有 `create_node`、`run_command`、`inspect_document` 时，使用实际工具 JSON schema；不猜测参数。通过 `list_commands` 找到本场景需要的命令及参数，再执行。

增强 Web 的 MCP 操作必须发生在已打开且就绪的同一页面。官方原版 Web 0.6.0 只有交互画面，文件服务尚未实现；没有这些 MCP 工具时不得假装已编辑或保存。独立原生 `figcraft-cli mcp` 是另一会话，切换必须明确告知。CLI 可用时用 `figcraft-cli commands --json` 检查命令；不自行安装缺失工具。

参考：[FigCraft v0.6.0 MCP](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)、[CLI](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)。命令以当前加载版本为准。

## 工作步骤

1. 盘点已有颜色、文本样式与重复结构，先约定命名和组件边界；保留现有实例关系。
2. 查询 style.create、variable 相关命令；创建颜色、字号与间距变量，按语义命名，建立明暗模式映射。
3. 查询 component.create、instance.place，将按钮、输入框、卡片做成组件；以实际 schema 创建状态与尺寸变体，记录返回 ID。
4. 在示例页面放置实例；修改主组件，检查实例继承和人工覆写是否符合预期。测试长文案、禁用和错误状态。
5. 检查变量绑定与样式链接，截图比较主题；保存 .figcraft，重开并验证实例与变量仍存在，交付组件表及使用说明。
