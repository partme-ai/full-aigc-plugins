## Context

当前插件把技能请求分流到 Python vendor、Rust 源码和外部 fork，环境钩子与 README 仍包含多个历史架构。新设计依赖 `jianying-cli` 变更 `unify-rust-jianying-engine` 的 JSON、capability、task 和 approval 契约，并依赖 `jianying-skills` 的锁定发布版本。

## Goals / Non-Goals

**Goals:**

- 插件成为纯 Harness：理解请求、准备事实、生成 Job、调 CLI、管理状态与验证交付。
- Codex、ZCode、Kimi 使用同一 CLI、同一技能锁和同一风险策略。
- 安装后即有可执行 Rust 能力，不需要 Python 或手工 Cargo 构建。

**Non-Goals:**

- 插件不重新实现草稿格式、媒体算法或原生导出。
- 插件不维护技能正文的独立分叉。
- 插件不把某宿主特有 UI 当作唯一审批机制。

## Decisions

### 1. 单一 Runtime Adapter

新增薄适配层负责定位平台二进制、验证 SHA-256、执行 `jianying ... --json`、解析失败信封和传递 task ID。commands、hooks 和技能都调用该适配层，不直接拼接不同命令。

### 2. Capability 驱动而非版本字符串分支

SessionStart 只做轻量 `doctor/status`；具体工作流在执行前读取 capability 清单。版本用于最低兼容提示，功能路由以 capability 为准，避免平台构建号导致硬编码分叉。

### 3. Harness 状态机

工作流阶段统一为：

```text
intake → inventory → plan → approve → execute → verify → deliver
                      ↘ blocked / recoverable / failed
```

状态保存 CLI task ID、输入摘要、素材哈希、计划路径、批准范围和验证等级。恢复只从已验证检查点继续。

### 4. 风险策略

- 只读：probe、inspect、doctor、catalog、task show，可自动执行。
- 可逆写入：新工作目录构建、代理预览，可在用户任务范围内执行。
- 高风险写入：发布、重命名、删除、修改已有草稿，要求目标明确批准。
- 原生/外部执行：原生导出、付费 ASR、启动/控制剪映，要求独立批准和输出范围。

批准记录绑定 command、arguments、cwd/target、有效期和任务，不跨目标复用。

### 5. 分发二进制而非源码快照

发布工作流为 macOS arm64/x64 与 Windows x64 生成 CLI 制品、checksums 和 capability manifest。插件选择匹配制品；不支持的平台给出安装式 fallback，但不能显示为 ready。开发模式可显式指向本地 CLI。

### 6. 三宿主适配保持薄层

Codex/ZCode/Kimi manifest 只负责宿主入口差异，核心 prompt、风险策略、命令 schema 和结果呈现来自共享数据。三宿主契约测试以相同 fixture 运行。

### 7. 技能单向同步

插件的 `skills.lock.json` 锁定 `jianying-skills` ref、commit、清单和摘要。同步脚本只允许从技能仓覆盖 vendor；插件 CI 检测人工漂移。插件内运行脚本不得被技能锁机制覆盖。

### 8. 迁移诊断而非静默回退

移除 Python vendor 与 fork 路径后，旧环境变量或命令触发时返回迁移说明。不得为“兼容”静默执行旧 Python 路径，否则无法证明单一 Rust 运行时。

## Risks / Trade-offs

- [CLI 尚未达到全能力] → 插件按 capability 阻止请求，不保留第二引擎回退。
- [插件体积因多平台二进制增大] → 发布资产按平台选择下载或拆分包，同时保持哈希验证。
- [三宿主审批 API 不同] → 使用宿主中立 approval record，宿主 UI 只是展示与响应渠道。
- [技能与 CLI 发布不同步] → 发布矩阵要求 CLI、技能和插件版本组合通过 fresh-install 测试。
- [恢复状态泄露本地路径] → 审计输出分为本地详细记录与默认脱敏摘要。

## Migration Plan

1. 添加 Runtime Adapter 和 CLI capability 握手，不改变现有默认路径。
2. 为每个工作流建立 Rust canary，对照旧路径但禁止双写同一目标。
3. Rust capability 达标后逐工作流切换为唯一执行路径。
4. 更新环境钩子、commands 和 manifests，删除 fork-first 提示。
5. 删除 Python vendor、Python runner 和相关依赖测试。
6. 接入技能仓新版本并验证摘要。
7. 在 Codex、ZCode、Kimi 执行新鲜安装、草稿构建、恢复和授权测试。
8. 删除迁移期旧变量支持，只保留明确错误说明。

回滚只允许回滚插件版本和 CLI 制品，不恢复已删除的 Python 自动回退；目标草稿由 CLI 快照机制恢复。

## Open Questions

- CLI 二进制最终采用随插件打包还是首次安装按平台下载，可在制品大小和宿主市场限制验证后决定。
