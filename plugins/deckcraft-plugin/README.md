# DeckCraft Use

当前开发预发布版本：`0.1.0-dev.20261017.6`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


> Minimal DeckCraft Agent Plugin candidate. Package files exist; host loading and native calls remain unverified.

English | [简体中文](README.zh-CN.md) · [Architecture](docs/DeckCraft-Plugin-Architecture.md) · [Verification](docs/verification.md)

## Positioning

Let an Agent host load DeckCraft operation skills and use the existing upstream MCP server to author, inspect and export presentations. The target is a portable plugin package, without replacing DeckCraft, its MCP server or the host runtime.

```text
User task → host loads plugin Skills → host connects deckcraft-cli mcp
          → DeckCraft edit / inspect / render / export → host delivers results
```

| Property | Current status (2026-10-09) |
|---|---|
| Target format | Agent Plugins 1.0.0 |
| Plugin version, remote, verified hosts | `0.1.0-dev.0`; no remote or verified host |
| Root `plugin.json`, `mcp.json`, `skills/` | Present; host verification pending |
| Bundled skills | One `deckcraft-use` skill, identical to the local deckcraft-skills source |
| License | Apache-2.0 here; upstream DeckCraft MIT OR Apache-2.0 |

## Plugin components

The portable core is root `plugin.json`, with optional `skills/` and `mcp.json`. Skills hold routing and operational knowledge; `mcp.json` connects the existing `deckcraft-cli mcp`. Commands and Hooks are client extensions and should be added only for a tested host need. The specification defines only Skills and MCP servers as portable components. See the [official specification](https://agent-plugins.org/specification).

## Capabilities and boundaries

| Goal | Owner | Acceptance |
|---|---|---|
| Routing and command guidance | Skills | Trigger and isolated installation scenarios |
| Authorization, tool execution and MCP lifecycle | Host | Actual loading and calls |
| Deck editing, undo, rendering and export | DeckCraft | Real deck readback and reopening |
| Packaging and source pinning | Plugin | Manifest, paths, skill hashes and installation checks |

Upstream Remote may resend a mutation after communication failure; this initial plugin cannot promise exactly-once execution across failures. Headless has no window screenshot. Current PDF artwork is raster with a real-text layer. Real-world PPTX compatibility needs separate corpus checks. See [compatibility](docs/compatibility.md).

## Local candidate and quick start

The local candidate can be loaded from this directory by a host supporting Agent Plugins 1.0.0. It has no public release or verified host. MCP requires an installed `deckcraft-cli` on the host PATH. The following read-only checks can be used first:

```bash
deckcraft-cli --version
deckcraft-cli commands
deckcraft-cli describe slide.new
```

Root `mcp.json` uses the single `deckcraft-cli` executable token with `mcp` as a separate argument. This repository does not install the CLI. Desktop Remote, window screenshots, client commands and Hooks need separate verification. See the [MCP guide](https://agent-plugins.org/plugin-authors/mcp-servers).

## Design and delivery

[English architecture](docs/DeckCraft-Plugin-Architecture.md) / [中文架构](docs/DeckCraft-Plugin-Architecture.zh_CN.md) defines composition and responsibilities. [Operation boundaries](docs/operation-contract.md) covers commands, Hooks and failures. [Dreamina lessons](docs/dreamina-reference-analysis.md) explain retained and rejected patterns. [Roadmap](ROADMAP.md) and [verification](docs/verification.md) separate structure, host and real-deck evidence.

Static package checks, host installation, MCP handshake and real DeckCraft operations are reported separately. See [contribution](CONTRIBUTING.md), [security](SECURITY.md), [attribution](ATTRIBUTION.md) and [Apache-2.0](LICENSE).

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

Plugin display name: **DeckCraft Use**. Official upstream icon provenance and licenses are included under `assets/official-icon-source.json` and adjacent LICENSE files.

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## 场景操作手册

新增 `deckcraft-scenario-playbooks`：8 条带具体命令、参数与检查的流程，见 [技能入口](skills/deckcraft-scenario-playbooks/SKILL.md)。示例数据需替换，实际运行与创作效果状态见命令证据；不将目录存在当验收通过。

## main模板与品牌复用候选

新增[main模板、页面复用及结构化目录指导](skills/deckcraft-scenario-playbooks/references/main-workflows.md)，保留89个新增标识和旧目录重复项的歧义。已有场景及新增模板/复用流程通过Windows原生main回归：真实starter、指定页顺序、可编辑PPTX和源文件保持已核对；外部PowerPoint渲染及真实宿主同步仍未验收。


### Six core workflow checks (2026-10-17)

Training, redesign, brand templates, weekly reports, pitches and data stories now carry concrete Craft methods and parameters. Windows main run 39014846480 and stable matrix 39014843673 passed native/PPTX editable structures, per-slide notes, duplicate object rebinding and chart data revision after import. These are technical fixture checks; real content, external PowerPoint rendering and installed-host synchronization remain unverified. The package remains an unpublished development candidate.

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

## 方案评审对比表开发候选

新增 `deckcraft-option-comparison` 独立技能入口，深化已有比较表流程：显式表格ID、逐格数据口径、完整列宽及PPTX重开改单元格。参考PptxGenJS固定GitHub提交的表格工作流，步骤及Craft参数原创；官方0.7.0 CLI结构与PPTX回读通过，Windows16条记录回归通过；隔离Codex原生MCP与内置浏览器已观察合成短表内容和单元格修改同步。候选发行记录见目录仓；真实素材、外部PowerPoint和其他宿主仍未验收。
