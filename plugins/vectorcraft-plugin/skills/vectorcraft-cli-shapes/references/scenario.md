# 形状与组合操作指南

## 目标与前置

建立几何形状并组合、变换品牌图形。变换保持单位和中心点明确；保留可编辑对象，不自动扩展全部外观。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands` 返回 JSON 参数目录；`run --in <工程> --cmd <id> --params <JSON> ... --export <新工程.vectorcraft>`，同批次解析对象 ID；convert 按扩展名输出。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `shape.rectangle` | Rectangle |
| `shape.ellipse` | Ellipse |
| `shape.polygon` | Polygon |
| `shape.star` | Star |
| `shape.flare` | Flare |
| `shape.line` | Line Segment |
| `shape.spiral` | Spiral |
| `shape.arc` | Arc |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

## 已验证的选择前置（CLI 0.2.0）

重新打开工程后，不把原会话的活动选择视为已保存。创建多个对象后，从各自真实回执取得 ID，再在同一 `run` 内执行 `select.set` 和 `object.group` 或 `object.pathfinder.unite`。不能仅因几何对象存在就执行依赖选择的命令。布尔运算返回 `ids` 数组，分组返回 `id`；采用实际结果继续操作。

分组保持子对象可编辑；布尔并集在此已测样本中生成原生路径，并移除参与运算的两个输入对象。核验其他 Logo、文字与画板未变化，保留原工程，另存新 `.vectorcraft`。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 36 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `object` — 26

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `object.transform` | Transform | `describe object.transform` |
| `object.move` | Move… | `describe object.move` |
| `object.rotate` | Rotate… | `describe object.rotate` |
| `object.scale` | Scale… | `describe object.scale` |
| `object.reflect` | Reflect… | `describe object.reflect` |
| `object.shear` | Shear… | `describe object.shear` |
| `object.transformAgain` | Transform Again | `describe object.transformAgain` |
| `object.nudge` | Nudge | `describe object.nudge` |
| `object.arrange.bringToFront` | Bring to Front | `describe object.arrange.bringToFront` |
| `object.arrange.bringForward` | Bring Forward | `describe object.arrange.bringForward` |
| `object.arrange.sendBackward` | Send Backward | `describe object.arrange.sendBackward` |
| `object.arrange.sendToBack` | Send to Back | `describe object.arrange.sendToBack` |
| `object.arrange.sendToCurrentLayer` | Send to Current Layer | `describe object.arrange.sendToCurrentLayer` |
| `object.group` | Group | `describe object.group` |
| `object.ungroup` | Ungroup | `describe object.ungroup` |
| `object.setProps` | Object Properties | `describe object.setProps` |
| `object.align` | Align | `describe object.align` |
| `object.distribute` | Distribute | `describe object.distribute` |
| `object.distributeSpacing` | Distribute Spacing | `describe object.distributeSpacing` |
| `object.setBounds` | Set Bounds | `describe object.setBounds` |
| `object.expandShape` | Expand Shape | `describe object.expandShape` |
| `object.setLiveShape` | Live Shape Properties | `describe object.setLiveShape` |
| `object.distort` | Free Distort | `describe object.distort` |
| `object.transformEach` | Transform Each… | `describe object.transformEach` |
| `object.resetBoundingBox` | Reset Bounding Box | `describe object.resetBoundingBox` |
| `object.shape.convertToShape` | Convert to Shape | `describe object.shape.convertToShape` |

### `shape` — 10

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `shape.rectangle` | Rectangle | `describe shape.rectangle` |
| `shape.ellipse` | Ellipse | `describe shape.ellipse` |
| `shape.polygon` | Polygon | `describe shape.polygon` |
| `shape.star` | Star | `describe shape.star` |
| `shape.flare` | Flare | `describe shape.flare` |
| `shape.line` | Line Segment | `describe shape.line` |
| `shape.spiral` | Spiral | `describe shape.spiral` |
| `shape.arc` | Arc | `describe shape.arc` |
| `shape.rectangularGrid` | Rectangular Grid | `describe shape.rectangularGrid` |
| `shape.polarGrid` | Polar Grid | `describe shape.polarGrid` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
