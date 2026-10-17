# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取实际轨道、片段和编辑范围，示例四秒/48kHz | `session.inspect` | `{"detail":"full"}` |
| 2. 明确选择Voice四秒片段，不沿用其他轨道的临时选区 | `edit.select` | `{"tracks":["Voice"],"start":{"seconds":0},"end":{"seconds":4}}` |
| 3. 在确认的2秒切口分割Voice，不默认使用当前播放光标 | `edit.separate` | `{"tracks":["Voice"],"at":{"seconds":2}}` |
| 4. 同源连续片段在切口两侧各50ms作互补线性交叉淡化 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":1.95},"end":{"seconds":2.05},"shape":"linear"}` |
| 5. 检查两个片段的源偏移、重叠区、长度与原时轴 | `session.inspect` | `{"detail":"full"}` |
| 6. 输出明确四秒24位PCM审核混音 | `file.bounce_mix` | `{"path":"output/edit-review.wav","format":"wav","bit_depth":24,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "session.inspect", "params": {"detail": "full"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

`soundcraft-cli run --in input.scraft --cmd '方法ID=JSON' … --save output.scraft`；每个`方法ID=JSON`作为独立argv参数，不拼接未转义的shell字符串。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

核对段落顺序、时长、首尾词与点击声，保存会话后重开。

边界：本例是同源连续音频在2秒分割，利用源余量在1.95至2.05秒重叠，采用互补linear避免相关信号等功率叠加增益；不将它原样用于两个不同录次。切口位置、可用源余量和100ms时长均需现场核实。余量不足时不假定已形成完整交叉淡化，先看实际片段源偏移/重叠，再听接缝；不为凑重叠移动已确认的时轴。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 限定技术回归

Windows main专项 [39012439447](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39012439447)与稳定版13应用矩阵 [39012427784](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39012427784)通过。合成信号核对本场景实际采样、原生片段/混音结构、四秒48kHz24位立体声PCM及保存重开；音频剪辑为同源连续素材的互补线性交叉淡化，音乐样例无共享总线效果。真实素材试听、感知响度标准和内嵌宿主同步未验收，不把方法目录查询当成实际效果处理。
