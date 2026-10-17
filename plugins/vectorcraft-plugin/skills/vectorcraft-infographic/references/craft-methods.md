# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 创建信息区块 | `shape.rectangle` | `{"x":20,"y":20,"width":160,"height":70,"radius":8}` |
| 2. 用明确示例标识代替未经核实的事实声明 | `text.create` | `{"x":28,"y":40,"text":"示例数量","size":16}` |
| 3. 按真实数据建立图表 | `graph.create` | `{"type":"column","x":20,"y":110,"width":240,"height":150,"categories":["A","B"],"series":["数量"],"rows":[[21],[42]]}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "shape.rectangle", "params": {"x": 20, "y": 20, "width": 160, "height": 70, "radius": 8}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

vectorcraft-cli run --in input.vectorcraft --cmd shape.ellipse --params '{"x":10,"y":10,"width":80,"height":60}' --export output.vectorcraft。多个 --cmd/--params 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

图形长度、数值、单位和来源对应，不能为了版面改动数据比例。

边界：示例数字仅用于格式说明；实际数据必须来自用户表或核实来源。 未替换并核实来源前保留示例标识；图表保存重开后先select.set实际图表ID，再graph.setData读取或修改。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
