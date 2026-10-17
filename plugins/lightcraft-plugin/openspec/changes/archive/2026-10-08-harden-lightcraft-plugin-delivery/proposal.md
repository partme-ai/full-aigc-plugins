## Why

LightCraft 插件当前是六项独立技能的本地快照，根清单通过已有 portable 校验器，但一项快照测试不能证明真实宿主或照片任务可交付。来源元数据错配仍能通过校验，且缺少任务恢复、产物审阅与发布证据闭环。

## What Changes

- 完整校验本地候选与正式来源身份，锁定来源版本、tag、解析后的 commit 和文件摘要，保护用户快照修改。
- 消费上游统一执行回执，增加持久任务状态、只读核对和并发边界；未知结果不自动重放。
- 增加输出事实与视觉审阅绑定、独立重开证据、局部修订及最终交付回执。
- 以 Codex 为首个目标宿主，按当前宿主契约补最小接入和验证，再按独立证据扩展其他宿主。
- 建立分层 CI、不可变来源同步与发行门禁，修正失效文档路径与许可证材料。
- **BREAKING（仅针对新状态读取器）**：无版本或缺少身份的新旧任务状态不混用；旧记录只读核对，不自动初始化成新任务。

## Capabilities

### New Capabilities

- `provenance-distribution`: 候选与发行身份、来源锁和快照保护。
- `task-recovery`: 持久任务状态、进程/照片库核对及并发恢复。
- `artifact-review`: 产物、重开、视觉审阅与修订交付证据。
- `host-delivery`: 宿主接入、分层测试及发布门禁。

### Modified Capabilities

无既有主规格，使用 ADDED 描述新约束及对当前实现的补强。

## Impact

影响插件清单、来源锁、插件本地控制器及 Schema、校验器、文档、测试与未来 CI。上游六项技能及公共运行资源由 [lightcraft-skills / harden-lightcraft-skill-workflows](https://github.com/full-aigc-skills/lightcraft-skills/blob/main/openspec/changes/archive/2026-10-08-harden-lightcraft-skill-workflows/proposal.md) 唯一维护；本项目按经过验证的来源同步，不直接修改受管快照解决缺陷。

`P-` 为本项目任务 ID，`S-` 为配套技能库任务 ID。当前只形成规格，不实施、安装、同步快照、创建 Git/远端或发布；主规格同步和归档等待实现与全部对应验收。
