# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 在已导入的屏幕内容层建立区域遮罩 | `layer.addMask` | `{"rect":[100,100,600,350],"shape":"rect"}` |
| 2. 匹配当前层不透明度 | `prop.set` | `{"path":"transform/opacity","value":90}` |
| 3. 根据实际透视逐层检查 | `project.summary` | `{}` |

先通过实际图层ID选择要处理的屏幕内容层，再调用 `layer.addMask` 新建遮罩。`layer.mask.shape` 仅用于改变已有遮罩的形状，没有遮罩时会失败；不能替代创建操作。rect 是图层局部坐标，不是合成坐标。在真实素材有缩放、位移或锚点变化时先换算。

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "layer.mask.shape", "params": {"rect": [100, 100, 600, 350], "shape": "rect"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

effectcraft-cli run --project input.ecproj prop.set '{"path":"transform/opacity","value":90}' --save-as output.ecproj。多个 id JSON 成对放同一批次；新工程显式 --empty，避免默认demo。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

逐关键帧检查边缘漂移、遮挡、反光与亮度，保留原镜头。

边界：矩形蒙版例子仅适合正面屏幕；真实透视需当前transform/角点能力，不能用矩形蒙版冒充自动追踪。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
