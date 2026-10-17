---
name: vectorcraft-scenario-playbooks
description: 用 VectorCraft 创建可编辑徽章、数据柱图、镂空圆环、联系卡、品牌色板、文字标志轮廓、半圆裁切和导视箭头时使用，提供逐步CLI/MCP方法、参数和保存重开检查。
license: Apache-2.0
---

# VectorCraft 矢量场景

从[8条基础流程](references/workflows.md)及[3条0.12新增场景](references/upstream-0.12.md)选当前任务，[recipes.json](references/recipes.json)含有序方法与示例参数，[命令证据](references/command-evidence.json)记录实际原生目录，[来源](references/sources.json)固定Illustrator工作流资料提交。正文与几何为原创适配，不执行外部JSX。

先探测`vectorcraft-cli --version`和`commands`。本技能不附带CLI；缺失时按[官方发行说明](https://github.com/storytold/vectorcraft/releases)选择系统版本并遵守安装授权。原生0.12命令与插件Web运行时可能不同，先查当前schema再使用。

## 同会话操作

内嵌编辑器就绪后保持同一MCP会话；查`run_command`实际schema，将步骤的command和params交给该工具，不猜工具参数名。`inspect_document`和原生`document.inspect`用于核对当前对象。原生CLI修改另一文件不能证明宿主画面同步。

独立CLI示例：`vectorcraft-cli run --cmd shape.rectangle --params '{"x":20,"y":20,"width":80,"height":60}' --export output.vectorcraft`。每个JSON为独立argv。一次run执行同一场景的全部步骤；既有文件用`--in input.vectorcraft`并跳过`newDocumentOnly`。保存后用新进程`run --in output.vectorcraft --cmd document.inspect`检查并以`convert output.vectorcraft output.svg`导出。

## 选择、布尔与交付

创建返回的实际ID必须保留。这里未显式指定ID的填色/描边作用于刚创建的当前选区；在既有图中先用`select.set {"ids":[实际返回ID]}`明确选择，具体参数见命令证据；数组内容绑定真实返回值，不能填示例ID。带ownedSelectionOnly的select.all仅适用于该独立新图；已有用户内容时替换为本次对象ID集合，不能整图布尔或归组。既有图可直接调用`object.pathfinder.minusFront {"ids":[实际外圆ID,实际内圆ID]}`，仅处理这两圆。外圆先建、内圆后建再minusFront；倒置堆叠不能得到同样的圆环。

file.new和示例文案不是既有图编辑步骤。每条默认独立文件，组合时需要安排画板、位置和对象选择。像素画板尺寸按运行时解释，不能直接当毫米印刷尺寸。转轮廓前保存可编辑文字母版，已有目标路径换新名称；转轮廓后显式file.save至不同的新路径，不能普通保存覆盖母版。该步骤只选择本次wordmark ID，已有用户标题和注释应保持原样。textCount=0只针对独立新图测试夹具，不能为满足它而轮廓化整份用户图。转轮廓后的目标文字不能声称仍可改字。半圆裁切是真实删去几何，保留原稿以便回改。

交付可编辑源与SVG/PNG，并检查结构与实际画面。随附assertions只适用于本例输入，不能用技术回归替代品牌、数据和真实用途的设计审阅。

## 技能商店场景经验

遇到文字母版与轮廓交付分开、品牌颜色检查、验证真实几何而非白色遮盖时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。

## 0.12发布能力

需要精简命令检索或向旧版Illustrator交付AI时，读取[0.12能力与版本边界](references/upstream-0.12.md)。原生CLI与内嵌引擎分别核对版本。

0.12另补三条具体场景：尺寸标注单位交付、交织遮挡与释放、CSV可编辑文案版本；按上面的0.12参考读取结构化参数。当前手册共11条配方。
