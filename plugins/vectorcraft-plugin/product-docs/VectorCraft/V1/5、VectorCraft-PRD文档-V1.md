# VectorCraft V1 — PRD文档

> **文档说明**：V1 实施阅读视图；规范事实源为 OpenSpec。
>
> **版本**：1.0.0
> **最后更新**：2026-10-05
> **状态**：目标设计；尚未实现。事实依据与验收结果单独标注。

关联文档：[品牌边界](../1%E3%80%81VectorCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](../5%E3%80%81VectorCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](../../../docs/VectorCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [证据](../../../docs/evidence/runtime-baseline.json)

## 1. 版本目标与非目标

制作 Logo 与图标资产，交付 .vectorcraft、SVG 和 PNG；修改品牌色后更新所有绑定的变体，并保留无关颜色。

本 PRD 是规范阅读视图；行为事实源是链接的 OpenSpec。未实现功能保持 planned。V1 不建设全新编辑器或多租户云平台。

## 2. 功能需求

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


## 3. 非功能要求

工程单写；幂等重复不得增加副作用；秘密不得进入回执；所有验收绑定真实产物哈希；计划变化和 GUI 修改必须检测。初始修订上限 3 轮、单项目渲染并发 1 是待验证默认值，不是性能测量。

## 4. 端到端验收步骤

1. 从干净环境安装锁定运行时与技能。
2. 登记 fixture 素材与预期输出。
3. 执行计划，验证工程与导出。
4. 关闭并重开原生工程，检查对象可编辑性。
5. 执行代表性局部修改，比较不变对象。
6. 注入中断并恢复，核对没有重复副作用。
7. 在目标宿主重新执行并记录宿主版本。

## 5. 发布门禁

每个 P0 需求至少有成功与失败证据；未执行项标为 NOT_RUN。技术失败、原生损坏、摘要漂移或重复提交均阻断发布。



---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。


VC-AR-001验收：公开58／源43、Codex0.153.4 macOS arm64已通过当前三个场景，验证原生移动重开、父修订、登记依赖及篡改拒绝；外部编辑器保真、创作和其他平台独立验收。 [Evidence](../../../docs/evidence/vectorcraft-lineage-fixed58-20261009.json).


VC-AR-002验收：实际公开59／源43、Codex0.153.4 macOS arm64通过当前三个场景，原生文字和自由渐变仍可编辑，SVG／PDF／PNG损失及20类拒绝已验证。GUI、创作和外部编辑器保真独立验收。 [Evidence](../../../docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json).

权限与秘密边界正在实施：本地候选已限制七类子进程入口的环境继承、禁止向错误输出转发原始子进程诊断、拒绝素材附加指令字段及明确命名的字面凭据；失败评审回执也不得将此类凭据写入审计表。8项定向测试和132项Node回归通过，146项Python测试通过；实际原生修订及后续技术检查消耗4次共享预算，相关进程组停止。本候选尚未公开固定分发或完成宿主秘密引用合同，7.4–7.6继续开放，当前仍120/127完成、7项开放。原发布63／源43不变；旧发布证据不得为改动后的工作树放行。该校验不声称识别任意正文中的秘密。 [Evidence](../../../docs/evidence/vectorcraft-permissions-candidate-20261009.json).

候选64已锁定公开技能源44（e5f8e1bb8528），旧63／源43保持不可变。源44的183项回归通过、30项跳过、6项目标测试及13项真实独立冷安装通过；候选插件132项Node与146项Python回归通过，实际原生修订和后续技术检查消耗4次共享预算并停止相关进程组。源44主分支和标签CI通过；插件64仍未公开固定分发，宿主秘密引用、完整权限入口审计与VC-RL-002全部场景尚待完成，7.4–7.6继续开放，总体120/127完成、7项开放。 [Evidence](../../../docs/evidence/vectorcraft-permissions-integration-candidate64-20261009.json).

候选插件64现锁定公开源45（a4b1e624818f）。源45的28项权限测试、193项回归（48跳过）、13项真实独立冷安装及原生修订／三导出／独立重开通过，包含真实GUI保存重开和绕过Python预检后的内核拒绝。当前插件132项Node／146项Python回归及原生修订检查通过，4次共享预算内停止所有拥有的进程组。旧源44快照与执行记录按原始字节归档。Python素材预检授权、实际宿主秘密引用与固定插件64权限验收仍开放；120/127完成、7项开放，候选64未发布，V1及市场资格未获得。 [Evidence](../../../docs/evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json).

当前候选64／源46已验证Python素材根边界及实际原生／受管素材创建与继承返工，属于VC-RL-002部分进展。Node父进程审计、宿主秘密与固定分发仍待完成。120/127任务完成、7项开放，未获得V1或市场资格。

父进程初始素材读取的检查后竞态已修复，并由真实受管原生创建／返工复验。VC-RL-002仍为部分完成，不新增任务完成标记或市场资格。

任务9.21完成：当前智能体实际评审与一次显式原生返工，技术与创作结论分别记录。绿色目标达成，小文字问题仍未解决。121/127任务完成、6项开放，不授予独立评审、自动循环、固定安装、V1或市场资格。
