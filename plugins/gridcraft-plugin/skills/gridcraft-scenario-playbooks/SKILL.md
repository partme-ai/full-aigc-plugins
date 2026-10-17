---
name: gridcraft-scenario-playbooks
description: 使用 GridCraft 制作报价明细、库存补货、加权评分、费用复核、重复键标记与结构化任务表时使用；按场景查具体CLI/MCP命令、参数与检查步骤。
license: Apache-2.0
---

# GridCraft 场景操作手册

先读取真实输入，按以下相关类别选流程。表格中的示例数据不代表实际业务事实。每条默认新建空文件，不直接覆盖原稿。

- [finance：2条](references/finance.md)：报价明细、折扣与税额、商品毛利与零收入边界。
- [operations：4条](references/operations.md)：库存低于安全线的补货清单、费用报销超限复核、交付验收比例与缺失项、项目任务表结构化与冻结表头。
- [analysis：4条](references/analysis.md)：供应商多维加权评分、销售额排行且整行保持对应、销售区域汇总并建立图表、月度增长率与零基期处理。
- [quality：2条](references/quality.md)：订单重复键标记而不删记录、受控状态下拉录入。

## 调用与会话

宿主已打开内嵌编辑器时，使用该同一MCP会话，等待 `editor_status` 就绪；读取宿主工具schema后以 `run_command {"command":"方法ID","params":{…}}` 逐条执行。工具名与参数因宿主适配有差异，不能把独立CLI文件改动称为同画面编辑。

独立CLI语法：`gridcraft-cli run --cmd <id=JSON> --out output.xlsx --quiet`。每个 `--cmd` 的值为方法ID、等号、JSON对象组成的一个argv参数。把整组步骤放在同一次run，避免光标、当前表格、图形选择丢失。使用0.7.0原生CLI命令目录作为观察依据；执行前查询实际版本和schema。保存后新进程重开，检查内容、公式或对象；导出格式另行检查。

[结构化步骤](references/recipes.json)含测试输入的可观察断言；[命令证据](references/command-evidence.json)证明方法在固定运行时被观察，不证明场景效果已验收。[来源与许可](references/sources.json)记录借鉴的GitHub工作流事实，正文与参数例子为原创适配，没有执行外部Office脚本。

`gridcraft-cli cat` 返回格式化显示值，例如 `35.0%`。读取计算值应在 run 中执行 `sheet.read {"range":"E2","formulas":false,"formatted":false}`，读取公式则另调用 `formulas:true`；不要将显示文本解析成底层金额或比率。

## 技能商店场景经验

遇到保留可重算的报价模型、标记重复而不丢失记录、增长率的零基期边界时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。
