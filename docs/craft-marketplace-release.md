# Craft 插件库开发候选

当前候选统一为 `0.1.0-dev.20261017.5`。Codex 的 Git 市场仓现在包含固定发行提交的完整薄包快照，入口为 `./plugins/<app>-plugin`；原生列表可在安装前读取包内官方logo和composerIcon。独立插件仓、不可变标签和其他宿主ZIP交付保留；运行资源仍固定到已核验的dev.20261017.2，未升级引擎。

本次修正的动因：Git插件条目的回退列表不解析包内图片，官方源码及本机原生plugin/list均可复现。仅补composerIcon无法改变未安装列表。快照包含技能、MCP清单、官方图标及bootstrap，不增加Agent运行时，亦不将全部创作和宿主同步视为通过。

## dev.20261017.5 图标发布验收

已按 feature → test/20261017 → main 发布，发行提交为 `7febc0370ca4b5e181d4b79276ea144f7330f2e3`。本机实际订阅市场检出该提交；Codex 0.162.1 和桌面附带的 0.162.0-alpha.17.2 原生 `plugin/list` 均返回13个v5条目，`logo`、`logoDark`、`composerIcon` 对应文件存在且SHA-256与独立插件仓官方PNG一致。此前13个v4条目的logo均为空。详见 [结构化结果](craft-icon-listing-validation.json)。

main 的市场安装工作流 [39028960653](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39028960653) 27项全部通过；[Windows安装/MCP](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39028960677)与[Windows业务回归](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39028960706)也通过。本机隔离安装13包的原生技能发现、MCP调用和编辑器HTML通过。以上不替代桌面列表刷新后的截图、编辑器视觉和同画面编辑同步验收。

本机定向市场升级命令报告另一个条目 `blender-design` 引用的 `v0.15.0` 不存在；市场Git索引实际已更新，随后两个原生宿主均正确读取13个Craft图标。该错误未记为整体升级成功，亦未修改Blender。独立candidate-marketplace保留远端Git来源；此处安装前图标结论对应用户订阅的主市场。

## 此前dev.20261017.4交付与验收记录

13 个插件统一为 `0.1.0-dev.20261017.4`。这是可安装开发预发布，生产发布仍 BLOCKED；并非全部上游 main 能力及全部场景已验收。

市场使用固定 Git 标签，官方图标也按标签固定。根 Agent Plugins MCP 和 Codex、ZCode、Kimi 入口统一执行 `ui/bootstrap.mjs`。Git 安装首次启动下载插件发行资源并核验 SHA-256，完整 ZIP 自带资源；运行要求 Node.js 24，不需要 Rust 或 npm 构建。

首次启动需要能访问 GitHub Releases；下载失败、摘要不符、非法路径或不支持的归档类型均拒绝执行，并输出 stderr 诊断。已验证的完整包/缓存允许离线启动。版本摘要详见各仓 `ui/runtime.lock.json`；编辑器原有上游来源保留在制品 BUILD/config 中，不与本次插件版本混为一谈。

## 验证状态

- 23项针对性归档、候选目录与可移植 MCP 回归通过，26份根 plugin/MCP 配置通过官方1.0.0 JSON Schema。
- 13个完整ZIP通过Windows路径与资源摘要预检，包含原有 editor.lock.json 与新的 runtime.lock.json 双重检查。
- 修正版13 个公开完整 ZIP 经下载、干净解包及真实 Codex 安装，原生 app-server MCP 的 `editor_status`、`open_browser_editor` 调用及编辑器HTML访问通过。
- 原生 `skills/list` 按安装路径核对187个技能入口，均已发现并启用；这不代表模型路由或187项创作质量验收通过。
- 修正版 Windows Git 安装13项、完整ZIP安装13项及Linux同时冷启动1项，共27个CI任务全部通过：[运行39021467206](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39021467206)。随后刷新主市场。
- 本轮未将上述安装检查计作13种编辑器的画面同步、创作效果或ZCode/Kimi全部宿主验收。

## 制品选择

CAD、Photo、Fig 使用此前已验证的 main Web 制品；Vector 使用0.12.0源码制品；Design、Deck、Sound、Grid、Word、Pdf 使用固定源码构建，Effect、Film、Light 使用已锁定官方Web包。其余尚未纳入的main能力继续按独立开发候选验证，不能由市场可安装性推定通过。源码目录的活动 ui/dist 未被覆盖，发行包在独立目录组装。

初次组包发现9个增强编辑器的旧 editor.lock.json 与本地残留制品不一致。初次dev.20261017.1未合入主市场；最终dev.20261017.2改用匹配来源的制品，重建适配器并刷新实际发行资源锁，重新执行完整包与宿主检查。

## 本轮发布边界

用户最终授权全部合入main，按feature→test/20261017→main处理13插件、13独立技能源及目录仓。插件版本统一为dev.20261017.4；技能快照、原生CLI和Web上游版本按各自锁定来源独立记录。

dev.20261017.2的公开冷启动实测暴露Codex实际30秒握手限制（忽略清单超时字段），多个大制品首次下载使部分服务超时。dev.20261017.3使用固定描述符立即完成MCP握手/发现，在首次工具或资源调用时准备运行时；复用已核验的dev.20261017.2运行资源。21项回归覆盖无资源时握手、并发首次调用与协议转发。包中实际业务操作仍由原编辑器实现。

Windows Git检出DesignCraft历史长路径曾失败。Windows CI显式启用Git长路径支持，Git安装用户同样需要Git支持长路径；完整ZIP排除历史验收记录，原记录保留源码仓。此环境前提不能写成未经配置的Windows已验收。

独立候选库仍保留在candidate-marketplace/，供隔离测试；主库的13条目固定到相同开发标签。完整场景/创作质量和三宿主全部内嵌同步尚未全部验收，生产发布保持BLOCKED。

## 完整发行压缩包验收

Git标签安装与完整ZIP安装分别验收。`verify-craft-release-zip.py`从GitHub Release下载每个固定完整ZIP，验证整包SHA-256，在干净目录解包，再通过真实Codex安装器、skills/list、原生MCP调用与编辑器HTML进行验证；最后复核已安装ui/dist逐文件摘要，防止从外部缓存兜底掩盖包缺资源。Windows ZIP验收明确关闭Git长路径配置，避免把Git检出的环境配置冒充完整包能力。

Windows兼容修正版dev.20261017.4统一入口真实路径，能力描述符摘要按LF规范化后校验，兼容Git CRLF检出；二进制资源摘要仍逐字节核验。重新执行公开ZIP下载验收及Windows Git/ZIP双路CI，结果以对应运行记录为准。

ZCode的12个市场入口采用完整ZIP地址、整包SHA-256和包内目录，安装即带运行资源；EffectCraft官方WASM约60MiB，当前ZCode0.16.9实际安装被单文件50MiB上限拒绝，因此该应用显式保留固定Git入口，完整ZIP在其他已验收路径可用；Codex原生Git来源仍保留独立的首次下载兼容路径。两种交付不混称为相同机制。

本机ZCode0.16.9真实安装器已安装13个候选：12个完整ZIP的已安装ui/dist逐文件摘要通过；EffectCraft为上述Git兼容例外。此次ZCode检查只覆盖安装，MCP调用及内嵌编辑同步不在该结论中。可用`verify-craft-zcode-install.py --cli-js <宿主CLI路径> --output <新隔离目录>`复验，不修改日常宿主配置。
