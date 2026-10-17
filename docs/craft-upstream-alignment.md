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
| vectorcraft | [v0.12.0](https://github.com/storytold/vectorcraft/releases/tag/v0.12.0) | 待升级至新发布版 | 122 |
| deckcraft | [v0.7.0](https://github.com/storytold/deckcraft/releases/tag/v0.7.0) | 同一提交 | 721 |
| soundcraft | [v0.7.0](https://github.com/storytold/soundcraft/releases/tag/v0.7.0) | 同一提交 | 3 |
| gridcraft | [v0.7.0](https://github.com/storytold/gridcraft/releases/tag/v0.7.0) | 同一提交 | 7 |
| wordcraft | [v0.7.0](https://github.com/storytold/wordcraft/releases/tag/v0.7.0) | 同一提交 | 274 |

VectorCraft0.12原生CLI已下载并核对官方SHA256：使用真正0.11与0.12二进制比较，命令749→770，新增21个、72个参数描述变化；原生MCP的两个目录入口新增query/menu/brief。原有Windows CI已经固定0.12，旧观察目录来自0.12，不能作为0.11基线。插件适配层补齐目录检索兼容，保留引擎enabled状态。旧AI7导出已分别通过CLI与原生stdio MCP实际执行，重开检查组/图层/活文字和母版不变。技能新增具体调用与版本边界，未扩大198条场景计数。

内嵌引擎仍是0.11，尚未将旧AI导出等引擎行为标成内嵌可用。原生0.12与旧内嵌版本并存必须明确说明，不能只改source.lock或editor.lock冒充构建完成。

DesignCraft、PhotoCraft、PrintCraft固定源码分别比对应发布标签多418、205、212个提交；它们不是仅凭显示版本就可判为落后。EffectCraft、FilmCraft、LightCraft采用对应官方Web发布包。主线比固定点更新不等于新增命令，包含UI、导入导出、性能、正确性和CI修复。

GitHub compare最多返回300个文件/默认250个提交；DesignCraft、FigCraft、LightCraft、DeckCraft、WordCraft的初次差异超过该范围，结构化报告明确标为截断，未把它们当成完整能力审计。未发布主线的运行时迁移及真实宿主同步仍待完成。

详细提交、上游链接、来源范围及本地验证见[结构化对齐记录](craft-upstream-alignment.json)。

已将本地适配器页面在Codex内置浏览器中实际加载，并通过同一编辑器工具桥调用目录：query graph.返回5条、Object > Path返回11条、完整graph.setType返回1条且保留参数。该测试证明浏览器与适配器的目录兼容，不是已安装插件的宿主MCP调用验收。4项适配器回归通过。
