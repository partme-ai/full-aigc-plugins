---
name: jianying-draft-filters
description: "Search, preview, apply, tune, inspect, remove, and verify JianYing color filters over explicit timeline ranges using released Rust catalogues and reversible edits."
license: Apache-2.0
---

# JianYing Filters

用于剪映“滤镜”能力。滤镜表达整体色彩风格；曝光、色温等单项参数属于调节技能，不能互相冒充。

## 什么时候使用

- 搜索和筛选风格滤镜，预览不同强度。
- 对片段或显式时间范围应用、调整、替换或删除滤镜。
- 验证滤镜在镜头之间的一致性和肤色影响。

## 能力边界

- ✅ 能做：滤镜目录、候选预览、显式范围/强度应用、替换、检查和删除。
- ⚠️ 需要条件：官方滤镜要权益；品牌色/肤色要参考；完成要播放比较。
- ❌ 不该用：不替代曝光/白平衡精调、不默认全片覆盖、不凭缩略图判定最终颜色。

## 快速开始

可以直接说：“给海边镜头找清透滤镜”“把滤镜强度降到 35”“只删除 5–8 秒的复古滤镜”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求滤镜搜索、预览、应用、强度调整、替换或删除。
- 所需 capability：`media.catalogue`、`media.enums`、`timeline.filter`、`media.official_resource_apply`、`timeline.remove`。
- 最低 CLI 版本：`1.6.19`；固定目录滤镜走 Rust 命令，在线资源未获支持时停在 Adapter 门禁。
- 默认风险：`reversible_write`。
- 输入事实：滤镜 slug/resource ID、目标片段或范围、强度、画面风格、肤色/品牌色保护和权益。
- 确认点：下载受限资源、整片应用、覆盖已调色片段和原生播放分别确认。
- 成功证据：`playback`；结构存在不能证明颜色观感。
- 禁止行为：不得用滤镜模拟未支持的曝光/白平衡精调，不得默认全片覆盖或凭缩略图推定最终颜色。

## 工作流

### Step 1 — 筛选候选
根据创作简报、镜头光线和权益筛选滤镜候选。

### Step 2 — 预览
预览候选和强度；官方资源先取得收据。

### Step 3 — 应用
按 [功能动线](references/workflow.md) 在隔离副本显式范围执行。

### Step 4 — 验证
读回滤镜材料、强度和范围，播放比较肤色、品牌色和镜头一致性。

### Step 5 — 恢复
不通过时删除目标 filter 段或恢复快照。

## Rules

- 滤镜和调节分别建模，不互相替代。
- 每次应用绑定 slug、强度和显式范围。
- 选择先满足权益，再比较风格。
- 肤色和品牌色保护优先于“更有氛围”。

## Gotchas

1. **滤镜代替白平衡：** 需要色温/色调时转入调节技能。
2. **默认覆盖整片：** 缺少范围先请求或生成审阅计划。
3. **强度尺度混乱：** 使用 CLI/目录约定尺度，不自行归一化。
4. **镜头光线不同：** 分镜头比较，不盲目统一强度。
5. **只看缩略图：** 最终以播放和参考画面为准。

## 安全与数据

滤镜流程默认本地处理，不上传画面；在线资源只保存资源身份和最小权益证据。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
