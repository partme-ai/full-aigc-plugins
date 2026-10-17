# 文字形状与图层操作指南

## 目标与前置

组织文本、形状、素材图层和层级合成。使用真实 layer/comp ID；文字改动保持其他动画，记录所用字体和替代。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `layer.newText` | Text |
| `layer.newSolid` | Solid... |
| `layer.newNull` | Null Object |
| `layer.newShape` | Shape Layer |
| `layer.newAdjustment` | Adjustment Layer |
| `layer.settings` | Layer Settings... |
| `layer.addItem` | Add Footage to Comp |
| `layer.select` | Select Layers |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 118 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `layer` — 100

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `layer.newText` | Text | `describe layer.newText` |
| `layer.newSolid` | Solid... | `describe layer.newSolid` |
| `layer.newNull` | Null Object | `describe layer.newNull` |
| `layer.newShape` | Shape Layer | `describe layer.newShape` |
| `layer.newAdjustment` | Adjustment Layer | `describe layer.newAdjustment` |
| `layer.settings` | Layer Settings... | `describe layer.settings` |
| `layer.addItem` | Add Footage to Comp | `describe layer.addItem` |
| `layer.select` | Select Layers | `describe layer.select` |
| `layer.selectNext` | Select Next Layer | `describe layer.selectNext` |
| `layer.selectPrevious` | Select Previous Layer | `describe layer.selectPrevious` |
| `layer.rename` | Rename | `describe layer.rename` |
| `layer.setComment` | Layer Comment | `describe layer.setComment` |
| `layer.setBlendMode` | Blending Mode | `describe layer.setBlendMode` |
| `layer.setTrackMatte` | Track Matte | `describe layer.setTrackMatte` |
| `layer.setParent` | Parent | `describe layer.setParent` |
| `layer.timing` | Layer Timing | `describe layer.timing` |
| `layer.slip` | Slip Edit | `describe layer.slip` |
| `layer.slipBack` | Slip Edit 1 Frame Earlier | `describe layer.slipBack` |
| `layer.slipForward` | Slip Edit 1 Frame Later | `describe layer.slipForward` |
| `layer.arrange` | Arrange | `describe layer.arrange` |
| `layer.precompose` | Pre-compose... | `describe layer.precompose` |
| `layer.addMask` | New Mask | `describe layer.addMask` |
| `layer.setMask` | Mask Mode | `describe layer.setMask` |
| `layer.addShapeItem` | Add (Shape) | `describe layer.addShapeItem` |
| `layer.setText` | Edit Text | `describe layer.setText` |
| `layer.transform` | Transform | `describe layer.transform` |
| `layer.style.convertToEditable` | Convert to Editable Styles | `describe layer.style.convertToEditable` |
| `layer.style.showAll` | Show All | `describe layer.style.showAll` |
| `layer.style.removeAll` | Remove All | `describe layer.style.removeAll` |
| `layer.style.dropShadow` | Drop Shadow | `describe layer.style.dropShadow` |
| `layer.style.innerShadow` | Inner Shadow | `describe layer.style.innerShadow` |
| `layer.style.outerGlow` | Outer Glow | `describe layer.style.outerGlow` |
| `layer.style.innerGlow` | Inner Glow | `describe layer.style.innerGlow` |
| `layer.style.bevelEmboss` | Bevel and Emboss | `describe layer.style.bevelEmboss` |
| `layer.style.satin` | Satin | `describe layer.style.satin` |
| `layer.style.colorOverlay` | Color Overlay | `describe layer.style.colorOverlay` |
| `layer.style.gradientOverlay` | Gradient Overlay | `describe layer.style.gradientOverlay` |
| `layer.style.stroke` | Stroke | `describe layer.style.stroke` |
| `layer.style.add` | Add Layer Style | `describe layer.style.add` |
| `layer.style.remove` | Remove Layer Style | `describe layer.style.remove` |
| `layer.style.toggle` | Toggle Layer Style | `describe layer.style.toggle` |
| `layer.style.globalLight` | Global Light | `describe layer.style.globalLight` |
| `layer.style.list` | List Layer Styles | `describe layer.style.list` |
| `layer.autoOrient` | Auto-Orient... | `describe layer.autoOrient` |
| `layer.lightSettings` | Light Settings... | `describe layer.lightSettings` |
| `layer.newModel` | 3D Model Layer | `describe layer.newModel` |
| `layer.newPrimitive` | New 3D Primitive | `describe layer.newPrimitive` |
| `layer.environment` | Environment Layer | `describe layer.environment` |
| `layer.addTextAnimator` | Animate Text | `describe layer.addTextAnimator` |
| `layer.addTextAnimatorProperty` | Add Property | `describe layer.addTextAnimatorProperty` |
| `layer.addTextSelector` | Add Text Selector | `describe layer.addTextSelector` |
| `layer.enablePerChar3D` | Enable Per-character 3D | `describe layer.enablePerChar3D` |
| `layer.applyTextPreset` | Apply Text Animation Preset | `describe layer.applyTextPreset` |
| `layer.timeStretch` | Time Stretch... | `describe layer.timeStretch` |
| `layer.timeReverse` | Time-Reverse Layer | `describe layer.timeReverse` |
| `layer.enableTimeRemap` | Enable Time Remapping | `describe layer.enableTimeRemap` |
| `layer.freezeFrame` | Freeze Frame | `describe layer.freezeFrame` |
| `layer.freezeOnLastFrame` | Freeze On Last Frame | `describe layer.freezeOnLastFrame` |
| `layer.updateMarkersFromSource` | Update Markers From Source | `describe layer.updateMarkersFromSource` |
| `layer.mask.motionBlur` | Motion Blur | `describe layer.mask.motionBlur` |
| `layer.mask.featherFalloff` | Feather Falloff | `describe layer.mask.featherFalloff` |
| `layer.mask.hideLocked` | Hide Locked Masks | `describe layer.mask.hideLocked` |
| `layer.tree` | Layer Property Tree | `describe layer.tree` |
| `layer.quality` | Quality | `describe layer.quality` |
| `layer.sampling` | Sampling | `describe layer.sampling` |
| `layer.frameBlending` | Frame Blending | `describe layer.frameBlending` |
| `layer.hideOtherVideo` | Hide Other Video | `describe layer.hideOtherVideo` |
| `layer.showAllVideo` | Show All Video | `describe layer.showAllVideo` |
| `layer.unlockAll` | Unlock All Layers | `describe layer.unlockAll` |
| `layer.expressions` | Enable/Disable Expressions | `describe layer.expressions` |
| `layer.setTransform` | Transform Value | `describe layer.setTransform` |
| `layer.centerAnchor` | Center Anchor Point in Layer Content | `describe layer.centerAnchor` |
| `layer.mask.shape` | Mask Shape... | `describe layer.mask.shape` |
| `layer.mask.set` | Mask Settings | `describe layer.mask.set` |
| `layer.mask.reset` | Reset Mask | `describe layer.mask.reset` |
| `layer.mask.remove` | Remove Mask | `describe layer.mask.remove` |
| `layer.mask.removeAll` | Remove All Masks | `describe layer.mask.removeAll` |
| `layer.mask.mode` | Mask Mode | `describe layer.mask.mode` |
| `layer.mask.invert` | Inverted | `describe layer.mask.invert` |
| `layer.mask.lock` | Locked | `describe layer.mask.lock` |
| `layer.mask.unlockAll` | Unlock All Masks | `describe layer.mask.unlockAll` |
| `layer.mask.lockOthers` | Lock Other Masks | `describe layer.mask.lockOthers` |
| `layer.addMarker` | Add Marker | `describe layer.addMarker` |
| `layer.markersLock` | Lock Markers | `describe layer.markersLock` |
| `layer.deleteAllMarkers` | Delete All Markers | `describe layer.deleteAllMarkers` |
| `layer.trackMatte` | Track Matte | `describe layer.trackMatte` |
| `layer.openSource` | Open Layer Source | `describe layer.openSource` |
| `layer.revealInFinder` | Reveal in Finder | `describe layer.revealInFinder` |
| `layer.revealSource` | Reveal Layer Source in Project | `describe layer.revealSource` |
| `layer.revealExpressionErrors` | Reveal Expression Errors | `describe layer.revealExpressionErrors` |
| `layer.sequence` | Sequence Layers... | `describe layer.sequence` |
| `layer.create` | Create | `describe layer.create` |
| `layer.style.options` | Layer Style Options... | `describe layer.style.options` |
| `layer.openLayer` | Open Layer | `describe layer.openLayer` |
| `layer.autoTrace` | Auto-trace... | `describe layer.autoTrace` |
| `layer.sceneEditDetection` | Scene Edit Detection... | `describe layer.sceneEditDetection` |
| `layer.alignVideoToData` | Align Video to Data | `describe layer.alignVideoToData` |
| `layer.align` | Align Layers | `describe layer.align` |
| `layer.distribute` | Distribute Layers | `describe layer.distribute` |
| `layer.newContentAwareFill` | Content-Aware Fill Layer... | `describe layer.newContentAwareFill` |

### `shape` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `shape.newPath` | Pen Tool (Shape Path) | `describe shape.newPath` |
| `shape.dashes.add` | Add Dash or Gap | `describe shape.dashes.add` |
| `shape.dashes.remove` | Remove Dash or Gap | `describe shape.dashes.remove` |
| `shape.stroke.taper` | Stroke Taper | `describe shape.stroke.taper` |
| `shape.stroke.wave` | Stroke Wave | `describe shape.stroke.wave` |

### `text` — 13

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `text.animatorFontAxes` | Variable Font Axes | `describe text.animatorFontAxes` |
| `text.presets` | Text Animation Presets | `describe text.presets` |
| `text.animatorProperties` | Text Animator Properties | `describe text.animatorProperties` |
| `text.edit` | Edit Text | `describe text.edit` |
| `text.endEdit` | Exit Text Editing | `describe text.endEdit` |
| `text.fontFeatures` | OpenType Features | `describe text.fontFeatures` |
| `text.fonts` | List Fonts | `describe text.fonts` |
| `text.setSelection` | Set Text Selection | `describe text.setSelection` |
| `text.moveCaret` | Move Text Caret | `describe text.moveCaret` |
| `text.insert` | Type Text | `describe text.insert` |
| `text.delete` | Delete Text | `describe text.delete` |
| `text.addSelector` | Add Text Selector | `describe text.addSelector` |
| `text.removeAllAnimators` | Remove All Text Animators | `describe text.removeAllAnimators` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
