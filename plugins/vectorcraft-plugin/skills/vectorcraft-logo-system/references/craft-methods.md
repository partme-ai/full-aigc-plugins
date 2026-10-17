# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 仅独立新标志任务创建空文档；已有工程不能直接重放 | `file.new` | `{"width":240,"height":180,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建不对称L形几何，避免镜像对称矩形产生重叠副本 | `path.create` | `{"d":"M 20 20 L 80 20 L 80 45 L 45 45 L 45 100 L 20 100 Z"}` |
| 3. 设置品牌主色 | `paint.setFill` | `{"color":"#2457cc"}` |
| 4. 几何符号不带继承描边 | `paint.setStroke` | `{"none":true}` |
| 5. 沿明确轴复制另一半，文字不参与镜像 | `object.reflect` | `{"axis":"vertical","origin":[90,60],"copy":true}` |
| 6. 只在本空文档中选择刚创建的两个符号部件 | `select.all` | `{}` |
| 7. 将两半共同编组，保留路径编辑 | `object.group` | `{}` |
| 8. 独立保留活文字；按实际品牌和合法字体替换 | `text.create` | `{"x":20,"y":140,"text":"CRAFT","size":24,"font":"Arial","color":"#2457cc"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "shape.rectangle", "params": {"x": 20, "y": 20, "width": 120, "height": 80, "radius": 12}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

vectorcraft-cli run --in input.vectorcraft --cmd shape.ellipse --params '{"x":10,"y":10,"width":80,"height":60}' --export output.vectorcraft。多个 --cmd/--params 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

检查负空间、小尺寸辨识度、单色与反白版，并保留文字字体信息。

边界：本配方仅独立新标志图。已有工程跳过file.new，按实际返回ID选择两半再编组，不能select.all处理用户其他对象。仅镜像几何，不镜像文字；本例不代替完整品牌设计与商标确认。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
