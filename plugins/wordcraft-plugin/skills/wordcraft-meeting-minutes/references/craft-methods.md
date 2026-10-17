# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 2. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"会议时间：待核实"}` |
| 3. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 4. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 5. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"参会人：待核实"}` |
| 6. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 7. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 8. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"讨论建议：待核实"}` |
| 9. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 10. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 11. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"决定：待确认（非已决议）"}` |
| 12. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 13. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 14. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"行动项："}` |
| 15. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 16. 填写表格一行，单元格内不得含制表或换行 | `text.insert` | `{"text":"行动项\t责任人\t截止时间\t状态"}` |
| 17. 真实段落分隔表格行 | `text.newParagraph` | `{}` |
| 18. 填写表格一行，单元格内不得含制表或换行 | `text.insert` | `{"text":"待确认事项\t待确认\t待确认\t未确认"}` |
| 19. 真实段落分隔表格行 | `text.newParagraph` | `{}` |
| 20. 填写表格一行，单元格内不得含制表或换行 | `text.insert` | `{"text":"待补充事项\t待确认\t待确认\t未确认"}` |
| 21. 从末尾定位连续表格文本 | `caret.docEnd` | `{"extend":false}` |
| 22. 向上扩选一行表格文本 | `caret.paraUp` | `{"extend":true}` |
| 23. 向上扩选一行表格文本 | `caret.paraUp` | `{"extend":true}` |
| 24. 向上扩选一行表格文本 | `caret.paraUp` | `{"extend":true}` |
| 25. 将选中的多段文本转为原生可编辑表格 | `table.fromText` | `{"separator":"tab"}` |
| 26. 表格适合页面 | `table.autofit` | `{"mode":"window"}` |
| 27. 跨页重复表头 | `table.repeatHeader` | `{}` |
| 28. 核对全文与表格 | `document.inspect` | `{"text":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "text.insert", "params": {"text": "会议时间：待核实\n参会人：待核实\n决定：\n行动项："}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

wordcraft-cli run --file input.docx --cmd 'text.insert={"text":"正文"}' --save output.docx。多个步骤使用多个 --cmd，同进程保留选择和插入点。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

区分讨论、决定和待办，行动项包含责任人、截止时间与状态。

边界：所有待核实/待确认占位按实际会议替换；示例两项不代表真实决定。每行必须用text.newParagraph，不能用软换行；仅扩选刚插入的表格行。已有文档应先定位新空段落再插入。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
