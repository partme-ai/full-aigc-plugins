# 本场景的 Craft 方法与参数

数值是原创示例，按真实输入、节点和目标替换；capture/$变量只是手册绑定标记，原生CLI不会自动替换。默认创建会改变选择，后续操作必须传真实id/ids。新建步骤仅用于新任务；已有工程另存并保护已有节点。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅新建任务初始化，已有工程不能清空 | `file.new` | `{"name":"Developer handoff"}` |
| 2. 创建Handoff，绑定实际返回ID | `node.create` | `{"type":"frame","name":"Handoff","x":0,"y":0,"width":390,"height":884,"props":{"fill":"#ffffff"}}` |
| 3. 创建Heading，绑定实际返回ID | `node.create` | `{"type":"text","name":"Heading","x":24,"y":40,"width":342,"height":36,"parent":"$root.id","text":"交付说明","props":{"fontFamily":"Inter","fontSize":24,"fill":"#172033","textAutoResize":"height"}}` |
| 4. 创建Icon/Primary，绑定实际返回ID | `node.create` | `{"type":"rectangle","name":"Icon/Primary","x":24,"y":120,"width":24,"height":24,"parent":"$root.id","props":{"fill":"#2563eb","cornerRadius":4}}` |
| 5. 指定1倍PNG导出 | `export.add` | `{"ids":["$icon.id"],"setting":{"size":"1x","format":"png"}}` |
| 6. 指定2倍PNG导出 | `export.add` | `{"ids":["$icon.id"],"setting":{"size":"2x","format":"png"}}` |
| 7. 读取真实尺寸、颜色和样式 | `inspect.properties` | `{"id":"$icon.id","colorFormat":"hex"}` |
| 8. 获取该图层CSS作为开发参考 | `inspect.code` | `{"id":"$icon.id","language":"css","unit":"px"}` |
| 9. 发现此画板下可交付资产 | `inspect.assets` | `{"ids":["$root.id"]}` |
| 10. 仅导出明确图标的真实设置 | `file.exportLayers` | `{"ids":["$icon.id"],"dir":"handoff-assets"}` |

## 执行方式

先读[实际观察参数](craft-command-evidence.json)并向当前后端查询。每个capture绑定该步真实result；例如node.create返回id后，将$frame.id替换成真实ID。不要猜编号或将$字符串直接传给原生CLI。

宿主内同步编辑使用同一编辑器会话的`run_command`，例如`{"command":"node.get","params":{"id":实际节点ID}}`；编辑器就绪后才能操作。独立CLI每批写JSON数组，如`[{"command":"node.get","params":{"id":2}}]`，以argv运行`figcraft-cli run steps.json --in input.figcraft --out output.figcraft`；用真实输入及返回ID替换示例2。读返回JSONL，核对每行ok及result。分批操作从上一批工程继续，不能启动一个空会话后猜原对象ID。新CLI进程不自动改变已打开编辑器。

[craft-steps.json](craft-steps.json)是参数模板。导出路径须在目标工作区，先检查冲突，保留输入；另存工程后用新进程读取结构和导出图片。

## 检查与边界

读取真实CSS与属性；明确图标两组导出设置，实际PNG分别24×24和48×48，文件可解码。

PNG/SVG导出、布局数字或连线存在不能替代真实设计审阅、原型点击、导入保真及宿主同步验收。

[工作流来源与许可](workflow-sources.json)：只借鉴Figma工作流事实，步骤及参数原创适配。
