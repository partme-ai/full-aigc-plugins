---
description: 生成一段 MiniMax H3 视频（t2v / 图生视频 / 白模首尾帧 FL2VA）
argument-hint: "[画面描述] [--first-frame 首帧图] [--last-frame 尾帧图] [--duration 4-15] [--resolution 480P|768P|2K]"
---

先跑能力预检（`scripts/minimax_video.py check`），未就绪则按指引让用户配置，已就绪再继续。

解析 $ARGUMENTS：画面描述 + 可选 flags（--first-frame / --last-frame / --reference-image / --duration / --resolution / --ratio / --model / --out）。

- 有首帧或首尾帧 → 走 `minimax-video-generation` 技能的 FL2VA 路径，提示词先经 vendored
  `h3-prompt-writing` 的对应结构起草（描述两帧之间的连续运动，时长与请求严格一致）。
- 纯文本 → T2VA 结构起草，提醒文生视频必须给 --ratio（不能 adaptive）。
- 确认模型/时长/分辨率组合合法（H3: 480P/768P/2K 4~15s；H3-Max: 480P/768P 5~15s）后提交，
  轮询至终态并下载到 --out。轮询超时 = 续查状态（query --task-id），永不重复提交付费任务。
