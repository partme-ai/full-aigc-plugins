---
description: MiniMax 文生图（image-01）：支持主体参考与多图批量
argument-hint: "<画面描述> [--aspect-ratio 16:9] [--n 3] [--subject-ref type=character,image=路径] [--out-dir 目录]"
---

按 vendored `minimax-multimodal-toolkit` 技能的 image generate 段执行：

```bash
mmx image generate --prompt "<描述>" [--aspect-ratio 16:9] [--n N] \
  [--subject-ref type=character,image=路径] [--out-dir 目录] --quiet
```

- 模型固定 `image-01`；`--n` 批量出图；`--subject-ref` 做角色一致性参考。
- `--out-dir` 落盘（缺省只回 URL）；产物路径交用户或下游命令。
- mmx 未安装：`npm install -g mmx-cli && mmx auth login --api-key sk-xxx`；
  或已设 `MINIMAX_API_KEY` 时按 toolkit 技能的免登录形态调用。

上游语法以 `minimax-multimodal-toolkit` 技能为准，不虚构 flag。
