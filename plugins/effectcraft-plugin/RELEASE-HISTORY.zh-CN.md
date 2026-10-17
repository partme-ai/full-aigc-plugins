# 版本绑定的历史发行记录

## dev.65 — 2026-10-09

本次发行 source dev.63／plugin dev.65 包含来源生产任务保护及 commands／自有桌面的公共产物映射：多工程分别登记真实任务、不可变包版本、原生工程、匹配PNG和媒体依赖；旧交付只读兼容。映射可随整包移动重验，不能替代技术、创作或用户验收。原候选报告保留观察时范围；当前发行证据见 [发行验证](docs/evidence/release63-validation-20261009.json)。字体／LUT发现、完整故障矩阵、其他原生平台与固定宿主派发继续开放；5.1–5.3不勾选，V1仍有69项未完成，不归档。

## dev.64 — 2026-10-09

工作流 craft-artifact/v1 血缘、不可变整包版本、源工程包授权与逐步写入检查；15份独立技能资源一致。回归697项633通过／64跳过；macOS arm64三个真实交付通过，其他平台和宿主验收仍开放。插件锁定已发行技能源dev.62；V1仍有69项开放。

Workflow artifact lineage and source-package integrity guards; partial EC-AR-001 implementation. [Evidence](docs/evidence/workflow-artifact-lineage-candidate-20261009.json).

## dev.61 — 2026-10-09

桌面原子冲突逐操作核对及命令完成证明恢复；15份独立资源同步。恢复只登记已核验的原交付，不重发编辑。当前证据见 [发行验证](docs/evidence/release59-validation-20261009.json)。完整V1与目标平台／宿主验收仍开放。

Atomic desktop conflict reconciliation and completion-seal recovery; development release, full V1 remains open.

## dev.59 — 2026-10-09

消费技能源dev.57不可变快照：源工程版本检查与跨账本工程认领保护。同步增量OpenSpec、设计、任务及原始候选证据；9.3.2不勾选，完整V1仍有70项开放。桌面内存版本保护未实现，未纳入本次发行。

Pinned source dev.57 adds source revision checks and shared project ownership. Desktop in-memory guards, full native platform/host acceptance and marketplace admission remain open.

## dev.58 — 2026-10-09

修正新增派发测试在Windows cp1252下读取中文技能清单失败：显式UTF-8，不修改技能运行载荷。替代source55／plugin57发行配对，保留旧标签与失败CI。完整V1仍有70项开放。

Fix UTF-8 decoding in portable routing tests; original failed Windows CI is retained. Execution payloads unchanged, full V1 remains open.

## dev.57 — 2026-10-09

15个技能默认受管理三模式派发；只读预检和旧状态拒绝执行合同通过。源码589项548通过／41条件跳过；本机三模式原生组合证据绑定未变执行资源，完整平台及固定宿主门禁仍开放，V1剩余70项。插件消费技能源dev.55固定发行快照。

Managed routing guidance and native three-mode composition evidence. Full V1 and native platform/host gates remain open. [Routing evidence](docs/evidence/managed-default-routing-20261009.json) · [Native composition evidence](docs/evidence/managed-three-mode-composition-20261009.json).

## dev.56 — 2026-10-09

锁定已发布技能源v0.1.0-dev.54／29fddc504ca2231bcc2d8de7bd7e589142ab656b的15个技能摘要。严格回执身份与统一管理入口9.3.5验收完成，完整V1剩余72项；历史15技能报告不覆盖新载荷，当前完整能力矩阵保持NOT_RUN。

Pins the released source dev.54 for all15 independent skills. Public interface task9.3.5 is verified; complete V1, native platform and fixed-host gates remain open. [Evidence](docs/evidence/managed-public-interface-candidate-20261009.json).

## dev.55 — 2026-10-09

插件 dev.55 消费不可变技能源 dev.53：完整载荷能力证据绑定、历史任务只读保护、直接取消交接原控制器。完整 V1、其他原生平台和宿主验收继续开放。

## dev.53 — 2026-10-09

开发版技能源 dev.51／插件 dev.53：POSIX 私有进程组归属及 nonce 绑定业务结果覆盖守护器丢失、孤儿后代和强制取消。当前回归及离线安装副本证据见 [发布验证](docs/evidence/group-ownership-release51-20261009.json)。下方历史检查点保留原摘要；跨平台原生、固定宿主、创作验收及完整 V1 仍开放。

## dev.52 — 2026-10-09

修正 Windows PowerShell 启动描述缺失时的稳定 bound_entry_invalid 诊断；失败仍拒绝执行、不创建材料、不准备当前 Python。source dev.49 的 Windows CI 失败记录保留，由 source dev.50／plugin dev.52 替代；原发布标签及归档不改写。完整 V1、其他原生平台及宿主验收仍开放。

Fix stable PowerShell missing-entry diagnostics; execution remains fail-closed. Supersedes source dev.49 / plugin dev.51 without rewriting their tags or archives. Full V1 remains open.


## dev.51 — 2026-10-09

技能源 dev.49／插件 dev.51：可信 v2 任务在当前 Python 安装前选择并校验原解释器；新增 CRAFT_RUNTIME_ARCHIVE 离线制品连接，显式参数优先，失败不回落联网。旧 v1 仍可检查，不自动重放。macOS 原生工程重开与完整解码已复核；Windows 原生、固定宿主及完整 V1 保持开放。

### Previous README status checkpoints

未发布的任务入口候选：可信 v2 任务在准备当前 Python 前选择并校验原解释器。当前缓存为空、归档错误且当前 Python 锁损坏时，macOS 隔离3.13.15／原生0.3.1实际恢复、工程重开和12帧解码通过；启动证据缺失／篡改则保留并拒绝执行。已发布 source48／plugin50 快照不变，真实 Windows 入口及完整9.29仍开放。[证据](docs/evidence/task-bound-entry-candidate-20261009.json)。

开发版技能源 dev.48／插件 dev.50 包含安装回执保护及 macOS 隔离 Python／原生版本升级的限定验证：490 项回归（452 通过／38 条件跳过），PowerShell 本机函数 19 例通过。真实 Windows 与固定宿主待验收；新 Python 准备失败仍阻止旧任务恢复（OpenSpec 9.29）。75 项任务及完整 V1 保持开放。[证据](docs/evidence/isolated-python-upgrade-candidate-20261009.json)。

上一原生升级组件：安装回执校验及macOS真实0.3.1→0.4.0活动任务隔离验证通过；486项回归（448通过／38条件跳过）。旧任务保留原代码与Python3.13.5执行文件，新任务使用隔离Python3.13.16及0.4.0；外部旧Python不作为隔离标准库证明。固定source47/plugin49不含此次安装器改动；跨状态根清理、其他平台／宿主及完整V1仍开放。[证据](docs/evidence/runtime-upgrade-component-candidate-20261009.json)。

技能源工作区执行绑定候选通过24项目标及482项回归（444通过／38条件跳过），完成本机限定旧任务原生恢复。9.25已勾选，9.1.4及74项实施任务仍开放；已发布source45/plugin47不含本增量。[证据](docs/evidence/task-execution-binding-candidate-20261009.json)。

开发版技能源45已完成只读doctor／目录任务9.2.1：显式已验证CLI能力发现、恢复argv和离线差异。回归420通过／38条件跳过，15个单技能实际诊断及15次无Python只读诊断通过。开发版source47/plugin49包含本增量，74项实施任务及完整V1仍开放。[证据](docs/evidence/doctor-capabilities-candidate-20261008.json)。

> **开发版 dev.50（2026-10-09）：**技能源 dev.48 新增 Python 和 CLI 安装回执严格校验，记录限定原生升级证据；完整 V1 及其他平台／宿主验收继续开放。


四领域RT-001运行时来源与完整性已完成当前全部场景验收，固定技能字节保持不变；运行时升级与完整首版仍开放。[验收架构](docs/Craft-Fixed-Runtime-Integrity-Architecture.zh_CN.md)。


## dev.50 — 2026-10-09

技能源 dev.48 新增严格 Python／CLI 安装回执校验；插件 dev.50 消费该不可变快照。490 项回归：452 通过／38 条件跳过；PowerShell 本机函数19例通过，macOS 完整隔离发行升级与原生工程／12帧解码通过。任务9.26–9.28为限定组件证据；9.29旧任务入口缺陷、75项开放任务、其他平台／宿主与完整V1未完成。

Strict Python/CLI receipt validation; bounded macOS upgrade and native decode evidence. 452 regression passes / 38 conditional skips; 19 local PowerShell function cases. Old-task bootstrap gap 9.29, 75 tasks and full V1 remain open.

## dev.49 — 2026-10-09

锁定source dev.47：修正新增绑定测试在Windows的UTF-8读取，15个技能执行载荷与dev.48相同。dev.48草稿由本版替代，保留不可变标签。完整V1与74项任务继续开放。

Pins source dev.47 with the Windows UTF-8 test correction. Runtime payload is unchanged from dev.48; supersedes its draft without rewriting tags. Full V1 stays open.

## 开发版 dev.48 — 2026-10-09

锁定技能源 dev.46 不可变快照，15 个技能包含任务私有执行快照及原运行时绑定。24 项绑定测试及482项回归（444通过／38条件跳过），含本机 macOS 限定原生恢复证据。任务9.25组件完成；74项任务、跨版本清理、目标平台与固定宿主验收及完整V1仍开放。

## 开发版 dev.47 — 2026-10-08

固定技能源 dev.45，修正 Windows 短/长路径测试身份断言。15 个技能快照与插件 dev.46 字节一致；独立核验技能源测试修复，完整 V1 仍开放。


## 开发版 dev.46 — 2026-10-08

固定技能源 dev.44：15 个独立技能新增只读 doctor、恢复执行参数及离线命令/schema 差异。运行时绑定草稿不纳入本版，74 项任务和完整 V1 仍开放。


开发版dev.45锁定source dev.43不可变快照：共享PNG资源记账及修订只读核对；任务9.23限定范围完成。源码388项回归通过、38项条件跳过。75项任务及完整V1继续开放，marketplaceEligible=false。证据：docs/evidence/command-revision-resource-candidate-20261008.json。

开发版dev.44固定技能源dev.42：限定范围局部修订和原生保全回执。40项目标测试；回归365通过／38条件跳过。命令视觉修订通过，桌面中断尚未验收。9.23、76项任务及完整V1保持开放。[证据](docs/evidence/command-revision-candidate-20261008.json)。

插件dev.43固定技能源dev.41：任务9.22命令／桌面Judge v2及不可变账本集成具有限定macOS原生抽样评价证据。76项任务仍开放，任务9.23局部修订草稿不进入运行快照；完整V1及新安装宿主验收继续开放。

插件dev.42固定技能源dev.40。命令及自有桌面保存工程/PNG质量组件9.21通过macOS arm64验证；75项任务仍开放，新固定宿主派发及完整V1尚未验收。

插件dev.40锁定技能源dev.38（0f7d95b6be9eeb45060dce1170f786dc859474ac）：Judge v2、不可覆盖评价账本、序列验证及过期回执诊断。源码298项中260通过/38条件跳过；完整V1、固定宿主及其他平台创作验收开放。

插件 dev.39 固定技能源 dev.37（8babe4b187b2f8d6de6f494d1bf1437e794946c5）：隔离Python、受管理任务、自有分段恢复与共享重试预算。本机原生组件验收及源码213通过/38条件跳过；完整V1及其他目标平台/宿主仍开放。[证据](docs/evidence/managed-orphan-retry-component-20261008.json)。

以下记录逐字移自 README 前部，描述各自版本，不作为当前安装合同。

固定EffectCraft插件dev.32／源dev.30通过本领域每个技能的独立冷安装、7项安装保护和1项冷原生创建／重开／返工／导出。三个更新领域合计41个独立空缓存、21项保护和3项原生验收通过，全部64安装摘要保持不变。Art捆绑升级与完整V1另行验收。[证据](docs/evidence/craft-three-domain-output-guards-fixed-first-use-20261007.json)。

EffectCraft 技能源dev.30候选在原生会话前保护公开工作流目标：7项保护测试、120项源回归（32项需显式环境的测试跳过）及1项实际冷原生创建／返工／重开／导出通过。完成记录绑定实际计划、原工程与运行时摘要。固定安装与Art捆绑升级分别验收。[证据](docs/evidence/effectcraft-output-execution-candidate-20261007.json) · [架构](docs/EffectCraft-Output-Execution-Architecture.zh_CN.md)。

固定插件31／源29跟踪验收通过：15技能发现零错误，原生冷任务与公开计划冷创建／重开通过，12关键帧保全，15安装摘要不变，两公开附件核验通过。 [Evidence / 证据](docs/evidence/effectcraft31-fixed-tracking-first-use-20261007.json).

领域场景验收现为 **43项原生测试通过／全部42个不同场景技能**。固定安装跟踪用例使用受支持H.264 High通过；此前无损输入不受原生解码器支持，失败证据保留。Art角色专项、实际Skills CLI及完整V1仍开放。 [Evidence / 证据](docs/evidence/craft-fixed-tracking-supported-input-20261007.json).

追加专项验收：**累计42项原生测试通过，覆盖41／42个领域场景技能**。多机位、带时间文本转录、滤镜及Puppet补验通过；Effect跟踪视频纹理未出现在预期像素，分析实际关键帧为0，尚未验收。64个安装摘要保持。Art角色专项、自动ASR、实际Skills CLI和完整V1继续开放。[证据](docs/evidence/craft-fixed-additional-task-scenes-20261007.json)。

已安装专项技能首用：**38项原生测试／37个不同领域场景技能通过**，各自使用独立空运行时。Film多机位／转录、Photo滤镜、Effect Puppet／跟踪五项尚未纳入本业务门禁；Art角色专项任务与通用Skills CLI另行验收。全部64安装摘要不变。[证据](docs/evidence/craft-fixed-installed-task-scenes-first-use-20261007.json)。

当前固定版本首版代表任务通过：四领域已安装技能各自使用新公开运行时缓存，验证可编辑原生工程、重开、局部返工及导出。覆盖短片字幕／配音同步与素材移动、片头改字保留动画、海报图层／蒙版／PSD／尺寸变体、矢量布尔／多画板／SVG-PDF-PNG／改色。全部64安装摘要不变。本证据仅覆盖四个代表任务，不等于完整首版或所有专项场景。[证据](docs/evidence/craft-fixed-v1-representative-native-baseline-20261007.json)。

逐技能独立冷启动：**64／64通过**（macOS arm64、Python3.13.5，620.155秒）。每个单技能分别使用独立空运行时与默认公开下载；锁定原生版本和命令发现通过，安装技能摘要不变。通用Skills CLI安装及完整首版仍开放。[证据](docs/evidence/craft-fixed64-every-skill-cold-first-use-20261007.json)。

当前插件：`0.1.0-dev.32`；技能源：`0.1.0-dev.30`。已同步输出执行保护；源冷原生创建／返工和保护测试通过，固定安装通过，Art捆绑集成与完整V1仍开放。

固定安装复验：五插件共62技能在隔离Codex宿主中加载成功，加载错误0；62技能完整命令查询与场景资源核对通过，248项安装失败诊断检查通过；四个新增专项技能的空运行时安装、版本与查询通过。原生创作、全量命令和完整V1按各自证据验收。[安装证据](docs/evidence/craft-fixed62-installation-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.28`；技能源：`0.1.0-dev.26`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次新固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.27`；技能源：`0.1.0-dev.25`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次新固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

固定安装诊断检查：58技能发现通过，184项诊断检查通过；四领域固定副本仍缺失安装脚本本身不存在时的补充修复，当前验收为部分完成。Art插件dev.92锁定技能源dev.66。[证据](docs/evidence/craft-first-use-diagnostics-installed-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.26`；技能源：`0.1.0-dev.24`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次新固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

本次固定版本追加原生验收：Art十项冷启动、四领域四项GUI编辑与保存重开，以及品牌色局部返工、依赖更新和交付打包通过；全量命令、全部GUI和创作质量仍待验收。[证据](docs/evidence/craft-fixed-scene-guidance-20261007.json)。

固定安装场景指引验收：五插件58技能发现与内容摘要、示例引用及完整命令查询通过；四领域运行脚本与锁和示例保持原固定版本身份。Art新分发十项实际冷启动复验通过，全量命令和完整V1仍开放。[证据](docs/evidence/craft-fixed-scene-guidance-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.25`；技能源：`0.1.0-dev.23`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次固定安装发现、场景资料与代表原生任务复验通过，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.24`；技能源：`0.1.0-dev.22`。完整反射命令入口、独立CLI与桌面安装已提供；固定版本58项独立冷启动、四领域进阶GUI保存／重开／渲染及Art混合返工通过。逐条原生命令执行验收与完整V1保持开放。[固定验收记录](docs/evidence/craft-full-command-fixed-first-use-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.23`；技能源：`0.1.0-dev.21`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。候选源码48项冷启动通过；本次固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.22`；技能源：`0.1.0-dev.20`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。候选源码48项冷启动通过；本次固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史 CLI 验收（原固定版本范围）：当前固定版本的 58 个技能全部通过独立冷启动：单技能目录、空运行环境、公开安装、版本查询及完整命令发现。此证据不代表 2639 条命令全部执行通过或完整场景验收。 [Evidence](docs/evidence/codex-current58-cold-cli-first-use-20261007.json).

历史发行记录：当前首次使用入口：插件 `0.1.0-dev.21`，技能源 `0.1.0-dev.19`。中英文安装与命令指南按当前固定发行核验；历史样例证据保留原版本范围。 [Guide](docs/Craft-Native-Gateway-Usage.zh_CN.md).

固定原生命令网关首用通过：48项领域安装技能与十项 Art85／技能源58 的公开入口独立冷安装、创建／重开／导出、返工并保全原交付。公开 Brief、四领域网关、五子工程、Logo选择性更新／无关图标复用、移动包、真实取消和六类未知回复故障通过；58项安装摘要不变。全2639命令／GUI／模型／通用Skills CLI／完整V1门禁保持开放。[使用指南](docs/Craft-Native-Gateway-Usage.zh_CN.md) · [固定证据](docs/evidence/codex-native-gateway-first-use-20261007.json)。



## 历史 README 原文 — 2026-10-09

[完整原文（保留原版本和证据边界）](README-HISTORY-20261009.zh-CN.md)
