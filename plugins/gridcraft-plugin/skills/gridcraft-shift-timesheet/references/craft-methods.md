# 具体方法与执行

先用CLI `info input.xlsx` 或同会话MCP `inspect_workbook {}` 查询现有工作表。模板只在新建的本任务工作表运行；`$sheet.name`选未占用的唯一名字，替换后才能执行。若会话已有同名表，停止创建并选择另一个名称，不沿用或清空用户原表。创建后回读实际名称。

| 顺序与目的 | 方法 | 参数模板 |
| --- | --- | --- |
| 1. 只在确认无同名工作表后新建本任务工作表 | `home.insertSheet` | `{"name":"$sheet.name"}` |
| 2. 显式激活刚建立的工作表 | `sheet.activate` | `{"sheet":"$sheet.name"}` |
| 3. 写入虚构班次输入，不读取员工个人资料 | `range.setValues` | `{"range":"A1","values":[["Shift","Start","End","Break hours","Work hours","Review"],["Night",0.8958333333333334,0.25,0.5],["Day",0.375,0.7291666666666666,0.5],["Missing",null,0.7083333333333334,0],["Invalid",0.375,0.4166666666666667,2]]}` |
| 4. 按日小数处理跨午夜；排除缺失、等时刻和无效休息 | `cell.set` | `{"cell":"E2","input":"=IF(AND(ISNUMBER(B2),ISNUMBER(C2),ISNUMBER(D2)),IF(OR(B2<0,B2>=1,C2<0,C2>=1,D2<0,B2=C2,D2>MOD(C2-B2,1)*24),\"\",MOD(C2-B2,1)*24-D2),\"\")"}` |
| 5. 显示缺失和无效行；不能只看合计 | `cell.set` | `{"cell":"F2","input":"=IF(OR(B2=\"\",C2=\"\",D2=\"\"),\"Missing input\",IF(E2=\"\",\"Review input\",\"OK\"))"}` |
| 6. 按日小数处理跨午夜；排除缺失、等时刻和无效休息 | `cell.set` | `{"cell":"E3","input":"=IF(AND(ISNUMBER(B3),ISNUMBER(C3),ISNUMBER(D3)),IF(OR(B3<0,B3>=1,C3<0,C3>=1,D3<0,B3=C3,D3>MOD(C3-B3,1)*24),\"\",MOD(C3-B3,1)*24-D3),\"\")"}` |
| 7. 显示缺失和无效行；不能只看合计 | `cell.set` | `{"cell":"F3","input":"=IF(OR(B3=\"\",C3=\"\",D3=\"\"),\"Missing input\",IF(E3=\"\",\"Review input\",\"OK\"))"}` |
| 8. 按日小数处理跨午夜；排除缺失、等时刻和无效休息 | `cell.set` | `{"cell":"E4","input":"=IF(AND(ISNUMBER(B4),ISNUMBER(C4),ISNUMBER(D4)),IF(OR(B4<0,B4>=1,C4<0,C4>=1,D4<0,B4=C4,D4>MOD(C4-B4,1)*24),\"\",MOD(C4-B4,1)*24-D4),\"\")"}` |
| 9. 显示缺失和无效行；不能只看合计 | `cell.set` | `{"cell":"F4","input":"=IF(OR(B4=\"\",C4=\"\",D4=\"\"),\"Missing input\",IF(E4=\"\",\"Review input\",\"OK\"))"}` |
| 10. 按日小数处理跨午夜；排除缺失、等时刻和无效休息 | `cell.set` | `{"cell":"E5","input":"=IF(AND(ISNUMBER(B5),ISNUMBER(C5),ISNUMBER(D5)),IF(OR(B5<0,B5>=1,C5<0,C5>=1,D5<0,B5=C5,D5>MOD(C5-B5,1)*24),\"\",MOD(C5-B5,1)*24-D5),\"\")"}` |
| 11. 显示缺失和无效行；不能只看合计 | `cell.set` | `{"cell":"F5","input":"=IF(OR(B5=\"\",C5=\"\",D5=\"\"),\"Missing input\",IF(E5=\"\",\"Review input\",\"OK\"))"}` |
| 12. 合计当前有效工时 | `cell.set` | `{"cell":"E7","input":"=SUM(E2:E5)"}` |
| 13. 提示无效和缺失行未计入 | `cell.set` | `{"cell":"F7","input":"=IF(COUNT(E2:E5)=ROWS(E2:E5),\"Complete\",\"Incomplete rows excluded\")"}` |
| 14. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"B2:C5","code":"hh:mm"}` |
| 15. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"D2:E7","code":"0.00"}` |
| 16. 添加输入范围规则；公式仍独立防护 | `data.validation` | `{"range":"B2:C5","type":"time","operator":"between","formula1":"0","formula2":"0.999999999","ignoreBlank":true,"errorStyle":"stop","errorTitle":"Check input","errorMessage":"Use values within the documented range."}` |
| 17. 添加输入范围规则；公式仍独立防护 | `data.validation` | `{"range":"D2:D5","type":"decimal","operator":"between","formula1":"0","formula2":"24","ignoreBlank":true,"errorStyle":"stop","errorTitle":"Check input","errorMessage":"Use values within the documented range."}` |
| 18. 给目标列留足显示宽度 | `home.columnWidth` | `{"cols":"A:A","width":110}` |
| 19. 给目标列留足显示宽度 | `home.columnWidth` | `{"cols":"B:E","width":90}` |
| 20. 给目标列留足显示宽度 | `home.columnWidth` | `{"cols":"F:F","width":215}` |
| 21. 冻结标题行 | `view.freezeTopRow` | `{}` |

## CLI与MCP

CLI使用参数数组：`gridcraft-cli run --in input.xlsx --cmd 方法ID=JSON … --out output.xlsx`。每个方法ID与JSON组成一个argv，不把用户文本拼成shell命令。结果是逐行JSON；逐项检查结果，不能只看进程退出码。

内嵌编辑器ready后，同一服务用 `execute_command`：

```json
{"command":"sheet.read","params":{"range":"A1:G10","sheet":"实际工作表名","formulas":false,"formatted":false}}
```

先执行创建和激活，再在同一会话逐条填写/格式化；`range.setValues`操作当前表，不虚构额外sheet参数。调用之间选择变化时重新激活真实目标表。原始数值用formatted:false回读，公式用formulas:true回读，两者分别验证。界面保存用实际schema的save_workbook路径，按实际写入回执交付。独立CLI进程不会自动改变打开的Web工作簿。

data.validation配置错误提示和允许范围，但本流程不依赖API自动拦截；公式本身处理缺失、类型及边界。输入涂色不等于加密或防改，真实输入仍由任务核实。

另存XLSX后由新进程/重新打开的同会话检查。修改副本输入后验证结果变化、原公式保留、非目标工作表与原输入摘要不变。不要把旧公式缓存或固定数字输出当成可重算模板。

## 真正的重开与分批填写

若open_workbook回执为alreadyOpen:true，只证明切回已打开的工作簿，不证明磁盘重载。保存后用实际文件的新路径副本重新打开并核对sheets/title，或用独立CLI新进程回读；保留原文件，不覆盖未保存更改。大范围公式可按行分批range.setValues，保持范围偏移与原公式；月历先填写A5锚点，再填其他行，完成后回读42格。
