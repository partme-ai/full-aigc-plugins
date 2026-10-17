# 双商店场景技能检索与适配

本批延续 `add-craft-scenario-playbooks`，由 skills.sh 公共搜索与已安装的 SkillHub CLI 发现来源。候选下载放在本地隔离参考目录，未全局加载商店技能、运行第三方脚本或调用付费服务。

## 数量与交付口径

- 56组查询（两个商店各28组），合并为501条候选记录；其中有模糊匹配、别名和无关项目，候选不是已适配能力。
- 41条采用的来源记录：skills.sh/GitHub固定提交28条，SkillHub版本与正文哈希13条。不同商店可能指向同一上游，41不代表41个独立作者项目。
- 39项原创场景指导，覆盖13应用，接入19个已有技能入口。沿用原生方法与参数模板，不重复增加配方计数。
- 场景映射仍为198条、82个包含结构化配方的技能；不声称新增39个已验证业务能力。
- 一次skills.sh的excel查询发生TLS错误；spreadsheet等查询和SkillHub的excel查询成功，保留失败记录。

## 具体覆盖

| 应用 | 本次接入的场景经验 |
| --- | --- |
| photocraft | 修复与推测分开交付；保留身份特征的人像修饰；代表样片后再批量调色 |
| lightcraft | 按照明分组的白平衡校正；技术纠正先于风格；以联系表筛出批量例外 |
| cadcraft | 由明确尺寸重建零件；平面图的几何关系；可复核的图框交接 |
| designcraft | 先规划阅读顺序再排页；长文按故事流排版；把印前发现转成待处理项 |
| vectorcraft | 文字母版与轮廓交付分开；品牌颜色检查；验证真实几何而非白色遮盖 |
| figcraft | 组件复用而非重复绘制；尺寸变化后再验收布局；有下一步的表单错误状态 |
| effectcraft | 先保证读懂再安排动画；有目的的标志进入；可编辑工程与渲染分别验收 |
| filmcraft | 保留上下文的采访摘编；按实际台词交付字幕；参考镜头匹配与风格分离 |
| soundcraft | 先处理切口再做全局音量；播客章节对应真实音频；保留独立人声与背景素材 |
| deckcraft | 用证据支撑演示叙事；结构化方案比较；讲稿和可见页面分别检查 |
| gridcraft | 保留可重算的报价模型；标记重复而不丢失记录；增长率的零基期边界 |
| wordcraft | 编号是文档结构；正文与节布局分开处理；修订副本保留上下文 |
| printcraft | 文本与视觉双路核查；先发现字段再填写；删除敏感内容而非盖黑框 |

## 适配方式

每项同时包含输入、原创任务判断、已有Craft配方的命令与参数、可观察检查及能力边界。参数按实际输入和返回ID绑定；不把Adobe ExtendScript/COM、Figma Plugin API、RawTherapee参数、AI-HIVE服务或Hyperframes构建链搬进插件。

技能源是编辑事实源，同步到对应插件；全部必要文件放在同一技能内。SKILL.md按任务链接 `references/market-workflows.md`，结构化方法与来源在同目录 `market-adaptations.json`。不依赖兄弟技能或作者本机绝对路径。

SkillHub按[官方安装说明](https://skillhub.cn/install/skillhub.md)检查，本机已有 `skillhub 2026.7.7`，已实际搜索和下载候选；未重复安装、升级或改变默认源。下载仅作为参考读取，不代表这些外部技能已供宿主调用。skills.sh通过公开站点搜索接口检索，未安装另一套CLI。

## 验证与限制

- 新增5项回归：合法既有配方不增加场景计数；未知方法、其他软件参数、缺失来源、缺失哈希应拒绝。先观察4个负例失败，补校验后5项全部通过。
- CI辅助测试52项通过；198条既有映射和新增商店指导的来源、方法、参数、技能内链接及源/插件字节一致性检查通过。
- 13套宿主适配清单与版本静态检查通过；13套可移植/Codex/Claude入口静态检查通过。
- 本批不新增真实媒体或宿主同步验收；新指导的创作效果和跨场景组合仍须实际任务验证。既有Windows原生CLI回归不能替代这一层。
- LightCraft/PrintCraft技能源校验器仍报skill_set_mismatch；插件校验器分别在lightcraft-raw-develop、printcraft-organize-pdf处报scene_digest_mismatch。4项在修改前HEAD的独立归档中同样复现，本批不宣称包级全绿，也未改写冻结快照。

候选、采用来源、版本、摘要与技能入口见 [结构化清单](craft-skill-market-research.json)。原始搜索响应和下载正文保存在本地忽略目录，插件不分发上游正文、代码、素材或凭据。

## 推送后的回归

目录仓提交a3630cd的[Windows原生业务矩阵](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38995872602)和[Windows安装/MCP回归](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38995872606)通过。这些运行沿用固定CLI与候选包，验证执行链和参数回归，不代表新指导已逐项通过真实媒体效果验收。DesignCraft技能源与插件CI通过。

PhotoCraft CI发现8个已打包场景技能缺少宿主命令入口，已按现有扩展格式补齐；本地完整70项测试通过。此修复不改可移植技能或执行引擎。LightCraft和PrintCraft包级CI仍复现上文既有失败。

PhotoCraft入口修复后的[CI运行38996108941](https://github.com/full-aigc-plugins/photocraft-plugin/actions/runs/38996108941)中，70项Python测试、快照和命令证据检查通过，后续Node运行时测试失败：仍引用不存在的skills/photocraft-use/scripts及plan_identity.py。修改前b369183的Git树中这些路径同样不存在，且本批没有修改src或tests；不为此次商店经验适配重新引入旧Harness平台。完整PhotoCraft运行时CI仍未通过。
