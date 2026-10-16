# Windows 完整包与原生 MCP 验证

入口：`.github/workflows/craft-windows.yml`，运行于 `windows-2022`，覆盖 13 个 Craft 插件。此流水线验证 Windows 安装和 MCP 启动，不替代 Windows 桌面内嵌 UI 或编辑同步验收。

## 检查内容

1. 检查下载的 index.json 和每个 ZIP 的 SHA-256；解压前拒绝路径越界、符号链接、Windows 保留名、ADS 路径、尾部空格/点及大小写冲突。
2. 检查主体与 Codex 清单版本、包内 adapter、增强运行时逐文件摘要，或官方 Web 包的启动文件与 WASM。
3. 安装至含中文和空格的目录，使用独立 CODEX_HOME，不修改用户配置。
4. 通过固定版本 `@openai/codex@0.162.1` 的原生安装器添加本地市场并安装插件；通过真实 app-server 发现 MCP、调用 editor_status、open_browser_editor，确认工作区解析和页面资源可访问。不开模型推理，不需要 API Key，不使用 MCP SDK 替代。
5. 保存安装日志、原生 RPC 和 result.json。HTML 可访问不标记为编辑器渲染或同步通过。

Windows 使用 `node <npm 全局目录>/@openai/codex/bin/codex.js` 调用 CLI，避免 `.cmd` 与 shell 引号转换影响含空格路径。

## 触发方式

- push / PR：执行 Windows 路径与异常包回归。
- 完整安装回归：workflow_dispatch 提供 `index_url` 和 `index_sha256`；或设置仓库变量 `CRAFT_WINDOWS_INDEX_URL`、`CRAFT_WINDOWS_INDEX_SHA256` 后由 push / PR 执行。URL 必须是 CI runner 可下载的 HTTPS 地址。
- index 使用 `scripts/package-craft-editors.py` 输出的格式；ZIP 与 index.json 放在同一下载目录，文件名、plugin、sha256 均从该索引读取。
- 没有提供完整包来源时，安装任务显示 skipped；路径单测绿色不代表 Windows 安装通过。

完整候选位于本机 `.local/craft-host-recovered-final/`，并已上传为[测试预发布制品](https://github.com/partme-ai/full-aigc-plugins/releases/tag/craft-windows-test-20261016-905f7aa)。源码 checkout 没有完整 dist，不能拿源码包替代可安装包，也不能依赖临时下载官方包掩盖发行物缺件。

## 本轮状态

2026-10-16：在用户授权下提交、推送并上传 13 个候选 ZIP。真实 Windows Server 2022 x64 runner 上，8 项回归测试及 13/13 个插件原生安装、MCP 调用、编辑器 HTML 访问全部通过。

- [成功运行 38914576783](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38914576783)，测试代码提交 `59a18fd0d937e872aeaaa9d7ff967467f596cc8b`。
- 固定索引 SHA-256：`b2c04c7441c6cbc34cc9c4c608b6c31cb50367cddc13be82eb39f65fefe18c46`，各包摘要见测试制品 index.json。
- 首轮 GridCraft、PrintCraft 在宿主 `starting` 状态下被脚本过早判错；修复为限时等待连接完成，终态失败仍立即失败。修复后全矩阵重新通过，未更换候选包。
- 原生宿主为 Codex CLI 0.162.1；没有通过 MCP SDK 替代宿主加载。
- Windows 桌面内嵌 UI、编辑同步、ZCode/Kimi 的 Windows 宿主、独立 `*craft-cli.exe` 及其业务操作仍未验证。这次通过不能直接证明用户尚未提供原文的 CLI 报错已经修复。
- 插件内置 Web 运行包不自动安装各应用独立 CLI。独立 CLI 场景仍需相应可执行文件及其运行依赖；不能把插件安装成功等同于独立 CLI 已安装。

文档内的成功结果只覆盖以上固定候选与固定 CI 提交。未来改动运行包后须更新测试制品索引并重跑。
