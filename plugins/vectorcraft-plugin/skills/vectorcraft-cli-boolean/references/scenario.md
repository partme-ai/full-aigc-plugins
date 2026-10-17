# 布尔与形状构建操作指南

## 目标与前置

使用 Pathfinder、复合路径与形状构建工具。布尔顺序影响结果；核对选中对象、孔洞和 winding，保留运算前检查点。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands` 返回 JSON 参数目录；`run --in <工程> --cmd <id> --params <JSON> ... --export <新工程.vectorcraft>`，同批次解析对象 ID；convert 按扩展名输出。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `object.compoundPath.make` | Make |
| `object.compoundPath.release` | Release |
| `object.pathfinder.unite` | Unite |
| `object.pathfinder.minusFront` | Minus Front |
| `object.pathfinder.intersect` | Intersect |
| `object.pathfinder.exclude` | Exclude |
| `object.pathfinder.divide` | Divide |
| `object.pathfinder.trim` | Trim |

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

本技能归属 14 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `object` — 12

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `object.compoundPath.make` | Make | `describe object.compoundPath.make` |
| `object.compoundPath.release` | Release | `describe object.compoundPath.release` |
| `object.pathfinder.unite` | Unite | `describe object.pathfinder.unite` |
| `object.pathfinder.minusFront` | Minus Front | `describe object.pathfinder.minusFront` |
| `object.pathfinder.intersect` | Intersect | `describe object.pathfinder.intersect` |
| `object.pathfinder.exclude` | Exclude | `describe object.pathfinder.exclude` |
| `object.pathfinder.divide` | Divide | `describe object.pathfinder.divide` |
| `object.pathfinder.trim` | Trim | `describe object.pathfinder.trim` |
| `object.pathfinder.merge` | Merge | `describe object.pathfinder.merge` |
| `object.pathfinder.crop` | Crop | `describe object.pathfinder.crop` |
| `object.pathfinder.outline` | Outline | `describe object.pathfinder.outline` |
| `object.pathfinder.minusBack` | Minus Back | `describe object.pathfinder.minusBack` |

### `shapeBuilder` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `shapeBuilder.merge` | Shape Builder | `describe shapeBuilder.merge` |
| `shapeBuilder.regions` | Shape Builder Regions | `describe shapeBuilder.regions` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
