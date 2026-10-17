---
name: soundcraft-finite-audio-loop
description: 当提示音、节拍或已检查接缝的短音效需要精确重复到目标总次数，并在后续解除循环继续编辑时使用；核对总次数、采样长度和接缝。
license: Apache-2.0
---

# 有限次重复音效与展开

1. 核对原片段起点、length及源offset。先在短区域试听头尾接缝；有突跳先修剪到合适边界或另用实际淡化方法，不能把重复称为无缝循环。
2. 用目标总份数填count；本例1秒素材总3份得到3秒，不是4秒。其他采样率和非整数秒按实际采样长度重算。
3. 需要继续独立编辑时，对该组原片段ID调用clip.unloop {clips:[实际ID],mode:"flatten"}；核对3份loop_id均为空、音频不变。
4. 只保留第一份时在副本使用mode:"remove"并核对只余原1秒。已观察0.7.0此时原片段可能仍保留loop_id，不把此字段为空作为已验证事实。

执行前读 [逐步参数](references/craft-steps.json) 和 [调用与检查](references/craft-methods.md)。先读真实输入，所有时长、轨道和片段ID按实际内容替换。已有项目不执行session.new，不覆盖源会话或原音频。

需要内嵌画面时交给 **soundcraft-editor** 技能。独立安装：`npx skills add full-aigc-skills/soundcraft-skills --skill soundcraft-editor`。本批技能随SoundCraft开发预发布提供，真实素材和其他宿主仍需分别验收。

输入1秒/48000采样的片段变为总3份，start为0/48000/96000，长度各48000；输出3秒无缺口，保存重开采样一致；flatten可展开为3个普通片段。

SoundCraft count=3含原片段；Audacity Number of repeats to add=3则额外加3份，两者不能照抄。循环不自动保证无爆音或节奏对齐；不为凑时长改变用户已确认素材速度。

真实素材试听、感知响度标准与宿主画面同步需分别验证，不以片段结构或导出成功代替。[GitHub来源与许可](references/workflow-sources.json)。
