# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 文本与视觉双路核查

参考：[openai/skills/pdf](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf/SKILL.md)；[community-access/accessibility-agents/pdf-remediator](https://github.com/community-access/accessibility-agents/blob/decf6bac7f086c19afb242797b4974671ceff597/skills/pdf-remediator/SKILL.md)。

先读页数、页面尺寸和文本层，再逐页渲染检查裁切、缺字、表格和顺序。把结构缺陷与视觉缺陷分开列出，自动修不了的交回源文档处理。

原配方：`pdf-preflight`。输入与边界：示例参数必须按当前输入、选择和实际返回ID替换；$变量先解析，数组变量整字段替换，不能将本文件直接当原生CLI脚本执行。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `doc_info` | `{"doc":1}` |
| 2 | `page_render` | `{"doc":1,"page":1,"dpi":144}` |
| 3 | `text_extract` | `{"doc":1}` |
| 4 | `form_fields` | `{"doc":1}` |

检查：文本存在且实际页面可读，未检查的标签和阅读顺序明确列出。

能力边界：不能由text_extract成功推导PDF/UA、PDF/A或PDF/X合规。

原配方结果检查："按要求核对每页尺寸、字体、文本、图像与书签，文件可打开不代表印前合规。"

原配方限制：该流程不自动认证PDF/X、PDF/A或可访问性标准；对应标准需当前真实检测工具。

## 版本与执行

执行包装沿用本技能主文件。先doc_open取得同一会话的真实doc编号，页码从1开始。直接MCP工具与内部命令表分别按实际schema使用。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
