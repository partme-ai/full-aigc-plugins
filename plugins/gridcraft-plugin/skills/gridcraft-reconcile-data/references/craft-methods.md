# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取本方主键与金额 | `sheet.read` | `{"range":"A1:D100","formulas":true}` |
| 2. 实际读取对方工作表字段和主键范围，不凭名称假设结构 | `sheet.read` | `{"sheet":"Sheet2","range":"A1:B100","formulas":true}` |
| 3. 确认对方空白辅助列；非空时更换列并同步公式范围 | `sheet.read` | `{"sheet":"Sheet2","range":"D1:E100","formulas":true}` |
| 4. 切换到对方表建立工作副本辅助索引 | `sheet.activate` | `{"sheet":"Sheet2"}` |
| 5. 在空白列写辅助表头，保留原A:B | `range.setValues` | `{"range":"D1","values":[["匹配键","对方金额"]]}` |
| 6. 为键加非数字前缀，避免COUNTIF把001与1合并 | `cell.set` | `{"cell":"D2","input":"=IF(A2=\"\",\"\",\"KEY:\"&A2)"}` |
| 7. 保留有效金额并标识缺失，不把空金额变成0 | `cell.set` | `{"cell":"E2","input":"=IF(A2=\"\",\"\",IF(ISNUMBER(B2),B2,\"待确认对方金额\"))"}` |
| 8. 按实际末行填充辅助索引 | `edit.fillDown` | `{"range":"D2:E100"}` |
| 9. 返回本方表写匹配结果 | `sheet.activate` | `{"sheet":"Sheet1"}` |
| 10. 使用同一前缀计数并只提取唯一匹配 | `cell.set` | `{"cell":"E2","input":"=IF(A2=\"\",IF(B2=\"\",\"\",\"缺少主键\"),IF(COUNTIF(Sheet2!$D$2:$D$100,\"KEY:\"&A2)=0,\"未匹配\",IF(COUNTIF(Sheet2!$D$2:$D$100,\"KEY:\"&A2)=1,VLOOKUP(\"KEY:\"&A2,Sheet2!$D$2:$E$100,2,FALSE),\"重复键\")))"}` |
| 11. 仅对双方有效数字计算金额差 | `cell.set` | `{"cell":"F2","input":"=IF(AND(ISNUMBER(B2),ISNUMBER(E2)),B2-E2,\"\")"}` |
| 12. 按实际末行填充，固定对方索引范围 | `edit.fillDown` | `{"range":"E2:F100"}` |
| 13. 核对全部状态和差额 | `sheet.read` | `{"range":"A2:F10"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute_command`，参数 `{"command": "sheet.read", "params": {"range": "A1:D100", "formulas": true}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

gridcraft-cli run --in input.xlsx --cmd 'cell.set={"cell":"B2","input":"=A2*2"}' --out output.xlsx；再用 cat/info 新进程读取。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

分别列出缺失、多对一和金额差异，不通过删除未匹配行让总数相等。

边界：工作表名、键列和重复键必须先查；VLOOKUP只取首条，不适合未处理的多对多。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

本轮实际边界：工作表名、键列和重复键必须先查；VLOOKUP只取首条，不适合未处理的多对多。 当前示例先COUNTIF分流重复键，不使用IFERROR把重复键隐藏成首条金额。示例100替换为真实范围，双方原始键/金额及所有未匹配行保留。

数字文本键补充：工作表名、键列和重复键必须先查；VLOOKUP只取首条，不适合未处理的多对多。 当前示例先COUNTIF分流重复键，不使用IFERROR把重复键隐藏成首条金额。示例100替换为真实范围，双方原始键/金额及所有未匹配行保留。 原生COUNTIF对纯数字文本条件会合并001/1，示例改为KEY:前缀索引；须先确认Sheet2的D:E以及Sheet1的E:F为空并按实际表名/列/末行替换。前缀不恢复原来已经丢失的零；原始主键须先按文本读取核对。本例验证字母/数字业务键，不推断大小写敏感或通配符键规则。
