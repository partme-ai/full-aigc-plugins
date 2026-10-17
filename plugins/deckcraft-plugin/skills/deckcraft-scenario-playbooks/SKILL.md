---
name: deckcraft-scenario-playbooks
description: 使用 DeckCraft 制作指标简报、方案比较、流程图、风险矩阵、趋势图、培训问答和演讲交接稿时使用；按场景查具体CLI/MCP命令、参数与检查步骤。
license: Apache-2.0
---

# DeckCraft 场景操作手册

先读取真实输入，按以下相关类别选流程。表格中的示例数据不代表实际业务事实。每条默认新建空文件，不直接覆盖原稿。

- [report：2条](references/report.md)：管理层一页指标简报、风险四象限汇报页。
- [decision：1条](references/decision.md)：可编辑方案比较表。
- [diagram：1条](references/diagram.md)：审批步骤流程图。
- [data：1条](references/data.md)：实际与计划趋势图。
- [presentation：2条](references/presentation.md)：产品演示的问题与结果叙事、可交接的演讲备注稿。
- [education：1条](references/education.md)：培训问答与隐藏答案页。

## 调用与会话

宿主已打开内嵌编辑器时，使用该同一MCP会话，等待 `editor_status` 就绪；读取宿主工具schema后以 `run_command {"command":"方法ID","params":{…}}` 逐条执行。工具名与参数因宿主适配有差异，不能把独立CLI文件改动称为同画面编辑。

独立CLI语法：`deckcraft-cli run --cmd <id=JSON> --save output.deckcraft`。每个 `--cmd` 的值为方法ID、等号、JSON对象组成的一个argv参数。把整组步骤放在同一次run，避免光标、当前表格、图形选择丢失。组合多个场景时只执行一次 `file.new`，其余流程跳过 `newDocumentOnly:true` 步骤，从 `slide.new` 开始；给既有页补备注时用实际页 index，不新建示例页。比较表与趋势图可以按此合并到一份演示，保留两页各自备注。使用0.7.0原生CLI命令目录作为观察依据；执行前查询实际版本和schema。保存后新进程重开，检查内容、公式或对象；导出格式另行检查。

[结构化步骤](references/recipes.json)含测试输入的可观察断言；[命令证据](references/command-evidence.json)证明方法在固定运行时被观察，不证明场景效果已验收。[来源与许可](references/sources.json)记录借鉴的GitHub工作流事实，正文与参数例子为原创适配，没有执行外部Office脚本。

## 技能商店场景经验

遇到用证据支撑演示叙事、结构化方案比较、讲稿和可见页面分别检查时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。

## main模板与复用

在main候选中使用starter模板或从品牌文稿插入指定页时，读取[main新增工作流与目录变化](references/main-workflows.md)。CLI帮助已改为人类可读文本；结构化发现使用当前MCP方法。

## 对比表深入操作

需要显式表格ID、完整列宽、来源备注及PPTX回读后改单元格时，交给 **deckcraft-option-comparison** 技能。独立安装：`npx skills add full-aigc-skills/deckcraft-skills --skill deckcraft-option-comparison`。该入口深化现有比较表场景，不增加独立场景数；随配套插件开发预发布提供。
