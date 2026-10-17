# EffectCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.6`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.6` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


Create editable `.ecproj` projects, dependencies and media from text, graphics and footage. This is a development release; full V1 remains open. Published releases and local documentation candidates have separate evidence.

Current plugin: `0.1.0-dev.20261017.6`; skill source: `0.1.0-dev.69`; 16 independent skills (15 domain + 1 bundled execution harness).

| Field | Value |
| --- | --- |
| Metadata version | 0.1.0-dev.20261017.6 |
| Skills source | effectcraft-skills / v0.1.0-dev.69 |
| Acceptance | Development; full V1 OPEN |

## Plugin boundary

Agent Plugins 1.0.0 discovers this package through root `plugin.json` and its 15 skills. Commands and hooks, when provided, are client extensions rather than portable core components. The official EffectCraft CLI performs native editing; the host agent plans, observes media and decides creative revisions. Skill scripts currently provide pinned first-use setup and deterministic execution/recovery checks. The package has no root `mcp.json`, so it does not yet expose a portable MCP server, even though the upstream CLI supports MCP. Cross-platform MCP startup and host acceptance remain open; see the [architecture decision](openspec/changes/establish-v1-plugin/design.md#agent-plugin-边界2026-10-09).


## First use

Invoke **`effectcraft-use`** in the host. For direct invocation, set `SKILL_DIR` to the absolute directory containing the actually loaded `SKILL.md`. Launchers prepare and verify pinned Python and EffectCraft in user data; system Python, global PATH and readonly skill files are preserved. Offline use requires pinned official archives or an intact verified cache.

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

[Workflow and delivery](skills/effectcraft-use/references/workflow.md) · [Setup and diagnostics](skills/effectcraft-cli-setup/SKILL.md). Generic Skills CLI installation and fixed-host natural-language dispatch retain separate acceptance gates.


## Current capabilities and evidence

The maintainer-generated [current matrix](docs/current-capabilities.json) binds the complete skill payload, Python/native artifacts and original report digest. Published source53 macOS arm64 technical samples passed. Source54/plugin56 change the receipt implementation; the old report does not validate the new payload, so the current matrix stays NOT_RUN. New public-interface native evidence is scoped separately; other architecture, browser, FreeBSD, creative and host gates stay NOT_RUN until verified. Portable CI contracts do not establish native creative acceptance.

The source53/plugin55 [15-skill report](docs/evidence/native-smoke-source53-20261009.json) passes native reopen and 12 decoded frames per case, using verified caches (zero cold installs). It does not prove 15 domain scenarios or model dispatch. [Cancellation recovery and family barriers](docs/evidence/cancel-family-candidate-20261009.json) preserve unknown edits; the full crash/GUI matrix remains open.


## Skill entry points

| Skill | Purpose |
| --- | --- |
| [effectcraft-use](skills/effectcraft-use/SKILL.md) | Task routing and delivery |
| [effectcraft-cli](skills/effectcraft-cli/SKILL.md) | General command planning |
| [effectcraft-cli-setup](skills/effectcraft-cli-setup/SKILL.md) | Runtime setup and diagnostics |
| [effectcraft-cli-project](skills/effectcraft-cli-project/SKILL.md) | Projects and native save/reopen |
| [effectcraft-cli-footage](skills/effectcraft-cli-footage/SKILL.md) | Footage and dependencies |
| [effectcraft-cli-composition](skills/effectcraft-cli-composition/SKILL.md) | Compositions |
| [effectcraft-cli-layers](skills/effectcraft-cli-layers/SKILL.md) | Layers and properties |
| [effectcraft-cli-animation](skills/effectcraft-cli-animation/SKILL.md) | Animation and keyframes |
| [effectcraft-cli-effects](skills/effectcraft-cli-effects/SKILL.md) | Effects |
| [effectcraft-cli-masks](skills/effectcraft-cli-masks/SKILL.md) | Masks |
| [effectcraft-cli-expressions](skills/effectcraft-cli-expressions/SKILL.md) | Expressions |
| [effectcraft-cli-camera](skills/effectcraft-cli-camera/SKILL.md) | Cameras and 3D scenes |
| [effectcraft-cli-export](skills/effectcraft-cli-export/SKILL.md) | Rendering and export |
| [effectcraft-cli-tracking](skills/effectcraft-cli-tracking/SKILL.md) | Tracking |
| [effectcraft-cli-puppet](skills/effectcraft-cli-puppet/SKILL.md) | Puppet pins and recording |

Each skill includes its own runtime resources and installs independently. Bundled references describe parameters, ownership and modes for 655 commands; catalog coverage does not prove every command was executed.


## Inspect, recover and cancel

Use `inspect` for the original task, `reconcile` to verify original receipts, and `resume` only for proven recoverable work. `cancel` persists intent; parents wait for descendants and unknown edits retain reconciling. Never replay unknown edits with a new task ID/output directory. Tasks retain their bound runtimes; corrupt or missing evidence is preserved and blocks further writes.

[Managed execution](skills/effectcraft-use/references/managed-execution.md)


## Maintenance and version history

The skill source owns execution code; the plugin consumes pinned tags, commits and whole-skill digests. The incremental authority is plugin `openspec/changes/establish-v1-plugin`; incomplete gates prevent archival. ArtCraft owns public `craft-task/v1` and `craft-artifact/v1`; EffectCraft consumes them.

[Version records and complete prior README](RELEASE-HISTORY.md) · [Plugin specifications](https://github.com/full-aigc-plugins/effectcraft-plugin/tree/main/openspec/changes/establish-v1-plugin)

The dev.56 [public interface acceptance](docs/evidence/managed-public-interface-candidate-20261009.json) completes task 9.3.5: receipt identity/orphan guards and nine management roles, with actual native recovery and Codex-observed local revision. Source54/plugin56 distribute this increment; source53/plugin55 remain historical releases. Other native platforms and fixed-host dispatch remain open; subsequent local three-mode composition evidence is below. The [source52 report](docs/evidence/native-smoke-source52-20261009.json) is historical evidence.

Local [three-mode public composition acceptance](docs/evidence/managed-three-mode-composition-20261009.json) completes task 9.3.6 against unchanged released source54/plugin56 payloads: workflow, command plans and actual owned desktop sessions pass installation/adapters/ledger/receipts/recovery, with original-plan replay refusal and legacy CLI compatibility. Default regression: 586 tests, 545 passed, 41 conditional skips; three native conditional cases separately pass. This test/evidence increment is distributed in source55/plugin57; its original native payload binding remains source54/plugin56. Full crash/GUI, other native targets, fixed-host dispatch and full V1 remain open.


Source dev.55 / plugin dev.57 distribute [default managed routing](docs/evidence/managed-default-routing-20261009.json): all 15 skills document workflow/commands/desktop writes; 45 readonly preflights and 18 legacy-action cases pass. Regression: 589 tests, 548 passed, 41 conditional skips. Tasks9.3.1 and9.3.6 are complete; 70 tasks remain open. Native evidence reuses only 105 unchanged execution resources; three guidance files differ. No new model dispatch or full-platform acceptance is claimed. Candidate reports retain their original validation timestamp; release bindings are recorded separately.


Source56/plugin58 fix Windows default-encoding dependence in the new routing tests by reading UTF-8 explicitly. Source55 failed Windows CI and original tags are retained. Skill execution payloads are unchanged; no new native or host acceptance is claimed.


Unpublished [source revision conflict protection](docs/evidence/source-revision-conflict-candidate-20261009.json) rechecks the source before each operation intent and final delivery. An external native save blocks the next edit while preserving the new source and existing receipts. Regression: 595 tests, 553 passed, 42 conditional skips; the explicit native save-conflict case also passes. Full task9.3.2 GUI/session/cross-state-root gates remain open; published source56/plugin58 snapshots are unchanged.


Unpublished [cross-store project claims](docs/evidence/shared-project-claims-candidate-20261009.json) coordinate source paths/file objects for new tasks. Missing, corrupt or unknown owners are not automatically cleared. Two real processes select only one owner; the native owner continues and saves/reopens after a competing store is rejected. Regression: 606 tests, 563 passed, 43 conditional skips; all 15 private resource copies match. GUI, complete sessions, parallel old runtimes and platform/host task9.3.2 gates remain open. Published snapshots are unchanged.

File-generation repair candidate: source claims now bind creation time with the file number, preserve legacy unconfirmed claims and reject unavailable creation identity. Linux uses verified-descriptor statx; native birth time is used elsewhere. [Evidence](docs/evidence/project-creation-generation-candidate-20261009.json) distinguishes local container contracts from pinned Python, native creative and host gates. Source57/plugin59 remain the immutable published baseline;9.3.2 remains open.

Local desktop revision candidate: owned managed sessions persist project/editor context and atomically guard execute_command, batch, open/save and run_script. Unmapped helpers are refused before sending; confirmed read tools are checked again afterward. [Evidence](docs/evidence/desktop-native-revision-candidate-20261009.json) separates native mapping, owned desktop control edits and installed public-entry checks from model dispatch and physical GUI input. Old published snapshots remain unchanged; full9.3.2 and V1 remain open.

Desktop atomic-conflict reconciliation candidate: `docs/evidence/desktop-conflict-reconcile-candidate-20261009.json`. Versioned proofs bind the task, operation arguments, original session baseline and stopped owned desktop. Public reconcile/resume can identify an individual operation as not executed while preserving attempted intents and successful receipts. Legacy proofs, non-atomic changes and missing stop evidence remain unknown; unresolved tasks block replacement task IDs. This increment is unpublished; full 9.3.3/9.3.4 and V1 remain open.

Source59 / plugin61 development release includes atomic desktop conflict reconciliation and versioned command completion seals. Recovery verifies original results before registering delivery; missing or changed evidence refuses recovery, and cancellation prevents late delivery. Earlier candidate reports retain their historical scope; see `docs/evidence/release59-validation-20261009.json` for this release. Full fault/recovery, other native platforms, host acceptance and V1 remain open.

Historical unpublished [real worker crash candidate](docs/evidence/command-completion-crash-candidate-20261009.json): commands and owned desktop cover SIGKILL before the proof, between proof and reference, and after both are durable. Only a complete original proof permits delivery registration after owned-process stop, isolated native reopen and actual PNG decode; missing or orphan proofs stay unknown and repeated resume does not replay edits. Malformed ownership returns structured failure without treating corruption as absence. Source59/plugin61 remain unchanged; full 9.3.3/9.3.4, other native platforms and fixed-host gates remain open.

Source60 / plugin62 release distributes the real worker crash increment and strict ownership validation. Candidate reports retain their original unpublished observation context; release binding is recorded in `docs/evidence/release62-plugin-validation-20261009.json`. Full V1 remains open (70 tasks).

Local native family cancellation acceptance (9.36): commands and owned desktop cover normal ancestor cancellation and supervisor SIGKILL after durable intent. Original frozen public entries reconcile the child before the parent; the unrecorded save response stays unknown. Native files/media, successful receipts, deadlines/revision budgets, shared resources and unrelated processes are preserved. Four native cases and 27 cancellation contracts pass; four native cases skip by default. [Evidence](docs/evidence/native-family-cancellation-candidate-20261009.json) preserves fixture corrections and limits: registered undispatched parent, reused cache, Python3.13.5 and macOS arm64 only. Production code and published source60/plugin62 snapshots are unchanged; new tests/evidence remain unpublished candidates. Full9.3.4 and 70 V1 tasks stay open.

Technical gate9.4.1 accepted: [evidence](docs/evidence/technical-gate-acceptance-20261009.json). Asset-bearing MP4, ordinary transparent and segmented sequences complete public plan/run/review/resume from one readonly independent skill, including native save/reopen and actual decoding. Isolated real-delivery mutants with invalid video, missing assets or invalid project fail; a high-score receipt cannot override technical failure. Six native positive/negative cases pass; targeted regression72 pass/6 conditional skip (78 total). Engineering, media technical, creative and user acceptance remain separate; the latter two are NOT_RUN. Acceptance is macOS arm64 with isolated Python3.13.16 and reused verified caches; other targets, model dispatch and all-command output qualification remain open. V1 has69 open tasks. Published source60/plugin62 production snapshots are unchanged; new acceptance is unpublished.


This release: source dev.61 / plugin dev.63 publishes the9.36 native family-cancellation and9.4.1 technical-gate tests and evidence. Earlier unpublished statements describe their observation checkpoints. Skill execution resources remain byte-identical to source60;69 V1 tasks and marketplace qualification remain open.


Local artifact-lineage candidate (EC-AR-001;5.1–5.3 in progress): workflows add the ArtCraft-owned craft-artifact/v1 object to the compatible manifest, binding logical identity, immutable whole-package version, actual task, parent version, native project, renditions and collected media. Review and moved-source revision verify every bound file; same-name replacement, stale versions, reference mismatches and links are rejected. Source-package binding persists in task authorization and is checked before subsequent edits and delivery. Direct CLI execution explicitly uses standalone identity; legacy packages contribute content-verifiable native references without invented task provenance. This is unpublished source work; the plugin remains pinned to released source61. Command/desktop public artifact mapping, font/LUT discovery and complete fixed-release protocol qualification remain open;5.1–5.3 are not checked off. [Evidence / 证据](docs/evidence/workflow-artifact-lineage-candidate-20261009.json).

Current release: source dev.62 / plugin dev.64 distributes workflow artifact lineage and source-package guards. Candidate evidence retains its observation checkpoint; release bindings are in release62-validation-20261009.json. Regression: 697 tests, 633 passed, 64 conditional skips; three macOS arm64 native deliveries bind current execution resources. Command/desktop public mapping, font/LUT discovery, other native targets and host acceptance remain open;5.1–5.3 remain unchecked and V1 has69 open tasks.


Unpublished source-producer guard: copying/moving a managed workflow package or changing state roots still requires original task, operation receipts, durable delivery digest and stopped-process evidence. A private user-level locator is not completion proof; each edit intent and delivery rechecks the persisted source binding. Ten targeted tests and708 regression cases pass (643 passed,65 conditional skips). Native SIGKILL after package completion but before ledger delivery confirms public cross-store plan/run refusal, original reconcile/resume without replay, and confirmed moved-source revision with native reopen/PNG checks. The first native fixture ordering failure is retained. macOS arm64 and reused caches only; full9.3.3, legacy/command/desktop matrices, other platforms and hosts remain open, with69 tasks unfinished. Plugin stays pinned to source62/plugin64. [Evidence / 证据](docs/evidence/source-producer-guard-candidate-20261009.json).

Source dev.63 / plugin dev.65 distributes source-producer guards and public artifacts for commands and owned desktop sessions: separate projects retain actual task identity, immutable package versions, native projects, matching PNGs and media dependencies. Legacy delivery remains readable. Portable mapping does not replace technical, creative or user acceptance. Prior candidates retain their observation-time scope; see [release validation](docs/evidence/release63-validation-20261009.json). Font/LUT discovery, complete fault matrices, other native platforms and fixed-host dispatch remain open;5.1–5.3 remain unchecked and V1 has69 unfinished tasks.


Source dev.64 / plugin dev.66 adds native font and LUT resource observations across saved text styles, character runs, keyframes and supported LUT properties. Only actual LUT bytes receive content hashes; font names never stand in for font files. Font resolution, dynamic values, file-LUT runtime paths and visual fidelity retain separate NOT_RUN states. Legacy delivery identities are not upgraded on read. See [current release evidence](docs/evidence/native-resources-release64-20261009.json). Tasks5.1–5.3 and69 V1 tasks remain open; the change is not archived.


Unpublished file-LUT review candidate: public command/owned-desktop reviews now verify declared packaged LUT inputs in isolated native copies, compare decoded sample frames and preserve originals. Each review render reserves durable task-family resources before execution; unknown resources, missing frames or exhausted budgets keep the engineering gate NOT_RUN, while mismatches fail it. Bound absolute declarations can relink to verified relative package content after relocation without reading the old location. Workflow routing is implemented but its native file-LUT creation/review acceptance remains open. The plugin still consumes released source64/plugin66; published CI and old native reports do not validate this candidate. See [candidate evidence](docs/evidence/file-lut-validation-candidate-20261009.json). Tasks5.1–5.3 and69 V1 tasks remain open.


Source dev.65 / plugin dev.67 distributes isolated file-LUT review, bound package relocation and durable review-render budgets. Historical candidate reports preserve their observation context. Current regression: 679 passed, 72 conditional skips; two macOS arm64 native cases pass. Workflow native file-LUT acceptance, fonts, full temporal/creative, other native platforms and host gates remain open. See [release evidence](docs/evidence/file-lut-release65-20261009.json). Tasks5.1–5.3 and69 V1 tasks remain open.


Source dev.66 / plugin dev.68 correct current release identity documentation. Execution payloads and test files are byte-identical to source65; immutable source65/plugin67 tags are retained. See [release binding](docs/evidence/file-lut-release66-20261009.json).


Source dev.67 / plugin dev.69 correct a Windows absolute-path test fixture without changing execution resources. Source65/66 Windows CI failed that fixture; prior tags are retained. The original content-rejection assertion is preserved and all15 file-LUT tests pass locally. [Release binding](docs/evidence/file-lut-release67-20261009.json).


Unpublished stop-observation candidate: POSIX guardians retry transient member-query failures only within the original five-second stop window, propagate remaining time to the query, and reject empty/malformed member tables as stop evidence. Persistent failures remain unknown; business results and forced-stop outcomes stay distinct. 100 real macOS sandbox cancellations pass after a 1/100 baseline failure was reproduced. Full fault/platform/host gates remain open; the plugin stays pinned to source67/plugin69. [Candidate evidence](docs/evidence/stop-observation-candidate-20261009.json).


Source dev.68 / plugin dev.70 distributes bounded POSIX stop observation and workflow composition configuration gates. Historical candidate evidence keeps its observation-time scope. See [release evidence](docs/evidence/release68-validation-20261009.json). Full domain, other native targets and host qualification remain open; marketplace eligibility remains false.

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

Plugin display name: **EffectCraft Use**. Official upstream icon provenance and licenses are included under `assets/official-icon-source.json` and adjacent LICENSE files.

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
