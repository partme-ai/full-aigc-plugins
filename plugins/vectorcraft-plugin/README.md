# VectorCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.6`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


**Plugin boundary:** The current development candidate includes root `plugin.json`, `mcp.json`, skills and the bundled stdio editor adapter. Plugin dev.65 uses the source-built VectorCraft0.12 editor; three new scenarios and the export bridge have bounded native/browser checks. Historical locked skill and Harness evidence below belongs to its named release and does not qualify this candidate or imply installed-host acceptance.

Fixed plugin37/source33 passed bounded installed brand-export acceptance. A newer source candidate and plugin orchestration modules are under local validation; their fixed-release and host acceptance remain separate. [Architecture](docs/VectorCraft-Brand-Gateway-Export-Architecture.md).

Fixed plugin36/source32 passes13 independent native cold installations,26 real workflow tests and52 injected erroneous-update refusals. All64 installed identities match;51 unchanged skills retain revalidated historical cold evidence. Art bundled upgrades and complete V1 remain open. [Fixed acceptance](docs/VectorCraft-Fixed-Brand-Guard-Architecture.md).

Fixed installed appearance-skill verification now includes same-RGB objects without a brand-token link. Only linked consumers change; native properties, unrelated SVG/PNG/PDF and original deliveries remain preserved. Warm runtime verification; no additional V1 task closes. [Acceptance architecture](docs/VectorCraft-Same-Color-Token-Architecture.md).

Four-domain RT-001 runtime source/integrity acceptance now covers every current scenario; existing pinned skill bytes remain unchanged. Runtime upgrades and fullV1 remain open. [Acceptance architecture](docs/Craft-Fixed-Runtime-Integrity-Architecture.md).

Create Logo, icon and brand assets as `.vectorcraft` with applicable SVG, PDF and PNG exports.

Current plugin: `0.1.0-dev.20261017.6`; skill source: `0.1.0-dev.47`; 25 discoverable skills including the frozen base and development scenarios. Historical qualification remains bound to its original payload; full V1 acceptance remains open.

Plugin55/source41 adds actual SVG image scope and a digest-bound technical disclosure guard. Minimum tasks4.13/4.14 pass; 4.15 qualifies for its current headless scenarios. [Architecture](docs/VectorCraft-Exchange-Scope.en.md).

Development plugin53 pins source39: SVG records the actual text export mode and explicit editing loss for outlined text while retaining native text and font dependencies. All three public text editing routes require explicit object IDs. Source regression:151 passed,30 skipped; native candidate checks are recorded separately. Fixed52 acceptance and full V1 remain open. [Text delivery architecture](docs/VectorCraft-Text-Outline.en.md).

All four current VC-DM-002 scenarios passed against public installed51/source38; task4.6 is complete.14 native workflow cases,8 managed authorization cases,2 native SDK selection/subtree refusals and17 source tests passed;13 skills remain unchanged and9 Harness registered groups stopped. Known/unknown faults were explicitly injected after actual native success; this is not an engine defect report. GUI,all Pathfinder contexts and creative topology judgments remain separate. [固定验收 / Fixed acceptance](docs/evidence/vectorcraft-boolean-fixed51-20261009.json).

All two VC-DM-001 scenarios passed against public installed51/source38; task4.3 is complete. Six native save/reopen cases and18 exports cover Pixels/Points, document/artboard-local coordinates, controls, open/closed paths and visible strokes. Four rejected contracts retain original artifacts and actual object IDs. Seven geometry tests pass,13 skill digests remain unchanged and6 registered groups stopped. Arbitrary transforms,GUI and creative acceptance remain separate. [固定验收 / Fixed acceptance](docs/evidence/vectorcraft-geometry-fixed51-20261009.json).

Candidate51 makes an explicit budgetId a shared workflow cancellation boundary. Cancellation fences all active members and future tasks/steps durably, including stale readers; each native group stops and each original artifact is inspected independently before epoch settlement. Expired resumes cancel the workflow; spent attempt/reserved-output quotas refuse admission. Public installed51 passed five actual native cases,115 Node and43 Python regressions; task3.9 is complete. [Architecture](docs/VectorCraft-Shared-Cancellation.md).

Public installed plugin50/source38 passes all seven current VC-TX-002 scenarios:13 actual native crash/recovery cases,109 Node and43 Python tests; all13 skill digests unchanged and30 registered groups stopped. Durable GO authorization and recovery sealing are mutually exclusive; original files and completed receipts are checked without replay. Task3.6 is complete;96 tasks completed and31 remain open. Full cancellation/budget, GUI, model and V1 acceptance remain separate. [Fixed scenario evidence](docs/evidence/vectorcraft-task-recovery-fixed50-20261009.json).

Plugin49 binds completed step receipts to runtime identity, manifest and every declared file. Changed receipts after inspection refuse settlement; old checks without step digests require a fresh inspection. Source38 persists actual delivery directory identity before rename, covering nested linked-asset packages. Four real plain/linked crashes before/after receipt pass as candidates; public fixed49 and actual host-loaded source38 pass the four cases,97 Node and43 Python tests with all13 skill digests unchanged; that release evidence does not alone close3.6. [Fixed evidence](docs/evidence/vectorcraft-receipt-recovery-fixed49-20261009.json).

Plugin48 adds source-dependency snapshot identity checks before recovery. A coordinator SIGKILL after real native save and nine exports, before ledger receipt, passes readonly original-output recovery without replay. 84 Node and43 Python regressions pass; public fixed48/source37 installation and these native cases pass with all13 skill digests unchanged; that release evidence does not alone close task3.6. [Fixed evidence](docs/evidence/vectorcraft-source-recovery-fixed48-20261008.json).

Additional nonempty-link cases pass against installed fixed48: a real linked PNG missing, modified or changed after inspection refuses recovery/settlement while preserving original-stage identity and source occupation.15 recovery regressions pass. Current external QA scripts call the installed fixed48 implementation; that release evidence does not alone close3.6. [Evidence](docs/evidence/vectorcraft-linked-recovery-fixed48-20261009.json).

Plugin47 additionally revalidates captured physical roots and request paths after probing, at launch and during supervision. Replacing a resolved root or output parent with a redirecting link is refused before task registration. Public installed plugin47 and its actual host-loaded source37 passed all seven current VC-TX-001 scenarios,77 Node and43 Python tests and10 native contract cases. Task3.3 closed at that release;32 tasks remained then. [Fixed evidence](docs/evidence/vectorcraft-single-writer-fixed47-20261008.json).

Source manifests, inherited plans and dependencies are now version-bound and copied into verified readonly execution snapshots. Both source projects and physical outputs are reserved before editing; old SQL connections follow the output guard. Native branch, GUI-change conflict and crash/handoff candidate cases pass. [Source and writer contract](docs/VectorCraft-Source-Single-Writer.md). Public installed plugin46/source37 passed the recorded native scenarios on macOS arm64, but the root replacement authorization boundary is still open. [Subset evidence](docs/evidence/vectorcraft-single-writer-fixed46-20261008.json). Task3.3 was not closed at that version; current acceptance is recorded at fixed47.

Published plugin45/source37 passed isolated Codex installation,63 Node and43 Python tests, and real cancellation and coordinator-crash recovery from the installed copy. All13 skill digests remain unchanged. [Fixed-install evidence](docs/evidence/vectorcraft-recovery-fixed45-20261008.json). These are bounded recovery cases; no additional V1 task closes.

Recovery now verifies retained skill, plan and control identities before launching native inspection; old unresolved tasks without an original control digest remain occupied. Real cancellation and coordinator-crash cases pass without replay. [Recovery contract](docs/VectorCraft-Recovery-Snapshot.md). Tasks3.3/3.6/3.9 have fixed scenario acceptance; complete V1 remains open.

Authorization now freezes caller scope, input fingerprints and physical paths before asynchronous probing, and requires write permission for the staging parent. Three coordinator regression cases cover these boundaries; complete task3.3 and V1 acceptance remain open.

Public plugin44/source37 also passed isolated Codex installation and discovery of13 skills, with57 Node and43 Python regressions run from the installed copy; all skill digests remain unchanged. [Fixed-install evidence](docs/evidence/vectorcraft-authorization-fixed44-20261008.json). No additional V1 task closes.

Runtime capability and isolated upgrades (task2.6) passed all current scenarios in public installed plugin43/source37: cold default, real version/bridge drain, two-process races, migration snapshots and legacy-reader budget rollback. [Fixed-install evidence](docs/evidence/vectorcraft-runtime-upgrade-fixed43-20261008.json). Scope is declared macOS arm64;32 other tasks remained open at that release.

Verified first-use platform: macOS arm64 and Python 3.11+. Pinned runtimes install into the user data directory; skill files stay in their host-loaded directory. These are development releases; complete V1 acceptance and generic Skills CLI installation remain open.

Maintainer source validation rejects symbolic links, incomplete locks and version-named branches, and checks all declared sources before replacing any managed skill. Published skill/runtime identities remain unchanged. [Snapshot preflight architecture](docs/Skill-Snapshot-Self-Contained.md).

## First use

Invoke **`vectorcraft-use`** in your host. For direct CLI use, set `SKILL_DIR` to the absolute directory of the `SKILL.md` actually loaded by that host. It may be under user/project `.agents/skills`, the plugin, or a host cache; use the actual path. Each entry below installs/verifies its locked runtime before invoking it.

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- --version
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- commands
```
<!-- CRAFT_FIRST_USE_END -->

Read the [editable workflow](skills/vectorcraft-use/references/workflow.md) for inputs, native projects and targeted revisions. [Setup and skill entry](skills/vectorcraft-use/SKILL.md) · [version-bound history](RELEASE-HISTORY.md). Command/version queries verify installation and discovery; they do not constitute creative completion.

[First-use navigation evidence](docs/evidence/craft-readme-first-use-navigation-20261007.json).

Fixed installed path acceptance: standalone skills and Art mixed work pass native creation/reopen, targeted revision and export under Chinese-and-space paths; Art also verifies moved delivery. Skills/runtime identities stay unchanged. This is bounded macOS arm64 first-use evidence. [Path acceptance evidence](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

Historical source candidate before the fixed release: structurally invalid runtime/Node locks now return local setup diagnostics before runtime writes/downloads. Five candidate native first-use checks pass; published plugin snapshots remain unchanged until separate immutable release acceptance. [Lock diagnostics candidate](docs/VectorCraft-Lock-Shape-Architecture.md).

---

Fixed native first-use and complete-command recovery acceptance passed:58 standalone cold installations, ten Art all-domain cold installations, four partial-download SSL EOF recoveries,72 post-save faults, four healthy command revisions and mixed HD revision/recovery/moved delivery. Installed identities remain unchanged. Only domain2.10/8.11 and Art4.10 close; exhaustive2639-command, GUI, model, generic Skills CLI and fullV1 gates remain open. [Version-bound evidence](docs/evidence/codex-native-download-first-use-20261007.json).

Historical release record: Current plugin: `0.1.0-dev.21`; skill source: `0.1.0-dev.19`; gradient/appearance recipes included; 12 fixed installed cold appearance cases pass; Art distribution update pending; full V1 remains open.

Historical candidate observation before fixed acceptance: Native download recovery candidate: up to three read-only attempts discard partial archives. Earlier fixed cold installs failed on SSL EOF; new fixed installed acceptance remains open.

Previous version-bound plugin: `0.1.0-dev.18`; skill source: `0.1.0-dev.16`; complete-command inner JSON fix is published, fixed installed acceptance pending.

Previous version-bound failed-stage acceptance: plugin dev.17, standalone source dev.15. All58 independent CLI cold starts,24 original-stage native fault cases and37 native scene tests plus6 contracts pass. Art77 bundle upgrade remains open. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

Fixed domain-client first use: Film plugin dev.16 / source dev.15; Effect/Photo/Vector plugin dev.15 / source dev.14. Codex discovers 58 skills without errors. Actual installed copies pass 24 post-save faults and four healthy public workflows; the published Art engine with the installed Vector client passes six faults. All58 installed identities remain unchanged. Art dev.75 still bundles earlier domain sources; exhaustive command/GUI/model acceptance remains open. [Version-bound evidence](docs/evidence/codex-public-workflow-session-first-use-20261007.json).
Previous version-bound protocol recovery acceptance passed: 288 cases across 48 standalone source skills, 24 cases in actual installed copies, four healthy revision cases, and 58 unchanged installed skill identities. See [fixed evidence](docs/evidence/codex-protocol-fault-first-use-20261007.json). Exhaustive command/GUI acceptance and the Art domain-bundle upgrade remain open.

Protocol fault repair candidate: all 12 independently copied skills pass separate empty public-runtime installation and six faulty replies after real native save (72 cases; zero skips). Requests are not replayed; unknown receipts, saved-project reopening and delivery/skill preservation are checked. [Evidence](docs/evidence/protocol-fault-first-use-20261007.json). Fixed installed release and Art bundle upgrade remain separate gates.

Fixed plugin 0.1.0-dev.13 / skills 0.1.0-dev.12 installed revision acceptance passes: isolated Codex discovers all 58 skills without loading errors; this installed domain skill completes the documented cold creation/revision plans, saved-project reopening and non-target preservation. All58 installed digests remain unchanged; current fixed release CI passes. [Fixed revision evidence](docs/evidence/codex-complete-command-revision-first-use-20261007.json). Full command/GUI/model acceptance remains open.

All 12 domain skills pass the paired revision plans when copied alone and installed from separate empty public runtimes (79.101 seconds; zero skips). [Revision evidence](docs/evidence/complete-command-revision-first-use-20261007.json). Fixed installation of the updated snapshot remains a separate gate.

The complete-command entry now includes paired executable creation/revision recipes, explicit selection prerequisites after reopening, and native persisted-state/non-target checks. Each standalone skill includes both JSON plans. [Usage](skills/vectorcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision). Full per-command and GUI acceptance remains open.

Previous version-bound release first use passed: isolated Codex 0.153.4 discovers all 58 skills without loading errors; every installed skill independently cold-installs its public locked runtime (385.234 seconds); installed domain command samples and Art 1080p mixed revision/recovery/package checks pass. All installed skill digests remain unchanged; fixed CI and five-bundle rebuild pass. [Version-bound evidence](docs/evidence/codex-complete-command-first-use-20261007.json). Generic Skills CLI installation, full command/GUI and creative acceptance remain open.

## Complete native command entry

All 12 standalone skills now pass separate empty-runtime installation from locked public CLI archives, followed by native creation, save/reopen, domain assertions and rendered image checks (74.946 seconds; zero skips). [Cold-first-use evidence](docs/evidence/complete-commands-cold-first-use-20261007.json). This verifies this complete-command sample in every skill; exhaustive command/GUI and actual host installation remain separate.

Published development snapshot: skills dev.11 / plugin dev.12; bounded fixed-host first use passed.

All 585 commands now have verbatim parameters, skill routing, and same-session invocation through `commands.py list / describe / check / run`. Live enabled state is checked; the existing 27-operation delivery workflow remains bounded. GUI commands require explicit bridge mode. Complete registry coverage does not establish full command acceptance.

[Architecture and usage](docs/VectorCraft-Complete-Commands-Architecture.md) · [Complete reference](skills/vectorcraft-use/references/command-reference.md) · [Runnable example](skills/vectorcraft-use/examples/commands-advanced.json)

Independent-skills-driven Editable vector brand assets and multi-artboard design.

[English](README.md) | [简体中文](README.zh-CN.md)

## Current release and reproducible host checks

Previously verified plugin/skill suite: `0.1.0-dev.3`. Codex 0.147.0 and 0.153.4 installed five fixed public releases and discovered all 58 enabled namespaced skills with zero loading errors and matching source digests. Five representative workflows passed through installed task-skill entrypoints on 0.147.0, including native projects, targeted revisions and the mixed ArtCraft online workflow. Model dispatch, desktop GUI, final creative review and full interchange fidelity remain unverified.

[Host verification design](docs/VectorCraft-Host-Verification-Architecture.md) · [Version-bound evidence](docs/evidence/codex-skill-suite.json). Historical milestones below retain their original scope; the current manifest and locks own version identity.

> Development release. Fixed-tag Codex installation, skill discovery and representative native workflows have passed; complete product and creative acceptance remain open.

Implementation has started in the independent skills package. The isolated first-use installer is tested on macOS arm64; complete creative workflows and plugin host acceptance remain pending. [Evidence](docs/evidence/bootstrap-tests.json)

The independent skill now includes a native workflow helper: shapes and paths, Boolean union, editable text, two artboards, SVG/PNG/PDF exports and targeted recoloring were exercised. It preserves unbound objects and exports in the fixture. This does not prove full plugin acceptance. [Workflow evidence](docs/evidence/vector-workflow-tests.json)

## Positioning

Create logo and icon assets in .vectorcraft, SVG and PNG; change a brand color and update bound variants while preserving unrelated colors.

For creators who need editable native projects, repeatable revisions and reliable automation.

## At a glance

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
| Execution | Upstream CLI; ArtCraft uses child adapters |
| Host compatibility | Public64/source46 Codex installation and13 cold starts verified;model routing/full-host acceptance open |
| License | Apache-2.0 (original repository content) |


## Capabilities and boundaries

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Paths, shapes and coordinates | Define artboard coordinates, units, control points, path closure and strokes; preview pixels are not vector path authority. | Full scope pending |
| Grouping and boolean operations | Record operand IDs, boolean operation and result identity with a pre-operation checkpoint; failure must not destroy source objects. | Full scope pending |
| Brand colors and text | Bind brand colors using explicit tokens instead of global color replacement; retain text and font dependencies and report editability loss when outlining. | Full scope pending |
| Artboards and variants | Give each artboard a stable ID, name, size and output mapping; define preview ordering and export ranges without index-base ambiguity. | Full scope pending |
| Interchange fidelity scope | Validate native .vectorcraft, SVG, PDF and PNG separately; report rasterized effects and keep native sources when interchange cannot preserve them. | Full scope pending |
| Brand variant revision | Update related variants from token and asset dependencies and verify that unrelated object properties and outputs remain unchanged. | Full scope pending |

Does not rewrite upstream editors, silently change native deliverable formats, or claim GUI/cross-platform acceptance.

## Architecture and documentation

- [Complete runtime architecture](docs/VectorCraft-Runtime-Architecture.md)
- [Technical plan and roadmap](product-docs/VectorCraft/en/5%E3%80%81VectorCraft-Technical-Plan.md)
- [V1 PRD and requirement mapping](product-docs/VectorCraft/en/V1/5%E3%80%81VectorCraft-PRD-V1.md)
- [Complete documentation index](docs/README.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [Domain technical design](docs/VectorCraft-Domain-Design.md)

## Currently executable quick start

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
These commands validate documentation and specifications, not product workflows. OpenSpec validation uses 1.13.1; this repository does not install tools automatically.

After installing the official CLI, perform a basic check:

```bash
vectorcraft-cli --version
```

The recorded result is 0.2.0. The public independent-skill bootstrap and workflow are development entry points; plugin-host installation remains unverified.

## Configuration and runtime

Target configuration includes CLI paths, allowed read/write roots, execution mode, budget, timeout and output directory; the configuration schema is not implemented yet. The skills lock pins the published source commit and whole-skill digest. Runtime lock hashes identify real official artifacts and establish only the recorded platform’s smoke evidence.

## Reliability and security

Planned safeguards include project write locks, revision preconditions, persisted intent, idempotency keys, outcome reconciliation, native checkpoints, artifact hashes and bounded revisions. Secrets are host-managed references; asset metadata is never an execution instruction.

## Verification and maturity

[Sanitized CLI evidence](docs/evidence/runtime-baseline.json)

| Layer | Status |
| :--- | :--- |
| Upstream CLI and read-only MCP | Observed on macOS arm64 only |
| Independent skill and adapter | Technical workflow tested; full harness pending |
| Native project and creative acceptance | Native technical cases pass; creative acceptance pending |
| Target host installation | Codex controlled install/discovery pass; full host acceptance pending |


## Roadmap and contribution

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |

Change OpenSpec before behavior; check a task only after actual acceptance. Maintain both document languages. See CONTRIBUTING.md and AGENTS.md.

## License and upstream

Original content uses [Apache-2.0](LICENSE). This is a third-party integration design, not upstream endorsement. Treat the four apps’ code licenses separately from ArtCraft/Services restrictions; do not copy restricted source or brand assets.

[Upstream VectorCraft](https://github.com/storytold/vectorcraft) · [Issues](https://github.com/full-aigc-plugins/vectorcraft-plugin/issues)

Independent skills are pinned at the current published development tag `v0.1.0-dev.4`, including the exact source commit and whole-skill digest in `skills.lock.json`. Verify using `python3 scripts/vendor/skill_vendor.py check`. These source snapshots do not establish plugin-host acceptance or production readiness.

## Development skill installation and use

Install the independent skill: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-use`. Run the public entry from the actual installed directory; this plugin snapshot includes the same skill.

```bash
python3 -I -B skills/vectorcraft-use/scripts/bootstrap.py
python3 -I -B skills/vectorcraft-use/scripts/workflow.py --help
```

First use installs the pinned official CLI into user-level storage. Requires macOS arm64 and Python 3.11+. Use the bundled example with real input assets; consult SKILL.md for delivery and revision contracts. [Source verification](docs/evidence/skill-publication.json).

## Codex development host checks

All five plugins installed from public tags into an isolated Codex configuration. App-server discovered their namespaced skills without loading errors; the installed ArtCraft entry produced four native projects. [Host evidence](docs/evidence/codex-installation.json). These controlled development checks do not establish desktop GUI, other hosts, complete creative or production marketplace acceptance.

Development version `0.1.0-dev.1` pins the independent skill install-lock fix: bounded coordination for concurrent installation/reuse, with no native task replay.

The current development milestone adds hash-bound exchange loss reports to native deliveries. lost, observed and unknown are separate; derivatives never substitute for native projects. Font/effect/mask fidelity across editors remains unverified, so full exchange acceptance stays open.

## CLI and task skill suite

The source suite contains 12 independently installable skills with setup, public CLI operations and focused tasks. [Architecture and catalogue](docs/VectorCraft-Skill-Suite-Architecture.md). Runtime and plugin versions are separate; prior host evidence retains its original version scope.

Previous version-bound plugin: `0.1.0-dev.5`; skill suite: `0.1.0-dev.4`. The corrected examples resolve scripts from the actual host-loaded `SKILL.md` directory. All skills passed isolated entry-point checks in user, project and plugin layouts with spaces. [Path evidence](docs/evidence/installed-skill-paths.json). Earlier host evidence above covers its recorded release; existing installations require an update.

Plugin `0.1.0-dev.5` corrects the whole-skill digests by fetching the immutable public source tag, without local Python caches. Plugin tag `v0.1.0-dev.4` is superseded and must not be installed because its source digests included ignored development caches.

Current plugin `0.1.0-dev.6` pins skill suite `0.1.0-dev.5`. Nine task skills each cold-installed and performed real native edits; selection, image embedding, symbol reuse and unaffected boards are verified. Full regression: 38 passed, no skips. [Evidence](docs/evidence/task-skill-first-use.json). Full creative/GUI/model acceptance remains pending.

Current fixed-release host verification (2026-10-06): Codex 0.153.4 installs all five current pinned plugins and discovers all 58 skills with exact content identity. This plugin’s representative native workflow runs from its actual installed skill path with a fresh native runtime; creation/reopening/revision checks pass. All 58 installed skill hashes remain unchanged after the five workflows. [Evidence](docs/evidence/codex-current-release-20261006.json). The shared explicit-tag generator belongs to ArtCraft. Model dispatch awaits authorization; GUI, creative and full host acceptance remain pending. This QA maintenance changes no published skill/runtime content or release tags.

The fixed FilmCraft dev.6 / EffectCraft dev.7 / PhotoCraft dev.6 / VectorCraft dev.6 / ArtCraft dev.17 matrix passed isolated Codex discovery of 58 skills and representative native workflows from installed skill content. All installed skill digests remained unchanged afterward. [Installed native evidence](docs/evidence/codex-release17-native-20261006.json). Model dispatch, GUI and complete creative acceptance remain unverified.

Additional installed-skill brand export verification passed: changing selected logo/wordmark objects updates both SVG color and decoded PNG pixels; unrelated icon properties and the second artboard PNG stay unchanged. This used existing verified runtime caches, not a new cold install. It does not prove automatic token dependency inference. [Evidence](docs/evidence/brand-export-color.json). Plugin and skill release tags are unchanged.

The native RGB global brand-swatch workflow passed a first-use public cold install from one copied appearance skill, including its own script and example. Linked SVG/PNG variants update while the unrelated icon and original project stay unchanged. Skill source v0.1.0-dev.6 is published; plugin v0.1.0-dev.7 is published. Actual host-installed single-skill public cold native acceptance also passes (6.487 seconds); all 58 installed skill hashes remain unchanged. Actual npx independent installation and model dispatch remain unverified. See [architecture](docs/VectorCraft-Brand-Tokens-Architecture.md) and [evidence](docs/evidence/native-brand-token-first-use.json).

Native Chinese text revision now has a single-skill cold test: explicit object edit keeps the first style, unrelated footer and original project; missing fonts stop delivery and successful font dependencies are recorded. Skill source dev.7 and plugin dev.8 are published. Actual installed single-skill public cold native testing passes in 8.275 seconds; all 58 installed hashes remain unchanged. [Architecture](docs/VectorCraft-Chinese-Text-Architecture.md), [evidence](docs/evidence/native-chinese-text.json).

Earlier skill source dev.7 full native regression passes all 42 tests with zero skips (111.204 seconds), including nine separately copied task scenes, brand swatches and Chinese text. Native task scenes use fresh public caches; CLI discovery and baseline native workflow explicitly reuse verified caches. [Evidence](docs/evidence/dev7-full-native-suite.json).

Installed plugin dev.8 / skill source dev.7 supplementary acceptance now checks four rectangular boolean operations, native compound-hole winding, independently decoded SVG/PNG/PDF, original delivery preservation and invalid selection rejection. This does not expand support to arbitrary geometry or editor round trips. [Acceptance](docs/VectorCraft-Boolean-Geometry-Acceptance.md).

Historical fixed dev.8 first-use gap, resolved by dev.9: an unrelated artboard SVG retains off-board brand paths and changes after a brand-token revision, although its PNG/PDF remain unchanged. A maintained native runtime is published; the repaired immutable skill/plugin snapshot is pending. [Reproduction and design boundary](docs/VectorCraft-Artboard-Export-Gap.md).

A local maintained CLI candidate `0.2.0-craft.1` now passes 954 engine tests, 12 CLI integration tests and the three-artboard isolated archive-install task, including byte-identical unrelated SVG/PNG/PDF after a brand-color edit. Twelve source skill installers support its maintained version identity and provenance. This paragraph records the earlier local candidate stage; the maintained runtime is now published, with fixed skill/plugin acceptance pending. [Candidate evidence](docs/evidence/native-artboard-svg-candidate-20261006.json).

The published maintained native runtime passed working-tree single-skill HTTPS cold first use (4.970 seconds). Immutable skill/plugin release and ArtCraft integration remain pending. [Evidence](docs/evidence/public-artboard-svg-runtime-20261006.json).

Plugin dev.9 vendors immutable skill source dev.8 and maintained native CLI 0.2.0-craft.1. The source native suite passes 46 tests without skips; fixed dev.9 host first use and the ArtCraft bundle update are the remaining integration gates. [Source native regression](docs/evidence/maintained-full-native-suite-20261006.json).

Fixed public plugin dev.9 / skill source dev.8 now passes actual Codex discovery of 58 skills and installed single-export-skill public cold native acceptance (4.985 seconds). All 58 installed skill hashes remain unchanged. OpenSpec 4.22 is verified at this domain scope; the ArtCraft bundle update and complete V1 acceptance remain pending. [Fixed installed evidence](docs/evidence/codex-vectorcraft9-artboard-first-use-20261006.json).

Plugin dev.10 vendors immutable skill source dev.9 and maintained CLI craft.2. Stable PDF creation dates and hash-bound date records pass the 49-test native source suite; fixed new host and ArtCraft mixed acceptance remain pending. [Date architecture](docs/VectorCraft-PDF-Date-Architecture.md), [native tests](docs/evidence/craft2-full-native-suite-20261006.json).

Fixed ArtCraft dev.50 / VectorCraft dev.10 first use passes in isolated Codex 0.153.4: five plugins, 58 skills and zero loading errors; one cold native export test with cross-second revision passes (8.108s), two mixed brand tests pass (51.409s), and all installed skill hashes remain unchanged. [Release-bound evidence](docs/evidence/codex-release50-vector10-stable-export-first-use-20261006.json). Generic Skills CLI installation, model/GUI, complete domain and creative acceptance remain open.

All 22 updated skills pass individual public cold first use (159.811s): each is copied alone to .agents/skills and installs into an independent empty runtime, checks exact version and command contracts, and preserves its files and all host-installed hashes. This does not establish generic Skills CLI installation or every creative scenario.

Registered-asset source candidate: linked PNG, embedded SVG, JPEG/SVG replacement, native dependency collection and relocation are implemented in the independent skill workflow. [Architecture](docs/VectorCraft-Asset-Handoff-Architecture.md). The existing fixed plugin snapshot is unchanged; new release and installed-host acceptance remain pending.

Plugin dev.11 vendors immutable skill source dev.10, adding registered PNG/SVG placement and JPEG/SVG replacement with native dependency collection. Installed-host acceptance for this release and the ArtCraft distribution upgrade are separate steps; full V1 acceptance remains open.

Fixed plugin dev.11 / skill source dev.10 has passed actual Codex 0.153.4 public-tag installation and discovery: 58 skills, zero loading errors. Installed single asset/export skills passed two native cold-start tests without skips (4.855s and 6.743s); 12 VectorCraft skills separately cold-installed in 56.275s. Linked/embedded PNG, SVG, JPEG/SVG replacement, direct relocated native reopening and unrelated artboard preservation were checked. All 58 installed hashes stayed unchanged. [Fixed evidence](docs/evidence/codex-vectorcraft11-assets-first-use-20261006.json). ArtCraft still consumes the older Vector bundle; its distribution upgrade and mixed first use remain open.

Current fixed-release domain task matrix: 37 native scenarios and 6 contract checks passed with zero skips across FilmCraft dev.10, EffectCraft dev.9, PhotoCraft dev.10 and VectorCraft dev.11. Each task copied only its selected installed skill and installed the native CLI into a fresh runtime directory from the default public archive. Native projects, actual pixels/audio and targeted preservation were checked; all 58 installed skill identities remained unchanged. [Version-bound evidence](docs/evidence/codex-current-domain-task-matrix-20261006.json). This does not close full V1, generic Skills CLI installation, model dispatch, GUI or creative acceptance.

Public-workflow reply validation is synchronized in the domain source candidates and has bounded native/Art protocol evidence. Fixed updated domain and Art distributions are still pending. [Candidate architecture](docs/VectorCraft-Complete-Commands-Architecture.md) · [Evidence](docs/evidence/public-workflow-session-candidate-20261007.json).

Failed-stage candidate: public workflows retain original native staging paths, dependency hashes, last submitted requests and completed receipts; replay is prohibited. Fixed releases and installed-host acceptance remain open. [Architecture](docs/VectorCraft-Failed-Stage-Architecture.md).

Fixed domain failed-stage first use passes: Film plugin18/source16 and other domain plugins17/source15; five plugins/58 skills without loading errors; all58 independent empty-runtime CLI starts (417.646s); actual installed24 post-save faults reopen product-retained original projects and dependencies; four healthy native creation/revision cases pass. All installed identities and16 fixed plugin CI runs pass. Source repositories have no CI runs, only local regression. Only domain OpenSpec3.12 closes; Art77 bundles older domain sources, task4.9 and fullV1 remain open. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

Fixed installed scene matrix passes37 native scenarios and6 contract checks with zero skips. The Photo fixture now resolves the maintained native version from the installed skill lock; the CLI and installed skills are unchanged. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


Candidate complete-command inner JSON fix: nonfinite values, overflow and duplicate keys now retain unknown receipts before binding results. All nine real post-save fault classes pass with original reopen; this is candidate-source evidence, fixed releases and installed-copy acceptance are pending. Complete per-command/GUI acceptance stays open.

Gradient and multiple appearance: source-candidate cold native creation/revision passes for 12 standalone skills; fixed installation and Art distribution are pending. [Architecture](docs/VectorCraft-Appearance-Gradient-Architecture.md).

Fixed installed gradient/multiple appearance: 12 skills pass, with control objects and original delivery preserved; updated Art distribution remains open. [Evidence](docs/evidence/codex-vectorcraft-gradient-first-use-20261007.json).

## Desktop installation component (source candidate)

The 48 standalone domain skills now have their own pinned official desktop installers. See the [installation architecture](docs/Craft-Desktop-First-Use-Architecture.md) and [48-skill installation evidence](docs/evidence/craft-desktop-source48-first-use-20261007.json). Existing release-tag skill copies do not yet contain this candidate component. Desktop startup, GUI edits/save/reopen and complete command execution remain open acceptance gates.

Source candidate now includes owned standalone desktop startup: 48/48 single-skill cold GUI save/reopen and cleanup cases passed. See [runtime evidence](docs/evidence/craft-owned-desktop-first-use-20261007.json). Fixed-release installation and complete command execution remain open.

Command-plan JSON source candidate: duplicate keys are rejected before installation and output creation. All 13 domain skills pass standalone-copy rejection and valid-plan checks. Three focused tests pass; fixed-plugin publication and installed acceptance remain NOT_RUN. [Evidence](docs/evidence/command-plan-json-candidate-20261007.json).

Fixed strict-plan installed verification passes: 64 CLI probes, 324 duplicate-key rejections across54 independently copied installed domain skills, 54 unique-plan structure checks and four cold native save/reopen/render samples. All64 installed skill hashes remain unchanged. Only the bounded strict-plan publication gate closes; generic Skills CLI, Art domain-bundle upgrade, exhaustive contexts and fullV1 remain open. [Evidence](docs/evidence/command-plan-json-fixed-first-use-20261007.json).

Scenario installation examples now name the loaded skill itself. Source paths/layout checks pass; fixed installed runtime acceptance is recorded separately. [Architecture / 架构](docs/Scenario-Own-Path-Architecture.md).

Fixed installed own-directory acceptance passes for the updated scenario skills; 64 host identities match. Complete V1 remains open. [Evidence / 证据](docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).

Fixed installation boundary qualification: all 64 current standalone skills pass 128 real unavailable-archive cases through their own bootstrap and CLI entries. Errors retain each skill’s local setup path without retry or native launch; source/copied skill hashes stay unchanged. Four domain SK-002 requirements qualify against the exact lock; Art SK-002 and generic Skills CLI installation remain open. Historical CLI red cases were reconstructed now, rather than treated as old runs. [Evidence](docs/evidence/craft-fixed-setup-boundary-20261008.json).

Public protocol authority is pinned to ArtCraft v0.1.0-dev.109: [reference and verification](docs/Craft-Protocol-Authority.md). This validates the source contract; full runtime protocol acceptance remains open.

Previously verified fixed protocol-reference release matrix (Film/Effect dev.37, Photo dev.36, Vector dev.34, Art dev.107) passes actual isolated Codex installation/discovery of 64 skills, 16 installed authority-file digest checks, and 64 independent public CLI probes using five fresh domain caches. Historical native scene proof is reused only for byte-identical skills; full V1 remains open. [Fixed release evidence](docs/evidence/craft-protocol-authority-fixed-first-use-20261008.json).

This plugin pins protocol authority to ArtCraft dev.109 and retains its locked standalone skill source. Actual installation of the updated matrix is being verified; complete V1 and runtime protocol acceptance remain open.

Fixed releases Film38/Effect38/Photo37/Vector35/Art109 pass actual isolated Codex installation/discovery of 64 skills, 16 installed protocol file digests, and 64 CLI probes using five fresh domain caches. Each of ten Art skills freshly passes its own empty-public-runtime native Photo mask/adjustment creation, source revision and moved package verification. The remaining 54 skills reuse historical native proof only when the entire skill hash matches. Maintainer defaults now select this matrix; generic Skills CLI installation, model dispatch, GUI and complete V1/protocol acceptance remain open. [Fixed evidence](docs/evidence/craft-archive-prefix-fixed-first-use-20261008.json).

Fixed plugin dev.37/source dev.33: all13 actual installed skills independently cold-install the native CLI. Direct and gateway revisions inherit nine SVG/PNG/PDF variants over three artboards; bound colors change, unrelated and source files stay intact, and explicit-empty/tampered-plan cases pass. The other51 skills reuse historical cold records after unchanged identity verification. Art116 still bundles Vector32; full V1 remains incomplete. [Fixed acceptance evidence](docs/evidence/craft-vector37-gateway-export-fixed-first-use-20261008.json).

## Optimization implementation

[Current fixed identity](docs/current-identity.json) and [layered evidence index](docs/evidence-index.json) distinguish published skills from source candidates. The root runtime lock is a historical baseline; each installed skill owns its execution lock. Plugin-local SQLite coordination and single-round review modules are development implementations. Their local tests do not imply complete cancellation, restart, host/model or V1 acceptance. See [implementation guide](docs/VectorCraft-Optimization-Implementation.md).

### dev.38 development prerelease

This release pins source dev.35. Earlier dev.37/source33 installation and candidate execution reports retain their original fingerprints as historical evidence. Local regression and CI do not establish new host installation, model routing, exhaustive command execution or full V1 acceptance. Marketplace eligibility remains false.

### Fixed dev.38/source35 technical acceptance

Codex 0.153.4 installed and discovered all13 skills in fresh isolated configuration. All13 cold native starts and12 declared create/revise pairs passed (setup is installation-only). Two workflow routes passed22 post-save protocol faults; the command entry passed9 faults, and10 ambiguous-plan cases stopped before setup/output. Brand boundary and nine-export preservation checks passed. Tasks9.3/9.6 close; model routing9.9, dependent9.18 and full V1 remain open. [Bound evidence](docs/evidence/vectorcraft-fixed38-optimization-20261008.json). Source36 is an unpublished contract-clarification candidate.

### dev.39 development prerelease

Pins source dev.36 with corrected revision object ID rendering. Adds `review-checked` with persisted actual decoding evidence, shared budgets and restart-safe file bindings. Technical failures block acceptance; unexecuted checks stay pending. Minimal task6.2 implementation is complete; native engineering acceptance6.3, model routing9.9 and full V1 remain open. Fixed dev.38 installation evidence is historical; new host installation acceptance has not been rerun for this version.

### Bounded revision source candidate

Minimal durable rounds, shared budgets, stagnation, native execution lineage and best-candidate retention are implemented; tasks6.4/6.5 are checked. This increment is included in development prerelease dev.40; published dev.39 remains unchanged. Two actual color revisions use injected scores; complete6.6 and real creative acceptance remain open. [Contract and operations](docs/VectorCraft-Revision-Cycle.md).

### dev.40 geometry and revision prerelease

Native geometry contracts check units, artboard offsets, controls, closure and strokes with persisted receipts. Bounded revision cycles retain the best verified candidate. Task4.3 now has fixed51 acceptance;6.6, host and creative acceptance remain open. [Geometry contract](docs/VectorCraft-Geometry-Contract.md).

### Boolean transaction source candidate

Independent source implements retained checkpoints, live participant/result IDs and restoration after known partial failures; linked checkpoints remain portable. At this historical dev.40 checkpoint, tasks4.4/4.5 were checked; complete4.6 and fixed snapshot uptake remained open. Published dev.40/source36 are unchanged. [Architecture](docs/VectorCraft-Boolean-Transactions.md).

### dev.41 structural revision prerelease

Pins source37 boolean checkpoints and explicit Harness `structure` authorization. Actual selection, participant subtrees, result IDs and unaffected model fields are checked. Published source36 and plugin40 stay immutable. At this historical source37 checkpoint, full4.6, host/model/GUI and creative acceptance remained open.

Published dev.41/source37 now passes actual isolated Codex0.153.4 installation:13 skill identities,13 independent public cold starts,12 declared create/revise pairs and8 managed structural cases. Installed bytes remain unchanged. [Fixed evidence](docs/evidence/vectorcraft-fixed41-structural-20261008.json). At this historical dev.41 checkpoint, complete4.6, model dispatch, GUI and creative acceptance remained open.

A new source candidate adds fixed runtime identity, live command/tool schemas, single-ledger draining and rollback compatibility guards.42 Node tests and9 native cases passed; different-version upgrades and desktop acceptance remain open. Published plugin41 is unchanged. See [entry points and boundaries](docs/Runtime-Gate.md).


Default Harness first use now validates plans, installs the fixed runtime and checks live command/tool schemas. Same-version concurrent tasks reuse selection; completed keys inspect original receipts. Source candidate evidence:46 Node tests,5 cold/concurrent/refusal scenarios and8 structural regressions passed. Published plugin41 is unchanged; complete2.6 remains open. See [default runtime gate](docs/Runtime-Gate.md).

Public installed51/source38 passed all five VC-TX-003 scenarios and closes OpenSpec task3.9: five actual native cases,115 Node and43 Python tests,13 unchanged skills and13 stopped registered groups. See [fixed cancellation and budget acceptance](docs/evidence/vectorcraft-budget-cancel-fixed51-20261009.json). Full V1, GUI, model, other platforms and marketplace qualification remain open.

Development53 archives original historical test bytes, resolving52 CI evidence dependency drift. Public installed52 passed actual host discovery of13 skills, two native text exports and18 route refusals; [limited qualification](docs/evidence/vectorcraft-text-smoke-fixed52-20261009.json). Tasks4.7–4.9 are qualified against fixed53; full V1 remains open.

Public fixed53/source39 qualifies all four VC-DM-003 scenarios; tasks4.7–4.9 complete,102 tasks complete/25 open. Eight injected brand faults, healthy/same-RGB isolation, Chinese revision and independent reopen, original-stage text refusals, two SVG text modes,18 route refusals and30 source tests passed;13 skill digests unchanged. Faults are explicit QA injection, native font-library status does not establish OS-font inventory, GUI or cross-editor fidelity. [Scenario evidence](docs/evidence/vectorcraft-brand-text-fixed53-20261009.json).

The test/minimum implementation gates4.10/4.11 are complete,105 tasks complete/22 open; full4.12 evidence is linked below. [Mapping candidate evidence](docs/evidence/vectorcraft-artboard-mapping-candidate54-20261009.json).

Public fixed54/source40 passes actual Codex0.153.4 isolated installation/discovery of13 skills, three successful installed-copy mappings/four refusals and14 decoded outputs;13 skill digests unchanged. Pinned runtime reused. This mapping subset does not close full4.12. [Fixed subset evidence](docs/evidence/vectorcraft-artboard-mapping-fixed54-20261009.json).

All four current VC-DM-004 scenarios qualify at fixed54/source40 on macOS arm64; task4.12 complete,105 tasks complete/22 open.31 native boundary cases, standalone export cold first use, same-source cross-second PDF identity and unrelated SVG/PNG/PDF identity after a brand edit passed;13 installed skill digests unchanged. Unknown paint bounds exercised using an empty native sublayer with pinned source evidence for None semantics; cross-artboard groups recorded as whole dependencies. Source regressions160 passed/30 skipped out of190; GUI,model,other platforms and full V1 remain open. [Full scenario evidence](docs/evidence/vectorcraft-artboards-fixed54-20261009.json).

Historical subset (qualification follows): Plugin55/source41 adds SVG image scope disclosure and technical guards. Three native vector/live-filter/expanded-raster reopening cases,nine decoded outputs and four disclosure refusals pass;4.13/4.14 complete,107 tasks complete/20 open;4.15 fixed installation remains open. [Exchange scope](docs/VectorCraft-Exchange-Scope.en.md).

Historical subset (qualification follows): Public fixed55/source41 passes isolated Codex0.153.4 installation/discovery of13 skills,three installed-copy native reopen cases,nine SVG/PDF/PNG decodes and four disclosure refusals;13 digests unchanged,pinned runtime reused. Only4.13/4.14 close,107 complete/20 open.4.15 still needs automatic fallback or explicit refusal for nonexchangeable live effects and preservation of the original live-effect project. The explicit effect.expandAppearance case does not establish that behavior. [Fixed subset evidence](docs/evidence/vectorcraft-exchange-fixed55-20261009.json).

Historical subset (qualification follows): Supplemental installed55 acceptance verifies automatic freeform SVG raster fallback without expansion (32×22 embedded PNG; local box12,16,60,40), three independent export decodes and seven refusals. Native gradient editing after independent reopen preserves the source and prior exports. Formal task4.15 closure review remains pending; GUI, model and full V1 acceptance are separate. [Evidence](docs/evidence/vectorcraft-exchange-automatic55-20261009.json).

Both current VC-DM-005-P and VC-DM-005-N scenarios qualify on fixed55/source41 macOS arm64. Task4.15 closes:108 complete/19 open. Automatic freeform SVG fallback produces a32×22 embedded PNG with disclosed local box12,16,60,40 and a blocked lossless claim. Independently reopened native gradients remain editable in a new revision while preserving the source and prior delivery. SVG/PDF/PNG decode separately and seven disclosure/format refusals pass. Six evidence tests include five rehashed omission/tampering refusals. GUI, models, other platforms, universal round-trip fidelity and full V1 remain unverified. [Evidence](docs/evidence/vectorcraft-exchange-qualified55-20261009.json).

Plugin56 pins independent source42. Registered raster/SVG consumers follow real native identities; native SVG replacement scaling is corrected to preserve instance bounds. Ten targeted units, source172-pass/30-skip regression, nine native asset exports and three byte-identical unrelated outputs pass; two swatch routes and eight mutation refusals regress successfully. At the candidate stage tasks4.16/4.17 closed; fixed qualification follows below. [Evidence](docs/evidence/vectorcraft-brand-variants-candidate56-20261009.json).

Actual public56/source42 isolated Codex0.153.4 installation qualifies all six current VC-DM-006 scenarios with13 unchanged skill digests. Two swatch routes,eight erroneous-update refusals,two raster and two SVG consumers,nine asset export decodes,three unchanged unrelated SVG/PDF/PNG outputs,unknown-token refusal and both linked-plan refusals pass. Failed checkpoints reopen independently without replay. Task4.18 closes:111 complete/16 open. GUI,model creative quality,other platforms,all formats,cross-file/external-editor behavior,Art bundled distribution and full V1 remain unverified. [Evidence](docs/evidence/vectorcraft-brand-variants-fixed56-20261009.json).


Plugin57/source43 adds digest-bound portable artifact lineage and public semantic integrity checks. Native creation, movement/reopen, revision and five integrity refusals pass as candidates; source177 passed/30 skipped, plugin73 Python tests passed. Tasks5.1/5.2 complete (113/127); fixed-install5.3 remains open. [Evidence](docs/evidence/vectorcraft-lineage-candidate57-20261009.json).


Plugin58 corrects public checker imports to preserve immutable installed skill bytes. The actual57 CI cache-write failure is retained; its read-only regression failed on57 and passes on58. All74 Python tests pass locally; fixed58 qualification remains pending. [Evidence](docs/evidence/vectorcraft-lineage-candidate58-20261009.json).


Actual public58/source43 installed on Codex0.153.4 macOS arm64 passes all three current VC-AR-001 scenarios: native creation, whole-package movement/reopen, parent-bound revision and public seven-case validation. All13 installed skill digests remain unchanged. Task5.3 closes;114/127 complete,13 open. Creative quality and other platforms remain separate. [Evidence](docs/evidence/vectorcraft-lineage-fixed58-20261009.json).


Plugin59/source43 adds uniform exchange-report checks for SVG/PDF/PNG, native and reopened-inspection identity, derivative-only roles, conservative font/effect fidelity and SVG live-text loss matching native settings. The installed58 PDF substitute gap is reproduced; candidate three decodes,20 refusals and85 Python tests pass. Fixed task5.6 remains open. [Evidence](docs/evidence/vectorcraft-exchange-delivery-candidate59-20261009.json).


Actual public59/source43 on Codex0.153.4 macOS arm64 passes all three current VC-AR-002 scenarios: independent native reopening, retained live-text/freeform editing, three decoded exports and20 refusals. All13 skill digests remain unchanged. Task5.6 closes;115/127 complete,12 open. GUI,creative,external editor fidelity and other platforms remain separate. [Evidence](docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json).

Plugin60/source43 binds the decoder, process launcher and local exchange-loss dependency to a readonly execution snapshot. Dependency drift invalidates checked reviews before first handoff and after restart; older checked evidence requires a fresh check. Three targeted tests,118 Node tests and92 Python tests pass locally. Task6.3 remains open;115/127 complete,12 open. [Local evidence](docs/evidence/vectorcraft-quality-checker-candidate60-20261009.json).

Plugin61 fixes receipt CLI restart across declared read roots, restoring the persisted checked authorization while rejecting roots supplied by the receipt. The previous fixed60 failure is reproduced by a public CLI red test;119 Node tests and19 native boundary cases pass as candidates. Task6.3 fixed61 qualification remains open. [Candidate evidence](docs/evidence/vectorcraft-quality-roots-candidate61-20261009.json).

Actual public61/source43 installed on Codex0.153.4 macOS arm64 qualifies all three current VC-QA-001 scenarios and19 native boundaries. Three real decodes pass; maximal-score QA receipts cannot override corrupt PNG/PDF/SVG; real missing decoders stay NOT_RUN. File/checker drift, shared budget before snapshots, timeout stop and coordinator SIGKILL/restart without replay pass.13 skill digests remain unchanged.12 evidence tests reject11 rehashed omissions/tamper cases. Task6.3 closes;116/127 complete,11 open. Actual creative judgment,GUI,other platforms,6.6 and full V1 remain separate. [Evidence](docs/evidence/vectorcraft-quality-fixed61-20261009.json).

Plugin62 fixes exhausted-budget observation: stop durably and preserve the best verified candidate; when another copy cannot be funded, reuse the already-paid readonly technical snapshot after identity and permission checks. Public61 native failure is reproduced, candidate62 keeps the higher scored native revision at exactly four shared attempts;122 Node tests pass, including three new regressions. QA scores are explicit fixtures. Task6.6 full qualification remains open;116/127 complete,11 open. [Evidence](docs/evidence/vectorcraft-revision-budget-candidate62-20261009.json).

Public62/source43 actual isolated Codex installation repeats the native budget boundary: four shared attempts retain the higher-score readonly native candidate, with source/control text preserved and13 unchanged skill digests. This closes no additional tasks;6.6 complete four-scenario qualification remains open. [Evidence](docs/evidence/vectorcraft-revision-budget-fixed62-20261009.json).

Public62/source43 adds three native revision cases: small improvement stops for stagnation while retaining the higher score, lower score keeps the prior best, and the round limit stops execution. An owned signed desktop bridge edits and saves the source; the stale proposal is rejected before revision effects, with two shared attempts, no new revision output and the best copy preserved. Ten evidence tests pass; all13 skill digests remain unchanged. Scores are QA fixtures; full four-scenario task6.6 remains open,116/127 complete and11 open. [Evidence](docs/evidence/vectorcraft-revision-limits-fixed62-20261009.json).

Plugin63 fixes changed-goal stopping: validate the original authority and checked review first, then persist the latest feedback while retaining the original-goal best. Re-observation is idempotent. Public62 native execution reproduces the stale-feedback gap; three regressions fail before the fix and14 targeted tests pass after it. The candidate also passes15 native authority, freshness and lineage boundaries. Fixed63 and complete6.6 qualification remain pending; no new task closes. [Evidence](docs/evidence/vectorcraft-revision-goal-candidate63-20261009.json).

Actual public63/source43 installed on Codex0.153.4 macOS arm64 passes all four current VC-QA-002 scenarios:6 native revisions,15 guards for authority/freshness/explicit feedback/lineage/preservation, and one owned signed desktop source mutation. Budget, stagnation, round-limit and changed-goal stops persist while retaining the appropriate verified best and reporting latest issues. The changed-goal authority/origin gap is fixed. All15 evidence tests pass, including14 rehashed tamper refusals;13 skill digests remain unchanged. Task6.6 completes;117/127 complete,10 open. QA scores test control mechanics;actual creative judgment,other platforms,all commands and full V1 remain separate. [Evidence](docs/evidence/vectorcraft-revision-fixed63-20261009.json).

Both VC-RL-001 scenarios pass. A readonly release-owner gate checks plugin structure,independent skill source,runtime,host load,real task and native delivery separately. Twelve target tests first fail for the missing behavior and then pass;four semantic evidence tests also pass. In an actual isolated package,documentation and OpenSpec pass while documentation-only attestations still fail the release gate,retaining prior bounded records. Unchanged public63/source43 installation,six native revisions and owned-desktop evidence are reused with current digest checks;this turn adds no native or model run. Tasks7.1–7.3 complete,120/127 complete and7 open;marketplaceEligible stays false and supportedPluginHosts stays empty. Permissions/secrets,all commands,model routing,full distribution and actual creative review remain separate. [Evidence](docs/evidence/vectorcraft-release-gate-20261009.json).

Permissions and secrets remain in progress. A local candidate filters inherited environments at seven subprocess entry points,withholds raw child diagnostics,rejects extra asset instruction fields and explicitly named literal credential fields,and refuses to persist those credentials in rejected-review audit events. Eight targeted tests and132 Node regressions pass;146 Python tests pass. An actual native revision and subsequent technical check consume four shared attempts,and owned groups stop. This candidate has no new public fixed distribution or completed host secret-reference contract;tasks7.4–7.6 remain open,120/127 complete and7 open. Published63/source43 stay unchanged;old release evidence cannot authorize the modified worktree. The named-field check does not claim arbitrary secret detection in document text. [Evidence](docs/evidence/vectorcraft-permissions-candidate-20261009.json).

Candidate64 pins public source44(e5f8e1bb8528),preserving immutable63/source43. Source44 passes183 regressions with30 skips,six target tests and13 real independent cold installs. Candidate plugin132 Node and146 Python regressions pass;actual native revision and subsequent technical checking consume four shared attempts and stop owned groups. Source44 main/tag CI pass. Plugin64 has no public fixed qualification yet;host secret references,complete permission entry-point audit and all VC-RL-002 scenarios remain pending. Tasks7.4–7.6 remain open,120/127 complete and7 open. [Evidence](docs/evidence/vectorcraft-permissions-integration-candidate64-20261009.json).

Candidate64 now pins public source45(a4b1e624818f). Source45 passes28 permission targets,193 regressions with48 skips,13 real independent cold installs,and actual native revision/three exports/reopen,including signed GUI persistence and direct kernel refusals without Python prechecks. Current plugin132 Node/146 Python regressions and native revision/check pass within four shared attempts with all owned groups stopped. Original source44 snapshot and execution bytes are archived. Python asset preflight authorization,real host secret references and fixed64 permission acceptance remain open:120/127 complete,7 open,candidate64 unpublished,no V1 or marketplace qualification. [Evidence](docs/evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json).

Candidate64 now pins public source46 (91092712e427). Current evidence adds trusted Python asset roots and safe descriptor copies,14 authorization tests,28 native permission tests,13 independent cold starts,and actual managed creation/inherited revision with six exports,two prelaunch refusals and stopped owned groups. Source45 evidence remains historical. Node parent preflight audit,host secret references and fixed64 qualification remain open;120/127 tasks complete,7 open,no V1 or marketplace claim. [Evidence](docs/evidence/vectorcraft-permissions-assets-integration-candidate64-20261009.json).

The parent Node asset read race is now reproduced and fixed: a filtered Python helper reuses the pinned descriptor reader under frozen roots.133 Node/146 Python tests and actual managed native create/inherit with six exports pass. Full secret/fixed-install acceptance remains open. [Evidence](docs/evidence/vectorcraft-permissions-parent-assets-candidate64-20261009.json).

Task9.21 is complete on current candidate64/source46: actual current-conversation inspection of128/64/32 native previews,one explicit authorized green-fill revision,control preservation,shared budget/stagnation and nine stale/schema/restart guards. Malformed receipts now retain redacted rejection evidence. Creative acceptance remains pending because the small label is unreadable; no independence,automatic loop or fixed-distribution claim.121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-single-round64-20261009.json).

Review-read boundary increment: authorize the technical manifest before parsing, intersect request and review-store roots for captured files, and refuse ancestor replacement through descriptor reads. Review digests stream authorized files; checked identities bind the pinned reader and host adapters so changed dependencies invalidate old receipts. This candidate increment does not close7.4–7.6; complete parent reads/writes,host secret references and fixed distribution remain open. [Evidence](docs/evidence/vectorcraft-permissions-review-read-candidate64-20261009.json).

Controller read-boundary increment: read plans and source manifests through frozen-root authorization; stream safe source/dependency/input hashes and batch runtime freshness checks. Three ancestor-swap failures are fixed; a65MiB sparse file digest and input lists beyond4096 entries pass. Source snapshot copies,delivery inspection,complete write-root audit,host secret references and fixed release remain open;7.4–7.6 stay unchecked. [Evidence](docs/evidence/vectorcraft-permissions-controller-read-candidate64-20261009.json).

Delivery-read increment: safely read the manifest,artifact hashes and geometry JSON within frozen roots; recheck the actual geometry JSON digest. Ledger receipts bind the manifest bytes that passed verification and reject a rewritten manifest before receipt. Delivery-root replacement,nested replacement and unbound geometry JSON regressions are fixed. Source snapshot copies,parent writes,host secret references and fixed release remain open;7.4–7.6 stay unchecked. [Evidence](docs/evidence/vectorcraft-permissions-delivery-read-candidate64-20261009.json).


Source snapshot copy increment: stream pinned source descriptors within frozen roots and match the bound digest. Destination parents use O_NOFOLLOW; exclusive creation preserves existing files,failed copies remove only newly created files,and successful snapshots are readonly and fsynced. Projects above64MiB remain supported. Source swaps,digest drift and destination link/scope/existence guards pass. Remaining parent writes,host secret references and fixed distribution stay open;7.4–7.6 remain unchecked,121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-permissions-source-copy-candidate64-20261009.json).


Controller content-write increment: persist state,plan,event and control files through frozen directory descriptors,per-component O_NOFOLLOW,exclusive creation and fsync. State updates use random temporary names and atomic replacement relative to the same held directory; old.next links are not followed. Event identity and control digest bind held files/input bytes without path rereads. Two baseline failures,five new boundary tests,16 targeted tests,158 Node cases and actual native revision pass. Directory creation,skill tree copying,other parent writers,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-permissions-state-write-candidate64-20261009.json).


Controller directory/tree increment: snapshot directory creation,pinned skill copying and source snapshot digests now hold directory descriptors with per-component O_NOFOLLOW. Creation stays inside frozen roots; exclusive targets preserve existing data. Digests bind copied bytes with compatible UTF-16 path sorting,binary content,executable modes and empty directories. Source changes,links,invalid types and digest drift are refused; partial files remain inside the private root for inspection. Two original external-effect failures are fixed;19 targeted tests,163 Node cases and actual native revision/four-attempt stop pass. Earlier race tests now inject at the same descriptor-operation boundary;original bytes are archived. Other parent/database writes,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-permissions-tree-write-candidate64-20261009.json).


Technical-review write increment: freeze request data and write roots before decode. Output,delivery and checker snapshots use descriptor-bound directories and exclusive readonly writes;report receipts bind the verified write digest. Checker snapshot hashes use safe batch reads. Checker identity expands from6 to10 files with four write/directory adapters;dependency drift invalidates old receipts. Three external-write failures and one async request mutation failure are fixed;21 targeted tests,171 Node cases and actual native revision/four-attempt stop pass. Database/backup paths,launch boundaries,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-permissions-technical-write-candidate64-20261009.json).


Ledger backup/read increment: VACUUM INTO writes a random host-private staging directory,then validates schema/digest and publishes an exclusive readonly400,fsynced backup through safe descriptors. The final digest is checked inside the frozen backup root. Cleanup ownership starts after exclusive directory creation;cleanup failures close the connection and stop migration. Ledger verification hashes only within the task frozen output. One external backup write and two external verification reads are fixed;11 targeted tests and176 Node cases pass,including real SQLite v1/v2,committed uncheckpointed WAL,budgets and runtime selection. Actual native revision/four-attempt stop passes on fresh schema3;this is not a legacy native-state migration. Primary database/SQLite scratch paths,launch boundaries,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-permissions-backup-write-candidate64-20261009.json).


Public-commit installed-copy acceptance: dev.64/source46 installs from the exact remote-main commit `11a49e9d1d5f471d1c4cbf93551bdb1c87abe3d1` into an isolated Codex0.153.4 home with spaces. All13 skills load with matching identities;13 independent HTTPS empty-cache starts and12 native create/revise pairs pass,with setup-only explicitly separate and zero skips. The installed Harness passes native revision,three-format decoding,four-attempt shared-budget stop and source/text preservation;feedback scores are explicit QA fixtures. Five reference guards and161 Python regressions pass. The installer still requires the public version tag by default;candidate mode accepts only a full SHA matching remote main and records publicTagVerified=false. Original drivers are archived without re-signing old reports. This advances the install/cold-start portions of9.9/9.18;model routing,public-tag revalidation,the six-layer release gate,exhaustive command/GUI and secret boundaries remain open.121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-public-commit64-install-20261009.json).


Current installed-copy four-scenario revalidation: public-commit dev.64/source46 passes6 native revisions,15 guards and stale-proposal refusal after an owned signed desktop modifies,saves and reopens its source project. VC-QA-002 checks best candidates,round/stagnation limits,budgets and text preservation. The initial desktop fixture was correctly refused outside its owned root;placing the fixture inside that root passes without broadening product permissions. Evidence v2 derives the complete10-file checker identity from bound checker_bundle.ts;the release gate verifies the selected current report. Original v1 three-file proofs and drivers remain archived. All six development-release layers now pass;marketplace eligibility remains false. Post-publication tag installation,model routing,complete permission/secret boundaries and per-command GUI acceptance remain open:121/127 tasks complete,6 open. Scores remain explicit QA fixtures,not creative judgment. [Evidence](docs/evidence/vectorcraft-revision-commit64-20261009.json).


Post-publication tag verification: plugin v0.1.0-dev.64 is published at6763caa1f0e6596fc01d298304794d0e9c139dc3,pinning independent source v0.1.0-dev.46. Actual public-tag installation into a fresh isolated Codex0.153.4 home discovers13 matching skills. All13 independent HTTPS empty-runtime starts and12 native create/revise pairs pass,setup-only separate,zero skips. Installed product files exactly match the pre-publication four-scenario copy;all4 main/tag CI runs pass. Thirteen completed runtime caches were removed after confirming no open handles;native projects and execution records remain. This completes the public-release/install/cold-start portion of9.18,whose9.9 model-routing prerequisite remains open;9.18 is not closed. Full permission/secret boundaries,per-command GUI,other platforms and completeV1 remain unqualified:121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-public-tag64-install-20261009.json).


Fixed-installed command increment: the actual public plugin dev.64/source46 copy passes22 paint commands,44 native save/reopen stages and88 decoded SVG/PNG exports in an owned signed desktop session. Checks bind live enabled state,verbatim parameters,target colors/gradients/freeform data,control text,source preservation and previous deliveries. Freeform splitting follows the pinned upstream Catmull-Rom curve. Initial QA assumptions about registry size,RGB readback,selection and linear positions were retained and corrected;product code was unchanged. The external complete catalog matrix records22/585 passed and563 NOT_RUN;frozen skills are unchanged. Native tool canvas images are not OS-window screenshots or creative review. Task8.3 remains open;121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-command-matrix-fixed64-20261009.json).


Fixed-installed swatch acceptance: all22 swatch commands pass44 native save/reopen stages and88 decoded SVG/PNG exports in an owned signed desktop using the actual public plugin dev.64/source46 copy. Per-command semantics cover global edits,deletion with color-preserving unlink,merge relinking,group edits/sorting/moves,Lab spot options and library save/load. Control text,source and previous deliveries are preserved;all13 installed skill digests remain unchanged. The first library-load run exposed a QA field-access error;the retained failure was corrected in the checker and the whole family revalidated,without product or skill changes. Reusing original paint22 evidence yields44/585 accepted commands,541 NOT_RUN,88 save/reopen stages and176 decoded exports;25 command-focused regressions pass. Native canvas images do not establish OS-window screenshots or creative review. Task8.3 remains open;121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families-fixed64-20261009.json).


Fixed-installed stroke acceptance: all10 stroke commands pass20 native save/reopen stages and40 decoded SVG/PNG exports on actual public plugin dev.64/source46;all13 installed skill digests remain unchanged. Open paths exercise arrows,advanced profiles and width points;closed paths exercise inside/outside alignment. Assertions cover pt-to-half-width factors,arrow scale swaps,along/across profile flips,and custom profile add/delete/reset. Fill,control text,geometry,source and previous deliveries are preserved. Ten actual canvas/PNG comparisons across five style revisions show142–1189 changed pixels;43 command-focused regressions pass. Native-disabled empty reset and duplicate-profile add QA failures were retained;corrected contexts pass without product or skill changes. Profile names are qualified only within the owned private desktop session;preference persistence across app restarts remains NOT_RUN. Canvas images do not establish OS-window screenshots or creative judgment. Original44-command matrix and verifier bytes remain preserved. Current coverage is54/585,531 NOT_RUN,108 save/reopen stages and216 decoded exports. Task8.3 remains open;121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families54-fixed64-20261009.json).


Fixed-installed transparency increment: all17 transparency commands pass34 native save/reopen stages and68 decoded SVG/PNG exports on actual public dev.64/source46 in an owned signed desktop. Checks cover object opacity/blend/knockout,mask art movement and release reidentification,enable/link/options,page flags,new-mask defaults,and native edit/view state. Temporary editing layers are excluded from saved projects;mask art,control text and all13 installed skill identities are preserved. Six actual canvas/PNG comparisons across three revisions show1208–2160 changed pixels. Retained QA setup failures for invalid stroke colors,omitted false defaults and an unsaved probe document were corrected;the complete family passed in a fresh owned session without product or locked-skill changes. Defaults are qualified only within the private session;restart persistence remains NOT_RUN. Default screenshots render the artboard and do not prove greyscale mask viewing or full-window GUI. Original54-command matrix/verifier bytes remain preserved. Current coverage:71/585 passed,514 NOT_RUN,142 save/reopen stages,284 decoded exports. Task8.3 remains open;121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families71-fixed64-20261009.json).


A separate owned-window check captures two1440×900 native app windows for viewOpacityMask: three interior samples are grey with viewing on and colored with viewing off,while native mask editing stays active. This qualifies only this command’s window behavior;full585-command GUI acceptance remains open. [Evidence](docs/evidence/vectorcraft-mask-window-fixed64-20261009.json).


Fixed-installed shape acceptance: all10 shape commands pass20 native save/reopen stages,40 decoded SVG/PNG exports and20 actual owned app-window captures on public dev.64/source46. Independent formulas check rounded corners,ellipse/arc handles,polygon/star vertices and rotation,reversed decaying spirals,grid divider ordering,and deterministic flare subtrees/radial gradients. Each second round revises only the actual previous return-ID object's opacity and creates a differently parameterized shape;control artwork/text,other fields,source and previous delivery files are preserved. All30 canvas/PNG/window comparisons change244–165235 pixels;all13 installed skill identities remain unchanged. Original physical window scales1x/2x are recorded;window analysis explicitly normalizes to1440x900. Failed screenshot reads are retained with at most three read-only attempts;edit requests are never replayed. Retained QA field assumptions and white-on-white flare visibility were corrected;an owned dark backdrop makes the complete fresh-session family observable. Original71-command matrix and verifier bytes remain preserved. Current coverage:81/585 passed,504 NOT_RUN,162 save/reopen stages,324 decoded exports. Window evidence covers only these10 shape commands,not all-command GUI,creative/model or completeV1 acceptance. Task8.3 remains open;121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families81-fixed64-20261009.json).


Fixed-installed layer acceptance:all11 layer commands pass22 native save/reopen stages,44 decoded SVG/PNG exports and22 actual owned app-window captures on public dev.64/source46. Independent full-tree assertions check insertion above the current layer,nested sublayers,deletion/current-layer fallback,fresh preorder IDs throughout duplicated subtrees,hidden/locked selection pruning,paint-order collection,immediate eligible children,clipping-path reorder/paint removal and unpainted release,and persisted paste options. Current layer,selection and target are independently read from native session state;project persistence is not claimed for session fields. Each second round first renames an owned layer;control objects,other fields,source and previous delivery remain preserved. All33 actual canvas/PNG/window comparisons pass their explicit preservation/change/measurement contracts;the four visibility/clipping canvas/PNG comparisons change964 and419 pixels. Window differences alone do not prove command semantics. All13 installed skill identities remain unchanged;22 new assertion/evidence regressions pass. Original81-command matrix and verifier bytes remain preserved. Current coverage:92/585 passed,493 NOT_RUN,184 save/reopen stages,368 decoded exports. Task8.3 remains open;121/127 tasks complete,6 open;no all-command GUI,creative/model,permission/secret,marketplace or completeV1 claim. [Evidence](docs/evidence/vectorcraft-command-families92-fixed64-20261009.json).


Fixed-installed graphic-style acceptance:all18 graphicStyle commands pass36 native save/reopen stages,72 decoded SVG/PNG exports and36 actual owned app-window captures on public dev.64/source46. Independent full-tree assertions check unit-box gradient placement on differently sized rectangles,replace/add appearance and transparency preservation,unique names/stable IDs,delete-with-look-preserved unlinking,redefinition propagation only to still-synchronized objects,preservation/unlinking of edited objects,merge stack order,sort/move,unused/link readbacks,built-in library inventory,and owned library save/load/name-conflict numbering/reimport deduplication. Each second round first renames an owned source object;control text,other fields,source and previous delivery remain preserved. All54 canvas/PNG/window comparisons use explicit change/preservation/measurement contracts. Delete rounds start with different primed appearances,so their cross-round images are measured only;each deletion preserves its prior appearance by full-tree assertion. Window differences alone do not prove semantics. All13 installed skill identities remain unchanged;23 new assertion/evidence regressions pass. Override Character Color covers private-session preference/list readback only;application-restart persistence is NOT_RUN. Original92-command matrix and verifier bytes remain preserved. Current coverage:110/585 passed,475 NOT_RUN,220 save/reopen stages,440 decoded exports. Task8.3 remains open;121/127 tasks complete,6 open;no exhaustive GUI,creative/model,permission/secret,marketplace or completeV1 claim. [Evidence](docs/evidence/vectorcraft-command-families110-fixed64-20261009.json).


Appearance QA diagnostic checkpoint: candidate drivers for16 commands, image checks and independent stack assertions are preserved without acceptance. Run a2 lost target object2 after save/reopen despite an in-memory undo restoration; a3 stopped on an unknown effect.apply result. Owned processes stopped with no automatic replay; root cause remains unassigned. Candidate checkpoint-reopen probe restoration is unqualified. The18 positive evidence tests require a missing fixed PASS report and remain explicit pending QA; CI runs stack units and failure-record assertions. Accepted coverage stays110/585,475 NOT_RUN;121/127 tasks complete,6 open,including8.3. Product tag dev.64/source46 remains unchanged. [Diagnostic](docs/VectorCraft-Appearance-Diagnostic.md).


Fixed-installed appearance acceptance:all16 appearance commands pass32 native save/reopen stages,64 decoded SVG/PNG exports and32 actual owned1440x900 app windows on public dev.64/source46. Independent full-tree assertions cover paint-only fill/stroke additions,clear/basic reduction,item/effect edits,unique descending deletion,whole-row duplication and Contents slot movement,relative gradient/reverse/append pickup,hidden restoration,locked-child filtering,and masked-source transfer/copy with source clearing and mask preservation. Actual edit/create probes establish active appearance row and new-art preference behavior,then restore owned native saved checkpoints;undo and preference restart acceptance remain open. Second rounds rename an owned control;control text,other fields,source,previous delivery and all13 installed skill identities remain preserved. All48 image comparisons use explicit change/preservation/measurement contracts;the8 canvas/PNG comparisons for4 change commands differ722–2062 pixels. Earlier undo/reopen,unknown-reply and cross-layer mask-order fixture failures are retained;correct source-layer/explicit-ID setup passes in a fresh full-family run without product or skill changes. The18 pending evidence tests now join regular discovery,with2 additional tamper and2 fixture tests. Original110-command matrix/verifier and diagnostic candidate bytes remain preserved. Current coverage126/585,459 NOT_RUN,252 save/reopen stages and504 decoded exports. Task8.3 remains open;121/127 tasks complete,6 open;no exhaustive GUI,undo,creative/model,secret-boundary,marketplace or completeV1 claim. [Evidence](docs/evidence/vectorcraft-command-families126-fixed64-20261009.json).


Fixed-installed effect supplement: all7 effect commands pass14 native save/reopen stages,28 decoded SVG/PNG exports and14 owned app-window captures on public dev.64/source46. Independent assertions cover the complete45-entry catalog,parameter merging,active-row versus explicit targeting,stack copying/moving,and geometry,stroke-outline,shadow/blur raster,text,crop-mark,transform-copy and container expansion. Two embedded PNG checks bind72ppi region formulas,digests,alpha and pixels;21 canvas/PNG/window comparisons pass. All13 installed skill identities,control text,source and previous deliveries are preserved. Aggregate coverage is133/585,452 NOT_RUN,266 save/reopen stages and532 decoded exports;42 new regressions pass. All effect/brush/symbol variants,undo,model,secret boundaries,full GUI and completeV1 remain unqualified;task8.3 stays open,121/127 tasks complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families133-fixed64-20261009.json).


Fixed-installed guide supplement: all3 guide commands pass6 native save/reopen stages,12 decoded SVG/PNG exports and6 owned app windows on public dev.64/source46. Independent list assertions check append indices,remove compaction and direction-preserving movement;round2 first renames only the owned control object. Six native locked/unlocked registry probes show add remains enabled while locked remove/move are disabled;models are preserved and unlock restored,without submitting disabled edits. Nine image comparisons preserve exported artwork;28 independent window-coordinate checks confirm present guides and absent removed/moved lines. A new runner waits at most20 read-only observations for fitted views and requires stable capture views. Initial null-return,canvas-width/height and unfitted-view failures remain retained. All13 skill identities,control text,source and previous deliveries are preserved.31 new regressions pass;aggregate136/585 passed,449 NOT_RUN,272 save/reopen stages,544 decoded exports. Task8.3 stays open,121/127 complete,6 open;undo,model,secret boundaries,full GUI,marketplace and completeV1 remain unqualified. [Evidence](docs/evidence/vectorcraft-command-families136-fixed64-20261009.json).


Fixed-installed attributes supplement: all2 attributes commands pass4 native save/reopen stages,8 decoded SVG/PNG exports and4 actual Attributes-panel windows on public dev.64/source46. Independent full-tree assertions cover group leaves versus text characters and appearance-row overprint targeting,unique changed-object counts,mixed attributes/fill rules/straight-rectangle winding,default center and empty-attribute cleanup,trimmed strings,and a session-local deduplicated10-URL history. Round2 first renames the owned control object;control text,source,previous deliveries and13 installed skill identities are preserved. Six canvas/PNG/window comparisons preserve normal-mode artwork;4 additional SVG files independently bind hyperlinks to the complete model,and8 fixed-layout checkbox pixel checks distinguish mixed/checked/unchecked states.38 new regressions pass;original136-command matrix/verifier are preserved. Current138/585 passed,447 NOT_RUN,276 save/reopen stages,552 decoded exports. Print overprint simulation,curved-path winding,URL history after app restart,undo,model,full GUI and completeV1 remain unqualified;task8.3 open,121/127 complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families138-fixed64-20261009.json).


Fixed-installed Magic Wand settings supplement: both magicWand commands pass4 native save/reopen stages,8 decoded SVG/PNG exports and4 actual Magic Wand-panel windows on public dev.64/source46. Independent settings assertions cover defaults,partial merge,reset then override,ignored unknown fields,four tolerance clamps and fractional values. Pen/selection tool switches and same-session native reopen preserve settings. Round2 first renames the owned control object;complete tree,swatches,control text,source,previous deliveries and13 installed skill identities are preserved. Six canvas/PNG/window comparisons preserve artwork;20 independent settings-derived checkbox pixel checks cover five flags.22 new regressions pass;original138-command matrix/verifier bytes are preserved. Current140/585 passed,445 NOT_RUN,280 save/reopen stages,560 decoded exports. App-restart preference persistence and select.magicWand matching remain unqualified;undo,model,fullGUI,creative,marketplace and completeV1 remain open;task8.3 open,121/127 complete,6 open. [Evidence](docs/evidence/vectorcraft-command-families140-fixed64-20261009.json).

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

Plugin display name: **VectorCraft Use**. Official upstream icon provenance and licenses are included under `assets/official-icon-source.json` and adjacent LICENSE files.

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

## Vector production scenario candidates

Adds three independent skills: vectorcraft-clipped-illustration, vectorcraft-sticker-grid and vectorcraft-sticker-offset-border. Each includes native methods, concrete parameters, actual returned ID binding and editability checks after reopening. These additions are not released yet; real design quality and host editor synchronization remain unverified.
