# 目标驱动视频质量循环实施任务

> 2026-10-12 过度设计裁剪：删除平台机制范围（1.1/1.3–1.7 依赖门禁与失败基线、4.4 步骤批准/预算/重试对账管道、7.3 批准摘要绑定与累计预算、7.4 预算/轮次/截止门禁持久化、7.7 单写/对账/取消故障注入、7.8 幂等恢复与占用对账、7.9 发布 Feature Gate 仪式、10.1/10.2 全量回归与干净安装验收仪式、10.4 Windows 支持边界矩阵、10.5 三宿主安装验证、10.6 发布与市场门禁、10.7 OpenSpec 归档门禁）及流水账段落；保留质量循环功能：合同 Schema 与规范化、场景 QualityProfile、评估器与代理/技术证据、Revision 规划与停滞检测、Vlog/课程/婚礼闭环与真实剪映验收。未完成任务收敛为单行；历史见 git 与 docs/evidence/。

## 1. 依赖门禁与失败基线

- [x] 1.2 冻结现有开放工作流、旧 Harness、VLOG-01/COURSE-01/WEDDING-01 黑盒结果，证明新增入口关闭时行为和结果摘要不变。（兼容性）

## 2. Schema 与规范化摘要

- [x] 2.1 实现并发布 fixture 覆盖的 `jianying-creative-target/v1` Schema、严格解析、规范化摘要和未知字段拒绝。（TARGET-01/02）
- [x] 2.2 实现 `jianying-quality-profile/v1` Schema，覆盖评估维度、硬门禁、阈值、证据要求、动作白名单和人工边界。（TARGET-03/04）
- [x] 2.3 实现 `jianying-evaluation-input/v1` 与 `jianying-evaluation-verdict/v1` Schema，限制字段大小、时间范围、证据引用和决定枚举。（EVAL-01/03）
- [x] 2.4 实现 `jianying-revision-request/v1` 与迭代策略 Schema，覆盖预算、轮次、截止时间、提升和重复问题门限。（ITER-01/03/04）
- [x] 2.5 实现 `jianying-evidence-bundle/v1` Schema，分开结构、技术、代理、冷重开、播放、原生导出和创作评审证据。（EVAL-02）
- [x] 2.6 建立六类合同的 canonicalization golden fixtures，验证键序、数组语义、Unicode、整数微秒和摘要在 Codex/ZCode/Kimi 入口一致。（全部合同）

## 3. Skills QualityProfile 正式消费

- [x] 3.1 在 `jianying-skills` 的独立 OpenSpec 变更中定义 Vlog、课程和婚礼 QualityProfile 的知识合同、来源与专业边界；插件仓只记录锁定消费要求。（TARGET-03/04）
- [x] 3.2 为 Vlog profile 提供叙事建立、变化、结尾回望、重复镜头、音画关系和隐私门禁 fixture，并验证不能输出执行器或命令。（TARGET-03）
- [x] 3.3 为课程 profile 提供教学完整性、预告语境、字幕可读性、语言审校和画幅安全区 fixture。（TARGET-04）
- [x] 3.4 为婚礼 profile 提供仪式连续性、私人纪念情绪、商业用途和授权隔离 fixture。（TARGET-04）
- [x] 3.5 发布不可变 Skills 版本、更新插件 `skills.lock.json`，在无开发目录的新安装中验证 profile Schema、版本、内容摘要和缺失/篡改失败行为。（TARGET-03）

## 4. CreativeTarget 与工作流步骤合同

- [x] 4.1 实现从已确认 CreativeBrief/场景路由构建 CreativeTarget，保留 `user_confirmed/observed/inferred_pending_review` 来源状态。（TARGET-01/02）
- [x] 4.2 实现多输出 CreativeTarget 隔离，验证婚礼三用途和课程四输出不共享隐含目标、许可或通过结论。（TARGET-04）
- [x] 4.3 扩展受信步骤注册表：`proxy_render`、`technical_validation`、`creative_evaluation`、`human_review`、`revision_planning`、`native_export`、`delivery_validation`。（ITER-01）
- [x] 4.5 更新 WorkflowPlan 编译和回执摘要，使 target/profile/iteration policy 参与语义摘要，评估步骤保持在 Job 外且草稿写入仍只生成 `jianying-job/v2`。（ITER-01/02）

## 5. 代理与确定性技术证据

- [x] 5.1 为发布 CLI `render.proxy` 建立 capability 和输出合同黑盒测试；缺能力时结构化阻断，禁止 Cargo、Rust 源码、Python 或外部 fork 兜底。（EVAL-02、ITER-01）
- [x] 5.2 实现代理工件摘要、媒体探测、可解码性、时长、画幅、帧率和音视频流证据采集。（EVAL-01/02）
- [x] 5.3 实现确定性关键帧/镜头证据采样，记录时间码、采样算法版本和源代理摘要。（EVAL-01）
- [x] 5.4 实现本地音频技术证据，至少覆盖无音轨、静音区间、峰值和响度；不把技术指标解释成主观质量通过。（EVAL-01/02）
- [x] 5.5 把字幕、ASR 和语言审校状态加入 EvaluationInput，验证未确认转写不能成为事实或通过依据。（TARGET-02、EVAL-01）
- [x] 5.6 实现 EvidenceBundle 聚合器，证明同一路径内容变化使旧结构、代理和创作证据失效，且低层证据不能提升高层状态。（EVAL-02）

## 6. 独立评估器与权限边界

- [x] 6.1 定义 evaluator adapter 接口和身份合同，先实现无外部调用的人工评审 adapter 与确定性技术 evaluator。（EVAL-03/04）
- [x] 6.2 实现 Verdict 严格解析、硬门禁优先、finding 证据引用和时间范围校验；总分通过但硬门禁失败必须拒绝 pass。（EVAL-03）
- [x] 6.3 实现一个获准模型 provider adapter，绑定模型版本、输入摘要、预算、上传资源范围、请求 ID、超时和对账状态。（EVAL-05）
- [x] 6.4 验证本地与远程 evaluator 使用同一输入/输出合同，provider 特有字段不能泄漏到 WorkflowPlan 或 Job。（EVAL-01/03/05）
- [x] 6.5 实现敏感日志净化和有界读取，验证密钥、完整私人转写、原始媒体和无关绝对路径不进入错误或审计输出。（EVAL-05）
- [x] 6.6 增加执行者/评估者隔离测试，证明 CLI 或编辑 executor 的自报成功不能产生独立 EvaluationVerdict。（EVAL-04）
- [x] 6.7 用真实 Vlog 无音轨代理建立 RED，确保锁定画像要求 `audio_metrics` 时确定性评估不得返回 `pass`；仅由发布 CLI 确认音轨后形成摘要绑定的音频证据，并测试缺失、伪造与完整证据路径。（EVAL-01）

## 7. Revision、批准、停滞和恢复

- [x] 7.1 实现 finding 到受信动作类别的过滤器，未知动作只保留建议；支持动作生成 RevisionRequest 而不直接执行。（ITER-01）
- [x] 7.2 实现 RevisionRequest 到新 WorkflowPlan revision 的确定性规划，验证目标、素材、决策、Job、CLI、profile 或输出变化使旧批准失效。（ITER-02）
- [x] 7.5 实现关键评分最小提升、重复 major/critical finding、硬门禁回退和无可执行动作的停滞检测。（ITER-04）
- [x] 7.6 扩展 WorkflowRuntime 状态和历史事件，覆盖 `rendering_proxy/evaluating/revision_requested/needs_human_review/capability_blocked/iteration_stopped`。（ITER-03/04）

## 8. VLOG-01 第一条完整质量闭环

- [x] 8.1 用合成素材建立 Vlog 第一版基线，使独立 evaluator 稳定发现一个有时间范围、可由当前能力修复的问题。（ITER-06）
- [x] 8.2 跑通第一版 `CreativeTarget → Plan → Job → 发布 CLI → Proxy → Verdict`，保存全部摘要、身份和分层证据。（TARGET/EVAL）
- [x] 8.3 将 verdict 转为 revision 2，验证旧批准不能使用，用户重新批准后只由发布 Rust CLI 生成隔离的新草稿。（ITER-01/02/05）
- [x] 8.4 再次生成代理并评估，验证问题已修复、无硬门禁回退且 EvidenceBundle 同 revision/摘要一致。（EVAL-01/02/03、ITER-04）
- [ ] 8.5 用获准真实 Vlog 素材重复两轮链路，完成真实剪映冷重开、连续播放、原生导出及叙事/音画人工验收。（ITER-06）
- [x] 8.6 保存 Vlog 失败向量：篡改 profile、替换同路径素材、评估超时、代理损坏、批准过期、执行后崩溃和停止循环。（全部门禁）

## 9. 课程与婚礼扩展

- [x] 9.1 跑通 COURSE-01 母版及三个派生输出的独立 QualityProfile、代理、字幕/语境评估和按输出返工。（TARGET-04、ITER-06）
- [x] 9.2 验证 COURSE-01 单个预告失败不污染其他输出，但父工作流在必需输出未通过时不 completed。（EVAL-02、ITER-06）
- [ ] 9.3 跑通 WEDDING-01 仪式、私人纪念、商业广告三用途的目标、授权、评审和证据隔离。（TARGET-04、ITER-06）
- [x] 9.4 验证商业许可缺失、多机位未支持、需专业审校或用户主观选择时进入明确阻塞/人工状态，不由模型补齐。（TARGET-02/04、ITER-04/06）

## 10. 发布、宿主与完成门禁

- [ ] 10.3 在 macOS 真实剪映完成 Vlog、课程和婚礼所需的冷重开、播放、原生导出与人工质量记录；未验收场景保持 pending。（ITER-06）
