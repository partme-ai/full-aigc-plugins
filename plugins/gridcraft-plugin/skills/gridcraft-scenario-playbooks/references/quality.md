# GridCraft quality 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## duplicate-order-review：订单重复键标记而不删记录

输入：重复键只表示需要复核；同一订单允许多行明细的场景应先定义复合键。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 将真实业务记录按列结构写入；示例为可计算的测试输入 | `range.setValues` | `{"range":"A1","values":[["订单号","金额","键计数"],["O01",100,"=COUNTIF($A$2:$A$4,A2)"],["O02",70,"=COUNTIF($A$2:$A$4,A3)"],["O01",100,"=COUNTIF($A$2:$A$4,A4)"]]}` |
| 2. 仅高亮重复订单键，不调用删除命令 | `home.conditionalFormat` | `{"range":"A2:A4","rule":{"type":"duplicate","preset":"yellowFill"}}` |
| 3. 检查公式与原始数据位置 | `sheet.read` | `{"range":"A1:C4","formulas":true}` |
| 4. 读取未格式化计算值，按检查项核对结果及错误值 | `sheet.read` | `{"range":"A1:C4","formulas":false,"formatted":false}` |

检查：C2=2，C3=1，C4=2；原始三行仍保留；先核查真实业务是否一单多行。

边界：不能仅因键重复就删除；需要去重时另存副本并明确保留规则。

## controlled-status-entry：受控状态下拉录入

输入：状态枚举由实际业务提供，示例为待处理/处理中/完成。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 将真实业务记录按列结构写入；示例为可计算的测试输入 | `range.setValues` | `{"range":"A1","values":[["事项","状态"],["导入资料","待处理"],["核验资料","处理中"]]}` |
| 2. 为新录入区域设置列表验证与错误提示 | `data.validation` | `{"range":"B2:B20","type":"list","formula1":"\"待处理,处理中,完成\"","ignoreBlank":true,"dropdown":true,"errorStyle":"stop","errorTitle":"状态无效","errorMessage":"请从下拉列表选择"}` |
| 3. 检查公式与原始数据位置 | `sheet.read` | `{"range":"A1:B3","formulas":true}` |
| 4. 读取未格式化计算值，按检查项核对结果及错误值 | `sheet.read` | `{"range":"A1:B3","formulas":false,"formatted":false}` |

检查：工作簿保存了B2:B20的验证规则；已有状态属于枚举；宿主中试输入非法状态观察提示。

边界：写入API可能不执行界面输入验证；序列化有规则不证明所有导入路径都拒绝非法值。

