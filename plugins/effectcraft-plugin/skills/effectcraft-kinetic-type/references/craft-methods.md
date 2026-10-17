# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 建立文字动画合成 | `comp.new` | `{"name":"Type","width":1080,"height":1920,"duration":5,"frameRate":30}` |
| 2. 按语义建立一组可读文案 | `layer.newText` | `{"text":"准确的短文案","name":"Phrase","size":64}` |
| 3. 为当前文本创建首末透明度 | `prop.addKey` | `{"path":"transform/opacity","time":0,"value":0}` |
| 4. 留足可读停留时长 | `prop.addKey` | `{"path":"transform/opacity","time":0.5,"value":100}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "comp.new", "params": {"name": "Type", "width": 1080, "height": 1920, "duration": 5, "frameRate": 30}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

effectcraft-cli run --project input.ecproj prop.set '{"path":"transform/opacity","value":90}' --save-as output.ecproj。多个 id JSON 成对放同一批次；新工程显式 --empty，避免默认demo。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

按真实播放速度检查字词顺序、标点与停留，不只看静止帧。

边界：多个词组分别建层和错开时间，不能同时闪入再称为节奏排版。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
