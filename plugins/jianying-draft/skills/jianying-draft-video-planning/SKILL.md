---
name: jianying-draft-video-planning
description: 为剪映视频按目标渠道、用途与素材选择剪辑类型，提供108个场景的具体剪法、素材缺口和能力映射；用于用户不知道该剪成什么或需要Vlog、婚礼、广告等工作流规划时，不代替已明确的草稿原子操作。
license: Apache-2.0
---

# 视频场景规划

把“这些素材能剪什么”变成用户能选择、Harness 能交接的剪辑方案。108 个场景属于一个规划技能，不是 108 个重复技能，也不代表 108 种原生能力已验收。

## 运行契约

- 触发条件：用户提供视频目标或素材，需要识别视频类型、比较剪法、选择工作流。
- 所需 capability：在线握手使用 `capabilities`；离线方法规划不调用 CLI，必须标能力未核验。
- 最低 CLI 版本：`1.6.13`；执行仍逐项检查实时 capability。
- 默认风险：`read_only`。
- 输入事实：目的、受众、发布渠道、目标交付、素材清单；探测到的时长与尺寸不可虚构。
- 确认点：场景歧义、改变交付、采用付费模型、上传素材、启动原生应用或正式写入前。
- 成功证据：`plan`；仅说明形成候选或通过规划预检，不是已剪辑、已播放或已导出。
- 禁止行为：不默认下载参考作品、不照搬镜头或文案、不自动调用模型、不覆盖原素材、不把方法示例当运行证据。

## 什么时候使用

“一堆旅行素材不知道怎么剪”进入此技能；“做婚礼全程还是快剪”进入候选选择。
“把第3段移动到2秒”属于已明确的原子编辑，直接交接 jianying-draft-edit，不必重做场景规划。

## 能力边界

能提供有来源的剪辑方法、场景选择和能力缺口。需要真实素材才能完成镜头判断；
不能从文件名推断画面内容，不能把关键字匹配当成视觉分析或自动成片。

## 开放目录兼容

旧 `plan-video` 继续使用冻结 v1 目录。支持 `workflow-plan` 的插件显式读取
[v2 目录](references/planning-catalog-v2.json) 和 [合同](references/planning-catalog-v2.schema.json)。
v2 的规模以目录 `scenes` 实际条数为准，不再把任何数量、家族数或 Recipe 数作为扩容上限；当前目录为 108 个种子。每个场景另声明 `skills`、`required_capabilities`、`beats` 与 `editorial_intent`，用于路由到具体技能与 CLI 能力。
12 维词表不表示每个场景已完整标注；当前仅迁移领域映射，其余未知条件须澄清。
[三条代表工作流知识向量](references/representative-workflows-v1.json)分别冻结 Vlog、课程多版本和婚礼多交付的
素材缺口、用途、Recipe、输出与验收边界；它们是正式知识，不是运行成功记录。
[质量档案目录](references/quality-profiles-v1.json)及其[严格合同](references/quality-profiles-v1.schema.json)
为这三条工作流提供分项阈值、硬门禁、证据类型、允许的返工动作类别和人工判断边界。
只在工作流已选定且需要编制质量合同时读取对应档案；它不授予执行、批准、模型调用或导出权限，
不能把档案阈值当作真实成片已通过的证据。
[辅助制作目录](references/assisted-production-workflows-v1.json)提供软件教程录屏、README 安装教程、
产品演示智能缩放、Web 数据可视化片头和影视解说五条 Recipe。目录中的 `provider_required`、
`capability_gated` 和 `plan_only` 是停止条件，不是已安装 Provider 或已通过真实剪映的证据。
案例没有命中时允许提出新策略，但不能伪造场景 ID、执行权限或媒体时间码。
旧插件缺少新入口时保持旧行为；不得自行复制开发目录覆盖其技能锁。

## Step 1–6 — 选型顺序

1. 先识别渠道、用途和交付形式。渠道未知可先用 custom，但不虚构平台规格；导出前补齐尺寸、时长和实时平台限制。
2. 打开 [场景索引](references/scene-index.md)。明确场景 ID 时直接选择；
   如“婚礼视频”覆盖快剪、全程、誓言等多个例子，给 2–3 个有差异候选并说明差别。
3. 只读选定的 example；比较其最小素材、故事段落、关键剪法和独有验收点。缺素材列补拍或调整方案，不能直接捏造 Plan 时间码。
4. 按 [Recipe](references/edit-recipes.json) 组织步骤。
   结构化 [目录](references/video-taxonomy.json) 是旧路由事实源；
   [渠道档案](references/channel-profiles.json) 是规划建议，不是平台官方硬上限。
   命中录屏、智能缩放、Web VFX、README 教程或影视解说时，再读取辅助制作目录；不得把其中步骤改写为自由命令。
5. 获取已安装二进制的 `jianying capabilities --json`，按所选交付和可选功能检查；不要求无配音计划具备 TTS。
6. 输出已选场景、Recipe、素材缺口、人工步骤、所需技能/能力、确认点和交付证据边界。流程见 [workflow](references/workflow.md)。

## 能力交接

规划归本技能，任务状态、审批与重试归插件 Harness，媒体原子操作归 Rust CLI。
进入确定性任务时交给 **`jianying-draft-schema`**；安装：
`npx skills add full-aigc-skills/jianying-skills --skill jianying-draft-schema`。
执行交给 **`jianying-draft-edit`**；安装：
`npx skills add full-aigc-skills/jianying-skills --skill jianying-draft-edit`。
其他目标技能的安装命令分别写在每个 example；粒度安装不会自动包含它们。

[最小 Job 结构](examples/minimal-job.json) 仅解释现有 v2 契约，不代表含素材的可执行剪辑成片。
[能力映射](references/capability-mapping.md) 区分原子操作、人工判断和原生执行。

## Rules — 来源与质量边界

[来源索引](references/source-index.json) 给每个场景保留检索词、链接、查阅日期、阅读范围与热度边界。
有播放量不代表场景必火；无数值标 popularity_unverified。视频简介与搜索摘录不能被描述成完整观看。
步骤是独立写作的适配方案，不是从第三方复制媒体或声称已经完成的用户案例。

内容统计必须分栏：正式目录当前含 108 个种子；`test_fixture` 只用于兼容与负例测试；
三条代表工作流是知识合同；编译、播放、导出和宿主结果只能由运行证据统计，不能由这些文件推导。

## Gotchas — 失败与恢复

- 缺素材：waiting_input，指出具体镜头/音轨/事实缺口。
- 多个合理场景：needs_selection，不偷偷选择最高排名。
- 必要 capability 非 supported：blocked_capability；不静默降低交付等级。
- 执行结果不明：保留任务和输入摘要，核查后再决定重试，规划器自身不执行重试。
- 原生导出仍须真实应用与产物证据；代理预览不能冒充最终验收。

## 验证清单

- [ ] 选择的是用户真实用途，渠道限制已确认或明确未知。
- [ ] 选中 example 的独有素材与验收条件已进入计划。
- [ ] 原子能力来自二进制握手，人工/外部能力另列。
- [ ] 素材来源、肖像、商业使用和敏感信息已审查。
- [ ] 输出只声明实际达到的证据等级。
