---
name: jianying-draft-digital-human
description: "Select, authorize, preview, submit, resume, verify, and apply JianYing stock or custom digital humans with portrait, voice, upload, provider, budget, and evidence gates."
license: Apache-2.0
---

# JianYing Digital Human

用于剪映“数字人”面板。库存数字人和自定义真人素材使用不同授权路径；任何上传、声音克隆或付费生成都必须精确批准。

## 什么时候使用

- 选择数字人形象、声音、脚本、背景和类别。
- 使用库存数字人，或经授权上传照片、视频、声音创建自定义数字人。
- 预览、提交、查询、恢复、验证并将产物加入草稿。

## 能力边界

- ✅ 能做：库存筛选、请求/预览计划、授权门禁、幂等任务、费用和产物验证。
- ⚠️ 需要条件：自定义真人要肖像/声音权和上传批准；付费 Provider 要预算与握手。
- ❌ 不该用：不克隆未授权声音、不上传无关文件、不把 queued/succeeded 当最终成片验收。

## 快速开始

可以直接说：“选一个职业女主播和普通话女声做预览”“使用这张已授权照片创建数字人，费用不超过 5 元”“继续查询上次的任务，不要重提”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求数字人、AI 主播、数字分身、声音选择/克隆或数字人口播。
- 所需 capability：`runtime.entitlement_verify`、`runtime.control_catalog`、`runtime.controls`、`media.tts_provider`、`render.native_task`。
- 最低 CLI 版本：`1.6.19`；远程 Provider、上传、费用或原生任务 capability 未获真实握手时保持关闭。
- 默认风险：`external_native_execution`。
- 输入事实：形象/声音资源、脚本摘要、背景、用途、Provider、权益、肖像/声音授权、上传范围、预算和有效期。
- 确认点：真人素材上传、声音克隆、付费提交、重试和应用到草稿分别使用独立批准。
- 成功证据：`native_export`；任务 queued/succeeded 或产物文件存在均不足以替代身份、音画和原生导出验收。
- 禁止行为：不得以专业版订阅替代肖像/声音权，不得上传未批准素材、记录秘密、静默重提 ambiguous 请求或复用不匹配批准。

## 工作流

### Step 1 — 检索与授权
检索库存目录并保存候选、筛选理由与资源权益；自定义来源先验证授权。

### Step 2 — 构造预览
构造稳定请求摘要和 [功能动线](references/workflow.md) 中的预览计划。

### Step 3 — 批准提交
用户审阅形象、声音、脚本、背景、费用和上传范围后再提交。

### Step 4 — 查询恢复
使用稳定 request/task ID 查询或恢复；不确定状态不新建请求。

### Step 5 — 验证应用
验证产物身份、时长、音画同步和费用回执，应用到隔离草稿后完成冷重开、播放与所需原生导出。

## Rules

- 肖像权、声音权、上传和费用分别批准。
- 请求 ID 由稳定摘要产生，同一请求不得静默重提。
- 凭据只引用环境变量名，不进入任务正文。
- 最终交付证据必须达到用户要求的播放/原生导出等级。

## Gotchas

1. **专业版被当授权：** 订阅不替代肖像和声音权。
2. **预览脚本与提交脚本漂移：** digest 改变必须重新批准。
3. **超时后再次计费：** 先用 task ID 查询供应商状态。
4. **库存声音用途不明：** 核对渠道和商业用途。
5. **产物存在就宣称完成：** 仍需身份、音画、账单和剪映验收。

## 安全与数据

真人照片、视频和声音属于敏感素材；默认不上传、不共享、不长期保留。只有精确批准后才发送到指定 Provider，并保存最小摘要与审计信息。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
