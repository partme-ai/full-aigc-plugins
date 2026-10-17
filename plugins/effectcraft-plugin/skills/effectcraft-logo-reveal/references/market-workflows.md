# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 有目的的标志进入

参考：[dylantarre/animation-principles/after-effects](https://github.com/dylantarre/animation-principles/blob/83597134ba8ff59838270f94d7ac7282ffa3b54d/skills/09-by-tool-framework/after-effects/SKILL.md)。

确认标志文字和画布，再安排进入与停留；先用明确的首末关键姿态建立节奏，只有实际支持的插值参数经过查询后才调整缓动。

原配方：`logo-reveal`。输入与边界：示例参数必须按当前输入、选择和实际返回ID替换；$变量先解析，数组变量整字段替换，不能将本文件直接当原生CLI脚本执行。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `comp.new` | `{"name":"Logo","width":1920,"height":1080,"frameRate":25,"duration":4}` |
| 2 | `layer.newText` | `{"text":"品牌名称","name":"LogoTitle"}` |
| 3 | `prop.addKey` | `{"path":"transform/opacity","time":0,"value":0}` |
| 4 | `prop.addKey` | `{"path":"transform/opacity","time":1,"value":100}` |

检查：首帧、完全显示帧和尾帧符合目标，停留可读。

能力边界：示例透明度变化不等于弹性表达式；不宣称兼容loopOut、MOGRT或Lottie。

原配方结果检查："预览0、0.5、1与末帧，标志比例不变且停留足够。"

原配方限制：真实标志应由layer.addItem引用已导入素材ID；文字示例不替代品牌标志。

## 版本与执行

执行包装沿用本技能主文件。先确认当前合成与选中图层；关键帧时间单位以当前schema为准。可编辑工程保存与视频渲染分别检查。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
