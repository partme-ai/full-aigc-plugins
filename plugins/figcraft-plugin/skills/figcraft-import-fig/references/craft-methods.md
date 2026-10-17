# 本场景的 Craft 方法与参数

数值是原创示例，按真实输入、节点和目标替换；capture/$变量只是手册绑定标记，原生CLI不会自动替换。默认创建会改变选择，后续操作必须传真实id/ids。新建步骤仅用于新任务；已有工程另存并保护已有节点。导入是best effort；变量sidecar按实际schema传入；保真或warnings异常需明确报告。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 在独立文档中导入实际Figma文件，保留warnings | `file.open` | `{"path":"input/design.fig"}` |
| 2. 检查导入后真实组件清单 | `component.list` | `{}` |
| 3. 另存SVG用于检查，不覆盖输入 | `file.exportSvg` | `{"path":"import-proof.svg"}` |

## 执行方式

先读[实际观察参数](craft-command-evidence.json)并向当前后端查询。每个capture绑定该步真实result；例如node.create返回id后，将$frame.id替换成真实ID。不要猜编号或将$字符串直接传给原生CLI。

宿主内同步编辑使用同一编辑器会话的`run_command`，例如`{"command":"node.get","params":{"id":实际节点ID}}`；编辑器就绪后才能操作。独立CLI每批写JSON数组，如`[{"command":"node.get","params":{"id":2}}]`，以argv运行`figcraft-cli run steps.json --in input.figcraft --out output.figcraft`；用真实输入及返回ID替换示例2。读返回JSONL，核对每行ok及result。分批操作从上一批工程继续，不能启动一个空会话后猜原对象ID。新CLI进程不自动改变已打开编辑器。

[craft-steps.json](craft-steps.json)是参数模板。导出路径须在目标工作区，先检查冲突，保留输入；另存工程后用新进程读取结构和导出图片。

## 检查与边界

用实际二进制.fig导入，记录warnings，保留输入，检查节点类型、名称、圆角及导出；单一样本通过不代表完整Figma保真。

PNG/SVG导出、布局数字或连线存在不能替代真实设计审阅、原型点击、导入保真及宿主同步验收。

[工作流来源与许可](workflow-sources.json)：只借鉴Figma工作流事实，步骤及参数原创适配。

## 按实际几何核对导入

真实corners.fig样例中，名为rect的节点实际是矢量，其四角保存在network.vertices；不能把通用corners字段当成矢量实际几何。独立画框则核对corners.radii。未打补丁的固定main d1d8c3f原始CLI保留了本样例的矢量顶点及画框圆角。此前通用字段检查导致误报，未采用额外运行时补丁。warnings为空仍不能代表其他文件都保真；按真实原稿逐项检查文字、蒙版、颜色、变量与几何，不根据图层名称猜数值。
