# 属性与关键帧动画操作指南

## 目标与前置

设置属性、关键帧、缓动和文字图形动画。props/get 核对路径与时刻；更新指定关键帧而非重建整层。关键时刻渲染比较。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `prop.get` | Get Property |
| `prop.set` | Set Property Value |
| `prop.toggleAnimation` | Toggle Stopwatch |
| `prop.addKey` | Add Keyframe |
| `prop.toggleKey` | Add or Remove Keyframe at Current Time |
| `keys.toggleTransform` | Add or Remove Transform Keyframe |
| `prop.setExpression` | Add Expression |
| `prop.reset` | Reset Property |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 55 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `anim` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `anim.savePreset` | Save Animation Preset... | `describe anim.savePreset` |
| `anim.applyPreset` | Apply Animation Preset... | `describe anim.applyPreset` |
| `anim.addKeyframe` | Add Keyframe | `describe anim.addKeyframe` |
| `anim.reveal` | Reveal Properties | `describe anim.reveal` |
| `anim.browsePresets` | Browse Presets... | `describe anim.browsePresets` |
| `anim.applyRecentPreset` | Recent Animation Presets | `describe anim.applyRecentPreset` |
| `anim.clearRecentPresets` | Clear Recent Presets | `describe anim.clearRecentPresets` |

### `keys` — 34

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `keys.toggleTransform` | Add or Remove Transform Keyframe | `describe keys.toggleTransform` |
| `keys.select` | Select Keyframes | `describe keys.select` |
| `keys.move` | Move Keyframes | `describe keys.move` |
| `keys.delete` | Delete Keyframes | `describe keys.delete` |
| `keys.easyEase` | Easy Ease | `describe keys.easyEase` |
| `keys.easyEaseIn` | Easy Ease In | `describe keys.easyEaseIn` |
| `keys.easyEaseOut` | Easy Ease Out | `describe keys.easyEaseOut` |
| `keys.toggleHold` | Toggle Hold Keyframe | `describe keys.toggleHold` |
| `keys.interpolation` | Keyframe Interpolation... | `describe keys.interpolation` |
| `keys.velocity` | Keyframe Velocity... | `describe keys.velocity` |
| `keys.copy` | Copy Keyframes | `describe keys.copy` |
| `keys.paste` | Paste Keyframes | `describe keys.paste` |
| `keys.selectAll` | Select All Keyframes | `describe keys.selectAll` |
| `keys.nudge` | Nudge Keyframes | `describe keys.nudge` |
| `keys.nudgeForward` | Move Keyframes 1 Frame Later | `describe keys.nudgeForward` |
| `keys.nudgeBackward` | Move Keyframes 1 Frame Earlier | `describe keys.nudgeBackward` |
| `keys.nudgeForward10` | Move Keyframes 10 Frames Later | `describe keys.nudgeForward10` |
| `keys.nudgeBackward10` | Move Keyframes 10 Frames Earlier | `describe keys.nudgeBackward10` |
| `keys.set` | Edit Keyframe | `describe keys.set` |
| `keys.selectEqual` | Select Equal Keyframes | `describe keys.selectEqual` |
| `keys.selectPrevious` | Select Previous Keyframes | `describe keys.selectPrevious` |
| `keys.selectFollowing` | Select Following Keyframes | `describe keys.selectFollowing` |
| `keys.setEase` | Set Keyframe Ease | `describe keys.setEase` |
| `keys.timeReverse` | Time-Reverse Keyframes | `describe keys.timeReverse` |
| `keys.info` | Keyframe Info | `describe keys.info` |
| `keys.wiggle` | Wiggler | `describe keys.wiggle` |
| `keys.smooth` | Smoother | `describe keys.smooth` |
| `keys.exponentialScale` | Exponential Scale | `describe keys.exponentialScale` |
| `keys.setLabel` | Keyframe Label | `describe keys.setLabel` |
| `keys.selectLabelGroup` | Select Keyframe Label Group | `describe keys.selectLabelGroup` |
| `keys.transform` | Transform Keyframes | `describe keys.transform` |
| `keys.setSpatialTangents` | Edit Spatial Tangents | `describe keys.setSpatialTangents` |
| `keys.audioToKeyframes` | Convert Audio to Keyframes | `describe keys.audioToKeyframes` |
| `keys.rpfCameraImport` | RPF Camera Import | `describe keys.rpfCameraImport` |

### `prop` — 14

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `prop.get` | Get Property | `describe prop.get` |
| `prop.set` | Set Property Value | `describe prop.set` |
| `prop.toggleAnimation` | Toggle Stopwatch | `describe prop.toggleAnimation` |
| `prop.addKey` | Add Keyframe | `describe prop.addKey` |
| `prop.toggleKey` | Add or Remove Keyframe at Current Time | `describe prop.toggleKey` |
| `prop.reset` | Reset Property | `describe prop.reset` |
| `prop.select` | Select Property | `describe prop.select` |
| `prop.renameGroup` | Rename Property Group | `describe prop.renameGroup` |
| `prop.setGroupEnabled` | Enable Property Group | `describe prop.setGroupEnabled` |
| `prop.removeGroup` | Delete Property Group | `describe prop.removeGroup` |
| `prop.duplicateGroup` | Duplicate Property Group | `describe prop.duplicateGroup` |
| `prop.moveGroup` | Reorder Property Group | `describe prop.moveGroup` |
| `prop.separateDimensions` | Separate Dimensions | `describe prop.separateDimensions` |
| `prop.pickWhip` | Pick Whip (Link Property) | `describe prop.pickWhip` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
