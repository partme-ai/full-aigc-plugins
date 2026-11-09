# 开放路由与确定性工作流编译

## Why

现有规划只能在固定目录中选型，不能把创作简报、组合策略和真实素材编译为可审计的执行闭环。
需要先冻结目录兼容、开放路由、WorkflowPlan、步骤合同及编译规则，再用三条代表链验证。

## What Changes

- 新增 opt-in 工作流入口，消费 Skills v2 目录；现有 v1 `plan-video` 与 Job 入口不变。
- 明确已知、组合、新提案路线，区分方法可规划与能力/权限可执行。
- 定义 WorkflowPlan、素材与片段账本、步骤类型、输出变体、能力与批准要求。
- 定义两段编译：知识到工作流、已确认编辑决策到 `jianying-job/v2`；不把整个流程塞入一个 Job。
- 定义修订、单写、批准复核、取消/崩溃对账和独立验证的可观察行为。
- 冻结生活 Vlog、课程多版本、婚礼多交付的正向与负向验收。

## Capabilities

### New Capabilities

- `open-scenario-routing`: 新目录消费、多维简报和可解释的三路选型。
- `workflow-plan-contract`: 工作流及步骤合同、输出变体和权限边界。
- `workflow-job-compilation`: 确定性编译、能力校验与 Job/回执绑定。
- `workflow-execution-evidence`: 单写、恢复、取消、分项验证和三链验收。

### Modified Capabilities

无。旧 `video-recipe-routing` 和旧执行入口保留原适用范围；新增版本入口不静默改变旧合同。
历史迁移变更的审批/证据缺口由本变更列明工作流门禁，不抹掉原发布阻塞。

## Impact

后续实施涉及目录加载器、新 Schema、路由/编译模块、步骤注册表、状态存储、适配器和测试。
Skills 目录事实源为配套 `evolve-open-scenario-catalog`；原子操作事实源仍为已发布 Rust CLI。
不要求新增 Rust 源码依赖，不生成任意 shell 脚本，不让模型自行授予权限。

非目标：本轮规格阶段不实施、不安装服务、不启动 GUI、不付费调用、不发布。
实时导播、全景/互动引擎、全部 TTS 提供方接入和全场景自动化不属于本次实现承诺。
