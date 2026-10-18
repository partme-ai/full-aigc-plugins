# PdfCraft Use

当前开发候选：`0.1.0-dev.20261018.2`。新增六类PDF交付场景；Codex市场使用完整薄包快照以在安装前读取官方图标。运行资源沿用已核验的dev.20261017.2，不代表引擎升级或全部创作验收通过。

## Installable editor development candidate

`0.1.0-dev.20261017.3` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


## Previous development candidate

`0.1.0-dev.20261017.1` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.


Prerelease **0.1.0-dev.6**: six digest-bound upstream skills plus a thin local Harness.
Independent execution/verification protocols preserve uncertain outcomes and require artifact review. Portable and generated Codex manifests share the product identity.

The upstream source is locked to a verified GitHub release, commit and 78 file digests. See project-status.json for publication status. Native sample, host, model-dispatch and release evidence remain separate.

See [中文说明](README.zh-CN.md), [host support](docs/host-support.md), [implementation evidence](docs/verification/implementation-2026-10-08.md), and [OpenSpec tasks](openspec/changes/harden-printcraft-plugin-delivery/tasks.md).

Install the prerelease after adding the marketplace:

```bash
codex plugin marketplace add partme-ai/full-aigc-plugins
codex plugin add printcraft@full-aigc-plugins
```

Codex is the tested host. Craft/Kimi manifests are generated metadata; runtime and model acceptance are NOT_RUN. Chinese OCR, other native platforms and mobile delivery remain open.

Explicit optional Tesseract Chinese OCR is available through Harness `ocr`; pinned native OCR remains English-only. Native PDF reading order and full-phrase search have known limitations; see [Chinese OCR evidence](docs/verification/external-ocr-2026-10-08.md).

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 内嵌编辑器候选

新增 MCP Apps 与宿主浏览器接入，详见 [配置与构建](docs/editor-integration.md)。`ui/dist/` 为本地生成物；首次分发须带齐生成物。

Plugin display name: **PdfCraft Use**. Official upstream icon provenance and licenses are included under `assets/official-icon-source.json` and adjacent LICENSE files.

源码增强候选采用 `ui/source.lock.json` 与 `ui/build-source.py`；兼容更新查询本插件自有 GitHub Releases，失败回退内置，原版 Web 不替换增强自动化运行时。当前会话保留；宿主安装验收另行记录。

## main交付检查候选

新增[main工具指导](skills/printcraft-pdf-preflight/references/main-workflows.md)：所选页字数、未标记内容定位及7个新增工具/16处契约变化。新增统计/定向检查已通过Windows main专项39008588714；不等于完整无障碍认证，不改变既有中文表单外观限制。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

### Windows 启动兼容修正

规范化入口真实路径，能力清单校验统一使用 LF 换行，兼容 Windows Git CRLF 检出。

### 候选启动修正

本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。

## PDF交付场景技能

以下独立技能自带完整步骤、当前原生工具schema、来源固定提交及CLI脚本编译器；不会改动冻结的六个基础技能。命令目录和技术回归不代表所有真实PDF或宿主同步已验收。

| 技能 | 任务与交付 |
| --- | --- |
| `printcraft-report-bookmarks` | 按确认章节页建立层级书签，保留原页内容 |
| `printcraft-review-watermark` | 只给选定审阅页加水印，检查非目标页不变 |
| `printcraft-invoice-split` | 按确认的单据起始页拆包，逐页核对无丢失与跨单据 |
| `printcraft-section-pagination` | 前言与正文分别添加可见页脚编号，区分PDF物理页和阅读编号 |
| `printcraft-linked-agenda` | 议程与附录双向内部跳转，核对热点和目标页 |
| `printcraft-revision-compare` | 对照新旧PDF生成文字差异报告，保留两个原件 |

本批作为开发候选集成，实际安装版本以市场条目和对应发布标签为准。当前后端工具缺失时如实报告，不将示例ID、页号和坐标直接套用真实文件。

表单场景新增基于实际字段的填写请求辅助工具；插件宿主在填写完成后触发视图重绘，指定英文文本/复选框样例经真实Codex验证。中文字体外观仍未通过，Windows包装层界面与其他宿主尚待验收。编辑器资源保持不变。
