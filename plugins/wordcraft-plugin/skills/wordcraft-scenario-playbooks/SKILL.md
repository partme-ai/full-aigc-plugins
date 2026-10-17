---
name: wordcraft-scenario-playbooks
description: 使用 WordCraft 编写项目说明、SOP、版本说明、决策表、业务函、培训讲义和双栏简报时使用；按场景查具体CLI/MCP命令、参数与检查步骤。
license: Apache-2.0
---

# WordCraft 场景操作手册

先读取真实输入，按以下相关类别选流程。表格中的示例数据不代表实际业务事实。每条默认新建空文件，不直接覆盖原稿。

- [business：3条](references/business.md)：项目启动说明书、决策记录与候选方案表、带页眉页脚的业务函。
- [procedure：1条](references/procedure.md)：可执行SOP与停止条件。
- [publishing：2条](references/publishing.md)：面向用户的版本说明、双栏内部简报。
- [education：1条](references/education.md)：培训讲义与独立练习页。
- [editing：1条](references/editing.md)：术语统一的编辑副本。

## 调用与会话

宿主已打开内嵌编辑器时，使用该同一MCP会话，等待 `editor_status` 就绪；读取宿主工具schema后以 `run_command {"command":"方法ID","params":{…}}` 逐条执行。工具名与参数因宿主适配有差异，不能把独立CLI文件改动称为同画面编辑。

独立CLI语法：`wordcraft-cli run --cmd <id=JSON> --save output.docx`。每个 `--cmd` 的值为方法ID、等号、JSON对象组成的一个argv参数。把整组步骤放在同一次run，避免光标、当前表格、图形选择丢失。使用0.7.0原生CLI命令目录作为观察依据；执行前查询实际版本和schema。保存后新进程重开，检查内容、公式或对象；导出格式另行检查。

[结构化步骤](references/recipes.json)含测试输入的可观察断言；[命令证据](references/command-evidence.json)证明方法在固定运行时被观察，不证明场景效果已验收。[来源与许可](references/sources.json)记录借鉴的GitHub工作流事实，正文与参数例子为原创适配，没有执行外部Office脚本。

## 技能商店场景经验

遇到编号是文档结构、正文与节布局分开处理、修订副本保留上下文时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。

## main开发候选

使用具备新命令的main候选制作原生页眉页脚、筛选排序邮件合并或调整文档内部链接时，先读[main新增工作流与参数变化](references/main-workflows.md)。此参考明确列出版本边界；原稳定版不保证支持。
