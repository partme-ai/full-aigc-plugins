---
name: jianying-draft-adjustments
description: "Plan and control JianYing exposure, contrast, color, sharpening, vignette, and related adjustment-panel operations through version-bound semantic adapters with before-and-after evidence."
license: Apache-2.0
---

# JianYing Adjustments

用于剪映“调节”面板，包括曝光、亮度、对比度、饱和度、色温、色调、锐化、暗角和颗粒等参数。当前发布 CLI 没有把这些参数全部提升为稳定草稿原子命令，因此默认先计划和回读能力。

## 什么时候使用

- 修正曝光、白平衡、对比度、饱和度或细节。
- 统一多镜头颜色，或做局部/全局调节。
- 读取、比较、重置和恢复调节参数。

## 能力边界

- ✅ 能做：调节参数计划、能力探测、绝对值写入请求、读回、前后比较和恢复。
- ⚠️ 需要条件：必须精确匹配剪映版本、语义控件和 readback；画面结论要播放。
- ❌ 不该用：不以滤镜替代调节、不猜滑杆刻度、不在只有相对拖动时自动执行。

## 快速开始

可以直接说：“把室内片段色温调暖但保护肤色”“读取当前曝光参数”“重置这个镜头的锐化和暗角”。首次使用加载 [功能动线](references/workflow.md)。
多镜头统一曝光或白平衡时加载 [曝光匹配流程](references/exposure-matching-workflow.md)，把分析建议、人工例外、绝对参数和 readback 分开保存。

## 运行契约

- 触发条件：用户提出调节面板、曝光、色温、对比度、饱和度、锐化、暗角或颗粒操作。
- 所需 capability：`runtime.control_catalog`、`runtime.controls`、`runtime.profile`、`project.edit_isolated`。
- 最低 CLI 版本：`1.6.19`；`runtime.controls` 或具体参数未 supported 时只能输出计划和版本绑定 Adapter 请求。
- 默认风险：`external_native_execution`。
- 输入事实：目标片段/范围、编辑器精确版本、原参数读回、参考画面、允许参数、保护肤色/品牌色规则。
- 确认点：首次调用 GUI Adapter、全片调节、重置已有调节和原生播放分别确认。
- 成功证据：`playback`；参数写入回执仍需前后画面证据。
- 禁止行为：不得用滤镜命令冒充调节，不得猜测滑杆数值、复用其他版本控件映射或在无法回读时连续累加参数。

## 工作流

### Step 1 — 探测控件
`runtime controls list/get` 查找精确版本的调节语义动作和状态回读合同。

### Step 2 — 保存基线
保存应用前参数与画面证据；缺少语义 ID 或 readback 时停止。

### Step 3 — 批准执行
按 [功能动线](references/workflow.md) 生成一次性、绝对值参数请求并获得批准。

### Step 4 — 验证
Adapter 执行后重新读回参数，比较前后代理/原生画面。

### Step 5 — 恢复
验证失败或状态不明时恢复快照，不重复增量操作。

## Rules

- 只接受绝对参数目标和可回读状态。
- 版本、build、语义 ID 任一变化都重新 Canary。
- 先保存原参数和画面基线，再写入。
- 滤镜、调节和 LUT 不可互相冒充。
- 分析 Provider 只能提出建议；没有绝对参数、版本绑定语义 ID 和 readback 时不得批量写入。

## Gotchas

1. **相对拖动不可幂等：** 无绝对值和回读时保持阻断。
2. **版本升级映射漂移：** 每个版本重新验证控件。
3. **曝光修正损坏肤色：** 同时检查亮部、阴影和人物肤色。
4. **批量复制覆盖例外镜头：** 先列出排除片段。
5. **超时后重复调节：** 先读回当前值，避免叠加。

## 安全与数据

调节默认只处理本地草稿和代理帧，不上传视频；远程评估需对精确代理、Provider 和费用另行批准。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
