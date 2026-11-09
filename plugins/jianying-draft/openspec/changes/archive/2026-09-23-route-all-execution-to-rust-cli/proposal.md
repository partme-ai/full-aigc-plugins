## Why

插件当前同时路由到 vendored pyJianYingDraft、Rust 源码快路径和外部 headless fork，导致安装、诊断、重试、许可和宿主行为不一致。插件需要收敛为纯智能体编排层，由 `jianying-cli` 提供唯一执行契约，并在 Codex、ZCode、Kimi 中保持相同任务行为。

## What Changes

- 将所有草稿生成、编辑、校验、发布、ASR、导出和恢复操作路由到版本锁定的 `jianying-cli`。
- 删除 Python 引擎运行路径、`pymediainfo` 运行依赖和外部 headless fork 强依赖。
- 增加 CLI 能力发现、版本握手、结构化错误解析、任务状态、重试、恢复、审批和审计编排。
- 将复杂剪辑请求编译为统一 Rust Job/Plan，而不是生成临时 Python 脚本。
- 为只读、可逆写入、高风险写入和原生导出定义不同授权策略。
- 在 Codex、ZCode、Kimi 三个宿主中提供一致的命令、技能路由和环境诊断。
- 与 `jianying-skills` 的版本锁同步，插件不得自行维护技能正文。
- **BREAKING**：移除 `jydraft_run.py` 及 fork-first 执行契约；旧环境变量仅在迁移诊断期给出明确替代提示。

## Capabilities

### New Capabilities

- `rust-cli-runtime-adapter`: 发现、校验并调用 `jianying-cli`，统一处理 JSON、错误、版本和能力协商。
- `agent-workflow-orchestration`: 素材盘点、计划生成、任务拆解、检查点、重试、恢复和交付验证。
- `runtime-approvals-and-observability`: 风险分级审批、任务状态、审计记录、诊断和宿主可观察输出。
- `cross-host-distribution`: Codex、ZCode、Kimi 一致清单、命令、技能锁、CLI 制品与安装验证。

### Modified Capabilities

无。仓库此前没有 OpenSpec 主规格。

## Impact

- 影响插件清单、commands、hooks、scripts、vendor/installer、测试、README 和发布工作流。
- 依赖 `jianying-cli` 变更 `unify-rust-jianying-engine` 提供稳定机器契约。
- 依赖 `jianying-skills` 变更 `align-skills-with-rust-cli` 提供唯一技能事实源。
- 迁移必须保留旧插件安装的明确诊断信息，但不能继续静默回退到 Python 或外部 fork。
