# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 查看公式原文 | `sheet.read` | `{"range":"A1:H100","formulas":true}` |
| 2. 列出计算错误 | `formulas.errorChecking` | `{}` |
| 3. 追查关键结果的引用 | `formulas.tracePrecedents` | `{"cell":"H2"}` |
| 4. 分步求值验证 | `formulas.evaluateFormula` | `{"cell":"H2"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute_command`，参数 `{"command": "sheet.read", "params": {"range": "A1:H100", "formulas": true}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

gridcraft-cli run --in input.xlsx --cmd 'cell.set={"cell":"B2","input":"=A2*2"}' --out output.xlsx；再用 cat/info 新进程读取。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

检查范围遗漏、相对绝对引用与手工常量，并记录修正前后数值。

边界：不以无错误码证明公式业务含义正确；跨表引用要与原始数据核对。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
