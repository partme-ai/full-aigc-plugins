# FigCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.5`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


独立插件，包含官方图标、stdio MCP、MCP Apps 面板和界面设计场景技能，另附 8 条带参数的详细流程。当前为本地未发布候选；没有修改全局插件设置。

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

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## 界面场景操作手册

新增8条界面设计流程，见 [figcraft-scenario-playbooks](skills/figcraft-scenario-playbooks/SKILL.md)。包含实际返回ID绑定、父子结构、自动布局和独立CLI执行脚本；宿主同步显示验收单独记录。

## main新增能力候选

新增[自动保存与协作成员控制指导](skills/figcraft-scenario-playbooks/references/main-workflows.md)，包括2个新方法和5处契约变化。仅核对固定main真实参数；新增业务、浏览器托管及协作服务器验收未完成。


## 原型真实宿主检查（2026-10-17，开发候选）

已通过隔离的Codex原生插件安装与app-server MCP路由，在Codex内置浏览器执行本仓prototype-flow步骤；实际点击Start→Result→Start。固定main d1d8c3f的Web候选可显示中文；同一会话node.set修改标题及按钮填色后，编辑器和proto.preview实时预览同时变化，原生工程保存成功。没有用独立SDK替代宿主调用。该结论仅覆盖一个合成原型，不是Kimi/ZCode、其他Fig场景或公开市场验收；默认旧内置Web未替换。

真实二进制.fig样例按对象类型核对矢量顶点与画框圆角；原始CLI保留了本样例几何。曾把矢量通用圆角字段当作真实几何导致误报，现已修正检查器并撤回不必要的运行时补丁。该单一样例不代表所有Figma文件完整保真。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。
