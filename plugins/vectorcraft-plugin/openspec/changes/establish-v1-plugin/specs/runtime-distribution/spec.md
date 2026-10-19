# VectorCraft — runtime-distribution

## Purpose

本能力定义 VectorCraft 在 runtime-distribution 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前实现与验收状态以 tasks 和逐场景证据为准。

## ADDED Requirements

### Requirement: VC-RT-001 运行时来源与完整性

运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。

#### Scenario: VC-RT-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行时来源与完整性并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: VC-RT-001-N 边界条件

- **WHEN** 下载内容与锁定摘要不符
- **THEN** 拒绝安装且现有运行时仍可使用

#### Scenario: 并行首次安装与复用
- **WHEN** 两个进程同时安装或复用同一锁定 CLI
- **THEN** 安装互斥等待最多 120 秒，取得锁后核验并复用已原子发布的版本；不存在重复下载或部分安装被运行
- **AND** 超时返回 runtime_install_busy，保留已有安装，不自动重放任何编辑或渲染

### Requirement: VC-RT-002 运行能力与隔离升级

适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。

#### Scenario: VC-RT-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行能力与隔离升级并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: VC-RT-002-N 边界条件

- **WHEN** 新运行时缺少计划要求的能力
- **THEN** 执行前报 capability_missing，禁止静默替换工具


#### Scenario: [VC-RT-002-DOWNLOAD-RECOVERY] 原生制品下载的临时中断

- **WHEN** 首用下载锁定原生CLI制品发生SSL EOF、超时、连接中断、短读或408／429／5xx
- **THEN** 安装器 SHALL 丢弃半包并最多执行三次只读下载，之后仍执行原摘要／安全解压／版本检查，不重试原生编辑
- **AND** 证书、权限、磁盘、大小限制、摘要及非临时HTTP拒绝错误 SHALL 不被重试或放宽；固定发行及安装首用另行验收

#### Scenario: [VC-RT-002-SCHEMA] 实际能力签名与执行模式

- **WHEN** 显式探测已安装的固定运行时
- **THEN** 核验二进制摘要及版本输出，读取同一只读MCP会话的命令参数签名和工具inputSchema；缺失或变化时拒绝激活
- **AND** headless与bridge独立绑定，不把空文档的enabled状态当作签名，也不静默替换模式

#### Scenario: 编辑器只显示一层正常加载提示
- **WHEN** 编辑器页面加载、MCP 客户端连接或正常打开文件
- **THEN** 包装层 SHALL 从初始 HTML 起隐藏通知浮层，保留引擎自身加载画面，不叠加第二个加载提示

#### Scenario: 启动或导出错误仍可见
- **WHEN** 编辑器启动或操作失败
- **THEN** 包装层 SHALL 显示错误；只有存在可重试导出时才显示导出重试按钮，恢复正常后隐藏错误浮层


### Requirement: VC-DS-002 Verified Vector desktop export alias

The VectorCraft bridge gateway SHALL apply the verified desktop export alias and preserve the complete validation and identity contract specified below.

#### Scenario: Complete execution contract
- **WHEN** the described standalone desktop or bridge workflow is requested
- **THEN** The standalone full-command gateway SHALL map `file.export` to `document.export` only in VectorCraft bridge mode, because the pinned official desktop advertises the engine operation while the CLI advertises its host alias. The gateway SHALL validate the complete mapped registry, check the actual operation's enabled state in the same session, preserve requested and backend command identities in its receipt, and fail on any unrelated missing command. Headless command identity SHALL remain unchanged.

#### Scenario: Export alias on official desktop
- **GIVEN** the pinned desktop has `document.export` and no `file.export`
- **WHEN** a bridge plan requests `file.export`
- **THEN** the gateway calls `run_command` with `document.export`, produces the requested export, and records both identities

#### Scenario: Unrelated registry drift
- **WHEN** any other mapped command is missing
- **THEN** the gateway refuses the workflow before edits

### Requirement: VC-DS-003 Explicit desktop Place registry variants
VectorCraft bridge discovery SHALL normalize only the verified `file.place` engine/UI pair in the pinned desktop registry. It SHALL retain the engine entry and its enabled state; the UI dialog entry cannot enable an otherwise disabled engine command. All unrecognized duplicates, multiple engine variants or multiple UI variants SHALL remain registry errors. Headless discovery SHALL retain strict uniqueness checks.

#### Scenario: Engine Place remains disabled despite UI variant
- **GIVEN** one engine and one UI `file.place` entry in the pinned bridge registry
- **WHEN** the engine entry is disabled
- **THEN** gateway execution remains blocked even if the UI dialog entry is enabled

#### Scenario: Unexpected registry duplicate
- **WHEN** a different command has duplicate entries or the Place variants are not exactly one engine and one UI entry
- **THEN** discovery returns an unknown registry outcome and performs no edit

### Requirement: VC-DS-001 Owned standalone desktop workflow

The system SHALL preserve the complete owned desktop execution contract in the scenario below, including fixed identities, process ownership, authentication isolation and no replay.

#### Scenario: Complete execution contract
- **WHEN** the described standalone desktop or bridge workflow is requested
- **THEN** Each domain skill SHALL offer `desktop.py run PLAN --output NEW_DIRECTORY` that validates the plan before installation, verifies fixed desktop and CLI identities, starts only its own isolated desktop, confirms the loopback listener belongs to that process, executes the existing full-command bridge gateway, and closes only its owned desktop/MCP processes on success or failure. Photo authentication SHALL use a private token file and the same authorized output root in both desktop and CLI. Unknown editing outcomes SHALL not be replayed.

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
