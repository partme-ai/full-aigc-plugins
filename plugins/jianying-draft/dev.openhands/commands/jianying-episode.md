---
description: 通过 Rust Job v2 批处理把逐镜成片、解说和字幕装配为剪映草稿
argument-hint: "<episode 目录（含视频、解说和字幕）>"
---

1. 运行统一 Harness doctor，确认 CLI、技能锁、媒体工具和所需 capability。
2. 清点 episode 中的视频、解说、BGM 和字幕；所有素材先经 Runtime Adapter 探测并记录哈希。
3. 生成确定性的 `jianying-job/v2` 或 batch Job：主视频轨按实测时长连续，解说/BGM 分轨，字幕按实测语音时间。
4. 对输出草稿范围建立批准，并仅通过：

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/runtime_adapter.mjs" job run <job.json> --out <draft-dir>
```

5. 保存 task ID，执行结构验证；失败时从最后已验证检查点恢复，不重复已完成的付费或外部操作。
6. 如实区分可编辑草稿、代理预览和原生导出证据。
