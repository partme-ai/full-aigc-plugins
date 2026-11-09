---
name: jianying-draft-audio
description: "Design JianYing audio layers and route local, system, open-source, or cloud TTS safely through the Rust CLI, including probing, volume, fades, sound effects, relinking, approval planning, and playback checks."
license: Apache-2.0
---

# JianYing Audio

处理对白、解说、原声、BGM 和音效的分层与同步。数值基于素材和试听事实，不使用固定万能音量。

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

- 触发条件：用户需要新增/替换/重链音频、调节音量、淡入淡出、音效或混音。
- 所需 capability：`media.audio`、`timeline.volume`、`timeline.audio_fade`；TTS 另检查
  `media.tts_local` 或 `media.tts_provider`，不得以其中一个替代另一个。
- 最低 CLI 版本：`1.6.0`；缺失或 partial capability 只能执行已支持子集。
- 默认风险：`reversible_write`。
- 输入事实：音频流/时长/采样事实、目标草稿副本、轨道角色、对白区间、响度目标和授权边界。
- 确认点：写入已有草稿、调用联网/付费 TTS、覆盖音频制品或原生播放前确认。
- 成功证据：`playback`；波形、文件存在和结构验证不足以证明混音结果。
- 禁止行为：不得生成 Python 草稿脚本，不得调用外部 headless checkout，不得让 BGM 掩盖语音、重复铺原声或把未试听结果标记完成。

## 工作流

1. `media probe` 确认素材包含预期音频流和真实时长。
2. `media add-audio/replace/relink` 处理素材；声音来自视频时优先调整视频段音量。
3. `timeline volume` 设置片段基础音量；淡入淡出 capability 未 supported 时停止该步骤并明确缺口。
4. 使用 `media sfx` 时先从目录按 slug 选择，并检查资源授权。
5. TTS 先按系统、本地进程/HTTP、联网客户端、云厂商四类确认边界；不得把 EdgeTTS 当离线模型，
   也不得把通用 `local-process`/`local-http` 当成具名开源模型已经通过许可证和握手的证据。
6. 云厂商先执行 `media tts ... --provider <cloud> --plan`；计划只绑定凭据环境变量名、内容/请求
   哈希、目标、任务和最大预算。只有用户明确要求该厂商、精确审批已落盘且当前 CLI 的该执行子路径
   已通过握手时，才可去掉 `--plan` 并携带 `--approval-id` 提交；不得自行拼 HTTP 请求。
   `media.tts_provider=partial` 仍禁止自动选用云厂商或宣称全厂商 supported，但不应把已获精确审批的
   具名执行路径误报为不存在。plan、queued、ambiguous 都不能说成已合成。
7. `project verify` 后试听对白清晰度、峰值、转场和同步。

影视解说或 README 教程的旁白必须先生成并探测真实音频，再按实际时长安排字幕与 ducking；
不得继承固定 BGM 音量。响度、峰值、对白优先级和人工听感决定最终混音。

分层、TTS 和恢复见 [references/workflow.md](references/workflow.md)。
隔离编辑 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。

## 渐进式资料

- 首次执行先加载 [正常路径](examples/happy-path.md) 取得端到端顺序。
- 遇到失败或状态未知时加载 [失败恢复](examples/failure-recovery.md) 与 [错误恢复表](references/error-recovery.md)。
- 用户要求越权、覆盖或自动重试时加载 [边界拒绝](examples/boundary-refusal.md)。
- 交付前逐项完成 [验证清单](references/validation-checklist.md)，不得只凭计划或文件存在宣称完成。
