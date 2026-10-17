# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 22 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `track` — 22

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `track.motion` | Track Motion | `describe track.motion` |
| `track.stabilize` | Stabilize Motion | `describe track.stabilize` |
| `track.new` | New Tracker | `describe track.new` |
| `track.property` | Track this Property | `describe track.property` |
| `track.select` | Current Track | `describe track.select` |
| `track.setType` | Track Type | `describe track.setType` |
| `track.setTarget` | Edit Target | `describe track.setTarget` |
| `track.options` | Motion Tracker Options | `describe track.options` |
| `track.setPoint` | Move Track Point | `describe track.setPoint` |
| `track.analyze` | Analyze | `describe track.analyze` |
| `track.stop` | Stop Analysis | `describe track.stop` |
| `track.apply` | Apply | `describe track.apply` |
| `track.reset` | Reset | `describe track.reset` |
| `track.delete` | Delete Tracker | `describe track.delete` |
| `track.editTargetDialog` | Edit Target... | `describe track.editTargetDialog` |
| `track.optionsDialog` | Options... | `describe track.optionsDialog` |
| `track.status` | Tracker Status | `describe track.status` |
| `track.mask` | Track Mask | `describe track.mask` |
| `track.maskMethod` | Mask Tracking Method | `describe track.maskMethod` |
| `track.extractFaceMeasurements` | Extract & Copy Face Measurements | `describe track.extractFaceMeasurements` |
| `track.warpStabilizer` | Warp Stabilizer VFX | `describe track.warpStabilizer` |
| `track.camera` | Track Camera | `describe track.camera` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
