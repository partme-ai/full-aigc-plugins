# 具体方法与执行

先用CLI `info input.xlsx` 或同会话MCP `inspect_workbook {}` 查询现有工作表。模板只在新建的本任务工作表运行；`$sheet.name`选未占用的唯一名字，替换后才能执行。若会话已有同名表，停止创建并选择另一个名称，不沿用或清空用户原表。创建后回读实际名称。

| 顺序与目的 | 方法 | 参数模板 |
| --- | --- | --- |
| 1. 只在确认无同名工作表后新建本任务工作表 | `home.insertSheet` | `{"name":"$sheet.name"}` |
| 2. 显式激活刚建立的工作表 | `sheet.activate` | `{"sheet":"$sheet.name"}` |
| 3. 分离虚构输入、单位与派生结果 | `range.setValues` | `{"range":"A1","values":[["Fixed payment example","Value"],["Principal",12000],["Nominal annual rate",0.06],["Number of months",12],[""],["Monthly payment"],["Total payments"],["Interest only"]]}` |
| 4. 等额月供；零利率单独处理，缺失和无效不计算 | `cell.set` | `{"cell":"B6","input":"=IF(OR(B2=\"\",B3=\"\",B4=\"\"),\"Missing input\",IF(AND(ISNUMBER(B2),ISNUMBER(B3),ISNUMBER(B4)),IF(OR(B2<=0,B3<0,B4<=0,MOD(B4,1)<>0),\"Invalid input\",IF(B3=0,B2/B4,-PMT(B3/12,B4,B2))),\"Invalid input\"))"}` |
| 5. 保留内部精度求总支付，不先按显示小数截断 | `cell.set` | `{"cell":"B7","input":"=IF(ISNUMBER(B6),B6*B4,\"\")"}` |
| 6. 求不含费用的利息部分 | `cell.set` | `{"cell":"B8","input":"=IF(ISNUMBER(B7),B7-B2,\"\")"}` |
| 7. 写明假设，不当作实际借款报价 | `range.setValues` | `{"range":"A11","values":[["Illustrative only; fixed nominal annual rate, monthly payments, no fees."],["No payment schedule, lender rounding or variable-rate assumptions are included."]]}` |
| 8. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"B2","code":"#,##0.00"}` |
| 9. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"B3","code":"0.00%"}` |
| 10. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"B4","code":"0"}` |
| 11. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"B6:B8","code":"#,##0.00"}` |
| 12. 添加输入范围规则；公式仍独立防护 | `data.validation` | `{"range":"B4","type":"whole","operator":"between","formula1":"1","formula2":"1200","ignoreBlank":true,"errorStyle":"stop","errorTitle":"Check input","errorMessage":"Use values within the documented range."}` |
| 13. 给目标列留足显示宽度 | `home.columnWidth` | `{"cols":"A:A","width":245}` |
| 14. 给目标列留足显示宽度 | `home.columnWidth` | `{"cols":"B:B","width":140}` |
| 15. 突出用户可修改的输入 | `home.fillColor` | `{"range":"B2:B4","color":"#FFF2CC"}` |
| 16. 假设说明换行显示 | `home.wrapText` | `{"range":"A11:B12","on":true}` |
| 17. 给说明留空间 | `home.mergeAcross` | `{"range":"A11:B12"}` |
| 18. 说明行高度 | `home.rowHeight` | `{"rows":"11:12","height":34}` |

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
