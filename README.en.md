<div align="center">

# Full AIGC Plugins

**11 plugins. The full AIGC pipeline. One unified ecosystem.**

*Image · Video · Audio · Music · 3D · Multimodal — production-grade, independently installable on Codex / ZCode / Kimi.*

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![Platforms](https://img.shields.io/badge/hosts-Codex%20%C2%B7%20ZCode%20%C2%B7%20Kimi-blue)](#install)
[![Plugins](https://img.shields.io/badge/plugins-11-green)](#plugin-catalog)

[简体中文](./README.md)

[About](#about) ·
[Install](#install) ·
[Plugin Catalog](#plugin-catalog) ·
[Architecture](#architecture) ·
[Ecosystem](#ecosystem) ·
[Contributing](#contributing)

</div>

## Plugin marketplaces

The marketplaces are organized by purpose. Each marketplace lists links to its plugin repositories.

| Category | Marketplace | Purpose |
| --- | --- | --- |
| Full-stack development | [Full Stack Plugins](https://github.com/partme-ai/full-stack-plugins) | Architecture and UI design, code understanding, quality checks, code review, workflow governance, and server operations |
| AIGC content creation | [Full AIGC Plugins](https://github.com/partme-ai/full-aigc-plugins) | Image, video, audio, music, 3D, and multimodal content creation |

---

## About

**Full AIGC Plugins** is the plugin marketplace for AI-generated content (AIGC), covering image generation, video creation, audio/music, 3D production, and multimodal workflows, across the Codex, ZCode, and Kimi Code host platforms.

This repository is the plugin-side counterpart of [Full AIGC Skills](https://github.com/partme-ai/full-aigc-skills): the skills side captures domain knowledge ("how to think"), while the plugin side ships executable capability ("what you can do") — MCP tools, generation pipelines, and approval/verification gates. Both follow the same domain layout within one ecosystem.

> This repository contains marketplace metadata only (catalog and per-platform manifests), not plugin runtime code. Each plugin is maintained in its own repository, aligned by `catalog.json` as the single source of truth for IDs, names, versions, categories, and repository addresses.

### Coverage

| Domain | Problem | Solution (plugins) |
|--------|---------|--------------------|
| **Image generation** | Text-to-image, batch production, quality evaluation | image-factory, dreamina-design, comfy-design |
| **Video creation** | Text/image-to-video, editing to final cut | minimax-design, video-factory, jianying-edit, volcengine-design |
| **3D production** | Scene building, previs, rendering | blender-design, maya-design |
| **Multimodal workflows** | Node canvases, structured orchestration | dreamina-canvas, comfy-design, volcengine-design |
| **Film production planning** | Story → shot list → storyboard | partme-cine-planning (planning repo, unreleased) |

---

## Install

### Codex

```bash
codex plugin marketplace add partme-ai/full-aigc-plugins
codex plugin add blender-design@full-aigc-plugins
codex plugin add comfy-design@full-aigc-plugins
codex plugin add content-factory@full-aigc-plugins  # RC preview, testing only
codex plugin add dreamina-canvas@full-aigc-plugins
codex plugin add dreamina-design@full-aigc-plugins
codex plugin add image-factory@full-aigc-plugins
codex plugin add jianying-edit@full-aigc-plugins
codex plugin add maya-design@full-aigc-plugins
codex plugin add minimax-design@full-aigc-plugins
codex plugin add video-factory@full-aigc-plugins
codex plugin add volcengine-design@full-aigc-plugins
```

### ZCode

Open Settings → Plugins → Create → Add plugin marketplace, enter `partme-ai/full-aigc-plugins`, then install from the personal marketplace section.

### Kimi Code CLI

```text
/plugins marketplace https://raw.githubusercontent.com/partme-ai/full-aigc-plugins/main/kimi-marketplace.json
```

---

## Plugin Catalog

The plugins below belong to **AIGC**. Open a plugin name or repository link for its documentation; use the marketplace links above for the other category.

| Plugin | ID | Version | Focus | Repository |
|--------|----|:-------:|-------|------------|
| [🧱 **Blender Production**](https://github.com/full-aigc-plugins/blender-design-plugin) | `blender-design` | 0.15.0 | Controlled Blender production with a four-tab workbench, provider capabilities, visual milestones, and recovery checkpoints; adds `blender-ai-replication` (LLM + VLM critic reference-image replication) | [blender-design-plugin](https://github.com/full-aigc-plugins/blender-design-plugin) |
| [🎞️ **Comfy Generation**](https://github.com/full-aigc-plugins/comfy-design-plugin) | `comfy-design` | 0.5.0 | Comfy Cloud generation workflows (image / video / audio / 3D) | [comfy-design-plugin](https://github.com/full-aigc-plugins/comfy-design-plugin) |
| [🧪 **Content Factory (RC)**](https://github.com/full-aigc-plugins/content-factory-plugin) | `content-factory` | 1.0.0-rc.2 | Governed creation, review, formatting, and export for 16 channels; preview testing only, not production-ready | [content-factory-plugin](https://github.com/full-aigc-plugins/content-factory-plugin) |
| [🎨 **Dreamina Canvas**](https://github.com/full-aigc-plugins/dreamina-canvas-plugin) | `dreamina-canvas` | 0.4.2 | Build and run structured Dreamina canvases and timelines (approval-aware, recoverable) | [dreamina-canvas-plugin](https://github.com/full-aigc-plugins/dreamina-canvas-plugin) |
| [🖼️ **Dreamina Design**](https://github.com/full-aigc-plugins/dreamina-design-plugin) | `dreamina-design` | 0.7.0 | Create images and videos with Dreamina | [dreamina-design-plugin](https://github.com/full-aigc-plugins/dreamina-design-plugin) |
| [🏭 **Image Factory**](https://github.com/full-aigc-plugins/image-factory-plugin) | `image-factory` | 0.8.0 | Discover, batch-produce, and evaluate images | [image-factory-plugin](https://github.com/full-aigc-plugins/image-factory-plugin) |
| [✂️ **JianYing Edit**](https://github.com/full-aigc-plugins/jianying-edit-plugin) | `jianying-edit` | 0.27.9 | Rust-only JianYing workflow orchestration and editable drafts | [jianying-edit-plugin](https://github.com/full-aigc-plugins/jianying-edit-plugin) |
| [🎬 **Maya Production**](https://github.com/full-aigc-plugins/maya-design-plugin) | `maya-design` | 0.1.5 | Inspect Maya scenes, create reversible Playblasts, produce verified Jimeng links | [maya-design-plugin](https://github.com/full-aigc-plugins/maya-design-plugin) |
| [🎵 **MiniMax Design**](https://github.com/full-aigc-plugins/minimax-design-plugin) | `minimax-design` | 0.4.3 | Generate H3 videos with MiniMax — white-model first/last-frame anchoring | [minimax-design-plugin](https://github.com/full-aigc-plugins/minimax-design-plugin) |
| [🎥 **Video Factory**](https://github.com/full-aigc-plugins/video-factory-plugin) | `video-factory` | 0.4.0 | Edit, compose, review, and verify videos | [video-factory-plugin](https://github.com/full-aigc-plugins/video-factory-plugin) |
| [🌋 **Volcengine Design**](https://github.com/full-aigc-plugins/volcengine-design-plugin) | `volcengine-design` | 0.1.2 | Doubao ASR/TTS plus image and video generation workflows | [volcengine-design-plugin](https://github.com/full-aigc-plugins/volcengine-design-plugin) |
| [🔮 **Xuanji Metaphysics**](https://github.com/full-aigc-plugins/xuanji-plugin) | `xuanji` | 0.1.1 | Entertainment-oriented Chinese metaphysics and tarot workflows with bounded AIGC visualization | [xuanji-plugin](https://github.com/full-aigc-plugins/xuanji-plugin) |

> The planning repository [`cine-planning`](https://github.com/full-aigc-plugins/cine-planning) (`director` / `script` / `storyboard`, specifications only) is tracked by this marketplace under the `design_baseline_not_released` status and stays out of every installable manifest until its own release boundary is complete.

> The candidate plugin [`content-factory-plugin`](https://github.com/full-aigc-plugins/content-factory-plugin) remains independently governed in `candidatePlugins`. Version `1.0.0-rc.2` is exposed to Codex, ZCode, and Kimi as `release_candidate_installable` for controlled test installation; its production release gate remains `BLOCKED`, so it is neither production-ready nor a stable release.

---

## Architecture

### How the marketplace works

`catalog.json` is the single source of truth. `scripts/sync-marketplaces.mjs` generates the three platform manifests from it and validates each plugin repository's skills directories (frontmatter, naming consistency), explicit candidate state (hidden blocked or installable RC), immutable release identity, and planning-repo constraints (no published manifests):

```
full-aigc-plugins/
├── catalog.json                        # Single source of truth: IDs / names / versions / categories / repos
├── .agents/plugins/marketplace.json    # Codex manifest (generated)
├── marketplace.json                    # ZCode manifest (generated)
├── kimi-marketplace.json               # Kimi manifest (generated)
└── scripts/                            # Sync and release tooling
```

Each independent plugin repository owns its runtime adapters: `.codex-plugin/plugin.json`, `.zcode-plugin/plugin.json`, and `kimi.plugin.json`.

`scripts/sync-release-tooling.mjs` only creates a missing `AGENTS.md` by default and preserves
repository-specific instructions. Existing templates are refreshed only with the explicit
`--refresh-agents` flag; use `--dry-run` to inspect the affected files first.

### Progressive disclosure

Skills inside plugins follow the [Agent Skills specification](https://agentskills.io):

1. **At startup**: only skill names and descriptions are loaded (minimal context)
2. **On demand**: the full `SKILL.md` loads when the agent recognizes a relevant task
3. **In depth**: reference files are read only when explicitly needed

---

## Ecosystem

| Resource | Link |
|----------|------|
| **Skills hub (AIGC)** | [partme-ai/full-aigc-skills](https://github.com/partme-ai/full-aigc-skills) |
| **Skill packages org (AIGC)** | [github.com/full-aigc-skills](https://github.com/full-aigc-skills) |
| **Dev-side plugin marketplace** | [github.com/full-stack-plugins](https://github.com/partme-ai/full-stack-plugins) |
| **Skills hub (full stack)** | [partme-ai/full-stack-skills](https://github.com/partme-ai/full-stack-skills) |
| **Agent Skills specification** | [agentskills.io](https://agentskills.io) |
| **Skills CLI** | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) |
| **PartMe.AI** | [github.com/partme-ai](https://github.com/partme-ai) |

---

## Contributing

### Release discipline

Any plugin code change (no matter the size) requires a version bump and release; marketplaces detect updates by version number:

```bash
node scripts/bump-plugin.mjs <plugin-id> <major|minor|patch>
```

The command updates the catalog version, syncs the four manifests in the plugin repository, and regenerates the three platform manifests.

### Adding a plugin

1. Build the plugin in its own repository with the three-platform adapter layer (`.codex-plugin` / `.zcode-plugin` / `kimi.plugin.json`)
2. Register the entry in `catalog.json`
3. Run `node scripts/sync-marketplaces.mjs --write` to regenerate manifests, then commit

---

## License

Apache 2.0 — see [LICENSE](LICENSE).

---

<div align="center">

**If this project helps you, please give us a ⭐️**

Made with ❤️ by PartMe.AI Team

</div>
