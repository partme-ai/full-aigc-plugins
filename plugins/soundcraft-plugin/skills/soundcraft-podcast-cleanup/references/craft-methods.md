# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取实际轨道、片段和编辑范围，示例四秒/48kHz | `session.inspect` | `{"detail":"full"}` |
| 2. 明确选择Voice四秒片段，不沿用其他轨道的临时选区 | `edit.select` | `{"tracks":["Voice"],"start":{"seconds":0},"end":{"seconds":4}}` |
| 3. 对本次选中人声片段设置-3dB增益保留余量 | `clip.gain` | `{"db":-3}` |
| 4. 仅在人声头部100ms做等功率淡入 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":0},"end":{"seconds":0.1},"shape":"equal power"}` |
| 5. 仅在人声尾部100ms做等功率淡出 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":3.9},"end":{"seconds":4},"shape":"equal power"}` |
| 6. 读取真实效果目录；仅查询不代表已做均衡或降噪 | `engine.plugins` | `{}` |
| 7. 输出明确四秒24位PCM审核混音 | `file.bounce_mix` | `{"path":"output/podcast-review.wav","format":"wav","bit_depth":24,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "session.inspect", "params": {"detail": "full"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

`soundcraft-cli run --in input.scraft --cmd '方法ID=JSON' … --save output.scraft`；每个`方法ID=JSON`作为独立argv参数，不拼接未转义的shell字符串。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

整段试听切口、呼吸声、尾音和电平，保留原轨。

边界：Voice、四秒范围、100ms和-3dB仅为示例；先核实真实首辅音、尾音和边界，不能把有效语音吞进淡变。示例只完成增益与边缘淡变：engine.plugins仅列出目录，没有执行EQ、压缩或降噪；必须找到真实处理方法并验证后才能声称已做该处理。错误语句、呼吸与内容连贯仍需按真实素材逐段试听，不能用门限器冒充频谱降噪。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 限定技术回归

Windows main专项 [39012439447](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39012439447)与稳定版13应用矩阵 [39012427784](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39012427784)通过。合成信号核对本场景实际采样、原生片段/混音结构、四秒48kHz24位立体声PCM及保存重开；音频剪辑为同源连续素材的互补线性交叉淡化，音乐样例无共享总线效果。真实素材试听、感知响度标准和内嵌宿主同步未验收，不把方法目录查询当成实际效果处理。
