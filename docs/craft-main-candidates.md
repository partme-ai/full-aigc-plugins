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

[首轮构建39006638202](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39006638202)分别执行13个Windows原生CLI构建和13个Web编辑器构建。原生CLI回归读取新编译二进制；显式摘要校验、源码与技能源固定点校验不允许用稳定版替代。WASM桥接仅应用于隔离checkout。产物命名UNACCEPTED，不代表安装或创作质量已验收。

发现并修复FigCraft main字体后备表提取为定长数组后的补丁失效（同时调整数组长度），以及DeckCraft main集中式io模块的WASM读写/长度入口；保留旧版兼容和原生权限检查。PhotoCraft、SoundCraft、GridCraft没有独立字体脚本，候选构建按其现有方式处理。[5个Web专项重跑39006903491](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39006903491)固定相同上游提交与已修复插件提交。

GridCraft main的18例/110次调用与SoundCraft main的8例/507次调用实际完成业务回归，35份/32份输出摘要分别核对。它们的341/478条实际命令目录相对稳定版观察目录无新增、删除或参数契约变化。业务报告已落盘，但首轮任务最后受到Python cp1252控制台输出中文的错误影响，不能据此标记CI成功。已修复报告输出，并使用同一份main二进制执行[专项重验39007057957](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39007057957)。命令目录不变不代表所有语义不变。

CADCraft main编辑器38份文件摘要校验通过，已在隔离Codex 0.162.1实际安装，通过原生app-server调用插件MCP，由桌面内置浏览器加载同一会话。实际创建圆、画布同步显示、保存DXF、新建空图、重开检查圆心与半径通过。详情见[宿主验证](craft-main-cad-host-validation.json)。这不等于当前桌面聊天重新注册了插件，也不证明其他12应用或Kimi/ZCode宿主通过。

剩余构建、命令参数差异、技能适配及其他宿主回归持续推进，未将本批构建作为13应用main全部交付。

PhotoCraft固定main的原生编译发现Persisted缺少export_presets初始化（E0063）。插件候选补丁补齐原有JSON字段读取，锁定补丁SHA-256并仅在CI副本应用；候选来源显式携带补丁，不当作未修改上游构建。重建同时执行上游已有的export_preset_cmds持久化往返与无效预设测试。
