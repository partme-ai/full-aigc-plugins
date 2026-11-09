## Purpose

将独立评估中的可执行问题转换为新的、需重新批准的工作流修订，并通过能力、预算、轮次、停滞和人工判断门禁避免无限循环或重复副作用。

## ADDED Requirements

### Requirement: ITER-01 评估不能直接执行

系统 SHALL 先把 verdict finding 映射为受信动作类别和 RevisionRequest，再由确定性规划/编译路径产生新 WorkflowPlan 和 Job。评估结果 MUST NOT 携带或执行 shell、任意 CLI 参数、文件写入 handler 或用户批准声明。

#### Scenario: 建议缩短开头

- **WHEN** Vlog verdict 指出开头过慢并给出有证据的时间范围
- **THEN** 系统产生受约束的选段/裁剪 RevisionRequest，等待新计划、编译和批准，而不直接修改草稿

#### Scenario: 建议当前能力不支持的效果

- **WHEN** finding 建议复杂转场但已发布 CLI 或编译器没有对应 supported capability
- **THEN** 系统返回 `capability_blocked` 或人工替代选择，不生成猜测字段或调用源码兜底

### Requirement: ITER-02 新修订重新绑定批准和证据

返工 SHALL 建立递增且有界的新 revision，并重新绑定目标、素材、编辑决策、Job、CLI 身份、用途、输出、预算和有效期。上一 revision 的写入批准、评估结论和下游交付证据 MUST NOT 自动继承。

#### Scenario: 第一轮评估要求返工

- **WHEN** revision 1 的 verdict 为 `revise` 且形成 revision 2
- **THEN** revision 2 在获得精确新批准前不得写草稿，revision 1 的工件和证据保留可追踪

### Requirement: ITER-03 有界迭代策略

WorkflowPlan SHALL 冻结最大修订次数、模型调用次数、累计预算、截止时间、最小有效提升、重复问题上限、回退容忍度和人工复核点。任一上限到达 SHALL 停止自动规划并报告实际原因。

#### Scenario: 达到预算上限

- **WHEN** 下一次模型评估会超过累计预算
- **THEN** 系统进入 `iteration_stopped` 或等待用户扩大批准，不发起调用且不伪报质量完成

#### Scenario: 达到最大修订次数

- **WHEN** 当前 revision 已达到 `maximum_revisions`
- **THEN** 系统停止自动返工，保留最后产物、所有 verdict 和未解决问题供人工决定

### Requirement: ITER-04 停滞与回退检测

系统 SHALL 检测连续关键评分提升不足、同一 major/critical finding 重复、修复导致硬门禁回退以及没有可执行修复动作。停滞时 SHALL 请求人工复核、补充素材、改变范围或明确停止，MUST NOT 继续无界修改。

#### Scenario: 相同重大问题重复出现

- **WHEN** 同一 major finding 达到策略规定的重复上限
- **THEN** 系统进入 `needs_human_review` 或 `iteration_stopped`，并列出已尝试修订和证据

#### Scenario: 修复节奏导致事实缺失

- **WHEN** 缩短片段提升节奏分但删除必须保留事件
- **THEN** 系统判定硬门禁回退，不接受该 revision 为最终完成

### Requirement: ITER-05 未知副作用先对账

质量返工 SHALL 服从现有单写、写前持久化、取消确认和恢复对账合同。草稿写入、模型调用或原生导出结果不明时 MUST 先查询原任务和验证已有产物，不得因新 verdict 或 resume 重复执行。

#### Scenario: 写草稿成功后状态落盘前崩溃

- **WHEN** 恢复时发现原执行可能已产生 revision 产物
- **THEN** 系统先验证和绑定已有产物；只有确认未执行且重新批准后才能开始新尝试

### Requirement: ITER-06 三类场景逐级验收

本变更 SHALL 先完成 VLOG-01 的两轮真实质量闭环，再分别验证 COURSE-01 多输出和 WEDDING-01 多用途。离线合同、发布二进制、真实剪映和 Codex/ZCode/Kimi 宿主证据 SHALL 分级记录，缺失层级保持未验证。

#### Scenario: Vlog 第一条完整闭环

- **WHEN** 第一版代理被独立评估发现可执行问题，用户批准新 revision，第二版再次评估并满足必需门禁
- **THEN** 系统保存两版计划、Job、CLI 身份、产物、verdict、批准和交付证据，且实际要求的冷重开、播放和原生导出未完成时不得宣称生产闭环完成

#### Scenario: 课程一个派生输出失败

- **WHEN** 课程母版和两个预告通过而第三个预告字幕或语境不通过
- **THEN** 第三个输出保持返工或失败，其他独立输出可保留通过，但父工作流不得标记全部完成

### Requirement: ITER-07 质量循环入口必须版本化且可安全回滚

质量循环 SHALL 由插件随包发布的严格、版本化 Feature Gate 控制。生产默认值在 10.6 发布门禁完成前 MUST 为关闭；关闭时只有调用方明确 opt-in 才能附加质量合同。配置缺失、未知字段、非法阶段或摘要不一致 SHALL 失败关闭。关闭入口或回滚插件锁版本 MUST NOT 删除或改写既有副作用账本、证据、未决请求和 ambiguous 资源占用。

#### Scenario: 默认关闭但显式启用

- **WHEN** 发布包的质量循环默认值为关闭，调用方未显式 opt-in
- **THEN** 系统以 `quality_loop_disabled` 拒绝附加质量合同；显式 opt-in 后生成绑定配置摘要和激活来源的门禁记录

#### Scenario: 回滚时存在未知副作用

- **WHEN** 远程评估、草稿写入或原生导出账本处于 ambiguous，随后关闭质量循环入口
- **THEN** 账本字节、历史和占用保持不变，后续同作用域执行仍以 `side_effect_reconciliation_required` 阻断，直到显式对账
