# Craft 插件库开发候选

13 个插件统一为 `0.1.0-dev.20261017.1`。这是可安装开发预发布，生产发布仍 BLOCKED；并非全部上游 main 能力及全部场景已验收。

市场使用固定 Git 标签，官方图标也按标签固定。根 Agent Plugins MCP 和 Codex、ZCode、Kimi 入口统一执行 `ui/bootstrap.mjs`。Git 安装首次启动下载插件发行资源并核验 SHA-256，完整 ZIP 自带资源；运行要求 Node.js 24，不需要 Rust 或 npm 构建。

首次启动需要能访问 GitHub Releases；下载失败、摘要不符、非法路径或不支持的归档类型均拒绝执行，并输出 stderr 诊断。已验证的完整包/缓存允许离线启动。版本摘要详见各仓 `ui/runtime.lock.json`；编辑器原有上游来源保留在制品 BUILD/config 中，不与本次插件版本混为一谈。

## 验证状态

- 针对性归档与可移植 MCP 回归通过。
- 13 个完整 ZIP 经真实 Codex 安装，原生 app-server MCP 的 `editor_status`、`open_browser_editor` 调用通过。
- GitHub 标签的干净安装、首次下载、Windows Git 安装 CI 与订阅主市场刷新：正在执行。
- 本轮未将上述安装检查计作13种编辑器的画面同步、创作效果或ZCode/Kimi全部宿主验收。
