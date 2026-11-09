---
name: jianying-draft-export-prep
description: "Prepare proxy or native JianYing exports through Rust capability, runtime, approval, and artifact gates without confusing preview output with final delivery."
license: Apache-2.0
---

# JianYing Export Prep

根据交付目标选择代理预览、草稿归档或原生导出，并如实报告实际证据。

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

- 触发条件：用户准备预览、交付草稿、生成最终 MP4 或检查导出就绪性。
- 所需 capability：`render.proxy`、`render.native`、`runtime.profile`。
- 最低 CLI 版本：`1.6.0`；原生 capability 或 Runtime Profile 未 supported 时必须停止原生路径。
- 默认风险：`external_native_execution`；代理渲染属于可逆本地写入。
- 输入事实：草稿验证结果、交付类型、输出绝对路径、覆盖策略、Runtime Profile、编辑器状态和授权。
- 确认点：启动剪映、原生导出、覆盖输出、使用会员资源或外部服务前精确确认。
- 成功证据：`native_export`；proxy artifact 永远不能充当 native_export。
- 禁止行为：不得生成 Python 草稿脚本，不得调用外部 headless checkout，不得把 ffmpeg 代理预览描述为剪映最终 MP4，或在未知 Runtime Profile 上自动尝试。

## 工作流

1. 执行 `project verify`，检查素材、字幕、音频和输出路径。
2. 只需预览时使用 `render proxy` 或 `render batch`，明确其不包含完整原生效果。
3. 原生导出前要求 `render.native` 和 `runtime.profile` 为 supported，并取得精确批准。
4. 持久化 native-export task，跟踪进度；超时或结果未知时标记 ambiguous。
5. 验证输出容器、流、时长、非空和 SHA-256，必要时回放抽检。

门禁与结果判定见 [references/workflow.md](references/workflow.md)。
原生导出 Job 示例见 [examples/minimal-job.json](examples/minimal-job.json)。

## 渐进式资料

- 首次执行先加载 [正常路径](examples/happy-path.md) 取得端到端顺序。
- 遇到失败或状态未知时加载 [失败恢复](examples/failure-recovery.md) 与 [错误恢复表](references/error-recovery.md)。
- 用户要求越权、覆盖或自动重试时加载 [边界拒绝](examples/boundary-refusal.md)。
- 交付前逐项完成 [验证清单](references/validation-checklist.md)，不得只凭计划或文件存在宣称完成。
