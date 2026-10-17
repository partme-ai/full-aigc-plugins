# EffectCraft Agent Plugin

Development source dev.52 / plugin dev.54: cancellation recovery and family completion barrier; 27 cancellation tests and a real macOS native parent/child cancel, controller crash and readonly recovery case pass. Parents wait for descendants; unknown edits retain reconciling. Cross-platform, host and full V1 acceptance remain open. [Evidence](docs/evidence/cancel-family-candidate-20261009.json).

Historical pre-release cancellation-recovery checkpoint beyond source51/plugin53: active startup leases retain cancel_requested; restart reconciliation confirms the original stopped lifecycle and preserves unknown edits. A versioned process-exit record separates forced group stop from a verified business exit. 12 targeted tests, 536 regressions (498 passes / 38 conditional skips), and a current readonly installed-skill native cancellation/crash/reconciliation case pass. Published snapshots stay unchanged; full task-family cancellation, other platforms, hosts and V1 remain open. [Evidence](docs/evidence/cancel-restart-candidate-20261009.json).

Development source dev.51 / plugin dev.53: POSIX private group ownership and nonce-bound business results cover guardian loss, orphan descendants and forced cancellation. Current regression and offline installed-copy evidence: [release validation](docs/evidence/group-ownership-release51-20261009.json). Historical checkpoints below retain their original fingerprints; cross-platform native, fixed-host, creative acceptance and full V1 remain open.

Historical single-skill offline checkpoint completes9.5.1:15/15 actual readonly macOS arm64 installs with spaces, unavailable system Python and network denied pass public run/review, native reopen and12-frame decode. All installed copies matched the source at that checkpoint. One cold cache and14 verified shared-cache reuses; official archives and ffmpeg/ffprobe are prerequisites. Target-platform9.1.2, domain/transparent handoff9.5.2, hosts and fullV1 stay open. [Evidence](docs/evidence/independent-offline15-candidate-20261009.json).

Historical process-group checkpoint:10 targeted tests and516 regressions pass (478 passes/38 conditional skips), including actual macOS sandbox exit and descendant cleanup. Historical unknown tasks remain preserved without replay. At that checkpoint source50/plugin52 snapshots were unchanged; target platforms and fullV1 remain open. [Evidence](docs/evidence/process-group-probe-candidate-20261009.json).

Development source dev.50 / plugin dev.52: trusted v2 tasks select their original Python before current-runtime preparation; managed entry supports CRAFT_RUNTIME_ARCHIVE offline native artifacts. Current macOS native reopen/decode passes; native Windows, fixed-host and full V1 acceptance remain open. [Evidence](docs/evidence/release-readiness-source50-20261009.json).

Turn text, graphics and footage into an editable `.ecproj`, dependencies and rendered media.

Current plugin: `0.1.0-dev.54`; skill source: `0.1.0-dev.52`; 15 independent skills.

Verified first-use platform: macOS arm64 and Python 3.11+. Pinned runtimes install into the user data directory; skill files stay in their host-loaded directory. These are development releases; complete V1 acceptance and generic Skills CLI installation remain open.

Maintainer source validation rejects symbolic links, incomplete locks and version-named branches, and checks all declared sources before replacing any managed skill. Published skill/runtime identities remain unchanged. [Snapshot preflight architecture](docs/Skill-Snapshot-Self-Contained.md).

## First use

Invoke **`effectcraft-use`** in your host. For direct CLI use, set `SKILL_DIR` to the absolute directory of the `SKILL.md` actually loaded by that host. It may be under user/project `.agents/skills`, the plugin, or a host cache; use the actual path. Each entry below installs/verifies its locked runtime before invoking it.

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
sh "$SKILL_DIR/scripts/launch.sh" doctor
sh "$SKILL_DIR/scripts/launch.sh" run --plan "$SKILL_DIR/examples/brand-intro.json" --output "$PWD/effectcraft-result"
```
<!-- CRAFT_FIRST_USE_END -->

Read the [editable workflow](skills/effectcraft-use/references/workflow.md) for inputs, native projects and targeted revisions. [Setup and skill entry](skills/effectcraft-use/SKILL.md) · [version-bound history](RELEASE-HISTORY.md). Command/version queries verify installation and discovery; they do not constitute creative completion.

[First-use navigation evidence](docs/evidence/craft-readme-first-use-navigation-20261007.json).

Fixed installed path acceptance: standalone skills and Art mixed work pass native creation/reopen, targeted revision and export under Chinese-and-space paths; Art also verifies moved delivery. Skills/runtime identities stay unchanged. This is bounded macOS arm64 first-use evidence. [Path acceptance evidence](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

Historical source candidate before the fixed release: structurally invalid runtime/Node locks now return local setup diagnostics before runtime writes/downloads. Five candidate native first-use checks pass; published plugin snapshots remain unchanged until separate immutable release acceptance. [Lock diagnostics candidate](docs/EffectCraft-Lock-Shape-Architecture.md).

---

Fixed native first-use and complete-command recovery acceptance passed:58 standalone cold installations, ten Art all-domain cold installations, four partial-download SSL EOF recoveries,72 post-save faults, four healthy command revisions and mixed HD revision/recovery/moved delivery. Installed identities remain unchanged. Only domain2.10/8.11 and Art4.10 close; exhaustive2639-command, GUI, model, generic Skills CLI and fullV1 gates remain open. [Version-bound evidence](docs/evidence/codex-native-download-first-use-20261007.json).

Historical release record: Current plugin: `0.1.0-dev.21`; skill source: `0.1.0-dev.19`; parenting/expression recipes included; 13 fixed installed expression/parent cold cases pass; Art bundle update pending; full V1 remains open.

Historical candidate observation before fixed acceptance: Native download recovery candidate: up to three read-only attempts discard partial archives. Earlier fixed cold installs failed on SSL EOF; new fixed installed acceptance remains open.

Previous version-bound plugin: `0.1.0-dev.18`; skill source: `0.1.0-dev.16`; complete-command inner JSON fix is published, fixed installed acceptance pending.

Previous version-bound failed-stage acceptance: plugin dev.17, standalone source dev.15. All58 independent CLI cold starts,24 original-stage native fault cases and37 native scene tests plus6 contracts pass. Art77 bundle upgrade remains open. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

Fixed domain-client first use: Film plugin dev.16 / source dev.15; Effect/Photo/Vector plugin dev.15 / source dev.14. Codex discovers 58 skills without errors. Actual installed copies pass 24 post-save faults and four healthy public workflows; the published Art engine with the installed Vector client passes six faults. All58 installed identities remain unchanged. Art dev.75 still bundles earlier domain sources; exhaustive command/GUI/model acceptance remains open. [Version-bound evidence](docs/evidence/codex-public-workflow-session-first-use-20261007.json).
Previous version-bound protocol recovery acceptance passed: 288 cases across 48 standalone source skills, 24 cases in actual installed copies, four healthy revision cases, and 58 unchanged installed skill identities. See [fixed evidence](docs/evidence/codex-protocol-fault-first-use-20261007.json). Exhaustive command/GUI acceptance and the Art domain-bundle upgrade remain open.

Protocol fault repair candidate: all 13 independently copied skills pass separate empty public-runtime installation and six faulty replies after real native save (78 cases; zero skips). Requests are not replayed; unknown receipts, saved-project reopening and delivery/skill preservation are checked. [Evidence](docs/evidence/protocol-fault-first-use-20261007.json). Fixed installed release and Art bundle upgrade remain separate gates.

Fixed plugin 0.1.0-dev.13 / skills 0.1.0-dev.12 installed revision acceptance passes: isolated Codex discovers all 58 skills without loading errors; this installed domain skill completes the documented cold creation/revision plans, saved-project reopening and non-target preservation. All58 installed digests remain unchanged; current fixed release CI passes. [Fixed revision evidence](docs/evidence/codex-complete-command-revision-first-use-20261007.json). Full command/GUI/model acceptance remains open.

All 13 domain skills pass the paired revision plans when copied alone and installed from separate empty public runtimes (145.856 seconds; zero skips). [Revision evidence](docs/evidence/complete-command-revision-first-use-20261007.json). Fixed installation of the updated snapshot remains a separate gate.

The complete-command entry now includes paired executable creation/revision recipes, explicit selection prerequisites after reopening, and native persisted-state/non-target checks. Each standalone skill includes both JSON plans. [Usage](skills/effectcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision). Full per-command and GUI acceptance remains open.

Previous version-bound release first use passed: isolated Codex 0.153.4 discovers all 58 skills without loading errors; every installed skill independently cold-installs its public locked runtime (385.234 seconds); installed domain command samples and Art 1080p mixed revision/recovery/package checks pass. All installed skill digests remain unchanged; fixed CI and five-bundle rebuild pass. [Version-bound evidence](docs/evidence/codex-complete-command-first-use-20261007.json). Generic Skills CLI installation, full command/GUI and creative acceptance remain open.

## Complete native command entry

All 13 standalone skills now pass separate empty-runtime installation from locked public CLI archives, followed by native creation, save/reopen, domain assertions and rendered image checks (152.42 seconds; zero skips). [Cold-first-use evidence](docs/evidence/complete-commands-cold-first-use-20261007.json). This verifies this complete-command sample in every skill; exhaustive command/GUI and actual host installation remain separate.

Published development snapshot: skills dev.11 / plugin dev.12; bounded fixed-host first use passed.

All 640 commands now have verbatim parameters, skill routing, and same-session invocation through `commands.py list / describe / check / run`. Live enabled state is checked; the existing 21-operation delivery workflow remains bounded. GUI commands require explicit bridge mode. Complete registry coverage does not establish full command acceptance.

[Architecture and usage](docs/EffectCraft-Complete-Commands-Architecture.md) · [Complete reference](skills/effectcraft-use/references/command-reference.md) · [Runnable example](skills/effectcraft-use/examples/commands-advanced.json)

Independent-skills-driven Layer compositing, motion graphics and shot effects.

[English](README.md) | [简体中文](README.zh-CN.md)

## Current release and reproducible host checks

Previously verified plugin/skill suite: `0.1.0-dev.3`. Codex 0.147.0 and 0.153.4 installed five fixed public releases and discovered all 58 enabled namespaced skills with zero loading errors and matching source digests. Five representative workflows passed through installed task-skill entrypoints on 0.147.0, including native projects, targeted revisions and the mixed ArtCraft online workflow. Model dispatch, desktop GUI, final creative review and full interchange fidelity remain unverified.

[Host verification design](docs/EffectCraft-Host-Verification-Architecture.md) · [Version-bound evidence](docs/evidence/codex-skill-suite.json). Historical milestones below retain their original scope; the current manifest and locks own version identity.

> Development release. Fixed-tag Codex installation, skill discovery and representative native workflows have passed; complete product and creative acceptance remain open.

Implementation has started in the independent skills package. The isolated first-use installer is tested on macOS arm64; complete creative workflows and plugin host acceptance remain pending. [Evidence](docs/evidence/bootstrap-tests.json)

## Positioning

Create a brand intro with a reopenable .ecproj and editor-ready render; edit its text while preserving other layers and animation curves.

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
| Plugin ID | effectcraft |
| Metadata version | 0.1.0-dev.54 |
| Stage | implementation-in-progress |
| Skills source | effectcraft-skills / v0.1.0-dev.52 |
| Execution | Upstream CLI; ArtCraft uses child adapters |
| Host compatibility | Codex development install/discovery pass; GUI and other hosts pending |
| License | Apache-2.0 (original repository content) |


## Capabilities and boundaries

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Composition creation and range | Set composition dimensions, frame rate, duration and work area explicitly; convert time units according to the verified adapter contract. | Full scope pending |
| Layers and footage dependencies | Maintain layer IDs, order, parenting, footage references and visibility; detect parent cycles and missing footage. | Full scope pending |
| Text, graphics and keyframes | Record text, transforms and keyframes by property path with interpolation; text revision must not rebuild unrelated animation. | Full scope pending |
| Effect and mask capability matching | Discover commands and parameter schemas before applying effects or masks; reject unsupported parameters before execution rather than skipping them. | Full scope pending |
| Alpha and color handoff | Record color space, bit depth, alpha interpretation and codec during handoff; verify transparency from actual pixels or channel inspection. | Full scope pending |
| Project and render delivery | Reopen .ecproj to inspect layers and keyframes; bind renders to composition revisions and report editability lost by baking. | Full scope pending |

Does not rewrite upstream editors, silently change native deliverable formats, or claim GUI/cross-platform acceptance.

## Architecture and documentation

- [Complete runtime architecture](docs/EffectCraft-Runtime-Architecture.md)
- [Technical plan and roadmap](product-docs/EffectCraft/en/5%E3%80%81EffectCraft-Technical-Plan.md)
- [V1 PRD and requirement mapping](product-docs/EffectCraft/en/V1/5%E3%80%81EffectCraft-PRD-V1.md)
- [Complete documentation index](docs/README.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [Domain technical design](docs/EffectCraft-Domain-Design.md)

## Currently executable quick start

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
These commands validate documentation and specifications, not product workflows. OpenSpec validation uses 1.13.1; this repository does not install tools automatically.

After installing the official CLI, perform a basic check:

```bash
effectcraft-cli --version
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

[Upstream EffectCraft](https://github.com/storytold/effectcraft) · [Issues](https://github.com/full-aigc-plugins/effectcraft-plugin/issues)

Independent skill workflow acceptance now covers native `.ecproj` round trips, transparent PNG previews, decoded H.264 export and text-only revisions preserving unrelated layers and keyframes (14 tests). See [test evidence](docs/evidence/effect-workflow-tests.json). Full Harness, external dependency packaging and plugin-host acceptance remain pending.

External PNG media collection and footprint-preserving replacement are now tested in the 15-test suite. See [current evidence](docs/evidence/effect-assets-tests.json). Full domain and host acceptance remain in progress.

Independent skills are pinned at the current published development tag `v0.1.0-dev.6`, including the exact source commit and whole-skill digest in `skills.lock.json`. Verify using `python3 scripts/vendor/skill_vendor.py check`. These source snapshots do not establish plugin-host acceptance or production readiness.

## Development skill installation and use

Install the independent skill: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-use`. Run the public entry from the actual installed directory; this plugin snapshot includes the same skill.

```bash
python3 -I -B skills/effectcraft-use/scripts/bootstrap.py
python3 -I -B skills/effectcraft-use/scripts/workflow.py --help
```

First use installs the pinned official CLI into user-level storage. Requires macOS arm64 and Python 3.11+. Use the bundled example with real input assets; consult SKILL.md for delivery and revision contracts. [Source verification](docs/evidence/skill-publication.json).

## Codex development host checks

All five plugins installed from public tags into an isolated Codex configuration. App-server discovered their namespaced skills without loading errors; the installed ArtCraft entry produced four native projects. [Host evidence](docs/evidence/codex-installation.json). These controlled development checks do not establish desktop GUI, other hosts, complete creative or production marketplace acceptance.

Development version `0.1.0-dev.1` pins the independent skill install-lock fix: bounded coordination for concurrent installation/reuse, with no native task replay.

The current development milestone adds hash-bound exchange loss reports to native deliveries. lost, observed and unknown are separate; derivatives never substitute for native projects. Font/effect/mask fidelity across editors remains unverified, so full exchange acceptance stays open.

## CLI and task skill suite

The source suite contains 13 independently installable skills with setup, public CLI operations and focused tasks. [Architecture and catalogue](docs/EffectCraft-Skill-Suite-Architecture.md). Runtime and plugin versions are separate; prior host evidence retains its original version scope.

Previous version-bound plugin: `0.1.0-dev.7`; skill suite: `0.1.0-dev.6`. The corrected examples resolve scripts from the actual host-loaded `SKILL.md` directory. All skills passed isolated entry-point checks in user, project and plugin layouts with spaces. [Path evidence](docs/evidence/installed-skill-paths.json). Earlier host evidence above covers its recorded release; existing installations require an update.

Plugin `0.1.0-dev.6` corrects the whole-skill digests by fetching the immutable public source tag, without local Python caches. Plugin tag `v0.1.0-dev.5` is superseded and must not be installed because its source digests included ignored development caches.

Plugin dev.7 pins source dev.6 with a self-contained editable-mask example and vertex-edit/removal workflow. All 39 default-public-download native tests pass with zero skipped; isolated task skills install into empty runtimes, preserve old projects and non-target layers, and verify actual RGBA mask boundaries. [Evidence](docs/evidence/task-skill-first-use.json). Native runtime remains 0.2.0; model/GUI and full creative acceptance remain open.

Current fixed-release host verification (2026-10-06): Codex 0.153.4 installs all five current pinned plugins and discovers all 58 skills with exact content identity. This plugin’s representative native workflow runs from its actual installed skill path with a fresh native runtime; creation/reopening/revision checks pass. All 58 installed skill hashes remain unchanged after the five workflows. [Evidence](docs/evidence/codex-current-release-20261006.json). The shared explicit-tag generator belongs to ArtCraft. Model dispatch awaits authorization; GUI, creative and full host acceptance remain pending. This QA maintenance changes no published skill/runtime content or release tags.

The fixed FilmCraft dev.6 / EffectCraft dev.7 / PhotoCraft dev.6 / VectorCraft dev.6 / ArtCraft dev.17 matrix passed isolated Codex discovery of 58 skills and representative native workflows from installed skill content. All installed skill digests remained unchanged afterward. [Installed native evidence](docs/evidence/codex-release17-native-20261006.json). Model dispatch, GUI and complete creative acceptance remain unverified.

[Actual transparent handoff to FilmCraft](docs/EffectCraft-FilmCraft-Alpha-Handoff-Acceptance.md): one installed two-domain empty-runtime case passes, preserving title animation and compositing native RGBA PNG over a video background with verified foreground pixels. Complete color and animated-alpha-video acceptance remain open.

Installed animation skill temporal first use passed: four native RGBA samples and 12 decoded video frames verify the fade; text revision preserves badge/key properties and original deliveries. [Temporal acceptance](docs/EffectCraft-Temporal-Animation-Acceptance.md). Full creative/animated-alpha acceptance remains open.

Independent EffectCraft source dev.7 maps matching effect/mask plan parameter validation errors to unsupported_mapping; native CLI stays at 0.2.0. Actual rejected creation/revision preserves prior deliveries. All 44 native source tests pass with zero skips (182.083s); fixed new plugin installed acceptance is recorded below. [Architecture](docs/EffectCraft-Parameter-Errors-Architecture.md) · [Evidence](docs/evidence/parameter-mapping-repair-20261006.json).

Fixed plugin dev.8 / source dev.7 installed acceptance passes: five plugins, 58 skills, zero loading errors; independent effect/mask skills cold-verify valid creation and rejected new/revision parameters (1 test, 24.714s), all 13 skills pass separate public cold first use, and all host-installed hashes remain intact. [Release-bound evidence](docs/evidence/codex-effectcraft8-parameter-first-use-20261006.json). ArtCraft bundle/domain-code propagation and complete V1 gates remain open.

Dynamic RGBA PNG sequences now retain the editable ecproj and every frame digest, rate and duration in craft-image-sequence/v1. Source cold installation and actual Film handoff pass; fixed new-plugin and Art acceptance remain pending. [Architecture](docs/EffectCraft-Dynamic-Sequence-Architecture.md).

Fixed Effect dev.9 and Film dev.10 installed-first-use dynamic handoff now passes: three native tests, all 58 skills discovered without loading errors, and all installed hashes unchanged after each execution. [Evidence](docs/evidence/codex-effectcraft9-filmcraft10-dynamic-first-use-20261006.json). Art dynamic integration remains pending.

Current fixed-release domain task matrix: 37 native scenarios and 6 contract checks passed with zero skips across FilmCraft dev.10, EffectCraft dev.9, PhotoCraft dev.10 and VectorCraft dev.11. Each task copied only its selected installed skill and installed the native CLI into a fresh runtime directory from the default public archive. Native projects, actual pixels/audio and targeted preservation were checked; all 58 installed skill identities remained unchanged. [Version-bound evidence](docs/evidence/codex-current-domain-task-matrix-20261006.json). This does not close full V1, generic Skills CLI installation, model dispatch, GUI or creative acceptance.

Current plugin dev.10 pins source dev.9 with whole-plan effect/mask field preflight and read-only live schema comparison before opening/creating a project. [Candidate evidence](docs/evidence/effect-preflight-source-candidate-20261006.json) records source tests only; fixed release host acceptance is separate.

Fixed plugin dev.10 / source dev.9 installed acceptance passes: Codex discovers all 58 skills with zero loading errors; all 13 Effect skills cold-install the public CLI and reject invalid plans before installation/editing; four temporal/sequence/Film-handoff regressions and the 13-test Effect domain matrix pass with zero skips. All installed skill hashes remain unchanged. [Version-bound evidence](docs/evidence/codex-effectcraft10-preflight-first-use-20261006.json). Art domain bundle upgrade, actual Skills CLI installation and complete V1 remain open.

Working-tree segmented producer candidate: bounded native ranges, hash-bound recovery and per-frame checks; fixed plugin and Film/Art consumption remain pending. [Architecture](docs/EffectCraft-Segmented-Render-Architecture.md).

Current-source HD segmented candidate passes 1080p / 24 fps / five seconds and animated-title checks; immutable installed releases and Art HD remain pending. [Architecture and evidence](docs/EffectCraft-HD-Sequence-Architecture.md).

Immutable plugin release candidate 0.1.0-dev.11 pins skill source 0.1.0-dev.10, including HD segmented workflows and pixel verification optimization. Actual installed first-use acceptance remains pending.

Public-workflow reply validation is synchronized in the domain source candidates and has bounded native/Art protocol evidence. Fixed updated domain and Art distributions are still pending. [Candidate architecture](docs/EffectCraft-Complete-Commands-Architecture.md) · [Evidence](docs/evidence/public-workflow-session-candidate-20261007.json).

Failed-stage candidate: public workflows retain original native staging paths, dependency hashes, last submitted requests and completed receipts; replay is prohibited. Fixed releases and installed-host acceptance remain open. [Architecture](docs/EffectCraft-Failed-Stage-Architecture.md).

Fixed domain failed-stage first use passes: Film plugin18/source16 and other domain plugins17/source15; five plugins/58 skills without loading errors; all58 independent empty-runtime CLI starts (417.646s); actual installed24 post-save faults reopen product-retained original projects and dependencies; four healthy native creation/revision cases pass. All installed identities and16 fixed plugin CI runs pass. Source repositories have no CI runs, only local regression. Only domain OpenSpec3.12 closes; Art77 bundles older domain sources, task4.9 and fullV1 remain open. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

Fixed installed scene matrix passes37 native scenarios and6 contract checks with zero skips. The Photo fixture now resolves the maintained native version from the installed skill lock; the CLI and installed skills are unchanged. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


Candidate complete-command inner JSON fix: nonfinite values, overflow and duplicate keys now retain unknown receipts before binding results. All nine real post-save fault classes pass with original reopen; this is candidate-source evidence, fixed releases and installed-copy acceptance are pending. Complete per-command/GUI acceptance stays open.

Parenting/expression:13 independent source-candidate cold native runs pass dynamic alpha, save/reopen and source revision; fixed install and Art distribution pending. [Architecture](docs/EffectCraft-Expression-Parent-Architecture.md).

Fixed parent/expression first use:13 independently installed skills pass dynamic alpha and source revision; all58 installed identities unchanged. Updated Art distribution remains pending. [Evidence](docs/evidence/codex-effectcraft-expression-first-use-20261007.json).

## Desktop installation component (source candidate)

The 48 standalone domain skills now have their own pinned official desktop installers. See the [installation architecture](docs/Craft-Desktop-First-Use-Architecture.md) and [48-skill installation evidence](docs/evidence/craft-desktop-source48-first-use-20261007.json). Existing release-tag skill copies do not yet contain this candidate component. Desktop startup, GUI edits/save/reopen and complete command execution remain open acceptance gates.

Source candidate now includes owned standalone desktop startup: 48/48 single-skill cold GUI save/reopen and cleanup cases passed. See [runtime evidence](docs/evidence/craft-owned-desktop-first-use-20261007.json). Fixed-release installation and complete command execution remain open.

Command-plan JSON source candidate: duplicate keys are rejected before installation and output creation. All 15 domain skills pass standalone-copy rejection and valid-plan checks. Three focused tests pass; fixed-plugin publication and installed acceptance remain NOT_RUN. [Evidence](docs/evidence/command-plan-json-candidate-20261007.json).

Fixed strict-plan installed verification passes: 64 CLI probes, 324 duplicate-key rejections across54 independently copied installed domain skills, 54 unique-plan structure checks and four cold native save/reopen/render samples. All64 installed skill hashes remain unchanged. Only the bounded strict-plan publication gate closes; generic Skills CLI, Art domain-bundle upgrade, exhaustive contexts and fullV1 remain open. [Evidence](docs/evidence/command-plan-json-fixed-first-use-20261007.json).

Scenario installation examples now name the loaded skill itself. Source paths/layout checks pass; fixed installed runtime acceptance is recorded separately. [Architecture / 架构](docs/Scenario-Own-Path-Architecture.md).

Fixed installed own-directory acceptance passes for the updated scenario skills; 64 host identities match. Complete V1 remains open. [Evidence / 证据](docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).

Puppet recording/follow source candidate: ten representative commands, frame-aligned keys, native reopen, targeted revision and three rejection paths pass. Immutable installed-release acceptance remains separate. [Architecture](docs/EffectCraft-Puppet-Record-Follow-Architecture.md).

Fixed EffectCraft plugin dev.35 / source dev.33 acceptance passes: 64 installed skill identities/discovery, 15 fresh standalone Effect CLI installs, and native puppet recording/follow/reopen/targeted revision plus three failure paths. The other 49 cold records are historical and byte-identical. Full V1 stays open. [Fixed evidence](docs/evidence/effectcraft-puppet-record-follow-fixed-first-use-20261008.json).

Camera scene source candidate passes native Advanced 3D rendering, projection growth, reopen identity, camera-only revision and three rejection paths. [Architecture](docs/EffectCraft-Camera-Scene-Architecture.md). Fixed installed-release acceptance remains separate; full V1 stays open.

Fixed EffectCraft plugin dev.36 / source dev.34 passes 64 installed skill identities/discovery, 15 fresh standalone Effect CLI cold installs, and the native camera render/reopen/targeted revision plus three rejection paths. The other 49 cold records are retained byte-identical historical runs. Full V1 remains open. [Fixed camera evidence](docs/evidence/effectcraft-camera-scene-fixed-first-use-20261008.json).

Fixed installation boundary qualification: all 64 current standalone skills pass 128 real unavailable-archive cases through their own bootstrap and CLI entries. Errors retain each skill’s local setup path without retry or native launch; source/copied skill hashes stay unchanged. Four domain SK-002 requirements qualify against the exact lock; Art SK-002 and generic Skills CLI installation remain open. Historical CLI red cases were reconstructed now, rather than treated as old runs. [Evidence](docs/evidence/craft-fixed-setup-boundary-20261008.json).

Public protocol authority is pinned to ArtCraft v0.1.0-dev.109: [reference and verification](docs/Craft-Protocol-Authority.md). This validates the source contract; full runtime protocol acceptance remains open.

Previously verified fixed protocol-reference release matrix (Film/Effect dev.37, Photo dev.36, Vector dev.34, Art dev.107) passes actual isolated Codex installation/discovery of 64 skills, 16 installed authority-file digest checks, and 64 independent public CLI probes using five fresh domain caches. Historical native scene proof is reused only for byte-identical skills; full V1 remains open. [Fixed release evidence](docs/evidence/craft-protocol-authority-fixed-first-use-20261008.json).

This plugin pins protocol authority to ArtCraft dev.109 and retains its locked standalone skill source. Actual installation of the updated matrix is being verified; complete V1 and runtime protocol acceptance remain open.

Fixed releases Film38/Effect38/Photo37/Vector35/Art109 pass actual isolated Codex installation/discovery of 64 skills, 16 installed protocol file digests, and 64 CLI probes using five fresh domain caches. Each of ten Art skills freshly passes its own empty-public-runtime native Photo mask/adjustment creation, source revision and moved package verification. The remaining 54 skills reuse historical native proof only when the entire skill hash matches. Maintainer defaults now select this matrix; generic Skills CLI installation, model dispatch, GUI and complete V1/protocol acceptance remain open. [Fixed evidence](docs/evidence/craft-archive-prefix-fixed-first-use-20261008.json).
