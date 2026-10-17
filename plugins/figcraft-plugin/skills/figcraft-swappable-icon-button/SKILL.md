---
name: figcraft-swappable-icon-button
description: 当用户需要用FigCraft完成可换图标并可隐藏图标的按钮时使用；提供实际CLI/MCP命令、返回ID绑定、可编辑交付及修改后复核步骤。
license: Apache-2.0
---

# 可换图标并可隐藏图标的按钮

先读取[命令与执行方法](references/craft-methods.md)，按照[参数配方](references/craft-steps.json)绑定实际对象。完整来源见[固定GitHub记录](references/workflow-sources.json)，独立[CLI执行器](scripts/run_recipe.py)随技能交付。

按钮为同一主组件的关联实例；一个换圆图标、一个隐藏图标，各自文字独立。检查实际嵌套组件ID、可见性、间距和主组件未被覆盖，主组件改色传播且实例文字仍保留。

不创建每图标一套变体，不detach实例。Figma属性键规则不能照搬；从FigCraft addProperty回执和component.properties读取。图标是合成几何，真实图标需核实素材许可与风格。

先核对目标文件、数据/令牌/组件的已有约定和空白区，保留输入，仅写新输出文件。回读设置及实际PNG/SVG，再独立重开验证；不能以模板或绿色命令代替视觉验收。

需要内嵌界面时交给 **figcraft-editor** 技能。独立安装：`npx skills add full-aigc-skills/figcraft-skills --skill figcraft-editor`。本批仍为开发候选，市场发行与宿主同步状态以本次实际记录为准。
