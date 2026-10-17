---
name: figcraft-wireframe
description: 当需要用 FigCraft 将页面需求变成低保真线框、信息架构或首版产品界面时使用。
license: Apache-2.0
---

# 低保真线框


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 连接与执行

先检查当前 MCP 的工具列表和 `editor_status`。有 `create_node`、`run_command`、`inspect_document` 时，使用实际工具 JSON schema；不猜测参数。通过 `list_commands` 找到本场景需要的命令及参数，再执行。

增强 Web 的 MCP 操作必须发生在已打开且就绪的同一页面。官方原版 Web 0.6.0 只有交互画面，文件服务尚未实现；没有这些 MCP 工具时不得假装已编辑或保存。独立原生 `figcraft-cli mcp` 是另一会话，切换必须明确告知。CLI 可用时用 `figcraft-cli commands --json` 检查命令；不自行安装缺失工具。

参考：[FigCraft v0.6.0 MCP](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)、[CLI](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)。命令以当前加载版本为准。

## 工作步骤

1. 从用户需求列出主任务、必要字段、导航入口与空状态；未知文案标注占位，避免虚构业务指标。
2. 创建 390×884、768×1024、1280×1024 的相应 frame；先做当前目标端，其他端按需求补齐。读取 create_node 返回的 ID，不推算后续 ID。
3. 以单色块和文字建立导航、标题、主内容、主操作；通过 set_properties 设置字体层级、留白和边界。先检查阅读顺序，再添加装饰。
4. 用 inspect_document 检查层级、父 frame、尺寸；使用 screenshot 验证溢出、遮挡、按钮可识别性。调整后重新检查受影响区域。
5. 通过 save_file 保存新的 .figcraft 路径，重开并比对 frame 与节点；导出每个页面 PNG，并交付未决业务问题清单。
