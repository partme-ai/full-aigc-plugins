# 本场景的 Craft 方法与参数

数值是原创示例，按真实输入、节点和目标替换；capture/$变量只是手册绑定标记，原生CLI不会自动替换。默认创建会改变选择，后续操作必须传真实id/ids。新建步骤仅用于新任务；已有工程另存并保护已有节点。原型的present请求仅启动界面，不等于用户已点击。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅新建任务初始化，已有工程不能清空 | `file.new` | `{"name":"Clickable prototype"}` |
| 2. 创建Start，绑定实际返回ID | `node.create` | `{"type":"frame","name":"Start","x":0,"y":0,"width":390,"height":884,"props":{"fill":"#ffffff"}}` |
| 3. 创建Result，绑定实际返回ID | `node.create` | `{"type":"frame","name":"Result","x":450,"y":0,"width":390,"height":884,"props":{"fill":"#f1f5f9"}}` |
| 4. 创建StartTitle，绑定实际返回ID | `node.create` | `{"type":"text","name":"StartTitle","x":24,"y":60,"width":342,"height":40,"parent":"$start.id","text":"开始流程","props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"}}` |
| 5. 创建ResultTitle，绑定实际返回ID | `node.create` | `{"type":"text","name":"ResultTitle","x":24,"y":60,"width":342,"height":40,"parent":"$result.id","text":"已到达结果","props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"}}` |
| 6. 创建Continue，绑定实际返回ID | `node.create` | `{"type":"rectangle","name":"Continue","x":24,"y":720,"width":342,"height":48,"parent":"$start.id","props":{"fill":"#2563eb","cornerRadius":8}}` |
| 7. 创建ContinueLabel，绑定实际返回ID | `node.create` | `{"type":"text","name":"ContinueLabel","x":40,"y":732,"width":310,"height":24,"parent":"$start.id","text":"继续","props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","textAlign":"center"}}` |
| 8. 创建Back，绑定实际返回ID | `node.create` | `{"type":"rectangle","name":"Back","x":24,"y":720,"width":342,"height":48,"parent":"$result.id","props":{"fill":"#2563eb","cornerRadius":8}}` |
| 9. 创建BackLabel，绑定实际返回ID | `node.create` | `{"type":"text","name":"BackLabel","x":40,"y":732,"width":310,"height":24,"parent":"$result.id","text":"返回","props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","textAlign":"center"}}` |
| 10. 连接明确的正向目标 | `proto.interaction.add` | `{"id":"$button.id","dest":"$result.id"}` |
| 11. 连接明确的返回目标 | `proto.interaction.add` | `{"id":"$back.id","dest":"$start.id"}` |
| 12. 登记顶层画框流程起点 | `proto.flow.add` | `{"start":"$start.id","name":"Main flow"}` |
| 13. 启动演示；随后必须实际点击正向和返回热点 | `proto.present` | `{"start":"$start.id"}` |

## 执行方式

先读[实际观察参数](craft-command-evidence.json)并向当前后端查询。每个capture绑定该步真实result；例如node.create返回id后，将$frame.id替换成真实ID。不要猜编号或将$字符串直接传给原生CLI。

宿主内同步编辑使用同一编辑器会话的`run_command`，例如`{"command":"node.get","params":{"id":实际节点ID}}`；编辑器就绪后才能操作。独立CLI每批写JSON数组，如`[{"command":"node.get","params":{"id":2}}]`，以argv运行`figcraft-cli run steps.json --in input.figcraft --out output.figcraft`；用真实输入及返回ID替换示例2。读返回JSONL，核对每行ok及result。分批操作从上一批工程继续，不能启动一个空会话后猜原对象ID。新CLI进程不自动改变已打开编辑器。

[craft-steps.json](craft-steps.json)是参数模板。导出路径须在目标工作区，先检查冲突，保留输入；另存工程后用新进程读取结构和导出图片。

## 检查与边界

保存重开保留正向和返回交互及流程起点；必须在实际浏览器演示中点击到结果，再返回起点，才完成交互验收。

PNG/SVG导出、布局数字或连线存在不能替代真实设计审阅、原型点击、导入保真及宿主同步验收。

[工作流来源与许可](workflow-sources.json)：只借鉴Figma工作流事实，步骤及参数原创适配。

## 实际宿主中的动态观察

同一编辑器会话可用`run_command {command:"proto.preview",params:{start:实际起点ID}}`打开跟随修改的浮动预览。通过同一会话node.set修改文字或填色后，核对编辑器与预览同时变化。全屏present的启动成功不能替代点击；实际点击正向及返回热点，看到目标页名与内容才算通过。中文还须实际查看；旧内置Web构建存在中文缺字，不能只根据节点characters正确就交付。
