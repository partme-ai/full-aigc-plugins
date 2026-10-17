# 对象布局、状态与路径编辑 / Object layout, state and paths

## 输入与目标集合 / Input and target set

输入为目标vectorcraft工程、对象范围、变换或布局规则、输出变体和需保留内容。先document.json或inspect_document记录对象ID、位置、形状类型、填充和图层，明确授权集合；用select.set选中实际ID再执行依赖选择的命令。同色不代表全部对象都可修改；锁定、隐藏和隔离状态会影响选择。保留原工程，另存修订。

Inspect actual object IDs and preserve the original. Selection is the editing target set; appearance similarity does not authorize unrelated edits. Record lock, visibility and isolation state.

## 形状与布局 / Shape and layout

由 **vectorcraft-cli-shapes** 负责。安装：`npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。

| 任务 | 命令 | 使用步骤与核验 |
| --- | --- | --- |
| 镜像、斜切与微移 | `object.reflect`、`object.shear`、`object.nudge` | 明确axis、origin、copy；角度单位为deg。nudge的dx/dy为方向，移动量由键盘增量决定，big乘10；copy产生副本，核对数量和对象身份 |
| 堆叠和图层 | `object.arrange.bringToFront`、`bringForward`、`sendBackward`、`sendToBack`、`sendToCurrentLayer` | 查询带完整object.arrange前缀的ID；记录原堆叠/图层，核对实际顺序。前移一层与置顶不同，当前图层必须先确认 |
| 对齐 | `object.align` | 明确horizontal/vertical，to为selection/artboard/key；bounds为geometric或preview，preview计入描边。关键对象对齐需先核对关键对象状态；对齐到画板不是对齐到当前选中边界 |
| 分布及间距 | `object.distribute`、`object.distributeSpacing` | 对齐边或中心与均匀间距分开；spacing单位pt。按实际对象顺序、外形边界和描边宽度核验，不把对象数不足的无变化结果当作完成布局 |
| 边界与对象属性 | `object.setBounds`、`object.setProps` | reference为九点参考，proportional/strokes/corners影响缩放；setProps指定真实id/ids和授权name/visible/locked/opacity等字段。核对非目标对象与嵌套内容 |
| 实时形状 | `object.setLiveShape`、`object.expandShape`、`object.shape.convertToShape` | 设置圆角/边数前核对类型；expandShape转为普通路径，convertToShape仅识别支持的矩形/椭圆。保留原实时形状版本并核对converted数量 |
| 四角变形 | `object.distort` | corners顺序TL/TR/BR/BL，from为原边界；核对锚点、控制柄、角点和非目标对象。透视变形不能只检查外框 |
| 重置边界框 | `object.resetBoundingBox` | 当前合同说明边界框始终与文档轴对齐，返回changed:0。该无操作行为不能作为图形改变的证据 |

## 选择、隐藏、锁定与隔离 / Selection state

由 **vectorcraft-cli-selection** 负责。安装：`npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。

`object.lock`、`object.unlockAll`、`object.hide`、`object.showAll`操作对象可编辑/显示状态；`.above`、`.otherLayers`后缀涉及更大范围，先检查当前图层及堆叠。unlockAll/showAll并非只针对当前选中对象，执行前需确认任务范围。`object.isolate`、`object.exitIsolation`改变隔离范围；进入后核对当前目标和返回路径，结束后恢复必要的工作状态。隐去或锁定对象不等于从交付工程删除；检查导出可见性及非目标状态保留。

## 路径生成与整理 / Path operations

由 **vectorcraft-cli-paths** 负责。安装：`npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。

| 任务 | 命令 | 步骤与核验 |
| --- | --- | --- |
| 描边轮廓化与偏移 | `object.path.outlineStroke`、`object.path.offsetPath` | 记录原描边、填充与路径；查询offset参数、连接及限值。轮廓化会改变可编辑结构，另存并核对视觉尺寸和路径数量 |
| 简化与加点 | `object.path.simplify`、`object.path.addAnchorPoints` | 明确误差/选项，比较曲线轮廓和点数。点数减少不等于形状准确，增加锚点不等于图形已变形 |
| 分割 | `object.path.divideObjectsBelow`、`object.path.splitIntoGrid` | 先确认被切对象、上下顺序、行列及间距；核对分割产物ID和数量、填充与非目标对象 |
| 清理 | `object.path.cleanUp` | 查询实际清理选项；记录孤立点、空路径等对象，核对删除范围。另存后核对原对象与无关路径保留 |

## 文档模式 / Document mode

`object.convertDocumentColorMode`归 **vectorcraft-cli-project**，是file.documentColorMode兼容别名。明确mode、convert和intent，核对实际文档模式、对象颜色与输出；设置模式和转换数值不同，模式成功不代表印刷颜色验收。安装：`npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。

## 执行、修订与交付 / Execution and delivery

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe object.align
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe object.path.offsetPath
python3 -I -B "$HARNESS_DIR/scripts/commands.py" check /absolute/object-plan.json
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run /absolute/object-plan.json --output /absolute/new-object-result
```

按本技能command-usage.md合同在同一会话连接返回值、重新选择对象、保存vectorcraft并导出适用SVG/PNG。重开核对目标几何、样式、堆叠和非目标对象；公开参数、归属和预检不等于36条新增归属命令均已运行验收。依赖GUI工作状态的任务按bridge合同执行，不能用headless成功替代GUI验收。

Save editable native projects and reopen them. Verify target geometry and unaffected objects. The guide adds task routes for36 commands, not complete runtime acceptance of those commands.

## 已执行布局实例 / Executed layout example

`examples/object-layout-create.json` 无需外部素材，建立96×64画板和三个无描边矩形；保存original.vectorcraft，再仅选择前两个对象，按geometric边界顶对齐并设置4pt水平间距，保存project.vectorcraft和PNG。对象ID通过创建返回值引用；第三个绿色对象不参与选择。`examples/object-layout-reopen.json` 接收 `--input project=/absolute/project.vectorcraft`，重开并导出；同例可核对original.vectorcraft。均使用本技能commands.py run和新输出目录。

已核验两个对象顶边y=8、水平间距4pt，未选对象不变，原工程重开保持原布局，修改工程重开图形与导出像素一致。路径变换、隔离/锁定、色彩模式及全部36条命令仍需独立验收。

This self-contained fixture verifies actual geometric alignment and spacing, unaffected object preservation and editable native reopening. Adapt object selection and bounds for real artwork.
