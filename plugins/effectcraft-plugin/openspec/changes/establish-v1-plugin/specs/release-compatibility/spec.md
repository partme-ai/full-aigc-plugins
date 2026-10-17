# EffectCraft — release-compatibility

## Purpose

本能力定义 EffectCraft 在 release-compatibility 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；已有实现与限定范围证据不等于完整需求验收。

## ADDED Requirements

### Requirement: EC-RL-001 宿主与发布证据

发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。

#### Scenario: EC-RL-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成宿主与发布证据并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: EC-RL-001-N 边界条件

- **WHEN** 只有 OpenSpec 校验与文档检查通过
- **THEN** 状态保持 documentation-baseline，所有实现任务仍未完成

#### Scenario: 已安装技能的宿主派发

- **WHEN** Codex 宿主收到自然语言安装、创作、故障恢复或交付请求
- **THEN** 验收 SHALL 使用实际安装的独立技能，记录模型选择技能、调用公开入口、任务回执、原生工程与媒体结果；手工直接调用脚本不构成自动派发证据
- **AND** 其他宿主未运行相同链路时保持待验收，不借用 Codex 结论

#### Scenario: 候选与固定发行边界

- **WHEN** 技能源候选通过本地测试但尚无正式固定来源版本，或插件快照与锁不一致
- **THEN** 发布校验 SHALL 拒绝将候选标成已发布；版本、技能摘要、运行时身份、协议引用和场景证据均须绑定当前来源
- **AND** 提交、推送、市场更新和正式发布按各自动作的授权执行；发布本身不替代目标平台及宿主验收

#### Scenario: EffectCraft 到 FilmCraft 的透明序列交接

- **WHEN** 向 FilmCraft 交付透明动画序列
- **THEN** 验收 SHALL 检查实际帧、时间基准、alpha 和来源摘要，并验证下游导入及保全；缺少任一证据时不得宣称完整交接

## Implementation evidence (non-normative)

`docs/evidence/codex-current-release.json` binds current fixed releases to two actual Codex CLI/app-server versions, five enabled namespaced skills, installed public workflow outcomes and explicit exclusions. The corresponding bilingual Host-Verification-Architecture documents specify the repeatable check. RL-001 tasks remain unchecked until their full P0 prerequisites and scenarios pass.

#### Scenario: 当前能力矩阵与公共协议兼容

- **WHEN** 生成候选或正式分发说明
- **THEN** 当前能力矩阵 SHALL 从锁文件及绑定当前来源的有效证据生成；历史报告与当前支持状态分开显示，规格任务的实现路径须对应真实独立技能源
- **AND** 保留 craft-task/v1、craft-artifact/v1 的既有所有权与读取兼容性，领域信息只做兼容扩展，不另建平行公共协议

#### Scenario: 完整完成门禁

- **WHEN** 判断本优化或整个 V1 是否完成
- **THEN** 每个目标平台与能力 SHALL 具备自己的真实证据；静态检查、模拟测试、历史报告、文档校验或发布成功不得替代原生任务与实际宿主验收
- **AND** 未通过项 SHALL 保持开放，全部实现、验证与规格同步条件满足前不得归档整个 establish-v1-plugin

#### Scenario: Agent Plugins 核心与客户端扩展边界

- **WHEN** 打包或说明 EffectCraft 的 Agent Plugins 1.0.0 能力
- **THEN** 根 `plugin.json` SHALL 是唯一可移植 manifest，`skills/` 与可选根 `mcp.json` 按规范固定位置发现；命令、钩子 SHALL 只作为明确标识的客户端扩展声明
- **AND** 缺少根 `mcp.json` 时不得宣称包提供标准 MCP 组件；有原生 CLI 或技能内部 MCP 客户端也不能代替宿主发现和实际 MCP 调用证据

#### Scenario: 当前能力矩阵拒绝过期技能和安装证据
- **WHEN** 维护者由锁文件生成当前能力矩阵
- **THEN** 原生验收状态须绑定完整独立技能载荷、Python 与原生制品身份，以及不可变原始报告摘要；任一文件新增、缺失、变化或报告摘要不符时，相关状态保持 NOT_RUN 并列出失效原因
- **AND** 原生技术样例不得升级为整个平台、领域代表场景、冷安装、Web 或宿主视觉验收；历史 README 记录保留在版本历史中，不能作为当前状态
