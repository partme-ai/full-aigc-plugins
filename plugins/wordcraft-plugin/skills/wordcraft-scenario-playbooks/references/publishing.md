# WordCraft publishing 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## release-bullet-notes：面向用户的版本说明

输入：版本号、上线日期和已验证变更清单。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 设置本段为一级标题 | `para.heading1` | `{}` |
| 3. 写入本节标题 | `text.insert` | `{"text":"版本说明 1.2"}` |
| 4. 新建正文段落 | `text.newParagraph` | `{}` |
| 5. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 6. 写入经核实的正文 | `text.insert` | `{"text":"适用范围：本次资料管理版本。"}` |
| 7. 段后另起一段 | `text.newParagraph` | `{}` |
| 8. 设置本段为一级标题 | `para.heading1` | `{}` |
| 9. 写入本节标题 | `text.insert` | `{"text":"新增与修复"}` |
| 10. 新建正文段落 | `text.newParagraph` | `{}` |
| 11. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 12. 启用项目符号列表 | `para.bullets` | `{"kind":"bullet"}` |
| 13. 写入经核实的正文 | `text.insert` | `{"text":"新增：按编号查询资料。"}` |
| 14. 段后另起一段 | `text.newParagraph` | `{}` |
| 15. 写入经核实的正文 | `text.insert` | `{"text":"修复：重复编号提示不明确。"}` |
| 16. 段后另起一段 | `text.newParagraph` | `{}` |
| 17. 退出项目列表 | `para.bullets` | `{"off":true}` |
| 18. 设置本段为一级标题 | `para.heading1` | `{}` |
| 19. 写入本节标题 | `text.insert` | `{"text":"已知限制"}` |
| 20. 新建正文段落 | `text.newParagraph` | `{}` |
| 21. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 22. 写入经核实的正文 | `text.insert` | `{"text":"历史导入资料仍需人工复核。"}` |
| 23. 段后另起一段 | `text.newParagraph` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：不能把未上线或未验证功能写入已发布项。

## two-column-brief：双栏内部简报

输入：简短已确认内容，适合双栏阅读；无宽表或复杂图片。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 整篇使用双栏并设置栏间距 | `layout.columns` | `{"count":2,"space":18,"separator":true,"apply":"document"}` |
| 3. 设置本段为一级标题 | `para.heading1` | `{}` |
| 4. 写入本节标题 | `text.insert` | `{"text":"本周简报"}` |
| 5. 新建正文段落 | `text.newParagraph` | `{}` |
| 6. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 7. 写入经核实的正文 | `text.insert` | `{"text":"进展：资料目录完成初步整理。\n风险：部分原件仍待补齐。\n下一步：完成缺件核验。"}` |
| 8. 段后另起一段 | `text.newParagraph` | `{}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：双栏结构保存不代表分页美观；真实内容较短时可能只占第一栏，需实际PDF检查。

