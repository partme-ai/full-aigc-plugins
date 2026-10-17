# WordCraft Use

当前可安装开发候选：`0.1.0-dev.20261017.6`。补齐官方输入框图标，Codex市场使用完整薄包快照以在安装前读取列表图标；运行资源沿用已核验的dev.20261017.2，不代表上游引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## 场景技能开发候选

当前包含 13 个领域场景技能、1 个内嵌编辑器入口和1个场景操作手册。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

插件展示使用上游官方图标；名称为 **WordCraft Use**。图标来源与许可证保存在 `assets/official-icon-source.json` 和相邻 LICENSE 文件中。

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## 场景操作手册

新增 `wordcraft-scenario-playbooks`：8 条带具体命令、参数与检查的流程，见 [技能入口](skills/wordcraft-scenario-playbooks/SKILL.md)。示例数据需替换，实际运行与创作效果状态见命令证据；不将目录存在当验收通过。

## 常用文档模板

首批六类模板，按文档任务直接选择；2个既有技能增强，新增4个独立入口。模板是章节、填字段指导和原生排版操作，不是只换标题的空提纲。

| 文档 | 技能 |
| --- | --- |
| 会议纪要 | [wordcraft-meeting-minutes](skills/wordcraft-meeting-minutes/SKILL.md) |
| 工作周报 | [wordcraft-weekly-report](skills/wordcraft-weekly-report/SKILL.md) |
| 项目方案 | [wordcraft-business-proposal](skills/wordcraft-business-proposal/SKILL.md) |
| 需求说明 | [wordcraft-requirements-document](skills/wordcraft-requirements-document/SKILL.md) |
| 验收报告 | [wordcraft-acceptance-report](skills/wordcraft-acceptance-report/SKILL.md) |
| 业务函 | [wordcraft-business-letter](skills/wordcraft-business-letter/SKILL.md) |

每种有独立的填写指南、虚构输入示例和可编辑表格。六份示例已通过Windows实际DOCX/PDF生成、重开与页面审阅，见[验证范围](docs/document-templates-validation.md)。长文档与真实宿主同步另行验证。

## main开发候选指导

新增[main工作流](skills/wordcraft-scenario-playbooks/references/main-workflows.md)：原生页眉页脚、筛选排序邮件合并，以及12个新增命令和27处参数变化。以固定main实际目录为依据，两个新流程已通过Windows原生main专项业务回归39007814128；不计入已有8条手册通过数，不宣称稳定版支持。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

## 具体文档排版场景开发候选

新增可更新目录手册、带图片题注的操作指南、纵向正文与横向矩阵附录三个独立技能，均包含自足方法、参数及可编辑结构检查。当前为未发布场景候选；不代表宿主同步和真实文档全部排版验收。
