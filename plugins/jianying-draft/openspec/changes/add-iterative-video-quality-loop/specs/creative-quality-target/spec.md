## Purpose

为视频质量循环建立与具体工作流修订绑定的创作目标和场景评审档案，使参考作品、用户要求、推断和授权保持可追溯且不被误当成执行指令。

## ADDED Requirements

### Requirement: TARGET-01 版本化创作目标

系统 SHALL 使用版本化 CreativeTarget 表达叙事目标、受众、渠道、目标时长、参考工件、必须保留内容、禁止内容和 QualityProfile 引用。CreativeTarget SHALL 绑定工作流、修订和内容摘要；未知版本或未声明执行字段 MUST 拒绝。

#### Scenario: 冻结 Vlog 创作目标

- **WHEN** 用户确认生活 Vlog 的叙事目标、目标片长、必须保留事件和隐私禁止项
- **THEN** 系统生成可摘要复核的 CreativeTarget，且其中不包含命令、脚本、工具授权或已执行声明

#### Scenario: 目标内容被改变

- **WHEN** 必须保留内容、禁止内容、目标时长或 QualityProfile 摘要发生变化
- **THEN** 系统要求新 revision，并使依赖旧目标的批准、评估和下游证据失效

### Requirement: TARGET-02 来源与确认状态分离

目标中的事实和约束 SHALL 标明 `user_confirmed`、`observed` 或 `inferred_pending_review` 来源状态。模型推断和参考作品中的内容 MUST NOT 自动成为用户事实、素材许可、商业用途许可或硬约束。

#### Scenario: 从参考广告推断商业用途

- **WHEN** 参考作品是商业广告但用户只批准私人 Vlog
- **THEN** 系统不得把商业用途、公开发布或素材许可写成已确认目标

#### Scenario: 推断的故事节点未确认

- **WHEN** 模型从素材描述推断存在情绪转折但没有观察证据或用户确认
- **THEN** 系统将其标记为待审推断，不据此裁剪或判定硬门禁通过

### Requirement: TARGET-03 锁定场景质量档案

QualityProfile SHALL 声明评估维度、硬门禁、阈值、所需证据、允许建议的动作类别和必须人工判断的边界。正式运行 SHALL 只消费插件锁定 Skills 中通过 Schema 和摘要校验的档案；开发目录或未锁定内容不得作为发布证据。

#### Scenario: 正式 Vlog 档案可用

- **WHEN** 锁定 Skills 中的 Vlog QualityProfile 版本、Schema 和内容摘要均匹配
- **THEN** 系统把 profile 身份和摘要写入目标及后续评估输入

#### Scenario: 档案被本地修改

- **WHEN** profile 路径存在但内容摘要与 Skills lock 不同
- **THEN** 正式工作流返回档案完整性错误，不降级读取该内容或旧缓存

### Requirement: TARGET-04 多输出目标隔离

同一素材集的不同交付 SHALL 分别绑定用途、目标、QualityProfile 和必需证据。一个输出的目标、评分或许可 MUST NOT 自动应用于另一个输出。

#### Scenario: 婚礼三用途

- **WHEN** 同一婚礼素材需要完整仪式、私人纪念和商业广告
- **THEN** 系统为三个输出保留独立目标和质量档案，商业分支缺许可不影响已获准的私人分支，但父工作流不得伪报全部完成

