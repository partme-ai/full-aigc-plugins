# EffectCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.6`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.6` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


从文字、图形和素材创建可编辑 `.ecproj` 工程、依赖和媒体。当前为开发版，完整 V1 未完成；已发布版本与本地文档候选分别记录。

当前插件：`0.1.0-dev.70`；技能源：`0.1.0-dev.68`；15 个独立技能。

| Field | Value |
| --- | --- |
| Metadata version | 0.1.0-dev.20261017.6 |
| Skills source | effectcraft-skills / v0.1.0-dev.69 |
| Acceptance | Development; full V1 OPEN |

## 插件边界

Agent Plugins 1.0.0 通过根 `plugin.json` 发现本包及其 15 个技能。命令和钩子如果提供，属于客户端扩展，不是可移植核心组件。官方 EffectCraft CLI 执行原生编辑；宿主智能体负责规划、观察实际媒体并决定创作修订。当前技能脚本承担固定首次安装和确定性的执行、恢复检查。本包没有根 `mcp.json`，因此尚未提供可移植 MCP 服务，尽管上游 CLI 自身支持 MCP。跨平台 MCP 启动及宿主验收仍开放；见[架构决策](openspec/changes/establish-v1-plugin/design.md#agent-plugin-边界2026-10-09)。


## 首次使用

在宿主中请求 **`effectcraft-use`**。直接调用时，将 `SKILL_DIR` 设为宿主实际加载的 `SKILL.md` 所在绝对目录。启动入口在用户数据目录准备并校验固定 Python 和 EffectCraft，不修改系统 Python、全局 PATH 或只读技能目录。离线运行须预备锁定官方制品或已有完整缓存。

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
sh "$SKILL_DIR/scripts/launch.sh" doctor
sh "$SKILL_DIR/scripts/launch.sh" run --plan "$SKILL_DIR/examples/brand-intro.json" --output "$PWD/effectcraft-result"
```
<!-- CRAFT_FIRST_USE_END -->

```powershell
$env:SKILL_DIR = "<actual loaded skill directory>"
& (Join-Path $env:SKILL_DIR "scripts/launch.ps1") doctor
```

[工作流和交付说明](skills/effectcraft-use/references/workflow.md) · [安装与环境诊断](skills/effectcraft-cli-setup/SKILL.md)。通用 Skills CLI 安装、固定宿主自然语言自动派发仍须独立验收。


## 当前能力与证据

维护者生成的[当前矩阵](docs/current-capabilities.json)绑定完整技能载荷、Python／原生制品和原始报告摘要。已发布source53的macOS arm64技术样例通过。source54／plugin56改变回执实现，旧报告不再证明新载荷，当前矩阵保持NOT_RUN；新的统一管理接口原生证据单独限范围记录。其他架构、Web浏览器、FreeBSD、创作评价和完整宿主验收未通过的格子保持NOT_RUN。CI 的平台合同测试不替代目标平台创作。

source53／plugin55 的[15 技能报告](docs/evidence/native-smoke-source53-20261009.json)通过工程重开和每例 12 帧完整解码，全部使用已验证缓存（0 次冷安装），不是 15 个领域场景或模型派发验收。[取消恢复与父子屏障](docs/evidence/cancel-family-candidate-20261009.json)保留未知编辑，完整崩溃／GUI矩阵仍开放。


## 技能入口

| Skill | 用途 |
| --- | --- |
| [effectcraft-use](skills/effectcraft-use/SKILL.md) | 完整任务路由 |
| [effectcraft-cli](skills/effectcraft-cli/SKILL.md) | CLI 公共操作 |
| [effectcraft-cli-setup](skills/effectcraft-cli-setup/SKILL.md) | CLI 安装诊断 |
| [effectcraft-cli-project](skills/effectcraft-cli-project/SKILL.md) | 工程与素材管理 |
| [effectcraft-cli-footage](skills/effectcraft-cli-footage/SKILL.md) | 素材与预合成输入 |
| [effectcraft-cli-composition](skills/effectcraft-cli-composition/SKILL.md) | 合成与时间范围 |
| [effectcraft-cli-layers](skills/effectcraft-cli-layers/SKILL.md) | 文字形状与图层 |
| [effectcraft-cli-animation](skills/effectcraft-cli-animation/SKILL.md) | 属性与关键帧动画 |
| [effectcraft-cli-effects](skills/effectcraft-cli-effects/SKILL.md) | 视觉效果 |
| [effectcraft-cli-masks](skills/effectcraft-cli-masks/SKILL.md) | 蒙版与路径动画 |
| [effectcraft-cli-expressions](skills/effectcraft-cli-expressions/SKILL.md) | 属性表达式 |
| [effectcraft-cli-camera](skills/effectcraft-cli-camera/SKILL.md) | 三维图层与摄像机 |
| [effectcraft-cli-export](skills/effectcraft-cli-export/SKILL.md) | 渲染与透明输出 |
| [effectcraft-cli-tracking](skills/effectcraft-cli-tracking/SKILL.md) | 镜头跟踪 |
| [effectcraft-cli-puppet](skills/effectcraft-cli-puppet/SKILL.md) | 木偶与局部变形动画 |

各技能包含自己的运行资源，可独立安装，不依赖兄弟目录。655 条命令的参数、归属和模式见技能自带命令说明；目录覆盖不等于每条命令已执行验收。


## 检查、恢复与取消

使用 `inspect` 查看原任务，`reconcile` 核对原回执，`resume` 仅继续已证明可恢复的工作。`cancel` 先持久化停止意图；父任务等待后代停止，未知编辑保持 reconciling。不得换任务 ID／输出目录重做未知编辑。任务继续使用绑定的原运行时，损坏或缺失证据保留现场并拒绝续写。

[Managed execution](skills/effectcraft-use/references/managed-execution.md)


## 维护与版本历史

技能源维护执行代码，插件消费固定标签、提交及完整技能摘要。唯一增量规格为插件的 `openspec/changes/establish-v1-plugin`；未完成门禁不归档。公共 `craft-task/v1` 和 `craft-artifact/v1` 的所有者保持 ArtCraft，本仓仅消费。

[版本记录及整理前 README](RELEASE-HISTORY.zh-CN.md) · [Plugin specifications](https://github.com/full-aigc-plugins/effectcraft-plugin/tree/main/openspec/changes/establish-v1-plugin)

dev.56 的[统一管理接口验收](docs/evidence/managed-public-interface-candidate-20261009.json)完成9.3.5：严格回执身份／孤立材料保护及九个管理角色，含真实原生恢复与Codex实际观察后的局部修订。source54／plugin56分发本增量，source53／plugin55保留为历史版本；其他原生平台和固定宿主派发继续开放；后续本机三模式组合验收见下。[source52报告](docs/evidence/native-smoke-source52-20261009.json)保留为历史证据。

本机[三模式公开组合验收](docs/evidence/managed-three-mode-composition-20261009.json)完成9.3.6，使用未改变的已发布source54／plugin56载荷：workflow、命令计划和真实自有桌面会话贯通安装器、真实适配器、账本、回执和恢复，原计划换ID／目录重做被拒绝，旧CLI兼容。默认586项回归545通过、41条件跳过，另行启用的3个原生条件案例全部通过。本次新增测试与证据尚未发布；完整崩溃／GUI矩阵、其他原生目标、固定宿主派发及完整V1仍开放。


dev.55 技能源／dev.57 插件分发 [默认受管理派发验收](docs/evidence/managed-default-routing-20261009.json)：15个技能明确 workflow／commands／desktop 写入入口，45组只读预检与18组历史状态操作通过。源码589项回归548通过／41条件跳过。9.3.1与9.3.6已完成，70项仍开放；原生证据仅复用105份未变执行资源，三份指引已更新，未声明新宿主模型派发或完整平台通过。原始候选报告保留验证时点，发行绑定另见版本记录。


source56／plugin58修正新增测试的Windows默认编码依赖，显式读取UTF-8；source55的Windows失败CI与原标签保留。技能执行载荷不变，此修正不新增原生或宿主验收。


未发布的[运行期源工程冲突保护](docs/evidence/source-revision-conflict-candidate-20261009.json)：逐操作登记前和最终交付前复核源工程版本，外部保存后拒绝下一编辑，保全用户新版本和既有回执。595项回归553通过／42条件跳过，另独立原生保存冲突案例通过；9.3.2完整GUI／会话／跨状态根范围仍开放，插件固定source56／plugin58不变。


未发布的[跨账本工程认领](docs/evidence/shared-project-claims-candidate-20261009.json)为新任务共享源工程路径／文件对象占用，原账本缺失、损坏或unknown时不自动转交。两个真实进程并发仅一方获认领；原生持有者保全并继续保存重开通过。606项回归563通过／43条件跳过，15技能资源一致；9.3.2的GUI、完整会话、旧运行时并行及平台／宿主范围仍开放，发布快照不变。

文件代际修复候选：文件对象键加入创建时间，旧未知认领保全，无法取得可靠代际时拒绝。Linux以核对过的文件描述符读取statx，其他平台使用原生birth time。[证据](docs/evidence/project-creation-generation-candidate-20261009.json)区分本地容器合同与锁定Python、原生创作、宿主验收。source57/plugin59已发布快照不变，9.3.2保持开放。

本地桌面版本候选：受管理自有会话持久化工程和编辑上下文，原子保护execute_command、batch、打开／保存与run_script；未映射工具发送前拒绝，已确认只读工具调用后再核对。[证据](docs/evidence/desktop-native-revision-candidate-20261009.json)分别记录原生映射、桌面独立控制修改和已安装公开入口，不等同模型派发或物理GUI操作。已发布快照保持不变，完整9.3.2及V1仍开放。

桌面原子冲突核对候选：`docs/evidence/desktop-conflict-reconcile-candidate-20261009.json`。v2证明绑定任务、操作参数、会话基线及已停止的所属桌面；公开reconcile/resume可报告单个操作未执行，原attempted与成功回执保全。旧v1、非原子变化或缺停止证明保持unknown；任务未决时拒绝新任务绕过。本增量尚未发布，完整9.3.3／9.3.4及V1继续开放。

本次 source59／plugin61 开发发行包含桌面原子冲突核对和版本化命令完成证明。完成证明仅支持核对原结果后补齐交付登记；缺失、损坏或产物改变时拒绝恢复，取消期间不登记迟到交付。旧候选报告是其记录时点的证据，当前发行验证另见 `docs/evidence/release59-validation-20261009.json`；完整9.3.3／9.3.4、其他原生平台、宿主与V1保持开放。

未发布的[完成证明真实强杀候选](docs/evidence/command-completion-crash-candidate-20261009.json)：命令与自有桌面覆盖证明写入前、证明已写但引用未保存、引用保存后三个SIGKILL窗口。仅原完整证明可经原进程停止、隔离重开与PNG实际解码后登记交付；无证明或悬空证明保持unknown，重复resume不重发。同时补齐损坏ownership的结构化诊断，显式坏值不回退为缺字段。此候选不替代已发布source59／plugin61，完整9.3.3／9.3.4、其他原生平台与固定宿主继续开放。

source60／plugin62 发行分发真实强杀恢复增量及严格进程归属校验。候选报告保留当时未发布的观察上下文；本次发行绑定见 `docs/evidence/release62-plugin-validation-20261009.json`。完整V1仍有70项开放。

本地父子原生取消验收（9.36）完成：命令与自有桌面分别覆盖正常取消、取消落盘后监督器强杀。原冻结公开入口重启核对，父项等待子项，保存响应未登记继续未知；原工程／媒体／成功回执、截止／修订预算、共享资源及无关进程保全。四个原生案例与27项取消合同通过，4项默认原生条件跳过。[证据](docs/evidence/native-family-cancellation-candidate-20261009.json)保留夹具修正历史与明确边界：父项已登记未调度，非完整修订父工程；缓存复用，Python3.13.5，只有macOS arm64。生产代码未改，source60／plugin62固定快照不变；新测试／证据未提交发布。完整9.3.4及70项V1继续开放。

当前技术门禁9.4.1已验收：[证据](docs/evidence/technical-gate-acceptance-20261009.json)。带真实收集素材的MP4、普通与分段透明序列从独立只读技能公开入口完成保存／重开、解码和恢复幂等核对；坏视频／缺素材／坏工程的真实交付副本分别被拒绝，高分回执不能覆盖技术失败。六个原生正反例通过；78项目标回归72通过／6条件跳过。工程、媒体技术、创作及用户接受分列，后两项保持NOT_RUN。macOS arm64、隔离Python3.13.16与已校验缓存复用，不替代其他平台、模型派发或逐命令全部输出验收。当前V1尚有69项开放；生产快照source60／plugin62不变，新验收未提交发布。


本次发行：技能源 dev.61／插件 dev.63 纳入9.36原生父子取消与9.4.1技术门禁验收测试及证据；此前“未发布”描述保留各自检查点时态。技能执行资源与source60完全相同，69项V1任务仍开放，市场资格未变。


本地血缘候选（EC-AR-001，5.1–5.3进行中）：工作流在兼容的manifest中生成ArtCraft持有的craft-artifact/v1，绑定逻辑身份、不可变整包版本、实际任务、源版本、原生工程、派生引用和已收集媒体依赖。review和移动源包修订重验完整文件表；同名内容替换、旧版本复用、引用错配及链接拒绝。源包完整绑定写入任务授权，登记后清单／依赖变化在下一次编辑和交付前阻止。独立CLI显式standalone，旧包引用只登记可验证的legacy工程内容。当前为未发布技能源候选，插件仍锁定已发布source61；命令／桌面公共产物映射、字体／LUT依赖发现、固定发行和完整协议原生验收尚未完成，5.1–5.3不提前勾选。 [Evidence / 证据](docs/evidence/workflow-artifact-lineage-candidate-20261009.json).

本次发行：技能源 dev.62／插件 dev.64 分发工作流产物血缘与源工程包保护。原候选证据保留采集时点，发行快照绑定另见 release62-validation-20261009.json。697项回归633通过／64条件跳过；macOS arm64三个原生交付与当前执行资源一致。命令／桌面公共产物映射、字体／LUT发现、其他原生平台与宿主验收保持开放；5.1–5.3未勾选，V1仍有69项开放。


未发布来源生产任务保护候选：完整包复制／移动或换state-root后，受管理来源仍核对原任务、逐操作回执、持久交付摘要及所属进程停止证明。用户级定位记录只指向原账本，不能证明完成；新任务持久绑定来源，并在每次编辑意图／交付前重核对。10项定向测试、708项回归（643通过／65条件跳过）和真实worker完成包后、账本交付前SIGKILL案例通过；公开plan/run跨账本拒绝未知副本，原reconcile/resume不重放，已确认交付移动后的跨账本修订与原生重开／实际PNG检查通过。首轮原生夹具顺序错误留证。仅macOS arm64及缓存复用；完整9.3.3、旧包／命令／桌面矩阵、其他平台和宿主保持开放，当前69项未完成。插件继续锁定source62／plugin64。 [Evidence / 证据](docs/evidence/source-producer-guard-candidate-20261009.json).

本次发行 source dev.63／plugin dev.65 包含来源生产任务保护及 commands／自有桌面的公共产物映射：多工程分别登记真实任务、不可变包版本、原生工程、匹配PNG和媒体依赖；旧交付只读兼容。映射可随整包移动重验，不能替代技术、创作或用户验收。原候选报告保留观察时范围；当前发行证据见 [发行验证](docs/evidence/release63-validation-20261009.json)。字体／LUT发现、完整故障矩阵、其他原生平台与固定宿主派发继续开放；5.1–5.3不勾选，V1仍有69项未完成，不归档。


本次发行 source dev.64／plugin dev.66 新增原生字体与 LUT 资源观察，覆盖保存工程的文字样式、字符样式、关键帧及支持的 LUT 属性。只为实际取得的 LUT 字节登记摘要；字体名称不会冒充字体文件。未知字体、动态资源、文件 LUT 的运行路径和视觉保真分别保留 NOT_RUN；旧交付不自动升级身份。验证范围见 [本次发行证据](docs/evidence/native-resources-release64-20261009.json)。5.1–5.3及69项V1任务继续开放，不归档。


未发布文件LUT审阅候选：公开命令／自有桌面review在隔离原生副本重关联已声明、打包的LUT输入，比较解码采样帧并保全原件。每次核验渲染先持久预占任务族预算；未知资源、缺帧或预算耗尽使工程门禁保持NOT_RUN，摘要／像素不符则FAIL。绑定的绝对声明可在搬迁后按相对包内容重关联，不读取旧地址。工作流已接通路由，但其文件LUT创建与review真实验收仍开放。插件继续消费已发布source64／plugin66，既有CI及原生报告不能证明本候选。证据：[文件LUT候选](docs/evidence/file-lut-validation-candidate-20261009.json)。5.1–5.3及69项V1任务继续开放。


技能源 dev.65 / 插件 dev.67 发布文件 LUT 隔离核验、绑定交付包迁移重关联与持久化审核渲染预算。历史候选报告保留当时观察状态；当前回归679项通过、72项条件跳过，macOS arm64两项原生用例通过。工作流文件 LUT 原生验收、字体、完整时序与创作评价、其他原生平台及宿主门禁继续开放。[发布证据](docs/evidence/file-lut-release65-20261009.json)。5.1–5.3及69项V1任务仍未完成。


Source dev.66 / plugin dev.68 correct current release identity documentation. Execution payloads and test files are byte-identical to source65; immutable source65/plugin67 tags are retained. See [release binding](docs/evidence/file-lut-release66-20261009.json).


Source dev.67 / plugin dev.69 correct a Windows absolute-path test fixture without changing execution resources. Source65/66 Windows CI failed that fixture; prior tags are retained. The original content-rejection assertion is preserved and all15 file-LUT tests pass locally. [Release binding](docs/evidence/file-lut-release67-20261009.json).


未发布停止观察候选：POSIX守护仅在原5秒停止窗口内重查瞬态成员查询失败，并把剩余时间传给查询；空表／畸形表不作为停止证明。持续失败仍unknown，业务结果与强制组停止分开。基线100次真实macOS沙箱取消复现1次失败，修复后100次通过。完整故障／平台／宿主门禁继续开放，插件保持source67／plugin69固定快照。[候选证据](docs/evidence/stop-observation-candidate-20261009.json)。


技能源 dev.68／插件 dev.70 分发POSIX有限停止核验及工作流合成配置门禁。历史候选证据保留观察时范围。[发布证据](docs/evidence/release68-validation-20261009.json)。完整领域、其他原生目标及宿主验收保持开放，仍不具备市场准入资格。

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

插件展示使用上游官方图标；名称为 **EffectCraft Use**。图标来源与许可证保存在 `assets/official-icon-source.json` 和相邻 LICENSE 文件中。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。


## 片头片尾场景候选 / Intro and outro scene candidates

新增章节标题卡、3–2–1开场倒数、片尾滚动署名三个独立技能。每项含原生CLI与同会话MCP方法、明确参数、时间单位、输入替换和输出检查。源于固定GitHub流程事实的原创适配，不复制模板代码。原生合成样本验证与真实成片、宿主同步分开记录；冻结基础技能版本与运行时不变。

- [effectcraft-chapter-card](skills/effectcraft-chapter-card/SKILL.md)
- [effectcraft-countdown-intro](skills/effectcraft-countdown-intro/SKILL.md)
- [effectcraft-credits-roll](skills/effectcraft-credits-roll/SKILL.md)
