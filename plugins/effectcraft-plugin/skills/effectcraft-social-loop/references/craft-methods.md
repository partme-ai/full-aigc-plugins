# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 建立短循环合成 | `comp.new` | `{"name":"Loop","width":1080,"height":1080,"duration":3,"frameRate":30}` |
| 2. 建立可循环运动的图形 | `layer.newShape` | `{"kind":"ellipse","name":"Dot","size":[80,80],"fill":"#2457cc"}` |
| 3. 起点关键帧 | `prop.addKey` | `{"path":"transform/position","time":0,"value":[200,540]}` |
| 4. 中点关键帧 | `prop.addKey` | `{"path":"transform/position","time":1.5,"value":[880,540]}` |
| 5. 终点恢复起点 | `prop.addKey` | `{"path":"transform/position","time":3,"value":[200,540]}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "comp.new", "params": {"name": "Loop", "width": 1080, "height": 1080, "duration": 3, "frameRate": 30}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

effectcraft-cli run --project input.ecproj prop.set '{"path":"transform/opacity","value":90}' --save-as output.ecproj。多个 id JSON 成对放同一批次；新工程显式 --empty，避免默认demo。

在时长为3秒、30fps的例子中，3.0秒是关键帧端点，不是有效输出帧；最后一张有效帧为2.966667秒。用 `get Loop Dot transform/position --time 3 --project output.ecproj --json` 核对端点，但渲染/播放只检查 `[0,3)`。首尾位置相同也不能证明速度连续，本例线性往返会在折返点改变运动方向；无缝且平滑的需求须另行调整缓动或运动曲线。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

连续循环看接缝，检查首尾位置和速度，必要时调缓动。

边界：首尾位置一致不证明速度连续；导出应避免重复计入终点帧。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
