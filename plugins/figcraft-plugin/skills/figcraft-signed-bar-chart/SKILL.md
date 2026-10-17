---
name: figcraft-signed-bar-chart
description: 当用户需要用FigCraft完成含正负与零值的可编辑柱状图时使用；提供实际CLI/MCP命令、返回ID绑定、可编辑交付及修改后复核步骤。
license: Apache-2.0
---

# 含正负与零值的可编辑柱状图

先读取[命令与执行方法](references/craft-methods.md)，按照[参数配方](references/craft-steps.json)绑定实际对象。完整来源见[固定GitHub记录](references/workflow-sources.json)，独立[CLI执行器](scripts/run_recipe.py)随技能交付。

正负柱以零基线分开、零值有标签且高度为0，类目与值一一对应；修改数据后按同一量程重算所有柱和基线，标签保持可编辑，SVG与PNG体现正确方向。

这是可编辑形状和文字，不是带自动数据绑定的图表控件。数据来源/单位/期间必须由任务核实；不接受NaN/无穷/缺失冒充0。全零用[-1,1]示意区间防除零，标签写0，不添加假柱高。

先核对目标文件、数据/令牌/组件的已有约定和空白区，保留输入，仅写新输出文件。回读设置及实际PNG/SVG，再独立重开验证；不能以模板或绿色命令代替视觉验收。

需要内嵌界面时交给 **figcraft-editor** 技能。独立安装：`npx skills add full-aigc-skills/figcraft-skills --skill figcraft-editor`。本批仍为开发候选，市场发行与宿主同步状态以本次实际记录为准。
