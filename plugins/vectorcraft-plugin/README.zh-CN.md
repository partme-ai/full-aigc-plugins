# VectorCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.6`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


**插件边界**：当前开发候选包含根 `plugin.json`、`mcp.json`、技能与随包stdio编辑器适配器。dev.65内嵌VectorCraft0.12，新增三条场景并修复宿主导出保存。下方锁定技能和Harness历史证据仅对应其标注版本，不代表当前候选已取得完整资格或真实宿主安装验收。

开发 plugin37／source33 修复完整网关品牌返工遗漏变体。原生候选通过，固定安装验收另行执行。[架构](docs/VectorCraft-Brand-Gateway-Export-Architecture.zh_CN.md)。

固定插件36／技能源32通过13项独立原生冷安装、26项真实工作流测试和52个误改拒绝案例。64安装身份保持；51项未变技能复用已复核的历史冷启动证据。Art内置升级与完整V1仍开放。[固定验收](docs/VectorCraft-Fixed-Brand-Guard-Architecture.zh_CN.md)。

固定安装外观技能新增“同色但未绑定 token”验收：仅已绑定消费者更新，非消费者原生属性、无关 SVG／PNG／PDF 与原交付保持不变。本轮复用运行时，不关闭新增 V1 任务。[验收架构](docs/VectorCraft-Same-Color-Token-Architecture.zh_CN.md)。

四领域RT-001运行时来源与完整性已完成当前全部场景验收，固定技能字节保持不变；运行时升级与完整首版仍开放。[验收架构](docs/Craft-Fixed-Runtime-Integrity-Architecture.zh_CN.md)。

Logo、图标与品牌图形需求进入，交付 `.vectorcraft` 及适用的 SVG、PDF、PNG。

当前插件：`0.1.0-dev.20261017.6`；技能源：`0.1.0-dev.47`；25个可发现技能，包含冻结基础技能和开发场景。历史资格仍绑定原始载荷；完整V1验收仍开放。

插件55／源41增加SVG实际图像范围及摘要绑定的技术披露门禁；最小任务4.13／4.14通过，4.15当前无界面场景验收通过。[架构](docs/VectorCraft-Exchange-Scope.zh_CN.md)。

开发插件53锁定技能源39：SVG记录实际文字导出模式，轮廓导出明确报告文字编辑性损失，并保留原生文字及字体依赖；三个公开文字修改入口统一要求显式对象ID。源回归151项通过、30项跳过，原生候选验证单独记录；固定52验收与完整V1任务仍开放。[文字交付架构](docs/VectorCraft-Text-Outline.zh_CN.md)。

公开固定51／源38已完成VC-DM-002全部四个当前场景，任务4.6完成：14组原生工作流、8组受控授权、2组原生SDK选择／子树拒绝，17项目标源测试通过；13技能摘要未变，9个Harness登记组停止。已知／未知失败在真实原生操作成功后显式注入，不是引擎缺陷报告；GUI、全Pathfinder上下文与创作拓扑判断保持独立。 [固定验收 / Fixed acceptance](docs/evidence/vectorcraft-boolean-fixed51-20261009.json).

公开固定51／源38的VC-DM-001全部两场景已验收，任务4.3完成：六组真实原生保存／重开与18份导出，覆盖Pixels／Points、文档／画板局部坐标、控制点、开闭路径和可见描边；四类错误合同保留原产物并报告实际对象ID。七项几何回归通过，13技能摘要未变、6个登记组停止；不提升任意变换、GUI或创作验收。 [固定验收 / Fixed acceptance](docs/evidence/vectorcraft-geometry-fixed51-20261009.json).

候选51将显式budgetId作为同一工作流的共享取消边界：持久封存所有活动成员与新任务／步骤，旧连接也受门禁约束；每个原生组分别停止、逐个核验原产物后才结算epoch。到期恢复先取消，耗尽次数／预留输出额度在新登记前拒绝。公开固定51五组真实验收、115项Node与43项Python回归通过，任务3.9已完成。[架构](docs/VectorCraft-Shared-Cancellation.zh_CN.md)。

公开固定插件50／实际宿主源38已通过全部七个当前VC-TX-002场景：13组真实原生崩溃／恢复、109项Node、43项Python回归，13技能摘要保持，30个登记进程组停止。持久GO授权与恢复封存互斥，原位置文件及已完成回执经核验后结算，不自动重放。任务3.6完成，当前96项完成／31项开放；完整取消预算、GUI、模型与V1验收分别保留。[固定逐场景证据](docs/evidence/vectorcraft-task-recovery-fixed50-20261009.json)。

插件49绑定已完成步骤回执、运行时身份、清单及全部文件摘要；核验后替换回执拒绝结算，旧检查缺少步骤摘要需重新检查。源38在重命名前持久记录真实交付目录身份，覆盖链接素材打包子目录；普通／链接工程的回执前后四个真实崩溃候选场景通过。公开固定49／实际宿主源38已通过四个场景及97项Node、43项Python回归；13技能摘要保持，该版证据不单独关闭3.6。[固定证据](docs/evidence/vectorcraft-receipt-recovery-fixed49-20261009.json)。

插件48补充恢复前的源依赖快照摘要校验；真实保存与9项导出完成后、回执写入前的协调器SIGKILL恢复通过，保持原输出且不重放。84项Node、43项Python回归通过。公开固定48／源37的隔离宿主安装及上述原生场景已通过；13技能摘要保持不变，该版证据不单独关闭任务3.6。[固定证据](docs/evidence/vectorcraft-source-recovery-fixed48-20261008.json)。

固定48实现的新增非空链接验收通过：真实链接PNG缺失、修改以及检查后再次修改均拒绝恢复／结算，保持原失败工程位置、inode与源占用；15项恢复回归通过。由当前外部验收脚本调用已安装固定48，该版证据不单独关闭3.6。[证据](docs/evidence/vectorcraft-linked-recovery-fixed48-20261009.json)。

插件47进一步在探测后、启动时和监督期间复核已解析物理根目录与请求路径；将原根目录或输出父目录替换为重定向链接时，在任务登记前拒绝。公开插件47及该宿主实际加载的技能源37通过全部七个VC-TX-001场景、77项Node、43项Python与10项真实原生合同案例；任务3.3在该版完成，当时32项OpenSpec任务开放。[固定证据](docs/evidence/vectorcraft-single-writer-fixed47-20261008.json)。

源清单、继承计划与依赖现已绑定版本，并复制为逐文件核验的只读执行快照；编辑前同时占用原源工程和物理输出，旧SQL连接亦受输出门禁约束。原生分支、GUI改后冲突、崩溃交接候选通过。[源与单写合同](docs/VectorCraft-Source-Single-Writer.zh_CN.md)。公开插件46／技能源37在macOS arm64通过已记录原生场景，但授权根目录替换边界仍开放。[子集证据](docs/evidence/vectorcraft-single-writer-fixed46-20261008.json)。该版本未关闭3.3；当前验收以固定47为准。

公开插件45／技能源37通过隔离Codex安装、63项Node与43项Python回归，已安装副本的真实取消与协调器崩溃恢复通过；13技能摘要保持不变。[固定安装证据](docs/evidence/vectorcraft-recovery-fixed45-20261008.json)。这些是有限恢复案例，本轮不关闭额外V1任务。

恢复入口现于原生检查前核验保留的技能、计划与控制文件身份；缺少原控制摘要的旧未完成任务继续保留占用。真实取消与协调器崩溃用例已通过，均不自动重放。[恢复合同](docs/VectorCraft-Recovery-Snapshot.zh_CN.md)。任务3.3／3.6／3.9已有固定版本逐场景验收；完整V1仍开放。

授权入口现于异步探测前固定调用方范围、输入摘要及物理路径，并要求暂存父目录具有写入授权。三个协调器回归案例覆盖这些边界；完整任务3.3及V1验收仍开放。

公开插件44／技能源37通过隔离Codex安装与13技能发现；已安装副本57项Node、43项Python回归通过，全部技能摘要保持不变。[固定安装证据](docs/evidence/vectorcraft-authorization-fixed44-20261008.json)。本次不关闭额外V1任务。

运行时能力与隔离升级（任务2.6）已通过公开插件43／技能源37的完整逐场景验收：默认冷启动、真实版本及bridge排空、双进程竞争、迁移快照与旧连接预算回滚均已验证。[固定安装证据](docs/evidence/vectorcraft-runtime-upgrade-fixed43-20261008.json)。仅覆盖声明支持的macOS arm64；该版验收时其余32项OpenSpec任务开放。

已验证首次使用平台：macOS arm64、Python 3.11+。固定运行时安装在用户数据目录，技能文件保留在宿主加载目录。当前为开发版本；完整首版验收及通用 Skills CLI 实际安装仍未完成。

维护者来源校验拒绝符号链接、不完整锁及版本同名分支，并在替换任一管理技能前检查全部声明来源；已发布技能／运行时身份保持。[快照预检架构](docs/Skill-Snapshot-Self-Contained.zh_CN.md)。

## 首次使用

在宿主中调用 **`vectorcraft-use`**。直接使用 CLI 时，将 `SKILL_DIR` 设为宿主实际加载的 `SKILL.md` 所在绝对目录；可能位于用户／项目 `.agents/skills`、插件内部或宿主缓存，以实际路径为准。以下入口在调用前安装并核验固定运行时。

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- --version
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- commands
```
<!-- CRAFT_FIRST_USE_END -->

实际制作、所需输入、原生工程和局部修改参见[可编辑工作流](skills/vectorcraft-use/references/workflow.md)。[安装与技能入口](skills/vectorcraft-use/SKILL.md) · [版本绑定历史](RELEASE-HISTORY.zh-CN.md)。版本与命令查询验证安装和发现，不代表创作完成。

[首次使用入口证据](docs/evidence/craft-readme-first-use-navigation-20261007.json)。

固定安装路径验收：独立技能及 Art 混合工作流在含中文和空格的路径下，通过原生创建与重开、定点返工及导出；Art 另验证移动交付包。技能与运行时身份保持不变。该结果仅覆盖 macOS arm64 的本次首次使用场景。 [路径验收证据](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

固定发行前的历史源码候选：结构损坏的 runtime／Node 锁在写运行时目录或下载前返回本地恢复诊断。五项候选原生首次使用通过；发布插件快照保持不变，新不可变发行安装需另行验收。 [锁诊断候选](docs/VectorCraft-Lock-Shape-Architecture.zh_CN.md).

---

固定原生首次安装与完整命令恢复验收通过：新版五插件58技能逐项独立冷安装，十个Art技能分别安装四领域；四个原生下载半包SSL EOF恢复、72个原生保存后故障、四个健康命令返工及混合HD返工／恢复／移动包通过，全部安装摘要保全。仅关闭领域2.10／8.11与Art4.10；2639条命令逐项、GUI、模型、通用Skills CLI及完整V1仍开放。 [版本及证据](docs/evidence/codex-native-download-first-use-20261007.json).

历史发行记录：当前插件：`0.1.0-dev.21`；技能源：`0.1.0-dev.19`；包含渐变／多重外观计划，12 项固定安装冷启动场景通过；Art 更新分发待验证，完整 V1 仍开放。

固定发布前的候选记录：原生下载恢复候选：最多三次只读重试并丢弃半包；此前固定版本冷安装遇到SSL EOF失败，修复后的固定安装验收仍开放。

历史插件版本记录 `0.1.0-dev.18`／技能源 `0.1.0-dev.16` 固定完整命令内层JSON修复；实际安装首用复验进行中。

当前固定失败暂存验收：插件 dev.17、独立技能源 dev.15。全部58项独立CLI冷启动、24个原暂存原生故障案例及37原生场景＋6合同检查通过；Art77领域包升级仍开放。[证据](docs/evidence/codex-failed-stage-first-use-20261007.json)。

固定领域客户端首用复验：Film 插件 dev.16／技能源 dev.15，Effect／Photo／Vector 插件 dev.15／技能源 dev.14。隔离 Codex 发现58项零错误；实际安装副本24类保存后故障、四个健康公开工作流和已发布 Art 引擎＋安装后 Vector 客户端六类故障通过，全部58项安装摘要保全。Art dev.75 内置旧领域分发包尚需升级，全量命令／GUI／模型验收仍开放。[版本绑定证据](docs/evidence/codex-public-workflow-session-first-use-20261007.json)。
先前固定版本协议故障首用复验通过：48个独立技能源共288例，实际安装副本24例及四领域健康返工通过；58项安装摘要保持一致。验收范围与固定标签见 [协议故障验收记录](docs/evidence/codex-protocol-fault-first-use-20261007.json)。全量逐命令／GUI验收以及Art领域包升级仍开放。

协议故障修复候选：本领域12项技能逐个单独复制、空运行时公开安装后，原生保存成功再注入六种坏回复全部通过（72例，零跳过）。不重放、未知回执、工程重开与交付／技能保全均已检查。[证据](docs/evidence/protocol-fault-first-use-20261007.json)。固定安装副本与Art领域包升级仍为独立门禁。

固定插件 0.1.0-dev.13／技能源 0.1.0-dev.12 已通过安装后的返工门禁：隔离 Codex 发现全部58项技能零加载错误，本领域安装技能从空运行时直接执行文档创建／返工计划、保存重开与非目标保全。全部58项安装摘要不变，当前固定发行CI通过。[固定返工证据](docs/evidence/codex-complete-command-revision-first-use-20261007.json)。全量命令／GUI／模型验收保持开放。

本领域 12 个技能逐个单独复制、从各自空运行时公开安装后，配套返工计划全部通过（79.101 秒，零跳过）。[返工证据](docs/evidence/complete-command-revision-first-use-20261007.json)。更新快照的真实固定宿主安装另设门禁。

完整命令入口补充了配套的创建／返工 JSON 示例、重新打开后的显式选择前置条件，以及原生保存重开、非目标对象与像素检查。每个独立技能均包含两个可执行计划。[调用指南](skills/vectorcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision)。全量逐命令及 GUI 验收保持开放。

先前固定发行首用通过：隔离 Codex 0.153.4 发现全部 58 项技能零加载错误；每项安装技能独立空运行时公开安装（385.234 秒）；安装后的领域新命令入口及 Art 1080p 混合返工／恢复／移动包检查通过。全部安装摘要保全，固定 CI 与五包重建通过。[版本绑定证据](docs/evidence/codex-complete-command-first-use-20261007.json)。通用 Skills CLI、全命令／GUI 与完整创作验收仍开放。

## 完整原生命令入口

全部 12 项独立技能分别从空运行时使用公开锁定 CLI 附件安装，随后完成创建、保存重开、领域参数及渲染检查（74.946 秒，零跳过）。[逐技能冷首用证据](docs/evidence/complete-commands-cold-first-use-20261007.json)。本轮覆盖每项技能的完整命令代表样例；全命令／GUI 和实际宿主安装另行验收。

已发布开发快照：skills dev.11 / plugin dev.12；固定宿主首用代表门禁通过。

585 条命令现在均有逐项参数说明、技能归属与同会话调用入口。运行 `commands.py list / describe / check / run`；原生状态按实时 enabled 校验。旧工作流的 27 项交付合同保留。GUI 命令需显式 bridge，命令目录覆盖不代表全量验收。

[架构与操作指南](docs/VectorCraft-Complete-Commands-Architecture.zh_CN.md) · [逐项参考](skills/vectorcraft-use/references/command-reference.md) · [可运行示例](skills/vectorcraft-use/examples/commands-advanced.json)

独立技能驱动的可编辑矢量品牌资产与多画板设计.

[English](README.md) | [简体中文](README.zh-CN.md)

## 当前版本与可复现宿主验证

此前完成宿主验证的插件/技能源版本：`0.1.0-dev.3`。Codex 0.147.0 与 0.153.4 均安装五个固定公开发布，发现全部 58 项启用的命名空间技能，加载错误为零，来源摘要一致。五项代表流程已通过 0.147.0 安装后的场景技能入口验证，包括原生工程、局部修订和 ArtCraft 在线混合流程。模型自动派发、桌面 GUI、创作最终评审和完整交换保真尚未验证。

[宿主验证设计](docs/VectorCraft-Host-Verification-Architecture.zh_CN.md) · [绑定版本的证据](docs/evidence/codex-skill-suite.json)。历史里程碑保留原证据范围；当前版本身份以 manifest 和锁文件为准。

> 开发版已通过固定标签的 Codex 安装、技能发现和原生代表工作流；完整产品与创作验收仍未完成。

独立技能包已进入实施，单技能隔离安装已在 macOS arm64 实测；完整创作流程与插件宿主验收仍未完成。[证据](docs/evidence/bootstrap-tests.json)

独立技能现已包含原生工作流助手：已实测形状与路径、布尔合并、可编辑文字、双画板、SVG/PNG/PDF 导出和定向改色。验收样例中未绑定对象及其导出保持不变，完整插件验收仍待完成。[工作流证据](docs/evidence/vector-workflow-tests.json)

## 定位

制作 Logo 与图标资产，交付 .vectorcraft、SVG 和 PNG；修改品牌色后更新所有绑定的变体，并保留无关颜色。

面向需要原生可编辑工程、反复修改和可靠自动化的创作者。

## 一眼了解

```text
Intent + assets
  -> independent Skills (pinned development release)
  -> public skill workflow / ArtCraft adapter
  -> verified runtime / child adapter
  -> native project + preview + export + evidence
```
| Property | Value |
| :--- | :--- |
| Plugin ID | vectorcraft |
| Metadata version | 0.1.0-dev.20261017.6 |
| Stage | implementation-in-progress |
| Skills source | vectorcraft-skills / v0.1.0-dev.47 |
| Execution | 上游 CLI；ArtCraft 使用子适配器 |
| Host compatibility | 公开dev.64/source46的Codex安装与13项冷启动已验证；模型派发和完整宿主验收开放 |
| License | Apache-2.0 (original repository content) |


## 能力与边界

| 能力 | 行为边界 | 状态 |
| :--- | :--- | :--- |
| 路径形状与坐标 | 定义画板坐标、单位、路径控制点、闭合性与描边；不可把预览像素当成路径事实。 | 待完整验收 |
| 组合与布尔操作 | 记录参与对象 ID、布尔运算与结果对象身份，保留修改前检查点；操作失败不丢失原对象。 | 待完整验收 |
| 品牌色与文字 | 以显式 token 绑定品牌色而非全文件颜色替换；保留文本内容与字体依赖，轮廓化输出记录可编辑性损失。 | 待完整验收 |
| 画板与变体 | 每个画板有稳定 ID、名称、尺寸和输出映射；预览顺序与导出范围明确，避免索引基准混淆。 | 待完整验收 |
| 交换格式能力范围 | 原生 .vectorcraft 与 SVG、PDF、PNG 分别验证；遇到不可交换效果时报告栅格化范围并保留原工程。 | 待完整验收 |
| 品牌变体更新 | 根据 token 与素材依赖更新相关变体，核对无关对象属性与输出没有变化。 | 待完整验收 |

不重写上游编辑引擎，不暗中改变原生交付格式，不宣称 GUI 或跨平台验收完成。

## 架构与文档

- [完整运行时架构](docs/VectorCraft-Runtime-Architecture.zh_CN.md)
- [技术方案与路线](product-docs/VectorCraft/5%E3%80%81VectorCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md)
- [V1 PRD 与需求映射](product-docs/VectorCraft/V1/5%E3%80%81VectorCraft-PRD%E6%96%87%E6%A1%A3-V1.md)
- [完整文档导航](docs/README.zh-CN.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [专业领域技术设计](docs/VectorCraft-Domain-Design.zh_CN.md)

## 当前可执行的快速开始

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
以上校验文档和规范，不运行产品工作流。OpenSpec 校验使用 1.13.1；本仓不自动安装工具。

已安装官方 CLI 后可执行基础检查：

```bash
vectorcraft-cli --version
```

本次记录结果为 0.2.0。独立技能的 bootstrap 与 workflow 是当前开发版入口；插件安装与技能发现已有证据；完整宿主验收仍待完成。

## 配置与运行时

目标配置包含 CLI 路径、允许读写根目录、运行模式、预算、超时与输出目录；配置 schema 尚待实现。技能锁文件固定已发布的独立技能源提交与内容摘要。运行时锁文件中的摘要来自真实官方制品，只证明已记录平台的基础运行。

## 可靠性与安全

规划要求：单工程写入锁、版本前置条件、持久化意图、幂等键、不明确结果核对、原生工程检查点、产物摘要及受限修订。密钥只通过宿主秘密引用传递；素材元数据不作为执行指令。

## 验证与成熟度

[脱敏 CLI 证据](docs/evidence/runtime-baseline.json)

| 层面 | 状态 |
| :--- | :--- |
| 上游 CLI 与只读 MCP | 已观察，仅 macOS arm64 |
| 独立技能与适配器 | 技术工作流已验证；完整 Harness 待完成 |
| 原生工程与创作验收 | 原生技术用例通过；创作质量待验收 |
| 目标宿主安装 | Codex 受控安装与发现通过；完整宿主验收待完成 |


## 路线与贡献

| 阶段 | 交付 | 进入下一阶段条件 |
| :--- | :--- | :--- |
| D0 | 双语文档与 OpenSpec 基线 | 文档、链接、规范校验通过；实现任务仍未完成 |
| M1 | 独立技能与运行时适配 | 清洁环境安装、摘要检查、真实 MCP 调用 |
| M2 | 专业领域完整闭环 | 代表任务、工程重开、输出解码、局部修改 |
| M3 | ArtCraft 跨插件协作 | 版本传播、局部失效、断线恢复与幂等 |
| M4 | 宿主与发布验收 | 宿主实装与多平台证据；市场清单一致 |

先更新 OpenSpec 再实现行为；每项任务通过实际验收后才能勾选。中英文文档同时维护。参考 CONTRIBUTING.md 与 AGENTS.md。

## 许可与上游

原创内容遵循 [Apache-2.0](LICENSE)。这是第三方集成规划，不代表上游背书。四款应用的代码许可与 ArtCraft/Services 的受限许可分别处理；不复制上游 ArtCraft/Services 代码或品牌资产。

[Upstream VectorCraft](https://github.com/storytold/vectorcraft) · [Issues](https://github.com/full-aigc-plugins/vectorcraft-plugin/issues)

独立技能现已绑定当前已发布开发标签 `v0.1.0-dev.4`，`skills.lock.json` 固定来源提交与整个技能摘要。使用 `python3 scripts/vendor/skill_vendor.py check` 核对。技能源快照发布不代表宿主验收或生产完成。

## 开发版独立技能安装与使用

安装独立技能：`npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-use`。安装技能后，从其真实目录运行公开入口；插件快照也包含相同技能。

```bash
python3 -I -B skills/vectorcraft-use/scripts/bootstrap.py
python3 -I -B skills/vectorcraft-use/scripts/workflow.py --help
```

首次入口会安装锁定官方 CLI 到用户数据目录；要求 macOS arm64 与 Python 3.11+。使用技能内示例计划并提供真实素材；交付与修订合同见技能的 SKILL.md。[来源与校验证据](docs/evidence/skill-publication.json)。

## Codex 开发版宿主验证

五个插件已在隔离 Codex 配置中从公开标签安装，app-server 发现带命名空间的技能且无加载错误；安装缓存中的 ArtCraft 入口已交付四种原生工程。[宿主证据](docs/evidence/codex-installation.json)。此为受控开发验收，不代表桌面 GUI、其他宿主、完整创作或正式市场发布通过。

开发版本 `0.1.0-dev.1` 同步独立技能的安装锁等待修复；并行安装和复用按有界互斥协调，原生任务不自动重放。

当前开发里程碑为原生交付增加摘要绑定的交换损失报告，区分 lost、observed、unknown；派生导出不替代原生工程。跨编辑器字体、效果和蒙版保真尚未验证，完整交换验收任务保持未完成。

## CLI 与场景技能体系

技能源包含 12 项可独立安装的技能，分为安装、CLI 公共操作与场景任务。[架构与清单](docs/VectorCraft-Skill-Suite-Architecture.zh_CN.md)。运行时与插件版本分别维护；旧宿主证据保持原版本范围。

历史插件版本记录版本：`0.1.0-dev.5`；技能源版本：`0.1.0-dev.4`。命令示例以宿主实际加载的 `SKILL.md` 所在目录调用脚本。全部技能在用户、项目与插件三种含空格布局中通过隔离入口检查。[路径证据](docs/evidence/installed-skill-paths.json)。此前宿主验证仍对应其记录版本，既有安装需更新。

插件 `0.1.0-dev.5` 从固定公开标签重新取快照并修正整个技能摘要，未带入本地 Python 缓存。插件标签 `v0.1.0-dev.4` 的摘要误包含被忽略的开发缓存，已被替代，不可安装该标签。

历史插件版本记录 `0.1.0-dev.6` 固定技能源 `0.1.0-dev.5`。九类场景技能各自冷安装并完成真实原生操作，验证显式选择、图像嵌入、符号复用与无关画板保护；完整回归 38 项、零跳过。[证据](docs/evidence/task-skill-first-use.json)。完整创作、GUI 与模型派发验收仍未完成。

当前固定发布的宿主核验（2026-10-06）：Codex 0.153.4 安装五个当前固定插件，加载全部 58 技能并逐项核对内容身份。本插件代表性原生工作流从实际安装路径调用，在新的原生运行时中完成创建、重开和修订检查；五工作流调用后，全部 58 个技能摘要保持不变。[证据](docs/evidence/codex-current-release-20261006.json)。显式标签生成器由 ArtCraft 统一持有。模型派发等待授权，GUI、创作与完整宿主验收仍未完成；本次 QA 维护不改变已发布技能/运行时内容或标签。

当前固定发布矩阵（FilmCraft dev.6、EffectCraft dev.7、PhotoCraft dev.6、VectorCraft dev.6、ArtCraft dev.17）在隔离 Codex 安装后通过 58 技能发现及原生代表工作流；执行后所有技能摘要保持不变。[宿主安装内容的原生验证](docs/evidence/codex-release17-native-20261006.json)。此证据不代表模型调度、GUI 或完整创作验收。

补充安装后品牌导出验证通过：选定 Logo／字标改色后，SVG 色值与 PNG 解码像素同时更新；无关图标属性及第二画板 PNG 保持不变。本次使用已核验运行时缓存，不是新的冷安装，也不证明自动推导 token 依赖。[证据](docs/evidence/brand-export-color.json)。插件及技能源发布标签保持不变。

原生 RGB 全局品牌色板工作流已通过单独复制 appearance 技能的首次在线冷启动验证，脚本与示例均来自同一技能；关联 SVG／PNG 更新、独立图标与旧工程保留有真实原生证据。独立技能源 v0.1.0-dev.6 已发布，插件 v0.1.0-dev.7 已发布；实际宿主安装后的单技能在线冷启动原生验证通过（6.487 秒），全部 58 个安装技能摘要保持一致。实际 npx 独立安装和模型派发仍待验证。详见 [品牌色架构](docs/VectorCraft-Brand-Tokens-Architecture.zh_CN.md) 与 [验证记录](docs/evidence/native-brand-token-first-use.json)。

原生中文文字修订通过单技能冷启动：明确对象修改保留首样式、独立页脚与旧工程；缺失字体停止交付，可用字体依赖写入清单。技能源 dev.7 与插件 dev.8 已发布；实际安装后的单技能在线冷启动原生验证通过（8.275 秒），全部 58 个安装摘要不变。[架构](docs/VectorCraft-Chinese-Text-Architecture.zh_CN.md)、[证据](docs/evidence/native-chinese-text.json)。

较早技能源 dev.7 的完整原生回归 42 项全部通过，零跳过（111.204 秒），包含九个独立任务场景、品牌色板与中文文字。任务场景使用全新公开缓存；命令发现和基线原生工作流明确复用已核验缓存。[证据](docs/evidence/dev7-full-native-suite.json)。

固定已安装插件 dev.8／技能源 dev.7 的补充验收验证四种矩形布尔操作、原生复合孔洞方向、SVG／PNG／PDF 独立解码、原交付保全和无效选择拒绝；不扩展为任意几何或编辑器往返支持。[验收记录](docs/VectorCraft-Boolean-Geometry-Acceptance.zh_CN.md)。

历史固定 dev.8 首次使用缺口，已由 dev.9 修复：无关画板 SVG 保留画板外品牌路径，品牌色修订后发生内容变化，其 PNG／PDF 保持不变。维护版原生运行时已发布，修复版不可变技能／插件快照尚待发布。[复现与修复边界](docs/VectorCraft-Artboard-Export-Gap.zh_CN.md)。

本地维护版 CLI 候选 `0.2.0-craft.1` 已通过 954 项引擎测试、12 项 CLI 集成测试及三画板单技能隔离安装任务；品牌改色后，无关 SVG／PNG／PDF 保持字节一致。12 个源技能安装器已支持维护版版本识别与来源记录。此段记录较早的本地候选阶段；维护版运行时现已发布，固定技能／插件验收仍待完成。[候选证据](docs/evidence/native-artboard-svg-candidate-20261006.json)。

已发布的维护版原生运行时通过工作区单技能 HTTPS 冷安装任务（4.970 秒）。不可变技能／插件发布和 ArtCraft 接入仍待完成。[证据](docs/evidence/public-artboard-svg-runtime-20261006.json)。

插件 dev.9 收录不可变技能源 dev.8，锁定维护版原生 CLI 0.2.0-craft.1。源原生回归 46 项全部通过、零跳过；固定 dev.9 宿主首次使用及 ArtCraft bundle 更新仍待完成。[源原生回归](docs/evidence/maintained-full-native-suite-20261006.json)。

固定公开插件 dev.9／技能源 dev.8 已通过 Codex 发现全部 58 个技能，以及实际安装后的单导出技能公开冷启动原生验收（4.985 秒）。全部 58 个安装技能摘要不变。OpenSpec 4.22 的领域验收已完成，ArtCraft bundle 更新与完整 V1 验收仍待完成。[固定安装证据](docs/evidence/codex-vectorcraft9-artboard-first-use-20261006.json).

插件 dev.10 收录不可变技能源 dev.9，锁定维护版 CLI craft.2。稳定 PDF 创建日期与摘要绑定的日期记录通过 49 项完整原生回归；固定新宿主与 ArtCraft 混合验收仍待完成。[日期架构](docs/VectorCraft-PDF-Date-Architecture.zh_CN.md)、[原生测试](docs/evidence/craft2-full-native-suite-20261006.json)。

固定 ArtCraft dev.50／VectorCraft dev.10 的 Codex 0.153.4 隔离首次使用通过：五插件 58 技能发现、零加载错误；单导出技能空运行时跨秒原生验收 1 项通过（8.108 秒），混合品牌返工 2 项通过（51.409 秒），全部安装摘要保留。[发行绑定证据](docs/evidence/codex-release50-vector10-stable-export-first-use-20261006.json)。通用 Skills CLI 安装、模型／GUI、完整领域与创作验收仍开放。

本次更新的 22 个技能逐项公开冷启动全部通过（159.811 秒）：每项只复制自身目录到 .agents/skills，独立空运行时完成版本与命令合同检查，目录摘要和全部宿主安装摘要保留。该证据不代表通用 Skills CLI 安装或全部创作场景。

登记素材技能源候选：公开工作流已接入 PNG 链接、SVG 嵌入、JPEG／SVG 替换、原生依赖收集与迁移。[架构](docs/VectorCraft-Asset-Handoff-Architecture.zh_CN.md)。既有固定插件快照未改动；新版发布与安装宿主复验仍待完成。

插件 dev.11 收录不可变技能源 dev.10，接入登记 PNG／SVG 置入、JPEG／SVG 替换与原生依赖收集。本版安装宿主验收与 ArtCraft 分发升级分别进行，完整 V1 验收保持开放。

固定插件 dev.11／技能源 dev.10 已通过 Codex 0.153.4 公开标签安装与发现：58 项技能、零加载错误。安装后的素材／导出单技能空运行时原生测试 2 项通过、零跳过（4.855 秒、6.743 秒）；12 项 VectorCraft 技能逐项独立冷安装通过（56.275 秒）。实际核验链接／嵌入 PNG、SVG、JPEG／SVG 替换、移动后直接重开原生工程及无关画板保全，全部 58 项安装摘要保持不变。[固定证据](docs/evidence/codex-vectorcraft11-assets-first-use-20261006.json)。ArtCraft 仍消费旧 Vector bundle，分发升级与混合首次使用仍待完成。

当前固定发行领域场景矩阵：FilmCraft dev.10、EffectCraft dev.9、PhotoCraft dev.10、VectorCraft dev.11 共 37 个原生场景及 6 项合同检查通过，零跳过。每个场景仅复制对应安装技能，从空运行时目录使用默认公开附件安装原生 CLI；核验原生工程、实际像素／音频及局部修改保持，全部 58 项安装身份保持一致。[版本绑定证据](docs/evidence/codex-current-domain-task-matrix-20261006.json)。完整首版、通用 Skills CLI 安装、模型派发、GUI 与创作验收仍开放。

公开工作流回复检查已同步领域技能源候选，并通过有界原生／Art 协议验证。新的固定领域和 Art 分发包仍待发行与实际安装验收。[候选架构](docs/VectorCraft-Complete-Commands-Architecture.zh_CN.md) · [证据](docs/evidence/public-workflow-session-candidate-20261007.json)。

失败暂存候选：公开工作流保留原生暂存原路径、依赖摘要、最后提交请求与已完成回执，禁止重放；固定发行与安装副本验收仍开放。[架构](docs/VectorCraft-Failed-Stage-Architecture.zh_CN.md)。

固定领域失败暂存首用门禁已通过：Film插件18／源16，其他领域插件17／源15；五插件58技能发现零错误，全部58项独立空运行时CLI冷启动通过（417.646秒），实际安装副本24个真实保存后故障直接重开产品保留的原工程及依赖，四个健康创作／返工通过。全部安装摘要和16项固定插件CI保持通过；源仓未提供CI运行，仅有本地回归。只关闭领域OpenSpec3.12；Art77内置旧领域源，4.9升级和完整V1仍开放。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

固定安装场景矩阵通过37个原生场景及6个合同检查，零跳过。Photo测试已从安装后的技能锁读取维护版原生版本，CLI与安装技能未修改。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


完整命令内层JSON修复候选：非有限值、溢出和重复键在绑定返回值前记录unknown，真实保存后九类故障与原工程重开通过。这是候选技能源证据，固定发布与实际安装复验尚未完成；逐命令／GUI门禁仍开放。

渐变与多重外观：12 项独立技能的源候选冷启动与原生返工验证已通过；固定安装与 Art 分发待验证。 [Architecture](docs/VectorCraft-Appearance-Gradient-Architecture.zh_CN.md).

固定安装渐变／多重外观：12 项技能通过，控制对象与原交付保全；Art 更新分发仍开放。 [Evidence](docs/evidence/codex-vectorcraft-gradient-first-use-20261007.json).

## 桌面安装组件（候选源码）

每个领域技能自带固定桌面安装、自动启动与完整命令工作流入口。使用当前技能实际目录运行 desktop.py run PLAN --output NEW_DIRECTORY；保留原生工程、命令与生命周期回执。源码48项冷启动已有证据，本次固定版本的实际安装复验仍待完成。见 [桌面使用架构](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

命令计划 JSON 源候选：重复键在安装和创建输出前被拒绝，全部 13 个领域技能的独立副本拒绝测试与有效计划校验通过，3 项专项测试通过。固定插件发布和安装后复验仍为 NOT_RUN。[证据](docs/evidence/command-plan-json-candidate-20261007.json)。

严格计划解析的固定安装复验通过：64 个 CLI 探测、54 个独立安装领域技能的 324 次重复键拒绝、54 次有效计划结构检查，以及四领域空缓存原生保存／重开／渲染实例通过；执行后全部 64 个安装技能摘要不变。仅关闭本次修复的发布门禁；通用 Skills CLI、Art 领域包升级、全部命令上下文和完整首版仍开放。[证据](docs/evidence/command-plan-json-fixed-first-use-20261007.json)。

场景安装示例已使用实际加载的技能自身目录。源路径／布局检查通过；固定安装运行时验收另行记录。 [Architecture / 架构](docs/Scenario-Own-Path-Architecture.zh_CN.md).

新场景自身目录已通过固定安装复验；64项宿主身份匹配。完整V1仍开放。 [Evidence / 证据](docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).

固定独立安装边界验收：全部 64 个当前技能的自身安装器／CLI 共 128 个不可用归档失败案例通过；错误保留本技能 setup 路径，无重试／原生启动，源副本摘要不变。四领域 SK-002 按当前精确锁验收；Art SK-002 和通用 Skills CLI 实际安装仍开放。历史 CLI 红灯为本轮重建，不冒充旧运行。[证据](docs/evidence/craft-fixed-setup-boundary-20261008.json)。

公共协议来源已固定到 ArtCraft v0.1.0-dev.109：[引用与校验说明](docs/Craft-Protocol-Authority.zh_CN.md)。这项检查核对协议来源，完整运行时协议验收仍未完成。

此前已验证的固定协议引用发行矩阵（Film／Effect dev.37、Photo dev.36、Vector dev.34、Art dev.107）已通过隔离 Codex 安装／发现 64 项技能、16 项实际安装所有者文件摘要核对，以及五个全新领域缓存下的 64 项独立公开 CLI 探测。原生场景证据仅对字节一致的技能复用，完整首版仍开放。[固定发行证据](docs/evidence/craft-protocol-authority-fixed-first-use-20261008.json)。

本次插件固定协议引用升级至 ArtCraft dev.109；技能快照保持原固定来源，新的实际宿主安装矩阵正在验证。完整首版与运行时协议验收仍开放。

固定发行 Film38／Effect38／Photo37／Vector35／Art109 已通过实际隔离 Codex 安装和发现 64 项技能、16 项安装副本协议文件摘要核对、五个全新领域缓存下的 64 项 CLI 探测。十项 ArtCraft 技能分别从空缓存完成原生 Photo 蒙版调整、源工程返工与迁移打包；另外 54 项技能仅复用整个技能摘要一致的历史原生证据。默认维护验收矩阵已更新；通用 Skills CLI 安装、模型调度、GUI 和完整 V1／协议验收仍开放。[本次固定证据](docs/evidence/craft-archive-prefix-fixed-first-use-20261008.json)。

固定插件 dev.37／技能源 dev.33：13 个实际安装技能副本各自空缓存安装原生 CLI，直接与网关返工均继承并导出三画板九份 SVG／PNG／PDF；关联颜色改变，无关图形及原交付字节保持，显式空列表与篡改拒绝通过。其余51项复核未变身份并沿用历史首用记录。Art116 内置 Vector32 尚未升级；完整 V1 未完成。[固定验收证据](docs/evidence/craft-vector37-gateway-export-fixed-first-use-20261008.json)。

## 优化实施

[当前固定身份](docs/current-identity.json)和[分层证据索引](docs/evidence-index.json)区分已发布技能与源码候选。根运行时锁为历史基线，执行版本由各已安装技能自身锁决定。插件本地SQLite编排和单轮评审模块已进入开发实现；本地测试不等于完整取消、重启、宿主／模型或首版验收。参见[实施指南](docs/VectorCraft-Optimization-Implementation.zh-CN.md)。

### dev.38 开发预发布

本版锁定技能源 dev.35。此前 dev.37／source33 的安装与候选执行报告保留原始摘要，按历史证据索引。本地回归与 CI 不代表新版本宿主安装、模型路由、全命令执行或完整 V1 验收；市场准入仍为 false。

### 固定 dev.38／source35 技术验收

Codex 0.153.4 在全新隔离配置中安装并发现13技能。13项独立空缓存原生启动、12项声明创建／返工合同通过，setup仅验证安装职责。两条工作流入口22项保存后协议异常、完整命令9项故障、10项安装／输出前歧义计划拒绝，以及品牌边界和九导出保全通过。关闭9.3／9.6；模型路由9.9、依赖它的9.18及完整V1仍开放。[绑定证据](docs/evidence/vectorcraft-fixed38-optimization-20261008.json)。source36为尚未发布的合同说明修正候选。

### dev.39 开发预发布

锁定技能源 dev.36，修正返工对象 ID 渲染说明；新增 `review-checked`，持久化真实解码报告、共享预算和重启后的文件绑定。技术失败阻止接受，未执行检查保持待处理。6.2 最小实现完成；6.3 原生工程完整验收、9.9 模型路由和完整 V1 仍开放。dev.38 固定安装证据保留为历史记录，本版尚未重新执行宿主安装验收。

### 受限修订源码候选

持久化轮次、共享预算、停滞、原生执行谱系及最佳候选保存的最小实现已完成，6.4／6.5已勾选。本增量纳入开发版dev.40，固定dev.39发行不变；两项真实颜色返工使用测试注入评分，完整6.6与真实创作验收仍开放。[合同与操作](docs/VectorCraft-Revision-Cycle.zh-CN.md)。

### dev.40 几何与修订开发版

原生几何合同核对单位、画板偏移、控制点、闭合性与描边，并持久化回执；受限修订循环保留最佳候选。任务4.3已通过固定51验收；6.6、宿主与创作验收继续开放。[几何合同](docs/VectorCraft-Geometry-Contract.zh-CN.md)。

### 布尔事务独立源码候选

独立技能源加入保留检查点、实时参与／结果ID与明确部分失败后的恢复，链接素材检查点可随交付迁移。当时dev.40阶段4.4／4.5已完成，完整4.6及固定快照接收仍开放；已发布dev.40／source36保持不变。[架构](docs/VectorCraft-Boolean-Transactions.zh-CN.md)。

### dev.41结构修订开发版

锁定技能源37的布尔检查点与Harness显式structure授权，核对实际选择、参与子树、结果ID及未选模型字段。旧source36和插件40保持不变。当时source37阶段完整4.6、宿主／模型／GUI和创作验收继续开放。

固定dev.41／source37已通过实际隔离Codex0.153.4安装：13技能身份、13次独立公开冷启动、12组声明创建／返工及8项受控结构验证，安装摘要保持。[固定证据](docs/evidence/vectorcraft-fixed41-structural-20261008.json)。当时dev.41阶段完整4.6、模型派发、GUI及创作验收仍开放。

运行能力与隔离选择新增源码候选已实现：固定版本／摘要、实时命令和工具schema、同账本任务排空及兼容回退门禁。42项Node回归及9项原生场景通过；不同版本升级与desktop验收仍开放，发布插件41保持不变。见[入口与边界](docs/Runtime-Gate.zh-CN.md)。


普通Harness首用现已自动执行计划验证、固定安装与实际命令／工具schema核验；同版本并发复用选择，已完成任务按原回执读取。源码候选46项Node、5项空缓存／并发／拒绝场景与8项结构回归通过；已发布插件41不变，完整2.6仍开放。见[默认首用门禁](docs/Runtime-Gate.zh-CN.md)。

公开固定51／源38已完成VC-TX-003全部五场景验收，OpenSpec任务3.9已勾选：五组真实原生用例、115项Node与43项Python回归通过，13技能摘要保持、13个登记组停止。见 [固定取消与预算验收](docs/evidence/vectorcraft-budget-cancel-fixed51-20261009.json)。完整V1、GUI、模型、其他平台与市场资格保持开放。

开发53补齐历史测试字节归档，修正52 CI的历史证据依赖失配。公开固定52已通过实际宿主13技能发现、两种原生文字导出及18项入口拒绝；[有限验收记录](docs/evidence/vectorcraft-text-smoke-fixed52-20261009.json)。4.7–4.9已按固定53逐场景证据完成，完整V1仍开放。

公开固定53／源39完成VC-DM-003全部四场景，任务4.7–4.9完成，当前102项完成／25项开放。8组品牌误改注入、正常品牌／同色隔离、中文返工及独立重开、原位置文字拒绝、两种SVG文字模式、18项入口拒绝和30项目标源测试通过；13技能摘要保持不变。故障为QA显式注入，字体状态仅来自原生库，不声称GUI、全富文本或跨编辑器保真。[逐场景证据](docs/evidence/vectorcraft-brand-text-fixed53-20261009.json)。

任务4.10／4.11的测试与最小实现门禁已完成，当前105项完成／22项开放；4.12完整验收证据见文末。[映射候选证据](docs/evidence/vectorcraft-artboard-mapping-candidate54-20261009.json)。

公开固定54／源40已通过Codex0.153.4隔离安装与13技能发现，实际安装副本三种成功映射、四种拒绝及14份输出解码通过，13技能摘要保持；复用已核验运行时。仅映射子集，不关闭完整4.12。 [Fixed subset evidence](docs/evidence/vectorcraft-artboard-mapping-fixed54-20261009.json).

固定54／源40的VC-DM-004四个当前场景已完成验收，任务4.12标记完成，当前105项完成／22项开放。31项原生边界、单导出技能空运行时首用、同工程跨秒PDF及局部品牌修改后的无关SVG／PNG／PDF字节一致性通过，13技能摘要保持。未知绘制范围以原生空子图层实测，并结合固定上游源码确认None语义；跨画板群组记录为完整依赖。源回归190项中160通过／30跳过，GUI、模型、其他平台和完整V1仍开放。 [Full scenario evidence](docs/evidence/vectorcraft-artboards-fixed54-20261009.json).

历史子集记录（正式验收见下）：插件55／源41增加SVG栅格范围披露与技术门禁。实际原生矢量／实时滤镜／展开栅格三类工程重开、九份输出解码和四类披露故障拒绝通过；4.13／4.14完成，当前107项完成／20项开放，4.15固定安装验收待执行。[交换范围](docs/VectorCraft-Exchange-Scope.zh_CN.md)。

历史子集记录（正式验收见下）：公开固定插件55／源41通过Codex0.153.4隔离安装与13技能发现，实际安装副本的三类原生重开、九份SVG／PDF／PNG解码和四类披露拒绝通过，13技能摘要保持，运行时复用。仅关闭4.13／4.14，107项完成／20项开放；4.15仍缺不可交换实时效果的自动导出退化或明确拒绝，以及原始效果工程保全验收。显式effect.expandAppearance案例不代替该证据。 [Fixed subset evidence](docs/evidence/vectorcraft-exchange-fixed55-20261009.json).

历史子集记录（正式验收见下）：补充固定55自动自由渐变退化验收：未调用展开命令，SVG实际产生32×22内嵌PNG，局部范围12,16,60,40；三格式独立解码、七类拒绝通过。原生渐变独立重开后可在新修订编辑，源工程和原导出摘要保持。4.15仍待正式规格闭环核验，GUI、模型和完整V1保持独立验收。 [证据](docs/evidence/vectorcraft-exchange-automatic55-20261009.json).

固定55／源41的VC-DM-005-P与VC-DM-005-N两个当前场景完成正式核验，任务4.15标记完成，当前108项完成／19项开放。自动自由渐变直接导出SVG产生32×22内嵌PNG，报告局部范围12,16,60,40及无损声明阻断；原生工程独立重开后可编辑渐变，新修订保留源工程与既有交付。SVG／PDF／PNG分别解码，七类披露与格式异常拒绝通过；六项证据校验测试含五项重新散列后的缺失／篡改拒绝。GUI、模型、其他平台、通用往返保真和完整V1仍未验证。 [Evidence](docs/evidence/vectorcraft-exchange-qualified55-20261009.json).

插件56锁定独立技能源42，登记品牌素材的栅格／SVG消费者只按真实回执替换；原生SVG导入缩放缺口通过实例边界校正修复。十项目标单元测试、源172通过／30跳过回归、原生九份素材输出与三份无关输出字节保全通过；色板两入口及八类误改拒绝回归通过。候选阶段完成4.16／4.17；固定完整验收见下。 [Evidence](docs/evidence/vectorcraft-brand-variants-candidate56-20261009.json).

固定插件56／源42在Codex0.153.4隔离安装副本通过VC-DM-006全部六个当前场景，13技能摘要保持。品牌色板两入口、八类误改拒绝、登记栅格／SVG各两实例替换、九份素材输出解码、三份无关SVG／PDF／PNG字节保全、未知色板及两入口符号链接清单拒绝通过；失败检查点独立重开且不重放。任务4.18完成，当前111项完成／16项开放。GUI、模型创作质量、其他平台、全部素材格式、跨文件／外部编辑器、Art捆绑包和完整V1分别保持未验。 [Evidence](docs/evidence/vectorcraft-brand-variants-fixed56-20261009.json).


插件57锁定源43，新增摘要绑定的可移动产物血缘和公开语义完整性校验。真实原生创建、移动重开、修订及五类拒绝候选通过；源177通过／30跳过，插件73项Python通过。5.1／5.2完成（113/127），固定安装验收5.3仍开放。 [Evidence](docs/evidence/vectorcraft-lineage-candidate57-20261009.json).


插件58修正公开校验的导入方式，保持安装技能字节不变。57真实CI缓存写入失败记录保留；只读回归在57失败、58通过。本地74项Python通过，固定58验收仍待完成。 [Evidence](docs/evidence/vectorcraft-lineage-candidate58-20261009.json).


公开58／源43实际安装于Codex0.153.4 macOS arm64，已通过当前VC-AR-001三个场景：原生创建、整包移动重开、父版本绑定修订及公开七案例校验。13项安装摘要保持不变。5.3关闭，总体114/127完成，13项开放；创作与其他平台验收独立。 [Evidence](docs/evidence/vectorcraft-lineage-fixed58-20261009.json).


插件59／源43补齐SVG／PDF／PNG交换报告的统一校验：原生与重开记录身份、派生物角色、保守字体／效果状态及符合原生设置的SVG文字损失。已复现安装58的PDF替代误放行；候选三输出解码、20类拒绝和85项Python测试通过。固定任务5.6仍开放。 [Evidence](docs/evidence/vectorcraft-exchange-delivery-candidate59-20261009.json).


公开59／源43实际安装于Codex0.153.4 macOS arm64后，通过当前VC-AR-002三个场景：原生独立重开、文字／自由渐变仍可编辑、三输出解码及20类拒绝。13项技能摘要未变，5.6关闭；115/127完成，12项开放。GUI、创作、外部编辑器保真及其他平台独立验收。 [Evidence](docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json).

插件60／源43将解码器、进程启动器和本地交换损失依赖一起绑定到只读执行快照。首次交接或重启后依赖变化均使旧评审失效，旧格式检查证据需重新检查。三项目标测试、118项Node与92项Python本地通过。任务6.3仍开放；115/127完成，12项开放。[本地证据](docs/evidence/vectorcraft-quality-checker-candidate60-20261009.json)。

插件61修复公开回执入口重启后跨已声明只读根目录的误拒绝：恢复已持久化技术检查授权，拒绝回执自行声明根目录。固定60缺口已由公开CLI红灯复现；119项Node与19项真实原生边界候选通过，任务6.3固定61验收仍开放。[候选证据](docs/evidence/vectorcraft-quality-roots-candidate61-20261009.json)。

公开插件61／源43实际安装于Codex0.153.4 macOS arm64，通过VC-QA-001当前三个场景与19项真实原生边界。三输出解码通过；QA注入满分回执不能覆盖损坏PNG／PDF／SVG，真实缺少解码器保持NOT_RUN。文件／检查器漂移、预算先于只读副本、超时停止及协调器SIGKILL重启不重放均通过；13技能摘要保持。12项证据测试含11项重签后缺失／篡改拒绝通过。6.3关闭；116/127完成，11项开放。真实创作判断、GUI、其他平台、6.6及完整V1分别未验。 [Evidence](docs/evidence/vectorcraft-quality-fixed61-20261009.json).

插件62修复评审到达时预算已耗尽的状态：持久停止并保留最佳可验证候选；无法再次支付封存时，核验身份和只读权限后复用已付费的技术检查副本。已复现公开61真实原生缺口，候选62以相同四次共享尝试保留更高分原生修订；122项Node通过，含三项新增回归。评分明确为QA注入；任务6.6完整验收仍开放，116/127完成、11项开放。 [Evidence](docs/evidence/vectorcraft-revision-budget-candidate62-20261009.json).

公开插件62／源43经Codex实际隔离安装，真实原生预算边界再次通过：四次共享尝试内保留更高分只读原生候选，源工程与控制文字保全，13技能摘要未变。本补充不关闭新任务；6.6完整四场景验收继续开放。 [Evidence](docs/evidence/vectorcraft-revision-budget-fixed62-20261009.json).

公开62／源43新增三项真实原生修订：小幅提升不足阈值仍停滞但保留新最佳、降分保留旧最佳、轮数上限停止。签名桌面独占bridge修改并保存源工程后，旧建议在执行前被拒绝，共享尝试保持2且无新修订输出；最佳副本保全。10项证据校验测试通过，13技能摘要未变。评分是QA注入；6.6完整四场景仍开放，116/127完成、11项开放。 [Evidence](docs/evidence/vectorcraft-revision-limits-fixed62-20261009.json).

插件63修复目标变化的停止分支：先校验原有授权及可信技术评审，再持久记录最新问题；原目标最佳候选保持独立可验证，重复观察不重复推进。公开62真实原生流程复现旧问题回传缺口，三个回归测试先失败、修复后14项目标测试通过；候选另通过15项原生授权／新鲜度／谱系边界。固定63与6.6完整验收仍待验证，不关闭新任务。 [Evidence](docs/evidence/vectorcraft-revision-goal-candidate63-20261009.json).

公开插件63／技能源43实际安装于Codex0.153.4 macOS arm64，通过VC-QA-002当前四个场景：6次真实原生修订、15项授权／新鲜度／显式反馈／谱系与保全守卫、1次独占签名桌面源工程修改。预算耗尽、停滞、轮数上限及目标变化均持久停止，保留对应最佳可验证候选并报告最新问题；目标变更授权／可信来源缺口已修复。15项证据测试含14项重签篡改拒绝通过，13技能摘要保持。6.6完成；117/127完成、10项开放。QA评分仅验证控制机制，真实创作判断、其他平台、全部命令及完整V1分别未验。 [Evidence](docs/evidence/vectorcraft-revision-fixed63-20261009.json).

VC-RL-001两场景完成：发布者只读门禁分别核验插件结构、独立技能源、运行时、宿主加载、真实任务和原生交付。12项门禁测试先因缺少目标行为失败，最小实现后通过；另4项证据校验通过。实际隔离包中文档与OpenSpec均通过时，仅文档证明仍被门禁拒绝；原有有界记录保持原范围。复用未变化的公开63／源43实际安装、6次原生修订与独占桌面证据，并重新校验当前摘要，本轮没有新增原生或模型运行。7.1–7.3完成，120/127完成、7项开放；marketplaceEligible仍false，supportedPluginHosts仍空。权限与秘密、全命令、模型路由、完整分发和真实创作仍待独立验收。 [Evidence](docs/evidence/vectorcraft-release-gate-20261009.json).

权限与秘密边界正在实施：本地候选已限制七类子进程入口的环境继承、禁止向错误输出转发原始子进程诊断、拒绝素材附加指令字段及明确命名的字面凭据；失败评审回执也不得将此类凭据写入审计表。8项定向测试和132项Node回归通过，146项Python测试通过；实际原生修订及后续技术检查消耗4次共享预算，相关进程组停止。本候选尚未公开固定分发或完成宿主秘密引用合同，7.4–7.6继续开放，当前仍120/127完成、7项开放。原发布63／源43不变；旧发布证据不得为改动后的工作树放行。该校验不声称识别任意正文中的秘密。 [Evidence](docs/evidence/vectorcraft-permissions-candidate-20261009.json).

候选64已锁定公开技能源44（e5f8e1bb8528），旧63／源43保持不可变。源44的183项回归通过、30项跳过、6项目标测试及13项真实独立冷安装通过；候选插件132项Node与146项Python回归通过，实际原生修订和后续技术检查消耗4次共享预算并停止相关进程组。源44主分支和标签CI通过；插件64仍未公开固定分发，宿主秘密引用、完整权限入口审计与VC-RL-002全部场景尚待完成，7.4–7.6继续开放，总体120/127完成、7项开放。 [Evidence](docs/evidence/vectorcraft-permissions-integration-candidate64-20261009.json).

候选插件64现锁定公开源45（a4b1e624818f）。源45的28项权限测试、193项回归（48跳过）、13项真实独立冷安装及原生修订／三导出／独立重开通过，包含真实GUI保存重开和绕过Python预检后的内核拒绝。当前插件132项Node／146项Python回归及原生修订检查通过，4次共享预算内停止所有拥有的进程组。旧源44快照与执行记录按原始字节归档。Python素材预检授权、实际宿主秘密引用与固定插件64权限验收仍开放；120/127完成、7项开放，候选64未发布，V1及市场资格未获得。 [Evidence](docs/evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json).

候选64现锁定公开源46（91092712e427）。本次补充可信Python素材根与文件描述符安全复制，14项授权测试、28项原生权限测试、13项独立冷启动，以及实际受管创建／继承返工的6个导出、2类启动前拒绝和拥有进程组停止证明。源45证据保持历史归属。Node父进程预检审计、宿主秘密引用及固定64验收仍开放；120/127完成、7项开放，不授予V1及市场资格。[证据](docs/evidence/vectorcraft-permissions-assets-integration-candidate64-20261009.json)。

Node父进程素材读取竞态已复现并修复：过滤环境的Python摘要入口复用固定技能描述符读取器，并沿用冻结根。133项Node／146项Python及实际受管原生创建／继承返工的6个导出通过；完整秘密与固定安装验收仍开放。 [Evidence](docs/evidence/vectorcraft-permissions-parent-assets-candidate64-20261009.json).

任务9.21已在当前候选64／源46完成：实际当前会话查看128／64／32原生预览，执行一次显式授权绿色填充返工，验证控制对象保全、共享预算／停滞及9类陈旧／schema／重启守卫。畸形回执现保留脱敏拒绝证据。小尺寸文字仍不可读，创作验收保持待定；不声明独立评审、自动循环或固定分发。121/127任务完成、6项开放。 [Evidence](docs/evidence/vectorcraft-single-round64-20261009.json).

评审读取边界继续修复：技术清单在解析前授权，捕获文件读取根取请求与评审存储的交集；目录替换后描述符读取拒绝外部字节。评审摘要流式读取，检查器身份同时绑定固定读取器及宿主适配代码，旧回执不能沿用变化后的依赖。该候选增量不关闭7.4–7.6；完整父进程读写、宿主秘密引用及固定发行继续开放。 [Evidence](docs/evidence/vectorcraft-permissions-review-read-candidate64-20261009.json).

Controller读取边界继续实现：计划与源清单先经冻结根授权读取；源工程、依赖与额外输入的摘要使用安全流式读取，运行期指纹采用批量核验。3类目录替换失败用例修复，65MiB稀疏文件摘要与超过4096项输入的分批行为通过。源快照复制、交付检查、写入根完整审计、宿主秘密引用和固定发行继续开放，7.4–7.6不勾选。 [Evidence](docs/evidence/vectorcraft-permissions-controller-read-candidate64-20261009.json).

交付读取边界增量：交付清单、文件摘要与几何JSON在冻结根内安全读取；几何验收重新核对实际JSON摘要。账本只接收实际验过的清单字节摘要，并在接收前检查清单未被改写。交付根／嵌套目录替换及未绑定几何JSON三个失败用例已修复。源快照复制、写入边界、宿主秘密引用和固定发行仍开放，7.4–7.6不勾选。 [Evidence](docs/evidence/vectorcraft-permissions-delivery-read-candidate64-20261009.json).


源快照复制增量：固定读取器在冻结源根内持有文件描述符，流式复制并核验预绑定摘要；目标父目录逐层O_NOFOLLOW，排他创建、失败移除本次文件、成功只读及fsync。保留大于64MiB工程语义。目录替换、摘要漂移、目标链接／越界／已存在守卫已验证。此增量不关闭父进程其余写入审计、宿主秘密引用和固定发行；7.4–7.6仍开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-permissions-source-copy-candidate64-20261009.json).


Controller内容写入增量：状态／计划／事件／控制文件通过冻结目录描述符持久化，逐层O_NOFOLLOW、排他创建和fsync；状态更新采用随机临时文件及相对同一目录描述符的原子替换，旧.next链接不被跟随。事件身份及控制摘要绑定持有的文件／输入字节，避免写后路径重读。2类旧实现失败、5项新增边界测试、16项目标回归、158项Node及实际原生受限返工通过。目录创建、技能树复制、其他父进程写入、宿主秘密引用及固定发行继续开放；7.4–7.6不勾选，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-permissions-state-write-candidate64-20261009.json).


Controller目录／整树增量：快照目录创建、固定技能树复制和源快照摘要改为持有目录描述符，逐层O_NOFOLLOW；只在冻结根内创建，排他目标不覆盖。整树摘要取实际复制字节并保持UTF-16路径排序、二进制、执行位及空目录；源变化、链接、类型和摘要漂移拒绝，失败保留根内部分产物供排查。2类原实现根外副作用失败已修复；19项目标、163项Node及实际原生返工／4次共享额度停止通过。旧竞态测试在相同阶段改为描述符入口注入，原字节已归档。其他父进程写入／数据库路径、宿主秘密引用及固定发行继续开放；7.4–7.6不勾选，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-permissions-tree-write-candidate64-20261009.json).


技术评审写入增量：请求数据及写入根在解码前冻结；输出／交付／检查器目录和文件通过描述符入口创建与排他只读持久化，报告回执取已核对写入摘要。检查器快照摘要使用安全批量读取；身份由6文件扩展为10文件，新增四个写入／目录适配器依赖，旧检查回执因漂移失效。3类根外写入及异步请求修改的4个旧实现失败已修复；21项目标、171项Node及实际原生受限返工／4次共享额度停止通过。数据库／备份、启动边界、宿主秘密引用和固定发行继续开放；7.4–7.6不勾选，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-permissions-technical-write-candidate64-20261009.json).


账本备份／读取增量：旧schema的VACUUM INTO先写宿主随机私有暂存，校验schema及摘要后，以安全描述符复制发布400只读、fsync的备份；最终再核对冻结备份根内摘要。暂存创建成功后才登记清理所有权，清理失败关闭连接并阻止迁移。账本verified摘要只读取任务冻结输出根。1类根外备份写入及2类越界验收读取失败已修复；11项目标、176项Node通过，真实SQLite v1/v2、未checkpoint的已提交WAL、预算及运行时选择保全。当前原生受限返工／4次额度停止通过，此运行使用新schema3，不冒充原生旧状态迁移。主数据库及SQLite暂存路径、启动边界、宿主秘密引用、固定发行继续开放；7.4–7.6不勾选，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-permissions-backup-write-candidate64-20261009.json).


公开提交固定副本验收：从远端main的完整不可变提交`11a49e9d1d5f471d1c4cbf93551bdb1c87abe3d1`安装dev.64/source46到独立、含空格的Codex0.153.4配置；13技能发现与身份匹配，13次独立HTTPS空缓存启动、12组原生创建／返工通过，setup-only单独标记，不计作跳过。实际安装Harness完成原生返工、三格式重新解码、4次共享额度停止及源／文本保全；回执评分为显式QA夹具。5项引用守卫及161项Python回归通过。新脚本默认仍要求公开版本标签；显式候选只允许与远端main相同的完整SHA，并记录publicTagVerified=false。旧脚本原字节已归档，旧报告不重签。此证据推进9.9／9.18的安装与冷启动部分，不关闭模型默认路由、公开标签复验、六层发行门禁、全命令GUI或秘密边界；121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-public-commit64-install-20261009.json).


当前固定副本四场景复验：dev.64/source46公开提交安装上，6次原生修订、15项守卫及拥有签名桌面的源工程修改／保存／重开后陈旧建议拒绝通过；最佳候选、轮数、停滞、额度与文本保全按VC-QA-002核验。桌面初次夹具越界被正确拒绝，调整为测试拥有的GUI根内工程后通过，产品权限未放宽。证据v2解析已绑定checker_bundle.ts的完整10文件身份；发布门禁核验所选当前报告，旧v1三文件证据与原脚本归档保留。当前六层开发发行门禁通过，市场资格仍为false；公开标签后的安装复验、模型路由、权限／秘密完整边界及逐命令GUI仍开放，121/127完成、6项开放。回执评分为QA夹具，不代表真实创意评审。 [Evidence](docs/evidence/vectorcraft-revision-commit64-20261009.json).


公开标签发布后复验：插件v0.1.0-dev.64已发布，标签指向6763caa1f0e6596fc01d298304794d0e9c139dc3，固定独立技能源v0.1.0-dev.46。从公开标签安装到全新Codex0.153.4隔离配置，13技能身份一致；13次独立HTTPS空缓存启动、12组原生创建／返工通过，setup-only单列，零跳过。安装产品源码与发行前四场景副本逐文件一致，main／tag共4个CI运行通过。已完成且无句柄的13个测试运行时缓存被清理，原生工程和执行记录保留。此结果补齐9.18的公开发行及实际安装／冷启动部分；其9.9真实模型默认路由等前置仍未完成，不关闭9.18。权限／秘密完整边界、全命令GUI、其他平台与完整V1不提升；121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-public-tag64-install-20261009.json).


逐命令固定安装增量：公开插件dev.64／源46的实际安装副本在拥有的签名桌面会话中完成22条paint命令、44轮原生保存／重开和88项SVG／PNG解码。逐条检查实时enabled、原始参数、目标颜色／渐变／自由渐变、控制文字、源工程和前次交付保全；自由渐变分线按固定上游Catmull-Rom曲线核验。初次QA的注册表数量、RGB读回形式、选择状态及线性位置假设错误已保留并修正，不属于产品修复。外置全目录矩阵明确22/585已验、563项NOT_RUN；固定技能快照不改写。画布图像来自原生工具，不是操作系统窗口截图或创意评审。任务8.3仍开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-matrix-fixed64-20261009.json).


色板逐命令固定验收：公开插件dev.64／源46实际安装副本在拥有的签名桌面中完成全部22条swatch命令、44轮原生保存／重开和88项SVG／PNG解码。全局色更新、删除保色解绑、合并重联、组编辑／排序／移动、Lab专色选项及色库保存／加载均有逐条语义断言，控制文字、源工程、前次交付保全；13个实际安装技能前后摘要一致。首次色库加载触发QA字段访问错误，原失败记录保留，修复验收器后全族复验通过，产品和固定技能源未修改。复用原paint22条证据，汇总44/585已验、541项NOT_RUN、88轮保存重开及176项导出解码；25项命令目标回归通过。原生画布图像不提升为系统窗口截图或创意评审。任务8.3仍开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families-fixed64-20261009.json).


描边逐命令固定验收：公开插件dev.64／源46实际安装副本完成全部10条stroke命令、20轮原生保存／重开及40项SVG／PNG解码；13个安装技能摘要一致。箭头、高级轮廓及宽度点使用开放路径，内外对齐使用封闭路径；按半宽系数核对pt宽度点、箭头缩放交换、沿线／跨线轮廓翻转以及自定义轮廓增删重置。填充、控制文字、几何、源文件和前次交付保全。5类样式修改的10组原生画布／PNG比较均有142–1189个像素变化，43项命令目标回归通过。空列表reset与重复轮廓add被原生禁用的QA失败保留，夹具修正后复验通过；产品及固定技能不修改。自定义轮廓名称仅验拥有的私有桌面会话内行为，跨应用重启的偏好持久化NOT_RUN，不提升为系统窗口截图或创意评审。保留原44条汇总及校验器原字节，当前汇总54/585已验、531项NOT_RUN、108轮保存重开与216项导出解码。任务8.3仍开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families54-fixed64-20261009.json).


逐命令透明度固定安装增量：公开dev.64/source46实际安装副本在拥有的签名桌面中完成全部17条transparency命令、34轮原生保存重开及68份解码SVG/PNG导出。逐命令核验对象百分比与混合／挖空选项、顶层蒙版移动与释放后重新编号、启停／链接选项、页面标志、默认值对新建蒙版的实际影响，以及编辑层进入／退出和查看开关的原生返回状态。临时编辑层不进入保存工程，蒙版艺术与控制文本保全；13技能身份不变。三种修订的6次实际画布／PNG比较有1208–2160像素变化。初次夹具错误（无效描边颜色、默认false省略字段、新探针文档未保存）已保留并修正，全族从新拥有会话复验通过，产品及锁定技能未改动。默认值只覆盖私有会话，应用重启后的偏好持久化仍NOT_RUN；普通screenshot是艺术板渲染，不能证明蒙版灰度查看或完整窗口GUI。原54命令矩阵与校验器原字节保留；当前71/585通过、514 NOT_RUN，142次保存重开、284份解码导出。任务8.3保持开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families71-fixed64-20261009.json).


单独窗口验收补充：viewOpacityMask开启／关闭各捕获一张真实1440×900应用窗口，三个内部像素样本分别为灰度／彩色，原生状态确认关闭查看后仍编辑蒙版。仅此命令的窗口行为通过，全585命令GUI仍开放。 [Evidence](docs/evidence/vectorcraft-mask-window-fixed64-20261009.json).


逐命令形状固定安装增量：公开dev.64/source46实际安装副本在拥有的签名桌面中完成全部10条shape命令、20次原生保存重开、40份解码SVG/PNG及20张真实应用窗口。独立公式核验矩形圆角、椭圆／弧线曲线手柄、多边形／星形旋转及顶点、螺旋反向和衰减、网格线序与分隔数、确定性光晕子树和径向渐变；第二轮仅调整前轮真实返回对象的透明度，再创建参数不同的同类对象，原艺术／控制文本、未授权字段、源工程及前轮交付文件保全。30组画布／PNG／窗口像素比较均有变化（244–165235像素），13安装技能身份不变。窗口原始物理像素比例1×／2×均保留，窗口差异分析显式归一至1440×900；首次只读窗口捕获错误保留，最多三次纯读取尝试，编辑请求不重放。初次QA字段假设和白底光晕不可见夹具已修正，加入自有深色背板后全族新会话复验。旧71命令矩阵及校验器原字节保留；当前81/585通过、504 NOT_RUN，162次保存重开、324份解码导出。此窗口证据只覆盖形状10命令，不推广为全命令／创意／模型／V1通过。8.3仍开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families81-fixed64-20261009.json).


逐命令图层固定安装增量：公开dev.64/source46实际安装副本完成全部11条layer命令、22轮原生保存重开、44份解码SVG/PNG及22张真实拥有应用窗口。独立完整树断言核验当前层上方插入、嵌套子层、删除及当前层回退、复制子树全新前序ID、隐藏／锁定选择清理、绘制顺序收集、仅直接可选子节点、剪切路径移底并去除画笔及释放后保留无画笔路径、文档粘贴选项持久化。当前层／选择／目标用原生会话读回，不虚称随工程持久化。第二轮先修改自有图层名称，完整保全控制对象、其他字段、源文件及前轮交付。33组实际画布／PNG／窗口比较完成：可见性与剪切的4组画布／PNG比较分别变化964和419像素，其余按显式保全或只记录契约核对；窗口变化不单独作为命令语义证明。13安装技能身份不变，22项新增断言／证据回归通过。旧81命令矩阵及校验器原字节保留，当前92/585通过、493 NOT_RUN、184轮保存重开及368份解码导出。任务8.3仍开放；121/127完成、6项开放，不提升全命令GUI、创意／模型、权限秘密边界、市场资格或完整V1。 [Evidence](docs/evidence/vectorcraft-command-families92-fixed64-20261009.json).


逐命令图形样式固定安装增量：公开dev.64/source46实际安装副本完成全部18条graphicStyle命令、36轮原生保存重开、72份解码SVG/PNG及36张真实拥有应用窗口。独立完整树断言核验不同尺寸矩形的单位框渐变映射、替换与追加外观／透明度保全、唯一名称与稳定ID、删除保色解绑、仍同步对象重定义跟随与已改外观对象保全解绑、合并堆栈顺序、排序／移动、未使用及绑定读回、内置目录和自有样式库保存／加载／名称冲突编号／再次导入复用。第二轮先修改自有源对象名称，原控制文字及其他字段、源工程与前轮交付保全。54组实际画布／PNG／窗口比较按显式变化／保全／测量契约核验；两轮删除预置不同外观，跨轮像素仅测量，每轮删除保色由执行前后完整树证明，不能把窗口差异独立当作语义验收。13安装技能身份不变；23项新增断言／证据回归通过。Override Character Color仅验证私有会话偏好及列表读回，跨应用重启持久化NOT_RUN。旧92命令矩阵及校验器原字节保留，当前110/585通过、475 NOT_RUN、220轮保存重开及440份解码导出。任务8.3仍开放，121/127完成、6项开放，不提升全命令GUI、创意／模型、权限秘密边界、市场资格或完整V1。 [Evidence](docs/evidence/vectorcraft-command-families110-fixed64-20261009.json).


外观验收诊断检查点：新增16条appearance命令的候选驱动、图像检查器和独立堆栈断言；尚未形成通过证据。a2在setActiveItem探针的内存undo恢复后，保存／重开缺少目标对象2；a3在effect.apply调用处结果未知并停止，所有自有进程停止，未自动重放。原因仍待隔离，不归因为产品缺陷。候选改为从原生保存快照恢复探针，但该修改尚未验收。缺少固定通过报告的18项正向证据测试保留在scripts/qa/pending/，不冒充已通过回归；CI执行堆栈单元测试及真实失败记录的断言。通过覆盖仍为110/585，475 NOT_RUN，任务121/127完成、6项开放，8.3不勾选。产品标签dev.64与技能源46保持不变。 [诊断](docs/VectorCraft-Appearance-Diagnostic.zh-CN.md)。


逐命令外观固定安装增量：公开dev.64/source46实际安装副本完成全部16条appearance命令、32轮原生保存重开、64份解码SVG/PNG及32张真实拥有应用窗口（实际1440×900，1x）。独立完整树断言核验仅复制画笔的新填充／描边、清空／基本化、逐行属性与效果、去重删除、完整复制及Contents槽移动、不同边界渐变拾取与反向追加、隐藏恢复、锁定过滤的内容选择，以及带蒙版源对象的复制／移动转移及清源保全。活动外观行与新艺术偏好由实际编辑／创建探针证明，再从自有原生保存快照重开恢复，不提升undo链或应用重启偏好验收。第二轮先修改自有控制对象名称；原文字、其他字段、源文件及前轮交付保全，13安装技能身份不变。48组实际画布／PNG／窗口比较按显式变化／保全／测量契约核验；4类变化命令的8组画布／PNG比较变化722–2062像素，窗口差异不单独作为语义证明。此前undo／重开、未知回复与跨层蒙版顺序夹具失败保留；源层和显式ID准备已修正，全族新会话通过，产品／技能未修改。18项原待执行证据测试已纳入常规回归，另补2项证据篡改和2项夹具失败测试。原110命令矩阵、原校验器及诊断候选字节保留；当前126/585通过、459 NOT_RUN，252轮保存重开、504份解码导出。8.3仍开放，121/127完成、6项开放，不提升全命令GUI、undo、创意／模型、秘密边界、市场或完整V1。 [Evidence](docs/evidence/vectorcraft-command-families126-fixed64-20261009.json)。


逐命令效果固定安装增量：公开dev.64/source46实际安装副本完成全部7条effect命令、14轮原生保存重开、28份解码SVG/PNG和14张真实拥有窗口。独立核验45项完整效果目录、参数合并、活动行与显式目标、堆栈复制／移动，以及几何、描边轮廓、阴影／模糊栅格、文字轮廓、裁切标记、变换副本和容器展开。两项嵌入PNG按源边界与72ppi公式核验区域、摘要、透明度和像素；21组画布／PNG／窗口比较完成。13安装技能身份、控制文字、源工程及前轮交付保全。汇总133/585通过、452 NOT_RUN、266轮保存重开、532份解码导出；42项新增回归通过。未覆盖全部效果／画笔／符号变体，不提升undo、模型、秘密边界、全GUI或完整V1；8.3仍开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families133-fixed64-20261009.json).


逐命令辅助线固定安装增量：公开dev.64/source46实际安装副本完成3条guide命令、6轮原生保存重开、12份解码SVG/PNG和6张真实拥有窗口。独立列表断言核验追加索引、删除后的索引收缩与移动时方向保全，第二轮仅先修改自有控制对象名称。6组真实锁定／解锁注册表探针证明新增始终可用、锁定禁用删除／移动，完整工程保全并恢复解锁；未提交禁用编辑请求。9组图像比较确认辅助线不进入艺术导出；28项按文档坐标与缩放计算的窗口检查确认现存线及删除／移动旧线的消失。新驱动最多20次纯读取等待画板适配，截图前后视图一致；首次null返回／画布宽高假设和未适配视图失败记录保留。13安装技能身份、原控制文字、源工程及前轮交付保全。31项新增回归通过；汇总136/585通过、449 NOT_RUN、272轮保存重开、544份解码导出。8.3保持开放，121/127完成、6项开放；不提升undo、模型、秘密边界、全GUI、市场或完整V1。 [Evidence](docs/evidence/vectorcraft-command-families136-fixed64-20261009.json).


逐命令属性固定安装增量：公开dev.64/source46实际安装副本完成2条attributes命令、4轮原生保存重开、8份解码SVG/PNG及4张真实Attributes面板窗口。独立完整树核验组内绘制叶、文字字符与外观行的叠印目标差异、唯一对象变更计数、混合属性／填充规则／直线矩形方向读回、默认中心点与空属性清理、字符串去空白，以及会话内去重10条URL历史。第二轮先修改自有控制对象名称；控制文字、源工程、前轮交付及13安装技能身份保全。6组画布／PNG／窗口比较通过，普通模式艺术像素保全；4份额外SVG按完整树独立解码核验链接，8项固定布局复选框像素检查区分混合横线／勾选／未勾选。38项新增回归通过；旧136命令矩阵及校验器保留，当前138/585通过、447 NOT_RUN、276轮保存重开、552份解码导出。此证据不提升印刷叠印模拟、曲线方向、重启后URL历史、undo、模型、全GUI或完整V1；8.3保持开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families138-fixed64-20261009.json).


逐命令魔棒设置固定安装增量：公开dev.64/source46实际安装副本完成2条magicWand命令、4轮原生保存重开、8份解码SVG/PNG及4张真实Magic Wand面板窗口。独立设置契约核验默认值、部分字段合并、重置后覆盖、未知字段忽略、颜色／描边粗细／不透明度的四种范围限制及小数保留；切换钢笔／选择工具和同会话原生重开后设置不变。第二轮先修改自有控制对象名称；完整树、色板、原控制文字、源工程、前轮交付及13安装技能身份保全。6组画布／PNG／窗口比较通过，艺术像素保全；20项独立设置导出的复选框像素断言核验五项开关。22项新增回归通过；旧138命令矩阵及校验器原字节保留，当前140/585通过、445 NOT_RUN、280轮保存重开、560份解码导出。应用重启后的偏好持久性和select.magicWand匹配仍未验收；不提升undo、模型、全GUI、创意、市场或完整V1；8.3保持开放，121/127完成、6项开放。 [Evidence](docs/evidence/vectorcraft-command-families140-fixed64-20261009.json).

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

插件展示使用上游官方图标；名称为 **VectorCraft Use**。图标来源与许可证保存在 `assets/official-icon-source.json` 和相邻 LICENSE 文件中。

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## 矢量场景操作手册 / Vector scene playbooks

当前11条带具体方法和参数的矢量工作流（8条基础与3条0.12新增），见 [vectorcraft-scenario-playbooks](skills/vectorcraft-scenario-playbooks/SKILL.md)。包含独立对象选择、文字母版和轮廓交付；本地候选不代表宿主同步显示已验收。

Eight workflows include explicit commands, parameters, object selection and editable/outlined delivery. This candidate does not establish host UI synchronization.

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

## 矢量制作场景开发候选

新增vectorcraft-clipped-illustration、vectorcraft-sticker-grid、vectorcraft-sticker-offset-border三个独立技能，包含原生方法、参数、实际ID绑定与保存后的编辑检查。当前新增内容未发布；完整真实设计质量及宿主同步仍待验收。
