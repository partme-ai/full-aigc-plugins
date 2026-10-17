# Craft 编辑器与场景技能本地候选

> 本文前段记录先前十二款 ZCode 快照候选，作为历史验证保留。新增 FigCraft 与 fork 源码构建的当前状态见 [源码增强接入](craft-source-integration.md)。

日期：2026-10-16。分支：`feature/REQ-20261016-wandl-craft-ui-skills`。尚未提交、推送、发布或全局安装。规格事实源：`openspec/changes/archive/2026-10-16-add-craft-editor-scenes/`；原有插件变更保持独立。

## 交付范围

十二个插件各新增一个编辑器入口技能和六个场景技能，共 84 个新技能，其中 72 个场景。技能源位于各自 `full-aigc-skills-repositories/*-skills`，插件中是本地候选副本；原有发布快照没有改写。候选技能目录见 [场景目录](craft-scene-catalog.json)。

| 插件 | 接入来源 | 新增场景举例 | 本地运行证据 |
|---|---|---|---|
| PhotoCraft | ZCode 0.2.2 编辑器构建 | 老照片修复、肖像修饰、产品抠图 | 分层工程保存重开、PNG 导出、刷新释放连接 |
| CADCraft | 同上 | 平面图、尺寸标注、图层整理 | 图元编辑、保存重开、渲染 |
| DesignCraft | 同上 | 宣传册、目录、长文档 | 文档编辑、保存重开、页面渲染 |
| VectorCraft | 同上 | 标志、图标、信息图 | 图形编辑、保存重开 |
| DeckCraft | 同上 | 路演、周报、培训课件 | 幻灯片编辑、保存重开 |
| PrintCraft / PdfCraft | 同上，底层 pdfcraft | PDF 整理、OCR、脱敏、预检 | PDF 创建、保存重开、页面渲染 |
| SoundCraft | 同上 | 播客、人声混音、音频交付 | 音频导入、混音导出、工程重开 |
| GridCraft | 同上 | 清洗、销售汇总、预算 | 单元格读写、撤销重做、保存重开 |
| WordCraft | 同上 | 提案、纪要、研究报告 | 文本编辑、保存重开、渲染 |
| EffectCraft | 官方 Web v0.10.0 | 标志动画、字幕条、动态文字 | 新建合成文字、工程保存重开并核对内容 |
| FilmCraft | 官方 Web v0.8.0 | 短视频、采访、字幕交付 | 序列文字、工程保存重开并核对内容 |
| LightCraft | 官方 Web v0.8.0 | RAW、批量风格、选片 | 图库检查、备份 ZIP 写入工作区 |

PrintCraft 上游现重定向到 PdfCraft，保留本地插件标识以兼容既有技能。音频上游为 `storytold/soundcraft`，用户提供的 `sourcecraft` 不是有效仓库。

## 整合机制

```mermaid
flowchart LR
  S[场景技能：诊断、步骤、检查] --> A[智能体]
  A --> M[插件 stdio MCP]
  M --> C[上游编辑器命令与工程 API]
  M --> U[MCP Apps 资源]
  M --> B[127.0.0.1 同会话页面]
  U --> Z[支持 Apps 的宿主面板]
  B --> X[Codex 内置浏览器或其他浏览器]
  C <--> W[工作区源工程与导出文件]
  X <--> C
```

普通 MCP 只定义工具、资源和消息，不要求宿主渲染编辑器。ZCode 增加了 MCP Apps 面板与宿主桥接；其它平台不识别其插件清单、资源元数据或消息协议时，只能看到“打开工具”的文本结果。本实现保留原生 Apps 资源，并增加共享同一 MCP 会话的浏览器接入。浏览器返回 URL 不等于已打开：智能体须用宿主打开页面并等待 editor_status 就绪。

九个编辑器复用上游 MCP，不复制其业务命令。Effect/Film/Light 直接连接官方 Web API。LightCraft 的图库保存在浏览器中，应使用备份 ZIP 交付；当前没有通用 save_project 实现，不伪造该能力。其导入与恢复未做真实样本验收。

## 宿主接入

- **ZCode**：`.zcode-plugin/plugin.json` 与原生 Apps 资源已准备；本轮未在 ZCode 安装新候选包做面板验收。
- **Codex**：`.codex-plugin/plugin.json` + `.mcp.json`；`open_browser_editor` 返回地址后通过宿主内置浏览器打开。本轮已在当前 Codex 中看到 PhotoCraft，并打开保存的分层工程。没有宣称 Codex 原生 MCP Apps 或插件发现、安装流程已验证。
- **WorkBuddy**：以连接器导入 stdio MCP。各包 `hosts/workbuddy/mcp.json` 是模板，不能原样安装；下列命令生成真实路径配置。独立加载技能目录需要宿主相应支持。本轮未在 WorkBuddy 实际安装或验收内嵌 UI；不支持页面嵌入时用浏览器编辑器。

从解压后的插件根目录执行（仅生成配置、不安装）：

```bash
python3 scripts/configure_editor_host.py --host workbuddy --workspace /absolute/workspace --output /absolute/output/workbuddy.json
python3 scripts/configure_editor_host.py --host codex --workspace /absolute/workspace --output /absolute/output/codex.toml
```

运行要求 Node.js 24+。每个工作区连接对应 MCP 实例；一个实例保留一个编辑页面。`--serve` 用于 UI 演示，不能再启动另一个 stdio 实例并假定它共享文档。关闭进程前保存工程。刷新页面会释放原页面连接，未保存编辑可能丢失。

[WorkBuddy 官方连接器](https://open.workbuddy.cn/docs/connector) · [MCP Apps](https://apps.extensions.modelcontextprotocol.io/api/documents/overview.html) · [Agent Plugins](https://agent-plugins.org/specification)

## 打包和验证

目录仓执行：

```bash
python3 scripts/package-craft-editors.py --repositories ../full-aigc-plugins-repositories --output .local/craft-editor-candidates
```

输出十二个本地候选 ZIP 和 SHA-256 index.json，包含已构建适配器、编辑器资源、技能、配置、来源锁和许可证；无需运行时依赖本机 ZCode 缓存。已有 ZIP 拒绝覆盖。十二个 ZIP 均通过摘要与 CRC 校验，并在独立解压目录、空工作区启动 MCP，列出工具和返回编辑页面；该检查只证明独立启动，编辑保存行为由前述浏览器测试提供证据。源码重建步骤位于各包 ui/README.md。

[本地测试摘要](craft-editor-local-tests.json) 记录实际范围。九个编辑器跑过 MCP + Chrome 1280×1024 保存重开链路；三种 Web 编辑器分别验证表中行为。PhotoCraft 的关闭、刷新与重开另有回归。DesignCraft 快照验证 17 项通过；各包新场景摘要校验通过；十二份 plugin.json 与十二份 mcp.json 通过官方 Agent Plugins 1.0.0 JSON Schema 验证。

**72 个场景是可执行流程说明，不是 72 种算法实现，也不代表 72 种最终作品已验收。** 老照片技能包含损伤分类、处理顺序、工具能力检查和交付标准，但没有内置人脸复原或生成式补全模型。还需用有许可的真实素材验证画质、音质、字幕、OCR、脱敏和复杂排版等结果。命令缺失时必须报告，不能用相近命令伪造完成。

当前完成本地实现及已列运行验证，保留各宿主安装与真实内容质量验收边界。没有用历史 host PASS 为本次候选背书。

## 官方图标与 Use 显示名

2026-10-16 已统一十二个本地候选的 `xxCraft Use` 显示名，使用对应官方图标；明细见 [展示名称与来源](craft-plugin-branding.md)。更新后的 ZIP 位于 `.local/craft-editor-candidates-branding`，此前 `.local/craft-editor-candidates` 为改名前产物。未修改已发布市场版本、未全局安装。十二包已通过名称、图标摘要、PNG 解码、标准 manifest Schema 与 ZIP 内容检查。PhotoCraft 全量文档检查被已有 `product-docs/.DS_Store` 误计目录影响，本轮未修改该校验器或删除文件。

## stdio 与在线更新策略

本地候选增加首次打开时的官方最新兼容完整包下载；失败使用内置版本。配置与状态字段见各包 `docs/editor-integration.md`。候选包仍包含完整内置编辑器。新版分发目录为 `.local/craft-editor-candidates-latest-fallback`。MCP 保持 stdio，HTTP 只服务预览界面。
