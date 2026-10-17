# 具体方法与执行

先用CLI `info input.xlsx` 或同会话MCP `inspect_workbook {}` 查询现有工作表。模板只在新建的本任务工作表运行；`$sheet.name`选未占用的唯一名字，替换后才能执行。若会话已有同名表，停止创建并选择另一个名称，不沿用或清空用户原表。创建后回读实际名称。

| 顺序与目的 | 方法 | 参数模板 |
| --- | --- | --- |
| 1. 只在确认无同名工作表后新建本任务工作表 | `home.insertSheet` | `{"name":"$sheet.name"}` |
| 2. 显式激活刚建立的工作表 | `sheet.activate` | `{"sheet":"$sheet.name"}` |
| 3. 明确年份和月份输入 | `range.setValues` | `{"range":"A1","values":[["Year",2028],["Month",2]]}` |
| 4. 使用周一起始的七列，不隐含地区默认值 | `range.setValues` | `{"range":"A4","values":[["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]]}` |
| 5. 建立可重算的六周日期网格 | `range.setValues` | `{"range":"A5","values":[["=IF(AND(ISNUMBER(B1),ISNUMBER(B2)),IF(OR(B1<1901,B1>9999,B2<1,B2>12,MOD(B1,1)<>0,MOD(B2,1)<>0),\"\",DATE(B1,B2,1)-WEEKDAY(DATE(B1,B2,1),2)+1),\"\")","=IF($A$5=\"\",\"\",$A$5+1)","=IF($A$5=\"\",\"\",$A$5+2)","=IF($A$5=\"\",\"\",$A$5+3)","=IF($A$5=\"\",\"\",$A$5+4)","=IF($A$5=\"\",\"\",$A$5+5)","=IF($A$5=\"\",\"\",$A$5+6)"],["=IF($A$5=\"\",\"\",$A$5+7)","=IF($A$5=\"\",\"\",$A$5+8)","=IF($A$5=\"\",\"\",$A$5+9)","=IF($A$5=\"\",\"\",$A$5+10)","=IF($A$5=\"\",\"\",$A$5+11)","=IF($A$5=\"\",\"\",$A$5+12)","=IF($A$5=\"\",\"\",$A$5+13)"],["=IF($A$5=\"\",\"\",$A$5+14)","=IF($A$5=\"\",\"\",$A$5+15)","=IF($A$5=\"\",\"\",$A$5+16)","=IF($A$5=\"\",\"\",$A$5+17)","=IF($A$5=\"\",\"\",$A$5+18)","=IF($A$5=\"\",\"\",$A$5+19)","=IF($A$5=\"\",\"\",$A$5+20)"],["=IF($A$5=\"\",\"\",$A$5+21)","=IF($A$5=\"\",\"\",$A$5+22)","=IF($A$5=\"\",\"\",$A$5+23)","=IF($A$5=\"\",\"\",$A$5+24)","=IF($A$5=\"\",\"\",$A$5+25)","=IF($A$5=\"\",\"\",$A$5+26)","=IF($A$5=\"\",\"\",$A$5+27)"],["=IF($A$5=\"\",\"\",$A$5+28)","=IF($A$5=\"\",\"\",$A$5+29)","=IF($A$5=\"\",\"\",$A$5+30)","=IF($A$5=\"\",\"\",$A$5+31)","=IF($A$5=\"\",\"\",$A$5+32)","=IF($A$5=\"\",\"\",$A$5+33)","=IF($A$5=\"\",\"\",$A$5+34)"],["=IF($A$5=\"\",\"\",$A$5+35)","=IF($A$5=\"\",\"\",$A$5+36)","=IF($A$5=\"\",\"\",$A$5+37)","=IF($A$5=\"\",\"\",$A$5+38)","=IF($A$5=\"\",\"\",$A$5+39)","=IF($A$5=\"\",\"\",$A$5+40)","=IF($A$5=\"\",\"\",$A$5+41)"]]}` |
| 6. 设置显示格式；不改变底层数值和公式 | `home.numberFormat` | `{"range":"A5:G10","code":"mm-dd"}` |
| 7. 添加输入范围规则；公式仍独立防护 | `data.validation` | `{"range":"B1","type":"whole","operator":"between","formula1":"1901","formula2":"9999","ignoreBlank":true,"errorStyle":"stop","errorTitle":"Check input","errorMessage":"Use values within the documented range."}` |
| 8. 添加输入范围规则；公式仍独立防护 | `data.validation` | `{"range":"B2","type":"whole","operator":"between","formula1":"1","formula2":"12","ignoreBlank":true,"errorStyle":"stop","errorTitle":"Check input","errorMessage":"Use values within the documented range."}` |
| 9. 给目标列留足显示宽度 | `home.columnWidth` | `{"cols":"A:G","width":90}` |
| 10. 标题行强调 | `home.fillColor` | `{"range":"A4:G4","color":"#DCE6F1"}` |
| 11. 固定星期六日所在两列 | `home.fillColor` | `{"range":"F5:G10","color":"#E7F0FA"}` |
| 12. 日期行留出记录空间 | `home.rowHeight` | `{"rows":"5:10","height":38}` |
| 13. 标明前后月份显示策略 | `cell.set` | `{"cell":"A12","input":"Monday first; adjacent-month dates are shown as mm-dd. No holidays assumed."}` |
| 14. 说明合并显示 | `home.mergeCells` | `{"range":"A12:G12"}` |
| 15. 说明换行 | `home.wrapText` | `{"range":"A12:G12","on":true}` |

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
