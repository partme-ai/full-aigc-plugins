# 本场景的 Craft 方法与参数

数值是原创示例，按真实输入、节点和目标替换；capture/$变量只是手册绑定标记，原生CLI不会自动替换。默认创建会改变选择，后续操作必须传真实id/ids。新建步骤仅用于新任务；已有工程另存并保护已有节点。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅新建任务初始化，已有工程不能清空 | `file.new` | `{"name":"Desktop wireframe"}` |
| 2. 创建Desktop，绑定实际返回ID | `node.create` | `{"type":"frame","name":"Desktop","x":0,"y":0,"width":1280,"height":1024,"props":{"fill":"#ffffff","clip":true}}` |
| 3. 创建Navigation，绑定实际返回ID | `node.create` | `{"type":"rectangle","name":"Navigation","x":0,"y":0,"width":240,"height":1024,"parent":"$frame.id","props":{"fill":"#e2e8f0"}}` |
| 4. 创建PageTitle，绑定实际返回ID | `node.create` | `{"type":"text","name":"PageTitle","x":280,"y":40,"width":900,"height":48,"parent":"$frame.id","text":"页面目标","props":{"fontFamily":"Inter","fontSize":30,"fill":"#172033","textAutoResize":"height"}}` |
| 5. 创建ContentCard，绑定实际返回ID | `node.create` | `{"type":"frame","name":"ContentCard","x":280,"y":120,"width":952,"height":300,"parent":"$frame.id","props":{"fill":"#f1f5f9","cornerRadius":12}}` |
| 6. 创建ContentSummary，绑定实际返回ID | `node.create` | `{"type":"text","name":"ContentSummary","x":24,"y":24,"width":904,"height":60,"parent":"$card.id","text":"先展示用户任务、信息层级和主要操作；内容待替换。","props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height"}}` |
| 7. 创建PrimaryAction，绑定实际返回ID | `node.create` | `{"type":"frame","name":"PrimaryAction","x":280,"y":460,"width":240,"height":48,"parent":"$frame.id","props":{"fill":"#2563eb","cornerRadius":8}}` |
| 8. 创建PrimaryActionLabel，绑定实际返回ID | `node.create` | `{"type":"text","name":"PrimaryActionLabel","x":16,"y":12,"width":208,"height":24,"parent":"$action.id","text":"继续","props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","textAlign":"center"}}` |

## 执行方式

先读[实际观察参数](craft-command-evidence.json)并向当前后端查询。每个capture绑定该步真实result；例如node.create返回id后，将$frame.id替换成真实ID。不要猜编号或将$字符串直接传给原生CLI。

宿主内同步编辑使用同一编辑器会话的`run_command`，例如`{"command":"node.get","params":{"id":实际节点ID}}`；编辑器就绪后才能操作。独立CLI每批写JSON数组，如`[{"command":"node.get","params":{"id":2}}]`，以argv运行`figcraft-cli run steps.json --in input.figcraft --out output.figcraft`；用真实输入及返回ID替换示例2。读返回JSONL，核对每行ok及result。分批操作从上一批工程继续，不能启动一个空会话后猜原对象ID。新CLI进程不自动改变已打开编辑器。

[craft-steps.json](craft-steps.json)是参数模板。导出路径须在目标工作区，先检查冲突，保留输入；另存工程后用新进程读取结构和导出图片。

## 检查与边界

1280×1024画板有导航、标题、内容卡和主操作，所有子节点归属正确，文字可编辑。

PNG/SVG导出、布局数字或连线存在不能替代真实设计审阅、原型点击、导入保真及宿主同步验收。

[工作流来源与许可](workflow-sources.json)：只借鉴Figma工作流事实，步骤及参数原创适配。
