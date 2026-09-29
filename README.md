<div align="center">

# Full AIGC Plugins

**11 个插件。AIGC 全链路。一个统一生态。**

*图像 · 视频 · 音频 · 音乐 · 3D · 多模态 — 生产级品质，Codex / ZCode / Kimi 三平台独立安装。*

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![Platforms](https://img.shields.io/badge/hosts-Codex%20%C2%B7%20ZCode%20%C2%B7%20Kimi-blue)](#-安装)
[![Plugins](https://img.shields.io/badge/plugins-11-green)](#-插件目录)

[English](./README.en.md)

[简介](#-简介) ·
[安装](#-安装) ·
[插件目录](#-插件目录) ·
[架构](#-架构) ·
[生态](#-生态) ·
[贡献](#-贡献指南)

</div>

---

## 简介

**Full AIGC Plugins** 是面向 AI 生成内容（AIGC）的插件市场，覆盖图像生成、视频创作、音频/音乐、3D 制作与多模态工作流，面向 Codex、ZCode 与 Kimi Code 三个宿主平台。

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

| 插件 | ID | 版本 | 定位 | 仓库 |
|------|----|:----:|------|------|
| 🧱 **Blender 制作** | `blender-design` | 0.15.0 | Blender 场景的受控设计、审阅与导出（四 Tab 工作台、供应商能力、视觉里程碑与恢复检查点）；新增 `blender-ai-replication`（LLM + VLM-critic 复刻参考图） | [blender-design-plugin](https://github.com/full-aigc-plugins/blender-design-plugin) |
| 🎞️ **Comfy 生成** | `comfy-design` | 0.2.0 | Comfy Cloud 生成工作流（图像 / 视频 / 音频 / 3D） | [comfy-design-plugin](https://github.com/full-aigc-plugins/comfy-design-plugin) |
| 🧪 **内容工厂（RC）** | `content-factory` | 1.0.0-rc.2 | 16 渠道的受控内容创作、审阅、排版与导出；预发布测试版，非生产就绪 | [content-factory-plugin](https://github.com/full-aigc-plugins/content-factory-plugin) |
| 🎨 **即梦画布** | `dreamina-canvas` | 0.4.0 | 结构化 Dreamina 画布与时间线的构建和运行（带审批与恢复） | [dreamina-canvas-plugin](https://github.com/full-aigc-plugins/dreamina-canvas-plugin) |
| 🖼️ **即梦设计** | `dreamina-design` | 0.6.1 | 即梦图像与视频创作 | [dreamina-design-plugin](https://github.com/full-aigc-plugins/dreamina-design-plugin) |
| 🏭 **图片工厂** | `image-factory` | 0.6.0 | 图像的发现、批量生产与评估闭环 | [image-factory-plugin](https://github.com/full-aigc-plugins/image-factory-plugin) |
| ✂️ **剪映剪辑** | `jianying-edit` | 0.27.5 | Rust-only 剪映工作流编排与可编辑草稿 | [jianying-edit-plugin](https://github.com/full-aigc-plugins/jianying-edit-plugin) |
| 🎬 **Maya 制作** | `maya-design` | 0.1.5 | Maya 场景检查与可逆 Playblast，产出经核验的即梦链接 | [maya-design-plugin](https://github.com/full-aigc-plugins/maya-design-plugin) |
| 🎵 **MiniMax 设计** | `minimax-design` | 0.4.3 | MiniMax H3 视频生成（白模首尾帧锚定） | [minimax-design-plugin](https://github.com/full-aigc-plugins/minimax-design-plugin) |
| 🎥 **视频工厂** | `video-factory` | 0.3.1 | 视频的剪辑、合成、审校与校验 | [video-factory-plugin](https://github.com/full-aigc-plugins/video-factory-plugin) |
| 🌋 **火山引擎设计** | `volcengine-design` | 0.1.2 | 豆包 ASR/TTS 与图像、视频生成工作流 | [volcengine-design-plugin](https://github.com/full-aigc-plugins/volcengine-design-plugin) |
| 🔮 **玄机玄学** | `xuanji` | 0.1.1 | 娱乐向术数六科（八字/奇门/紫微/姻缘/风水/塔罗）+ AIGC 成象（观象环 ≤3 轮） | [xuanji-plugin](https://github.com/full-aigc-plugins/xuanji-plugin) |

> 规划仓 [`cine-planning`](https://github.com/full-aigc-plugins/cine-planning)（`director` / `script` / `storyboard` 纯规格）按 `design_baseline_not_released` 状态跟随本市场管理，在自身发布边界完成前不进入任何可安装清单。

> 候选插件 [`content-factory-plugin`](https://github.com/full-aigc-plugins/content-factory-plugin) 仍由 `candidatePlugins` 独立管理。`1.0.0-rc.2` 以 `release_candidate_installable` 状态进入 Codex、ZCode 与 Kimi 清单，可用于受控测试安装；其正式发布门禁仍为 `BLOCKED`，不得视为生产就绪或稳定版。

---

## 架构

### 市场如何工作

`catalog.json` 是唯一事实源。`scripts/sync-marketplaces.mjs` 从它生成三平台清单，并校验每个插件仓的 skills 目录（frontmatter、命名一致性）、候选插件的明确状态（隐藏阻断或 RC 测试安装）、不可变发布身份与规划仓约束（不得发布 manifest）：

```
full-aigc-plugins/
├── catalog.json                        # 单一事实源：ID / 名称 / 版本 / 分类 / 仓库
├── .agents/plugins/marketplace.json    # Codex 清单（生成物）
├── marketplace.json                    # ZCode 清单（生成物）
├── kimi-marketplace.json               # Kimi 清单（生成物）
└── scripts/                            # 同步与发版工具
```

每个独立插件仓负责自己的运行时适配：`.codex-plugin/plugin.json`、`.zcode-plugin/plugin.json` 与 `kimi.plugin.json`。

`scripts/sync-release-tooling.mjs` 默认只补齐缺失的 `AGENTS.md`，不会覆盖仓库已有的项目级指令。
只有维护者明确传入 `--refresh-agents` 时才更新既有模板；`--dry-run` 可先查看影响范围。

### 渐进式披露

插件内的技能遵循 [Agent Skills 规范](https://agentskills.io)：

1. **启动时**：仅加载技能名称和描述（最小上下文）
2. **按需**：当智能体识别到相关任务时加载完整的 `SKILL.md`
3. **深入**：仅在明确需要时读取参考文件

---

## 生态

| 资源 | 链接 |
|------|------|
| **技能侧导航（AIGC）** | [partme-ai/full-aigc-skills](https://github.com/partme-ai/full-aigc-skills) |
| **技能包组织（AIGC）** | [github.com/full-aigc-skills](https://github.com/full-aigc-skills) |
| **研发侧插件市场** | [github.com/full-stack-plugins](https://github.com/full-stack-plugins) |
| **研发侧技能导航** | [partme-ai/full-stack-skills](https://github.com/partme-ai/full-stack-skills) |
| **Agent Skills 规范** | [agentskills.io](https://agentskills.io) |
| **Skills CLI** | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) |
| **PartMe.AI** | [github.com/partme-ai](https://github.com/partme-ai) |

---

## 贡献指南

### 发版纪律

任何插件代码改动（无论大小）都要 bump + 发版，市场端靠版本号感知更新：

```bash
node scripts/bump-plugin.mjs <plugin-id> <major|minor|patch>
```

该命令会同步更新 catalog 版本、插件仓四个 manifest，并重新生成三平台清单。

### 新增插件

1. 在独立仓库中按三平台适配层构建插件（`.codex-plugin` / `.zcode-plugin` / `kimi.plugin.json`）
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
