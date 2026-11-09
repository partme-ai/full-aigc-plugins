## Why

现有质量循环能够对当前 revision 做独立评估并检测停滞，但没有版本化的视觉目标集、当前/上一版/目标三方比较合同，也没有“最多一次宏观重规划”和目标变更必须人工批准的结构化门禁。结果是评审可以指出问题，却不能可靠证明相对目标是否改善，停滞后也只能停止。

## What Changes

- 新增 `VisualReferenceSet`，记录参考视频、故事板和目标关键帧的来源、摘要、用途、许可状态和允许偏离范围。
- 新增 `ComparativeEvaluationContext`，同时绑定目标、当前 revision、上一 revision、上一 verdict 和全新只读 Critic 会话。
- 新增 `MacroRevisionRequest`，只在可证明停滞后生成，每个输出最多一次，必须重新人工批准。
- 新增 `RetargetProposal`，目标不可达时仅提出新目标；没有精确人工批准不得生效，生效后旧批准、verdict 和 evidence 全部失效。
- 不引入 `dream-loop`、FAL 脚本或自由文本 Worker/Judge 作为运行时依赖。

## Capabilities

### New Capabilities

- `comparative-video-quality`: 定义视觉目标、三方比较评审、一次性宏观重规划和人工 Retarget 的合同及状态转换。

### Modified Capabilities

无。本变更扩展现有 `add-iterative-video-quality-loop`，但不重复其真实剪映、宿主和发布门禁。

## Impact

- 新增四个严格 JSON Schema、fixture、规范化摘要和语义校验。
- 扩展质量迭代模块，生成比较上下文、宏观重规划请求及 Retarget 后的失效结果。
- 评估器继续无草稿写权限；所有实际剪辑仍通过 WorkflowPlan 和发布 Rust CLI。
- Dream Loop 仅作为 MIT 许可的设计来源登记，不复制运行时代码。
