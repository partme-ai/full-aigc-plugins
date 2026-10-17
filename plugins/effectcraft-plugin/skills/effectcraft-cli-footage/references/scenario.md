# 素材与预合成输入操作指南

## 目标与前置

导入图像、视频、矢量或 PSD 素材并登记依赖。检查实际导入结构；PSD/SVG 图层、字体与效果保真必须另行核验。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `footage.check` | Check Footage |
| `mediaBrowser.list` | List Folder |
| `mediaBrowser.go` | Go to Folder |
| `mediaBrowser.addFavorite` | Add to Favorites |
| `mediaBrowser.removeFavorite` | Remove from Favorites |
| `mediaBrowser.import` | Import |
| `mediaBrowser.action` | Media Browser Action |
| `mediaBrowser.fileInfo` | File Info |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 16 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `footage` — 9

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `footage.check` | Check Footage | `describe footage.check` |
| `footage.open` | Open in Footage Panel | `describe footage.open` |
| `footage.info` | Footage Panel State | `describe footage.info` |
| `footage.setTime` | Footage Panel Time | `describe footage.setTime` |
| `footage.setIn` | Set In Point | `describe footage.setIn` |
| `footage.setOut` | Set Out Point | `describe footage.setOut` |
| `footage.clearInOut` | Clear In and Out | `describe footage.clearInOut` |
| `footage.overlayEdit` | Overlay Edit | `describe footage.overlayEdit` |
| `footage.rippleInsertEdit` | Ripple Insert Edit | `describe footage.rippleInsertEdit` |

### `mediaBrowser` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `mediaBrowser.list` | List Folder | `describe mediaBrowser.list` |
| `mediaBrowser.go` | Go to Folder | `describe mediaBrowser.go` |
| `mediaBrowser.addFavorite` | Add to Favorites | `describe mediaBrowser.addFavorite` |
| `mediaBrowser.removeFavorite` | Remove from Favorites | `describe mediaBrowser.removeFavorite` |
| `mediaBrowser.import` | Import | `describe mediaBrowser.import` |
| `mediaBrowser.action` | Media Browser Action | `describe mediaBrowser.action` |
| `mediaBrowser.fileInfo` | File Info | `describe mediaBrowser.fileInfo` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
