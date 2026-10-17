# WordCraft business 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## project-charter：项目启动说明书

输入：目标、范围、负责人和验收方式均已提供。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 设置本段为一级标题 | `para.heading1` | `{}` |
| 3. 写入本节标题 | `text.insert` | `{"text":"项目启动说明"}` |
| 4. 新建正文段落 | `text.newParagraph` | `{}` |
| 5. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 6. 写入经核实的正文 | `text.insert` | `{"text":"目标：完成资料归档。\n范围：本期历史资料；不包含新系统开发。"}` |
| 7. 段后另起一段 | `text.newParagraph` | `{}` |
| 8. 设置本段为一级标题 | `para.heading1` | `{}` |
| 9. 写入本节标题 | `text.insert` | `{"text":"责任与验收"}` |
| 10. 新建正文段落 | `text.newParagraph` | `{}` |
| 11. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 12. 写入经核实的正文 | `text.insert` | `{"text":"负责人：甲。验收：目录与原件逐条对应。"}` |
| 13. 段后另起一段 | `text.newParagraph` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：目标、承诺和责任人须经任务输入确认，示例不构成实际授权。

## decision-register-table：决策记录与候选方案表

输入：提供备选方案、依据、决策人与日期。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用横向页面容纳方案表 | `layout.orientation` | `{"value":"landscape"}` |
| 2. 写入三行制表符分隔数据 | `text.insert` | `{"text":"方案\t优点\t约束\n方案A\t上线快\t手工核验\n方案B\t自动化高\t实施周期长"}` |
| 3. 新文档只有待转换表格数据，选择全部 | `select.all` | `{}` |
| 4. 按制表符转换成可编辑表格 | `table.fromText` | `{"separator":"tab"}` |
| 5. 表格按页面宽度自动调整 | `table.autofit` | `{"mode":"window"}` |
| 6. 将第一行设为重复表头 | `table.repeatHeader` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：仅用于新建方案表。已有文档应先定位所需段落，不能直接全选替换整篇。补充真实决策人与日期，表格不代替审批。

## letter-header-footer：带页眉页脚的业务函

输入：已确认的发文单位、收件人和正文；不自动发送。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 设置适中的页边距 | `layout.margins` | `{"preset":"normal"}` |
| 3. 插入单位页眉 | `insert.header` | `{"text":"示例单位 · 项目办公室"}` |
| 4. 退出页眉回到正文 | `insert.closeHeader` | `{}` |
| 5. 设置本段为一级标题 | `para.heading1` | `{}` |
| 6. 写入本节标题 | `text.insert` | `{"text":"资料补充函"}` |
| 7. 新建正文段落 | `text.newParagraph` | `{}` |
| 8. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 9. 写入经核实的正文 | `text.insert` | `{"text":"收件人：项目联系人。\n请补充缺失的归档目录与版本说明。"}` |
| 10. 段后另起一段 | `text.newParagraph` | `{}` |
| 11. 插入仅供草稿流转的页脚 | `insert.footer` | `{"text":"草稿 · 待审核"}` |
| 12. 退出页脚回到正文 | `insert.closeHeader` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：姓名、单位、落款必须来自真实输入；本技能不发送函件。

