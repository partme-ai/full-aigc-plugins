---
description: 将需求编译为 jianying-job/v2，并仅通过 Rust Runtime Adapter 生成可编辑剪映草稿
argument-hint: "<需求描述或分镜/素材清单> [草稿名]"
---

1. 用 `node "${CLAUDE_PLUGIN_ROOT}/scripts/harness.mjs" doctor` 完成版本、技能锁和 capability 握手。
2. 通过 Runtime Adapter 调用 `media probe`，固定每个素材的真实时长、流、尺寸、绝对路径与 SHA-256。
3. 只询问会改变剪辑的选择，生成 `jianying-job/v2`；已有草稿必须指定隔离输出。
4. 对写入目标建立任务级批准，然后执行：

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/runtime_adapter.mjs" job run <job.json> --out <draft-dir>
```

5. 使用 Rust CLI 的 `project verify` 和任务审计验证；按请求继续冷重开、播放或原生导出门禁。
6. 报告 CLI task ID、输出路径和实际证据等级。代理预览不能描述为最终 MP4。
