## Why

EffectCraft 需要将“图层合成、动态图形与镜头效果”落为可独立安装、可追溯、可恢复的 Agent 插件。已安装的上游 CLI 仅证明运行时可用，不能替代技能、Harness 与原生交付验收。

## What Changes

- 建立独立 `effectcraft-skills` 的发布与插件锁定引用规范；本变更不把技能源码改成插件私有内容。
- 定义运行时安装、能力探测、任务执行、工程与素材交付、质量修订和宿主发布门禁。
- 固化代表性验收：制作品牌片头，交付可重开的 .ecproj 与可导入剪辑工程的渲染结果；修改文字后保持其他图层和动画曲线不变。
- 交付中英文产品文档、架构、技术方案与 README；实现按任务与证据逐项推进。

## Capabilities

### New Capabilities

- `skills-distribution`: 独立技能与不可变分发。
- `runtime-distribution`: 运行时安装、能力与回退。
- `task-execution`: 任务状态、幂等、授权与恢复。
- `artifact-delivery`: 原生工程、素材和产物证据。
- `quality-review`: 技术门禁与受限创作修订。
- `release-compatibility`: 宿主、权限与发布验收。
- `domain-workflow`: 图层合成、动态图形与镜头效果。

### Modified Capabilities

无。新仓库没有已实现行为或既有主规格。

## Impact

执行事实源为独立 effectcraft-skills 仓库的 `skills/effectcraft-use/scripts/`；插件维护宿主适配、候选校验、固定快照和协议引用。四款上游应用保留各自工程格式；现有插件通过公开接口适配。ArtCraft Services 仅作为架构参考，不复制其受限许可代码。

## Non-goals

本变更不分发 GUI 应用、不新增独立付费模型依赖；未完成宿主与创作验收前不把候选宣称为正式发布。提交、推送、市场更新及发布按各自授权执行。协议内容属于目标设计，不能仅因规格存在而当作已验收工具。

## 本轮优化范围与默认值

本轮目标是用户未安装 Python 和 EffectCraft 时，由已安装技能完成环境准备、创作、验证、预算内局部修订及原生工程/媒体交付。保留现有 15 个技能、独立安装、公开入口及交付格式。实施范围为 effectcraft-skills 和 effectcraft-plugin；research 保持只读，其他 Craft 仅参与必要交接验证。

默认包含隔离 Python 准备、既有授权与预算内最多两轮自动局部修订、30 分钟父子共享截止时间；优先完成 Codex 真实宿主验收，其他宿主独立保留待验收。本轮不因编写规范而授权提交、推送、插件安装升级、市场更新或发布；执行相关动作仍沿用会话的实际授权。阶段门禁和具体管理接口见 design.md，任务及未完成状态见 tasks.md。
