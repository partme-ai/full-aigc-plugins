# 13仓main开发候选

2026-10-17用户确认将13仓main同时构建适配，候选明确标记为未验收。固定上游提交、插件构建适配提交与技能源提交见[候选清单](../scripts/ci/craft_main_candidates.lock.json)。原有稳定版来源锁和活动编辑器均保留；未正式发布或替换全局安装。

| 应用 | main固定提交 |
| --- | --- |
| cadcraft | [9b2308b138e9](https://github.com/storytold/cadcraft/commit/9b2308b138e90a01d28d46c84021a74b1ae7ef4a) |
| designcraft | [fc36957fe05f](https://github.com/storytold/designcraft/commit/fc36957fe05f38a6976df4734d52b9250cd54a2c) |
| effectcraft | [8f02f52a44a4](https://github.com/storytold/effectcraft/commit/8f02f52a44a4b1ea807d8824b92301b96f896a06) |
| photocraft | [5f65579ecb44](https://github.com/storytold/photocraft/commit/5f65579ecb44047c2a619036c18ff273202e1389) |
| figcraft | [d1d8c3f652ce](https://github.com/storytold/figcraft/commit/d1d8c3f652cea20bee02bdbc3ded9a2f5362ba08) |
| filmcraft | [09aaf9bf15d5](https://github.com/storytold/filmcraft/commit/09aaf9bf15d510eda1c413c0ccabb1d7e08b41c5) |
| lightcraft | [f34c7a8a89e0](https://github.com/storytold/lightcraft/commit/f34c7a8a89e0d1bade0a6889185f40acecc84a9f) |
| printcraft | [924c4da4ac28](https://github.com/storytold/pdfcraft/commit/924c4da4ac2879ac9107c6c82e20ac6be5570f0a) |
| vectorcraft | [8bc65329286d](https://github.com/storytold/vectorcraft/commit/8bc65329286dc1b84aa392997bb205613c3e96cb) |
| deckcraft | [1dc69720db64](https://github.com/storytold/deckcraft/commit/1dc69720db64323370dda061226becb09ad79fd4) |
| soundcraft | [f3a19480d8cc](https://github.com/storytold/soundcraft/commit/f3a19480d8cc2d7a98cda492f5464d8c54558c9f) |
| gridcraft | [f1894c6da64d](https://github.com/storytold/gridcraft/commit/f1894c6da64d4326022ae644c767581816a23c2c) |
| wordcraft | [eae242176108](https://github.com/storytold/wordcraft/commit/eae242176108d328c5dd81fbc10370c51ab90706) |

13个固定main均已完成Web编译、Windows原生CLI构建与既有业务回归。构建只发生在隔离副本，源仓保持只读；不替换当前稳定版、全局安装或正式发行。候选产物继续标为`UNACCEPTED`。完整原生目录比较见[能力差异](craft-main-capability-deltas.json)：基线是实际观察到的稳定版CLI目录，并非旧嵌入式引擎。参数契约不变也不能证明所有语义不变。

## 实际CI

| 范围 | 成功运行 |
| --- | --- |
| Web：CAD、Design、Effect、Film、Light、Print、Vector、Word | [39006638202中的对应Web任务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39006638202)，该轮整体有失败 |
| Web：Grid、Sound、Fig、Deck | [39006903491中的对应Web任务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39006903491)，该轮Photo失败 |
| Web：Photo，含中文字体修复 | [39009228204](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39009228204) |
| Windows：Grid、Sound | [39007057957](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39007057957) |
| Windows：CAD、Fig | [39007496391对应任务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39007496391)，该轮Deck失败 |
| Windows：Deck、Word，含Word新增业务 | [39007814128](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39007814128) |
| Windows：Design、Print、Film、Vector、Effect、Light | [39007949879](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39007949879) |
| Windows：Photo，含上游两项预设持久化测试 | [39008034368](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39008034368) |
| Windows：Print新增文字统计与无障碍检查 | [39008588714](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39008588714) |
| Windows：Film关联素材单侧删除与撤销 | [39011329666](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39011329666) |
| Windows：Deck实际starter和品牌页复用 | [39010982169](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39010982169) |
| Windows：Light新增模板恢复和联系印样PDF | [39010884426](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39010884426) |
| Windows：Design新增SVG导入与可编辑PPTX交付 | [39008681404](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39008681404) |

原生报告及落盘输出摘要已核对。复验使用同一份已校验SHA-256的main二进制；测试报告保留二进制构建时的插件固定点和本次技能源固定点，不把后续纯文档提交冒充旧CI执行版本。源提交与插件构建适配见每份CI provenance；候选清单记录当前适配源码，不能反推所有历史产物均由最新文档提交构建。

新增流程的结构化验证摘要见[业务验证](craft-main-new-workflow-validation.json)。

## 差异与技能补充

| 应用 | 原生目录差异 | 已补充到独立技能源与插件的内容 | 新流程验证 |
| --- | --- | --- | --- |
| PhotoCraft | +9方法、17契约变化 | 导出预设CRUD、参数映射、图层列表及其他五类方法边界 | Codex原生宿主预设CRUD、320×240 JPEG交付、两层工程列表通过；其余方法未专项执行 |
| WordCraft | +12、27变化 | 原生页眉页脚、筛选排序邮件合并 | Windows实际DOCX部件、收件人顺序、重开读取通过 |
| DesignCraft | +60、119变化 | SVG导入、可编辑PPTX、Flex操作指引 | Windows原生保存重开、活文字与矢量对象PPTX、PDF通过；Flex未执行 |
| PrintCraft（上游PdfCraft） | +7 MCP工具、16变化 | 文字统计、选定无障碍规则及其能力边界 | Windows统计3个英文词、重复页去重、未标记内容检测及输入摘要保持通过；非完整无障碍认证 |
| LightCraft | +58、7变化 | 联系印样PDF、版式模板、蒙版效果模板、幻灯片导出 | Windows模板恢复、两张照片单页PDF及原片保持通过；蒙版和幻灯片未执行 |
| DeckCraft | +89、36个无歧义契约变化 | starter模板、指定页面复用、结构化MCP目录读取 | Windows实际starter、指定品牌页顺序、可编辑PPTX和源文件保护通过；外部渲染未执行 |
| FigCraft | +2、5变化 | 自动保存、显式协作成员移除及宿主限制 | 真实契约已适配，新流程未专项执行 |
| FilmCraft | 无新增ID、1变化 | timeline.select linked单侧音视频选择及全局设置边界 | Windows演示工程验证单侧删除、伙伴保护、撤销和重开；真实媒体试听与宿主同步未执行 |
| CAD、Grid、Sound、Effect、Vector | 相对此处稳定目录无方法/契约变化 | 沿用现有指导，按main重新构建回归 | 既有原生业务通过，未据此宣称所有主线行为已验收 |

Deck旧目录234条仅232个唯一ID：text.delete/text.move存在不同参数的重复定义。比较器保留歧义，不任意取最后一个覆盖；89是唯一ID集合差，36处契约变化排除了这两个歧义ID。Print比较使用实际MCP工具的snake_case input_schema，与其他应用的引擎命令分开统计。

本批指导复用现有技能入口；目录索引不算新场景，新增main专项结果也未混入原201条场景统计。原201条目前为167条限定技术回归通过、1条部分通过、33条待执行，媒体创作质量和全部宿主同步仍须分别验收。

## 修复

- Fig main后备字体表变为定长数组，适配同时修改数组长度，保留旧版本入口。
- Deck main集中式io模块新增WASM读写与长度桥接，保留原生权限和原子写入分支。
- Photo上游main的Persisted初始化遗漏export_presets，导致Windows与WASM E0063。候选显式携带摘要锁定补丁，仅应用CI副本；Windows补丁固定LF。该产物明确为带插件补丁的开发候选。
- Photo main实际内嵌页面缺中文字形。补齐带许可与摘要的字体输入、WASM字体注入及产物声明，重建后在内嵌浏览器确认中文标题正常。
- Windows控制台报告使用ASCII安全JSON，落盘业务JSON仍保留UTF-8；Deck main目录通过原生stdio MCP list_commands读取，不误用人类可读commands输出。

## 真实宿主与剩余范围

[CAD宿主记录](craft-main-cad-host-validation.json)：隔离Codex CLI 0.162.1实际安装，通过原生app-server调用插件MCP，桌面内置浏览器打开同会话，创建圆、保存DXF、新建空图、重开检查圆心与半径通过。

[Photo宿主记录](craft-main-photo-host-validation.json)：同样使用真实Codex安装与原生宿主调用，内嵌画布同步显示绿色/蓝色笔画，原生工程保存重开、PNG像素、预设CRUD、映射JPEG尺寸、中文字体与layer.list通过。首次layer.list调用时原页签已经关闭，连接租约过期；重开已保存文档后成功，未观察到此方法实现缺陷。

这两项不等于当前桌面聊天重新注册插件，也不证明其余11个main候选、Kimi、ZCode真实宿主通过。新main专有流程中标为未执行的部分、全部新方法的业务覆盖、实际媒体质量、外部Office兼容及13应用完整宿主同步仍未验收；OpenSpec对应任务保持未完成。
