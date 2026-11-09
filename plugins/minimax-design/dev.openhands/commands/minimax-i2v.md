---
description: 图生视频（I2VA）：从首帧向前发展运动
argument-hint: "<运动描述> --first-frame 首帧图 [--duration 4-15] [--resolution 480P|768P|2K]"
---

先跑能力预检（`scripts/minimax_video.py check`），未就绪按指引配置。

解析 $ARGUMENTS：运动描述 + `--first-frame`（**必填**，本地路径或 URL，自动转
data URI）+ 可选 `--duration` / `--resolution` / `--model` / `--out`。

走 `minimax-video-generation` 技能的 I2VA 路径：提示词先经 vendored
`h3-prompt-writing` 起草——**从首帧出发向前发展**，不重述帧里已有的内容。
确认模型/时长/分辨率组合合法后提交，轮询至终态并下载。
轮询超时 = 续查状态，永不重复提交付费任务。

需要控制终点画面时改用 `/minimax-fl2va`（首+尾帧）。
