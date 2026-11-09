---
name: jianying-draft-smart-package
description: "Preview, decompose, approve, apply, verify, and recover JianYing smart packaging and smart B-Roll proposals while protecting dialogue, brands, locked shots, budget, and user intent."
license: Apache-2.0
---

# JianYing Smart Package

用于剪映“智能包装”和“智能 B-Roll”。它们是组合工作流，不是一个可盲点的一键按钮；必须先把提案拆成可审阅变更集。

## 什么时候使用

- 选择智能推荐、科技风、生活 Vlog、营销带货、知识分享或综艺娱乐包装。
- 请求 AI 自动补 B-Roll、字幕、花字、音效、特效或转场。
- 审阅、批准、局部返工、停止或恢复智能包装任务。

## 能力边界

- ✅ 能做：风格路由、预览请求、提案拆解、保护规则、批准、应用、评审和恢复。
- ⚠️ 需要条件：必须有版本绑定 Adapter、预算、允许轨道和应用前快照。
- ❌ 不该用：不接受不可解释变更、不删除受保护内容、不把 GUI 提示当质量通过。

## 快速开始

可以直接说：“预览生活 Vlog 智能包装但不要改对白”“把提案拆成 B-Roll 和字幕供我审阅”“恢复上次超时的包装任务”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求智能包装、一键成片、智能 B-Roll 或组合式 AI 剪辑。
- 所需 capability：`runtime.control_catalog`、`runtime.controls`、`media.official_resource`、`project.edit_isolated`、`render.proxy`。
- 最低 CLI 版本：`1.6.19`；没有版本绑定 Adapter 和变更集证据时只允许预览计划。
- 默认风险：`external_native_execution`。
- 输入事实：风格、素材清单、允许轨道、受保护对白/品牌/镜头、预算、最大时长、目标渠道和编辑器版本。
- 确认点：预览、下载资源、应用组合变更、模型调用/费用和原生播放分别确认。
- 成功证据：`playback`；提案成功或 GUI toast 不等于草稿和叙事通过。
- 禁止行为：不得自动删除受保护内容、接受无法解释的变更、静默重提 ambiguous 任务或用智能包装替代用户指定剪法。

## 工作流

### Step 1 — 冻结请求
形成 `jianying-smart-package-request/v1`，冻结输入摘要、保护项和预算。

### Step 2 — 预览与拆解
按 [功能动线](references/workflow.md) 生成预览提案并拆分 B-Roll、字幕、花字、音效、特效和转场。

### Step 3 — 独立批准
验证保护规则、资源权益、时间范围和预算，再请求绑定变更摘要的批准。

### Step 4 — 应用与验证
对隔离草稿应用并重新检查草稿差分、代理预览和播放。

### Step 5 — 恢复
失败时局部删除可解释变更或恢复应用前快照；状态不明时保留任务 ID 查询。

## Rules

- 请求、提案、批准和证据使用稳定 digest 串联。
- 保护对白、品牌声明和锁定镜头默认不可修改。
- 每项资源分别校验权益、范围和成本。
- ambiguous 任务只查询/恢复，不新建请求。

## Gotchas

1. **把一键包装当黑盒：** 必须拆解可观察变更。
2. **预览与应用内容漂移：** 批准绑定 proposal digest。
3. **AI 删除关键对白：** 保护规则失败立即拒绝。
4. **预算只在提交后检查：** 必须在预览和批准前门禁。
5. **GUI toast 冒充完成：** 以草稿差分、播放和人工叙事评审为准。

## 安全与数据

不上传原素材，除非精确批准包含 Provider、文件摘要、用途、保留期和费用；凭据与原始账号数据不进入计划或日志。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
