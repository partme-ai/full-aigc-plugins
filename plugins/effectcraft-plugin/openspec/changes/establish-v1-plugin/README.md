# establish-v1-plugin

定义 effectcraft 独立技能、运行时与插件 V1 规格及验收任务

本次优化沿用此变更作为唯一规格事实源。目标为无 Python/EffectCraft 的用户通过独立技能完成环境准备、创作、结果检查、预算内局部修订及原生工程/媒体交付；保留15技能、旧公开入口和交付协议。当前仍处实施与验收阶段，未满足全部门禁前不归档。

| 优化范围 | 行为规范 | 实施任务 |
| :--- | :--- | :--- |
| 隔离安装、七种原生平台、Web/FreeBSD、doctor与能力发现 | [runtime-distribution](specs/runtime-distribution/spec.md) | 9.1、9.2及其子项 |
| 统一任务、单写、回执、恢复、取消和父子预算 | [task-execution](specs/task-execution/spec.md) | 9.3及其子项；9.7–9.14组件追踪 |
| 实际技术检查、宿主Judge、最多两轮/30分钟局部修订 | [quality-review](specs/quality-review/spec.md) | 9.4及其子项 |
| 单技能双入口、资源一致性和15技能代表任务 | [skills-distribution](specs/skills-distribution/spec.md) | 9.5及其子项；9.1.3 |
| Codex自然语言派发、透明交接、固定分发与证据门禁 | [release-compatibility](specs/release-compatibility/spec.md) | 9.6及其子项；9.5.2 |

完整边界见 [proposal](proposal.md)，执行决策、管理接口及四阶段门禁见 [design](design.md)，完成状态和证据见 [tasks](tasks.md)。已通过的组件只关闭自身范围；未验平台、宿主及能力保持开放。提交、推送、安装升级、市场更新和发布遵循各自已有授权，本次文档更新不新增这些授权。
