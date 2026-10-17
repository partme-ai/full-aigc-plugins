# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取实际轨道、片段和编辑范围，示例四秒/48kHz | `session.inspect` | `{"detail":"full"}` |
| 2. 仅将主旋律Lead调整至示例-6dB | `mix.volume` | `{"tracks":["Lead"],"db":-6}` |
| 3. 仅将主旋律略偏左，保持Bed声像独立 | `mix.pan` | `{"tracks":["Lead"],"pan":-0.2}` |
| 4. 仅将背景Bed调整至示例-12dB | `mix.volume` | `{"tracks":["Bed"],"db":-12}` |
| 5. 背景保持中央，不沿用Lead当前对象 | `mix.pan` | `{"tracks":["Bed"],"pan":0}` |
| 6. 输出明确四秒24位PCM审核混音 | `file.bounce_mix` | `{"path":"output/music-review.wav","format":"wav","bit_depth":24,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |
| 7. 导出当前全部启用且未静音轨的同起点同长度24位stems | `file.bounce_stems` | `{"dir":"output/stems","format":"wav","bit_depth":24,"start":{"seconds":0},"end":{"seconds":4}}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "session.inspect", "params": {"detail": "full"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

`soundcraft-cli run --in input.scraft --cmd '方法ID=JSON' … --save output.scraft`；每个`方法ID=JSON`作为独立argv参数，不拼接未转义的shell字符串。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

单声道核对主旋律与低频，分轨长度、起点和采样率一致。

边界：Lead/Bed是示例角色名，按inspect解析实际唯一轨道，-6/-12dB与声像按素材测量重算。本方法导出所有启用且未静音的音频/乐器/MIDI轨，不是仅选中轨；交付前列清单，不能把其他轨意外打包或自动静音用户轨。stems保留单轨混音处理，不是原始干声备份；共享总线效果、发送或压缩存在时，各stem相加不一定等于全混音，需要另验。示例无插入/发送/共享效果，才能以两stem相加核对混音。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 限定技术回归

Windows main专项 [39012439447](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39012439447)与稳定版13应用矩阵 [39012427784](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39012427784)通过。合成信号核对本场景实际采样、原生片段/混音结构、四秒48kHz24位立体声PCM及保存重开；音频剪辑为同源连续素材的互补线性交叉淡化，音乐样例无共享总线效果。真实素材试听、感知响度标准和内嵌宿主同步未验收，不把方法目录查询当成实际效果处理。
