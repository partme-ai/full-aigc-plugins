---
name: figcraft-light-dark-token-card
description: 当用户需要用FigCraft完成明暗主题与语义颜色变量卡时使用；提供实际CLI/MCP命令、返回ID绑定、可编辑交付及修改后复核步骤。
license: Apache-2.0
---

# 明暗主题与语义颜色变量卡

先读取[命令与执行方法](references/craft-methods.md)，按照[参数配方](references/craft-steps.json)绑定实际对象。完整来源见[固定GitHub记录](references/workflow-sources.json)，独立[CLI执行器](scripts/run_recipe.py)随技能交付。

背景与文字颜色经真实语义别名和模式继承；修改Dark基础色只改变Dark容器。JSON/CSS保留模式及可用引用，保存重开仍可编辑。

不是直接导入Figma/W3C token；不得把颜色截图当作变量绑定。检查同名集合并选择新任务名，不能覆盖既有品牌变量；示例不代表自动满足对比度规范。

先核对目标文件、数据/令牌/组件的已有约定和空白区，保留输入，仅写新输出文件。回读设置及实际PNG/SVG，再独立重开验证；不能以模板或绿色命令代替视觉验收。

需要内嵌界面时交给 **figcraft-editor** 技能。独立安装：`npx skills add full-aigc-skills/figcraft-skills --skill figcraft-editor`。本批仍为开发候选，市场发行与宿主同步状态以本次实际记录为准。
