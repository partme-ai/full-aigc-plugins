# Craft上游能力对齐（2026-10-17）

核对13个官方仓库的最新稳定发布、内嵌源码固定点及主分支。稳定发布版本与源码祖先关系已检查；主分支包含未发布工作，不能由目录或版本号推断全部可用。

| 应用 | 最新稳定版 | 内嵌相对发布版 | 主线后续提交数 |
| --- | --- | --- | --- |
| cadcraft | [v0.7.0](https://github.com/storytold/cadcraft/releases/tag/v0.7.0) | 同一提交 | 3 |
| designcraft | [v0.8.0](https://github.com/storytold/designcraft/releases/tag/v0.8.0) | 内嵌源码更新于发布版 | 1560 |
| effectcraft | [v0.10.0](https://github.com/storytold/effectcraft/releases/tag/v0.10.0) | 官方Web发布包 | 177 |
| photocraft | [v0.9.0](https://github.com/storytold/photocraft/releases/tag/v0.9.0) | 内嵌源码更新于发布版 | 70 |
| figcraft | [v0.6.0](https://github.com/storytold/figcraft/releases/tag/v0.6.0) | 同一提交 | 435 |
| filmcraft | [v0.8.0](https://github.com/storytold/filmcraft/releases/tag/v0.8.0) | 官方Web发布包 | 7 |
| lightcraft | [v0.8.0](https://github.com/storytold/lightcraft/releases/tag/v0.8.0) | 官方Web发布包 | 561 |
| printcraft | [v0.8.0](https://github.com/storytold/pdfcraft/releases/tag/v0.8.0) | 内嵌源码更新于发布版 | 8 |
| vectorcraft | [v0.12.0](https://github.com/storytold/vectorcraft/releases/tag/v0.12.0) | dev.65已构建并验证0.12内嵌候选 | 122（相对旧内嵌基线） |
| deckcraft | [v0.7.0](https://github.com/storytold/deckcraft/releases/tag/v0.7.0) | 同一提交 | 721 |
| soundcraft | [v0.7.0](https://github.com/storytold/soundcraft/releases/tag/v0.7.0) | 同一提交 | 3 |
| gridcraft | [v0.7.0](https://github.com/storytold/gridcraft/releases/tag/v0.7.0) | 同一提交 | 7 |
| wordcraft | [v0.7.0](https://github.com/storytold/wordcraft/releases/tag/v0.7.0) | 同一提交 | 274 |

VectorCraft0.12原生CLI已下载并核对官方SHA256：使用真正0.11与0.12二进制比较，命令749→770，新增21个、72个参数描述变化；原生MCP的两个目录入口新增query/menu/brief。原有Windows CI已经固定0.12，旧观察目录来自0.12，不能作为0.11基线。插件适配层补齐目录检索兼容，保留引擎enabled状态。旧AI7导出已分别通过CLI与原生stdio MCP实际执行，重开检查组/图层/活文字和母版不变。技能新增具体调用与版本边界，未扩大198条场景计数。

现已独立构建0.12内嵌候选并激活dev.65，保留0.11资源用于回退；根manifest与Codex/ZCode/Claude/Kimi版本一致。不能只改source.lock或editor.lock冒充构建完成。

DesignCraft、PhotoCraft、PrintCraft固定源码分别比对应发布标签多418、205、212个提交；它们不是仅凭显示版本就可判为落后。EffectCraft、FilmCraft、LightCraft采用对应官方Web发布包。主线比固定点更新不等于新增命令，包含UI、导入导出、性能、正确性和CI修复。

GitHub compare最多返回300个文件/默认250个提交；DesignCraft、FigCraft、LightCraft、DeckCraft、WordCraft的初次差异超过该范围，结构化报告明确标为截断，未把它们当成完整能力审计。未发布主线的运行时迁移及真实宿主同步仍待完成。

详细提交、上游链接、来源范围及本地验证见[结构化对齐记录](craft-upstream-alignment.json)。

已将本地适配器页面在Codex内置浏览器中实际加载，并通过同一编辑器工具桥调用目录：query graph.返回5条、Object > Path返回11条、完整graph.setType返回1条且保留参数。该测试证明浏览器与适配器的目录兼容，不是已安装插件的宿主MCP调用验收。4项适配器回归通过。

为补足compare截断，另读取13仓基线与主线的完整Git树（26份，均未截断），逐文件比较blob摘要。实现文件与API相关文件的变化路径已加入结构化记录；这补足文件变化范围，不把文件变化数量当作语义能力验收。

按真实0.11→0.12目录新增21个命令补充三条结构化场景：尺寸标注单位交付、交织重叠切换与释放、CSV可编辑文案版本。实际原生保存重开及派生渲染通过，并检查标注恢复单位、释放恢复遮挡、重开切换数据集。场景映射198→201；原8条手册、3条新增和1条既有工程组合在本地12例通过。新增能力不由旧版缓存目录推断。

## 最终验证范围

Windows运行39004180010绑定技能源9ce5ea0与目录仓4eb1ecc，13应用业务通过；VectorCraft11条手册加1组合、73次调用通过，下载50份输出核对摘要。既有安装/MCP运行39004179976通过，不证明dev.65已在宿主重新安装。早先39004029132误绑DeckCraft提交而失败，且VectorCraft仍读取旧配方，不能作为新增三条的证明；已修正并增加新版配方必需检查。

0.12内嵌候选在Codex内置浏览器实际加载，目录1058条（含UI命令，不能与原生770直接比总数），21个新增命令均存在；标注单位、交织、CSV三场景实际调用、画面同步与原生保存通过，另进程重开核验。宿主路径导出桥接修复后，AI7输出可重开，保留格式损失警告；越界和既存文件覆盖被拒绝。9项适配器测试包含实际Unicode文件写入，CI增加Windows/Linux矩阵。以上通过本地工具桥，未冒充已安装Codex/ZCode/Kimi的MCP验收。

当前201条场景映射：158条限定技术回归通过、1条部分通过、42条待执行，另有4组合用例。未发布main先作为候选；21个新增命令的存在与三个场景通过，不意味着所有新增方法均已完成业务验收。完整VectorCraft实现CI39003638135仍失败于两项release-gate合同测试，专项通过不替代整仓结果。

dev.65源码与技能已推送（插件eba3008、技能源11575de）。适配器Windows/Linux专项CI39004888523的9项测试均通过；文档CI39004989180与架构CI通过。完整实现CI39004888507仍未通过release-gate合同测试，不将其写成整仓通过。生成完整约56MB候选ZIP并通过Windows路径语义、五宿主版本及编辑器44文件摘要检查；未正式发布或将其冒充真实宿主安装通过。

## main候选扩展

用户已确认同时构建13仓main；当前main固定点、构建结果、实际业务及宿主同步验证分列见[main开发候选](craft-main-candidates.md)。原稳定版审计仍作为历史基线，不能代替main验证。
