# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 设置预算结构示例 | `range.setValues` | `{"range":"A1","values":[["项目","预算","实际","差额"],["示例项目",100,80,"=IF(ISNUMBER(B2),IF(ISNUMBER(C2),B2-C2,\"待确认实际\"),\"待确认预算\")"]]}` |
| 2. 统一金额格式 | `home.numberFormat` | `{"range":"B2:D100","format":"0.00"}` |
| 3. 核对差额与原数 | `sheet.read` | `{"range":"A1:D2","formulas":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute_command`，参数 `{"command": "range.setValues", "params": {"range": "A1", "values": [["项目", "预算", "实际", "差额"], ["示例项目", 100, 80, "=B2-C2"]]}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

gridcraft-cli run --in input.xlsx --cmd 'cell.set={"cell":"B2","input":"=A2*2"}' --out output.xlsx；再用 cat/info 新进程读取。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

预算-实际的符号定义固定，空预算不当零预算，数值与凭据对应。

边界：示例金额应在真实任务中替换，日期、币种与审批状态另行保留。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

本轮实际边界：示例金额应在真实任务中替换，日期、币种与审批状态另行保留。 空预算或空实际先显示待确认，数值0仍作为有效预算。批量时按实际数据范围填充相对行引用，不能只改显示格式掩盖缺值。
