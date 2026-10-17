# WordCraft editing 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## term-normalization-draft：术语统一的编辑副本

输入：原文与经批准的术语映射；替换前先审查上下文。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 使用A4页面规格 | `layout.size` | `{"name":"A4"}` |
| 2. 设置本段为一级标题 | `para.heading1` | `{}` |
| 3. 写入本节标题 | `text.insert` | `{"text":"术语统一稿"}` |
| 4. 新建正文段落 | `text.newParagraph` | `{}` |
| 5. 恢复正文样式，避免正文进入目录 | `para.normal` | `{}` |
| 6. 写入经核实的正文 | `text.insert` | `{"text":"旧称：资料包。请将资料包提交至资料包目录。"}` |
| 7. 段后另起一段 | `text.newParagraph` | `{}` |
| 8. 按整词匹配替换术语，保留原文副本 | `edit.replaceAll` | `{"text":"资料包","matchCase":false,"wholeWord":false,"with":"档案包"}` |

检查：正文包含输入事实；标题样式与正文分离；保存DOCX后重开并导出PDF检查分页。

边界：真实任务先保留原文件；不对机构名称、引用或专有名称做未授权全局替换。

