# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 确认Quiet/Loud两段边界，示例同轨前两秒比后两秒低6dB | `session.inspect` | `{"detail":"full"}` |
| 2. 在已核实2秒说话人边界分开Voice片段，不移动内容 | `edit.separate` | `{"tracks":["Voice"],"at":{"seconds":2}}` |
| 3. 选择第一段内部0.1至1.9秒，选中第一段而非边界处两个片段 | `edit.select` | `{"tracks":["Voice"],"start":{"seconds":0.1},"end":{"seconds":1.9}}` |
| 4. 把选中较轻片段设为+6dB绝对增益，较响片段保持原样 | `clip.gain` | `{"db":6}` |
| 5. 仅将Voice总轨降低3dB保留输出余量 | `mix.volume` | `{"tracks":["Voice"],"db":-3}` |
| 6. 输出实际四秒24位审核音频 | `file.bounce_mix` | `{"start":{"seconds":0},"end":{"seconds":4},"format":"wav","bit_depth":24,"normalize":false,"dither":false,"path":"output/dialogue-review.wav"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "session.inspect", "params": {"detail": "full"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

`soundcraft-cli run --in input.scraft --cmd '方法ID=JSON' … --save output.scraft`；每个`方法ID=JSON`作为一个独立argv参数。格式转换使用实际`convert --rate`参数。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

切换说话人时响度自然，低声、笑声、停顿没有异常放大。

边界：2秒边界、前段低6dB及0.1至1.9秒选区仅适用于该示例；按实际段落边界与实测差异替换，必要时用inspect返回的精确片段ID。先确认只选中较轻片段，不能按每个说话人统一套6dB。clip.gain是片段增益，不会只修改片段中被时间选区覆盖的采样；LUFS和真实语音自然度另验。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 限定技术回归

Windows原生main [39011827930](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39011827930)通过合成四秒信号核对目标轨道/片段的处理结果、48kHz/24位立体声PCM、源工程保护和保存重开采样保持。参数中的轨道名、段落边界、增益和输出区间均为该输入的示例；真实语音自然度、LUFS标准和内嵌宿主同步未验收。
