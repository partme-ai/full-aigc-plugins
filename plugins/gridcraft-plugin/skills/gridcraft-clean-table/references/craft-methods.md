# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取原始值与公式 | `sheet.read` | `{"range":"A1:D100","formulas":true}` |
| 2. 确认空白输出区域；非空时换新区域而不是覆盖 | `sheet.read` | `{"range":"F1:I100","formulas":true}` |
| 3. 先把目标主键列设为文本，保留001与1的区别 | `home.numberFormat` | `{"range":"F1:F100","format":"@"}` |
| 4. 连同表头拆列到已确认的空白区域 | `data.textToColumns` | `{"range":"A1:A100","delimiters":[","],"destination":"F1"}` |
| 5. 只删除整行完全相同的记录，主键冲突不丢弃 | `data.removeDuplicates` | `{"range":"F1:I100","columns":["F","G","H","I"],"header":true}` |
| 6. 复核保留的文本主键、冲突记录及数量 | `sheet.read` | `{"range":"F1:I100","formulas":false,"formatted":false}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute_command`，参数 `{"command": "sheet.read", "params": {"range": "A1:D100", "formulas": true}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

gridcraft-cli run --in input.xlsx --cmd 'cell.set={"cell":"B2","input":"=A2*2"}' --out output.xlsx；再用 cat/info 新进程读取。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

抽查行数、空值、主键和前导零，重复合并规则有业务依据。

边界：先检查目标列为空；不同记录不能仅因某一列相同就删除。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

本轮实际边界：先读取并确认输出区域为空。原始CSV单列本例包含表头，分隔符/列数/范围按实际输入替换；先设文本格式再拆分，零已经丢失后不能靠设置格式恢复。此默认流程只去除整行一致的重复，主键相同但字段不同的记录必须保留并单列冲突，不按任意首行或末行决策。
