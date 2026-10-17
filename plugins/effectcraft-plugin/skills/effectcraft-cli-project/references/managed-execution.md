# 受管理任务 / Managed execution

从 effectcraft-harness 技能实际加载目录调用 `scripts/launch.sh`（macOS/Linux）或 `scripts/launch.ps1`（Windows）。启动器仅在用户缓存准备锁定 Python；脚本、工程与输出均不得写入技能目录。七个平台制品可用不等于七个平台已通过原生验收。

| 操作 | 参数与行为 |
| --- | --- |
| doctor | Python 入口只读环境与锁定能力，不安装 EffectCraft |
| plan | `--plan FILE --output NEW_DIR [--mode workflow/commands/desktop]`，不编辑工程 |
| run | 同上，可指定 `--task ID`；先持久化身份再执行 |
| inspect | `--task ID`，返回期限、步骤、未知结果、回执 |
| reconcile | `--task ID`，核对原交付，不发送原编辑 |
| resume | `--task ID`，继续确定尚未开始的任务或已核对的分段导出；未知编辑不重放 |
| cancel | `--task ID`，先阻止父子任务调度；监督器确认自有进程停止 |
| review | `--task ID --criteria FILE [--judge RECEIPT]`，实际解码与宿主评价 |
| revise | `--task ID --plan FILE --output NEW_DIR`，范围、版本、预算均校验 |

全局参数 `--state-root`、`--runtime-home` 放在操作前。环境变量 `CRAFT_STATE_HOME`、`CRAFT_RUNTIME_HOME`、`CRAFT_PYTHON_HOME` 可隔离不同安装。固定离线 Python 包使用 `CRAFT_PYTHON_ARCHIVE`，EffectCraft 原生包使用 `CRAFT_RUNTIME_ARCHIVE`；公开 `run` 自动消费两者，无需先安装 Python 或手工调用另一安装器。原生安装器／兼容 CLI 的显式 `--archive` 优先于环境变量。离线制品仍必须匹配当前平台锁定摘要；缺失、损坏或安装失败会停止，不回落联网下载。完整已安装版本先核验复用，无需读取待用归档。路径建议使用绝对路径，可含空格；缓存放在用户可写目录，技能目录可以只读。

`workflow` 计划沿用原生合成格式；`commands` / `desktop` 沿用 `craft-command-plan/v1`。不得把未解析的自然语言直接当作原生参数。输入通过 `--input name=/absolute/file` 指定；已有工程通过 `--source DELIVERY --expectedProjectSha256` 对应计划字段核对（摘要写在计划，非命令行参数）。

### 按计划格式选择写入模式

`workflow` 是默认模式，仅接收原生合成计划（例如 `brand-intro.json`）；`craft-command-plan/v1` 必须显式选择 `commands` 或自有桌面 `desktop`，不能交给默认 workflow。桌面模式会准备固定桌面制品并启动本任务拥有的会话，不连接或关闭用户已有桌面。

```sh
sh "$HARNESS_DIR/scripts/launch.sh" plan --mode workflow --plan "$SKILL_DIR/examples/brand-intro.json" --output "/absolute/new workflow"
sh "$HARNESS_DIR/scripts/launch.sh" run --mode commands --plan "$SKILL_DIR/examples/commands-advanced.json" --output "/absolute/new commands"
sh "$HARNESS_DIR/scripts/launch.sh" run --mode desktop --plan "$SKILL_DIR/examples/desktop-first-use.json" --output "/absolute/new desktop"
```

```powershell
& "$HARNESS_DIR/scripts/launch.ps1" plan --mode workflow --plan "$SKILL_DIR/examples/brand-intro.json" --output 'C:\new workflow'
& "$HARNESS_DIR/scripts/launch.ps1" run --mode commands --plan "$SKILL_DIR/examples/commands-advanced.json" --output 'C:\new commands'
& "$HARNESS_DIR/scripts/launch.ps1" run --mode desktop --plan "$SKILL_DIR/examples/desktop-first-use.json" --output 'C:\new desktop'
```

原始 `commands.py run PLAN --output DIR`、`desktop.py run PLAN --output DIR` 和 `cli.py -- ARGV` 保留公开兼容契约，供明确指定的兼容调用使用；技能默认创作不直接调用它们。已有未知任务只用原任务的inspect/reconcile/resume核对，不能借兼容入口另做一遍。

任务记录使用内部 `effectcraft-managed-task/v2`，公共 `craft-task/v1`、`craft-artifact/v1` 所有权不变。旧交付可以复核；旧 v1 状态可检查但不可恢复执行；缺少版本化状态的历史任务不能自动转成可执行任务。运行时改变时原任务拒绝切换，应保留原技能快照与旧缓存执行诊断。

POSIX 离线首用（制品须预先准备，版本与平台以技能内锁为准）：

```sh
export CRAFT_PYTHON_ARCHIVE="/absolute/offline artifacts/python.tar.gz"
export CRAFT_RUNTIME_ARCHIVE="/absolute/offline artifacts/effectcraft.zip"
sh "$HARNESS_DIR/scripts/launch.sh" run --plan PLAN.json --output "/absolute/new result"
```

Windows PowerShell：

```powershell
$env:CRAFT_PYTHON_ARCHIVE='C:\offline artifacts\python.zip'
$env:CRAFT_RUNTIME_ARCHIVE='C:\offline artifacts\effectcraft.zip'
& "$HARNESS_DIR/scripts/launch.ps1" run --plan PLAN.json --output 'C:\new result'
```

原生桌面制品另有锁与安装入口；这两个环境变量准备 Python／headless CLI，不冒用桌面安装验收。网络完全不可用时，离线创作与评估所需素材、字体及媒体解码器也须已具备；缺少解码器的技术评价保持 `NOT_RUN`。

## 宿主 Judge 与有限修订

计划默认保留透明预览契约。明确需要普通不透明背景预览时设置 `previewAlpha: false`；透明交付保持 true 并检查真实 alpha，不事后改写门禁来迁就成品。初始计划应根据用户已授权的文字、位置等范围填写 `revisionScope`（参考 brand-intro 模板）；不允许通过 `run --source` 为受管理工程换新任务绕过修订预算。

1. `review` 输出 `judgeRequest`，绑定任务、工程、全部产物与评价标准。实际打开请求列出的图片/视频；技术检查 PASS 不能代替视觉与时序观察。
2. 使用显式 `effectcraft-judge-request/v2` / `effectcraft-judge-receipt/v2`。回执原样绑定 `requestId`、`taskId`、`binding`、`criteriaHash`、`scopeHash`；实际观察请求的帧样本后填写 `capabilities`、`observations`（媒体路径/摘要、帧索引、方法及观察描述）、`status`、`score`、`passed`、`issues`、`temporalReviewed`。缺视觉/时序能力或样本覆盖时返回 NOT_RUN，不计分、不选最佳。具体宿主步骤见 [Codex Judge 适配](codex-judge.md)。
3. 再次 `review --judge RECEIPT` 导入回执。过期文件、摘要变化或技术失败均拒绝。`accepted` 保持 false，等待用户接受。
4. workflow初始计划声明 `revisionScope: [{"layer":"title","properties":["text/sourceText"]}]`。创作 FAIL 后可调用 `revise`，仅支持该范围内 `layer.setText` / `prop.set`，不开放任意命令网关；修订计划必须包含 `expectedProjectSha256`，不得新建 document 或扩大素材/对象范围。
5. 每轮先持久化预算，再基于原工程另存。完整比较非目标属性与关键帧，重开、渲染、再评估。最多 2 轮、任务总期限 1800 秒；连续两次无改善停止。`bestTask` 指向最佳已评价版本，失败现场保留。

工程 PASS、媒体 PASS、创作 PASS/FAIL/NOT_RUN、用户接受分别记录。取消进程后如果存在已尝试而无回执的编辑，状态保持 reconciling，终止成功不等于编辑未发生。

受管理执行通过独立 `process_guard.py` 持有生命周期锁。监督进程消失时控制管道关闭，守护器继续停止自有进程树并写入 `lifecycle.json`；reconcile 在生命周期锁被占用或停止证据不完整时拒绝核对续写。POSIX 使用独立进程组，Windows 使用带门控启动的 Job Object，Windows 原生验证仍待完成。没有生命周期证据的旧任务只能诊断，不能据 PID 推断可以恢复。

分段恢复：先 `reconcile` 核对原任务及自有进程停止证据，再 `resume`。工程、输入、运行时、执行资源及帧检查点必须一致；只续跑导出，完整已完成段和编辑回执保全。重复调用已交付任务返回原结果，不重发编辑。

共享资源：受管理 `workflow` 在预览/导出前将帧数和解码字节预占到根任务 `resources` 账本；父子共享10000帧、64GiB解码量与2GiB编码媒体上限，序列仍保留原有更严格的单次限制。初次输出及修订合计使用额度；恢复复用原预占，失败不自动归还。实际媒体字节按高水位记录，删文件或重启不会降低已用量。使用 `inspect --task ROOT_ID` 查看根任务账本；子任务的 `parent` 指向原任务族。缺少账本的历史任务仅可诊断；损坏或悬空预占保留现场并拒绝写入。命令计划、桌面、CPU/内存及跨平台资源计量仍待验收。

当前限制：管理入口不自动重放部分创作任务。Web 与 FreeBSD 不走 Linux 二进制；分别使用浏览器与源码通道，并单独记录验收。


## Web 与 FreeBSD 独立通道

`additional_platforms.py web-install --archive PINNED_ZIP` 验证并安装固定 Web 包，`web-serve --port 0` 只在回环地址提供带 COOP/COEP 的站点。浏览器载入后使用本技能 `web_adapter.mjs` 的 `discover/inspect/readArtifact`，读取上游公开的 `window.effectcraft` API。Web 的受管理写入与完整作品验收仍是独立开放项；不能把页面载入当成创作成功。

`additional_platforms.py freebsd-build` 只在实际 FreeBSD 上执行固定提交源码的 `cargo build --locked` 和引擎测试，要求已准备构建工具与锁文件列出的系统库。失败保留构建日志和源码，不借用 Linux 包或静默安装全局工具。当前主机没有 FreeBSD 目标环境，源码构建及原生任务验收未通过。


## 固定版本评价 / Settled version reviews

`review` 对同一版本复用原Judge请求。任务族的评价标准从首次请求起固定，重复导入同一回执不会再次计入停滞；同一请求的冲突评分拒绝。已结算请求、响应和报告保存在任务私有 `reviews/REQUEST_ID/`，根任务内部 `effectcraft-review-ledger/v1` 原子结算，子引用写入中断可由相同导入修复。`inspect` 返回的 `bestVerified` 绑定最佳工程/技术验证版本及不可覆盖的报告摘要。原产物改变、回执损坏、祖先取消或期限到达会拒绝新的评价状态变更。缺少评价账本的历史评分仅允许检查，不自动重置比较和停滞预算。

For a settled version, `review` reuses its original Judge request. A task family keeps the first criteria; identical imports are idempotent and conflicting responses are rejected. Immutable request/response/report files live in private `reviews/REQUEST_ID/` directories. The root `effectcraft-review-ledger/v1` commits each version once, and an interrupted child reference can be repaired by the same import. `bestVerified` binds the best engineering/technical verified version to its report digest. Changed artifacts, corrupt receipts, ancestor cancellation or deadline expiry prevent further review mutations. Historical scores without this ledger remain diagnostic; comparison and stagnation budgets are never reset automatically.

Judge v2仅验收`scope.coverage=sampled`列出的具体样本，不能据此声称全帧创作通过。旧v1请求/评分保留诊断读取，不自动升级或用于新的修订。无能力的回执保存在`review-attempts/`，不会消耗停滞次数。 / Judge v2 accepts only its declared sample coverage. It does not claim all-frame creative acceptance. Legacy v1 requests/scores remain diagnostic; NOT_RUN receipts are retained without scoring or consuming stagnation.

## 视频与素材复检 / Video and dependency verification

视频技术检查实际解码全部媒体，核对合成帧数、零起点及连续时间格；封装时长容差不能掩盖少一帧。声明alpha的视频须实际解码为带alpha的像素格式，不透明视频不能冒称透明保真。素材声明的包内路径与摘要必须同时匹配实际文件和交付文件表。缺解码器保留NOT_RUN；这些技术结果不能代替原生工程重开或创作评价。

Video checks decode the media and verify exact composition frame count, zero-based timestamps and continuous frame timing. Duration tolerance cannot hide a missing frame. Declared video alpha requires an actual decoded alpha pixel format; opaque media does not prove transparency. Each declared dependency must match both its actual package file and file-table digest. Missing decoders remain NOT_RUN. Technical results do not replace engineering reopen or creative judgment.

## 当前工程检查 / Current engineering verification

`review`每次都核验任务绑定的已安装原生运行时，在临时目录复制工程及声明素材，实际重开、执行缺失素材检查，并比较原生合成与图层。原工程和素材不保存、不修改；前后摘要变化会失败。缺运行时或重开超时保持工程NOT_RUN，不能沿用历史PASS；原生错误或结构差异为FAIL。已结算报告原样保留，当前检查不通过时创作NOT_RUN、不可接受，不生成新的视觉请求。`revise`在预算检查后、扣减轮数前再次执行同一工程核验。

Each `review` verifies the task-bound installed native runtime, copies the project and declared assets to a temporary package, reopens it, checks missing footage and compares the exact native composition/layers. It never saves or edits originals; changed original digests fail. Missing runtime or incomplete timeout is engineering NOT_RUN, while native errors/structural drift fail. Immutable historical reports remain intact but do not replace current verification. Failed current checks leave creative NOT_RUN, with no new visual request. `revise` repeats engineering verification before consuming a revision round.

质量回执兼容`accepted`布尔值，并增加独立`userAcceptance.status=NOT_RUN`；工程、技术和模型创作通过均不能代替明确的用户决定。 / The quality report retains the compatible `accepted` boolean and adds independent `userAcceptance.status=NOT_RUN`. Engineering, media and model judgments never substitute for an explicit user decision.

## 命令与桌面交付复检 / Command and desktop delivery review

受管理 `--mode commands` 和 `--mode desktop` 会在任务状态目录保存内部交付观察：保存/PNG渲染前读取全部原生合成与图层，返回后固定工程、媒体与素材摘要。`craft-command-plan/v1`、`craft-command-receipt/v1` 和用户输出文件名保持兼容；不向交付目录写入额外 manifest/native 文件。多次写入同一路径只把最后明确写出的文件列为当前交付，之前观察保留。

`review --task TASK --criteria CRITERIA.json` 核对原成功回执和完整输出清单，使用固定运行时隔离打开每个当前工程，检查全部合成、图层和素材。PNG按自身渲染时合成、实际解码尺寸及alpha核验；只有匹配保存版本的媒体才能通过来源关联。未保存渲染版本、未覆盖导出、缺运行时或观察记录变化不会被旧PASS覆盖。缺观察的历史命令任务仅供诊断，不补建基线、不重放。

当前命令与桌面候选在工程/技术PASS后产生既有Judge v2请求，复用不可覆盖账本。`scope.contexts`分别绑定每个合成/原生版本及素材身份、时间基准和所需帧；每个媒体通过`context`关联对应范围。必须分别满足各上下文样本并实际查看全部`requiredMediaPaths`，不同作品不能互补缺帧。缺视觉/时序/媒体覆盖保留NOT_RUN；冲突或过期回执拒绝，相同回执幂等。创作PASS不代签用户接受。命令视频/序列及自动局部修订整合仍待完成。

Managed commands and owned-desktop runs persist internal observations in task state, binding each saved project or named PNG to its native context and actual bytes. Public command schemas and user outputs stay compatible. Review checks the original receipt, full inventory, every saved composition/layer and dependency through isolated native reopening, and actual PNG dimensions/alpha against its own render context. A later project cannot stand in for an unsaved render version. Historical tasks without observations remain diagnostic-only. Video/sequence, Judge and automatic command revision integration remain open; engineering/technical PASS alone never sets creative or user acceptance to PASS.

Command/desktop review now emits the existing Judge v2 request after current engineering and technical gates. `scope.contexts` independently binds each composition/native version, dependency identity, timebase and required frames; media rows reference their context. Observe every required media path and meet each context’s sample coverage. Frames from different works cannot fill one another’s gaps. Missing visual/temporal/media evidence remains NOT_RUN; conflicting/stale receipts are rejected and identical imports are idempotent. User acceptance stays independent. Command video/sequence and local revision integration remain open.

## 命令／桌面局部修订候选 / Command and desktop local revision candidate

原始 `craft-command-plan/v1` 不增加字段。`plan` 与 `run --mode commands|desktop` 通过独立 `--revision-scope SCOPE.json` 在创建任务前绑定授权；文件内容示例：

```json
[{"project":"title.ecproj","comp":"main","layer":"title","properties":["text/sourceText"]}]
```

`main` 必须是原计划 `comp.new` 的创建别名，`title` 为原计划的图层创建别名，工程路径必须由原计划声明保存。别名只从原成功回执解析，不能以新ID扩大范围。缺范围的历史任务不补建授权。

当前工程和技术通过、Judge FAIL 已结算后，`revise --task ORIGINAL_ID --plan REVISION.json --output NEW_DIRECTORY` 接收以下内部管理请求；不是新的公开 craft 交付协议：

```json
{"schema":"effectcraft-command-revision/v1","binding":{"commandDeliverySha256":"COPY_CURRENT_BINDING","receiptSha256":"COPY_CURRENT_BINDING","filesHash":"COPY_CURRENT_BINDING"},"project":"title.ecproj","operations":[{"comp":1,"command":"layer.setText","params":{"layer":2,"text":"NOVA"}}]}
```

完整复制当前 Judge 请求的 `binding`，使用原成功回执的实际 comp/layer ID。仅支持事先授权的 `layer.setText` 与静态 `prop.set`；有动画关键帧的目标属性拒绝，未来时间范围授权另行验收。text-only 操作只豁免文字内容比较，字号、字体、描边等仍须保全。

子任务沿用原模式和运行时，以私有工程副本重开，在新输出保存全部当前工程并重新渲染全部绑定PNG。只允许目标属性变化及摘要相同素材的路径搬迁；其他原生字段、关键帧和未受影响媒体像素保持一致。原任务／工程／媒体不改写。子版本共享原任务30分钟期限、最多两轮、停滞及资源预算，尝试前持久扣轮数，失败不退回。完成后对返回子任务ID执行 `review`，实际查看新样本后导入新的Judge回执。

若监督器在原生完成后断开，只能 `inspect` / `reconcile` 原子任务。必须有已退出进程证据和既有 `preservation.json` 才解除根任务修订占用；缺回执不补建基线，部分编辑保持未知，不通过另起任务自动重做。视频／序列、动画目标时间范围、完整宿主派发与各平台验收保持独立开放。

Commands and desktop runs bind a separate `--revision-scope` file before execution; raw command plans stay compatible. A settled creative FAIL plus fresh engineering/technical PASS permits the internal revision request above, bound to the current Judge binding and original native IDs. Only authorized static properties/text can change; animated targets require a future time-scoped contract. Text-only changes preserve nested font/style fields. Child versions reopen private copies, save all projects and rerender all bound PNGs, preserving originals and non-target native fields/pixels. They share the original deadline, two-round, stagnation and resource budgets. Review the returned child ID and actually observe its samples. Interrupted completion can release ownership only through verified stopped-process and existing preservation receipts; unknown edits are never replayed. Video/sequences, animated time scopes, full host dispatch and target-platform acceptance remain separate gates.

生成器内部版本2在编辑前显式选中授权图层。旧版计划不改写或重发；`reconcile` 可核对注册表阻断：仅当持久调用序列、参数/结果摘要、失败日志、源/种子和停止证明完全对应，且全部已发送调用只有读取/open_project/comp.open/layer.select、无工程或媒体新输出时，才记录 `revision_not_executed`。这会保留失败子任务、记录 `not-executed.json`、解除占用，但不退回轮数或自动重试。缺证据仍为unknown。 / Generator v2 explicitly selects the authorized layer before editing. Old plans are never rewritten or resent. Reconciliation can prove a registry-blocked edit was not sent only through exact durable call/argument/result matching, unchanged source/seeds, stopped-process evidence and absence of edited outputs. It retains the failed child and spent attempt; no automatic retry or refund occurs.

未执行结算中断的子任务仍需通过公开reconcile核对既有证明与原始证据才能解除根占用，子任务failed状态本身不足以证明安全。缺失败回执返回revision_outcome_unknown。初始commands/desktop渲染的全任务族资源计量，以及过期／取消后完整结算矩阵仍待完善；当前只证明子版本重渲染预占，不据此声明全资源合同完成。

Interrupted not-executed settlement requires public reconcile to verify the existing immutable proof and original evidence; a failed child alone cannot release occupation. Missing failure receipts report revision_outcome_unknown. Initial command/desktop family-wide render accounting and expired/cancelled settlement qualification remain open; child rerender reservations do not prove the complete resource contract.

当前候选命名PNG模式已把根计划帧数和逐帧原生尺寸计入共享账本；对子版本预占取覆盖上界，编码字节高水位跨重启／删除保持。旧根任务缺少帧计量时拒绝自动revise，仍可检查诊断。reconcile核对既有完成／未执行证明时可在过期或取消后结算占用，但不能恢复执行权限、退款或重放。其他导出模式、CPU／内存、动画目标时间范围及跨平台／固定宿主仍独立开放。

Current candidate named-PNG modes account for original and child frames/native decoded sizes without double billing, and retain encoded high water. Roots lacking original frame evidence refuse automatic revise. Reconcile may settle existing completed/not-executed proof after expiry/cancel without authorizing more work, refunding or replaying. Other export modes,CPU/memory,animated-target scope and platform/fixed-host gates remain open.


### 只读诊断与实际能力 / Readonly diagnostic and actual capability discovery

```bash
sh "$HARNESS_DIR/scripts/launch.sh" doctor
sh "$HARNESS_DIR/scripts/launch.sh" doctor --probe-native
sh "$HARNESS_DIR/scripts/launch.sh" doctor --compare-catalog /absolute/previous-command-coverage.json
```

默认doctor只核验平台、锁、当前Python、已安装CLI完整性及固定目录，返回实际可调用的恢复argv，不执行恢复动作。没有Python时Shell／PowerShell入口仍只读返回缺失信息，不自动下载；直接Python入口也不创建运行时或任务目录。显式`--probe-native`仅在CLI完整性、最低系统条件均通过后查询`--version`及自有`--empty mcp`的`tools/list`／`list_commands`，限时、不重试，不连接已有桌面，不编辑／渲染，也不恢复未知任务。探测PASS仅表示版本／注册身份／工具schema一致，创作、原生平台整体和宿主验收仍NOT_RUN。

目录／schema漂移或版本不符报告FAIL；查询失败／超时保持NOT_RUN。损坏安装保留原样，探测不启动。`--compare-catalog`复用离线差异合同，坏旧目录先失败，不借诊断启动原生进程。恢复argv是可选动作，不是新安装或扩大编辑授权。

Default doctor is static and readonly. Explicit --probe-native checks only a previously integrity-verified CLI in its own empty headless session; discovery PASS never establishes creative, desktop or host acceptance. Version/schema drift is FAIL, unavailable discovery remains NOT_RUN. Recovery argv is reported and never executed automatically; corrupted runtime and unknown task records are preserved.

## 任务私有执行绑定 / Task-private execution binding

新任务在启动 worker 前保存 `effectcraft-execution-binding/v1` 及私有 `execution/skill` 快照，绑定解释器、执行代码、参数/命令合同和原生版本。技能目录更新后，resume/reconcile/review/revise 使用原组合；修订子任务沿用原控制器并冻结自身执行资源。默认隔离 Python 校验整个发行载荷；直接 Python 兼容入口只绑定解释器文件，不表示已隔离。

缺少或损坏快照/清单/解释器时保留现场并拒绝启动，不从当前技能重建。历史无绑定任务可 inspect 和诊断，resume/revise 返回 `legacy_execution_binding_missing`；未知任务不得换 ID 或输出目录重做。所有被引用版本继续保留；单一状态根的引用清单不授权跨状态根清理。Windows 接管使用自有 Job 守护和监督通道，真实目标验收单独记录。

New tasks freeze execution resources before starting a worker. Recovery/review/revision dispatch to the original Python/controller/native combination after validating the manifest. Locked Python checks its complete distribution; the direct external-Python compatibility entry binds only the executable. Missing/corrupt snapshots and legacy tasks are never reconstructed or replayed. Retain referenced versions; state-root references cannot authorize global cleanup. Native Windows handoff qualification remains separate from adapter tests.


父子任务取消：根任务的 `cancellationFamily` 绑定后代身份。`pendingTasks` 非空时保持 cancel_requested；通过各子任务原控制器 reconcile 后再核对父任务。`unknownTasks` 非空时保持 reconciling，不得换任务 ID 或输出目录重做。未启动证明只在原取消时、全部执行租约可取时生成，恢复不补造。

Family cancellation binds descendant identities in `cancellationFamily`. Pending descendants retain cancel_requested; reconcile children through their original controllers before reconciling the parent. Unknown edits retain reconciling and must never be replayed with a new ID or output directory. A not-started proof is captured only during original cancellation while all execution leases are available.


## 历史记录与取消入口

缺少原运行绑定的历史任务仅允许 `inspect` 与诊断导出。`reconcile`、`resume`、`cancel`、`review`、`revise` 拒绝写入，不补造身份、租约或回执，不借新任务重做未知编辑。状态缺失、损坏、悬空回执和状态根链接返回错误并保留现场。

直接调用 `managed.py cancel` 与 Shell / PowerShell 入口遵循同一任务绑定，交接原隔离 Python 和冻结控制器。当前父任务取消遇到旧版子任务时保留取消意图，旧子任务保持只读且停止未确认，父任务不会提前声称全部停止。
