---
name: deckcraft-use
description: 使用 DeckCraft 创建、修改、检查或导出演示文稿时使用；通过宿主已连接的 DeckCraft MCP 或已安装的 deckcraft-cli 操作真实文稿，并回读结果。
---

# DeckCraft 演示文稿

使用宿主提供的 DeckCraft MCP 工具完成连续编辑。若宿主未连接 MCP，但已安装 `deckcraft-cli`，使用其现有 CLI。插件和本技能不安装 CLI，也不实现第二套编辑引擎。

## 开始

1. 确认用户指定的源文件、输出位置、目标格式和是否允许修改；审查任务只读。
2. 优先调用 `list_commands` 查看当前可用命令及参数，或运行 `deckcraft-cli commands` 和 `deckcraft-cli describe <命令ID>`。命令是否可用以当前工具返回为准，不照抄静态示例推断。
3. MCP 路径在同一次任务中继续使用宿主保持的连接。Headless 默认操作私有文稿；只有用户明确要求连接已运行的桌面应用且宿主已配置 Remote 时才使用桌面模式。不要关闭用户的桌面进程。

## 创建与修改

- 新稿使用 `new_presentation`；需要更多页时用 `add_slide`。既有文稿使用 `open_presentation`。
- 复杂编辑先读取 `list_commands` 的当前 ID、参数和 enabled 状态，再调用 `run_command`。`batch` 仅用于顺序和失败语义已明确的一组命令。
- 每段修改后调用 `inspect_document` 或 `inspect_slide` 回读文字、页数和对象；需要视觉判断时调用 `render_slide`。
- 保存使用 `save_presentation`，优先保留可编辑的 `.deckcraft` 源文件。CLI 路径可用 `deckcraft-cli run`、`info`、`render` 和 `convert`，参数以当前 `deckcraft-cli` 输出为准。

## 交付与异常

- 导出使用 `export`，检查返回和目标文件。PPTX、PDF、图片的结果要分别核对；不要声称所有格式与源文稿无损等价。
- 修改操作超时或连接断开后，先重新打开或检查现有文稿，报告已确认状态；不要盲目重发可能已经执行的修改。
- CLI 缺失、MCP 未连接或命令不可用时说明准确的前置条件。未经用户授权不安装工具、不启动或接管桌面应用。
- 交付时给出源文稿、导出文件、结构回读与视觉检查的实际结果；未运行的检查标明未运行。
