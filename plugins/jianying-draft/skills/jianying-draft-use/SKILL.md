---
name: jianying-draft-use
description: "Route JianYing editing requests through the single Rust jianying CLI, asking only essential questions and stopping on missing capabilities or insufficient evidence."
license: Apache-2.0
---

# JianYing Use

把用户目标路由到统一 Rust CLI。先获取事实，再决定是直接调用结构化命令、生成
`jianying-job/v2`，还是停止并给出诊断。不要让用户先学习完整命令面。

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

- 触发条件：用户提出剪映草稿创建、编辑、检查、恢复或导出目标，但尚未选定具体工作流。
- 所需 capability：`doctor`、`capabilities`。
- 最低 CLI 版本：`1.6.0`；版本仅用于升级提示，实际路由以 capability 状态为准。
- 默认风险：`read_only`；进入具体写入流程后采用目标技能的风险等级。
- 输入事实：CLI 版本、capability manifest、素材路径、目标草稿、期望交付物和宿主平台。
- 确认点：仅在后续操作产生写入、费用或原生执行时，由目标工作流绑定具体调用请求确认。
- 成功证据：`structural`；路由成功不代表草稿已冷重开、播放或导出。
- 禁止行为：不得生成 Python 草稿脚本，不得调用外部 headless checkout，不得把低等级证据描述为最终完成。

## 最小路由

1. 执行 `jianying --version`、`jianying doctor --json` 和
   `jianying capabilities --json`。
2. 只询问会改变计划的事实：目标是新建还是编辑、素材位置、是否要求最终 MP4、是否允许外部/原生执行。
3. capability 为 `supported` 才可调用；`partial`、`external_dependency` 或缺失时停止，并报告缺少的证据或环境。
4. 创建/编辑使用 `jianying-job/v2`；只读探测优先使用 `media probe`、`project inspect`、`project verify`。
5. 返回实际达到的证据等级和下一项人工或宿主验证。

常见路由、停止条件和恢复方式见 [references/workflow.md](references/workflow.md)。
最小 Job 示例见 [examples/minimal-job.json](examples/minimal-job.json)。

## 跨技能交接

当用户不知道剪成哪一种视频，先交给 **`jianying-draft-video-planning`**，按渠道、目的、素材从 108 个场景选择方案。
安装：`npx skills add full-aigc-skills/jianying-skills --skill jianying-draft-video-planning`。
场景规划只返回 plan，不应提前要求 TTS 或原生导出；最终执行按所选步骤逐项预检。

需要领域细节时按名称交接，并确保目标技能已安装。例如编辑工作交给
**`jianying-draft-edit`**。安装：
`npx skills add full-aigc-skills/jianying-skills --skill jianying-draft-edit`。

### 剪映面板分类路由

| 用户入口 | 目标技能 | 典型语义动作 |
|---|---|---|
| 素材 | `jianying-draft-media` | `media.import.asset`、`media.import.subdraft` |
| 音频 | `jianying-draft-audio` | `audio.import.asset`、`audio.music.search` |
| 文本 | `jianying-draft-text` | `text.create.default`、`text.create.template` |
| 贴纸 | `jianying-draft-stickers` | `sticker.resource.download`、`sticker.timeline.add` |
| 特效 | `jianying-draft-effects` | `effect.timeline.add_scene`、`effect.timeline.add_character` |
| 转场 | `jianying-draft-transitions` | `transition.timeline.apply` |
| 字幕 | `jianying-draft-subtitles` | `caption.file.import`、`caption.style.apply` |
| 智能包装 | `jianying-draft-smart-package` | `smart_package.preview.request`、`smart_package.apply.changes` |
| 滤镜 | `jianying-draft-filters` | `filter.timeline.apply` |
| 调节 | `jianying-draft-adjustments` | `adjustment.basic.set`、`adjustment.color.set` |
| 模板 | `jianying-draft-templates` | `template.library.apply`、`template.track.import` |
| 数字人 | `jianying-draft-digital-human` | `digital_human.task.submit`、`digital_human.task.resume` |
| 剪辑控制台 | `jianying-draft-editing-console` | `console.segment.split`、`console.session.snap` |

每个目标技能均可粒度安装：`npx skills add full-aigc-skills/jianying-skills --skill <skill-name>`。
只加载用户当前分类对应的技能；跨分类 WorkflowPlan 再组合多个技能，不一次性加载全部说明。

## 渐进式资料

- 首次执行先加载 [正常路径](examples/happy-path.md) 取得端到端顺序。
- 遇到失败或状态未知时加载 [失败恢复](examples/failure-recovery.md) 与 [错误恢复表](references/error-recovery.md)。
- 用户要求越权、覆盖或自动重试时加载 [边界拒绝](examples/boundary-refusal.md)。
- 交付前逐项完成 [验证清单](references/validation-checklist.md)，不得只凭计划或文件存在宣称完成。
