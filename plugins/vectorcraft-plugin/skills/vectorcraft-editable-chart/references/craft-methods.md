# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 创建有数据模型的图表 | `graph.create` | `{"type":"bar","x":20,"y":20,"width":320,"height":200,"categories":["A","B"],"series":["收入"],"rows":[[21],[42]]}` |
| 2. 修改图表类型保持数据 | `graph.setType` | `{"type":"column","legend":true}` |
| 3. 读取当前数据做核对 | `graph.setData` | `{}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "graph.create", "params": {"type": "bar", "x": 20, "y": 20, "width": 320, "height": 200, "categories": ["A", "B"], "series": ["收入"], "rows": [[21], [42]]}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

vectorcraft-cli run --in input.vectorcraft --cmd shape.ellipse --params '{"x":10,"y":10,"width":80,"height":60}' --export output.vectorcraft。多个 --cmd/--params 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

核对类别顺序、缺失值、单位、轴范围；保留可编辑graph对象。

边界：不要先转曲或解组图表；graph.setData 空参只查询当前选中图表。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

保存重开后，先调用 `select.set {"ids":[实际图表ID]}`，再 `graph.setData {"id":实际图表ID}`。当前0.12即使传id也仍检查选择状态，未选择会报nothing selected。图表在inspect中可表现为Group；是否有数据模型必须用graph.setData读取验证，不能只看对象类型或柱形外观。
