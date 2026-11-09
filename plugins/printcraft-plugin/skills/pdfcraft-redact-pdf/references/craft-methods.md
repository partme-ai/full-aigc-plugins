# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 检查隐藏信息，按已授权范围另行处理元数据/附件等残留 | `doc_hidden_info` | `{"doc":1}` |
| 2. 标记已经确认需遮盖的字符串 | `redact_mark` | `{"doc":1,"find":"CONFIDENTIAL","whole_words":true}` |
| 3. 核对标记后实际应用脱敏 | `redact_apply` | `{"doc":1}` |
| 4. 审计内容移除结果 | `doc_audit_redactions` | `{"doc":1}` |
| 5. 完整重写到新文件 | `doc_save` | `{"doc":1,"path":"output/redacted.pdf","full":true}` |
| 6. 重新抽取文本核查残留 | `text_extract` | `{"doc":1}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

MCP 直接调用 `redact_mark`，参数 `{"doc": 1, "find": "CONFIDENTIAL", "whole_words": true}`。先 `doc_open` 得到真实doc编号，页码1起，页面坐标为左上角PDF点；直接工具与command_run的内部命令表不能混用。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

pdfcraft-cli run --script steps.json --root WORKSPACE。steps.json 是 [{"tool":"doc_open","args":{"path":"input.pdf"}}, {"tool":"doc_info","args":{"doc":1}}]。doc编号必须取同会话返回值，后续保存与编辑在同一脚本。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

新进程重开后搜索目标词、复制文字、检查元数据与图像内敏感内容。

边界：仅画黑框不算脱敏；find示例必须替换为实际授权范围，不误删相似非敏感内容。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 本轮运行边界

仅画黑框不算脱敏；find示例必须替换为实际授权范围，不误删相似非敏感内容。 doc_audit_redactions只审计假遮盖，不能证明所有元数据、附件、表单或像素内秘密都消失；隐藏信息须按已授权类别另行处理，不能无条件删除全部内容。
