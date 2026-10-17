# 品牌对象选择与变换 / Brand object selection and transformation

适用于 Logo/图标变体的指定对象修改与品牌色批量更新。先读取画板、图层、对象 ID、锁定/隐藏状态和当前选择；相同颜色不代表同一品牌语义，不能据颜色相同修改无关装饰或其他品牌元素。

Use for targeted logo/icon variants and brand-color revisions. Inspect object IDs, artboards and visibility/lock state. Matching a color does not establish brand ownership.

## 选择与变换合同 / Selection and transform contracts

| 请求 / Request | 命令 / Command | 参数与边界 / Contract |
| --- | --- | --- |
| 精确选择 | `select.set` | `ids` 为当前工程实际对象 ID；查询选择结果再变换 |
| 按填色扩展选择 | `select.same.fillColor` | 依赖当前选择与上下文；扩展后检查全部对象，去除非目标项 |
| 移动 | `object.move` | `dx`、`dy` 为实际坐标增量；明确 `copy`，防止把移动变成重复对象 |
| 旋转 | `object.rotate` | angle 为逆时针度数；确认 origin 和 copy |
| 缩放 | `object.scale` | sx/sy 是百分比；明确 strokes/corners，避免依赖用户偏好改变笔画或圆角 |
| 仿射变换 | `object.transform` | matrix 是 [a,b,c,d,e,f]；核对 ids 或当前选择，以及 strokes/corners/copy |

Scale parameters use percentages, rotation uses counter-clockwise degrees, and affine transforms use six matrix coefficients. Specify stroke/corner behavior when it matters to the requested design.

## 场景操作 / Scenario workflow

1. 保存原生检查点，读取品牌对象的 ID、填色、笔画、几何边界和画板归属。
2. 品牌色替换先建立授权对象集合。相同填色查询只用于找候选，检查候选后以精确 ID 选择；渐变、笔画和文本填色按各自合同处理。
3. 使用 `commands.py describe` 核对选择、变换或外观命令；按 `command-usage.md` 构造计划，check 后 run。同会话核验选择和实际返回对象。
4. 保存新 `.vectorcraft`，重开检查路径、文字、画板及非目标对象。导出 SVG/PNG，任务适用时另导出 PDF；交换格式的视觉正确不替代原生对象可编辑。
5. 返工修改单个变体时，只更新所属对象/画板；核验其他变体和旧交付摘要。复制变体时记录新对象 ID，不继续使用原选择猜测新对象。

Preserve a checkpoint, build the authorized object set and inspect all candidates from same-color selection. Save/reopen the native project and compare unrelated variants. Track new object IDs when making copies.

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe select.same.fillColor
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe select.set
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe object.scale
```

交付原生工程、适用的 SVG/PNG/PDF 和对象修改记录；检查边界、笔画、文字可编辑性、画板范围及导出像素。完整选择与对象命令逐项执行验收仍未完成。

Deliver the native project, applicable exports and object revision records. Verify bounds, strokes, editable text and artboard coverage. Full per-command execution acceptance remains open.

## 已执行代表实例 / Executed representative example

`examples/selection-brand-create.json` 建立三对象测试工程，其中两项同填色。先按填色找到两个候选，再精确选择授权 Logo 修改颜色，保留同色装饰与第三个对象。`examples/selection-brand-reopen.json` 使用 `--input project=/absolute/project.vectorcraft` 重开并导出。两例通过本技能 `commands.py run` 执行，使用新的输出目录。已核验非目标对象结构不变、重开对象保留与导出像素一致；这些例子不代表用户 Logo 规格或全部选择命令验收。

Run the local create/reopen fixtures through the public gateway. The bounded example narrows same-color candidates to the authorized object and verifies preserved unrelated objects and pixels after reopening.
