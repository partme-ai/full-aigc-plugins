# WordCraft procedure 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## sop-numbered-steps：可执行SOP与停止条件

输入：已有操作顺序、必要输入与停止条件。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 设置本段为一级标题 | `para.heading1` | `{}` |
| 3. 写入本节标题 | `text.insert` | `{"text":"资料归档SOP"}` |
| 4. 新建正文段落 | `text.newParagraph` | `{}` |
| 5. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 6. 开启当前段落的有序步骤列表 | `para.numbering` | `{"kind":"numbered"}` |
| 7. 写入经核实的正文 | `text.insert` | `{"text":"核对原件编号"}` |
| 8. 段后另起一段 | `text.newParagraph` | `{}` |
| 9. 写入经核实的正文 | `text.insert` | `{"text":"登记目录与存放位置"}` |
| 10. 段后另起一段 | `text.newParagraph` | `{}` |
| 11. 写入经核实的正文 | `text.insert` | `{"text":"复核后归档"}` |
| 12. 段后另起一段 | `text.newParagraph` | `{}` |
| 13. 退出列表，后续内容使用正文 | `para.numbering` | `{"off":true}` |
| 14. 写入经核实的正文 | `text.insert` | `{"text":"停止条件：编号冲突或原件缺失时，暂停归档并报告负责人。"}` |
| 15. 段后另起一段 | `text.newParagraph` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：不得把这些示例步骤用于无关高风险设备操作；编号连续性需看实际DOCX与PDF。

