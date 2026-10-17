# 蒙版与路径动画操作指南

## 目标与前置

创建和编辑蒙版路径、羽化及局部遮罩。闭合路径、合成坐标和羽化范围需验证；不要称尚未测试的自动 roto 为可靠主体识别。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `mask.new` | New Mask from Points |
| `mask.addVertex` | Add Mask Vertex |
| `mask.setVertex` | Set Mask Vertex |
| `mask.setClosed` | Closed |
| `mask.selectVertices` | Select Mask Vertices |
| `mask.moveVertices` | Move Mask Vertices |
| `mask.deleteVertices` | Delete Mask Vertices |
| `mask.convertVertex` | Convert Vertex |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。


## 单技能首次使用：创建与局部修改

先使用本技能目录的 `examples/layer-mask.json`。闭合矩形顶点使用图层坐标（此例图层大小 320×180），不是未经转换的合成坐标。默认 Add 蒙版保留左半幅，透明交付看 RGBA PNG 帧；MP4 不保存 alpha。

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" "$SKILL_DIR/examples/layer-mask.json" --output mask-v1
```

保存回执中的 `bindings.product.layer` 与 `bindings.crop.mask`，以及 `files["project.ecproj"]`。局部修订计划使用 `expectedProjectSha256` 和两条 `mask.setVertex` 操作：顶点索引 1 移到 `[240,0]`，索引 2 移到 `[240,180]`；`layer` 用 `{"$ref":"product.layer"}`，`mask` 用 `{"$ref":"crop.mask"}`。通过本技能 workflow.py 的 `--source mask-v1 --output mask-v2` 另存，重开并比较 RGBA 实际边界。移除蒙版用 `mask.remove`，不删除原始图层。

路径与顶点不是主体识别结果。只有当前版本真正执行并渲染通过的操作才可称已验证；自动抠像、羽化动画和任意复杂路径仍按具体任务验收。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 37 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `mask` — 17

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `mask.new` | New Mask from Points | `describe mask.new` |
| `mask.addVertex` | Add Mask Vertex | `describe mask.addVertex` |
| `mask.setVertex` | Set Mask Vertex | `describe mask.setVertex` |
| `mask.setClosed` | Closed | `describe mask.setClosed` |
| `mask.selectVertices` | Select Mask Vertices | `describe mask.selectVertices` |
| `mask.moveVertices` | Move Mask Vertices | `describe mask.moveVertices` |
| `mask.deleteVertices` | Delete Mask Vertices | `describe mask.deleteVertices` |
| `mask.convertVertex` | Convert Vertex | `describe mask.convertVertex` |
| `mask.insertVertex` | Add Vertex | `describe mask.insertVertex` |
| `mask.featherPoint.add` | Add Mask Feather Point | `describe mask.featherPoint.add` |
| `mask.featherPoint.set` | Move Mask Feather Point | `describe mask.featherPoint.set` |
| `mask.featherPoint.remove` | Delete Mask Feather Point | `describe mask.featherPoint.remove` |
| `mask.featherPoint.list` | Mask Feather Points | `describe mask.featherPoint.list` |
| `mask.remove` | Remove Mask | `describe mask.remove` |
| `mask.removeAll` | Remove All Masks | `describe mask.removeAll` |
| `mask.interpolate` | Apply Mask Interpolation | `describe mask.interpolate` |
| `mask.interpolationOptions` | Mask Interpolation Options | `describe mask.interpolationOptions` |

### `path` — 6

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `path.rotoBezier` | RotoBezier | `describe path.rotoBezier` |
| `path.convertToBezier` | Convert To Bezier Path | `describe path.convertToBezier` |
| `path.groupShapes` | Group Shapes | `describe path.groupShapes` |
| `path.ungroupShapes` | Ungroup Shapes | `describe path.ungroupShapes` |
| `path.setFirstVertex` | Set First Vertex | `describe path.setFirstVertex` |
| `path.freeTransform` | Free Transform Points | `describe path.freeTransform` |

### `roto` — 14

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `roto.models` | Roto Brush Models | `describe roto.models` |
| `roto.model.select` | Use Roto Brush Model | `describe roto.model.select` |
| `roto.model.install` | Install Roto Brush Model | `describe roto.model.install` |
| `roto.model.download` | Download Roto Brush Model | `describe roto.model.download` |
| `roto.model.remove` | Remove Roto Brush Model | `describe roto.model.remove` |
| `roto.stroke` | Roto Brush Stroke | `describe roto.stroke` |
| `roto.propagate` | Propagate Roto Brush | `describe roto.propagate` |
| `roto.span` | Set Segmentation Span | `describe roto.span` |
| `roto.freeze` | Freeze | `describe roto.freeze` |
| `roto.unfreeze` | Unfreeze | `describe roto.unfreeze` |
| `roto.clearStrokes` | Remove Roto Brush Strokes | `describe roto.clearStrokes` |
| `roto.cancel` | Stop Roto Brush | `describe roto.cancel` |
| `roto.options` | Roto Brush Options | `describe roto.options` |
| `roto.status` | Roto Brush Status | `describe roto.status` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
