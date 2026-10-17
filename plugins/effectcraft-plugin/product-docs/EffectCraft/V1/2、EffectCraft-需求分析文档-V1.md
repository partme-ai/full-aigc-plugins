# EffectCraft V1 — 需求分析文档

> **文档说明**：V1 实施阅读视图；规范事实源为 OpenSpec。
>
> **版本**：1.0.0
> **最后更新**：2026-10-05
> **状态**：目标设计；尚未实现。事实依据与验收结果单独标注。

关联文档：[品牌边界](../1%E3%80%81EffectCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](../5%E3%80%81EffectCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](../../../docs/EffectCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [证据](../../../docs/evidence/runtime-baseline.json)

## 1. 用户故事

| 角色 | 需求 | 完成条件 |
| :--- | :--- | :--- |
| 创作者 | 图层合成、动态图形与镜头效果 | 制作品牌片头，交付可重开的 .ecproj 与可导入剪辑工程的渲染结果；修改文字后保持其他图层和动画曲线不变。 |
| 审阅者 | 检查当前版本与局部问题 | 每条问题能定位到对象或帧 |
| 维护者 | 定位与恢复失败 | 有运行身份、状态账本和可复用检查点 |


## 2. 需求分析与验收映射

| ID | 需求 | 行为摘要 | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| EC-SK-001 | 独立技能事实源 | 技能 SHALL 在独立技能仓库维护；插件仅同步固定 tag、commit 和 SHA-256 的发布副本；不得使用 latest、分支浮动引用或包外符号链接。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| EC-SK-002 | 独立安装与依赖声明 | 专业技能 SHALL 通过公开 CLI 接口运行；单独安装时不得依赖插件私有路径；ArtCraft 技能 SHALL 明确声明编排运行时依赖。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| EC-RT-001 | 运行时来源与完整性 | 运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| EC-RT-002 | 运行能力与隔离升级 | 适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| EC-TX-001 | 版本绑定与单写 | 执行 SHALL 绑定 planHash、inputHashes、projectRevision、runtimeIdentity 和有效授权范围；同一工程只有一个写入者，冲突不得覆盖用户修改。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| EC-TX-002 | 幂等与不明确结果恢复 | 任务 SHALL 在副作用前登记幂等键；超时且执行结果未知时进入 reconciling；核对原任务或产物前不得重新提交。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| EC-TX-003 | 取消与预算边界 | 任务 SHALL 区分 cancel_requested 与 cancelled；父子调用共享预算和截止时间；只允许一个层级负责同一副作用的重试。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| EC-AR-001 | 产物血缘与包完整性 | 产物 SHALL 登记逻辑 ID、不可变版本、内容摘要、来源任务、原生工程和依赖；交付前重新校验文件，移动后可按清单重关联。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| EC-AR-002 | 原生工程与交换损失 | 交付 SHALL 同时保留约定的原生工程与导出；工程需重新打开检查，交换中的扁平化、栅格化、字体和效果损失必须显式记录。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| EC-QA-001 | 技术与创作证据分离 | 质量结果 SHALL 分别记录工程、技术、创作和接受状态；证据绑定文件摘要及运行身份，NOT_RUN 不得当作 PASS，视觉评分不得覆盖技术失败。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| EC-QA-002 | 受限局部修订 | 质量循环 SHALL 将问题绑定对象、帧或区域及责任插件；设置最大轮数、预算与停滞规则；目标变化使旧验收与授权失效。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| EC-RL-001 | 宿主与发布证据 | 发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| EC-RL-002 | 权限与秘密边界 | 运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| EC-DM-001 | 合成建立与范围 | EffectCraft SHALL 显式设置合成尺寸、帧率、时长与工作区；输入的时间单位必须转换为适配器确认的上游单位。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-002 | 图层与素材依赖 | EffectCraft SHALL 维护图层 ID、顺序、父子关系、素材引用和可见性；检查循环父子关系与丢失素材。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-003 | 文字图形与关键帧 | EffectCraft SHALL 以属性路径记录文字、变换与关键帧，保留插值方式；修改文字不得重建无关动画。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-004 | 效果与蒙版能力匹配 | EffectCraft SHALL 在应用效果或蒙版前发现命令与参数 schema；不支持的参数在执行前返回明确错误，禁止静默跳过。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-005 | 透明与色彩交接 | EffectCraft SHALL 交接时记录颜色空间、位深、alpha 类型与编码；透明背景必须通过实际像素或通道检查验证。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-006 | 工程与渲染交付 | EffectCraft SHALL 重开 .ecproj 验证图层与关键帧；渲染结果与源合成版本绑定；向下游提供素材化损失说明。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. 冲突处理

交付格式、预算或素材权限冲突时优先保留用户明确约束，并将相关步骤置为 blocked。独立检查仍可运行。需求变化产生新版本并计算失效范围，不能原地覆盖旧计划与验收。



---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。
