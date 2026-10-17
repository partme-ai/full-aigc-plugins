# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 组件复用而非重复绘制

参考：[figma/mcp-server-guide/figma-generate-library](https://github.com/figma/mcp-server-guide/blob/f2789420e7e8b4e2465dfeb1e12e1fc6a31397e5/skills/figma-generate-library/SKILL.md)。

先确认只需一组指标卡还是完整设计系统；本任务只建立所需组件，再放实例展示数据。修改组件或实例之前取实际ID，避免把展示页当成组件库完成。

原配方：`metric-card-component`。输入与边界：320×180指标卡，标题、数值和变化说明，转换为本地组件。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"name":"复用指标卡组件"}` |
| 2 | `node.create` | `{"type":"frame","name":"Metrics/Revenue","x":0,"y":0,"width":320,"height":180,"props":{"fill":"#ffffff","clip":true,"cornerRadius":12}}` |
| 3 | `node.create` | `{"type":"text","name":"MetricName","x":24,"y":22,"width":272,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Revenue"}` |
| 4 | `node.create` | `{"type":"text","name":"MetricValue","x":24,"y":60,"width":272,"height":30,"props":{"fontFamily":"Inter","fontSize":36,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"$12,480"}` |
| 5 | `node.create` | `{"type":"text","name":"MetricDelta","x":24,"y":120,"width":272,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#16804a","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"+8.2% vs last month"}` |
| 6 | `component.create` | `{"ids":[{"$ref":"root.id"}]}` |

检查：实例仍关联组件，数据差异在正确实例中，原有节点保持。

能力边界：不宣称Craft支持Figma发布库、全部变量作用域或Code Connect。

原配方结果检查：["组件清单含该卡片", "标题数值与比较周期保留", "子文字仍可编辑"]

原配方限制：没有绑定实时业务数据；百分比须由实际数据计算，不能凭颜色宣称增长。

## 尺寸变化后再验收布局

参考：[figma/mcp-server-guide/figma-use](https://github.com/figma/mcp-server-guide/blob/f2789420e7e8b4e2465dfeb1e12e1fc6a31397e5/skills/figma-use/SKILL.md)。

先明确容器与子节点的父子关系，再设置实际支持的布局和填充。用两个真实容器宽度观察文本、按钮与间距，不靠静态截图推断响应行为。

原配方：`responsive-fill-resize`。输入与边界：先建360宽卡片，再改为640；左右内边距24，内容应填满592。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"name":"容器变宽后的自适应内容"}` |
| 2 | `node.create` | `{"type":"frame","name":"ResponsiveCard","x":0,"y":0,"width":360,"height":220,"props":{"fill":"#ffffff","clip":true,"layout":"vertical","padding":24,"gap":16}}` |
| 3 | `node.create` | `{"type":"text","name":"ResponsiveHeading","x":0,"y":0,"width":312,"height":30,"props":{"fontFamily":"Inter","fontSize":22,"fill":"#172033","textAutoResize":"height","sizingH":"fill"},"parent":{"$ref":"root.id"},"text":"One layout, flexible width"}` |
| 4 | `node.create` | `{"type":"rectangle","name":"ContentArea","x":0,"y":0,"width":312,"height":90,"props":{"fill":"#f1f5f9","cornerRadius":8,"sizingH":"fill"},"parent":{"$ref":"root.id"}}` |
| 5 | `node.set` | `{"id":{"$ref":"root.id"},"props":{"width":640}}` |

检查：变宽后内容跟随且无裁切；关键节点ID和边界可查询。

能力边界：不发送Figma Plugin API代码；Figma的HUG/FILL取值不直接当Craft参数。

原配方结果检查：["实际画板宽640", "内容与标题宽592且保留左右24间距", "文字未因绝对坐标放大而拉伸"]

原配方限制：这是一次指定宽度的布局回归，不能据此承诺任意设备与任意文案都自适应。

## 有下一步的表单错误状态

参考：[figma/mcp-server-guide/figma-generate-design](https://github.com/figma/mcp-server-guide/blob/f2789420e7e8b4e2465dfeb1e12e1fc6a31397e5/skills/figma-generate-design/SKILL.md)。

从真实字段错误和可采取的修正动作组织界面，保留标签、用户输入和可读错误提示；确认提示出现后不遮住按钮或改变阅读顺序。

原配方：`field-error-state`。输入与边界：420×240表单片段，字段标签、无效输入与可读错误说明。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `file.new` | `{"name":"带明确错误信息的字段状态"}` |
| 2 | `node.create` | `{"type":"frame","name":"EmailError","x":0,"y":0,"width":420,"height":240,"props":{"fill":"#ffffff","clip":true}}` |
| 3 | `node.create` | `{"type":"text","name":"FieldLabel","x":24,"y":24,"width":372,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Email address"}` |
| 4 | `node.create` | `{"type":"rectangle","name":"InvalidEmailField","x":24,"y":70,"width":372,"height":52,"props":{"fill":"#ffffff","cornerRadius":8,"stroke":"#b91c1c","strokeWeight":2},"parent":{"$ref":"root.id"}}` |
| 5 | `node.create` | `{"type":"text","name":"InvalidValue","x":40,"y":84,"width":340,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"not-an-email"}` |
| 6 | `node.create` | `{"type":"text","name":"ErrorMessage","x":24,"y":140,"width":372,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#b91c1c","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Enter a valid email address."}` |

检查：错误内容具体、文本未截断、操作按钮仍可见。

能力边界：这里只制作可编辑视觉状态，不声称已连后端验证或实现真实表单行为。

原配方结果检查：["错误不只依赖红色，还提供文字", "字段、标签和错误关系清晰", "错误说明保持可编辑"]

原配方限制：不是实际校验器，也不证明可访问性程序关联已实现；开发交付仍需label/description语义绑定。

## 版本与执行

执行包装沿用本技能主文件。以真实返回的节点ID建立父子和组件关系，命名引用先绑定；不能将Figma Plugin API代码直接当Craft命令。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
