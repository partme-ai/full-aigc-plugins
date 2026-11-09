---
description: 纯文生视频（T2VA）：文本直达 H3，必须给 --ratio
argument-hint: "<画面与声音描述> [--ratio 16:9|9:16|1:1] [--duration 4-15] [--resolution 480P|768P|2K]"
---

先跑能力预检（`scripts/minimax_video.py check`），未就绪按指引配置。

解析 $ARGUMENTS：视听描述 + 可选 `--duration` / `--resolution` / `--model` / `--out`。
**纯文本模式必须给 `--ratio`**（T2VA 不能 adaptive，缺省按 16:9 处理并提示用户）。

走 `minimax-video-generation` 技能的 T2VA 路径：提示词先经 vendored
`h3-prompt-writing` 起草完整视听时间线（integrated_multimodal_description →
overall_soundscape → non_diegetic_music）。确认模型/时长/分辨率组合合法后提交，
轮询至终态并下载。轮询超时 = 续查状态，永不重复提交付费任务。
