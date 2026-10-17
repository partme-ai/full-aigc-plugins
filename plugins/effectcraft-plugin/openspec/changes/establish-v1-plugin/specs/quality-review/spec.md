# EffectCraft — quality-review

## Purpose

本能力定义 EffectCraft 在 quality-review 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前按需求逐项实施；各需求和目标环境的完成状态以tasks及绑定证据为准。

## ADDED Requirements

### Requirement: EC-QA-002 受限局部修订

质量循环 SHALL 将问题绑定对象、帧或区域及责任插件；设置最大轮数、预算与停滞规则；目标变化使旧验收与授权失效。

#### Scenario: EC-QA-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成受限局部修订并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: EC-QA-002-N 边界条件

- **WHEN** 连续修订无改善或达到预算
- **THEN** 停止自动修订，保留最佳可验证版本并报告未解决问题
