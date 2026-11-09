## Purpose

定义智能体如何发现、筛选、组合和验证剪映自带资源与 AI 能力，使创作工作流能够安全使用基础版和专业版的原生内容生产能力。

## ADDED Requirements

### Requirement: Native capabilities are discoverable by domain
系统 SHALL 以机器可读目录区分 `media`、`music`、`text`、`sticker`、`effect`、`transition`、`caption`、`smart_package`、`filter`、`adjustment`、`template` 和 `digital_human`，并保留未知新域而不自动执行。

#### Scenario: Current editor exposes all observed domains
- **WHEN** Adapter 观察到用户截图所示的剪映功能栏
- **THEN** 系统输出每个域的可见性、版型要求、可执行动作和证据等级，不把可见性等同于可用性

#### Scenario: Editor adds an unknown domain
- **WHEN** 新版本出现目录未建模的能力域
- **THEN** 系统记录原始标识并暂停自动路由

### Requirement: Resource selection is goal-driven and auditable
Harness SHALL 根据创作简报、平台、受众、用途、风格、节奏和许可约束检索候选，并 SHALL 保存候选、筛选理由、拒绝理由和最终选择。

#### Scenario: Vlog requests travel resources
- **WHEN** 生活 Vlog 需要旅行画面、轻快音乐、Vlog 贴纸和自然转场
- **THEN** 系统分别检索对应资源域并生成可审阅的候选集合，不使用单一关键词命中直接执行

#### Scenario: Candidate conflicts with commercial use
- **WHEN** 候选资源没有覆盖目标商业用途或发布渠道
- **THEN** 系统拒绝候选并继续筛选其他已授权资源；无合格候选时暂停

### Requirement: Atomic operations and orchestration have separate owners
CLI SHALL 提供目录、搜索、筛选、选择、应用、移除、检查、状态、证据和恢复原子合同；插件 SHALL 负责编译步骤、依赖关系、批准、质量循环和跨资源协调。

#### Scenario: Plugin selects a transition
- **WHEN** WorkflowPlan 决定在两个片段之间使用转场
- **THEN** 插件调用 CLI 预检相邻片段与资源权益，再执行一个可回滚的应用动作

#### Scenario: Published CLI lacks an operation
- **WHEN** 锁定发布二进制未声明计划所需能力
- **THEN** 插件返回缺失 capability，不读取 Rust 源码或调用旧 Python 引擎补偿

#### Scenario: Homepage folder lifecycle is compiled to Rust CLI
- **WHEN** WorkflowPlan 需要查询、创建、移入最近删除、查询回收站或恢复首页本地文件夹
- **THEN** 插件只生成 `home folder` 固定 argv，写操作要求明确批准，执行后再用 CLI 列表命令按精确 ID 复核状态

#### Scenario: Homepage folder capability is partial or absent
- **WHEN** 锁定发布二进制将 `home.folder_lifecycle` 报告为 `partial`、`external_dependency` 或缺失
- **THEN** Harness 在任何写操作前返回 `missing_capability`，不直接编辑剪映配置，不生成 GUI 点击或视觉坐标回退

#### Scenario: CLI mutation cannot be read back
- **WHEN** Rust CLI 返回写入成功，但随后的活动文件夹或回收站回读未出现预期 ID 状态
- **THEN** Harness 将该步骤标记为不明确，保留 CLI 快照路径并停止自动后续步骤，不把“命令已返回”视为业务恢复成功

### Requirement: Harness prefers semantic bottom-level controls
插件 SHALL 根据 CLI 的控制目录选择执行路由，并 SHALL 优先使用草稿协议直接操作，其次使用 Runtime 原生控制，再其次使用可访问性 Adapter；视觉坐标兜底不得成为默认路由。

#### Scenario: Timeline button maps to a draft operation
- **WHEN** 分割、裁剪、移动、删除、关键帧、滤镜、特效或转场能够由发布 CLI 直接表达
- **THEN** WorkflowPlan 编译为对应 Rust 原子命令，不生成 GUI 点击步骤

#### Scenario: Timeline button changes only session state
- **WHEN** 操作目标是撤销、重做、磁吸、吸附、联动、录音或时间线缩放
- **THEN** WorkflowPlan 使用版本绑定的 Runtime Control，并要求调用前后状态证据

#### Scenario: Only a screen coordinate is known
- **WHEN** Adapter 只能识别控件坐标而无法验证语义 ID和状态
- **THEN** 系统禁止生产执行并要求完成该版本的控件探测 Canary

#### Scenario: Surface inventory contains repeated and unresolved entries
- **WHEN** CLI 报告同一语义的多个界面实例，或报告 `unresolved` 图标入口
- **THEN** Harness 保留每个 Surface ID 及来源区域；只对 `supported` 语义编译执行步骤，未知入口不得被过滤、合并或猜测执行

#### Scenario: Parent surface expands into child actions
- **WHEN** Surface Inventory 包含页签菜单、选择工具、联动、预览轴、更多设置或右键菜单等可展开入口
- **THEN** Harness 要求对应版本的子操作清单完成后才报告菜单覆盖完整，并在缺项时输出明确 coverage gap

#### Scenario: Editing gesture has no toolbar button
- **WHEN** 操作通过播放头、标尺、片段拖动、边缘裁切、轨道重排或框选触发
- **THEN** Harness 仍以语义动作和参数编排，不因界面没有独立按钮而遗漏该操作

### Requirement: Smart packaging is a composite workflow
智能包装和智能 B-Roll SHALL 被建模为组合步骤，明确输入素材、目标风格、允许自动修改的轨道、预算、预览、变更集和确认边界。

#### Scenario: Smart B-Roll proposes a package
- **WHEN** 用户选择一键 AI 自动剪辑或智能 B-Roll
- **THEN** 系统先生成包含字幕、花字、音效、特效和补充画面的变更计划，预览和批准后才能写入草稿

#### Scenario: Package changes protected content
- **WHEN** 组合结果删除受保护对白、品牌声明或锁定镜头
- **THEN** 独立验证拒绝该结果并恢复到应用前快照

### Requirement: Digital-human generation has dedicated safety gates
数字人步骤 SHALL 分离形象选择、声音选择、脚本、背景、生成、费用、肖像/声音权利和应用，并 SHALL 对上传与远程生成使用独立批准和账本。

#### Scenario: Stock digital human is selected
- **WHEN** 用户选择剪映提供的数字人形象和声音
- **THEN** 系统记录形象/声音资源 ID、权益要求、脚本摘要、费用上限和生成回执

#### Scenario: Custom likeness or voice is requested
- **WHEN** 请求使用真人照片、视频或声音创建数字人
- **THEN** 系统要求明确的肖像/声音授权和上传批准，缺失时不得提交

### Requirement: Execution closes with independent validation
每个原生能力步骤 SHALL 在执行后重新检查草稿资源、时间线范围、画面/音频结果、版权证据和可恢复快照；GUI 成功提示不得单独满足完成门禁。

#### Scenario: GUI reports success but draft evidence is absent
- **WHEN** GUI 显示下载或应用成功但 CLI 无法在草稿或资源库中验证结果
- **THEN** 步骤进入不明确状态并禁止自动重试

#### Scenario: Composite result passes validation
- **WHEN** 资源身份、权益、时间线变更、代理预览和人工要求均通过
- **THEN** 系统保存证据并允许质量循环进入下一步

### Requirement: Panel capabilities are exposed as independent skills
插件 SHALL 从不可变 `jianying-skills` 发布消费素材、音频、文本、贴纸、特效、转场、字幕、智能包装、滤镜、调节、模板、数字人和剪辑控制台 13 个独立技能。每个技能 SHALL 描述逐级入口、语义动作、能力门禁、执行路由、验证和恢复，不得以技能文本替代 CLI 或 GUI Adapter 的实际能力。

#### Scenario: Agent routes an asset import request
- **WHEN** 用户要求“素材 → 导入 → 素材”
- **THEN** 插件选择素材技能并生成 `media.import.asset` 动线，先探测素材，再通过固定 Rust argv 写入隔离草稿并验证

#### Scenario: A panel action is GUI-only
- **WHEN** 分类技能中的动作没有 supported CLI capability
- **THEN** 插件保留版本绑定 GUI Adapter 和 Canary 门禁，不从 Skill 文本推定成功

#### Scenario: Formal host acceptance covers panel discovery and control flow
- **WHEN** Codex、ZCode 或 Kimi 对当前正式插件版本生成真实宿主 observation
- **THEN** observation 必须分别证明 13 分类发现、分类路由、选择解释、批准、停止、恢复和证据展示，缺少任一检查时不得进入三宿主汇总
