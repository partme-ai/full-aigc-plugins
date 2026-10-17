# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 用统一尺寸创建代表图形 | `shape.ellipse` | `{"x":8,"y":8,"width":32,"height":32}` |
| 2. 统一颜色 | `paint.setFill` | `{"color":"#243042"}` |
| 3. 实心图标显式去掉继承的描边 | `paint.setStroke` | `{"none":true}` |
| 4. 对齐选中图形 | `object.align` | `{"horizontal":"center","vertical":"center","to":"artboard"}` |
| 5. 等比例缩放并控制描边 | `object.scale` | `{"sx":50,"sy":50,"strokes":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "shape.ellipse", "params": {"x": 8, "y": 8, "width": 32, "height": 32}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

vectorcraft-cli run --in input.vectorcraft --cmd shape.ellipse --params '{"x":10,"y":10,"width":80,"height":60}' --export output.vectorcraft。多个 --cmd/--params 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

在目标像素尺寸检查线宽、端点、负空间与裁切，圆方做视觉补偿。

边界：当前画板尺寸与选择需先核对；只等比例缩放不能自动生成一致图标语言。 本例画板48×48，最终16×16；新建图形继承的描边须明确清除，真实尺寸/描边另按用途核对。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
