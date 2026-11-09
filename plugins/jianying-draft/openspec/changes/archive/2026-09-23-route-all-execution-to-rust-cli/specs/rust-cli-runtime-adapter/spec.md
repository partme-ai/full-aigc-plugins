## Purpose

定义插件与统一 Rust CLI 之间唯一、稳定且可诊断的运行时边界，消除 Python 引擎和外部 fork 的执行分歧。

## ADDED Requirements

### Requirement: 唯一执行路径
插件 SHALL 仅通过 `jianying-cli` 执行剪映相关操作，不得 import 或运行 pyJianYingDraft，也不得要求外部 headless checkout。

#### Scenario: 生成草稿
- **WHEN** 任一宿主请求生成剪映草稿
- **THEN** 插件生成统一 Job/Plan 并调用版本锁定的 Rust CLI

#### Scenario: 检查插件运行文件
- **WHEN** 分发校验扫描 commands、hooks、scripts 和安装式 runtime
- **THEN** 不存在 Python runner、Python SessionStart shim、vendored pyJianYingDraft 或相关安装依赖；完成 Rust-only cutover 后，Node Harness 不再读取或诊断旧外部 checkout 变量，也不能触发任何 fork-first 执行

#### Scenario: 历史迁移记录提及旧引擎
- **WHEN** OpenSpec、来源基线或迁移文档以历史语态记录 pyJianYingDraft、外部 headless 或旧 vendor 路径
- **THEN** 分发审计允许保留来源和迁移证据，但 README、活动 runbook、脚本、commands、hooks 和 CI 不得包含可执行旧 Python runner、外部 headless clone/checkout、`JIANYING_HEADLESS_ROOT` 赋值或 vendored Rust 源码启动命令

#### Scenario: 文档或 CI 重新引入可执行旧依赖
- **WHEN** 任一活动文档、脚本或 workflow 新增旧 runner 命令、外部 fork checkout 或迁移变量赋值
- **THEN** distribution validator 与结构化 release readiness 都必须将 Rust-only 发布面判为失败，并给出文件与命中命令；不能因为 commands/hooks 已切换就忽略其他发布表面

#### Scenario: 审计实际插件归档
- **WHEN** release gate 从待发布 commit 生成插件源码归档
- **THEN** 门禁必须直接读取归档成员并验证单一根目录、普通文件类型、必要清单、13 个技能入口和 Rust-only 运行面；路径穿越、链接或特殊文件、Python 缓存、退休引擎路径及活动外部 fork 指令均须 fail closed；归档本体与机器可读审计必须同时进入发布证据，审计绑定归档 SHA-256、插件版本和插件源码 commit，聚合器重新计算摘要并拒绝缺失、篡改、身份漂移或额外资产

### Requirement: 版本与 capability 握手
插件 SHALL 在执行前获取 CLI 版本、Schema 版本和 capability 清单，并对缺失能力返回明确诊断。

#### Scenario: CLI 版本过旧
- **WHEN** 请求需要 ASR 账本而已安装 CLI 未声明该 capability
- **THEN** 插件停止执行并返回最低兼容版本与升级指引

### Requirement: 结构化错误适配
插件 SHALL 保留 CLI 错误类型、退出码、任务 ID 和恢复提示，不能把所有失败压缩为通用文本。

#### Scenario: 可恢复任务失败
- **WHEN** CLI 返回带任务 ID 的可恢复失败
- **THEN** 插件向智能体暴露同一任务 ID和允许的恢复动作
