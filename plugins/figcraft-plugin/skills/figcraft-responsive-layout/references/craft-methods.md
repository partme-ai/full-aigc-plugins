# 本场景的 Craft 方法与参数

数值是原创示例，按真实输入、节点和目标替换；capture/$变量只是手册绑定标记，原生CLI不会自动替换。默认创建会改变选择，后续操作必须传真实id/ids。新建步骤仅用于新任务；已有工程另存并保护已有节点。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅新建任务初始化，已有工程不能清空 | `file.new` | `{"name":"Responsive layout"}` |
| 2. 创建Cards，绑定实际返回ID | `node.create` | `{"type":"frame","name":"Cards","x":0,"y":0,"width":768,"height":1024,"props":{"fill":"#ffffff","clip":true,"layout":"vertical","gap":24,"padding":24}}` |
| 3. 创建Heading，绑定实际返回ID | `node.create` | `{"type":"text","name":"Heading","x":0,"y":0,"width":720,"height":60,"parent":"$root.id","text":"根据画板宽度调整的内容标题","props":{"fontFamily":"Inter","fontSize":24,"fill":"#172033","textAutoResize":"height","sizingH":"fill"}}` |
| 4. 创建ContentCard，绑定实际返回ID | `node.create` | `{"type":"frame","name":"ContentCard","x":0,"y":0,"width":720,"height":120,"parent":"$root.id","props":{"fill":"#f1f5f9","cornerRadius":8,"layout":"vertical","padding":16,"gap":16,"sizingH":"fill","sizingV":"hug"}}` |
| 5. 创建Body，绑定实际返回ID | `node.create` | `{"type":"text","name":"Body","x":0,"y":0,"width":688,"height":48,"parent":"$card.id","text":"用真实长文案检查换行；容器尺寸变化不等于产品断点已经实现。","props":{"fontFamily":"Inter","fontSize":18,"fill":"#172033","textAutoResize":"height","sizingH":"fill"}}` |
| 6. 创建PrimaryAction，绑定实际返回ID | `node.create` | `{"type":"frame","name":"PrimaryAction","x":0,"y":0,"width":720,"height":48,"parent":"$root.id","props":{"fill":"#2563eb","cornerRadius":8,"sizingH":"fill","layout":"horizontal","padding":[12,16,12,16],"crossAlign":"center"}}` |
| 7. 创建ButtonLabel，绑定实际返回ID | `node.create` | `{"type":"text","name":"ButtonLabel","x":0,"y":0,"width":688,"height":24,"parent":"$button.id","text":"继续","props":{"fontFamily":"Inter","fontSize":18,"fill":"#ffffff","textAutoResize":"height","sizingH":"fill","textAlign":"center"}}` |
| 8. 实际切换390宽并检查子项 | `node.set` | `{"id":"$root.id","props":{"width":390,"height":884}}` |
| 9. 实际切换768宽并检查子项 | `node.set` | `{"id":"$root.id","props":{"width":768,"height":1024}}` |
| 10. 实际切换1280宽并检查子项 | `node.set` | `{"id":"$root.id","props":{"width":1280,"height":1024}}` |

## 执行方式

先读[实际观察参数](craft-command-evidence.json)并向当前后端查询。每个capture绑定该步真实result；例如node.create返回id后，将$frame.id替换成真实ID。不要猜编号或将$字符串直接传给原生CLI。

宿主内同步编辑使用同一编辑器会话的`run_command`，例如`{"command":"node.get","params":{"id":实际节点ID}}`；编辑器就绪后才能操作。独立CLI每批写JSON数组，如`[{"command":"node.get","params":{"id":2}}]`，以argv运行`figcraft-cli run steps.json --in input.figcraft --out output.figcraft`；用真实输入及返回ID替换示例2。读返回JSONL，核对每行ok及result。分批操作从上一批工程继续，不能启动一个空会话后猜原对象ID。新CLI进程不自动改变已打开编辑器。

[craft-steps.json](craft-steps.json)是参数模板。导出路径须在目标工作区，先检查冲突，保留输入；另存工程后用新进程读取结构和导出图片。

## 检查与边界

依次实际检查390×884、768×1024、1280×1024；标题/卡片/按钮宽度为父宽减48、左内边距24、间距24，无纵向越界；真实文案另查换行。

PNG/SVG导出、布局数字或连线存在不能替代真实设计审阅、原型点击、导入保真及宿主同步验收。

[工作流来源与许可](workflow-sources.json)：只借鉴Figma工作流事实，步骤及参数原创适配。
