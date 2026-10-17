<div align="center">

Craft 插件的 `plugins/` 为固定独立仓发行提交生成的 Codex 分发快照，保证安装前图标可读；技能及代码仍在各独立插件仓维护，不在目录仓手工修改快照。

## Craft 可安装开发候选

13 个 Craft 编辑器候选按应用固定到 `0.1.0-dev.20261017.5` 或 `0.1.0-dev.20261017.6` 或 `0.1.0-dev.20261017.7`，名称为 `PhotoCraft Use (RC)` 等，使用官方图标。它们是开发预发布；生产与全部场景验收尚未完成。安装要求 Node.js 24。Git 安装首次启动会下载固定摘要的编辑器资源；完整发行 ZIP 自带资源。详见 [安装与验证状态](docs/craft-marketplace-release.md)。 交付参考 ZCode 的已构建 ZIP 分发方式：支持该协议的宿主绑定完整包、摘要和包内目录。当前 EffectCraft 超出 ZCode 单文件解包上限，显式使用 Git 入口兼容；Codex 原生 Git 入口单独验收。


# Full AIGC Plugins

**11 个插件。AIGC 全链路。一个统一生态。**

*图像 · 视频 · 音频 · 音乐 · 3D · 多模态 — 生产级品质，多宿主插件与技能集成。*

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![Platforms](https://img.shields.io/badge/hosts-Agent%20Plugins-blue)](#安装)
[![Plugins](https://img.shields.io/badge/plugins-11-green)](#插件目录)

[English](./README.en.md)

[简介](#简介) ·
[生态](#生态) ·
[安装](#安装) ·
[插件目录](#插件目录) ·
[架构](#架构) ·
[贡献](#贡献指南)

</div>

---

## 简介

**Full AIGC Plugins** 是面向 AI 生成内容（AIGC）的插件市场，覆盖图像生成、视频创作、音频/音乐、3D 制作与多模态工作流，面向 支持插件的宿主平台。

本仓库与技能侧的 [Full AIGC Skills](https://github.com/partme-ai/full-aigc-skills) 对位：技能侧沉淀「怎么想」的领域知识（提示词工程、工作流方法论），插件侧提供「能做到」的可执行能力（MCP 工具、生成流水线、审批与校验门禁）。两者按同一套领域划分共建同一个生态。

> 本仓库只包含市场元数据（catalog 与三平台清单），不包含插件运行时代码。每个插件在各自独立仓库中维护，通过 `catalog.json` 单一事实源对齐 ID、名称、版本、分类与仓库地址。

### 覆盖领域

| 领域 | 问题 | 解决方案（插件） |
|------|------|------------------|
| **图像生成** | 文生图、批量生产、质量评估 | image-factory、dreamina-design、comfy-design |
| **视频创作** | 文生视频、图生视频、剪辑成片 | minimax-design、video-factory、jianying-edit、volcengine-design |
| **3D 制作** | 场景搭建、预演、渲染出图 | blender-design、maya-design |
| **多模态工作流** | 节点画布、结构化编排 | dreamina-canvas、comfy-design、volcengine-design |
| **影视制片规划** | 故事 → 镜头表 → 分镜 | cine-planning（规划仓，未发布） |

---

## 生态

<!-- ecosystem-navigation:start -->

| 方向 | 适用任务 | 目录与安装 | 组织 |
| --- | --- | --- | --- |
| Full Stack Skills | 软件开发、架构设计、测试与运维 | [PartMe.AI / full-stack-skills](https://github.com/partme-ai/full-stack-skills) | [full-stack-skills](https://github.com/full-stack-skills) |
| Full AIGC Skills | 图像、视频、音频等内容创作 | [PartMe.AI / full-aigc-skills](https://github.com/partme-ai/full-aigc-skills) | [full-aigc-skills](https://github.com/full-aigc-skills) |
| Full Stack Plugins | 研发与运维的工具集成和工作流 | [PartMe.AI / full-stack-plugins](https://github.com/partme-ai/full-stack-plugins) | [full-stack-plugins](https://github.com/full-stack-plugins) |
| Full AIGC Plugins | 内容制作的工具集成和生成工作流 | [PartMe.AI / full-aigc-plugins](https://github.com/partme-ai/full-aigc-plugins) | [full-aigc-plugins](https://github.com/full-aigc-plugins) |

<!-- ecosystem-navigation:end -->

### 相关资源

| 资源 | 链接 |
|------|------|
| **Agent Skills 规范** | [agentskills.io](https://agentskills.io) |
| **Skills CLI** | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) |
| **PartMe.AI** | [github.com/partme-ai](https://github.com/partme-ai) |

---

## 安装

### Codex

```bash
codex plugin marketplace add partme-ai/full-aigc-plugins
codex plugin add blender-design@full-aigc-plugins
codex plugin add comfy-design@full-aigc-plugins
codex plugin add content-factory@full-aigc-plugins  # RC 预览，仅用于测试
codex plugin add dreamina-canvas@full-aigc-plugins
codex plugin add dreamina-design@full-aigc-plugins
codex plugin add image-factory@full-aigc-plugins
codex plugin add jianying-edit@full-aigc-plugins
codex plugin add maya-design@full-aigc-plugins
codex plugin add minimax-design@full-aigc-plugins
codex plugin add printcraft@full-aigc-plugins  # 开发预发布，仅用于受控测试
codex plugin add video-factory@full-aigc-plugins
codex plugin add volcengine-design@full-aigc-plugins
```

### ZCode

打开 设置 → 插件 → 创建 → 添加插件市场，输入 `partme-ai/full-aigc-plugins`，然后在个人市场分区中安装。

### Kimi Code CLI

```text
/plugins marketplace https://raw.githubusercontent.com/partme-ai/full-aigc-plugins/main/kimi-marketplace.json
```

---

## 插件目录

以下为 **AIGC** 插件；点击插件名称或仓库链接查看各插件文档，另一分类请使用上方市场入口。

| 插件 | ID | 版本 | 定位 | 仓库 |
|------|----|:----:|------|------|
| [**CADCraft Use (RC)**](https://github.com/full-aigc-plugins/cadcraft-plugin) | `cadcraft` | 0.1.0-dev.20261018.2 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [cadcraft-plugin](https://github.com/full-aigc-plugins/cadcraft-plugin) |
| [**DeckCraft Use (RC)**](https://github.com/full-aigc-plugins/deckcraft-plugin) | `deckcraft` | 0.1.0-dev.20261018.2 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [deckcraft-plugin](https://github.com/full-aigc-plugins/deckcraft-plugin) |
| [**DesignCraft Use (RC)**](https://github.com/full-aigc-plugins/designcraft-plugin) | `designcraft` | 0.1.0-dev.20261018.2 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [designcraft-plugin](https://github.com/full-aigc-plugins/designcraft-plugin) |
| [**EffectCraft Use (RC)**](https://github.com/full-aigc-plugins/effectcraft-plugin) | `effectcraft` | 0.1.0-dev.20261018.3 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [effectcraft-plugin](https://github.com/full-aigc-plugins/effectcraft-plugin) |
| [**FigCraft Use (RC)**](https://github.com/full-aigc-plugins/figcraft-plugin) | `figcraft` | 0.1.0-dev.20261018.2 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [figcraft-plugin](https://github.com/full-aigc-plugins/figcraft-plugin) |
| [**FilmCraft Use (RC)**](https://github.com/full-aigc-plugins/filmcraft-plugin) | `filmcraft` | 0.1.0-dev.20261018.3 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [filmcraft-plugin](https://github.com/full-aigc-plugins/filmcraft-plugin) |
| [**GridCraft Use (RC)**](https://github.com/full-aigc-plugins/gridcraft-plugin) | `gridcraft` | 0.1.0-dev.20261018.2 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [gridcraft-plugin](https://github.com/full-aigc-plugins/gridcraft-plugin) |
| [**LightCraft Use (RC)**](https://github.com/full-aigc-plugins/lightcraft-plugin) | `lightcraft` | 0.1.0-dev.20261018.2 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [lightcraft-plugin](https://github.com/full-aigc-plugins/lightcraft-plugin) |
| [**PhotoCraft Use (RC)**](https://github.com/full-aigc-plugins/photocraft-plugin) | `photocraft` | 0.1.0-dev.20261018.3 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [photocraft-plugin](https://github.com/full-aigc-plugins/photocraft-plugin) |
| [**PdfCraft Use (RC)**](https://github.com/full-aigc-plugins/printcraft-plugin) | `printcraft` | 0.1.0-dev.20261017.6 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [printcraft-plugin](https://github.com/full-aigc-plugins/printcraft-plugin) |
| [**SoundCraft Use (RC)**](https://github.com/full-aigc-plugins/soundcraft-plugin) | `soundcraft` | 0.1.0-dev.20261018.1 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [soundcraft-plugin](https://github.com/full-aigc-plugins/soundcraft-plugin) |
| [**VectorCraft Use (RC)**](https://github.com/full-aigc-plugins/vectorcraft-plugin) | `vectorcraft` | 0.1.0-dev.20261017.6 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [vectorcraft-plugin](https://github.com/full-aigc-plugins/vectorcraft-plugin) |
| [**WordCraft Use (RC)**](https://github.com/full-aigc-plugins/wordcraft-plugin) | `wordcraft` | 0.1.0-dev.20261018.4 | 场景技能、stdio MCP 与同会话编辑器；开发候选，完整创作验收未完成 | [wordcraft-plugin](https://github.com/full-aigc-plugins/wordcraft-plugin) |
| [🧱 **Blender 制作**](https://github.com/full-aigc-plugins/blender-design-plugin) | `blender-design` | 0.14.1 | Blender 场景的受控设计、审阅与导出（四 Tab 工作台、供应商能力、视觉里程碑与恢复检查点）；新增 `blender-ai-replication`（LLM + VLM-critic 复刻参考图） | [blender-design-plugin](https://github.com/full-aigc-plugins/blender-design-plugin) |
| [🎞️ **Comfy 生成**](https://github.com/full-aigc-plugins/comfy-design-plugin) | `comfy-design` | 0.5.0 | Comfy Cloud 生成工作流（图像 / 视频 / 音频 / 3D） | [comfy-design-plugin](https://github.com/full-aigc-plugins/comfy-design-plugin) |
| [🧪 **内容工厂（RC）**](https://github.com/full-aigc-plugins/content-factory-plugin) | `content-factory` | 1.0.0-rc.2 | 16 渠道的受控内容创作、审阅、排版与导出；预发布测试版，非生产就绪 | [content-factory-plugin](https://github.com/full-aigc-plugins/content-factory-plugin) |
| [🎨 **即梦画布**](https://github.com/full-aigc-plugins/dreamina-canvas-plugin) | `dreamina-canvas` | 0.4.3 | 结构化 Dreamina 画布与时间线的构建和运行（带审批与恢复） | [dreamina-canvas-plugin](https://github.com/full-aigc-plugins/dreamina-canvas-plugin) |
| [🖼️ **即梦设计**](https://github.com/full-aigc-plugins/dreamina-design-plugin) | `dreamina-design` | 0.7.0 | 即梦图像与视频创作 | [dreamina-design-plugin](https://github.com/full-aigc-plugins/dreamina-design-plugin) |
| [🏭 **图片工厂**](https://github.com/full-aigc-plugins/image-factory-plugin) | `image-factory` | 0.8.0 | 图像的发现、批量生产与评估闭环 | [image-factory-plugin](https://github.com/full-aigc-plugins/image-factory-plugin) |
| [✂️ **剪映剪辑**](https://github.com/full-aigc-plugins/jianying-edit-plugin) | `jianying-edit` | 0.27.9 | Rust-only 剪映工作流编排与可编辑草稿 | [jianying-edit-plugin](https://github.com/full-aigc-plugins/jianying-edit-plugin) |
| [🎬 **Maya 制作**](https://github.com/full-aigc-plugins/maya-design-plugin) | `maya-design` | 0.1.5 | Maya 场景检查与可逆 Playblast，产出经核验的即梦链接 | [maya-design-plugin](https://github.com/full-aigc-plugins/maya-design-plugin) |
| [🎵 **MiniMax 设计**](https://github.com/full-aigc-plugins/minimax-design-plugin) | `minimax-design` | 0.4.3 | MiniMax H3 视频生成（白模首尾帧锚定） | [minimax-design-plugin](https://github.com/full-aigc-plugins/minimax-design-plugin) |
| [🎥 **视频工厂**](https://github.com/full-aigc-plugins/video-factory-plugin) | `video-factory` | 0.4.0 | 视频的剪辑、合成、审校与校验 | [video-factory-plugin](https://github.com/full-aigc-plugins/video-factory-plugin) |
| [🌋 **火山引擎设计**](https://github.com/full-aigc-plugins/volcengine-design-plugin) | `volcengine-design` | 0.1.2 | 豆包 ASR/TTS 与图像、视频生成工作流 | [volcengine-design-plugin](https://github.com/full-aigc-plugins/volcengine-design-plugin) |
| [🔮 **玄机玄学**](https://github.com/full-aigc-plugins/xuanji-plugin) | `xuanji` | 0.1.1 | 娱乐向术数六科（八字/奇门/紫微/姻缘/风水/塔罗）+ AIGC 成象（观象环 ≤3 轮） | [xuanji-plugin](https://github.com/full-aigc-plugins/xuanji-plugin) |

> 规划仓 [`cine-planning`](https://github.com/full-aigc-plugins/cine-planning)（`director` / `script` / `storyboard` 纯规格）按 `design_baseline_not_released` 状态跟随本市场管理，在自身发布边界完成前不进入任何可安装清单。

> 候选插件 [`content-factory-plugin`](https://github.com/full-aigc-plugins/content-factory-plugin) 仍由 `candidatePlugins` 独立管理。`1.0.0-rc.2` 以 `release_candidate_installable` 状态进入 现有宿主清单，可用于受控测试安装；其正式发布门禁仍为 `BLOCKED`，不得视为生产就绪或稳定版。

---

## 架构

### 市场如何工作

`catalog.json` 是唯一事实源。`scripts/sync-marketplaces.mjs` 从它生成三平台清单，并校验每个插件仓的 skills 目录（frontmatter、命名一致性）、候选插件的明确状态（隐藏阻断或 RC 测试安装）、不可变发布身份与规划仓约束（不得发布 manifest）：

```
full-aigc-plugins/
├── catalog.json                        # 单一事实源：ID / 名称 / 版本 / 分类 / 仓库
├── .agents/plugins/marketplace.json    # Codex 清单（生成物）
├── marketplace.json                    # 兼容市场清单（生成物）
├── kimi-marketplace.json               # Kimi 清单（生成物）
└── scripts/                            # 同步与发版工具
```

每个独立插件仓负责自己的运行时适配：对应宿主的插件清单；Craft 当前入口见下方便携安装说明。

`scripts/sync-release-tooling.mjs` 默认只补齐缺失的 `AGENTS.md`，不会覆盖仓库已有的项目级指令。
只有维护者明确传入 `--refresh-agents` 时才更新既有模板；`--dry-run` 可先查看影响范围。

### 渐进式披露

插件内的技能遵循 [Agent Skills 规范](https://agentskills.io)：

1. **启动时**：仅加载技能名称和描述（最小上下文）
2. **按需**：当智能体识别到相关任务时加载完整的 `SKILL.md`
3. **深入**：仅在明确需要时读取参考文件

---

## 贡献指南

### 发版纪律

任何插件代码改动（无论大小）都要 bump + 发版，市场端靠版本号感知更新：

```bash
node scripts/bump-plugin.mjs <plugin-id> <major|minor|patch>
```

该命令会同步更新 catalog 版本、插件仓四个 manifest，并重新生成三平台清单。

### 新增插件

1. 在独立仓库中按三平台适配层构建插件（标准插件清单及对应宿主适配）
2. 在 `catalog.json` 中登记条目
3. 运行 `node scripts/sync-marketplaces.mjs --write` 重新生成清单并提交

---

## 许可证

Apache 2.0 — 详见 [LICENSE](LICENSE)。

---

<div align="center">

**如果这个项目对你有帮助，请给我们一个 ⭐️**

Made with ❤️ by PartMe.AI Team

</div>

> PrintCraft 由 candidatePlugins 管理为受控测试预发布，生产门禁仍为 BLOCKED。中文 OCR、其他原生平台与移动端验收开放；可安装清单不代表全部宿主已验收。

## Craft 编辑器与场景技能候选

2026-10-16 本地候选覆盖十三种编辑器、78 个场景技能和十三个编辑器入口。接入方法与实际验证边界见 [交付说明](docs/craft-editor-delivery.md)。尚未发布，不将当前市场版本等同于本地候选。

### Craft 独立插件候选（13 款）

[源码增强接入说明](docs/craft-source-integration.md) · [独立插件与源码清单](docs/craft-plugin-map.json)。本地开发候选，不改变已发布市场的固定版本。

- **CADCraft Use**：`cadcraft-plugin`，7 个候选技能（含编辑器入口）。
- **DesignCraft Use**：`designcraft-plugin`，15 个候选技能（含编辑器入口）。
- **EffectCraft Use**：`effectcraft-plugin`，7 个候选技能（含编辑器入口）。
- **PhotoCraft Use**：`photocraft-plugin`，7 个候选技能（含编辑器入口）。
- **FigCraft Use**：`figcraft-plugin`，7 个候选技能（含编辑器入口）。
- **FilmCraft Use**：`filmcraft-plugin`，10 个候选技能（含编辑器入口）。
- **LightCraft Use**：`lightcraft-plugin`，7 个候选技能（含编辑器入口）。
- **PdfCraft Use**：`printcraft-plugin`，20 个候选技能（含编辑器入口）。
- **VectorCraft Use**：`vectorcraft-plugin`，11 个候选技能（含编辑器入口）。
- **DeckCraft Use**：`deckcraft-plugin`，7 个候选技能（含编辑器入口）。
- **SoundCraft Use**：`soundcraft-plugin`，7 个候选技能（含编辑器入口）。
- **GridCraft Use**：`gridcraft-plugin`，7 个候选技能（含编辑器入口）。
- **WordCraft Use**：`wordcraft-plugin`，14 个候选技能（含编辑器入口）。

### Craft 便携安装

当前 13 款 Craft 候选优先使用 [便携插件市场](docs/craft-portable-installation.md)，分别提供标准插件、Codex 和 Claude Code 入口。旧的逐项本机 MCP 配置不再作为推荐安装方式；当前候选不修改已发布市场版本。
