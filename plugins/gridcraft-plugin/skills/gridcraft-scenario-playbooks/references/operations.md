# GridCraft operations 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## inventory-reorder：库存低于安全线的补货清单

输入：每个SKU一行，现存与安全库存为同一计量单位。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 将真实业务记录按列结构写入；示例为可计算的测试输入 | `range.setValues` | `{"range":"A1","values":[["SKU","现存","安全线","补货量"],["A",8,20,"=MAX(0,C2-B2)"],["B",25,20,"=MAX(0,C3-B3)"]]}` |
| 2. 高亮正补货量，零补货保持中性 | `home.conditionalFormat` | `{"range":"D2:D3","rule":{"type":"cellIs","operator":"greaterThan","value":0,"preset":"yellowFill"}}` |
| 3. 冻结表头便于核对SKU | `view.freezeTopRow` | `{}` |
| 4. 检查公式与原始数据位置 | `sheet.read` | `{"range":"A1:D3","formulas":true}` |
| 5. 读取未格式化计算值，按检查项核对结果及错误值 | `sheet.read` | `{"range":"A1:D3","formulas":false,"formatted":false}` |

检查：D2=12，D3=0；没有负补货量；SKU未排序错位。

边界：不包含在途库存、最小起订量与销售预测；这些约束需提供数据后扩展公式。

## expense-threshold-review：费用报销超限复核

输入：使用经批准的类别限额；原始凭据关联在真实输入中保留。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 将真实业务记录按列结构写入；示例为可计算的测试输入 | `range.setValues` | `{"range":"A1","values":[["单号","金额","限额","超限额"],["R01",120,100,"=MAX(0,B2-C2)"],["R02",60,100,"=MAX(0,B3-C3)"]]}` |
| 2. 将超限金额标红作为待复核提示 | `home.conditionalFormat` | `{"range":"D2:D3","rule":{"type":"cellIs","operator":"greaterThan","value":0,"preset":"lightRedFill"}}` |
| 3. 检查公式与原始数据位置 | `sheet.read` | `{"range":"A1:D3","formulas":true}` |
| 4. 读取未格式化计算值，按检查项核对结果及错误值 | `sheet.read` | `{"range":"A1:D3","formulas":false,"formatted":false}` |

检查：D2=20，D3=0；规则只标记未自动拒绝报销；记录与凭据可追溯。

边界：超限提示不代表审批结论；不得自行改变报销状态。

## delivery-acceptance-ratio：交付验收比例与缺失项

输入：每行交付件的应验数量、已验数量非负且不超过应验。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 将真实业务记录按列结构写入；示例为可计算的测试输入 | `range.setValues` | `{"range":"A1","values":[["交付件","应验","已验","缺失","完成率"],["文档",10,8,"=MAX(0,B2-C2)","=IF(B2=0,0,C2/B2)"],["图片",5,5,"=MAX(0,B3-C3)","=IF(B3=0,0,C3/B3)"]]}` |
| 2. 以百分比显示完成率 | `home.numberFormat` | `{"range":"E2:E3","format":"0%"}` |
| 3. 标记未完成项 | `home.conditionalFormat` | `{"range":"D2:D3","rule":{"type":"cellIs","operator":"greaterThan","value":0,"preset":"yellowFill"}}` |
| 4. 检查公式与原始数据位置 | `sheet.read` | `{"range":"A1:E3","formulas":true}` |
| 5. 读取未格式化计算值，按检查项核对结果及错误值 | `sheet.read` | `{"range":"A1:E3","formulas":false,"formatted":false}` |

检查：D2=2，E2=0.8，E3=1；数量对应同一个交付包；超额验收不隐藏成100%。

边界：这些公式不检查已验超过应验的异常；真实输入需先校验数量。

## project-input-table：项目任务表结构化与冻结表头

输入：任务、负责人、状态由输入提供；每任务一行。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 将真实业务记录按列结构写入；示例为可计算的测试输入 | `range.setValues` | `{"range":"A1","values":[["任务","负责人","状态"],["资料收集","甲","完成"],["内容复核","乙","处理中"]]}` |
| 2. 把数据矩形转换成有表头的命名表 | `insert.table` | `{"range":"A1:C3","header":true,"name":"ProjectTasks","style":"TableStyleMedium2"}` |
| 3. 冻结标题行 | `view.freezeTopRow` | `{}` |
| 4. 设置文本列宽，便于编辑 | `home.columnWidth` | `{"cols":"A:C","chars":20}` |
| 5. 检查公式与原始数据位置 | `sheet.read` | `{"range":"A1:C3","formulas":true}` |
| 6. 读取未格式化计算值，按检查项核对结果及错误值 | `sheet.read` | `{"range":"A1:C3","formulas":false,"formatted":false}` |

检查：表名ProjectTasks及三列标题保存；两条任务未丢失；列宽与表头可读。

边界：表格结构化不自动完成任务或发送提醒；状态仍以业务事实为准。

