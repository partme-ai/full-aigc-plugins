# LightCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.5`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


待发布开发预发行 `0.1.0-dev.3`，包含技能库六项技能的受摘要保护快照。`candidate-source.json` 锁定已公开来源 v0.1.0-dev.1 / 87fe7ce；`source-suite.json` 记录来源版本，原生版本独立为 `0.2.1`。插件运行不需要来源仓库。

已实现持久任务锁、原子状态、只读核对、停止请求、明确剩余步骤建议、有界修订、绑定目标/原片/候选/设置的审阅，以及独立重开交付门禁。`.codex-plugin/plugin.json` 是最小接入清单；不添加自动 hooks。来源升级默认只预检，拒绝快照漂移或用户修改。

```bash
python3 -I -B scripts/validate_package.py
python3 -I -B -m unittest discover -s tests -v
python3 -I -B scripts/controller.py --help
```

控制器通过 `init/run/status/inspect/reconcile/stop/remaining/review-request/review/revise/deliver` 显式调用。run 可能触发原生安装；只在已有授权内执行。inspect/reconcile 不启动原生程序，UNKNOWN 不重放。

输入 JSON、恢复与审阅交接见 [控制器操作契约](docs/controller.zh-CN.md)。

主 OpenSpec 任务 **26/26** 完成，主变更适用验收与公开开发预发行已完成。已通过宿主安装/发现、缓存控制器原生闭环与合成图视觉审阅；Codex 0.161.0 六技能隔离环境的五类宿主场景已通过，全量技能环境仍有上下文预算限制；Git main 已推送，Python 3.11/3.12/3.13 远端离线 CI 全部通过；插件开发预发行 v0.1.0-dev.2 已公开，锁定技能库 v0.1.0-dev.1。三个 P3 独立扩展变更保持 OPEN。

[任务与规格](openspec/README.md) · [当前证据及差距](docs/verification/implementation-evidence.md) · [分层报告](docs/verification/local-report.json) · [架构](docs/architecture.md) · [回执与来源同步](docs/task-receipts.zh-CN.md)

本轮候选状态与实际证据以 [六目标验收记录](docs/verification/windows-20261008/README.md) 为准，历史版本通过记录不能代替当前候选验收。

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

插件展示使用上游官方图标；名称为 **LightCraft Use**。图标来源与许可证保存在 `assets/official-icon-source.json` 和相邻 LICENSE 文件中。

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
