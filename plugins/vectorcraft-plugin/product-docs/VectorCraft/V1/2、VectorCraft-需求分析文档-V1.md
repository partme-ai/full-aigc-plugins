# VectorCraft V1 — 需求分析文档

> **文档说明**：V1 实施阅读视图；规范事实源为 OpenSpec。
>
> **版本**：1.0.0
> **最后更新**：2026-10-05
> **状态**：目标设计；尚未实现。事实依据与验收结果单独标注。

关联文档：[品牌边界](../1%E3%80%81VectorCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](../5%E3%80%81VectorCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](../../../docs/VectorCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [证据](../../../docs/evidence/runtime-baseline.json)

## 1. 用户故事

| 角色 | 需求 | 完成条件 |
| :--- | :--- | :--- |
| 创作者 | 可编辑矢量品牌资产与多画板设计 | 制作 Logo 与图标资产，交付 .vectorcraft、SVG 和 PNG；修改品牌色后更新所有绑定的变体，并保留无关颜色。 |
| 审阅者 | 检查当前版本与局部问题 | 每条问题能定位到对象或帧 |
| 维护者 | 定位与恢复失败 | 有运行身份、状态账本和可复用检查点 |


## 2. 需求分析与验收映射

| ID | 需求 | 行为摘要 | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| VC-SK-001 | 独立技能事实源 | 技能 SHALL 在独立技能仓库维护；插件仅同步固定 tag、commit 和 SHA-256 的发布副本；不得使用 latest、分支浮动引用或包外符号链接。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| VC-SK-002 | 独立安装与依赖声明 | 专业技能 SHALL 通过公开 CLI 接口运行；单独安装时不得依赖插件私有路径；ArtCraft 技能 SHALL 明确声明编排运行时依赖。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| VC-RT-001 | 运行时来源与完整性 | 运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| VC-RT-002 | 运行能力与隔离升级 | 适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| VC-TX-001 | 版本绑定与单写 | 执行 SHALL 绑定 planHash、inputHashes、projectRevision、runtimeIdentity 和有效授权范围；同一工程只有一个写入者，冲突不得覆盖用户修改。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| VC-TX-002 | 幂等与不明确结果恢复 | 任务 SHALL 在副作用前登记幂等键；超时且执行结果未知时进入 reconciling；核对原任务或产物前不得重新提交。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| VC-TX-003 | 取消与预算边界 | 任务 SHALL 区分 cancel_requested 与 cancelled；父子调用共享预算和截止时间；只允许一个层级负责同一副作用的重试。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| VC-AR-001 | 产物血缘与包完整性 | 产物 SHALL 登记逻辑 ID、不可变版本、内容摘要、来源任务、原生工程和依赖；交付前重新校验文件，移动后可按清单重关联。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| VC-AR-002 | 原生工程与交换损失 | 交付 SHALL 同时保留约定的原生工程与导出；工程需重新打开检查，交换中的扁平化、栅格化、字体和效果损失必须显式记录。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| VC-QA-001 | 技术与创作证据分离 | 质量结果 SHALL 分别记录工程、技术、创作和接受状态；证据绑定文件摘要及运行身份，NOT_RUN 不得当作 PASS，视觉评分不得覆盖技术失败。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| VC-QA-002 | 受限局部修订 | 质量循环 SHALL 将问题绑定对象、帧或区域及责任插件；设置最大轮数、预算与停滞规则；目标变化使旧验收与授权失效。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| VC-RL-001 | 宿主与发布证据 | 发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| VC-RL-002 | 权限与秘密边界 | 运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| VC-DM-001 | 路径形状与坐标 | VectorCraft SHALL 定义画板坐标、单位、路径控制点、闭合性与描边；不可把预览像素当成路径事实。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-002 | 组合与布尔操作 | VectorCraft SHALL 记录参与对象 ID、布尔运算与结果对象身份，保留修改前检查点；操作失败不丢失原对象。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-003 | 品牌色与文字 | VectorCraft SHALL 以显式 token 绑定品牌色而非全文件颜色替换；保留文本内容与字体依赖，轮廓化输出记录可编辑性损失。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-004 | 画板与变体 | VectorCraft SHALL 每个画板有稳定 ID、名称、尺寸和输出映射；预览顺序与导出范围明确，避免索引基准混淆。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-005 | 交换格式能力范围 | VectorCraft SHALL 原生 .vectorcraft 与 SVG、PDF、PNG 分别验证；遇到不可交换效果时报告栅格化范围并保留原工程。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-006 | 品牌变体更新 | VectorCraft SHALL 根据 token 与素材依赖更新相关变体，核对无关对象属性与输出没有变化。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. 冲突处理

交付格式、预算或素材权限冲突时优先保留用户明确约束，并将相关步骤置为 blocked。独立检查仍可运行。需求变化产生新版本并计算失效范围，不能原地覆盖旧计划与验收。



---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。


VC-AR-001验收：公开58／源43、Codex0.153.4 macOS arm64已通过当前三个场景，验证原生移动重开、父修订、登记依赖及篡改拒绝；外部编辑器保真、创作和其他平台独立验收。 [Evidence](../../../docs/evidence/vectorcraft-lineage-fixed58-20261009.json).


VC-AR-002验收：实际公开59／源43、Codex0.153.4 macOS arm64通过当前三个场景，原生文字和自由渐变仍可编辑，SVG／PDF／PNG损失及20类拒绝已验证。GUI、创作和外部编辑器保真独立验收。 [Evidence](../../../docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json).
