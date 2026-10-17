# 矢量工程与图层操作指南

## 目标与前置

建立和重开 vectorcraft，整理图层与文档属性。先确定单位、画板和颜色模式；原生另存并 info 重开。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands` 返回 JSON 参数目录；`run --in <工程> --cmd <id> --params <JSON> ... --export <新工程.vectorcraft>`，同批次解析对象 ID；convert 按扩展名输出。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `file.new` | New… |
| `file.close` | Close |
| `document.activate` | Activate Document |
| `document.inspect` | Inspect Document |
| `document.node` | Inspect Object |
| `document.json` | Document JSON |
| `document.setUnits` | Units |
| `document.open` | Open Document |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 43 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `document` — 14

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `document.activate` | Activate Document | `describe document.activate` |
| `document.inspect` | Inspect Document | `describe document.inspect` |
| `document.node` | Inspect Object | `describe document.node` |
| `document.json` | Document JSON | `describe document.json` |
| `document.setUnits` | Units | `describe document.setUnits` |
| `document.open` | Open Document | `describe document.open` |
| `document.serialize` | Serialize Document | `describe document.serialize` |
| `document.formats` | File Formats | `describe document.formats` |
| `document.pdfInfo` | PDF Info | `describe document.pdfInfo` |
| `document.save` | Save Document | `describe document.save` |
| `document.rasterEffectsSettings` | Document Raster Effects Settings… | `describe document.rasterEffectsSettings` |
| `document.info` | Document Info | `describe document.info` |
| `document.pdfSettings` | PDF Settings | `describe document.pdfSettings` |
| `document.setup` | Document Setup | `describe document.setup` |

### `file` — 17

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `file.new` | New… | `describe file.new` |
| `file.close` | Close | `describe file.close` |
| `file.saveAs` | Save As… | `describe file.saveAs` |
| `file.saveCopy` | Save a Copy… | `describe file.saveCopy` |
| `file.saveAsTemplate` | Save as Template… | `describe file.saveAsTemplate` |
| `file.newFromTemplate` | New from Template… | `describe file.newFromTemplate` |
| `file.revert` | Revert | `describe file.revert` |
| `file.formatOptions` | Format Options | `describe file.formatOptions` |
| `file.closeAll` | Close All | `describe file.closeAll` |
| `file.documentColorMode` | Document Color Mode | `describe file.documentColorMode` |
| `file.info` | File Info… | `describe file.info` |
| `file.newPresets` | New Document Presets | `describe file.newPresets` |
| `file.newPresets.save` | Save Preset | `describe file.newPresets.save` |
| `file.newPresets.delete` | Delete Preset | `describe file.newPresets.delete` |
| `file.package` | Package | `describe file.package` |
| `file.open` | Open… | `describe file.open` |
| `file.save` | Save | `describe file.save` |

### `layer` — 11

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `layer.new` | New Layer… | `describe layer.new` |
| `layer.newSublayer` | New Sublayer… | `describe layer.newSublayer` |
| `layer.delete` | Delete Layer | `describe layer.delete` |
| `layer.duplicate` | Duplicate Layer | `describe layer.duplicate` |
| `layer.setCurrent` | Set Current Layer | `describe layer.setCurrent` |
| `layer.setProps` | Layer Options… | `describe layer.setProps` |
| `layer.collectInNew` | Collect in New Layer | `describe layer.collectInNew` |
| `layer.selectAll` | Select All Art on Layer | `describe layer.selectAll` |
| `layer.clippingMask.toggle` | Make/Release Clipping Mask | `describe layer.clippingMask.toggle` |
| `layer.target` | Target | `describe layer.target` |
| `layer.pasteRemembersLayers` | Paste Remembers Layers | `describe layer.pasteRemembersLayers` |

### `object` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `object.convertDocumentColorMode` | Convert Document Color Mode | `describe object.convertDocumentColorMode` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
