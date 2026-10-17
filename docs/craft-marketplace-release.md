# Craft 插件库开发候选

当前 DesignCraft、PdfCraft、EffectCraft、PhotoCraft、WordCraft、VectorCraft 候选为 `0.1.0-dev.20261017.6`，FilmCraft 为 `0.1.0-dev.20261017.7`，其余 6 个 Craft 保持 `0.1.0-dev.20261017.5`。Codex 的 Git 市场仓现在包含固定发行提交的完整薄包快照，入口为 `./plugins/<app>-plugin`；原生列表可在安装前读取包内官方logo和composerIcon。独立插件仓、不可变标签和其他宿主ZIP交付保留；运行资源仍固定到已核验的dev.20261017.2，未升级引擎。

本次修正的动因：Git插件条目的回退列表不解析包内图片，官方源码及本机原生plugin/list均可复现。仅补composerIcon无法改变未安装列表。快照包含技能、MCP清单、官方图标及bootstrap，不增加Agent运行时，亦不将全部创作和宿主同步视为通过。

## PhotoCraft dev.20261017.6 老照片工作流深化

完善已有老照片技能的五条方法及两阶段检查，场景总数保持210。macOS/Windows合成夹具验证局部保护区、原层保留、可编辑色阶、保存重开；真实Codex原生MCP及内置浏览器中，v5已安装实例的同一画布观察到修补、工作层及色阶同步，v6复用完全相同运行资源，不将v5视觉样例写成v6新增GUI验收。公开v6完整ZIP安装、22个技能发现、MCP基础调用和资源摘要通过。全局渲染Web/CLI最大1/255差异、首次下载404后内置回退均保留；真实旧照片质量与其他宿主仍未证明。已按feature→test→main发布，源码提交`211af69fcba564f8ea75c35e0eb50ac4d44a8ee4`；test三组CI通过，main同源码[市场27项](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39037360133)、[安装/MCP 14项](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39037360144)、[13应用业务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39037360174)也全部通过。实际订阅刷新errors为空，原生列表版本v6且独立修复计划存在、图标有效。详见[回归记录](craft-photo-restoration-validation.json)。

## EffectCraft dev.20261017.6 场景技能交付

新增章节标题卡、3–2–1倒数和滚动署名三个独立技能，冻结基础技能源与v2编辑器资源保持不变。macOS和Windows完整九场景原生回归通过，新增各500张PNG已解码；Windows下载616个产物逐项核验摘要并比对真实执行argv与技能步骤。完整公开ZIP已通过真实Codex安装、26个技能发现、MCP基础调用和ui/dist摘要检查。已按feature→test→main发布，源码提交`1b3c4c16e217b0e8d08d8f01153f4d25073a437c`；test三组CI全部通过；main同源码[市场27项](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39035230105)、[安装/MCP 14项](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39035230058)、[13应用业务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39035230081)也全部通过，实际订阅刷新errors为空，原生列表确认v6、26技能及三个新入口，logo/composerIcon有效。详见[回归记录](craft-effect-delivery-validation.json)。合成样本不代表真实成片、MCP场景编辑或宿主同步通过。

## DesignCraft / PdfCraft dev.20261017.6 场景技能交付

DesignCraft 增补实际四页宣传册、A3 活动海报的逐步配方、参数及脚本编译器；PdfCraft 增加报告书签、审阅水印、发票拆分、分节页码、可点击议程和修订对比六个独立技能。两包合计35个技能入口。每项保留固定GitHub来源、许可、真实命令参数与输出检查，生产创作及同画面同步仍未全部验收。

两份不可变完整ZIP已发布，远端标签提交和GitHub制品摘要已核验；市场快照直接来自对应发行提交，仍复用已验证的dev.20261017.2编辑器资源。公开完整ZIP已重新下载、校验并干净解包：真实Codex安装、35个技能发现、MCP调用、编辑器HTML及安装后ui/dist逐文件摘要通过，见 [v6安装结果](craft-v6-installation-validation.json)。完整ZIP与薄包Git安装分别验证，不将编辑器HTML可访问作为视觉或同步验收。源技能的macOS和Windows业务检查见 [PDF场景](craft-pdf-delivery-validation.json)、[宣传册](craft-brochure-validation.json)、[海报](craft-poster-validation.json)。

已按feature → test/20261017 → main发布，主库提交`46078cf39601f800030028cae727aaac827d4f5d`。test分支市场Git/ZIP的27项、Windows安装/MCP及13应用CLI业务CI全部通过。实际订阅市场定向刷新返回errors为空，桌面附带Codex原生plugin/list返回两个v6可安装条目，市场包包含15/20个技能和有效logo/composerIcon。没有安装进日常用户配置，公开ZIP安装验收使用隔离配置。main同提交的[市场Git/ZIP 27项](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39033717411)、[Windows安装/MCP 14项](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39033717426)及[Windows CLI业务13应用](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39033717250)全部通过。

Blender 市场安装引用已独立修复为真实存在的v0.14.1，主市场提交a68a407；本次两项候选同步保留该修复。

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

## FilmCraft dev.20261017.7 三个具体剪辑场景

新增定格说明、讲解画中画、采访 J-cut 三个独立技能。macOS 九场景117次、Windows九场景123次原生CLI操作通过；Windows下载73个输出摘要一致。完整候选ZIP通过真实Codex安装、24个技能发现、MCP基础调用和编辑器HTML检查。运行资源沿用dev.20261017.2；真实素材语义、主观音质和宿主同步尚未验收。详见[回归记录](craft-film-delivery-validation.json)。

FilmCraft v7已按feature→test→main进入主市场，当前源码提交`a030e9291b4987e3f67b74a3aba9ee53e1866fd6`。test三组CI全部通过，实际订阅刷新errors为空；桌面原生plugin/list确认v7、官方logo/composerIcon及三个新技能文件，市场包共24技能。日常配置中仍显示未安装；隔离真实Codex安装与MCP通过，不将列表可见写成日常已安装。main同源码三组CI也全部通过：市场27项（39039823429）、Windows安装/MCP14项（39039823442）、13应用原生业务（39039823453）。

## WordCraft dev.20261017.6 文档排版场景

新增可更新目录、图片题注、横向附录三个独立技能。macOS/Windows官方0.7.0原生17场景均通过；Windows54个输出和原始配方摘要一致。真实Codex完整包安装与MCP基础调用通过，发现15个技能。此候选复用v2运行资源；真实文档质量、长文档分页和宿主内编辑同步未验收。详见[回归记录](craft-word-publishing-validation.json)。

WordCraft v6已按feature→test→main进入主市场，源码提交`a5249f6a5b9fb58b84538c3f6efadb906ed0b209`。test市场27项（39041041036）、安装/MCP14项（39041154003）、13应用业务（39041153991）通过。实际订阅刷新errors为空，桌面原生列表确认v6、15技能及三个新入口，logo/composerIcon存在；日常配置未安装，隔离真实宿主安装与基础MCP调用已通过。main同源码三组CI全部通过：市场27项（39041454980）、Windows安装/MCP14项（39041454996）、13应用业务（39041454975）。

## VectorCraft dev.20261017.6 制作场景

新增可释放蒙版、共享源阵列、独立偏移白边三个技能。20场景加1个已有文档保护用例通过macOS/Windows原生回归；公开完整ZIP安装、25技能发现、MCP基础调用和已安装资源摘要检查通过。复用固定v2编辑资源；真实设计与印刷质量及其他宿主同步未验收。隔离的真实Codex原生MCP和内置浏览器已观察到阵列改色/改行列、蒙版释放及白边生成；五个实际保存工程由独立CLI重开检查通过。此限定样例不代表所有编辑动作或其他宿主已通过。详见[回归记录](craft-vector-production-validation.json)。
