## Why

当前插件仅封装六项技能快照，唯一快照测试不能证明来源身份、宿主加载或 PDF 交付。校验器接受错误 releaseTag、外来 sourceProject 和非字符串版本；还缺少独立的宿主编排与真实分发验收。

## What Changes

- 建立候选与正式来源的身份规则、精确技能清单、完整 manifest 校验和受控同步。
- 增加插件本地薄 Harness，消费技能源的执行与 PDF 验收契约，展示任务状态、失败对账与定向返工。
- 为声明支持的宿主生成适配清单并检查一致性，分开验证加载、模型路由和真实任务。
- 建立发布、更新、历史证据、品牌和隐私边界；不因静态 PASS 自动登记市场。
- **BREAKING（实施时）**：含错误来源身份或不完整元数据的旧快照不再通过校验；原文件保留，不能自动伪造 release 身份或强制覆盖用户修改。

## Capabilities

### New Capabilities
- `plugin-provenance`: 来源身份、候选/正式锁、精确清单及安全同步。
- `host-orchestration`: 插件本地 Harness、协议兼容、状态交接和授权复用。
- `host-distribution`: 宿主适配、模型选择、发布更新及当前证据门禁。

### Modified Capabilities
无。当前无正式主规格，以 ADDED 建立目标行为和已有保护的基线。

## Impact

涉及 plugin.json、candidate-source.json、后续正式来源锁/本地技能白名单、宿主兼容清单、插件本地 Harness、scripts/、tests/、docs/。现有 36 个上游技能文件继续由技能源维护；不得在插件中分叉修改。

依赖：full-aigc-skills-repositories/printcraft-skills 的 `harden-printcraft-skill-execution`，特别是 execution-lifecycle、pdf-delivery-verification 和 acceptance-evidence。插件不得自行改写其回执、超时或 PDF 验收含义。

本次仅写规格和任务，不运行 apply/sync/archive，不安装宿主插件、不初始化 Git、不创建远端、不发布。能力实现和验证完成前所有任务保持开放。
