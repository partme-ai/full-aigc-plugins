---
name: soundcraft-voice-silence-gaps
description: 当多轨对白需要把长低电平区变成可见片段间隙，同时保持与视频或其他轨道对时关系时使用；按阈值、最短静音和前后保留量逐段核对。
license: Apache-2.0
---

# 保留时轴的静音区处理

1. 先诊断噪声底和最轻语音；-40dB/100ms/10ms/20ms只是合成例子，不是通用播客预设。真实素材先在副本试一个短段。
2. Audacity手册提供阈值与持续时间的判断方法，但其截短会删时间；SoundCraft本流程保持后续语音的位置，适合保留对时。
3. 检查每个新片段的start、length、源offset及有效词首尾；不要只看片段数。多轨音乐或视频应单独确认同步位置。
4. 输出明确原范围，即使最后一段提前结束也保留尾部静音；不要把自动工程末尾当成原素材总时长。

执行前读 [逐步参数](references/craft-steps.json) 和 [调用与检查](references/craft-methods.md)。先读真实输入，所有时长、轨道和片段ID按实际内容替换。已有项目不执行session.new，不覆盖源会话或原音频。

需要内嵌画面时交给 **soundcraft-editor** 技能。独立安装：`npx skills add full-aigc-skills/soundcraft-skills --skill soundcraft-editor`。本批技能随SoundCraft开发预发布提供，真实素材和其他宿主仍需分别验收。

两段有效信号保留原0.5和2.5秒时间位置，前10ms后20ms余量保留；其他轨道不变；按原4秒范围导出后比较有效区及间隙。

此方法创建间隙，不是Audacity Truncate Silence的删时缩短；不用于按停顿自动压缩总时长。阈值以下可能有气声、尾音或音乐，不能当成不存在。它不是降噪或人声识别。

真实素材试听、感知响度标准与宿主画面同步需分别验证，不以片段结构或导出成功代替。[GitHub来源与许可](references/workflow-sources.json)。
