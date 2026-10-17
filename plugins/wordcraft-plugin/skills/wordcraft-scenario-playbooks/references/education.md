# WordCraft education 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## training-exercise-handout：培训讲义与独立练习页

输入：提供教学目标、示例内容与练习题，不编造培训结论。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 设置本段为一级标题 | `para.heading1` | `{}` |
| 3. 写入本节标题 | `text.insert` | `{"text":"资料核验培训"}` |
| 4. 新建正文段落 | `text.newParagraph` | `{}` |
| 5. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 6. 写入经核实的正文 | `text.insert` | `{"text":"学习目标：识别目录编号与原件编号不一致的情况。"}` |
| 7. 段后另起一段 | `text.newParagraph` | `{}` |
| 8. 设置本段为一级标题 | `para.heading1` | `{}` |
| 9. 写入本节标题 | `text.insert` | `{"text":"示例与解释"}` |
| 10. 新建正文段落 | `text.newParagraph` | `{}` |
| 11. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 12. 写入经核实的正文 | `text.insert` | `{"text":"示例：目录写A01，原件写A10。先确认是否录入错误。"}` |
| 13. 段后另起一段 | `text.newParagraph` | `{}` |
| 14. 练习单独起页 | `text.pageBreak` | `{}` |
| 15. 设置本段为一级标题 | `para.heading1` | `{}` |
| 16. 写入本节标题 | `text.insert` | `{"text":"练习"}` |
| 17. 新建正文段落 | `text.newParagraph` | `{}` |
| 18. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 19. 写入经核实的正文 | `text.insert` | `{"text":"请核对三份资料的编号，并写明差异与下一步。"}` |
| 20. 段后另起一段 | `text.newParagraph` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：PDF需逐页检查标题不孤悬、练习留白足够；页面断行受字体影响。

