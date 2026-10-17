# Craft 插件库开发候选

13 个插件统一为 `0.1.0-dev.20261017.3`。这是可安装开发预发布，生产发布仍 BLOCKED；并非全部上游 main 能力及全部场景已验收。

市场使用固定 Git 标签，官方图标也按标签固定。根 Agent Plugins MCP 和 Codex、ZCode、Kimi 入口统一执行 `ui/bootstrap.mjs`。Git 安装首次启动下载插件发行资源并核验 SHA-256，完整 ZIP 自带资源；运行要求 Node.js 24，不需要 Rust 或 npm 构建。

首次启动需要能访问 GitHub Releases；下载失败、摘要不符、非法路径或不支持的归档类型均拒绝执行，并输出 stderr 诊断。已验证的完整包/缓存允许离线启动。版本摘要详见各仓 `ui/runtime.lock.json`；编辑器原有上游来源保留在制品 BUILD/config 中，不与本次插件版本混为一谈。

## 验证状态

- 21项针对性归档、候选目录与可移植 MCP 回归通过，26份根 plugin/MCP 配置通过官方1.0.0 JSON Schema。
- 13个完整ZIP通过Windows路径与资源摘要预检，包含原有 editor.lock.json 与新的 runtime.lock.json 双重检查。
- 13 个完整 ZIP 经真实 Codex 安装，原生 app-server MCP 的 `editor_status`、`open_browser_editor` 调用及编辑器HTML访问通过。
- 原生 `skills/list` 按安装路径核对187个技能入口，均已发现并启用；这不代表模型路由或187项创作质量验收通过。
- 修正候选的 GitHub 标签干净安装、首次下载、Windows Git 安装 CI：正在执行。主市场刷新不在本轮范围内。
- 本轮未将上述安装检查计作13种编辑器的画面同步、创作效果或ZCode/Kimi全部宿主验收。

## 制品选择

CAD、Photo、Fig 使用此前已验证的 main Web 制品；Vector 使用0.12.0源码制品；Design、Deck、Sound、Grid、Word、Pdf 使用固定源码构建，Effect、Film、Light 使用已锁定官方Web包。其余尚未纳入的main能力继续按独立开发候选验证，不能由市场可安装性推定通过。源码目录的活动 ui/dist 未被覆盖，发行包在独立目录组装。

初次组包发现9个增强编辑器的旧 editor.lock.json 与本地残留制品不一致。初次dev.20261017.1未合入主市场；最终dev.20261017.2改用匹配来源的制品，重建适配器并刷新实际发行资源锁，重新执行完整包与宿主检查。

## 本轮发布边界

用户最终授权全部合入main，按feature→test/20261017→main处理13插件、13独立技能源及目录仓。插件版本统一为dev.20261017.3；技能快照、原生CLI和Web上游版本按各自锁定来源独立记录。

dev.20261017.2的公开冷启动实测暴露Codex实际30秒握手限制（忽略清单超时字段），多个大制品首次下载使部分服务超时。dev.20261017.3使用固定描述符立即完成MCP握手/发现，在首次工具或资源调用时准备运行时；复用已核验的dev.20261017.2运行资源。21项回归覆盖无资源时握手、并发首次调用与协议转发。包中实际业务操作仍由原编辑器实现。

Windows Git检出DesignCraft历史长路径曾失败。Windows CI显式启用Git长路径支持，Git安装用户同样需要Git支持长路径；完整ZIP排除历史验收记录，原记录保留源码仓。此环境前提不能写成未经配置的Windows已验收。

独立候选库仍保留在candidate-marketplace/，供隔离测试；主库的13条目固定到相同开发标签。完整场景/创作质量和三宿主全部内嵌同步尚未全部验收，生产发布保持BLOCKED。
