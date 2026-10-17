# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取当前可用描摹预设 | `imageTrace.presets` | `{}` |
| 2. 对已选择位图执行描摹 | `imageTrace.make` | `{"preset":"Black and White Logo"}` |
| 3. 核对描摹后转为路径 | `imageTrace.expand` | `{}` |
| 4. 适度减少冗余节点 | `object.path.simplify` | `{"tolerance":0.5,"cornerAngle":30}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "imageTrace.presets", "params": {}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

vectorcraft-cli run --in input.vectorcraft --cmd shape.ellipse --params '{"x":10,"y":10,"width":80,"height":60}' --export output.vectorcraft。多个 --cmd/--params 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

细线、孔洞和轮廓对照原图，不以节点变少代替形状保真。

边界：预设名必须由 imageTrace.presets 实际返回确认；失焦照片不适合精确图纸描摹。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

0.12实际返回的Black and White Logo预设为ignoreWhite:true。本例将白底视为留空，保存后的孔洞与外部区域需检查alpha=0，不能用白色覆盖图形冒充孔洞；若白色本身属于标志内容，须重新选择参数并复核，不能照搬该预设。
