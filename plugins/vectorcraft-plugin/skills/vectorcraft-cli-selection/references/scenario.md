# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 57 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `object` — 10

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `object.lock` | Selection | `describe object.lock` |
| `object.unlockAll` | Unlock All | `describe object.unlockAll` |
| `object.hide` | Selection | `describe object.hide` |
| `object.showAll` | Show All | `describe object.showAll` |
| `object.isolate` | Enter Isolation Mode | `describe object.isolate` |
| `object.exitIsolation` | Exit Isolation Mode | `describe object.exitIsolation` |
| `object.lock.above` | All Artwork Above | `describe object.lock.above` |
| `object.lock.otherLayers` | Other Layers | `describe object.lock.otherLayers` |
| `object.hide.above` | All Artwork Above | `describe object.hide.above` |
| `object.hide.otherLayers` | Other Layers | `describe object.hide.otherLayers` |

### `select` — 47

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `select.all` | All | `describe select.all` |
| `select.allOnArtboard` | All on Active Artboard | `describe select.allOnArtboard` |
| `select.none` | Deselect | `describe select.none` |
| `select.reselect` | Reselect | `describe select.reselect` |
| `select.inverse` | Inverse | `describe select.inverse` |
| `select.nextAbove` | Next Object Above | `describe select.nextAbove` |
| `select.nextBelow` | Next Object Below | `describe select.nextBelow` |
| `select.set` | Select Objects | `describe select.set` |
| `select.add` | Add to Selection | `describe select.add` |
| `select.toggle` | Toggle Selection | `describe select.toggle` |
| `select.key` | Set Key Object | `describe select.key` |
| `select.anchors` | Select Anchors | `describe select.anchors` |
| `select.anchorsMany` | Select Anchors | `describe select.anchorsMany` |
| `select.same.fillColor` | Fill Color | `describe select.same.fillColor` |
| `select.same.strokeColor` | Stroke Color | `describe select.same.strokeColor` |
| `select.same.strokeWeight` | Stroke Weight | `describe select.same.strokeWeight` |
| `select.same.fillAndStroke` | Fill & Stroke | `describe select.same.fillAndStroke` |
| `select.same.opacity` | Opacity | `describe select.same.opacity` |
| `select.same.blendingMode` | Blending Mode | `describe select.same.blendingMode` |
| `select.same.appearance` | Appearance | `describe select.same.appearance` |
| `select.same.shapeType` | Shape | `describe select.same.shapeType` |
| `select.object.allOnSameLayers` | All on Same Layers | `describe select.object.allOnSameLayers` |
| `select.object.clippingMasks` | Clipping Masks | `describe select.object.clippingMasks` |
| `select.object.textObjects` | All Text Objects | `describe select.object.textObjects` |
| `select.object.strayPoints` | Stray Points | `describe select.object.strayPoints` |
| `select.object.openPaths` | Open Paths | `describe select.object.openPaths` |
| `select.same.graphicStyle` | Graphic Style | `describe select.same.graphicStyle` |
| `select.same.appearanceAttribute` | Appearance Attribute | `describe select.same.appearanceAttribute` |
| `select.magicWand` | Magic Wand | `describe select.magicWand` |
| `select.font` | Select Text by Font | `describe select.font` |
| `select.same.symbolInstance` | Symbol Instance | `describe select.same.symbolInstance` |
| `select.same.fontFamily` | Font Family | `describe select.same.fontFamily` |
| `select.same.fontFamilyStyle` | Font Family & Style | `describe select.same.fontFamilyStyle` |
| `select.same.fontFamilyStyleSize` | Font Family, Style & Size | `describe select.same.fontFamilyStyleSize` |
| `select.same.fontSize` | Font Size | `describe select.same.fontSize` |
| `select.same.textFillColor` | Text Fill Color | `describe select.same.textFillColor` |
| `select.same.textStrokeColor` | Text Stroke Color | `describe select.same.textStrokeColor` |
| `select.object.directionHandles` | Direction Handles | `describe select.object.directionHandles` |
| `select.object.pointText` | Point Text Objects | `describe select.object.pointText` |
| `select.object.areaText` | Area Text Objects | `describe select.object.areaText` |
| `select.object.brushStrokes` | Brush Strokes | `describe select.object.brushStrokes` |
| `select.object.bristleBrushStrokes` | Bristle Brush Strokes | `describe select.object.bristleBrushStrokes` |
| `select.save` | Save Selection… | `describe select.save` |
| `select.recall` | Recall Selection | `describe select.recall` |
| `select.editSaved` | Edit Selection… | `describe select.editSaved` |
| `select.savedList` | Saved Selections | `describe select.savedList` |
| `select.object.slices` | Slices | `describe select.object.slices` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
