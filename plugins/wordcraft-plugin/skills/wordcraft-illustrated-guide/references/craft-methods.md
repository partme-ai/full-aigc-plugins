# 带图片题注的操作指南的方法和参数

## 输入与任务边界

input/config.png与input/connect.png是用户批准的截图，先核对顺序、内容及像素尺寸。单位为pt，不能将像素宽度直接当打印尺寸。

按步骤插图并立即添加连续编号题注；保留图片比例与替代文本，检查两幅嵌入图片、SEQ编号1/2和题注位置，逐页看图文是否分离。

## 具体步骤

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 2. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"设备配置图解"}` |
| 3. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 4. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 5. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"仅使用已确认的截图，不编造界面步骤。"}` |
| 6. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 7. 从工作区导入已核对的截图并设置pt宽度与替代文本 | `insert.picture` | `{"path":"input/config.png","width":240,"alt":"配置步骤截图"}` |
| 8. 紧跟所选图片插入原生SEQ题注 | `references.caption` | `{"label":"Figure","text":"配置位置示例","position":"below"}` |
| 9. 移动到当前文档末尾 | `caret.docEnd` | `{}` |
| 10. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 11. 为当前段落应用真实语义样式 | `para.style` | `{"style":"Normal"}` |
| 12. 插入已核实内容；示例字段按任务替换 | `text.insert` | `{"text":"核对连接"}` |
| 13. 创建独立段落，不能用软换行代替 | `text.newParagraph` | `{}` |
| 14. 从工作区导入已核对的截图并设置pt宽度与替代文本 | `insert.picture` | `{"path":"input/connect.png","width":180,"alt":"连接检查截图"}` |
| 15. 紧跟所选图片插入原生SEQ题注 | `references.caption` | `{"label":"Figure","text":"连接检查示例","position":"below"}` |
| 16. 更新原生题注序号字段 | `references.updateFields` | `{}` |
| 17. 核对真实内容和对象结构 | `document.inspect` | `{"text":true}` |

## CLI与宿主MCP

CLI先用`wordcraft-cli commands --json`核对当前版本方法和参数。逐条以argv添加`--cmd`，同一个`wordcraft-cli run --cmd <id=JSON> ... --save 新输出.docx`进程执行全部步骤。已有文件操作需显式`--file 输入.docx`，本技能默认新建，不自动覆盖。`craft-steps.json`是编排手册，不是CLI脚本文件；用每步command和params构造参数，不把purpose等字段传给引擎。

宿主内先调用该插件的open_browser_editor，使用实际editorUrl打开内置浏览器，等待editor_status.attached。读取本实例实际工具schema，使用`execute`和`{"command":"具体方法","params":{实际参数}}`，按相同顺序执行。不得另外启动headless CLI声称画面会同步；若同会话命令目录缺少方法，明确说明并询问用户是否改用保存后重开，不能假装执行。

完成后使用save_document等当前实际工具保存新文件。保存路径和参数以本会话schema为准，不能猜测固定ID。光标位置和选区是状态，任何插入前先核对，失败后不要跳过继续。

## 结果检查

独立CLI另起进程`wordcraft-cli text 输出.docx`核对文本，再`wordcraft-cli convert 输出.docx 审阅.pdf`及`wordcraft-cli render 输出.docx 首页面.png --page 1 --scale 1`。长文档逐页渲染。DOCX域、书签、图片关系、分节和原生表格必须仍在；PDF为派生交付，不能代替可编辑DOCX。重排、增删章节后重新更新域和目录再检查。

技术样例通过不代表真实文案正确、全部页码准确、目标宿主同步或真实截图可读。发现能力缺口先说明，不能用手写编号、扁平截图或整篇横向冒充本场景完成。来源与许可见[工作流来源](workflow-sources.json)，实测参数见[命令观察](craft-command-evidence.json)，具体配方见[步骤](craft-steps.json)。

两张示例宽度分别240/180pt，对应EMU为3048000/2286000，保留实际源图比例。题注应紧邻图片；本配方不承诺浮动图片与题注绑定为同一框，跨页位置必须渲染后审阅。不得仅把Figure 1敲成文本就声称存在自动编号。
