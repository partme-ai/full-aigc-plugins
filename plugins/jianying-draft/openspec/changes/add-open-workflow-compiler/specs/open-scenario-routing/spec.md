# 开放场景路由

## Purpose

让用户的创作简报能够进入已有案例、组合方案或新场景提案，并明确缺素材、歧义与能力差距。
通过显式版本入口保留旧规划行为，避免场景扩容造成错误硬套、静默丢失或未经授权的执行。

## ADDED Requirements

### Requirement: ROUTE-01 新旧入口与目录兼容

工作流入口 SHALL 消费配套 `open-scenario-catalog` v2 合同，检查版本、完整性和正式 provenance。
既有 v1 `plan-video` SHALL 保持输入、种子结果和失败基线；v2 不存在时新入口不得静默回退为完整开放支持。
默认规划 MUST NOT 调用模型、联网读取来源、读取媒体内容或启动剪映。

#### Scenario: 扩容目录与旧命令并存

- **WHEN** 合法 v2 有 109 项且同包保留冻结 v1
- **THEN** 新入口可检索第 109 项，旧入口仍遵守原 108 项行为

#### Scenario: 缺少 v2

- **WHEN** 新入口只找到旧版技能
- **THEN** 返回 `catalog_v2_unavailable` 与恢复建议，不篡改技能锁

#### Scenario: 关闭新入口回滚

- **WHEN** 运维显式设置 `JIANYING_OPEN_WORKFLOW_DISABLED=1`
- **THEN** 新工作流的规划、编译、启动、批准、执行和恢复返回 `open_workflow_disabled`；旧 `plan-video` 保持原合同，持久任务与副作用账本不被删除

### Requirement: ROUTE-02 结构化简报和事实来源

简报 SHALL 区分用途、受众、领域、形式、素材条件、渠道、交付与硬约束；
每项事实 SHALL 标识用户给定、机器探测、模型推断、人工确认或未知。
多个目标冲突时 SHALL 要求澄清或拆分交付，不以题材关键词覆盖用户用途。

#### Scenario: 婚礼用途不清

- **WHEN** 用户只说婚礼视频
- **THEN** 返回差异明确的候选和关键问题，不自动选择快剪

### Requirement: ROUTE-03 三路决策和独立就绪状态

输出 SHALL 分别记录 `route=known|composed|proposed` 与 readiness，无法选型时 route 为 null。
readiness SHALL 区分需选择、需输入、需审核、能力阻断和已形成方案；
规划输出始终 SHALL 为 `evidence_level=plan`、`executable=false`。
未知题材可复用策略，但新技术或交付方式 MUST NOT 被普通视频路线冒充。

#### Scenario: 宠物故事未命中目录

- **WHEN** 无精确案例但已有事实叙事策略可参考
- **THEN** 返回提案、方法来源和不确定性，不伪造正式 scene ID 或写入公共目录

#### Scenario: 全景交付缺能力

- **WHEN** 提案要求全景交付而执行端不能证明对应能力
- **THEN** 允许保留方法方案，但执行能力阻断，不返回普通 MP4 成功替代

### Requirement: ROUTE-04 可解释与有界检索

候选 SHALL 给出命中/冲突条件、素材缺口和所用策略；首屏最多 3 项，剩余候选通过稳定游标分页。
检索 SHALL 先处理硬约束，再比较用途和素材适配；相同输入和目录版本的确定性路线顺序必须稳定。
模型可选，MUST NOT 将其自报置信度当作已校准概率或执行许可。

#### Scenario: 空查询

- **WHEN** 未提供足够用途且目录含大量条目
- **THEN** 返回关键问题与有界候选，不把全部例文读入模型上下文
