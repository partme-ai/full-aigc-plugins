# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 文字母版与轮廓交付分开

参考：[github/awesome-copilot/adobe-illustrator-scripting](https://github.com/github/awesome-copilot/blob/cb64ad12e32737ae764becd6885462e9b4c7cb00/skills/adobe-illustrator-scripting/SKILL.md)；[skillhub:adobe-illustrator-scripting](https://api.skillhub.cn/api/v1/download?slug=adobe-illustrator-scripting)。

先确认实际字体可用，再制作活文字母版；复制为另一个输出后，仅对本次标志转轮廓。交接时说明哪份可改字，哪份用于无字体环境。

原配方：`wordmark-live-and-outlined`。输入与边界：示例文字CRAFT，Arial字体；先确认实际字体存在和使用授权。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"name":"文字标志母版与轮廓交付","width":420,"height":160,"units":"Pixels","backgroundContents":"white"}` |
| 2 | `text.create` | `{"x":30,"y":105,"text":"CRAFT","size":64,"font":"Arial","color":"#172033"}` |
| 3 | `file.save` | `{"path":"wordmark-live.vectorcraft"}` |
| 4 | `type.createOutlines` | `{}` |
| 5 | `file.save` | `{"path":"wordmark-outlined.vectorcraft"}` |

检查：母版文字仍可编辑，轮廓版外观一致且文件名不同。

能力边界：不运行Illustrator JSX；不把整份既有图的其他文字一起转轮廓。

原配方结果检查：["母版仍含CRAFT文字", "独立新图交付工程无活文字且含轮廓；既有图仅检查本次文字，其他文字保留可编辑", "母版与轮廓版文件名不同"]

原配方限制：转轮廓不可当成仍可改字；不能仅保存最终轮廓而丢失母版。固定母版路径是新目录示例，真实任务用未占用路径。

## 品牌颜色检查

参考：[ie3jp/illustrator-mcp-server/illustrator-preflight](https://github.com/ie3jp/illustrator-mcp-server/blob/57c5c101a5192c61535493f39b653e6f92b8eb29/plugins/ie3-design-bridge/skills/illustrator-preflight/SKILL.md)。

从品牌资料确认实际色值，用可编辑色块和文字标签建立对照。逐一核对标签与对象颜色，屏幕配色和印刷分色分别判断。

原配方：`editable-brand-palette`。输入与边界：4个示例sRGB色，标签必须与填色一致。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"name":"品牌色板与十六进制标签","width":440,"height":180,"units":"Pixels","backgroundContents":"white"}` |
| 2 | `shape.rectangle` | `{"x":20,"y":30,"width":80,"height":80}` |
| 3 | `paint.setFill` | `{"color":"#172033"}` |
| 4 | `paint.setStroke` | `{"none":true}` |
| 5 | `text.create` | `{"x":20,"y":140,"text":"#172033","size":13,"font":"Arial","color":"#172033"}` |
| 6 | `shape.rectangle` | `{"x":120,"y":30,"width":80,"height":80}` |
| 7 | `paint.setFill` | `{"color":"#2563eb"}` |
| 8 | `paint.setStroke` | `{"none":true}` |
| 9 | `text.create` | `{"x":120,"y":140,"text":"#2563eb","size":13,"font":"Arial","color":"#172033"}` |
| 10 | `shape.rectangle` | `{"x":220,"y":30,"width":80,"height":80}` |
| 11 | `paint.setFill` | `{"color":"#16a34a"}` |
| 12 | `paint.setStroke` | `{"none":true}` |
| 13 | `text.create` | `{"x":220,"y":140,"text":"#16a34a","size":13,"font":"Arial","color":"#172033"}` |
| 14 | `shape.rectangle` | `{"x":320,"y":30,"width":80,"height":80}` |
| 15 | `paint.setFill` | `{"color":"#d97706"}` |
| 16 | `paint.setStroke` | `{"none":true}` |
| 17 | `text.create` | `{"x":320,"y":140,"text":"#d97706","size":13,"font":"Arial","color":"#172033"}` |
| 18 | `select.all` | `{}` |
| 19 | `object.group` | `{}` |

检查：色块实际值对应标签；说明色彩模式与尚未检查的分色问题。

能力边界：十六进制RGB色板不能证明专色、叠印或PDF/X合规。

原配方结果检查：["四个色块与四个标签对应", "组内对象仍可编辑", "不把普通RGB色块说成全局专色色板"]

原配方限制：这不是印刷色样或自动全局色同步；已有图纸按返回ID归组，不选中其他用户内容。

## 验证真实几何而非白色遮盖

参考：[github/awesome-copilot/adobe-illustrator-scripting](https://github.com/github/awesome-copilot/blob/cb64ad12e32737ae764becd6885462e9b4c7cb00/skills/adobe-illustrator-scripting/SKILL.md)。

明确外径和内径，按真实对象执行布尔减法；随后在有色背景检查透空部分，查看对象结构确认不是白圆覆盖。

原配方：`hollow-ring-minus-front`。输入与边界：外圆160内圆80，先外后内；共同中心120,120。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"name":"真实镂空圆环","width":240,"height":240,"units":"Pixels","backgroundContents":"white"}` |
| 2 | `shape.ellipse` | `{"x":40,"y":40,"width":160,"height":160}` |
| 3 | `paint.setFill` | `{"color":"#2563eb"}` |
| 4 | `paint.setStroke` | `{"none":true}` |
| 5 | `shape.ellipse` | `{"x":80,"y":80,"width":80,"height":80}` |
| 6 | `paint.setFill` | `{"color":"#2563eb"}` |
| 7 | `paint.setStroke` | `{"none":true}` |
| 8 | `select.all` | `{}` |
| 9 | `object.pathfinder.minusFront` | `{}` |
| 10 | `paint.setFill` | `{"color":"#2563eb"}` |
| 11 | `paint.setStroke` | `{"none":true}` |

检查：中心透明且布尔结果可保存重开，不依赖白色背景。

能力边界：路径与颜色值使用Craft当前schema，不能照搬Illustrator坐标对象。

原配方结果检查：["中心透明/底色透出且环带存在", "不是白圆盖住蓝圆", "SVG保留复合路径"]

原配方限制：已有图纸用实际两圆ID调用select.set，不可select.all；反向堆叠会产生不同结果。

## 版本与执行

执行包装沿用本技能主文件。文字、对象及布尔运算操作使用实际返回或选择的目标；转轮廓前另存活文字母版，避免影响已有图中的其他文本。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
