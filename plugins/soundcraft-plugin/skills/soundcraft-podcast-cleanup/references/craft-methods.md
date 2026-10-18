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

## 用实际片段参数生成配方

读取本技能 `scripts/podcast_input.py`，输入 JSON 必须含 track、startSeconds、endSeconds、fadeInSeconds、fadeOutSeconds、gainDb、output。例如轨道“访谈 主轨”、范围12到42秒、头部0.02秒、尾部0.05秒、增益-2.5dB、output为“审核/访谈.wav”。运行 `python podcast_input.py --input input.json --output recipe.json`；脚本只生成参数，不执行编辑，已有配方输出会拒绝覆盖。

先用 session.inspect 确认此范围恰好对应一个独立片段。clip.gain 修改选中的整片段，不是仅处理时间选区；范围跨越多个片段时先明确选择和拆分方案，不能直接套用。淡变时间采用会话绝对秒；零长度不创建淡变，重叠淡变拒绝。生成后读取 steps，MCP逐项调用execute(command,params)，或把每项编码为独立CLI argv `--cmd`、`方法ID=JSON`，保持同一进程；不能将配方文件直接当作CLI原生脚本。

实际输出目录由任务创建并确认文件尚不存在；助手不会替混音器防止覆盖既有WAV。先保存新工程，回读片段/淡变与输出采样长度，再试听辅音、换气与尾音。混音输出包括会话中未静音的其他轨道，需根据任务明确混音状态。此流程不裁掉范围外内容，也没有降噪、均衡、压缩或LUFS归一化。新参数配方移除四秒旧夹具的验收记录，不能继承其通过结论。
