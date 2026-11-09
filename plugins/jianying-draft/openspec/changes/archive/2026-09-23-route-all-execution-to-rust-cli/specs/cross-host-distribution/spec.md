## Purpose

确保 Codex、ZCode、Kimi 获得相同的 CLI 制品、技能版本、命令契约和安装验证，不因宿主清单不同产生功能分叉。

## ADDED Requirements

### Requirement: 三宿主行为一致
插件 SHALL 在 Codex、ZCode、Kimi 上暴露等价的核心工作流、风险门禁和结构化结果。

#### Scenario: 同一计划跨宿主执行
- **WHEN** 三个宿主对相同素材和计划调用插件
- **THEN** 它们使用同一 CLI 版本与 Schema，并产生语义等价结果

#### Scenario: 最终 cutover 读取真实宿主证据
- **WHEN** 自动化准备删除迁移期环境变量诊断
- **THEN** readiness 必须验证 Codex、ZCode、Kimi 各自的真实宿主证据文件、SHA-256、插件/CLI/Skills 版本和同一 Job 输入；三者规范化结果语义摘要必须完全相同

#### Scenario: 宿主观察遗漏生产交互门禁
- **WHEN** 任一正式安装包没有证明 fresh install、doctor、技能发现、单技能安装、13 分类发现与路由、选择解释、批准、简单 Job、停止、恢复、证据展示及原生导出授权中的任一项
- **THEN** observation 与汇总验收均 fail closed；旧版五项检查记录不得提升为当前版本真实宿主通过

#### Scenario: 宿主观察只有人工布尔声明
- **WHEN** 任一生产交互检查只有 `true` 声明，缺少带时间戳的宿主/命令证据对象及其规范化 SHA-256，或内嵌证据被篡改
- **THEN** observation、记录器和汇总验收均 fail closed；不得把手写布尔值当作真实宿主证明

#### Scenario: 宿主证据缺失、漂移或分叉
- **WHEN** 任一宿主缺失、证据被篡改、版本不匹配，或相同 Job 产生不同语义摘要
- **THEN** 发布和 Rust-only cutover 均 fail-closed，静态 fixture 与开发 checkout 不得替代

#### Scenario: CLI、Skills 或插件版本发生变化
- **WHEN** 正式导入新的 CLI release index、Skills manifest，或提升插件版本
- **THEN** 自动将宿主验收状态重置为 pending 并清空旧宿主条目；新版本不得继承旧版本通过证据

#### Scenario: 市场工具提升插件版本
- **WHEN** 市场事实源的 bump 工具更新 catalog 与三宿主 manifest
- **THEN** 它必须同时更新中英文 README 的完整 Codex 包版本，并把真实宿主验收重置为新基础版本的 pending 空集合；distribution validator 必须拒绝 README 与 manifest 漂移

#### Scenario: Bump 完成但 tag 与 Release 尚未建立
- **WHEN** bump 工具已生成 catalog、manifest、README 和市场清单变更，但尚未提交、推送 tag、通过不可变 Release workflow 或完成真实市场安装
- **THEN** 工具只能报告“发版候选已生成”，必须明确列出 tag、Immutable Release、制品校验和真实消费验证仍待完成；不得把版本文件写入成功称为发布完成

#### Scenario: 发布前只读远端预检
- **WHEN** 维护者准备发布 Skills、CLI 或插件，但尚未授权创建 tag、Release 或修改仓库设置
- **THEN** 插件提供机器可读的只读预检，分别报告三仓 Immutable Releases 设置、预期 `v1.6.0` CLI、`v2.0.3` Skills 和当前插件 Release；每个 Release 必须精确包含其三平台包/index、Skills manifest 或插件归档/审计/readiness/canary/verification 资产集合，且每个资产必须为非空 uploaded 状态、具有 GitHub `sha256:` digest 并使用对应仓库/tag 的正典下载 URL；空壳、缺项、额外资产、摘要或 URL 漂移均不得标记 ready；报告区分“前置条件已具备”和“插件 Release 已完成”，查询失败必须结构化为 blocked 且不得修改远端

#### Scenario: 市场同步遇到仓库自定义指令
- **WHEN** release-tooling 同步发现插件仓已有与通用模板不同的 `AGENTS.md`
- **THEN** 默认保留仓库指令并从写入计划排除；只有维护者显式传入 `--refresh-agents` 才允许替换，且 `--dry-run` 必须提前显示保留或更新决策

### Requirement: 可执行 CLI 分发
插件 SHALL 提供经过哈希验证的可执行 CLI 或确定性的安装/构建流程，不得把源码目录冒充已安装能力。

#### Scenario: 安装后首次检查
- **WHEN** 插件完成安装
- **THEN** Doctor 能直接执行 CLI 版本与 capability 握手，无需用户手工 Cargo 构建

#### Scenario: 下载制品身份与发布锁分裂
- **WHEN** archive 及成员摘要均有效，但 capability manifest 的 schema、CLI 版本、released 状态、tag 或 source commit 与不可变发布锁任一不一致
- **THEN** fetcher 在激活运行时前 fail closed；缺少 source commit 或 capability schema 的锁必须在发起网络请求前被拒绝

#### Scenario: 包内 capability 与二进制握手分裂
- **WHEN** fresh-install 后二进制 `capabilities --json` 与已校验的包内 capability manifest 内容不完全相同，即使两者发布身份字段相同
- **THEN** canary 必须失败；成功证据必须显式记录二者完全一致，并由三平台证据汇总器再次要求该断言

#### Scenario: 已安装 CLI 不满足锁定技能能力下界
- **WHEN** fresh-install 后 CLI 版本低于 `skills.lock.json` 的 `minimumCliVersion`，或任一 `minimumCapabilities` 在已安装二进制 manifest 中缺失或状态不是 `supported`
- **THEN** canary 必须以结构化错误 fail closed；成功证据必须固定 Skills 版本、CLI 最低版本、完整能力列表和全部 supported 断言，并由三平台汇总器逐项绑定当前技能锁

### Requirement: 技能版本锁
插件 SHALL 仅消费 `jianying-skills` 发布版本并验证 ref、commit 和逐技能摘要；本地修改副本必须导致分发校验失败。

#### Scenario: 同步入口资产与 GitHub 发布元数据绑定
- **WHEN** CLI 或 Skills 同步流程从稳定 immutable Release 下载 index 或 manifest
- **THEN** 流程必须读取同一 Release 的资产元数据，要求目标文件名唯一、状态为 uploaded、大小为正、携带 `sha256:` 摘要并使用对应仓库/tag 的正典 URL；在 attestation 和导入前重新计算下载文件大小与 SHA-256，任一不一致均 fail closed

#### Scenario: 插件技能发生漂移
- **WHEN** vendored 技能内容与锁文件摘要不一致
- **THEN** CI 和发布检查失败并指向上游同步流程

#### Scenario: 发布技能通过链接逃逸来源目录
- **WHEN** 已下载的技能 checkout 在技能目录或内容中包含 symlink 或其他特殊文件
- **THEN** 导入器必须在计算摘要和复制前 fail closed，并保留原有技能与 lock；即使链接目标内容能产生与 manifest 一致的摘要也不得导入

#### Scenario: 锁定版本仍包含退休活动契约
- **WHEN** 当前不可变技能锁完整匹配摘要，但版本早于已确认的 Rust Job supporting-reference 修复
- **THEN** readiness、导入器和发布门禁拒绝最终 cutover，直到更高的修复版本实际发布并完成锁定同步

### Requirement: 插件发布证明可恢复
插件发布 SHALL 固定三平台 fresh-install 证据的完整资产集合和 SHA-256，并允许在 immutable Release 已建立但 attestation 尚未可见时幂等恢复验证。公开前上传中断形成的 Draft 只有在已有证据是本次完整集合的逐字节相同子集时才可续传。

#### Scenario: 插件证据 Draft 上传中断
- **WHEN** tag workflow 已创建 Draft 且只上传部分三平台证据
- **THEN** 重跑必须按名称、uploaded 状态、字节长度和 GitHub SHA-256 校验已有资产，只上传缺失证据；完整集合再次验证后才可公开，且不得 clobber

#### Scenario: 插件证据 Draft 含污染资产
- **WHEN** 同 tag Draft 含额外资产，或同名资产的状态、长度、SHA-256 与本次 evidence job 不同
- **THEN** workflow 必须在公开前 fail closed，不得覆盖、删除或锁定污染 Draft

#### Scenario: 同 tag 插件发布并发重跑
- **WHEN** 同一 tag 的多个 release-gate 运行同时到达 publish，或完整 Draft 在初次规划后发生变化
- **THEN** workflow 必须按 workflow/ref 保证同一时刻只有一个运行进入发布区且不取消已运行中的发布；GitHub 可以替换尚未开始的旧 pending 重跑。任何实际获准运行的发布都必须在公开 Draft 前重新读取远端证据资产执行完整状态机校验

#### Scenario: Draft 阶段插件 tag 被移动
- **WHEN** 插件 Release 仍为 Draft，远端 lightweight tag 或 annotated tag 的 peeled commit 不再等于本次插件 checkout
- **THEN** 初次和公开前最终 publication plan 均必须 fail closed，不得将三平台证据锁定到不同插件源码提交

#### Scenario: 插件发布缺少 tag 防篡改规则
- **WHEN** 插件正典仓库缺少覆盖 `refs/tags/v*` 的 active、无 bypass、禁止删除和非快进更新的 tag ruleset，且没有已批准并完整验证的等价 tag-commit 复核策略
- **THEN** 插件 tag 发布预检必须在三平台构建和 Draft 公开前 fail closed，并把该门禁写入结构化证据；CLI 与 Skills 各自由其发布 workflow 验证本仓保护，插件消费端只要求两者已经形成匹配的 immutable Release

#### Scenario: 私有仓套餐不提供 tag ruleset
- **WHEN** GitHub 对 ruleset 查询返回当前私有仓套餐不可用
- **THEN** 只读预检只有在仓库携带明确批准的等价策略、Immutable Releases 已开启，且发布 workflow 在建 Draft 前、公开前和公开后都重新解析 lightweight/annotated tag 的 peeled commit 并绑定发布 checkout 时才可把发布保护标记 ready；缺少任一复核仍以稳定错误码 fail closed，不得把 403 当作“未配置”后自动弱化门禁

#### Scenario: 发布重跑遇到已锁定 Release
- **WHEN** 同 tag Release 已存在
- **THEN** 流水线要求其为稳定 immutable Release，下载全部证据并与本次构建逐文件比较；完全一致时只重试证明验证，任何差异均失败且不得覆盖

#### Scenario: 手工预演三平台 fresh-install
- **WHEN** 通过 `workflow_dispatch` 运行发布门禁而不创建 tag Release
- **THEN** 独立 evidence job 必须汇合 readiness 和三个平台 canary、执行同一最终证据验证器并产出可下载 verification JSON；每个平台证据固定 archive、binary、capability manifest、SBOM 四重摘要，但不因插件仓库尚未启用 Immutable Releases 而提前退出，tag 发布仍必须在完整测试前要求该设置

#### Scenario: Tag 发布缺少远端不可变前置条件
- **WHEN** 插件 tag workflow 启动，而 CLI 或 Skills 的预期稳定 immutable Release 不存在，CLI、Skills、插件任一仓库未启用 Immutable Releases，或插件仓库既无所需 tag ruleset 也无已批准且完整验证的等价 tag-commit 复核策略
- **THEN** contract job 必须在三平台构建前失败，并无论成功或失败都上传结构化远端预检 JSON；同一检查在 `workflow_dispatch` 中仅记录证据，不得阻止本地候选与三平台安装预演继续执行

#### Scenario: 上游平台或契约门禁失败
- **WHEN** contract 或任一 fresh-install 矩阵项失败，导致 readiness 或平台 canary artifact 缺失
- **THEN** evidence job 仍必须运行，容忍下载步骤缺件但由最终证据验证器 fail closed，并上传包含稳定错误类型的结构化 verification JSON；不得因依赖 job 失败而跳过聚合诊断

#### Scenario: 最终 cutover 需要先证明三平台安装
- **WHEN** CLI 和 Skills 已锁定不可变版本、真实宿主验收已完成，但迁移期环境诊断仍使 `runtime.release_surface_rust_only` 成为唯一阻塞项
- **THEN** cutover 必须先在 macOS arm64、macOS x64 和 Windows x64 分别执行无 Cargo fresh-install 与 capability 握手，聚合器只能显式延后该唯一阻塞项；三个 canary 完整通过后才可删除迁移诊断，并重新要求 release readiness、distribution gate 和完整测试集全绿

#### Scenario: Cutover 前仍有其他阻塞项
- **WHEN** cutover readiness 除 `runtime.release_surface_rust_only` 外还包含宿主、制品、技能、身份、摘要、兼容矩阵或许可证阻塞
- **THEN** 聚合器必须 fail closed，三平台 canary 不得授权删除迁移面

#### Scenario: Evidence 资产被混入或 verification 已过期
- **WHEN** evidence 目录除一个 readiness、三个唯一平台 canary 和至多一个 verification 外还有其他 JSON，或已有 verification 的 lock 身份、平台集合、基础文件集合与当前输入不一致
- **THEN** 汇总和发布均 fail closed；不得忽略未知证据或复用旧汇总结果

#### Scenario: Readiness 只有全绿外壳但缺少真实检查
- **WHEN** readiness 声称 `ready=true`，但缺少固定检查项、存在重复 ID、任一检查非 ready，或其中的插件版本、CLI ref/source commit、Skills ref/commit 与当前 checkout/锁不一致
- **THEN** 三平台汇总必须拒绝该报告；空 blocked 列表不能单独作为正式发布证明

#### Scenario: 新增发布契约测试
- **WHEN** `tests/` 新增 Node `*.test.mjs`，包括条件化真实制品或宿主测试
- **THEN** release contract job 自动执行完整测试 glob；不得依赖容易漏项的手工文件列表，真实外部测试只能依据其明确环境前置条件跳过

#### Scenario: 自动同步分支已存在或并发触发
- **WHEN** 定时任务、release dispatch 或人工触发同时更新同一个 CLI、Skills 或 cutover 专用分支
- **THEN** 同类 workflow 串行执行；推送使用刚读取的远端 SHA 作为显式 lease，远端在读取后变化时拒绝覆盖并要求下一次运行重试

#### Scenario: 仓库没有自动化专用标签
- **WHEN** CLI 同步、Skills 同步或最终 cutover 已推送专用分支，而仓库没有预创建对应 PR label
- **THEN** workflow 仍必须创建或更新 PR，不得把未声明标签作为成功路径的强依赖；标签治理不属于制品或运行时真实性证明
