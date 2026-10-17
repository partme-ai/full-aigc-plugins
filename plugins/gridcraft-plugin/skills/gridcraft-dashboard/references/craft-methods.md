# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 建立供图表使用的汇总表 | `range.setValues` | `{"range":"F1","values":[["周期","数量"],["上期",21],["本期",42]]}` |
| 2. 插入可编辑趋势图 | `insert.chart` | `{"range":"F1:G3","type":"line","title":"数量趋势","at":"I2"}` |
| 3. 读取图表来源核对口径 | `sheet.read` | `{"range":"F1:G3"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute_command`，参数 `{"command": "range.setValues", "params": {"range": "F1", "values": [["周期", "数量"], ["上期", 21], ["本期", 42]]}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

gridcraft-cli run --in input.xlsx --cmd 'cell.set={"cell":"B2","input":"=A2*2"}' --out output.xlsx；再用 cat/info 新进程读取。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

图表数据源、单位与统计周期清楚，刷新后没有硬编码旧值。

边界：示例汇总必须换成真实数据或公式；看板不能只交付静态截图。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
