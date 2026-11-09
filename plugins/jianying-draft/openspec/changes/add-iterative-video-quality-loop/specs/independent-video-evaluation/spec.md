## Purpose

定义基于真实视频工件、媒体事实和场景目标的独立评估合同，使结构正确、技术可用、创作质量和真实剪映交付证据可以分别验证而不互相冒充。

## ADDED Requirements

### Requirement: EVAL-01 摘要绑定的评估输入

每次评估 SHALL 绑定工作流与 revision、CreativeTarget 和 QualityProfile 摘要、草稿/代理/原生工件摘要、所用媒体事实、评估者身份及允许的资源范围。评估者 MUST NOT 声称观察了未提供的完整视频、音频、GUI 播放或原生导出。

#### Scenario: 代理视频发生变化

- **WHEN** 代理视频路径不变但内容摘要变化
- **THEN** 旧 EvaluationVerdict 不能证明新代理有效，系统要求重新评估

#### Scenario: 缺少音频证据

- **WHEN** QualityProfile 要求音画关系而 EvaluationInput 没有音频流或可验证音频事实
- **THEN** 评估返回证据不足，不推测音频质量或把该维度标为通过；确定性技术评估不得返回 `pass`，而发布 CLI 确认无音轨时不得生成 `audio_metrics` 证据

### Requirement: EVAL-02 分层独立证据

系统 SHALL 分别记录草稿结构、媒体技术、代理内容、真实剪映冷重开、播放、原生导出和人工/模型创作评审证据。请求的 evidence level、CLI 成功或生成者自述 MUST NOT 直接成为实际通过证据。

#### Scenario: CLI 成功但代理不可解码

- **WHEN** CLI 返回成功而代理视频缺失、摘要不符或不能解码
- **THEN** 技术验证失败，工作流不得进入创作通过或 completed

#### Scenario: 代理评审通过但尚未原生导出

- **WHEN** 创作评估通过而交付目标要求真实剪映原生导出
- **THEN** 系统保持原生导出证据未完成，不以代理通过代替交付门禁

### Requirement: EVAL-03 结构化评估结论

EvaluationVerdict SHALL 只使用 `pass`、`revise`、`blocked` 或 `stop` 决定，并包含分项评分、硬门禁结果、证据引用、评估者身份和限制。每个可定位 finding SHALL 包含稳定 code、严重度、输出、时间范围或工件引用、观察证据、关联规则和建议动作类别。

#### Scenario: 总分达标但硬门禁失败

- **WHEN** 加权总分达到阈值但存在未处理的隐私泄漏或必须保留内容缺失
- **THEN** verdict 不得为 `pass`，并明确失败硬门禁及证据位置

#### Scenario: 自然语言输出不符合合同

- **WHEN** 模型只返回自由文本、任意命令、未经引用的时间码或自称已经获得批准
- **THEN** 系统拒绝该结果，不进入修订编译或执行

### Requirement: EVAL-04 评估者与执行者分离

执行器 SHALL 只报告执行结果和工件，不得为自己的创作质量签发独立通过。评估者 SHALL 无草稿写权限且不得授予模型调用、上传、草稿写入、GUI 控制或导出批准。

#### Scenario: 执行器同时提交通过结论

- **WHEN** 同一执行步骤返回草稿并自报所有创作维度通过
- **THEN** 系统只接收工件结果，仍要求符合身份与输入绑定的独立 verdict

### Requirement: EVAL-05 供应商权限和不确定调用

远程评估 SHALL 在调用前核对 provider、模型、预算、上传素材范围、隐私和有效批准。调用结果不明时 SHALL 查询原请求；无法确认时进入人工对账，MUST NOT 自动重复付费调用。

#### Scenario: 只有本地剪辑批准

- **WHEN** 用户批准本地草稿写入但未批准向远程模型上传视频
- **THEN** 系统不得调用远程评估，可选择符合策略的本地验证器或返回批准缺口

#### Scenario: 评估请求超时

- **WHEN** 远程 provider 可能已经接受请求但连接超时
- **THEN** 系统保存请求身份并进入对账，不以新请求自动重试
