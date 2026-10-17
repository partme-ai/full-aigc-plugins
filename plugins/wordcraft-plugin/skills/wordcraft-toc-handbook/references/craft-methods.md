# 可更新目录的操作手册的方法和参数

## 输入与任务边界

根据真实内容创建一二级标题；标题层级来自文档逻辑，不能仅凭字体大小推断。新建文档样例，不在既有目录上重复插入。

先创建正文标题及段落，再在文首插入两级自动目录；修改后更新目录，核对真实TOC域、四个标题和有效书签跳转。

## 具体步骤

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 2. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"安装准备"}` |
| 3. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 4. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 5. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"核对系统与素材。"}` |
| 6. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 7. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 8. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"安装步骤"}` |
| 9. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 10. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 11. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"使用已批准的安装包。"}` |
| 12. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 13. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 14. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"使用与排错"}` |
| 15. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 16. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 17. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"排错路径"}` |
| 18. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 19. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 20. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"记录实际错误与修复。"}` |
| 21. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 22. 将目录插入点移到正文之前 | `caret.docStart` | `{}` |
| 23. 创建基于一二级标题的可更新目录 | `references.toc` | `{"levels":2,"title":"目录","pageNumbers":true,"hyperlinks":true}` |
| 24. 更新目录文字、页码和书签 | `references.updateToc` | `{}` |
| 25. 核对真实内容和对象结构 | `document.inspect` | `{"text":true}` |

## CLI与宿主MCP

CLI先用`wordcraft-cli commands --json`核对当前版本方法和参数。逐条以argv添加`--cmd`，同一个`wordcraft-cli run --cmd <id=JSON> ... --save 新输出.docx`进程执行全部步骤。已有文件操作需显式`--file 输入.docx`，本技能默认新建，不自动覆盖。`craft-steps.json`是编排手册，不是CLI脚本文件；用每步command和params构造参数，不把purpose等字段传给引擎。

宿主内先调用该插件的open_browser_editor，使用实际editorUrl打开内置浏览器，等待editor_status.attached。读取本实例实际工具schema，使用`execute`和`{"command":"具体方法","params":{实际参数}}`，按相同顺序执行。不得另外启动headless CLI声称画面会同步；若同会话命令目录缺少方法，明确说明并询问用户是否改用保存后重开，不能假装执行。

完成后使用save_document等当前实际工具保存新文件。保存路径和参数以本会话schema为准，不能猜测固定ID。光标位置和选区是状态，任何插入前先核对，失败后不要跳过继续。

## 结果检查

独立CLI另起进程`wordcraft-cli text 输出.docx`核对文本，再`wordcraft-cli convert 输出.docx 审阅.pdf`及`wordcraft-cli render 输出.docx 首页面.png --page 1 --scale 1`。长文档逐页渲染。DOCX域、书签、图片关系、分节和原生表格必须仍在；PDF为派生交付，不能代替可编辑DOCX。重排、增删章节后重新更新域和目录再检查。

技术样例通过不代表真实文案正确、全部页码准确、目标宿主同步或真实截图可读。发现能力缺口先说明，不能用手写编号、扁平截图或整篇横向冒充本场景完成。来源与许可见[工作流来源](workflow-sources.json)，实测参数见[命令观察](craft-command-evidence.json)，具体配方见[步骤](craft-steps.json)。

目录应含一二级标题、可更新TOC域和指向现存书签的超链接。渲染与分页随字体和内容改变，示例页码不应照抄；更新目录后需在实际目标查看器检查跳转和页码。
