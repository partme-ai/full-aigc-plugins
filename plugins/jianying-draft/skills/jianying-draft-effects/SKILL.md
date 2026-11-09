---
name: jianying-draft-effects
description: "Discover, parameterize, apply, inspect, remove, and recover JianYing scene, character, and audio effects through released Rust catalogues and bounded timeline ranges."
license: Apache-2.0
---

# JianYing Effects

用于剪映“特效”面板中的画面特效、人物特效和音频效果。特效必须绑定明确资源、目标范围和可回滚快照。

## 什么时候使用

- 搜索热门、基础、动感、氛围、光、复古、自然等画面特效。
- 应用人物特效或音频效果，并调节公开参数。
- 检查、替换或删除已有特效。

## 能力边界

- ✅ 能做：场景、人物、音频特效的目录查询、参数化应用、检查、删除和恢复。
- ⚠️ 需要条件：人物特效要适用主体；官方资源要权益；观感和性能要播放验证。
- ❌ 不该用：不猜参数范围、不把滤镜/调节伪装为特效、不越过受保护镜头。

## 快速开始

可以直接说：“给 1–2 秒加电视故障特效”“为人物段加轮廓光”“删掉导致卡顿的全局特效”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求画面、人物或音频特效的查询、添加、参数调整、替换或删除。
- 所需 capability：`media.catalogue`、`media.enums`、`timeline.effect`、`media.sfx`、`media.official_resource_apply`、`timeline.remove`。
- 最低 CLI 版本：`1.6.19`；固定目录特效可直接执行，官方在线特效仍受收据和 Adapter 门禁。
- 默认风险：`reversible_write`。
- 输入事实：特效类别、slug/resource ID、作用对象、起止范围、参数范围、版型、用途和权益。
- 确认点：使用专业/限免资源、覆盖人物外观、写入已有草稿或执行原生播放分别确认。
- 成功证据：`playback`；目录命中或材料存在不能证明观感和性能。
- 禁止行为：不得将人物特效误作普通全局特效、越过受保护片段、猜测参数范围或用全片默认范围掩盖缺失输入。

## 工作流

### Step 1 — 选择类别
从目录选择场景/人物/音频类别，保存候选和参数定义。

### Step 2 — 取得资源
对官方资源先预览、权益校验和下载登记。

### Step 3 — 应用
按 [功能动线](references/workflow.md) 在隔离草稿的显式范围执行。

### Step 4 — 验证
读回材料、轨道和参数，并通过代理/原生播放检查闪烁、主体误识别和卡顿。

### Step 5 — 恢复
不通过时删除单一特效段或恢复快照。

## Rules

- 类别、slug、参数、范围和目标类型必须来自目录与用户计划。
- 没有显式范围时先生成可审阅计划。
- 人物特效不得自动扩展到未授权人物。
- 只报告实际播放和性能证据。

## Gotchas

1. **场景与人物特效混淆：** 先确定 apply target type。
2. **参数刻度猜测：** 只使用目录声明范围并规范化。
3. **全片误应用：** 缺少范围时停止，不默认整片。
4. **资源缓存被当授权：** 缓存存在不证明当前用途允许。
5. **效果成功但播放卡顿：** 结构验证后仍需播放和性能检查。

## 安全与数据

不上传视频或人物数据；需要在线特效分析时必须绑定精确 Provider、素材摘要、用途和授权。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
