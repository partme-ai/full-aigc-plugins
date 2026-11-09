---
description: 参考生视频（Ref2VA）：参考图/视频/音频驱动的生成
argument-hint: "<生成描述> --reference-image 图1 [--reference-image 图2 ...] [--duration 4-15]"
---

先跑能力预检（`scripts/minimax_video.py check`），未就绪按指引配置。

解析 $ARGUMENTS：生成描述 + 一个或多个 `--reference-image` / `--reference-video` /
`--reference-audio`（与 first/last_frame 互斥，不可混用）。

走 `minimax-video-generation` 技能的 Ref2VA 路径：提示词先经 vendored
`h3-prompt-writing` 的六段式改写（references/ref-en.txt 结构），参考标签
（`<Picture 1>` …）保持一致。确认模型/时长/分辨率组合合法后提交，轮询至终态并下载。
轮询超时 = 续查状态，永不重复提交付费任务。
