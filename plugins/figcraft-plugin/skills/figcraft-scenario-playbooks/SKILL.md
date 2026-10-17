---
name: figcraft-scenario-playbooks
description: 使用 FigCraft 制作登录页、套餐卡、指标组件、导航、自适应容器、确认弹窗、空状态和字段错误状态时使用；提供真实 CLI/MCP 参数、返回 ID 绑定与结构检查。
license: Apache-2.0
---

# FigCraft 界面场景

从[8条流程](references/workflows.md)选当前任务，[recipes.json](references/recipes.json)含具体方法和参数，[命令证据](references/command-evidence.json)记录实际目录，[来源](references/sources.json)固定Figma示例提交。图稿不代表后端业务、点击或可访问性语义已经实现。

## 返回ID与同会话MCP

先读取当前宿主工具schema。内嵌编辑器就绪后，通过同一MCP服务的create_node、set_properties或run_command调用实际方法；参数封装以tools/list为准，不猜测。父frame先创建，保存实际返回id，再交给子node.create.parent。props中的x/y相对父frame；不能把画布坐标直接当子坐标。

手册的`capture:root`表示记住该步返回对象，`{"$ref":"root.id"}`是手册绑定标记，必须替换成真实值；这不是FigCraft原生变量语法。node.set使用`{"id":实际ID,"props":{"width":640}}`明确对象。不要对未知当前选区执行宽泛修改。已有文件跳过newDocumentOnly，保留既有对象与当前画板，给本次根frame安排空白位置。

## 独立CLI

先检查`figcraft-cli --version`及`commands --json`；技能不附带二进制，缺失时按[官方发行说明](https://github.com/storytold/figcraft/releases)选择当前系统版本并遵守安装授权。原生CLI用`run steps.json --in input.figcraft --out new.figcraft`，JSON数组每项为command/params，原生不会展开$ref。

需要执行本手册的新建示例时，可运行本技能的[scripts/run_recipe.py](scripts/run_recipe.py)：`python run_recipe.py --recipes recipes.json --scene mobile-login-wireframe --output new.figcraft`，将两个路径换成本技能内实际路径。`--cli`可指定已核实的CLI。该可选脚本需要Python 3（Windows CI使用3.13），分批执行原生命令，读取创建返回ID后绑定后续参数，利用临时检查点保存重开；不实现编辑器业务、不依赖SDK。拒绝覆盖已有输出。已有文件可传`--input`，但先调整根frame位置和示例文案；当前示例坐标默认从原点开始。

CLI检查点不会保留临时选择，所以步骤使用明确parent/id/ids，不能把选择状态当跨进程契约。附带脚本用于独立文件操作，不能用于宣称宿主画面同步；可见编辑器仍须用同一MCP会话逐步操作。

## 检查与交付

保存新工程后重开，node.get检查真实节点、父子关系和文字；component.list检查组件。自动布局须核对实际子节点位置、间距和填充宽度，不仅检查layout字段存在。以export输出目标根frame再查看成图。按真实文案复核溢出、按钮含义与信息层级，替换示例价格和账号文案。assertions仅适用于嵌入的示例，不代表任意屏幕与真实产品已验收。

## 技能商店场景经验

遇到组件复用而非重复绘制、尺寸变化后再验收布局、有下一步的表单错误状态时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。

## main协作与自动保存

用户明确要求改变自动保存或移除指定协作成员时，读取[main新增能力和权限边界](references/main-workflows.md)。两个新方法的业务和宿主验收尚未完成，不因原生命令存在就推断浏览器能托管会话。

## 更具体的设计工作流

主题与语义令牌交付使用 **figcraft-light-dark-token-card**，图标可换可隐藏的复用按钮使用 **figcraft-swappable-icon-button**，正负零值柱图使用 **figcraft-signed-bar-chart**。独立安装：`npx skills add full-aigc-skills/figcraft-skills --skill 对应技能名`。当前是开发候选，不能以目录存在当作市场发布或宿主同步验收。
