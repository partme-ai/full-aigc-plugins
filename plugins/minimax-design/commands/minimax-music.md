---
description: 用 MiniMax 音乐 API 生成歌曲/BGM（走 minimax-music-gen 技能）
argument-hint: "[风格/情绪/歌词或主题] [--out 路径]"
---

按 vendored `minimax-music-gen` 技能生成音乐：先确认参考格式（歌词/情绪/时长），
调 MiniMax 音乐 API，产物写到 --out 指定路径（缺省 outputs/audio/）。
注意 mmx CLI 没有音乐命令，音乐只能走 API。
