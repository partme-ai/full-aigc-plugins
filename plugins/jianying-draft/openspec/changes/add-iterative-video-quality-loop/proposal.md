## Why

现有开放工作流已经能把创作简报编译为受审批约束的 `jianying-job/v2`，并验证草稿结构，但结构正确和 CLI 成功不能证明作品满足叙事、节奏、音画、字幕或场景目标。需要在不削弱 Rust-only 执行、批准、恢复和证据门禁的前提下，引入目标驱动、独立评估、受控返工和再次验证的有界质量循环。

## What Changes

- 新增版本化 `CreativeTarget`，冻结叙事目标、参考素材、必须保留/禁止内容、目标时长和质量档案，而不把参考风格当成执行授权。
- 新增场景专属 `QualityProfile`，由锁定 Skills 提供知识规则，插件只消费已校验档案并绑定内容摘要。
- 新增独立 `EvaluationVerdict` 与 `EvidenceBundle`，把结构、代理视频、技术质量、创作质量、真实剪映和原生导出证据分项记录。
- 新增 `RevisionRequest` 和 `IterationPolicy`，将可执行评审意见转换为新 WorkflowPlan revision，并以轮次、预算、时间和停滞规则限制循环。
- 扩展工作流步骤注册表，支持代理渲染、技术验证、创作评估、人工复核、修订规划、原生导出和交付验证；所有草稿写入仍只编译到发布 Rust CLI。
- 先以 VLOG-01 跑通真实质量返工闭环，再扩展 COURSE-01 和 WEDDING-01；合成、发布二进制、真实剪映和三宿主证据继续分层记账。
- 不直接引入 Dream Loop 的 Fal/3D 辅助代码、固定三轮策略、单图评分或允许 Worker 直接修改项目的流程。

## Capabilities

### New Capabilities

- `creative-quality-target`: 定义目标视频的创作基准、场景质量档案、引用来源、摘要绑定及失效规则。
- `independent-video-evaluation`: 定义代理与媒体证据输入、独立评估者、结构化结论、硬门禁和分项证据。
- `bounded-quality-iteration`: 定义评审到新修订的转换、重新批准、停滞检测、预算限制和退出状态。

### Modified Capabilities

无。本变更依赖尚未归档的 `add-open-workflow-compiler` 合同，不重复修改其 delta spec；实施前必须先满足该变更的 P0 执行与恢复门禁。

## Impact

- 插件：WorkflowPlan 步骤注册表、工作流编译器、运行状态机、评估器适配层、证据账本、宿主入口及对应 Schema/测试。
- CLI：继续作为唯一草稿写入和本地剪映控制执行器；如缺少代理渲染、媒体检查、播放或导出原子能力，须在 `jianying-cli` 独立立项并发布后由插件锁定消费。
- Skills：`jianying-skills` 提供版本化场景 QualityProfile、失败模式和评审规则；插件不得从开发目录读取或把知识文档当作运行证据。
- 权限：模型上传、付费评估、草稿写入、GUI 控制、原生导出和商业用途分别批准，评估器不得自行授权返工。
- 兼容性：现有 `plan-video`、旧 Harness 和开放工作流入口保持兼容；质量循环采用显式 opt-in，关闭后保留账本与待对账占用。
