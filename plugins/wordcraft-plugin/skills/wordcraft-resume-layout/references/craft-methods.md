# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 设置简历页面 | `layout.size` | `{"name":"A4"}` |
| 2. 设置页面边距，单位pt | `layout.margins` | `{"top":36,"bottom":36,"left":42,"right":42}` |
| 3. 应用本段语义样式 | `para.style` | `{"style":"Heading 1"}` |
| 4. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"姓名与联系方式：待核实"}` |
| 5. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 6. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 7. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"工作经历"}` |
| 8. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 9. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 10. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"单位、岗位、任职日期与可证实业绩：待核实"}` |
| 11. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 12. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 13. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"教育经历"}` |
| 14. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 15. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 16. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"学校、专业与日期：待核实"}` |
| 17. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 18. 应用本段语义样式 | `para.style` | `{"style":"Heading 2"}` |
| 19. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"技能与项目"}` |
| 20. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 21. 应用本段语义样式 | `para.style` | `{"style":"Normal"}` |
| 22. 输入已核实内容或明确待确认占位 | `text.insert` | `{"text":"实际技能、本人贡献及可核验项目：待核实"}` |
| 23. 创建真实段落边界 | `text.newParagraph` | `{}` |
| 24. 核对结构，不虚构履历 | `document.inspect` | `{"text":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "layout.size", "params": {"name": "A4"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

wordcraft-cli run --file input.docx --cmd 'text.insert={"text":"正文"}' --save output.docx。多个步骤使用多个 --cmd，同进程保留选择和插入点。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

姓名联系信息准确，日期连续，PDF无截字，文本可复制。

边界：示例结构需替换为真实履历；不虚构岗位、学历和业绩。 示例章节为结构起点，待核实字段不能当作已填文档交付；每个章节用真实段落与Heading样式。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
