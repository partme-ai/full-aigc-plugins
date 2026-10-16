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

当前完整候选位于本机 `.local/craft-host-recovered-final/`，尚未上传给 GitHub runner。源码 checkout 没有完整 dist，不能拿源码包替代可安装包，也不能依赖临时下载官方包掩盖发行物缺件。

## 本轮状态

2026-10-16：actionlint 通过；5 项离线回归通过；13 个真实 ZIP 的预检查通过，执行平台为 macOS。Windows runner 未运行，Windows 桌面 UI 未验证。未提交、推送或发布。

同一 CI 驱动在 macOS 上已完成 CADCraft（增强运行包）和 EffectCraft（官方 Web 运行包）的隔离原生安装、app-server MCP 调用和页面资源检查，用于排除脚本自身的流程错误；这两项结果仍不是 Windows 验收。

要取得 Windows CI 结果，需要先将本次 CI 文件提交到可运行分支，并提供 runner 可访问的候选包与固定摘要。继续沿用既有不提交推送边界，未自行发布候选包。
