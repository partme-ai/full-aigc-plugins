---
name: soundcraft-scenario-playbooks
description: 使用 SoundCraft 处理配音电平、切口淡变、采访引用、分轨交付、倒放音效、去直流或极性诊断时使用；按场景查询具体CLI/MCP参数和检查。
license: Apache-2.0
---

# SoundCraft 场景操作手册

从[8条具体流程](references/workflows.md)选择当前任务。详细步骤与参数在[recipes.json](references/recipes.json)，实际方法观察在[命令证据](references/command-evidence.json)，[GitHub来源](references/sources.json)记录工作流事实与许可，正文与例子为原创适配，不复制外部脚本。

## 同会话与独立CLI

已打开内嵌编辑器时使用该MCP会话，等editor_status就绪，读取宿主schema后调用 `execute {"command":"方法ID","params":{…}}`；不对另一个文件运行CLI后声称画面同步。每步按当前输入和返回对象选择执行，保存源工程与导出文件并重新打开检查。

CLI：`soundcraft-cli run --cmd <方法ID=JSON> … --save output.scraft`，每个id=JSON为一个argv参数。原文件先用 `soundcraft-cli info input.wav` 测量。每条默认新建48kHz空会话；在已有工程执行时跳过newDocumentOnly初始化，先inspect、按实际轨道/片段ID选择，不能导入示例Voice覆盖真实选择。保存后以新进程 `run --in output.scraft --cmd session.inspect={}` 核对，并重新bounce检查效果。`session.audio_health`只检查引用，不分析底噪、削波或响度。

AudioSuite normalize的目标参数为`target_db`；反转极性为`invert`，时间倒放为`reverse`，两者不是同一操作。数字position默认样本，使用`{seconds:…}`可显式表示秒。

## 执行边界

每条例子是独立任务。初始化、新导入和示例set不能无条件用于既有工程。输出路径使用新名称，原始文件保持不变。真实内容必须整段试听，确认无失真、吞字与意外静音。结构化assertions仅适用于嵌入的合成输入，不替代真实素材效果验收。

## 技能商店场景经验

遇到先处理切口再做全局音量、播客章节对应真实音频、保留独立人声与背景素材时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。

## 对时静音与有限循环

保留对白与视频对时关系、把低电平段变为间隙时，交给 **soundcraft-voice-silence-gaps** 技能。独立安装：`npx skills add full-aigc-skills/soundcraft-skills --skill soundcraft-voice-silence-gaps`。

提示音或已核查接缝的音效需精确总次数、后续展开编辑时，交给 **soundcraft-finite-audio-loop** 技能。独立安装：`npx skills add full-aigc-skills/soundcraft-skills --skill soundcraft-finite-audio-loop`。本批随配套插件开发预发布提供；真实素材试听与宿主同步尚未验收。
