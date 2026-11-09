---
description: 固定模式整集流水线：镜头表 → 白模提醒 → 逐镜生成 → 实测切点 → 解说后期
argument-hint: "<公有领域经典片名与场面>"
---

执行固定模式起号流水线（每集一条）：

1. **镜头表**：按 `blender-previs` 的 shot-table schema 把指定场面拆成 4~9 镜
   （时长/景别/机位/运镜/切点，整数帧）。
2. **白模**：Blender 白模逐镜渲染**首帧与尾帧 PNG**（占位体+固定配色， LINEAR 插值）。
   不重渲整集视频时可只用首尾帧。
3. **逐镜生成**：每镜走 FL2VA：白模首尾帧 + mmx-cli 版技能的风格 prompt 起草。
   主分支用 `minimax-video-generation`（H3）；备用分支用 volcengine-design 的
   Seedance FL2VA（`scripts/volcengine_ark.py video-submit --first-frame --last-frame`，
   模型 doubao-seedance-1-5-pro）——两供应商可 A/B 对比或按配额切换。先跑单镜
   A/B 验证灰块风格泄漏，再批量。
4. **实测切点**：对拼后的成片跑场景切分（ZCode 端用 video-agent-kit 的 detect_shots；Codex/Kimi 端用 ffmpeg 场景切分等价物）——生成会漂移，**必须实测**，不沿用镜头表。
5. **解说后期**：解说词用 volcengine-design 的 TTS 配音
   （`scripts/volcengine_tts.py`，volcengine-tts-narration），装配与烧录字幕走
   video-factory（episode-slice 的 SRT 已对齐粗剪时间轴 + episode-roughcut，
   QC 按其管线）。video-agent-kit 仅 ZCode 端可用，跨平台一律走前两者。
6. **发布物料**：白模 vs 成片对比图封面 + 标题（钩子三层：标题/正文首句/置顶评论）。

版权红线：只做公有领域经典（1927 大都会 / 1922 诺斯费拉图 / 1902 月里嫦娥 /
1924 福尔摩斯二世 / 1926 将军号 / 1968 不死僵尸 等）；版权期经典禁止逐镜复刻。
