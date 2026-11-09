---
description: MiniMax 语音合成（speech-2.8-hd）：解说/配音/多语种
argument-hint: "<文本或 --text-file 路径> [--voice 音色ID] [--out 路径] [--language zh]"
---

按 vendored `minimax-multimodal-toolkit` 技能的 speech synthesize 段执行：

```bash
mmx speech synthesize --text "<文本>" [--voice 音色ID] [--language zh] \
  [--speed N] [--format mp3] --out 路径 --quiet
```

- 默认模型 `speech-2.8-hd`，单次上限 10k 字符；长文本按段拆分后拼接。
- 起号解说场景：`--subtitles` 可带回字幕时间轴；中文加 `--language zh`。
- `--out` 必填落盘（缺省只回流）；产物交后期命令（/minimax-episode 第 5 步）。
- mmx 未安装：`npm install -g mmx-cli && mmx auth login --api-key sk-xxx`。

上游语法以 `minimax-multimodal-toolkit` 技能为准，不虚构 flag。
