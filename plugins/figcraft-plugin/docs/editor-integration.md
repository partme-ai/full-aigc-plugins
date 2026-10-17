# FigCraft Use

独立插件，包含官方图标、stdio MCP、MCP Apps 面板和 7 个界面设计场景技能。当前为本地未发布候选；没有修改全局插件设置。

编辑器基于 FigCraft v0.6.0 的固定源码加入自动化与工作区文件桥接，参考 Craft craft-runtime，保留其 Apache-2.0 许可。`ui/source.lock.json` 记录来源提交；`ui/editor.lock.json` 记录内置制品摘要。它是我们构建的增强版，不是官方原版 Web ZIP。

通过 `open_editor` 在支持 MCP Apps 的宿主显示；宿主未渲染时，用 `open_browser_editor` 返回的 URL 在宿主内置浏览器打开。Codex Desktop 可使用 `open_in_codex`。不支持 Apps 或内置浏览器的 MCP 客户端无法靠服务器配置获得内部页面。

## 使用

运行环境：Node.js 24。已构建候选的入口是 `node ui/dist/adapter.mjs`，使用 stdio。工作区通过 `CRAFT_WORKSPACE_ROOT` 指定。`--serve` 用于单独展示界面，自动化必须连接同一个 MCP 实例。

- `open_editor` / `open_browser_editor`：打开界面。
- `create_node`、`set_properties`、`run_command`：编辑可见文档。
- `inspect_document`、`screenshot`：检查结构与画面。
- `save_file`、`open_file`、`export`：工作区工程保存、重开与导出。

首次打开尝试下载本插件最新兼容增强发行包；未发布、下载失败或接口不兼容时使用内置版本。`CRAFT_EDITOR_UPDATE=off` 可明确选择内置资源。

## 宿主配置

使用完整插件市场包安装。Codex 入口为 `.codex-plugin/plugin.json` 和 `.codex-plugin/mcp.json`；Claude Code 入口为 `.claude-plugin/plugin.json` 和根 `.mcp.json`。标准宿主读取 `plugin.json` 和 `mcp.json`。安装路径由宿主解析，不再推荐逐项绝对路径配置。

## 验证

源码增强构建已在本机通过创建 frame/文字、保存重开、PNG 导出、页面刷新与断开回归。`ui/tests/editor-smoke.mjs` 是可重复的实际 stdio + Chromium 测试。它不等于每个目标宿主均已安装验收。

构建方法见 [ui/README.md](ui/README.md)；源码技能在独立 `figcraft-skills` 仓维护，本地副本由 `scenario-candidates.json` 校验。

## 源码增强构建与更新源

2026-10-16 起采用同会话编辑器模式：从 `ui/source.lock.json` 的固定源码构建同会话自动化 WASM。`ui/build-source.py` 生成独立候选，`ui/finalize-source.py` 提取真实工具目录并保留许可。没有匹配的编译器时明确失败，不安装工具。

首次打开查询本插件 `full-aigc-plugins/*-plugin` Release 的增强发行包；没有已发布兼容包则继续使用内置。原版 Web ZIP 不会替代增强版。版本记录包括插件版本和上游源码版本。旧候选及当前打开的编辑器会话保留，新候选必须通过实际编辑、保存、重开再交付。

## 插件安装与界面

优先通过插件市场安装完整发布包，不需要手工填写每个 MCP 的绝对路径。开发仓必须先构建编辑器资源；仅克隆源码不等于已安装运行包。

| 入口 | 配置 | 路径基准 |
| --- | --- | --- |
| 标准 Agent Plugins | `plugin.json`、`mcp.json` | `${PLUGIN_ROOT}` 由支持该规范的宿主展开 |
| Codex | `.codex-plugin/plugin.json`、`.codex-plugin/mcp.json` | 相对 `cwd` 由宿主定位到插件根目录 |
| Claude Code | `.claude-plugin/plugin.json`、根 `.mcp.json` | `${CLAUDE_PLUGIN_ROOT}` 由宿主展开 |

连接后调用 `open_editor` 或 `open_browser_editor`，显式传入本次任务目录 `workspace`。这是用户文件的位置，不是插件安装位置，不写死在安装清单中。

支持 MCP Apps 的宿主可呈现工具关联的 UI 资源；支持内置浏览器的桌面宿主可打开 `open_browser_editor` 返回的地址。Claude Code 终端本身不提供浏览器面板。支持插件或 stdio MCP 并不自动意味着支持内嵌 UI；缺少 UI 能力时只能在浏览器打开同一会话，不能宣称宿主内嵌已通过。

stdio 负责 Agent 与插件通信，本地 HTTP 负责页面和同会话编辑桥接。Agent 指令作用于当前页面的编辑器状态；等待 `editor_status` 就绪后再执行编辑。保存源工程后重开检查，关闭 MCP 进程前先保存。

本轮优先验证标准插件入口、Codex 和 Claude Code 清单。仅支持 MCP 的工具不属于当前安装交付范围。
