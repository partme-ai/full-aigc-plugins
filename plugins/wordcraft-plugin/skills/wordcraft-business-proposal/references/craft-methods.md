# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 设置页面基本规格 | `layout.size` | `{"name":"A4"}` |
| 2. 应用本段语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 3. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"业务方案"}` |
| 4. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 5. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 6. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"目标"}` |
| 7. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 8. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 9. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"目标与衡量方式：待核实"}` |
| 10. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 11. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 12. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"方案与边界"}` |
| 13. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 14. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 15. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"实施范围、非目标与责任人：待核实"}` |
| 16. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 17. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 18. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"成本依据"}` |
| 19. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 20. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 21. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"金额、币种、来源与估算日期：待核实"}` |
| 22. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 23. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 24. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"验收方式"}` |
| 25. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 26. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 27. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"交付项、检查方式与验收人：待核实"}` |
| 28. 创建真实段落边界 | `text.newParagraph` | `{}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "layout.size", "params": {"name": "A4"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

wordcraft-cli run --file input.docx --cmd 'text.insert={"text":"正文"}' --save output.docx。多个步骤使用多个 --cmd，同进程保留选择和插入点。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

标题样式可生成目录，方案中的承诺、数字、版本和责任人一致。

边界：样式名需由 styles.list 确认；英文内置名在当前运行时不一定等于界面本地化名称。 示例章节为结构起点，待核实字段不能当作已填文档交付；每个章节用真实段落与Heading样式。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
