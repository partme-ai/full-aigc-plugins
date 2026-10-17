# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 创建人物条合成 | `comp.new` | `{"name":"LowerThird","width":1920,"height":1080,"frameRate":25,"duration":6}` |
| 2. 建立姓名文本 | `layer.newText` | `{"text":"真实姓名","name":"Name","position":[180,880],"size":48}` |
| 3. 建立职位文本 | `layer.newText` | `{"text":"真实职位","name":"Role","position":[180,940],"size":28}` |
| 4. 核对图层与文本 | `project.summary` | `{}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "comp.new", "params": {"name": "LowerThird", "width": 1920, "height": 1080, "frameRate": 25, "duration": 6}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

effectcraft-cli run --project input.ecproj prop.set '{"path":"transform/opacity","value":90}' --save-as output.ecproj。多个 id JSON 成对放同一批次；新工程显式 --empty，避免默认demo。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

最长姓名、职位、安全区与透明背景正确，入退场时文字不截断。

边界：以实际文本与返回层ID布局；姓名职位不能凭空补全。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
