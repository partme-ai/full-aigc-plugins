# DeckCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.5`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


> DeckCraft 的 Agent Plugin 最小候选包。包结构已创建；宿主加载和原生调用尚未验证。

[English](README.md) | 简体中文 · [架构](docs/DeckCraft-Plugin-Architecture.zh_CN.md) · [验证](docs/verification.md)

## 项目定位

让 Agent 宿主加载 DeckCraft 操作技能，并通过上游已有 MCP 服务端制作、检查和导出演示文稿。本仓目标是可移植插件包，不重写 DeckCraft、MCP 服务器或宿主运行时。

```text
用户任务 → 宿主加载插件 Skills → 宿主连接 deckcraft-cli mcp
       → DeckCraft 编辑 / inspect / render / export → 宿主交付结果
```

| 属性 | 当前状态（2026-10-09） |
|---|---|
| 格式目标 | Agent Plugins 1.0.0 |
| 插件版本、远端、已验证宿主 | `0.1.0-dev.0`；无远端或已验证宿主 |
| 根 `plugin.json`、`mcp.json`、`skills/` | 已创建，待宿主验证 |
| 包内技能 | 1 个 `deckcraft-use`；与本地 deckcraft-skills 源文件一致 |
| 许可证 | Apache-2.0；DeckCraft 上游 MIT OR Apache-2.0 |

## 插件组成

可移植核心是根 `plugin.json`，以及按需存在的 `skills/` 和 `mcp.json`。Skills 承载路由与操作知识；`mcp.json` 连接现有 `deckcraft-cli mcp`。命令和 Hooks 属于具体客户端扩展，只有真实宿主场景需要且已验证其格式时才加入。规范只定义 Skills、MCP servers 两类可移植组件。[正式规范](https://agent-plugins.org/specification)

## 能力与边界

| 目标 | 所有者 | 验收 |
|---|---|---|
| 操作路由、命令参考 | Skills | 触发与单独安装场景 |
| 权限、工具执行、MCP 生命周期 | 宿主 | 实际加载和调用 |
| 文稿编辑、撤销、渲染、导出 | DeckCraft | 真实文稿回读与重开 |
| 包装与来源固定 | 插件 | manifest、路径、技能摘要和安装检查 |

上游 Remote 可能在通信错误后重发修改；本插件初版不承诺异常场景恰好执行一次。Headless 没有整窗截图。PDF 图稿目前是栅格加真实文本层。真实 PPTX 兼容性需独立语料验收。[兼容性](docs/compatibility.md)

## 本地候选与快速开始

本地候选可供支持 Agent Plugins 1.0.0 的宿主从本目录加载。尚无公开发行或宿主验证；MCP 需要宿主能找到已安装的 `deckcraft-cli`。可先运行以下只读检查：

```bash
deckcraft-cli --version
deckcraft-cli commands
deckcraft-cli describe slide.new
```

根 `mcp.json` 使用单一 `deckcraft-cli` 命令 token 和 `mcp` 参数；本仓不安装 CLI。桌面 Remote、窗口截图、客户端命令和 Hooks 均需分别验证，不是默认能力。[MCP 指南](https://agent-plugins.org/plugin-authors/mcp-servers)

## 设计与交付

[中文架构](docs/DeckCraft-Plugin-Architecture.zh_CN.md) / [English architecture](docs/DeckCraft-Plugin-Architecture.md) 明确组成和责任；[操作边界](docs/operation-contract.md) 记录命令、Hooks 与失败语义；[Dreamina 借鉴](docs/dreamina-reference-analysis.md) 说明保留与裁剪理由。[路线](ROADMAP.md) 和 [验证矩阵](docs/verification.md) 将结构、宿主和真实文稿证据分开。

静态包检查与实际宿主、MCP 握手、真实 DeckCraft 调用分开记录。参见 [贡献](CONTRIBUTING.md)、[安全](SECURITY.md)、[来源](ATTRIBUTION.md) 和 [Apache-2.0](LICENSE)。

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

插件展示使用上游官方图标；名称为 **DeckCraft Use**。图标来源与许可证保存在 `assets/official-icon-source.json` 和相邻 LICENSE 文件中。

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## 场景操作手册

新增 `deckcraft-scenario-playbooks`：8 条带具体命令、参数与检查的流程，见 [技能入口](skills/deckcraft-scenario-playbooks/SKILL.md)。示例数据需替换，实际运行与创作效果状态见命令证据；不将目录存在当验收通过。

## main模板与品牌复用候选

新增[main模板、页面复用及结构化目录指导](skills/deckcraft-scenario-playbooks/references/main-workflows.md)，保留89个新增标识和旧目录重复项的歧义。已有场景及新增模板/复用流程通过Windows原生main回归：真实starter、指定页顺序、可编辑PPTX和源文件保持已核对；外部PowerPoint渲染及真实宿主同步仍未验收。


### 六项核心场景技术回归（2026-10-17）

培训、改版、品牌模板、周报、提案和数据故事已重建实际方法与参数，并同步到独立技能。Windows main运行39014846480和稳定版矩阵39014843673通过：逐页备注、复制后新ID、品牌主题、原生图表/表格及PPTX保存回读；图表回读后再次修改数据。只证明示例结构及技术链，不代表真实内容、外部PowerPoint版式或宿主画面同步验收。当前仍为开发候选，未上架公共市场。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。
