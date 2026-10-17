# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 保留可重算的报价模型

参考：[skillhub:excel-xlsx](https://api.skillhub.cn/api/v1/download?slug=excel-xlsx)；[anthropics/skills/xlsx](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/xlsx/SKILL.md)。

把数量、单价、折扣和税率作为输入，计算列保持公式；核对税率单位和舍入口径。先测正常值，再测零数量与折扣边界，保存后读取公式和实际数值。

原配方：`invoice-line-tax`。输入与边界：新建报价表；数量、单价、折扣与税率由任务提供，不内置现实税制。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `range.setValues` | `{"range":"A1","values":[["项目","数量","单价","折扣","未税金额","税率","税额","含税金额"],["服务A",2,100,0.1,"=B2*C2*(1-D2)",0.06,"=E2*F2","=E2+G2"],["服务B",1,50,0,"=B3*C3*(1-D3)",0.06,"=E3*F3","=E3+G3"],["合计",null,null,null,"=SUM(E2:E3)",null,"=SUM(G2:G3)","=SUM(H2:H3)"]]}` |
| 2 | `home.numberFormat` | `{"range":"E2:H4","format":"0.00"}` |
| 3 | `sheet.read` | `{"range":"A1:H4","formulas":true}` |
| 4 | `sheet.read` | `{"range":"A1:H4","formulas":false,"formatted":false}` |

检查：公式仍存在且结果符合独立算例，不能只比较显示字符串。

能力边界：不引入openpyxl或LibreOffice执行链；不把CSV当成有格式和公式的完整工作簿。

原配方结果检查：["E4未税230，G4税额13.8，H4含税243.8", "数量与单价仍为数值", "税率与币种在交付中明确"]

原配方限制：示例不是现实税务规则；舍入方式需按具体业务规定补充。

## 标记重复而不丢失记录

参考：[skillhub:excel-xlsx](https://api.skillhub.cn/api/v1/download?slug=excel-xlsx)。

先明确订单键是否含店铺、日期或版本；保留原行，用辅助列标记重复并审阅。真正删除重复项需要确认业务保留规则，排序须整行一起移动。

原配方：`duplicate-order-review`。输入与边界：重复键只表示需要复核；同一订单允许多行明细的场景应先定义复合键。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `range.setValues` | `{"range":"A1","values":[["订单号","金额","键计数"],["O01",100,"=COUNTIF($A$2:$A$4,A2)"],["O02",70,"=COUNTIF($A$2:$A$4,A3)"],["O01",100,"=COUNTIF($A$2:$A$4,A4)"]]}` |
| 2 | `home.conditionalFormat` | `{"range":"A2:A4","rule":{"type":"duplicate","preset":"yellowFill"}}` |
| 3 | `sheet.read` | `{"range":"A1:C4","formulas":true}` |
| 4 | `sheet.read` | `{"range":"A1:C4","formulas":false,"formatted":false}` |

检查：重复标志对应实际键，原始记录和关联列保持。

能力边界：长编号按文本保真；不能用数值显示相同来断定原始订单号相同。

原配方结果检查：["C2=2，C3=1，C4=2", "原始三行仍保留", "先核查真实业务是否一单多行"]

原配方限制：不能仅因键重复就删除；需要去重时另存副本并明确保留规则。

## 增长率的零基期边界

参考：[anthropics/skills/xlsx](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/xlsx/SKILL.md)；[skillhub:excel-xlsx](https://api.skillhub.cn/api/v1/download?slug=excel-xlsx)。

明确比较基期和百分比显示，零基期用约定的空值或说明处理，不能产生除零错误。保存后分别读公式、未格式化数值和显示格式。

原配方：`month-growth-guard`。输入与边界：月份已按时间顺序排列；0基期采用明确的示例规则。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `range.setValues` | `{"range":"A1","values":[["月份","金额","环比"],["2026-01",0,null],["2026-02",120,"=IF(B2=0,0,B3/B2-1)"],["2026-03",150,"=IF(B3=0,0,B4/B3-1)"]]}` |
| 2 | `home.numberFormat` | `{"range":"C3:C4","format":"0.0%"}` |
| 3 | `sheet.read` | `{"range":"A1:C4","formulas":true}` |
| 4 | `sheet.read` | `{"range":"A1:C4","formulas":false,"formatted":false}` |

检查：正常月份与零基期各有算例，缺失值与零值不混为一谈。

能力边界：这里沿用示例的业务口径，真实报表先确定零基期政策；不假称所有Excel函数兼容。

原配方结果检查：["C3=0，C4=0.25", "第一期无伪造增长率", "月份顺序没有按金额重排"]

原配方限制：零基期的0不是自然增长率；真实交付须标注为不可比或按业务定义处理。

## 版本与执行

执行包装沿用本技能主文件。分别读取公式、未格式化值与显示格式；编号和日期类型先确认，公式错误与业务零值分开检查。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
