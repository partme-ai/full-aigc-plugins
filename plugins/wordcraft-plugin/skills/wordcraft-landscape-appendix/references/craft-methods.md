# 纵向正文与横向矩阵附录的方法和参数

## 输入与任务边界

真实矩阵字段及数据已确认，单元格不能含制表或换行。仅新建文档；既有文档需先读分节和页眉页脚，不能整篇改方向。

正文A4纵向；通过nextPage分节后仅附录横向，建立原生四列表格并重复表头，核对两节方向、准确两行数据及PDF两页尺寸。

## 具体步骤

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 确定新文档A4页面 | `layout.size` | `{"name":"A4"}` |
| 2. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 3. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"正文摘要"}` |
| 4. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 5. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 6. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"正文保留纵向，附录单独横向。"}` |
| 7. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 8. 新起一页并创建真正的分节，不能用layout.section对话框代替 | `layout.break` | `{"kind":"nextPage"}` |
| 9. 只将新附录节改为横向 | `layout.orientation` | `{"value":"landscape"}` |
| 10. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 11. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"附录：对照矩阵"}` |
| 12. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 13. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 14. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"方案\t适用范围\t限制\t负责人"}` |
| 15. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 16. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 17. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"方案甲\t示例范围\t待核实\t待确认"}` |
| 18. 移动到当前文档末尾 | `caret.docEnd` | `{}` |
| 19. 向上扩选刚插入的两行表格原文，不触及正文标题 | `caret.paraUp` | `{"extend":true}` |
| 20. 向上扩选刚插入的两行表格原文，不触及正文标题 | `caret.paraUp` | `{"extend":true}` |
| 21. 将精确选中的制表文本转换为原生表格 | `table.fromText` | `{"separator":"tab"}` |
| 22. 让四列适应当前横向节宽 | `table.autofit` | `{"mode":"window"}` |
| 23. 设置首行重复表头 | `table.repeatHeader` | `{}` |
| 24. 核对真实内容和对象结构 | `document.inspect` | `{"text":true}` |

## CLI与宿主MCP

CLI先用`wordcraft-cli commands --json`核对当前版本方法和参数。逐条以argv添加`--cmd`，同一个`wordcraft-cli run --cmd <id=JSON> ... --save 新输出.docx`进程执行全部步骤。已有文件操作需显式`--file 输入.docx`，本技能默认新建，不自动覆盖。`craft-steps.json`是编排手册，不是CLI脚本文件；用每步command和params构造参数，不把purpose等字段传给引擎。

宿主内先调用该插件的open_browser_editor，使用实际editorUrl打开内置浏览器，等待editor_status.attached。读取本实例实际工具schema，使用`execute`和`{"command":"具体方法","params":{实际参数}}`，按相同顺序执行。不得另外启动headless CLI声称画面会同步；若同会话命令目录缺少方法，明确说明并询问用户是否改用保存后重开，不能假装执行。

完成后使用save_document等当前实际工具保存新文件。保存路径和参数以本会话schema为准，不能猜测固定ID。光标位置和选区是状态，任何插入前先核对，失败后不要跳过继续。

## 结果检查

独立CLI另起进程`wordcraft-cli text 输出.docx`核对文本，再`wordcraft-cli convert 输出.docx 审阅.pdf`及`wordcraft-cli render 输出.docx 首页面.png --page 1 --scale 1`。长文档逐页渲染。DOCX域、书签、图片关系、分节和原生表格必须仍在；PDF为派生交付，不能代替可编辑DOCX。重排、增删章节后重新更新域和目录再检查。

技术样例通过不代表真实文案正确、全部页码准确、目标宿主同步或真实截图可读。发现能力缺口先说明，不能用手写编号、扁平截图或整篇横向冒充本场景完成。来源与许可见[工作流来源](workflow-sources.json)，实测参数见[命令观察](craft-command-evidence.json)，具体配方见[步骤](craft-steps.json)。

正文结束后用`layout.break {"kind":"nextPage"}`建立新节，再设置landscape。`layout.section {}`仅打开节设置，不会创建分节。示例最后一行不加text.newParagraph，避免table.fromText多出空白第三行；任何真实行数变化都必须重算扩选范围。
