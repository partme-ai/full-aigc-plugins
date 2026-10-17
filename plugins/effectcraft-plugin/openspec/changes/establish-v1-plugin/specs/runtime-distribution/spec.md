# EffectCraft — runtime-distribution

## Purpose

本能力定义 EffectCraft 在 runtime-distribution 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前实现与验收状态以 tasks 和逐场景证据为准。

## ADDED Requirements

### Requirement: EC-RT-001 运行时来源与完整性

运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。

#### Scenario: EC-RT-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行时来源与完整性并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: EC-RT-001-N 边界条件

- **WHEN** 下载内容与锁定摘要不符
- **THEN** 拒绝安装且现有运行时仍可使用

#### Scenario: 并行首次安装与复用
- **WHEN** 两个进程同时安装或复用同一锁定 CLI
- **THEN** 安装互斥等待最多 120 秒，取得锁后核验并复用已原子发布的版本；不存在重复下载或部分安装被运行
- **AND** 超时返回 runtime_install_busy，保留已有安装，不自动重放任何编辑或渲染

#### Scenario: 已安装版本回执损坏或身份漂移

- **WHEN** 复用已安装CLI时，安装回执不是无歧义UTF-8 JSON对象，或其中版本、平台、来源、制品摘要、版本输出与固定锁不一致
- **THEN** 安装器 SHALL 拒绝复用并保留原目录和回执供核对，不覆盖、不重新下载、不自动回退到其他版本
- **AND** 新版本安装失败 SHALL 不改变旧版本的文件和回执；只有完成摘要、许可、完整载荷与实际版本验证的新目录才能原子发布

### Requirement: EC-RT-002 运行能力与隔离升级

适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。

#### Scenario: EC-RT-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行能力与隔离升级并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: EC-RT-002-N 边界条件

- **WHEN** 新运行时缺少计划要求的能力
- **THEN** 执行前报 capability_missing，禁止静默替换工具


#### Scenario: [EC-RT-002-DOWNLOAD-RECOVERY] 原生制品下载的临时中断

- **WHEN** 首用下载锁定原生CLI制品发生SSL EOF、超时、连接中断、短读或408／429／5xx
- **THEN** 安装器 SHALL 丢弃半包并最多执行三次只读下载，之后仍执行原摘要／安全解压／版本检查，不重试原生编辑
- **AND** 证书、权限、磁盘、大小限制、摘要及非临时HTTP拒绝错误 SHALL 不被重试或放宽；固定发行及安装首用另行验收

#### Scenario: 固定命令目录的离线升级差异

- **WHEN** 智能体比较已发布旧覆盖目录和候选固定目录
- **THEN** 入口 SHALL 不安装、不启动原生编辑、不写任务或工程，确定性列出新增、移除、参数合同、技能归属、工作流映射、运行模式路由及原生工具schema变化；未知schema、领域不符、重复身份及歧义JSON SHALL 拒绝
- **AND** 新增／变化合同 SHALL 保持 NOT_RUN，运行时或工具网关变化 SHALL 列出需要重新验收的命令；旧目录缺少模式或工具schema SHALL 显式记录缺失，不视为合同相同或继承历史PASS
- **AND** 覆盖目录生成 SHALL 核对固定反射与原生目录的完整身份集合，新增／缺失／重复命令 SHALL 在写出文档前报 native_registry_drift；模式路由不替代实际enabled状态及逐命令创作验收

### Requirement: EC-DS-001 Owned standalone desktop workflow
Each domain skill SHALL offer `desktop.py run PLAN --output NEW_DIRECTORY` that validates the plan before installation, verifies fixed desktop and CLI identities, starts only its own isolated desktop, confirms the loopback listener belongs to that process, executes the existing full-command bridge gateway, and closes only its owned desktop/MCP processes on success or failure. Photo authentication SHALL use a private token file and the same authorized output root in both desktop and CLI. Unknown editing outcomes SHALL not be replayed.

#### Scenario: First use without a running desktop
- **WHEN** a standalone skill runs a valid plan against empty runtime caches
- **THEN** fixed desktop and CLI are installed, an owned bridge is started and the workflow receipt plus desktop lifecycle receipt are preserved

#### Scenario: Invalid plan or startup failure
- **WHEN** the plan is invalid
- **THEN** no installation or desktop launch occurs
- **WHEN** owned desktop startup or MCP initialization fails
- **THEN** only owned processes are closed, logs and failure receipts are retained, and edits are not retried

#### Scenario: Interrupted command is not replayed
- **WHEN** a standalone desktop workflow is interrupted with an editing request started
- **THEN** completed steps remain preserved, the started request becomes unknown, and failure plus owned-process lifecycle receipts are written before exit code 130

#### Scenario: Ambiguous JSON plan
- **WHEN** a plan contains duplicate object keys or nonfinite numeric values
- **THEN** the runner rejects it before installing or starting a desktop

#### Scenario: Workflow metadata cannot be overwritten
- **WHEN** a command plan names desktop-session.json, desktop.log, .desktop-data or artcraft-domain-command.json as a root deliverable through $output
- **THEN** validation rejects the plan before installation or editing, preserving workflow receipts and owned desktop configuration

#### Scenario: Bounded TLS download recovery
- **WHEN** a pinned desktop download fails with curl TLS handshake exit35
- **THEN** the installer retries at most three total attempts with clean private downloads and bounded connection/request timeouts before any desktop starts
- **AND** other failure classes are propagated without an extra outer retry; archive identity and signature checks remain mandatory

#### Scenario: Native bridge-only GUI tools
- **WHEN** a plan uses one of the nine pinned Effect bridge-only tools
- **THEN** headless preflight rejects it before setup; explicit bridge or owned desktop mode validates its actual live input schema before execution
- **AND** local list/describe exposes the real bridge-only schemas without requiring installation
