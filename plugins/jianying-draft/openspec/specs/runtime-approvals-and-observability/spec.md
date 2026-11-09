# runtime-approvals-and-observability Specification

## Purpose
提供与操作风险匹配的审批、任务状态、审计、恢复和诊断契约，使 Codex、ZCode、Kimi 中的剪映自动化都能绑定明确目标、保留可重算证据、展示一致终态，并且不会越过用户授权范围。
## Requirements
### Requirement: 风险分级审批
插件 SHALL 将调用划分为只读、可逆写入、高风险写入和外部/原生执行，并只在对应授权范围内继续。

#### Scenario: 删除草稿
- **WHEN** 智能体准备执行草稿删除
- **THEN** 插件要求目标明确的一次性批准，且批准不能扩展到其他草稿

#### Scenario: 编辑已有草稿的隔离副本
- **WHEN** Harness 准备执行 `job.run.edit`
- **THEN** 批准精确绑定 Job 文件摘要、源草稿、最终输出目录、任务和有效期，且 Runtime Adapter 不额外传递 create 专用的 `--out`

### Requirement: 任务与审计可见性
插件 SHALL 提供任务 list/show/cancel/retry/audit 语义，并在三宿主中展示一致的状态与终态原因。

#### Scenario: 用户查询导出状态
- **WHEN** 用户在任一宿主查询运行中的导出任务
- **THEN** 插件返回相同任务 ID、阶段、进度、阻塞原因和下一动作

### Requirement: Doctor 诊断
插件 SHALL 检查 CLI、Schema、技能锁、媒体工具、草稿根和剪映运行时，并区分只读检查和显式修复。

#### Scenario: Python 依赖已删除
- **WHEN** 环境没有 `pymediainfo` 或 pyJianYingDraft
- **THEN** Doctor 不应报错，因为它们不再属于运行依赖
