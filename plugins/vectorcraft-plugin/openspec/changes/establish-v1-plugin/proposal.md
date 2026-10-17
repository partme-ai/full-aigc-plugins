## Why

VectorCraft 需要将“可编辑矢量品牌资产与多画板设计”落为可独立安装、可追溯、可恢复的 Agent 插件。已安装的上游 CLI 仅证明运行时可用，不能替代技能、Harness 与原生交付验收。

## What Changes

- 建立独立 `vectorcraft-skills` 的发布与插件锁定引用规范；本变更不把技能源码改成插件私有内容。
- 定义运行时安装、能力探测、任务执行、工程与素材交付、质量修订和宿主发布门禁。
- 固化代表性验收：制作 Logo 与图标资产，交付 .vectorcraft、SVG 和 PNG；修改品牌色后更新所有绑定的变体，并保留无关颜色。
- 交付中英文产品文档、架构、技术方案与 README；实现按任务与证据逐项推进。
- 2026-10-08 增补 Dreamina 对照分析形成的七项需求：统一严格解析、品牌消费者字段保全、原子技能合同、版本事实源、证据索引、持续验证与单轮质量回执；为已有单写、恢复、取消和局部修订需求增加具体失败场景。
- 本次交付仅更新本 change 的规范、设计、任务及需求追踪，新增任务全部待实施；保留已完成子门禁及原证据，不将本次文档校验当作缺陷修复或完整 V1 验收。

## Capabilities

### New Capabilities

- `skills-distribution`: 独立技能与不可变分发。
- `runtime-distribution`: 运行时安装、能力与回退。
- `task-execution`: 任务状态、幂等、授权与恢复。
- `artifact-delivery`: 原生工程、素材和产物证据。
- `quality-review`: 技术门禁与受限创作修订。
- `release-compatibility`: 宿主、权限与发布验收。
- `domain-workflow`: 可编辑矢量品牌资产与多画板设计。

### Modified Capabilities

无既有主规格变更。仓库已进入实施且存在有界验证；本次仍延续当前 change 的七个增量能力，不重复创建规格事实源。

## Impact

目标模块为未来的 `src/harness/`、`src/adapters/`、`runtime/`、`schemas/` 与独立技能仓库。四款上游应用保留各自工程格式；现有插件通过公开接口适配。ArtCraft Services 仅作为架构参考，不复制其受限许可代码。

优化的跨仓库责任为：独立 `vectorcraft-skills` 维护 Python 执行、技能合同、同步与源仓测试；`vectorcraft-plugin` 消费固定快照，维护插件编排、评审、证据与发行校验。`research/vectorcraft` 仅作只读能力参考；Dreamina 的请求／回执和恢复机制按 Vector 本地语义改造，不直接复制远端积分、登录或提交协议。公共 craft-task/v1 与 craft-artifact/v1 仍由 ArtCraft 持有。

## Non-goals

不重写原生编辑器、不新增 SaaS 或真实付费生成。本次规范补充不执行运行代码修改、安装升级、标签发布、Art 捆绑升级或市场发布；已有桌面安装／GUI 的有界证据保留原范围，不等于完整 GUI 支持。目标 Harness 与质量协议须实施及验收后才能声明可用。
