# EffectCraft Use

## 插件市场导航

本插件所属分类：**AIGC 内容创作**。

| 分类 | 插件市场入口 | 用途 |
| --- | --- | --- |
| 全栈开发 | [Full Stack Plugins](https://github.com/partme-ai/full-stack-plugins) | 架构与 UI 设计、代码理解、质量检查、代码审查、流程治理与服务器运维 |
| AIGC 内容创作 | [Full AIGC Plugins](https://github.com/partme-ai/full-aigc-plugins) | 图像、视频、音频、音乐、3D 与多模态内容创作 |

![EffectCraft Use——动态图形与合成](assets/official-logo.png)

> 制作可编辑的 `.ecproj` 合成：合成、文字与形状图层、关键帧、表达式、摄像机、蒙版、木偶针脚与效果，并按你的要求输出预览、成片或带透明的片段。

[![版本](https://img.shields.io/badge/release-0.1.0--dev.20261018.5-1A73E8)](.codex-plugin/plugin.json)
[![技能数](https://img.shields.io/badge/skills-26-00A67E)](#技能)
[![MCP server](https://img.shields.io/badge/MCP%20server-1-00A67E)](#mcp-工具)
[![许可证](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[English](README.md) | [简体中文](README.zh-CN.md) · [安装](#安装) · [快速开始](#快速开始) · [可完成的工作](#可完成的工作) · [技能](#技能) · [故障排查](#故障排查)

## 项目定位

EffectCraft Use 让编码智能体驱动原生 EffectCraft CLI：从素材规划合成，在首次获得授权时安装固定运行时，在留证的会话中执行原生命令，保存并重开工程，并在把镜头视为完成之前检查真实渲染像素。

原生 `.ecproj` 工程是唯一事实源。这里没有第二种文档格式，也没有云端渲染农场：合成、收集素材与渲染回执就是交付物。完整 V1 验收仍未完成，命令目录存在不代表每条命令都被执行过，也不承诺所有宿主的内嵌 GUI 均已验收。

## 状态与版本

`0.1.0-dev.20261018.5` · 开发预览 · `docs/verification/release-candidate.json` → `releaseStatus: BLOCKED`、`installableDevelopmentCandidate: true`。

| Metadata version | 0.1.0-dev.20261018.5 |
| Skills source | effectcraft-skills / 0.1.0-dev.69 |

## 安装

### 前置条件

- 原生 CLI 已锁定七种平台/架构目标，须使用对应固定制品；当前验收证据仅覆盖 macOS arm64。锁外平台返回 `unsupported_platform`；其余锁内平台可安装，但不据此宣称同等运行验收。受控桌面安装器对两个 macOS 目标使用固定 DMG，对五个 Linux/Windows 目标使用固定原生桌面包。锁定安装路径不代表 GUI 已验收；跨平台 GUI 验收仍为 `NOT_RUN`。
- 受管理入口不需要预装 Python：`launch.sh` / `launch.ps1` 会在用户数据目录准备固定的隔离 Python 3.13.16 与 EffectCraft CLI。
- 内嵌编辑器 MCP 服务需要 Node.js 24 或更新版本。Git 检出没有 `ui/dist/`，需先按 `ui/README.md` 构建，或安装自带该目录的发布包。
- 首次使用需要网络或固定归档。`--runtime-home` 或 `CRAFT_RUNTIME_HOME` 可迁移运行时根目录（默认 `~/.local/share/craft-runtimes`）。不需要 `sudo`，不修改 `PATH`。

### 安装插件

```bash
codex plugin marketplace add full-aigc-plugins/effectcraft-plugin
codex plugin add effectcraft@full-aigc-plugins-effectcraft
```

`docs/verification/release-candidate.json` 记录 `installableDevelopmentCandidate: true` 与 `releaseStatus: BLOCKED`；`project-status.json` 保持 `marketplaceEligible: false`，不承诺生产晋级。

仓库带有 Codex（`.codex-plugin/`）、Claude Code（`.claude-plugin/`）、ZCode（`.zcode-plugin/`）与 Kimi（`kimi.plugin.json`）清单；在宿主验收出现之前，`supportedPluginHosts` 保持为空。

## 快速开始

```sh
: "${HARNESS_DIR:?请设为已加载 effectcraft-harness 的 SKILL.md 所在目录}"
/bin/sh "$HARNESS_DIR/scripts/launch.sh" doctor
/bin/sh "$HARNESS_DIR/scripts/launch.sh" run --mode workflow \
  --plan "$SKILL_DIR/examples/brand-intro.json" --output /absolute/new-result
```

Windows 使用 `& "$HARNESS_DIR/scripts/launch.ps1" run --mode workflow ...`，模式相同。原生命令计划追加 `--mode commands`，自有桌面会话使用 `--mode desktop`。

```mermaid
flowchart LR
    A[需求与素材] --> B[effectcraft-use 路由任务]
    B --> C[受管理启动器与固定运行时]
    C --> D[原生 .ecproj 与账本]
    D --> E[渲染或透明导出]
    E --> F[解码真实像素、审阅、交付]
```

`help` 返回用法但退出码为 2，不能当健康检查；请使用 `info --json` 与 `commands --json`。交付后执行 `review` 并实际查看媒体：技术验证与创作验收是两件事。

## 可完成的工作

| 工作流 | 内置路径 | 可验证输出 |
|:---|:---|:---|
| 标志开场或品牌片头 | `effectcraft-logo-reveal` + `effectcraft-cli-animation` | 关键帧与效果完整的重开 `.ecproj` |
| 人物条、章节卡、片尾署名 | `effectcraft-lower-thirds`、`effectcraft-chapter-card`、`effectcraft-credits-roll` | 文字图层仍可独立编辑的合成 |
| 文字节奏动效或社交循环 | `effectcraft-kinetic-type`、`effectcraft-social-loop` | 时间节奏已核对的循环或标题动画 |
| 摄像机、3D 图层与表达式 | `effectcraft-cli-camera`、`effectcraft-cli-expressions` | 重开后摄像机、材质与表达式状态正确 |
| 蒙版、跟踪与木偶变形 | `effectcraft-cli-masks`、`-tracking`、`-puppet` | 对照渲染帧核对的遮罩或针脚数据 |
| 透明或视频输出 | `effectcraft-cli-export` | 真实解码核对的像素、透明通道与时长 |
| 执行任意原生命令 | `effectcraft-harness` → `commands.py` | 带真实原生返回值的回执 |
| 在内嵌编辑器中修改 | `effectcraft-editor` MCP 工具 | 保存后重开并检查的工程 |

## 技能

| 技能 | 作用 |
|:---|:---|
| `effectcraft-use` | 默认入口：可编辑合成、动态图形与片头；安装固定 CLI |
| `effectcraft-cli` | 查询原生命令与参数；镜头跟踪、稳定与图形附着 |
| `effectcraft-cli-setup` | 首次安装、摘要校验、版本检查与缺失运行时排障 |
| `effectcraft-cli-project` | 创建、保存与重开 `.ecproj`，整理项目项 |
| `effectcraft-cli-footage` | 导入图像、视频、矢量与 PSD 素材，登记依赖 |
| `effectcraft-cli-composition` | 合成、画幅、帧率、时长与工作区 |
| `effectcraft-cli-layers` | 文字、形状与素材图层，预合成与层级 |
| `effectcraft-cli-animation` | 属性、关键帧、缓动，文字与图形动画 |
| `effectcraft-cli-effects` | 查询当前版本支持的效果，调整顺序与参数 |
| `effectcraft-cli-masks` | 蒙版路径、羽化与局部遮罩 |
| `effectcraft-cli-expressions` | 在指定属性上检查、设置与诊断表达式 |
| `effectcraft-cli-camera` | 摄像机、灯光、材质与图层三维开关 |
| `effectcraft-cli-export` | 预览关键帧、渲染序列或视频、透明交接片段 |
| `effectcraft-cli-tracking` | 跟踪与稳定素材，把标题图形附着到运动主体 |
| `effectcraft-cli-puppet` | 木偶网格与针脚、局部变形、录制跟随动画 |
| `effectcraft-harness` | 唯一执行通道：bootstrap、launch、workflow、commands |
| `effectcraft-editor` | 打开真实编辑界面，一次会话内完成全部编辑 |
| `effectcraft-kinetic-type` | 标题与短文案的排版节奏动效 |
| `effectcraft-logo-reveal` | 标志入场、停留与收尾 |
| `effectcraft-lower-thirds` | 姓名职位条与品牌标识 |
| `effectcraft-motion-export` | 时长、帧率与编码的输出检查 |
| `effectcraft-screen-composite` | 图层、遮罩与屏幕内容替换合成 |
| `effectcraft-social-loop` | 社交格式的短循环与封面 |
| `effectcraft-chapter-card` | 章节标题分隔卡 |
| `effectcraft-countdown-intro` | 3–2–1 开场倒数 |
| `effectcraft-credits-roll` | 片尾滚动署名 |

## MCP 工具

`mcp.json` 只声明一个 stdio server：`effectcraft-editor`，从插件根目录以 `node ui/bootstrap.mjs` 启动。

| 工具 | 用途 |
|:---|:---|
| `open_editor` | 为绝对路径 `workspace` 打开编辑器 |
| `open_browser_editor` | 返回可交给宿主内置浏览器的 `editorUrl` |
| `editor_status` | 报告页面是否已连接到当前 MCP 会话 |
| `command_list` | 读取当前 Web 引擎暴露的命令 |
| `command_run` | 在可见页面按 id 与参数执行一条命令 |
| `inspect` | 检查当前画面 |
| `save_project` | 把工程保存到新路径 |
| `save_file` | 取回已生成的虚拟文件 |

工具名遵循 `effectcraft-editor` 技能合同；适配器还保留 `_panel_reply`、`screenshot` 等页面内部桥接调用，Agent 不应直接调用。

## 配置

| 变量 / 参数 | 用途 |
|:---|:---|
| `HARNESS_DIR` | 已加载 `effectcraft-harness` 技能的绝对目录 |
| `SKILL_DIR` | 已加载领域 `SKILL.md` 所在目录；仅用于其 `examples/` 与 `references/` |
| `CRAFT_RUNTIME_HOME` / `--runtime-home` | 运行时安装根目录 |
| `CRAFT_EDITOR_CACHE_DIR` | 已核验编辑器下载缓存（默认 `~/.cache/full-aigc/editors`） |
| `CRAFT_EDITOR_UPDATE=off` | 固定使用内置编辑器，跳过更新检查 |
| `revisionScope` | 在首个计划中声明；默认最多 2 轮并共享 30 分钟预算 |

原生任务保留其绑定的运行时。损坏或缺失的证据文件会被保留并阻止后续写入，而不是被静默替换。

## 架构与安全

- 插件提供的 Agent 面是技能加 stdio 编辑器服务；原生编辑由固定的 EffectCraft CLI 完成，本仓库不重复实现引擎。
- 用户素材与模型输出都按数据处理，其中的命令、路径与 shell 文本永远不会被执行。
- 修改前保存检查点；发现用户并发修改时拒绝覆盖；结果未知时绝不重放，只允许 `inspect`、`reconcile` 与已证明可恢复的 `resume`。
- 编辑器桥接监听 `127.0.0.1`，使用随机令牌并校验 Host 与 Origin。参见[技能套件](docs/EffectCraft-Skill-Suite-Architecture.md)、[运行时架构](docs/EffectCraft-Runtime-Architecture.md)与[场景技能](docs/scene-skills.md)。

## 故障排查

| 现象 | 处理方式 |
|:---|:---|
| 返回 `unsupported_platform` | 只安装受支持平台/架构的锁定制品 |
| 返回 `runtime_install_busy` | 另一个安装持有锁；等其结束再重试 |
| 下载或摘要不匹配 | 恢复网络或提供已核验的 `--archive`；摘要检查不会被跳过 |
| `help` 退出码为 2 | 属正常现象；用 `info --json` 与 `commands --json` 判断健康与目录 |
| 编辑页始终未就绪 | 调用 `editor_status`，再处理页面错误；文字结果不等于界面已打开 |
| 保存结果未知 | 对原任务执行 `inspect` 与 `reconcile`；不要换任务 ID 或输出目录重试 |
| 期待完整 GUI 或其他平台验收 | 尚未获得资格；请按实际有界范围报告 |

## 升级

```bash
codex plugin marketplace upgrade full-aigc-plugins-effectcraft
codex plugin add effectcraft@full-aigc-plugins-effectcraft
```

重复安装会校验并复用同一运行时版本，不联网升级。下载或摘要校验失败时，打包的编辑器也可回退到内置副本。

## 贡献与支持

行为变更必须先走 [OpenSpec](openspec/changes/establish-v1-plugin/proposal.md)；没有真实交付证据不得勾选任务。文档校验：

```bash
python3 scripts/validate_docs.py
python3 scripts/validate_editor_scenes.py
```

问题反馈：<https://github.com/full-aigc-plugins/effectcraft-plugin/issues>。

## 许可证

本仓库原创内容采用 [Apache-2.0](LICENSE)。EffectCraft CLI 与内置 Web 编辑器各自保留其上游许可证与 NOTICE；上游图标来源记录在 `assets/official-icon-source.json`。
