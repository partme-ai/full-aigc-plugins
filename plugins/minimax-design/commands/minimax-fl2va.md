---
description: 白模首尾帧专用：FL2VA 锚定生成（起号模式，首尾帧必填）
argument-hint: "<两帧之间的连续运动描述> --first-frame 首帧图 --last-frame 尾帧图 [--duration 4-15] [--resolution 480P|768P|2K]"
---

固定模式起号的锚点命令：白模逐镜渲染出的**首帧与尾帧 PNG**（blender-previs
产物）作两端锚，生成两帧之间的连续运动。**两个帧图都必须提供**——只有首帧请用
`/minimax-i2v`。

先跑能力预检（`scripts/minimax_video.py check`），未就绪按指引配置。

解析 $ARGUMENTS：运动描述 + `--first-frame` + `--last-frame`（必填）+ 可选
`--duration`（4-15s，描述必须与时长严格一致）/ `--resolution` / `--model` / `--out`。

走 `minimax-video-generation` 技能的 FL2VA 路径：提示词先经 vendored
`h3-prompt-writing` 起草——**描述两帧之间的连续路径**，不重复描述帧内容本身。
确认模型/时长/分辨率组合合法（H3: 480P/768P/2K 4~15s；H3-Max: 480P/768P 5~15s）后提交，
轮询至终态并下载到 --out。轮询超时 = 续查状态（query --task-id），永不重复提交付费任务。

批量起号场景：整集流水线走 `/minimax-episode`（含单镜 A/B 验风格泄漏与实测切点）。
