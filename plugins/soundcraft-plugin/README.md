# SoundCraft Use

当前准备中的开发候选：`0.1.0-dev.20261018.4`（尚未发布）。新增播客实际片段输入助手；原生macOS/Windows与真实Codex同会话限定验证已通过，中文后备字体Web构建、真实Codex同页面字形与音频回归已通过，运行锁已指向待发布的新资源；公共发行尚未创建。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

Plugin display name: **SoundCraft Use**. Official upstream icon provenance and licenses are included under `assets/official-icon-source.json` and adjacent LICENSE files.

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## 场景操作手册

新增8条带具体命令、参数和效果检查的流程，见 [soundcraft-scenario-playbooks](skills/soundcraft-scenario-playbooks/SKILL.md)。输入坐标与时长须现场重算，原生技术验证与真实素材效果状态独立记录。

## 配音核心场景回归

配音混音、对话分段增益、音频母版交付三项核心指导已补齐明确轨道/片段和时间范围，通过Windows原生main合成信号与保存重开检查。原8条手册与6条核心，共14条具备限定技术回归。播客淡变、同源切口、音乐小样的片段结构与采样结果已另行核对；这不等于完整播客降噪、音乐制作或真实素材试听通过。真实试听、响度标准及宿主画面同步未验收。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

## 对时静音与有限循环开发候选

新增 `soundcraft-voice-silence-gaps` 与 `soundcraft-finite-audio-loop`，参考Audacity固定GitHub提交的工作流事实，原创映射实际方法、参数、ID及采样检查。官方0.7.0 macOS实际完成两场景11次CLI，保留原时轴、循环三份/展开及源文件保护通过；Windows完整16记录与输出摘要复核通过；隔离本地候选已通过真实Codex MCP与内置浏览器限定同步、scraftz保存重开及独立CLI音频回读。发行记录见目录仓；真实素材试听和其他宿主待验证。双麦克风拆轨在0.7.0导出时左右内容未分离，本批不提供该技能，不以轨道元数据当成音频正确性证明。
