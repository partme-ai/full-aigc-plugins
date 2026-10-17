# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 先保证读懂再安排动画

参考：[dylantarre/animation-principles/video-motion-graphics](https://github.com/dylantarre/animation-principles/blob/83597134ba8ff59838270f94d7ac7282ffa3b54d/skills/01-by-domain/video-motion-graphics/SKILL.md)；[skillhub:motion-graphics](https://api.skillhub.cn/api/v1/download?slug=motion-graphics)。

把文案按语义拆组，为每组安排进入、停留和离开；先确定可读停留，再写透明度关键帧。不同组错开时间，按原速度播放检查。

原配方：`kinetic-type`。输入与边界：示例参数必须按当前输入、选择和实际返回ID替换；$变量先解析，数组变量整字段替换，不能将本文件直接当原生CLI脚本执行。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `comp.new` | `{"name":"Type","width":1080,"height":1920,"duration":5,"frameRate":30}` |
| 2 | `layer.newText` | `{"text":"准确的短文案","name":"Phrase","size":64}` |
| 3 | `prop.addKey` | `{"path":"transform/opacity","time":0,"value":0}` |
| 4 | `prop.addKey` | `{"path":"transform/opacity","time":0.5,"value":100}` |

检查：文案能读完，动作服务信息层级，关键帧时间与合成帧率一致。

能力边界：不移植Hyperframes构建流程或AE表达式；本例只映射已知关键帧能力。

原配方结果检查："按真实播放速度检查字词顺序、标点与停留，不只看静止帧。"

原配方限制：多个词组分别建层和错开时间，不能同时闪入再称为节奏排版。

## 版本与执行

执行包装沿用本技能主文件。先确认当前合成与选中图层；关键帧时间单位以当前schema为准。可编辑工程保存与视频渲染分别检查。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
