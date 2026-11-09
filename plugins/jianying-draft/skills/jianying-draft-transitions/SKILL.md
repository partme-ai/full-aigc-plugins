---
name: jianying-draft-transitions
description: "Select and apply JianYing transitions through Rust catalogue and timeline capability gates, validating adjacent segments, resource authorization, duration, and playback."
license: Apache-2.0
---

# JianYing Transitions

转场是相邻片段之间的语义连接。先验证边界和资源，再决定是否使用。

## 什么时候使用

- 用户明确要求本技能标题所对应的剪映能力，并接受通过统一 Rust `jianying` CLI 处理。
- 用户需要可审计的计划、执行或验证证据，而不是仅要一个概念性回答。
- 需求尚不明确时先交给 **`jianying-draft-use`** 路由；不该用本技能处理其他剪辑器、普通视频知识问答或缺少必要素材的猜测性执行。

## 能力边界

- ✅ **能做：** 基于真实路径和探测结果生成确定性计划；在 capability 为 `supported` 时执行本领域操作；输出实际达到的证据等级。
- ⚠️ **需要条件：** 写入必须使用隔离副本；费用、外部服务和原生应用动作必须有精确批准；播放或导出结论必须有对应运行证据。
- ❌ **超出范围：** 不自动安装或升级 CLI，不生成 Python 草稿脚本，不调用外部 headless checkout，不覆盖源草稿，不伪造资源 ID、媒体事实或成功状态。

## Step 1 — 建立事实基线

记录用户目标、绝对路径、宿主平台、目标交付物和允许的副作用；信息不足时先给只读诊断方案，并逐项列出缺少的事实。

## Step 2 — 握手能力

执行 version、doctor 与 capabilities 检查。版本满足不代表 capability 可用；`partial`、`external_dependency` 或缺失状态必须进入降级路径。

## Step 3 — 校验输入

探测媒体、草稿、配置或任务状态；拒绝不存在的路径、越界时间、未知 schema、失配哈希和无法绑定目标的批准。

## Step 4 — 形成确定性计划

把操作、参数、输出路径、风险等级、确认点和期望证据写入计划。多任务按“只读事实 → 可逆写入 → 外部/原生动作”排序。

## Step 5 — 执行或停在门禁前

只执行已支持且已获授权的步骤。输出 ambiguous、超时或部分成功时保留 task ID、审计日志和制品，不自动重试。

## Step 6 — 验证并交付

运行结构校验，再按目标追加冷重开、播放或原生导出证据；报告实际等级、失败字段、可恢复动作和未验证项。

## Rules

- 计划中的素材时长、尺寸、流、哈希和草稿版本必须来自工具输出。
- 批准必须绑定命令、参数、目标、有效期和预算；任一字段改变即重新确认。
- 用户数据仅在本地目标路径和声明的外部 Provider 边界内处理；不得收集、上传或记录无关凭据。
- 当前证据不足时使用 `UNVERIFIED`、`BLOCKED` 或 `AMBIGUOUS`，禁止用推断补齐结果。

## Gotchas

1. **把版本当能力：** 始终检查具体 capability，不能因为 CLI 版本够新就直接执行。
2. **把结构验证当成片验收：** `project verify` 只证明结构层，播放和原生导出需要独立证据。
3. **直接修改源草稿：** 先创建隔离副本并记录输入哈希，任何原地覆盖请求都要停止并改为新输出。
4. **对 ambiguous 自动重试：** 先查询 task、审计与外部制品，只有确认未发生副作用后才能由用户批准重试。
5. **凭记忆填写资源或时间：** 资源 ID 来自目录，时间来自 probe/ASR/项目数据；无法取得时明确阻塞。
6. **笼统索要更多信息：** 先给可执行的只读方案，再明确列出路径、交付等级或授权等缺口。

## 验证清单

- [ ] CLI identity、版本和 capability 已记录。
- [ ] 所有输入路径、媒体事实与哈希可复核。
- [ ] 写入目标与源草稿隔离，确认点精确绑定。
- [ ] 失败和 ambiguous 路径保留 task ID、日志和恢复建议。
- [ ] 最终措辞与实际 evidence level 一致。

## 运行契约

- 触发条件：用户要求转场、镜头衔接、卡点或查询可用转场资源。
- 所需 capability：`timeline.transition`、`media.catalogue`。
- 最低 CLI 版本：`1.6.0`；transition 为 partial 时只生成计划和诊断。
- 默认风险：`reversible_write`。
- 输入事实：相邻片段 ID、时长/句柄、节拍或章节边界、资源目录状态和授权。
- 确认点：使用会员/受限资源、写入已有草稿或执行原生播放前确认。
- 成功证据：`playback`；目录命中或 wire 字段存在不是观感验收。
- 禁止行为：不得生成 Python 草稿脚本，不得调用外部 headless checkout，不得对末段加转场、滥用每个切点或把缓存存在当授权。

## 工作流

1. 用 `media catalog` 检索名称，禁止凭记忆伪造资源 ID。
2. 检查前后片段相邻关系、持续时间和可用 handle。
3. 转场挂在出段，持续时间不得超过双方可用窗口。
4. capability 未 supported 时输出建议计划，不写入草稿。
5. 支持后在隔离副本写入，并通过冷重开和播放检查节奏、黑帧和资源缺失。

边界策略和恢复见 [references/workflow.md](references/workflow.md)。
隔离编辑 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。

## 渐进式资料

- 首次执行先加载 [正常路径](examples/happy-path.md) 取得端到端顺序。
- 遇到失败或状态未知时加载 [失败恢复](examples/failure-recovery.md) 与 [错误恢复表](references/error-recovery.md)。
- 用户要求越权、覆盖或自动重试时加载 [边界拒绝](examples/boundary-refusal.md)。
- 交付前逐项完成 [验证清单](references/validation-checklist.md)，不得只凭计划或文件存在宣称完成。
