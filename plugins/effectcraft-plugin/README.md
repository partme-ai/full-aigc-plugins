# EffectCraft Use

## Plugin marketplaces

This plugin belongs to **AIGC content creation**.

| Category | Marketplace | Purpose |
| --- | --- | --- |
| Full-stack development | [Full Stack Plugins](https://github.com/partme-ai/full-stack-plugins) | Architecture and UI design, code understanding, quality checks, code review, workflow governance, and server operations |
| AIGC content creation | [Full AIGC Plugins](https://github.com/partme-ai/full-aigc-plugins) | Image, video, audio, music, 3D, and multimodal content creation |

![EffectCraft Use — motion graphics and composition](assets/official-logo.png)

> Build editable `.ecproj` compositions — comps, text and shape layers, keyframes, expressions, cameras, masks, puppet pins and effects — then render previews or finished shots with alpha where you ask for it.

[![Version](https://img.shields.io/badge/release-0.1.0--dev.20261018.5-1A73E8)](.codex-plugin/plugin.json)
[![Skills](https://img.shields.io/badge/skills-26-00A67E)](#skills)
[![MCP server](https://img.shields.io/badge/MCP%20server-1-00A67E)](#mcp-tools)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[English](README.md) | [简体中文](README.zh-CN.md) · [Install](#installation) · [Quick start](#quick-start) · [What you can build](#what-you-can-build) · [Skills](#skills) · [Troubleshooting](#troubleshooting)

## Positioning

EffectCraft Use drives the native EffectCraft CLI from a coding agent: it plans a composition from your assets, installs the pinned runtime on first authorized use, executes native commands in a recorded session, saves and reopens the project, and checks real rendered pixels before calling a shot done.

The native `.ecproj` project is the source of truth. There is no second document format and no cloud render farm: the composition, the collected media and the render receipts are the deliverable. Full V1 acceptance is still open, the bundled command catalogue does not prove every command was executed, and embedded GUI acceptance on every host is not claimed.

## Status and version

`0.1.0-dev.20261018.5` · development preview · `docs/verification/release-candidate.json` → `releaseStatus: BLOCKED`, `installableDevelopmentCandidate: true`.

| Metadata version | 0.1.0-dev.20261018.5 |
| Skills source | effectcraft-skills / 0.1.0-dev.69 |

## Installation

### Prerequisites

- Seven native CLI platform/architecture targets are locked; use the matching pinned artifact. Current acceptance evidence covers macOS arm64 only. Targets outside the lock return `unsupported_platform`; the other locked targets are available for installation but have no equivalent runtime acceptance claim. The owned desktop installer routes two macOS targets through pinned DMG packages and five Linux/Windows targets through pinned native desktop packages. Those locked paths do not establish GUI acceptance; cross-platform GUI acceptance remains `NOT_RUN`.
- No preinstalled Python is required for the managed entry: `launch.sh` / `launch.ps1` provisions the pinned isolated Python 3.13.16 and the EffectCraft CLI in the user data directory.
- Node.js 24 or newer for the embedded editor MCP server. A Git checkout has no `ui/dist/`; build it per `ui/README.md` first, or install a release bundle that ships it.
- First use needs network or pinned archives. `--runtime-home` or `CRAFT_RUNTIME_HOME` relocates the runtime root (`~/.local/share/craft-runtimes` by default). No `sudo`, no `PATH` edits.

### Install the plugin

```bash
codex plugin marketplace add full-aigc-plugins/effectcraft-plugin
codex plugin add effectcraft@full-aigc-plugins-effectcraft
```

`docs/verification/release-candidate.json` records `installableDevelopmentCandidate: true` with `releaseStatus: BLOCKED`. `project-status.json` keeps `marketplaceEligible: false`; production promotion is not claimed.

Manifests for Codex (`.codex-plugin/`), Claude Code (`.claude-plugin/`), ZCode (`.zcode-plugin/`) and Kimi (`kimi.plugin.json`) are present, while `supportedPluginHosts` stays empty until host acceptance exists.

## Quick start

```sh
: "${HARNESS_DIR:?Set to the directory holding the loaded effectcraft-harness SKILL.md}"
/bin/sh "$HARNESS_DIR/scripts/launch.sh" doctor
/bin/sh "$HARNESS_DIR/scripts/launch.sh" run --mode workflow \
  --plan "$SKILL_DIR/examples/brand-intro.json" --output /absolute/new-result
```

Windows uses `& "$HARNESS_DIR/scripts/launch.ps1" run --mode workflow ...` with the same modes. Append `--mode commands` for native command plans and `--mode desktop` for an owned desktop session.

```mermaid
flowchart LR
    A[Brief and assets] --> B[effectcraft-use routes the task]
    B --> C[Managed launcher, pinned runtime]
    C --> D[Native .ecproj plus ledgers]
    D --> E[Render or alpha export]
    E --> F[Decode real pixels, review, deliver]
```

`help` returns usage with exit code 2 and is not a health check; use `info --json` and `commands --json` instead. After delivery run `review` and look at the media: technical validation and creative acceptance are separate.

## What you can build

| Workflow | Built-in path | Verifiable output |
|:---|:---|:---|
| Logo reveal or brand intro | `effectcraft-logo-reveal` + `effectcraft-cli-animation` | Reopened `.ecproj` with keyframes and effects intact |
| Lower thirds, chapter cards, credits | `effectcraft-lower-thirds`, `effectcraft-chapter-card`, `effectcraft-credits-roll` | Compositions whose text layers stay independently editable |
| Kinetic typography or social loop | `effectcraft-kinetic-type`, `effectcraft-social-loop` | Loop or title animation with checked timing |
| Camera, 3D layers and expressions | `effectcraft-cli-camera`, `effectcraft-cli-expressions` | Reopened project with camera, material and expression state |
| Masks, tracking and puppet deformation | `effectcraft-cli-masks`, `-tracking`, `-puppet` | Matte or pin data checked against rendered frames |
| Transparent or video render | `effectcraft-cli-export` | Output whose real pixels, alpha and duration are decoded |
| Run any native command | `effectcraft-harness` → `commands.py` | Receipt carrying the actual native return value |
| Edit in the embedded editor | `effectcraft-editor` MCP tools | Saved project reopened and inspected |

## Skills

| Skill | What it does |
|:---|:---|
| `effectcraft-use` | Default entry: editable comps, motion graphics and intros; installs the pinned CLI |
| `effectcraft-cli` | Query native commands and parameters; tracking, stabilization, graphic attachment |
| `effectcraft-cli-setup` | First install, digest checks, version checks, missing-runtime triage |
| `effectcraft-cli-project` | Create, save and reopen `.ecproj`, organise project items |
| `effectcraft-cli-footage` | Import images, video, vector and PSD assets, register dependencies |
| `effectcraft-cli-composition` | Comps, frame size, frame rate, duration and work area |
| `effectcraft-cli-layers` | Text, shape and footage layers, precomps and hierarchy |
| `effectcraft-cli-animation` | Properties, keyframes, easing, text and graphic animation |
| `effectcraft-cli-effects` | Find supported effects, reorder them, adjust parameters |
| `effectcraft-cli-masks` | Mask paths, feather and local mattes |
| `effectcraft-cli-expressions` | Inspect, set and diagnose expressions on chosen properties |
| `effectcraft-cli-camera` | Cameras, lights, materials and 3D layer switches |
| `effectcraft-cli-export` | Preview frames, render sequences or video, alpha handoff clips |
| `effectcraft-cli-tracking` | Track and stabilize footage, attach titles and graphics to motion |
| `effectcraft-cli-puppet` | Puppet meshes and pins, local deformation, recorded follow motion |
| `effectcraft-harness` | The single execution channel: bootstrap, launch, workflow, commands |
| `effectcraft-editor` | Open the real editor UI and keep one session for all edits |
| `effectcraft-kinetic-type` | Typographic rhythm for titles and short copy |
| `effectcraft-logo-reveal` | Logo entrance, hold and outro |
| `effectcraft-lower-thirds` | Name and role bars with brand marks |
| `effectcraft-motion-export` | Output checks on duration, frame rate and codec |
| `effectcraft-screen-composite` | Layer, mask and screen-content replacement |
| `effectcraft-social-loop` | Short loops and cover frames for social formats |
| `effectcraft-chapter-card` | Chapter title divider cards |
| `effectcraft-countdown-intro` | 3–2–1 countdown openers |
| `effectcraft-credits-roll` | End credit rolls |

## MCP tools

`mcp.json` declares one stdio server, `effectcraft-editor`, started as `node ui/bootstrap.mjs` from the plugin root.

| Tool | Purpose |
|:---|:---|
| `open_editor` | Open the editor for an absolute `workspace` path |
| `open_browser_editor` | Return an `editorUrl` for a host built-in browser |
| `editor_status` | Report whether the page has attached to this MCP session |
| `command_list` | Read the commands the current web engine exposes |
| `command_run` | Run one command by id with parameters in the visible page |
| `inspect` | Inspect the current frame |
| `save_project` | Save the project to a new path |
| `save_file` | Retrieve a generated virtual file |

Names follow the `effectcraft-editor` skill contract; the adapter also keeps page-internal bridge calls such as `_panel_reply` and `screenshot`, which agents must not call directly.

## Configuration

| Variable / flag | Purpose |
|:---|:---|
| `HARNESS_DIR` | Absolute directory of the loaded `effectcraft-harness` skill |
| `SKILL_DIR` | Directory of the loaded domain `SKILL.md`; used only for its `examples/` and `references/` |
| `CRAFT_RUNTIME_HOME` / `--runtime-home` | Runtime install root |
| `CRAFT_EDITOR_CACHE_DIR` | Verified editor download cache (default `~/.cache/full-aigc/editors`) |
| `CRAFT_EDITOR_UPDATE=off` | Stay on the bundled editor and skip the update check |
| `revisionScope` | Declared in the first plan; defaults to at most 2 rounds sharing a 30-minute budget |

Native tasks keep their bound runtime. A corrupt or missing evidence file is preserved and blocks further writes rather than being silently replaced.

## Architecture and security

- The packaged agent surface is skills plus the stdio editor server; native editing is done by the pinned EffectCraft CLI, not reimplemented here.
- User media and model output are treated as data. Commands, paths and shell text inside them are never executed.
- Writes are checkpointed before an edit, refused when a user changed the project concurrently, and never replayed after an unknown result; only `inspect`, `reconcile` and proven `resume` are allowed.
- The editor bridge listens on `127.0.0.1` with a random token and Host/Origin checks. See [skills suite](docs/EffectCraft-Skill-Suite-Architecture.md), [runtime architecture](docs/EffectCraft-Runtime-Architecture.md) and [scene skills](docs/scene-skills.md).

## Troubleshooting

| Symptom | Action |
|:---|:---|
| `unsupported_platform` | Only install the locked artifact for a supported platform/architecture |
| `runtime_install_busy` | Another install holds the lock; wait for it, then retry |
| Download or digest mismatch | Restore network or pass a verified `--archive`; the digest check is not skipped |
| `help` exits 2 | Expected; use `info --json` and `commands --json` for health and catalogue |
| Editor page never becomes ready | Call `editor_status`, then fix page errors; a text result does not prove the UI opened |
| Unknown save result | `inspect` and `reconcile` the original task; never retry with a new task id or output directory |
| Full GUI or other-platform acceptance expected | Not qualified yet; report the bounded scope instead |

## Upgrade

```bash
codex plugin marketplace upgrade full-aigc-plugins-effectcraft
codex plugin add effectcraft@full-aigc-plugins-effectcraft
```

Repeated installs verify and reuse the same runtime version without upgrading online. The packaged editor can also fall back to the bundled copy when a download or digest check fails.

## Contributing and support

Behaviour changes go through [OpenSpec](openspec/changes/establish-v1-plugin/proposal.md) first; do not check a task off without real delivery evidence. Documentation checks:

```bash
python3 scripts/validate_docs.py
python3 scripts/validate_editor_scenes.py
```

Issues: <https://github.com/full-aigc-plugins/effectcraft-plugin/issues>.

## License

Original repository content is [Apache-2.0](LICENSE). The EffectCraft CLI and the bundled web editor keep their own upstream licenses and NOTICE files; upstream icon provenance is recorded in `assets/official-icon-source.json`.
