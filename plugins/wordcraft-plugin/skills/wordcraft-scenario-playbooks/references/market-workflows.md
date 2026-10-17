# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 编号是文档结构

参考：[skillhub:word-docx](https://api.skillhub.cn/api/v1/download?slug=word-docx)；[anthropics/skills/docx](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/docx/SKILL.md)。

按实际动作组织步骤，用原生编号而不是手写数字；每步有可观察结果，必要位置注明停止条件。插入新步骤后检查编号连续性与缩进。

原配方：`sop-numbered-steps`。输入与边界：已有操作顺序、必要输入与停止条件。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `layout.size` | `{"name":"A4"}` |
| 2 | `para.heading1` | `{}` |
| 3 | `text.insert` | `{"text":"资料归档SOP"}` |
| 4 | `text.newParagraph` | `{}` |
| 5 | `para.normal` | `{}` |
| 6 | `para.numbering` | `{"kind":"numbered"}` |
| 7 | `text.insert` | `{"text":"核对原件编号"}` |
| 8 | `text.newParagraph` | `{}` |
| 9 | `text.insert` | `{"text":"登记目录与存放位置"}` |
| 10 | `text.newParagraph` | `{}` |
| 11 | `text.insert` | `{"text":"复核后归档"}` |
| 12 | `text.newParagraph` | `{}` |
| 13 | `para.numbering` | `{"off":true}` |
| 14 | `text.insert` | `{"text":"停止条件：编号冲突或原件缺失时，暂停归档并报告负责人。"}` |
| 15 | `text.newParagraph` | `{}` |

检查：编号可继续编辑，新增一步后顺序正确，分页处可读。

能力边界：不把字符1.当成原生编号，也不要求上游固定字体。

原配方结果检查：["正文包含输入事实", "标题样式与正文分离", "保存DOCX后重开并导出PDF检查分页"]

原配方限制：不得把这些示例步骤用于无关高风险设备操作；编号连续性需看实际DOCX与PDF。

## 正文与节布局分开处理

参考：[skillhub:word-docx](https://api.skillhub.cn/api/v1/download?slug=word-docx)；[skillhub:moways-doc](https://api.skillhub.cn/api/v1/download?slug=moways-doc)。

先确认纸张、页边距和页眉页脚属于哪一节，再写本次业务函；长正文后检查跨页和页码，避免只对第一页截图作判断。

原配方：`letter-header-footer`。输入与边界：已确认的发文单位、收件人和正文；不自动发送。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `layout.size` | `{"name":"A4"}` |
| 2 | `layout.margins` | `{"preset":"normal"}` |
| 3 | `insert.header` | `{"text":"示例单位 · 项目办公室"}` |
| 4 | `insert.closeHeader` | `{}` |
| 5 | `para.heading1` | `{}` |
| 6 | `text.insert` | `{"text":"资料补充函"}` |
| 7 | `text.newParagraph` | `{}` |
| 8 | `para.normal` | `{}` |
| 9 | `text.insert` | `{"text":"收件人：项目联系人。\n请补充缺失的归档目录与版本说明。"}` |
| 10 | `text.newParagraph` | `{}` |
| 11 | `insert.footer` | `{"text":"草稿 · 待审核"}` |
| 12 | `insert.closeHeader` | `{}` |

检查：所有页的页眉页脚、正文和分页正确，中文字体可用。

能力边界：不采用商业机构的专有排版标准，不以示例声明国标或公文合规。

原配方结果检查：["正文包含输入事实", "标题样式与正文分离", "保存DOCX后重开并导出PDF检查分页"]

原配方限制：姓名、单位、落款必须来自真实输入；本技能不发送函件。

## 修订副本保留上下文

参考：[anthropics/skills/docx](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/docx/SKILL.md)；[skillhub:word-docx](https://api.skillhub.cn/api/v1/download?slug=word-docx)。

先列术语替换表和不应改动的引用、编号与原话，在副本中按范围替换；回读命中数量，检查段落样式和附近文本。

原配方：`term-normalization-draft`。输入与边界：原文与经批准的术语映射；替换前先审查上下文。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `layout.size` | `{"name":"A4"}` |
| 2 | `para.heading1` | `{}` |
| 3 | `text.insert` | `{"text":"术语统一稿"}` |
| 4 | `text.newParagraph` | `{}` |
| 5 | `para.normal` | `{}` |
| 6 | `text.insert` | `{"text":"旧称：资料包。请将资料包提交至资料包目录。"}` |
| 7 | `text.newParagraph` | `{}` |
| 8 | `edit.replaceAll` | `{"text":"资料包","matchCase":false,"wholeWord":false,"with":"档案包"}` |

检查：替换只覆盖约定范围，段落结构保留，原文件不被覆盖。

能力边界：普通替换不等于保留修订痕迹、评论锚点或所有复杂OOXML结构；按当前能力说明限制。

原配方结果检查：["正文包含输入事实", "标题样式与正文分离", "保存DOCX后重开并导出PDF检查分页"]

原配方限制：真实任务先保留原文件；不对机构名称、引用或专有名称做未授权全局替换。

## 版本与执行

执行包装沿用本技能主文件。段落样式、原生编号和节设置分别检查；修改既有文档时保存副本，不能从纯文本替换推断评论或修订结构完整。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
