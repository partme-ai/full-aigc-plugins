# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 用证据支撑演示叙事

参考：[skillhub:afrexai-presentation-mastery](https://api.skillhub.cn/api/v1/download?slug=afrexai-presentation-mastery)；[anthropics/skills/pptx](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/pptx/SKILL.md)。

先明确观众需要做什么决定，再将真实问题、操作证据与结果分别落页。每页用明确结论组织图表或截图，结果数字来自输入，不用空泛标题代替证据。

原配方：`demo-problem-result`。输入与边界：已验证的用户问题、演示步骤与可观察结果；保留已知限制。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2 | `slide.new` | `{"layout":"titleAndContent","title":"用户问题","body":"资料编号重复，人工核对成本高。"}` |
| 3 | `slide.notes` | `{"text":"先解释输入与问题，不先堆功能。"}` |
| 4 | `slide.new` | `{"layout":"titleAndContent","title":"演示步骤","body":"导入资料 → 检查编号 → 定位重复项。"}` |
| 5 | `slide.notes` | `{"text":"使用已授权的演示数据，不展示私人资料。"}` |
| 6 | `slide.new` | `{"layout":"titleAndContent","title":"结果与限制","body":"定位重复项；是否删除由使用者复核。"}` |

检查：每页有明确用途，结论与证据一致，实际投影尺寸可读。

能力边界：不强制上游固定配色、字体或全页图片；交付保留原生可编辑对象。

原配方结果检查：["版心内无溢出与遮挡", "备注记录来源与待确认假设", "保存源工程、导出PPTX后核对可编辑对象"]

原配方限制：不能把计划能力写成已完成结果；实际演示需预演并检查页面信息密度。

## 结构化方案比较

参考：[skillhub:powerpoint-pptx](https://api.skillhub.cn/api/v1/download?slug=powerpoint-pptx)。

先检查现有页面和主题；比较维度固定在列，实际方案固定在行，单位、缺失值与口径统一。既有模板先识别对象，再替换本次内容。

原配方：`option-comparison-table`。输入与边界：提供相同维度的候选方案，禁止把不等口径数字直接并列。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2 | `slide.new` | `{"layout":"titleAndContent","title":"方案比较","body":""}` |
| 3 | `insert.table` | `{"rows":3,"cols":3,"rect":[48,130,864,280]}` |
| 4 | `text.set` | `{"cell":[0,0],"text":"维度"}` |
| 5 | `text.set` | `{"cell":[0,1],"text":"方案A"}` |
| 6 | `text.set` | `{"cell":[0,2],"text":"方案B"}` |
| 7 | `text.set` | `{"cell":[1,0],"text":"交付"}` |
| 8 | `text.set` | `{"cell":[1,1],"text":"快速试点"}` |
| 9 | `text.set` | `{"cell":[1,2],"text":"完整建设"}` |
| 10 | `text.set` | `{"cell":[2,0],"text":"约束"}` |
| 11 | `text.set` | `{"cell":[2,1],"text":"人工复核"}` |
| 12 | `text.set` | `{"cell":[2,2],"text":"实施周期"}` |
| 13 | `table.options` | `{"headerRow":true}` |
| 14 | `slide.notes` | `{"text":"比较依据：当前范围与资源。最终选择由决策人确认。"}` |

检查：表格可编辑，行列与原数据对应，文字没有越界。

能力边界：新建示例不能直接覆盖既有模板或假定占位符编号通用。

原配方结果检查：["版心内无溢出与遮挡", "备注记录来源与待确认假设", "保存源工程、导出PPTX后核对可编辑对象"]

原配方限制：此处不自动作商业决策；真实任务应补充来源与决策条件。

## 讲稿和可见页面分别检查

参考：[skillhub:powerpoint-pptx](https://api.skillhub.cn/api/v1/download?slug=powerpoint-pptx)；[skillhub:afrexai-presentation-mastery](https://api.skillhub.cn/api/v1/download?slug=afrexai-presentation-mastery)。

页面只保留观众需要看的结论，把展开解释与演讲提示放入备注。保存后分别查页面文字与备注，并查看逐页渲染。

原配方：`speaker-handoff-notes`。输入与边界：讲者需接手演示，提供每页目标、用时、来源与转场提示。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2 | `slide.new` | `{"layout":"titleAndContent","title":"项目进展","body":"本期完成目录整理。"}` |
| 3 | `slide.notes` | `{"text":"目标：说明范围。用时：1分钟。来源：项目台账。转场：解释剩余缺件。"}` |
| 4 | `slide.new` | `{"layout":"titleAndContent","title":"风险与下一步","body":"缺件核验完成后进入最终复核。"}` |
| 5 | `slide.notes` | `{"text":"目标：请求补齐输入。用时：1分钟。来源：缺件清单。结尾：确认负责人和期限。"}` |

检查：备注可回读，页面没有误放内部提示，字体和遮挡经过查看。

能力边界：备注保存成功不证明演讲模式、远程演示或平台协作已通过。

原配方结果检查：["版心内无溢出与遮挡", "备注记录来源与待确认假设", "保存源工程、导出PPTX后核对可编辑对象"]

原配方限制：备注不是已发送通知或批准事项；责任人与期限必须现场或从真实输入确认。

## 版本与执行

执行包装沿用本技能主文件。区分新建示例与既有模板；对已有演示先读取页、对象、主题和备注，不能假定占位符或对象编号固定。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
