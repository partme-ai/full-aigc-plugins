# LightCraft Use

本轮开发预发布：`0.1.0-dev.20261018.2`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


待发布开发预发行 `0.1.0-dev.3`，包含技能库六项技能的受摘要保护快照。`candidate-source.json` 锁定已公开来源 v0.1.0-dev.1 / 87fe7ce；`source-suite.json` 记录来源版本，原生版本独立为 `0.2.1`。插件运行不需要来源仓库。

已实现持久任务锁、原子状态、只读核对、停止请求、明确剩余步骤建议、有界修订、绑定目标/原片/候选/设置的审阅，以及独立重开交付门禁。`.codex-plugin/plugin.json` 是最小接入清单；不添加自动 hooks。来源升级默认只预检，拒绝快照漂移或用户修改。

```bash
python3 -I -B scripts/validate_package.py --source-git /path/to/lightcraft-skills
python3 -I -B -m unittest discover -s tests -v
python3 -I -B scripts/controller.py --help
```

控制器通过 `init/run/status/inspect/reconcile/stop/remaining/review-request/review/revise/deliver` 显式调用。run 可能触发原生安装；只在已有授权内执行。inspect/reconcile 不启动原生程序，UNKNOWN 不重放。

输入 JSON、恢复与审阅交接见 [控制器操作契约](docs/controller.zh-CN.md)。

主 OpenSpec 任务 **26/26** 完成，主变更适用验收与公开开发预发行已完成。已通过宿主安装/发现、缓存控制器原生闭环与合成图视觉审阅；Codex 0.161.0 六技能隔离环境的五类宿主场景已通过，全量技能环境仍有上下文预算限制；Git main 已推送，Python 3.11/3.12/3.13 远端离线 CI 全部通过；插件开发预发行 v0.1.0-dev.2 已公开，锁定技能库 v0.1.0-dev.1。三个 P3 独立扩展变更保持 OPEN。

[任务与规格](openspec/README.md) · [当前证据及差距](docs/verification/implementation-evidence.md) · [公开预发行历史报告](docs/verification/local-report.json) · [架构](docs/architecture.md) · [回执与来源同步](docs/task-receipts.zh-CN.md)

Connect/MCP 增量正在验收，见 [当前增量证据](docs/verification/connect-mcp-20261008/README.md)。上述公开预发行与宿主通过记录绑定历史源码，不能证明本次增量已完成宿主或桌面验收。三个独立扩展继续保持 OPEN。

批量范围与选择性修订增量已完成实际三照片验收，见 [批量证据](docs/verification/batch-20261008/README.md)。扩展变更尚未整体完成，当前发布草稿的旧目标提交不会自动包含此增量。

逐样本 RAW 身份与结果分层已完成当前原生验收，见 [RAW 证据](docs/verification/raw-20261008/README.md)。完整解码、预览回退和不支持分别记录，仅适用于所测摘要与相机变体。

SAM 当前只读评估与未完成门禁见 [验收记录](docs/verification/sam-20261008/README.md)。

三领域协议消费与失效规则已验证，宿主自动调度仍未验收，见 [实际证据](docs/verification/exchange-20261008/README.md)。

当前候选隔离宿主五类场景通过；Nikon RAW 视觉复核发现明显偏色，公开发布门禁保持开放，见 [当前宿主及视觉证据](docs/verification/current-host-20261008/README.md)。宿主 MCP 与桌面验收尚未完成。

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

Plugin display name: **LightCraft Use**. Official upstream icon provenance and licenses are included under `assets/official-icon-source.json` and adjacent LICENSE files.

## 场景操作手册

新增8条带具体命令、参数和效果检查的流程，见 [lightcraft-scenario-playbooks](skills/lightcraft-scenario-playbooks/SKILL.md)。输入坐标与时长须现场重算，原生技术验证与真实素材效果状态独立记录。

## main新流程候选

新增[联系印样、局部蒙版模板与幻灯片导出指导](skills/lightcraft-scenario-playbooks/references/main-workflows.md)，并提供固定main完整参数入口，覆盖新增58个方法。新流程尚未业务验收，Web能力逐项检查，不据目录推断通过。

## 六项核心显影场景回归

选片、批量风格、人像整体曝光、风景拉直、照片交付、RAW基础显影六项指导已明确照片ID、选择与设置组边界；原8条手册加6条核心，共14条通过Windows限定技术回归。固定Nikon D2H NEF的运行时报告为完整RAW，导出与嵌入预览已查看；不推广到其他相机/变体，也不构成独立解码或色彩校准。EXIF GPS移除有保留对照，同名交付保护已验证。此处绑定官方0.8/main，不替代以上旧CLI 0.2.1、旧发行或宿主资格；创作效果与宿主同步仍开放。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

## 独立副本、版本恢复与曲线迁移开发候选

新增`lightcraft-virtual-copy-review`、`lightcraft-named-version-restore`、`lightcraft-tone-curve-transfer`，固定darktable手册GitHub提交并原创映射实际命令参数。官方0.8.0 macOS三场景27次CLI调用通过：副本独立编辑、命名版本恢复后的设置和像素一致、仅toneCurve组迁移且目标曝光/色彩/裁切保持，源文件与排除照片不变，新进程重开可继续。当前未发布新市场版本；Windows完整17场景116次CLI及输出摘要通过，真实Codex MCP/IAB的副本、恢复、曲线与页面重载验证通过。真实媒体质量、备份恢复UI和其他宿主仍未验收。

## 18.2发行标签修正

18.2对齐Git标签与完整ZIP的源码提交。旧18.1标签及制品保留并标记替代；技能和固定编辑器资源字节保持，此前媒体/宿主验收仍保留原版本与平台限定。本次补充标签、完整ZIP与实际安装核对。
