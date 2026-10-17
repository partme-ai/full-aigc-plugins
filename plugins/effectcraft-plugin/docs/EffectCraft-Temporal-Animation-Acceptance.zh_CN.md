# EffectCraft 动画时序验收

固定插件 dev.7／技能源 dev.6／原生 CLI 0.2.0。安装后的动画技能单独复制到 `.agents/skills`，使用空运行目录默认公开安装；没有离线归档覆盖。

320×180、12 fps、一秒品牌片头，为徽标添加 0 秒／0、0.5 秒／100 的透明度关键帧。重开的原生关键帧记录一致；0、0.25、0.5、0.75 秒 RGBA 透明度为 0、128、255、255。现有 ffmpeg 解码全部 12 帧 H.264，核对徽标亮度递增和视频时序。

NOVA 改为 NOVA PLUS 后，整个徽标图层与标题透明度属性保持不变。文字变长会覆盖新的像素，因此在两版文字范围外的 (45,75) 核对原动画，H.264 RGB 容差为 3。隐藏文字的首帧一致，可见标题帧发生变化；原交付全部文件与 13 项安装技能摘要不变。

真实 1 项通过，用时 9.398 秒。技能源回归 24 项通过、17 项跳过；插件回归 4 项通过。[证据](evidence/codex-effectcraft7-temporal-animation-first-use-20261006.json)。复现时设置 `CRAFT_TEMPORAL_FIRST_USE=1`、实际安装动画技能目录 `CRAFT_INSTALLED_ANIMATION_SKILL`，可选新证据文件 `CRAFT_TEMPORAL_EVIDENCE`；在独立技能源仓使用已有 Pillow／ffmpeg 执行 `python3 -B -m unittest discover -s tests -p test_animation_temporal_first_use.py`。

未证明动画透明视频、所有插值方式、GUI／模型派发或创作验收。原有完整 OpenSpec 任务保持开放，只完成有界时序验证任务。
