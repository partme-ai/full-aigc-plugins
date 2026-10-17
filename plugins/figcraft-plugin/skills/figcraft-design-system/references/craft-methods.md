# 本场景的 Craft 方法与参数

数值是原创示例，按真实输入、节点和目标替换；capture/$变量只是手册绑定标记，原生CLI不会自动替换。默认创建会改变选择，后续操作必须传真实id/ids。新建步骤仅用于新任务；已有工程另存并保护已有节点。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅新建任务初始化，已有工程不能清空 | `file.new` | `{"name":"Component library"}` |
| 2. 创建Button/Primary，绑定实际返回ID | `node.create` | `{"type":"frame","name":"Button/Primary","x":0,"y":0,"width":240,"height":48,"props":{"fill":"#2563eb","layout":"horizontal","padding":[12,16,12,16],"crossAlign":"center","gap":8,"cornerRadius":8}}` |
| 3. 创建Label，绑定实际返回ID | `node.create` | `{"type":"text","name":"Label","x":0,"y":0,"width":208,"height":24,"parent":"$root.id","text":"Continue","props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","sizingH":"fill","textAlign":"center"}}` |
| 4. 明确组件底稿ID，不依赖当前文字选择 | `component.create` | `{"ids":["$root.id"]}` |
| 5. 给文字建立可覆盖属性 | `component.addProperty` | `{"id":"$root.id","name":"Label","type":"text","default":"Continue","layer":"$label.id"}` |
| 6. 创建真实关联实例 | `instance.create` | `{"component":"$root.id","x":280,"y":0}` |
| 7. 只覆盖实例文字 | `instance.setProperties` | `{"ids":["$instance.id"],"properties":{"Label":"Proceed"}}` |
| 8. 检查主组件注册 | `component.list` | `{}` |
| 9. 检查实例可暴露属性 | `component.properties` | `{"id":"$instance.id"}` |

## 执行方式

先读[实际观察参数](craft-command-evidence.json)并向当前后端查询。每个capture绑定该步真实result；例如node.create返回id后，将$frame.id替换成真实ID。不要猜编号或将$字符串直接传给原生CLI。

宿主内同步编辑使用同一编辑器会话的`run_command`，例如`{"command":"node.get","params":{"id":实际节点ID}}`；编辑器就绪后才能操作。独立CLI每批写JSON数组，如`[{"command":"node.get","params":{"id":2}}]`，以argv运行`figcraft-cli run steps.json --in input.figcraft --out output.figcraft`；用真实输入及返回ID替换示例2。读返回JSONL，核对每行ok及result。分批操作从上一批工程继续，不能启动一个空会话后猜原对象ID。新CLI进程不自动改变已打开编辑器。

[craft-steps.json](craft-steps.json)是参数模板。导出路径须在目标工作区，先检查冲突，保留输入；另存工程后用新进程读取结构和导出图片。

## 检查与边界

存在主组件和真实关联实例；实例Label为Proceed、主文字仍Continue；调整主宽度后实例尺寸跟随且文字覆盖保留。

PNG/SVG导出、布局数字或连线存在不能替代真实设计审阅、原型点击、导入保真及宿主同步验收。

[工作流来源与许可](workflow-sources.json)：只借鉴Figma工作流事实，步骤及参数原创适配。
