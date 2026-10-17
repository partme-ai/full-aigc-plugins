# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取实际轨道名/ID，确认配音Voice与音乐Bed分别存在 | `session.inspect` | `{"detail":"full"}` |
| 2. 仅降低音乐Bed，示例-18dB需要按配音与音乐实测重算 | `mix.volume` | `{"tracks":["Bed"],"db":-18}` |
| 3. 明确将配音Voice居中，不沿用音乐轨的当前选择 | `mix.pan` | `{"tracks":["Voice"],"pan":0}` |
| 4. 导出明确四秒的24位审核母版 | `file.bounce_mix` | `{"start":{"seconds":0},"end":{"seconds":4},"format":"wav","bit_depth":24,"normalize":false,"dither":false,"path":"output/voice-mix.wav"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "session.inspect", "params": {"detail": "full"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

`soundcraft-cli run --in input.scraft --cmd '方法ID=JSON' … --save output.scraft`；每个`方法ID=JSON`作为一个独立argv参数。格式转换使用实际`convert --rate`参数。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

单独听人声、音乐和混合结果，讲话期间字句清楚，输出无削波。

边界：Voice/Bed为示例轨道名；先由inspect匹配真实ID/名称，缺失或同名歧义时停止，不能新建同名轨代替用户素材。-18dB是测量起点，不是自动ducking或LUFS标准化；逐句试听音乐是否遮住配音。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 限定技术回归

Windows原生main [39011827930](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39011827930)通过合成四秒信号核对目标轨道/片段的处理结果、48kHz/24位立体声PCM、源工程保护和保存重开采样保持。参数中的轨道名、段落边界、增益和输出区间均为该输入的示例；真实语音自然度、LUFS标准和内嵌宿主同步未验收。
