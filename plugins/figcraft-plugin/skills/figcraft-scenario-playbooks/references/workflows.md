# FigCraft 场景步骤

每条默认独立新文件。`capture`命名该步返回值；`{"$ref":"root.id"}`必须替换成真实返回ID，不可原样传给原生CLI/MCP。

## mobile-login-wireframe：移动端登录界面

输入：390×884画板，标签、输入区域和主按钮；示例不含真实账号。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"移动端登录界面"}` |
| 2. 创建Login并保留真实返回ID | `node.create` | `{"type":"frame","name":"Login","x":0,"y":0,"width":390,"height":884,"props":{"fill":"#ffffff","clip":true}}`；返回记为`root` |
| 3. 创建Title并保留真实返回ID | `node.create` | `{"type":"text","name":"Title","x":24,"y":70,"width":342,"height":30,"props":{"fontFamily":"Inter","fontSize":30,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Welcome back"}`；返回记为`title` |
| 4. 创建EmailLabel并保留真实返回ID | `node.create` | `{"type":"text","name":"EmailLabel","x":24,"y":160,"width":342,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Email"}`；返回记为`email_label` |
| 5. 创建EmailField并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"EmailField","x":24,"y":194,"width":342,"height":52,"props":{"fill":"#f1f5f9","cornerRadius":8},"parent":{"$ref":"root.id"}}`；返回记为`email` |
| 6. 创建EmailPlaceholder并保留真实返回ID | `node.create` | `{"type":"text","name":"EmailPlaceholder","x":40,"y":208,"width":310,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"name@example.test"}`；返回记为`placeholder` |
| 7. 创建PasswordLabel并保留真实返回ID | `node.create` | `{"type":"text","name":"PasswordLabel","x":24,"y":278,"width":342,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Password"}`；返回记为`password_label` |
| 8. 创建PasswordField并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"PasswordField","x":24,"y":312,"width":342,"height":52,"props":{"fill":"#f1f5f9","cornerRadius":8},"parent":{"$ref":"root.id"}}`；返回记为`password` |
| 9. 创建SignInButton并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"SignInButton","x":24,"y":410,"width":342,"height":52,"props":{"fill":"#2563eb","cornerRadius":8},"parent":{"$ref":"root.id"}}`；返回记为`submit` |
| 10. 创建SignInText并保留真实返回ID | `node.create` | `{"type":"text","name":"SignInText","x":40,"y":424,"width":310,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","textAlign":"center"},"parent":{"$ref":"root.id"},"text":"Sign in"}`；返回记为`submit_text` |

检查：全部内容挂在Login画板而非散落页面；标签与输入区对应；主按钮文字可编辑。

边界：这是界面设计，不代表表单验证、密码存储或登录后端已实现。

## pricing-card-auto-layout：自动布局套餐卡

输入：360×460套餐卡，纵向24像素间距和24像素内边距。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"自动布局套餐卡"}` |
| 2. 创建Pricing并保留真实返回ID | `node.create` | `{"type":"frame","name":"Pricing","x":0,"y":0,"width":360,"height":460,"props":{"fill":"#ffffff","clip":true,"layout":"vertical","padding":24,"gap":24}}`；返回记为`root` |
| 3. 创建PlanName并保留真实返回ID | `node.create` | `{"type":"text","name":"PlanName","x":0,"y":0,"width":312,"height":30,"props":{"fontFamily":"Inter","fontSize":26,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Starter"}`；返回记为`plan` |
| 4. 创建Price并保留真实返回ID | `node.create` | `{"type":"text","name":"Price","x":0,"y":0,"width":312,"height":30,"props":{"fontFamily":"Inter","fontSize":30,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"$19 / month"}`；返回记为`price` |
| 5. 创建FeatureOne并保留真实返回ID | `node.create` | `{"type":"text","name":"FeatureOne","x":0,"y":0,"width":312,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"10 projects"}`；返回记为`feature1` |
| 6. 创建FeatureTwo并保留真实返回ID | `node.create` | `{"type":"text","name":"FeatureTwo","x":0,"y":0,"width":312,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Email support"}`；返回记为`feature2` |
| 7. 创建ChooseButton并保留真实返回ID | `node.create` | `{"type":"frame","name":"ChooseButton","x":0,"y":0,"width":312,"height":52,"props":{"fill":"#2563eb","layout":"horizontal","padding":12,"mainAlign":"center","crossAlign":"center"},"parent":{"$ref":"root.id"}}`；返回记为`button` |
| 8. 创建ChooseText并保留真实返回ID | `node.create` | `{"type":"text","name":"ChooseText","x":0,"y":0,"width":220,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","textAlign":"center"},"parent":{"$ref":"button.id"},"text":"Choose plan"}`；返回记为`cta` |

检查：保留纵向自动布局和间距；按钮文字是按钮子节点；修改文案后检查是否溢出。

边界：示例价格和权益是占位内容；真正计费、订阅和点击行为不包含在图稿中。

## metric-card-component：复用指标卡组件

输入：320×180指标卡，标题、数值和变化说明，转换为本地组件。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"复用指标卡组件"}` |
| 2. 创建Metrics/Revenue并保留真实返回ID | `node.create` | `{"type":"frame","name":"Metrics/Revenue","x":0,"y":0,"width":320,"height":180,"props":{"fill":"#ffffff","clip":true,"cornerRadius":12}}`；返回记为`root` |
| 3. 创建MetricName并保留真实返回ID | `node.create` | `{"type":"text","name":"MetricName","x":24,"y":22,"width":272,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Revenue"}`；返回记为`metric` |
| 4. 创建MetricValue并保留真实返回ID | `node.create` | `{"type":"text","name":"MetricValue","x":24,"y":60,"width":272,"height":30,"props":{"fontFamily":"Inter","fontSize":36,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"$12,480"}`；返回记为`value` |
| 5. 创建MetricDelta并保留真实返回ID | `node.create` | `{"type":"text","name":"MetricDelta","x":24,"y":120,"width":272,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#16804a","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"+8.2% vs last month"}`；返回记为`delta` |
| 6. 仅将本次卡片转为组件 | `component.create` | `{"ids":[{"$ref":"root.id"}]}`；返回记为`component` |

检查：组件清单含该卡片；标题数值与比较周期保留；子文字仍可编辑。

边界：没有绑定实时业务数据；百分比须由实际数据计算，不能凭颜色宣称增长。

## navigation-auto-layout：横向导航与阅读顺序

输入：640×96导航条，横向间距24、内边距24。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"横向导航与阅读顺序"}` |
| 2. 创建Navigation并保留真实返回ID | `node.create` | `{"type":"frame","name":"Navigation","x":0,"y":0,"width":640,"height":96,"props":{"fill":"#ffffff","clip":true,"layout":"horizontal","padding":24,"gap":24,"crossAlign":"center"}}`；返回记为`root` |
| 3. 创建Brand并保留真实返回ID | `node.create` | `{"type":"text","name":"Brand","x":0,"y":0,"width":130,"height":30,"props":{"fontFamily":"Inter","fontSize":24,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"CRAFT"}`；返回记为`brand` |
| 4. 创建HomeLink并保留真实返回ID | `node.create` | `{"type":"text","name":"HomeLink","x":0,"y":0,"width":80,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Home"}`；返回记为`home` |
| 5. 创建WorkLink并保留真实返回ID | `node.create` | `{"type":"text","name":"WorkLink","x":0,"y":0,"width":80,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Work"}`；返回记为`work` |
| 6. 创建AboutLink并保留真实返回ID | `node.create` | `{"type":"text","name":"AboutLink","x":0,"y":0,"width":80,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"About"}`；返回记为`about` |

检查：横向布局顺序保留；节点之间无覆盖；导航文案保持文字对象。

边界：仅导航图稿，未设置路由；真实链接与键盘交互须由产品实现。

## responsive-fill-resize：容器变宽后的自适应内容

输入：先建360宽卡片，再改为640；左右内边距24，内容应填满592。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"容器变宽后的自适应内容"}` |
| 2. 创建ResponsiveCard并保留真实返回ID | `node.create` | `{"type":"frame","name":"ResponsiveCard","x":0,"y":0,"width":360,"height":220,"props":{"fill":"#ffffff","clip":true,"layout":"vertical","padding":24,"gap":16}}`；返回记为`root` |
| 3. 创建ResponsiveHeading并保留真实返回ID | `node.create` | `{"type":"text","name":"ResponsiveHeading","x":0,"y":0,"width":312,"height":30,"props":{"fontFamily":"Inter","fontSize":22,"fill":"#172033","textAutoResize":"height","sizingH":"fill"},"parent":{"$ref":"root.id"},"text":"One layout, flexible width"}`；返回记为`heading` |
| 4. 创建ContentArea并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"ContentArea","x":0,"y":0,"width":312,"height":90,"props":{"fill":"#f1f5f9","cornerRadius":8,"sizingH":"fill"},"parent":{"$ref":"root.id"}}`；返回记为`content` |
| 5. 只修改本次根画板宽度 | `node.set` | `{"id":{"$ref":"root.id"},"props":{"width":640}}` |

检查：实际画板宽640；内容与标题宽592且保留左右24间距；文字未因绝对坐标放大而拉伸。

边界：这是一次指定宽度的布局回归，不能据此承诺任意设备与任意文案都自适应。

## confirmation-dialog：确认弹窗与操作层级

输入：480×280对话框，保留取消与确认两种动作的视觉层级。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"确认弹窗与操作层级"}` |
| 2. 创建ConfirmDialog并保留真实返回ID | `node.create` | `{"type":"frame","name":"ConfirmDialog","x":0,"y":0,"width":480,"height":280,"props":{"fill":"#ffffff","clip":true,"cornerRadius":16}}`；返回记为`root` |
| 3. 创建DialogTitle并保留真实返回ID | `node.create` | `{"type":"text","name":"DialogTitle","x":24,"y":24,"width":432,"height":30,"props":{"fontFamily":"Inter","fontSize":26,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Archive this project?"}`；返回记为`title` |
| 4. 创建DialogBody并保留真实返回ID | `node.create` | `{"type":"text","name":"DialogBody","x":24,"y":80,"width":432,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"You can restore it from the archive."}`；返回记为`body` |
| 5. 创建CancelButton并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"CancelButton","x":180,"y":196,"width":120,"height":48,"props":{"fill":"#f1f5f9","cornerRadius":8},"parent":{"$ref":"root.id"}}`；返回记为`cancel` |
| 6. 创建CancelText并保留真实返回ID | `node.create` | `{"type":"text","name":"CancelText","x":192,"y":208,"width":96,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Cancel"}`；返回记为`cancel_text` |
| 7. 创建ConfirmButton并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"ConfirmButton","x":320,"y":196,"width":136,"height":48,"props":{"fill":"#2563eb","cornerRadius":8},"parent":{"$ref":"root.id"}}`；返回记为`confirm` |
| 8. 创建ConfirmText并保留真实返回ID | `node.create` | `{"type":"text","name":"ConfirmText","x":332,"y":208,"width":112,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#ffffff","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Archive"}`；返回记为`confirm_text` |

检查：标题说明与两个按钮均可编辑；非破坏文案与用户实际动作一致；确认与取消可区分。

边界：此图不执行归档，也不证明实际系统支持恢复；文案必须按产品真实能力调整。

## empty-state-panel：空状态说明与下一步

输入：480×320空状态面板，包含简单矢量占位图标、解释与主按钮。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"空状态说明与下一步"}` |
| 2. 创建EmptyState并保留真实返回ID | `node.create` | `{"type":"frame","name":"EmptyState","x":0,"y":0,"width":480,"height":320,"props":{"fill":"#ffffff","clip":true}}`；返回记为`root` |
| 3. 创建EmptyIcon并保留真实返回ID | `node.create` | `{"type":"vector","name":"EmptyIcon","x":208,"y":34,"width":64,"height":56,"props":{"fill":"#e2e8f0","stroke":"#64748b","strokeWeight":2},"parent":{"$ref":"root.id"},"path":"M 0 12 L 22 12 L 30 0 L 64 0 L 64 56 L 0 56 Z"}`；返回记为`icon` |
| 4. 创建EmptyTitle并保留真实返回ID | `node.create` | `{"type":"text","name":"EmptyTitle","x":60,"y":120,"width":360,"height":30,"props":{"fontFamily":"Inter","fontSize":26,"fill":"#172033","textAutoResize":"height","textAlign":"center"},"parent":{"$ref":"root.id"},"text":"No projects yet"}`；返回记为`title` |
| 5. 创建EmptyDescription并保留真实返回ID | `node.create` | `{"type":"text","name":"EmptyDescription","x":40,"y":166,"width":400,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height","textAlign":"center"},"parent":{"$ref":"root.id"},"text":"Create your first project to get started."}`；返回记为`body` |
| 6. 创建CreateButton并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"CreateButton","x":140,"y":230,"width":200,"height":48,"props":{"fill":"#2563eb","cornerRadius":8},"parent":{"$ref":"root.id"}}`；返回记为`cta` |
| 7. 创建CreateText并保留真实返回ID | `node.create` | `{"type":"text","name":"CreateText","x":152,"y":243,"width":176,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#ffffff","textAutoResize":"height","textAlign":"center"},"parent":{"$ref":"root.id"},"text":"Create project"}`；返回记为`cta_text` |

检查：空状态说明下一步；图标与文字保持独立可编辑；CTA未被长文案挤出面板。

边界：按钮是设计对象而非已连通创建项目功能；真实长文案和语言仍需审阅。

## field-error-state：带明确错误信息的字段状态

输入：420×240表单片段，字段标签、无效输入与可读错误说明。

| 步骤与目的 | 方法 | 参数及返回绑定 |
| --- | --- | --- |
| 1. 仅新建独立文件时初始化 | `file.new` | `{"name":"带明确错误信息的字段状态"}` |
| 2. 创建EmailError并保留真实返回ID | `node.create` | `{"type":"frame","name":"EmailError","x":0,"y":0,"width":420,"height":240,"props":{"fill":"#ffffff","clip":true}}`；返回记为`root` |
| 3. 创建FieldLabel并保留真实返回ID | `node.create` | `{"type":"text","name":"FieldLabel","x":24,"y":24,"width":372,"height":30,"props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Email address"}`；返回记为`label` |
| 4. 创建InvalidEmailField并保留真实返回ID | `node.create` | `{"type":"rectangle","name":"InvalidEmailField","x":24,"y":70,"width":372,"height":52,"props":{"fill":"#ffffff","cornerRadius":8,"stroke":"#b91c1c","strokeWeight":2},"parent":{"$ref":"root.id"}}`；返回记为`field` |
| 5. 创建InvalidValue并保留真实返回ID | `node.create` | `{"type":"text","name":"InvalidValue","x":40,"y":84,"width":340,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#172033","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"not-an-email"}`；返回记为`value` |
| 6. 创建ErrorMessage并保留真实返回ID | `node.create` | `{"type":"text","name":"ErrorMessage","x":24,"y":140,"width":372,"height":30,"props":{"fontFamily":"Inter","fontSize":16,"fill":"#b91c1c","textAutoResize":"height"},"parent":{"$ref":"root.id"},"text":"Enter a valid email address."}`；返回记为`error` |

检查：错误不只依赖红色，还提供文字；字段、标签和错误关系清晰；错误说明保持可编辑。

边界：不是实际校验器，也不证明可访问性程序关联已实现；开发交付仍需label/description语义绑定。


独立CLI执行脚本的JSON回执使用ASCII转义，接收方按JSON解码还原中文路径和文本；不依赖终端默认编码。四个执行器已通过原生Windows的ASCII输出/中文路径专项回归，不将原生文件已生成但打印失败误报为业务失败。
