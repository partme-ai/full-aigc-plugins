---
description: 通过统一 Rust Runtime Adapter 检查剪映 CLI、技能锁、媒体工具、草稿根和 Runtime Profile
---

运行：

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/harness.mjs" doctor
```

解析单一 JSON 信封，逐项报告 CLI 版本/哈希/capability schema、技能锁摘要、
ffprobe/ffmpeg、草稿根和 Runtime Profile。该命令只读；缺失项只给诊断，
不自动安装、不修改配置、不启动剪映，也不回退到其他引擎。
