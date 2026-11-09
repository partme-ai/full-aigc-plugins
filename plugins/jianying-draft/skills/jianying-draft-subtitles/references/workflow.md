# 字幕工作流参考

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `caption.timeline.inspect` | 字幕 → 我的/时间线 | 草稿路径 | `captions list/get` | 文本、ID、时间和样式 | 只读 |
| `caption.timeline.add` | 字幕 → 新建字幕 | 文本、实测起点/时长、轨道 | `captions add` | cue 精确读回 | `timeline remove` |
| `caption.file.import` | 字幕 → 导入本地字幕 | SRT/ASS 编码、时间基准、offset | `captions import-srt/import-ass` | cue 数、时间、round-trip 导出 | 快照恢复 |
| `caption.content.edit` | 字幕段 → 编辑 | segment ID、文本 | `captions set` | 文案与 ID 不变 | 恢复原文案 |
| `caption.style.apply` | 字幕 → 样式/气泡/动画 | 字体、样式、资源、授权 | `captions style/style-ranges/bubble/animation` | 样式材料、范围和冷重开 | 恢复原样式 |
| `caption.translation.apply` | 字幕 → 翻译 | by_id/by_text 映射或获批 Provider | `captions translate` | ID/时间不变、缺失映射报告 | 恢复原语言文本 |
| `caption.file.export` | 字幕 → 导出 | 输出路径不存在或覆盖已批准 | `captions export-srt/export-ass` | 解析、时间和 round-trip | 删除未接受输出 |
| `caption.timeline.verify` | 字幕 → 检查 | 目标安全区、字体、语言和播放证据要求 | `project verify` + 冷重开/播放 | 换行、安全区、同步和可读性 | 返回局部修订 |

## 执行路由

字幕时间只来自 SRT/ASS、ASR 制品或真实媒体测量。官方字幕样式需要资源预览/下载时，先校验权益和收据，再调用样式命令或版本绑定 Adapter。

## 最小命令面

```text
jianying captions list|get
jianying captions import-srt|import-ass
jianying captions add|set|style|translate
jianying captions export-srt|export-ass
```

具体参数从 `jianying captions <command> --help` 获取。

字幕源尚不存在且允许使用本地 whisper.cpp 时，先交给 **`jianying-draft-narration`** skill 运行
`media transcribe` 并取得经账本验证的 SRT/VTT/JSON 制品，再回到本技能导入。Install:
`npx skills add full-aigc-skills/jianying-skills --skill jianying-draft-narration`。不得把 ASR segment
时间戳直接当作剪映播放验收，也不得在 `media.asr_whisper_cpp` 未 supported 时自动选用它。

## 样式规则

- 同一字幕轨保持字体、描边和基准位置一致。
- 中文可读时长和行长按内容调整，不硬编码为所有项目的统一阈值。
- 平台 UI 安全区属于项目约束；冷重开后目视检查。
- 翻译保持 segment ID 和时间不变，缺失映射要报告而非删除原文。

## 恢复

导入失败时源草稿不变；查看 mutation audit，修正字幕文件后重新创建隔离副本。导出文件已存在时不覆盖，除非批准明确包含该路径。
