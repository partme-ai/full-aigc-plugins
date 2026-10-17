---
name: wordcraft-weekly-report
description: 当用户需要用WordCraft撰写或整理工作周报，依据本周工作记录、任务进度和下周计划生成可编辑Word文档时使用；提供具体章节、字段和结果检查。
license: Apache-2.0
---

# 工作周报

读取[填写指南](references/template-guide.md)，按[模板数据](assets/template.json)整理字段，参考[虚构示例](examples/input.json)理解结构。完成、进行中与受阻分开；不把下周计划写成完成成果。

## 生成与检查

- 已打开内嵌编辑器时，确认新建空文档，编译后用该同会话MCP逐条执行实际方法；读取当前schema，不另开headless文件代替画面同步。
- 独立文件任务可用当前技能的`scripts/render_document_template.py --input 字段.json --output 步骤.json --save 新文档.docx --pdf 审阅稿.pdf`。CLI应已可用，不自动安装或覆盖已有输出。
- 未提供的事实不编造；必要时生成标注待确认的不完整草稿。输出DOCX后重开核对章节和每个表格单元格，再逐页查看PDF。

本模板只创建新文档；修改用户既有文件时先读原结构，局部修改并保留已接受内容。
