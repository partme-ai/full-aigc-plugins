# EffectCraft Agent Plugin

开发版技能源 dev.52／插件 dev.54：取消恢复与父子终态屏障；27 项取消测试及 macOS 真实原生父子取消／控制器中断／只读恢复通过。父任务等待后代停止，未知编辑保留 reconciling。完整跨平台、宿主及 V1 验收仍开放。 [证据](docs/evidence/cancel-family-candidate-20261009.json)。

历史发布前取消恢复检查点（基于source51／plugin53）：启动租约仍占用时保留cancel_requested；重启后核对原停止回执，保留未知编辑。版本化退出记录区分强制组停止与已核对业务退出。12项目标、536项回归（498通过／38条件跳过）及当前只读独立技能真实原生取消／监督器中断／重启核对通过。已发布快照不变；完整父子取消终态、其他平台、宿主及V1仍开放。 [证据](docs/evidence/cancel-restart-candidate-20261009.json)。

开发版技能源 dev.51／插件 dev.53：POSIX 私有进程组归属及 nonce 绑定业务结果覆盖守护器丢失、孤儿后代和强制取消。当前回归及离线安装副本证据见 [发布验证](docs/evidence/group-ownership-release51-20261009.json)。下方历史检查点保留原摘要；跨平台原生、固定宿主、创作验收及完整 V1 仍开放。

历史单技能离线检查点已完成9.5.1：macOS arm64实际15/15只读、空格路径、无系统Python及禁止联网的公开run/review通过，工程重开与每例12帧解码通过，15份安装与该检查点技能源一致。首例冷缓存、14例共享用户缓存复用；需要预备官方归档及ffmpeg/ffprobe，不是15次冷安装或领域代表验收。其他平台9.1.2、领域与透明交接9.5.2、宿主及完整V1仍开放。 [Evidence](docs/evidence/independent-offline15-candidate-20261009.json).

历史进程组核对检查点：10项目标与516项回归通过（478通过／38条件跳过），真实macOS沙箱空组退出及后代清理通过；历史unknown保留且不重放。该检查点的source50／plugin52快照不变，跨平台与完整V1仍开放。 [Evidence](docs/evidence/process-group-probe-candidate-20261009.json).

开发版技能源 dev.50／插件 dev.52：旧 v2 任务在准备当前 Python 前校验并派发原解释器；受管理入口支持 CRAFT_RUNTIME_ARCHIVE 离线原生制品。macOS 原生重开与完整解码通过，真实 Windows、固定宿主及完整 V1 待验收。 [Evidence](docs/evidence/release-readiness-source50-20261009.json).

文字、图形与镜头需求进入，交付可编辑 `.ecproj`、依赖素材和渲染结果。

当前插件：`0.1.0-dev.54`；技能源：`0.1.0-dev.52`；15 个独立技能。

已验证首次使用平台：macOS arm64、Python 3.11+。固定运行时安装在用户数据目录，技能文件保留在宿主加载目录。当前为开发版本；完整首版验收及通用 Skills CLI 实际安装仍未完成。

维护者来源校验拒绝符号链接、不完整锁及版本同名分支，并在替换任一管理技能前检查全部声明来源；已发布技能／运行时身份保持。[快照预检架构](docs/Skill-Snapshot-Self-Contained.zh_CN.md)。

## 首次使用

在宿主中调用 **`effectcraft-use`**。直接使用 CLI 时，将 `SKILL_DIR` 设为宿主实际加载的 `SKILL.md` 所在绝对目录；可能位于用户／项目 `.agents/skills`、插件内部或宿主缓存，以实际路径为准。以下入口在调用前安装并核验固定运行时。

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
sh "$SKILL_DIR/scripts/launch.sh" doctor
sh "$SKILL_DIR/scripts/launch.sh" run --plan "$SKILL_DIR/examples/brand-intro.json" --output "$PWD/effectcraft-result"
```
<!-- CRAFT_FIRST_USE_END -->

实际制作、所需输入、原生工程和局部修改参见[可编辑工作流](skills/effectcraft-use/references/workflow.md)。[安装与技能入口](skills/effectcraft-use/SKILL.md) · [版本绑定历史](RELEASE-HISTORY.zh-CN.md)。版本与命令查询验证安装和发现，不代表创作完成。

[首次使用入口证据](docs/evidence/craft-readme-first-use-navigation-20261007.json)。

固定安装路径验收：独立技能及 Art 混合工作流在含中文和空格的路径下，通过原生创建与重开、定点返工及导出；Art 另验证移动交付包。技能与运行时身份保持不变。该结果仅覆盖 macOS arm64 的本次首次使用场景。 [路径验收证据](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

固定发行前的历史源码候选：结构损坏的 runtime／Node 锁在写运行时目录或下载前返回本地恢复诊断。五项候选原生首次使用通过；发布插件快照保持不变，新不可变发行安装需另行验收。 [锁诊断候选](docs/EffectCraft-Lock-Shape-Architecture.zh_CN.md).

---

固定原生首次安装与完整命令恢复验收通过：新版五插件58技能逐项独立冷安装，十个Art技能分别安装四领域；四个原生下载半包SSL EOF恢复、72个原生保存后故障、四个健康命令返工及混合HD返工／恢复／移动包通过，全部安装摘要保全。仅关闭领域2.10／8.11与Art4.10；2639条命令逐项、GUI、模型、通用Skills CLI及完整V1仍开放。 [版本及证据](docs/evidence/codex-native-download-first-use-20261007.json).

历史发行记录：当前插件：`0.1.0-dev.21`；技能源：`0.1.0-dev.19`；包含父级／表达式计划，十三项固定安装父级／表达式冷启动通过；Art领域包待更新，完整V1仍开放。

固定发布前的候选记录：原生下载恢复候选：最多三次只读重试并丢弃半包；此前固定版本冷安装遇到SSL EOF失败，修复后的固定安装验收仍开放。

历史插件版本记录 `0.1.0-dev.18`／技能源 `0.1.0-dev.16` 固定完整命令内层JSON修复；实际安装首用复验进行中。

当前固定失败暂存验收：插件 dev.17、独立技能源 dev.15。全部58项独立CLI冷启动、24个原暂存原生故障案例及37原生场景＋6合同检查通过；Art77领域包升级仍开放。[证据](docs/evidence/codex-failed-stage-first-use-20261007.json)。

固定领域客户端首用复验：Film 插件 dev.16／技能源 dev.15，Effect／Photo／Vector 插件 dev.15／技能源 dev.14。隔离 Codex 发现58项零错误；实际安装副本24类保存后故障、四个健康公开工作流和已发布 Art 引擎＋安装后 Vector 客户端六类故障通过，全部58项安装摘要保全。Art dev.75 内置旧领域分发包尚需升级，全量命令／GUI／模型验收仍开放。[版本绑定证据](docs/evidence/codex-public-workflow-session-first-use-20261007.json)。
先前固定版本协议故障首用复验通过：48个独立技能源共288例，实际安装副本24例及四领域健康返工通过；58项安装摘要保持一致。验收范围与固定标签见 [协议故障验收记录](docs/evidence/codex-protocol-fault-first-use-20261007.json)。全量逐命令／GUI验收以及Art领域包升级仍开放。

协议故障修复候选：本领域13项技能逐个单独复制、空运行时公开安装后，原生保存成功再注入六种坏回复全部通过（78例，零跳过）。不重放、未知回执、工程重开与交付／技能保全均已检查。[证据](docs/evidence/protocol-fault-first-use-20261007.json)。固定安装副本与Art领域包升级仍为独立门禁。

固定插件 0.1.0-dev.13／技能源 0.1.0-dev.12 已通过安装后的返工门禁：隔离 Codex 发现全部58项技能零加载错误，本领域安装技能从空运行时直接执行文档创建／返工计划、保存重开与非目标保全。全部58项安装摘要不变，当前固定发行CI通过。[固定返工证据](docs/evidence/codex-complete-command-revision-first-use-20261007.json)。全量命令／GUI／模型验收保持开放。

本领域 13 个技能逐个单独复制、从各自空运行时公开安装后，配套返工计划全部通过（145.856 秒，零跳过）。[返工证据](docs/evidence/complete-command-revision-first-use-20261007.json)。更新快照的真实固定宿主安装另设门禁。

完整命令入口补充了配套的创建／返工 JSON 示例、重新打开后的显式选择前置条件，以及原生保存重开、非目标对象与像素检查。每个独立技能均包含两个可执行计划。[调用指南](skills/effectcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision)。全量逐命令及 GUI 验收保持开放。

先前固定发行首用通过：隔离 Codex 0.153.4 发现全部 58 项技能零加载错误；每项安装技能独立空运行时公开安装（385.234 秒）；安装后的领域新命令入口及 Art 1080p 混合返工／恢复／移动包检查通过。全部安装摘要保全，固定 CI 与五包重建通过。[版本绑定证据](docs/evidence/codex-complete-command-first-use-20261007.json)。通用 Skills CLI、全命令／GUI 与完整创作验收仍开放。

## 完整原生命令入口

全部 13 项独立技能分别从空运行时使用公开锁定 CLI 附件安装，随后完成创建、保存重开、领域参数及渲染检查（152.42 秒，零跳过）。[逐技能冷首用证据](docs/evidence/complete-commands-cold-first-use-20261007.json)。本轮覆盖每项技能的完整命令代表样例；全命令／GUI 和实际宿主安装另行验收。

已发布开发快照：skills dev.11 / plugin dev.12；固定宿主首用代表门禁通过。

640 条命令现在均有逐项参数说明、技能归属与同会话调用入口。运行 `commands.py list / describe / check / run`；原生状态按实时 enabled 校验。旧工作流的 21 项交付合同保留。GUI 命令需显式 bridge，命令目录覆盖不代表全量验收。

[架构与操作指南](docs/EffectCraft-Complete-Commands-Architecture.zh_CN.md) · [逐项参考](skills/effectcraft-use/references/command-reference.md) · [可运行示例](skills/effectcraft-use/examples/commands-advanced.json)

独立技能驱动的图层合成、动态图形与镜头效果.

[English](README.md) | [简体中文](README.zh-CN.md)

## 当前版本与可复现宿主验证

此前完成宿主验证的插件/技能源版本：`0.1.0-dev.3`。Codex 0.147.0 与 0.153.4 均安装五个固定公开发布，发现全部 58 项启用的命名空间技能，加载错误为零，来源摘要一致。五项代表流程已通过 0.147.0 安装后的场景技能入口验证，包括原生工程、局部修订和 ArtCraft 在线混合流程。模型自动派发、桌面 GUI、创作最终评审和完整交换保真尚未验证。

[宿主验证设计](docs/EffectCraft-Host-Verification-Architecture.zh_CN.md) · [绑定版本的证据](docs/evidence/codex-skill-suite.json)。历史里程碑保留原证据范围；当前版本身份以 manifest 和锁文件为准。

> 开发版已通过固定标签的 Codex 安装、技能发现和原生代表工作流；完整产品与创作验收仍未完成。

独立技能包已进入实施，单技能隔离安装已在 macOS arm64 实测；完整创作流程与插件宿主验收仍未完成。[证据](docs/evidence/bootstrap-tests.json)

## 定位

制作品牌片头，交付可重开的 .ecproj 与可导入剪辑工程的渲染结果；修改文字后保持其他图层和动画曲线不变。

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
| Plugin ID | effectcraft |
| Metadata version | 0.1.0-dev.54 |
| Stage | implementation-in-progress |
| Skills source | effectcraft-skills / v0.1.0-dev.52 |
| Execution | 上游 CLI；ArtCraft 使用子适配器 |
| Host compatibility | Codex development install/discovery pass; GUI and other hosts pending |
| License | Apache-2.0 (original repository content) |


## 能力与边界

| 能力 | 行为边界 | 状态 |
| :--- | :--- | :--- |
| 合成建立与范围 | 显式设置合成尺寸、帧率、时长与工作区；输入的时间单位必须转换为适配器确认的上游单位。 | 待完整验收 |
| 图层与素材依赖 | 维护图层 ID、顺序、父子关系、素材引用和可见性；检查循环父子关系与丢失素材。 | 待完整验收 |
| 文字图形与关键帧 | 以属性路径记录文字、变换与关键帧，保留插值方式；修改文字不得重建无关动画。 | 待完整验收 |
| 效果与蒙版能力匹配 | 在应用效果或蒙版前发现命令与参数 schema；不支持的参数在执行前返回明确错误，禁止静默跳过。 | 待完整验收 |
| 透明与色彩交接 | 交接时记录颜色空间、位深、alpha 类型与编码；透明背景必须通过实际像素或通道检查验证。 | 待完整验收 |
| 工程与渲染交付 | 重开 .ecproj 验证图层与关键帧；渲染结果与源合成版本绑定；向下游提供素材化损失说明。 | 待完整验收 |

不重写上游编辑引擎，不暗中改变原生交付格式，不宣称 GUI 或跨平台验收完成。

## 架构与文档

- [完整运行时架构](docs/EffectCraft-Runtime-Architecture.zh_CN.md)
- [技术方案与路线](product-docs/EffectCraft/5%E3%80%81EffectCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md)
- [V1 PRD 与需求映射](product-docs/EffectCraft/V1/5%E3%80%81EffectCraft-PRD%E6%96%87%E6%A1%A3-V1.md)
- [完整文档导航](docs/README.zh-CN.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [专业领域技术设计](docs/EffectCraft-Domain-Design.zh_CN.md)

## 当前可执行的快速开始

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
以上校验文档和规范，不运行产品工作流。OpenSpec 校验使用 1.13.1；本仓不自动安装工具。

已安装官方 CLI 后可执行基础检查：

```bash
effectcraft-cli --version
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

[Upstream EffectCraft](https://github.com/storytold/effectcraft) · [Issues](https://github.com/full-aigc-plugins/effectcraft-plugin/issues)

独立技能工作流已通过原生 `.ecproj` 往返、透明 PNG 预览、H.264 解码，以及保留无关图层和关键帧的文字修订验证（14 项测试）。参见[测试证据](docs/evidence/effect-workflow-tests.json)。完整 Harness、外部依赖打包和插件宿主验收仍未完成。

外部 PNG 素材收集与保留图层动画的替换已纳入 15 项测试，见[当前证据](docs/evidence/effect-assets-tests.json)。完整领域和宿主验收仍在进行。

独立技能现已绑定当前已发布开发标签 `v0.1.0-dev.5`，`skills.lock.json` 固定来源提交与整个技能摘要。使用 `python3 scripts/vendor/skill_vendor.py check` 核对。技能源快照发布不代表宿主验收或生产完成。

## 开发版独立技能安装与使用

安装独立技能：`npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-use`。安装技能后，从其真实目录运行公开入口；插件快照也包含相同技能。

```bash
python3 -I -B skills/effectcraft-use/scripts/bootstrap.py
python3 -I -B skills/effectcraft-use/scripts/workflow.py --help
```

首次入口会安装锁定官方 CLI 到用户数据目录；要求 macOS arm64 与 Python 3.11+。使用技能内示例计划并提供真实素材；交付与修订合同见技能的 SKILL.md。[来源与校验证据](docs/evidence/skill-publication.json)。

## Codex 开发版宿主验证

五个插件已在隔离 Codex 配置中从公开标签安装，app-server 发现带命名空间的技能且无加载错误；安装缓存中的 ArtCraft 入口已交付四种原生工程。[宿主证据](docs/evidence/codex-installation.json)。此为受控开发验收，不代表桌面 GUI、其他宿主、完整创作或正式市场发布通过。

开发版本 `0.1.0-dev.1` 同步独立技能的安装锁等待修复；并行安装和复用按有界互斥协调，原生任务不自动重放。

当前开发里程碑为原生交付增加摘要绑定的交换损失报告，区分 lost、observed、unknown；派生导出不替代原生工程。跨编辑器字体、效果和蒙版保真尚未验证，完整交换验收任务保持未完成。

## CLI 与场景技能体系

技能源包含 13 项可独立安装的技能，分为安装、CLI 公共操作与场景任务。[架构与清单](docs/EffectCraft-Skill-Suite-Architecture.zh_CN.md)。运行时与插件版本分别维护；旧宿主证据保持原版本范围。

历史插件版本记录版本：`0.1.0-dev.7`；技能源版本：`0.1.0-dev.6`。命令示例以宿主实际加载的 `SKILL.md` 所在目录调用脚本。全部技能在用户、项目与插件三种含空格布局中通过隔离入口检查。[路径证据](docs/evidence/installed-skill-paths.json)。此前宿主验证仍对应其记录版本，既有安装需更新。

插件 `0.1.0-dev.6` 从固定公开标签重新取快照并修正整个技能摘要，未带入本地 Python 缓存。插件标签 `v0.1.0-dev.5` 的摘要误包含被忽略的开发缓存，已被替代，不可安装该标签。

插件 dev.7 固定技能源 dev.6，增加自包含可编辑蒙版示例与顶点修改/移除工作流。默认公开下载原生回归 39 项全部通过、无跳过；独立场景技能从空运行时安装，保留旧工程和非目标图层，以 RGBA 像素核验真实蒙版边界。[证据](docs/evidence/task-skill-first-use.json)。运行时保持 0.2.0；模型/GUI 与完整创作验收仍未完成。

当前固定发布的宿主核验（2026-10-06）：Codex 0.153.4 安装五个当前固定插件，加载全部 58 技能并逐项核对内容身份。本插件代表性原生工作流从实际安装路径调用，在新的原生运行时中完成创建、重开和修订检查；五工作流调用后，全部 58 个技能摘要保持不变。[证据](docs/evidence/codex-current-release-20261006.json)。显式标签生成器由 ArtCraft 统一持有。模型派发等待授权，GUI、创作与完整宿主验收仍未完成；本次 QA 维护不改变已发布技能/运行时内容或标签。

当前固定发布矩阵（FilmCraft dev.6、EffectCraft dev.7、PhotoCraft dev.6、VectorCraft dev.6、ArtCraft dev.17）在隔离 Codex 安装后通过 58 技能发现及原生代表工作流；执行后所有技能摘要保持不变。[宿主安装内容的原生验证](docs/evidence/codex-release17-native-20261006.json)。此证据不代表模型调度、GUI 或完整创作验收。

[透明素材到 FilmCraft 的实际交接](docs/EffectCraft-FilmCraft-Alpha-Handoff-Acceptance.zh_CN.md)：安装后双领域空运行时 1 项通过；修改片头文字保留动画，原生 RGBA PNG 在 FilmCraft 中露出底层并保留不透明前景像素。完整色彩／动画透明视频验收仍开放。

安装后的动画技能时序首次使用通过：4 个原生 RGBA 时刻与 12 帧视频解码核对淡入；文字返工保留徽标、关键帧属性及原交付。[时序验收](docs/EffectCraft-Temporal-Animation-Acceptance.zh_CN.md)。完整创作及动画透明视频验收仍开放。

EffectCraft 独立技能源 dev.7 对效果／蒙版计划参数校验错误返回 unsupported_mapping；原生 CLI 仍为 0.2.0。真实新建／修订拒绝保留原交付，完整原生技能源回归 44 项通过、零跳过（182.083 秒）。固定新版插件安装后的限定范围复验见下文。[架构](docs/EffectCraft-Parameter-Errors-Architecture.zh_CN.md) · [证据](docs/evidence/parameter-mapping-repair-20261006.json)。

固定插件 dev.8／技能源 dev.7 的安装后验收通过：五插件 58 技能、零加载错误；独立效果／蒙版技能从空运行时核对有效创建及非法新建／修订 1 项通过（24.714 秒），13 技能分别公开冷启动全部通过，全部宿主安装摘要保留。[发行绑定证据](docs/evidence/codex-effectcraft8-parameter-first-use-20261006.json)。ArtCraft 的领域包升级及错误传播、完整首版等门禁仍开放。

动态 RGBA PNG 序列保留可编辑 ecproj，并通过 craft-image-sequence/v1 交付全部帧摘要、帧率和时长。源码冷安装及实际 Film 交接通过；新固定插件和 Art 验收仍待完成。[架构](docs/EffectCraft-Dynamic-Sequence-Architecture.zh_CN.md)。

固定 Effect dev.9 与 Film dev.10 安装后的动态交接已通过：三项真实原生测试、58 技能发现零错误、逐项执行后全部安装摘要保全。[证据](docs/evidence/codex-effectcraft9-filmcraft10-dynamic-first-use-20261006.json)。Art 动态集成仍待完成。

当前固定发行领域场景矩阵：FilmCraft dev.10、EffectCraft dev.9、PhotoCraft dev.10、VectorCraft dev.11 共 37 个原生场景及 6 项合同检查通过，零跳过。每个场景仅复制对应安装技能，从空运行时目录使用默认公开附件安装原生 CLI；核验原生工程、实际像素／音频及局部修改保持，全部 58 项安装身份保持一致。[版本绑定证据](docs/evidence/codex-current-domain-task-matrix-20261006.json)。完整首版、通用 Skills CLI 安装、模型派发、GUI 与创作验收仍开放。

历史插件版本记录 dev.10 锁定技能源 dev.9，包含整份效果／蒙版计划字段预检，以及工程打开／创建前的只读原生 schema 核对。[候选证据](docs/evidence/effect-preflight-source-candidate-20261006.json)仅记录源码检查，固定发行宿主验收另行记录。

固定插件 dev.10／技能源 dev.9 安装后验收通过：Codex 发现全部 58 技能且零加载错误；13 项 Effect 技能分别从空目录公开安装 CLI，非法计划在安装／编辑前拒绝；4 项动画／序列／Film 交接回归与 13 项领域矩阵通过，零跳过。全部安装技能摘要保持不变。[版本绑定证据](docs/evidence/codex-effectcraft10-preflight-first-use-20261006.json)。Art 领域包升级、真实 Skills CLI 安装及完整首版仍开放。

工作区分段生产器候选：有界原生帧范围、摘要绑定恢复及逐帧核验；固定插件与 Film／Art 消费仍待完成。[架构](docs/EffectCraft-Segmented-Render-Architecture.zh_CN.md)。

当前源码 HD 分段候选通过 1080p／24 fps／五秒及动态标题核验；固定安装版与 Art HD 仍待完成。[架构与证据](docs/EffectCraft-HD-Sequence-Architecture.zh_CN.md)。

固定插件发行候选 0.1.0-dev.11 锁定技能源 0.1.0-dev.10，包含 HD 分段工作流与像素校验优化。实际安装版首次使用验收待完成。

公开工作流回复检查已同步领域技能源候选，并通过有界原生／Art 协议验证。新的固定领域和 Art 分发包仍待发行与实际安装验收。[候选架构](docs/EffectCraft-Complete-Commands-Architecture.zh_CN.md) · [证据](docs/evidence/public-workflow-session-candidate-20261007.json)。

失败暂存候选：公开工作流保留原生暂存原路径、依赖摘要、最后提交请求与已完成回执，禁止重放；固定发行与安装副本验收仍开放。[架构](docs/EffectCraft-Failed-Stage-Architecture.zh_CN.md)。

固定领域失败暂存首用门禁已通过：Film插件18／源16，其他领域插件17／源15；五插件58技能发现零错误，全部58项独立空运行时CLI冷启动通过（417.646秒），实际安装副本24个真实保存后故障直接重开产品保留的原工程及依赖，四个健康创作／返工通过。全部安装摘要和16项固定插件CI保持通过；源仓未提供CI运行，仅有本地回归。只关闭领域OpenSpec3.12；Art77内置旧领域源，4.9升级和完整V1仍开放。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

固定安装场景矩阵通过37个原生场景及6个合同检查，零跳过。Photo测试已从安装后的技能锁读取维护版原生版本，CLI与安装技能未修改。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


完整命令内层JSON修复候选：非有限值、溢出和重复键在绑定返回值前记录unknown，真实保存后九类故障与原工程重开通过。这是候选技能源证据，固定发布与实际安装复验尚未完成；逐命令／GUI门禁仍开放。

父级与表达式：十三项独立技能源候选冷安装、原生保存重开、动态Alpha和源返工保全通过；固定安装及Art分发待验证。 [Architecture](docs/EffectCraft-Expression-Parent-Architecture.zh_CN.md).

固定父级／表达式首用：十三项实际安装技能通过动态Alpha与源返工，58安装身份保持不变；Art新分发仍待验收。 [Evidence](docs/evidence/codex-effectcraft-expression-first-use-20261007.json).

## 桌面安装组件（候选源码）

每个领域技能自带固定桌面安装、自动启动与完整命令工作流入口。使用当前技能实际目录运行 desktop.py run PLAN --output NEW_DIRECTORY；保留原生工程、命令与生命周期回执。源码48项冷启动已有证据，本次固定版本的实际安装复验仍待完成。见 [桌面使用架构](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

命令计划 JSON 源候选：重复键在安装和创建输出前被拒绝，全部 15 个领域技能的独立副本拒绝测试与有效计划校验通过，3 项专项测试通过。固定插件发布和安装后复验仍为 NOT_RUN。[证据](docs/evidence/command-plan-json-candidate-20261007.json)。

严格计划解析的固定安装复验通过：64 个 CLI 探测、54 个独立安装领域技能的 324 次重复键拒绝、54 次有效计划结构检查，以及四领域空缓存原生保存／重开／渲染实例通过；执行后全部 64 个安装技能摘要不变。仅关闭本次修复的发布门禁；通用 Skills CLI、Art 领域包升级、全部命令上下文和完整首版仍开放。[证据](docs/evidence/command-plan-json-fixed-first-use-20261007.json)。

场景安装示例已使用实际加载的技能自身目录。源路径／布局检查通过；固定安装运行时验收另行记录。 [Architecture / 架构](docs/Scenario-Own-Path-Architecture.zh_CN.md).

新场景自身目录已通过固定安装复验；64项宿主身份匹配。完整V1仍开放。 [Evidence / 证据](docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).

木偶录制／跟随源码候选通过：10 条代表命令、逐帧关键帧、原生重开、局部返工和三类错误路径。固定发行安装复验另行记录。[架构](docs/EffectCraft-Puppet-Record-Follow-Architecture.zh_CN.md)。

固定 EffectCraft 插件 dev.35／技能源 dev.33 验收通过：64 项安装身份与发现、15 项独立 Effect CLI 空缓存安装，以及原生木偶录制／跟随／重开／局部返工和三类失败路径。另 49 项冷安装记录复用摘要一致的历史证据。完整首版仍开放。[固定证据](docs/evidence/effectcraft-puppet-record-follow-fixed-first-use-20261008.json)。

摄像机场景源码候选通过 Advanced 3D 实际渲染、投影变化、重开一致、仅镜头返工与三类失败路径。[架构](docs/EffectCraft-Camera-Scene-Architecture.zh_CN.md)。固定发行安装复验另行记录，完整首版仍开放。

固定 EffectCraft 插件 dev.36／技能源 dev.34 通过 64 项安装身份与发现、15 项独立 Effect CLI 空缓存安装，以及原生摄像机渲染／重开／局部返工和三类失败路径。其余 49 项冷安装记录仅复用摘要一致的历史运行。完整首版仍开放。[固定摄像机证据](docs/evidence/effectcraft-camera-scene-fixed-first-use-20261008.json)。

固定独立安装边界验收：全部 64 个当前技能的自身安装器／CLI 共 128 个不可用归档失败案例通过；错误保留本技能 setup 路径，无重试／原生启动，源副本摘要不变。四领域 SK-002 按当前精确锁验收；Art SK-002 和通用 Skills CLI 实际安装仍开放。历史 CLI 红灯为本轮重建，不冒充旧运行。[证据](docs/evidence/craft-fixed-setup-boundary-20261008.json)。

公共协议来源已固定到 ArtCraft v0.1.0-dev.109：[引用与校验说明](docs/Craft-Protocol-Authority.zh_CN.md)。这项检查核对协议来源，完整运行时协议验收仍未完成。

此前已验证的固定协议引用发行矩阵（Film／Effect dev.37、Photo dev.36、Vector dev.34、Art dev.107）已通过隔离 Codex 安装／发现 64 项技能、16 项实际安装所有者文件摘要核对，以及五个全新领域缓存下的 64 项独立公开 CLI 探测。原生场景证据仅对字节一致的技能复用，完整首版仍开放。[固定发行证据](docs/evidence/craft-protocol-authority-fixed-first-use-20261008.json)。

本次插件固定协议引用升级至 ArtCraft dev.109；技能快照保持原固定来源，新的实际宿主安装矩阵正在验证。完整首版与运行时协议验收仍开放。

固定发行 Film38／Effect38／Photo37／Vector35／Art109 已通过实际隔离 Codex 安装和发现 64 项技能、16 项安装副本协议文件摘要核对、五个全新领域缓存下的 64 项 CLI 探测。十项 ArtCraft 技能分别从空缓存完成原生 Photo 蒙版调整、源工程返工与迁移打包；另外 54 项技能仅复用整个技能摘要一致的历史原生证据。默认维护验收矩阵已更新；通用 Skills CLI 安装、模型调度、GUI 和完整 V1／协议验收仍开放。[本次固定证据](docs/evidence/craft-archive-prefix-fixed-first-use-20261008.json)。
