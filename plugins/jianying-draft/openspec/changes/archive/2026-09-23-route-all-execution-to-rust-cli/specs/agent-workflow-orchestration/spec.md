## Purpose

定义从用户意图、素材事实、编辑计划到 CLI 任务和交付验证的智能体编排行为，使复杂剪辑可暂停、恢复和审计。

## ADDED Requirements

### Requirement: 素材事实先于计划
插件 MUST 在计划生成前探测实际素材时长、流、尺寸和路径可用性，不得沿用示例或猜测数据。

#### Scenario: 用户未提供时长
- **WHEN** 用户提供媒体但没有时长信息
- **THEN** 插件先调用只读探测，再生成时间线计划

### Requirement: 可恢复工作流
插件 SHALL 将多步工作流记录为带检查点的任务，允许从最后一个已验证阶段恢复而不重复已完成的付费或副作用操作。

#### Scenario: ASR 完成后草稿构建失败
- **WHEN** ASR 已完成但后续构建失败
- **THEN** 恢复流程复用 ASR 结果并只重试安全的构建阶段

### Requirement: 交付验证
插件 SHALL 根据请求的目标证据等级执行验证，并清楚区分代理预览、可编辑草稿和原生导出。

#### Scenario: 用户要求最终 MP4
- **WHEN** 原生导出任务只完成了代理预览
- **THEN** 插件不得报告最终交付完成，并继续显示缺失的原生导出门禁

### Requirement: 已有草稿强类型编辑编排
插件 SHALL 将已有草稿编辑意图编译为包含明确 `source`、全新 `output` 和非空强类型 `operations` 的 `jianying-job/v2` edit 作业，并通过同一个 Rust Runtime Adapter 执行。

#### Scenario: 组合编辑已有草稿
- **WHEN** 智能体请求替换文字、移动片段或删除片段
- **THEN** Harness 不生成 Python 脚本、不探测无关媒体，把三类操作无损写入 edit Job，并以 `job.run.edit` 和最终输出目录建立一次性高风险批准绑定

#### Scenario: 不支持的新增操作
- **WHEN** 编辑意图提交尚未完成原生闭包映射的 `add_material` 或 `add_segment`
- **THEN** Harness 在写入任务状态前返回稳定的 `edit_operation_not_supported`，不得把部分能力伪装成完整支持
