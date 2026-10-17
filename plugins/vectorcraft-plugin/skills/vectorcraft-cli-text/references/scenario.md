# 字体与字形操作指南

## 目标与前置

设置 Logo 和品牌文字，处理字体与导出轮廓。工程文字保持可编辑；outline-text 仅对指定交换副本使用，并记录字体编辑性损失。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands` 返回 JSON 参数目录；`run --in <工程> --cmd <id> --params <JSON> ... --export <新工程.vectorcraft>`，同批次解析对象 ID；convert 按扩展名输出。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `text.create` | Create Text |
| `type.createOutlines` | Create Outlines |
| `text.setText` | Set Text |
| `text.areaOptions` | Area Type Options… |
| `text.fitHeadline` | Fit Headline |
| `text.setStyle` | Character |
| `type.changeCase` | Change Case |
| `type.smartPunctuation` | Smart Punctuation… |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 44 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `charStyle` — 8

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `charStyle.list` | Character Styles | `describe charStyle.list` |
| `charStyle.new` | New Character Style | `describe charStyle.new` |
| `charStyle.apply` | Apply Character Style | `describe charStyle.apply` |
| `charStyle.redefine` | Redefine Character Style | `describe charStyle.redefine` |
| `charStyle.setAttrs` | Character Style Options | `describe charStyle.setAttrs` |
| `charStyle.duplicate` | Duplicate Character Style | `describe charStyle.duplicate` |
| `charStyle.rename` | Rename Character Style | `describe charStyle.rename` |
| `charStyle.delete` | Delete Character Style | `describe charStyle.delete` |

### `paraStyle` — 8

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `paraStyle.list` | Paragraph Styles | `describe paraStyle.list` |
| `paraStyle.new` | New Paragraph Style | `describe paraStyle.new` |
| `paraStyle.apply` | Apply Paragraph Style | `describe paraStyle.apply` |
| `paraStyle.redefine` | Redefine Paragraph Style | `describe paraStyle.redefine` |
| `paraStyle.setAttrs` | Paragraph Style Options | `describe paraStyle.setAttrs` |
| `paraStyle.duplicate` | Duplicate Paragraph Style | `describe paraStyle.duplicate` |
| `paraStyle.rename` | Rename Paragraph Style | `describe paraStyle.rename` |
| `paraStyle.delete` | Delete Paragraph Style | `describe paraStyle.delete` |

### `text` — 19

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `text.create` | Create Text | `describe text.create` |
| `text.setText` | Set Text | `describe text.setText` |
| `text.areaOptions` | Area Type Options… | `describe text.areaOptions` |
| `text.fitHeadline` | Fit Headline | `describe text.fitHeadline` |
| `text.setStyle` | Character | `describe text.setStyle` |
| `text.editRange` | Edit Text | `describe text.editRange` |
| `text.setRangeStyle` | Character | `describe text.setRangeStyle` |
| `text.getRange` | Get Text Range | `describe text.getRange` |
| `text.createInPath` | Area / Path Type | `describe text.createInPath` |
| `text.fonts` | Fonts in Document | `describe text.fonts` |
| `text.replaceFont` | Replace Font | `describe text.replaceFont` |
| `text.thread.create` | Create | `describe text.thread.create` |
| `text.thread.releaseSelection` | Release Selection | `describe text.thread.releaseSelection` |
| `text.thread.remove` | Remove Threading | `describe text.thread.remove` |
| `text.thread.info` | Threads | `describe text.thread.info` |
| `text.tabs.set` | Set Tab Stops | `describe text.tabs.set` |
| `text.tabs.get` | Tab Stops | `describe text.tabs.get` |
| `text.tabs.clear` | Clear All Tabs | `describe text.tabs.clear` |
| `text.setFormat` | Character / Paragraph | `describe text.setFormat` |

### `type` — 9

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `type.createOutlines` | Create Outlines | `describe type.createOutlines` |
| `type.changeCase` | Change Case | `describe type.changeCase` |
| `type.smartPunctuation` | Smart Punctuation… | `describe type.smartPunctuation` |
| `type.convertToAreaType` | Convert To Area Type | `describe type.convertToAreaType` |
| `type.convertToPointType` | Convert To Point Type | `describe type.convertToPointType` |
| `type.pathOptions` | Type on a Path Options… | `describe type.pathOptions` |
| `type.fillPlaceholder` | Fill with Placeholder Text | `describe type.fillPlaceholder` |
| `type.insert` | Insert Character | `describe type.insert` |
| `type.fitHeadline` | Fit Headline | `describe type.fitHeadline` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
