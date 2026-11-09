# 工作流到 Job 的确定性编译

## Purpose

把经过确认的素材选择和编辑决策转换为发布 Rust CLI 可接受的 Job，并为每个输出提供可复现回执。
隔离模型判断、运行能力、执行授权和真实交付证据，使编译成功不越权触发副作用。

## ADDED Requirements

### Requirement: COMPILE-01 两段编译与就绪区分

知识规划 SHALL 先产生 WorkflowPlan；仅具体剪辑节点可生成 `jianying-job/v2`。
模型、人工、翻译和生命周期步骤 MUST NOT 伪装为 Job 字段。
输出 SHALL 分别报告 `can_compile`、`can_execute` 与缺口；编译不启动剪映、模型或原生导出。

#### Scenario: 未选片的方案

- **WHEN** 只有故事段落而没有已确认素材范围
- **THEN** `can_compile=false`，列出缺片段事实，不编造可执行 Job

#### Scenario: 已编译但未批准

- **WHEN** 输入与能力合法但缺本次输出的执行批准
- **THEN** 可返回编译回执和 Job，`can_execute=false`，不触发执行

### Requirement: COMPILE-02 时间与媒体完整性

所有片段 SHALL 使用已探测媒体和已确认源范围；时间采用非负安全整数微秒，时长必须正。
源区间 SHALL 不超出素材时长，目标区间和音轨/字幕引用 SHALL 满足各自轨道规则。
首批仅支持明确的等速编辑；未实现变速、同步、转场或外部资产处理 MUST 明确拒绝对应步骤。

#### Scenario: 超界、无效数值与未支持变速

- **WHEN** 片段越界、时间不是安全整数，或计划要求未实现的变速映射
- **THEN** 返回 `media_range_invalid` 或 `unsupported_edit_mapping`，不静默裁剪或改变速度

### Requirement: COMPILE-03 确定性与回执

相同规范化输入、素材账本、目录、步骤注册表与 CLI 身份 SHALL 产生相同语义 Job 和摘要。
回执 SHALL 记录输入/计划/Job 摘要、编译器版本、CLI 身份、目标输出和警告。
运行时间、临时工作路径和任务尝试 ID 不得破坏语义可复现比较。

#### Scenario: 连续编译两次

- **WHEN** 冻结输入在不同临时工作目录重复编译
- **THEN** 语义 Job 与摘要相等，运行记录可不同；不调用执行器证明确定性

### Requirement: COMPILE-04 能力与原子操作边界

编译 SHALL 对已发布二进制进行身份和能力核对，未知/非 supported 能力 MUST 阻断受影响节点。
执行前 SHALL 再核对回执绑定；二进制或输入变化不得沿用旧批准。
不存在的原子能力 SHALL 形成明确缺口，不读取 Rust 源码、安装 fork 或生成临时引擎补洞。

#### Scenario: 编译后更换二进制

- **WHEN** 执行时 CLI 摘要与回执不一致
- **THEN** 停止执行并要求重新检查和批准，不仅比较版本字符串

### Requirement: COMPILE-05 多输出和隔离

每个输出 SHALL 编译到独立目标，保留母版/派生关系；源媒体和已有草稿不得被默认覆盖。
父计划 SHALL 明确失败策略；受阻子任务不得让父任务报告全部完成。

#### Scenario: 商业子任务受阻

- **WHEN** 婚礼私人交付允许而广告缺商业许可
- **THEN** 默认暂停父计划；只有显式允许独立分支继续时执行私人分支，父计划仍报告未全部完成
