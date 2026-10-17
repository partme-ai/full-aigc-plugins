# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 删除敏感内容而非盖黑框

参考：[anthropics/skills/pdf](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/pdf/SKILL.md)；[community-access/accessibility-agents/pdf-remediator](https://github.com/community-access/accessibility-agents/blob/decf6bac7f086c19afb242797b4974671ceff597/skills/pdf-remediator/SKILL.md)。

先确认需要删除的具体词及匹配范围，标记后再应用真正删改；完整保存新文件，重开抽取文本并审核删改结果，同时检查渲染。

原配方：`redact-pdf`。输入与边界：示例参数必须按当前输入、选择和实际返回ID替换；$变量先解析，数组变量整字段替换，不能将本文件直接当原生CLI脚本执行。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `doc_hidden_info` | `{"doc":1}` |
| 2 | `redact_mark` | `{"doc":1,"find":"CONFIDENTIAL","whole_words":true}` |
| 3 | `redact_apply` | `{"doc":1}` |
| 4 | `doc_audit_redactions` | `{"doc":1}` |
| 5 | `doc_save` | `{"doc":1,"path":"output/redacted.pdf","full":true}` |
| 6 | `text_extract` | `{"doc":1}` |

检查：敏感内容不可再从文本层提取，未目标文本仍在，审计无遗留项。

能力边界：擦除可能破坏既有签名；黑色矩形不是删改，未测试图层或附件不能声称已清除。

原配方结果检查："新进程重开后搜索目标词、复制文字、检查元数据与图像内敏感内容。"

原配方限制：仅画黑框不算脱敏；find示例必须替换为实际授权范围，不误删相似非敏感内容。 doc_audit_redactions只审计假遮盖，不能证明所有元数据、附件、表单或像素内秘密都消失；隐藏信息须按已授权类别另行处理，不能无条件删除全部内容。

## 版本与执行

执行包装沿用本技能主文件。先doc_open取得同一会话的真实doc编号，页码从1开始。直接MCP工具与内部命令表分别按实际schema使用。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
