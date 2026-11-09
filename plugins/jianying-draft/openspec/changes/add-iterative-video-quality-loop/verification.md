# 目标驱动视频质量循环验证记录

核对日期：2026-09-21。当前 apply 已实现合同、本地/远程评估适配器、代理证据采集、三类副作用账本和质量状态机；质量循环尚未默认启用。

## 依赖门禁

`add-open-workflow-compiler` 仍缺 5.1、7.3 至 7.7，因此本变更不得启用真实自动返工。具体缺口包含启动后落盘前崩溃红测、三条真实剪映链、Windows/三宿主以及回滚验收。

现有质量循环没有 feature flag 为 true 的默认路径。Harness 已增加显式 `quality-evidence`、
`quality-evaluate` 和 `quality-evaluate-remote` 入口；远程入口仍要求精确上传批准、凭据环境变量和预算，不会隐式启动 GUI 或原生导出。

## 红—绿证据

新增 `tests/quality_contracts.test.mjs` 后，首次执行因 `scripts/quality_contracts.mjs` 不存在而 6/6 失败。实现七个严格 Schema、语义校验、大小限制和规范化摘要后，同一组基础测试 6/6 通过；加入 CreativeTarget 构建红测后由 6/8 变为 8/8 通过。

覆盖行为：

- 未知字段、重复键、过深 JSON 和超限输入拒绝。
- CreativeTarget 来源状态、revision、时长和 profile 摘要约束。
- QualityProfile 重复维度、评分边界和未注册动作拒绝。
- EvaluationInput 工件/证据引用和 Verdict 硬门禁优先。
- RevisionRequest 连续 revision、IterationPolicy 有界值和 EvidenceBundle 分层结论。
- 对象键顺序不改变 canonical SHA-256；中文 Unicode 内容保持原值。
- 已确认 Brief 与已审 Route 生成按输出隔离的 CreativeTarget；未确认时长、缺 Profile 或请求身份不匹配均失败。
- 七个质量步骤先因未注册失败，再由受信注册表固定 executor 和端口；handler、错误 executor 或错误端口被拒绝。
- 三份宿主 manifest 指向同一 Harness 时，对同一合同生成相同摘要并保留相同中文内容。
- CreativeTarget 与 IterationPolicy 绑定 WorkflowPlan 和编译回执；改变目标会改变语义摘要，但不会把质量合同写入 `jianying-job/v2`。
- EvidenceBundle 根据实际分项计算 `passed/failed/incomplete`；工件摘要、revision 或输出不一致时拒绝复用。
- Verdict finding 只通过固定动作映射生成 RevisionRequest；未知动作和缺 capability 不能生成命令或 Job。
- 人工评审与确定性技术 evaluator 共用严格输入/输出合同；执行器身份、自由文本结果、命令和批准字段均被拒绝。
- `jianying-skills` 独立变更 `add-video-quality-profiles` 已完成 9/9；不可变 `v2.2.2`、commit `0f0ea4e2f2f9472fba5a03ec394721468ed7073a` 和 manifest SHA-256 `ae62ff9b3a0a5596ade75789c0eb00431969d456e3f7be496a4a341d138e2d41` 已由插件锁定。包级安装能力只要求 `capabilities`、`job.run`、`schema.job_v2`，每项技能仍保留完整场景 capability 门禁。移除开发源码后，fresh install 发布门禁、目录/路由及内容摘要验证通过。
- RevisionRequest 只能生成连续的新 WorkflowPlan revision，并绑定旧计划、verdict 和 request 摘要；原对象保持不变。
- 质量运行批准现在额外绑定 target/profile/policy/verdict/request 摘要、累计预算和 evaluator 资源范围。计划、素材/决策形成的执行摘要、Job、CLI、输出路径或任一质量摘要变化都会使旧批准失效。
- revision、模型调用、累计预算、截止时间和人工复核在替换 compilation 前检查并持久化；最小提升、重复严重 finding、硬门禁或评分回退会产生停止原因。
- 代理证据只通过校验过的 Rust Runtime Adapter 调用固定 `media.probe` 能力；摘要、字节数、时长、画幅、帧率和流信息均绑定同一普通文件。缺失、空文件、符号链接、探测字段不全或探测期间内容替换均失败。
- 调用者不能传入 `passed` 或请求更高 evidence level；代理与技术证据在缺少结构和创作证据时只能形成 `incomplete`，不能提升为最终通过。
- EvaluationInput 现在显式记录字幕、转写和逐语言审校状态；未确认文本只能作为 `context_only`，不能成为事实证据或支撑 pass。Verdict 引用也必须来自同一输入，未知证据 ID 会失败。
- WorkflowRuntime 在质量模式下不再把草稿结构通过直接标成完成，而是依次进入 `rendering_proxy`、`evaluating`，再按严格 verdict 进入 `revision_requested`、`needs_human_review` 或 `iteration_stopped`；缺 capability 可进入 `capability_blocked`。每次转换均落盘历史事件。
- 远程 evaluator 只接受 HTTPS 或本机回环端点，上传批准精确绑定 provider/model、input/profile 摘要、资源摘要、币种和费用上限；请求 ID 确定性生成，调用前写账本。超时/传输未知进入 `ambiguous`，同请求不会重提；响应大小、未知字段和超预算均 fail closed，密钥和 provider 原始错误不进入账本。
- `SideEffectLedger` 对 `draft_write`、`remote_evaluation`、`native_export` 三类副作用统一提供写前落盘、epoch、单写锁、未知结果占用和显式对账；故障注入证明 ambiguous 状态不能自动重试，摘要匹配的成功工件可复用。
- 发布 CLI `v1.6.18`（commit `1dc42790075d3b7f6dace34268d0ba57c98bab2a`）已完成 macOS ARM64、macOS Intel 和 Windows 不可变 Release。macOS ARM64 二进制 SHA-256 为 `82f8ab74468c4864e6e426cda482f5f3c43dc53d59baedfb7e946011c54b41b6`，发布归档 SHA-256 为 `4eaa4b75971d91be9969410bdac1bdbf03f3c2a91eab3b800a92c1a8deac29c8`，capability manifest SHA-256 为 `de4ea006a8478a12c6c69d5f91e83a3354f44f21bd5c30fc5677b156808d0623`，SBOM SHA-256 为 `03c36cda638790c5df7756b0e8cbbbf5f4d53df12644938d0992b6f3281193b5`。
- `v1.6.18` 发布二进制的 `media evidence` 将关键帧、静音、响度和峰值绑定到同一输入摘要。真实素材 `/Users/wandl/Movies/ApowerREC/video/20251224_175557.mp4` 的 SHA-256 为 `2d73da9e64c4a349fa0c144f80bbcf0820f6b7ba0bb829fea7ceaea6314d0c51`；探测为 18.75 秒、1662×1080、帧率 788/75，存在音视频流；关键帧为 0、2.708333、13.1、17.658333 秒，检测到 5 个静音区间，综合响度 -29.9 LUFS、true peak -13.7 dBFS、平均音量 -39.5 dB、最大音量 -14.0 dB。该 bundle 正确保持 `incomplete`，没有把技术证据冒充叙事或审美通过。

## 发布二进制两轮 Vlog 闭环

`scripts/vlog_quality_loop_acceptance.mjs` 拒绝开发 override，只接受校验和锁定的正式 CLI。每一轮保存 Job、草稿、代理、探测、媒体证据、EvaluationInput 和 Verdict；revision 变化会改变目标与 Job 摘要，使旧批准失效。

- 合成素材根目录：`/tmp/jianying-vlog-synthetic.QrEqTX/output`。输入 SHA-256 `da707c7fa0088065425361af90fe368770d2f26405a40fdd97302908a863c58b`；revision 1 代理 SHA-256 `4d7b63aae66b9f298d128793a80909b9bb45034f599fe0560e5f0c4531439410`，确定性 evaluator 返回 `revise`；revision 2 代理 SHA-256 `ad40e9ec5d5c6798546df8815982214980f6c7877534e864423747c7567d37ae`，返回 `pass`；批准重新绑定为真。
- 获准真实素材根目录：`/tmp/jianying-vlog-v1618.sGzPa7/output`。revision 1 代理 6.2 秒、SHA-256 `b43e8321493e1bb911c16944d6771fc8a11b3fbe9b55aee8d875d04ff9d14159`，返回 `revise`；revision 2 代理 3.033333 秒、SHA-256 `20d4ed1e75a6e160b099b28486ba8a92c3b098d3b40eba56d7f29b6be391f10a`，返回 `pass`；批准重新绑定为真。
- 以上 `pass` 仅表示批准的四秒开场规则已修复；脚本明确记录它不替代真实剪映冷重开、连续播放、原生导出和人工叙事/音画评审，因此 8.5 仍未完成。

## macOS 真实剪映 GUI 与原生导出

2026-09-21 使用 `/Applications/VideoFusion-macOS.app`（`CFBundleShortVersionString=11.5.13243`，
`CFBundleVersion=11.6.0-beta2`）在笔记本内置屏逐个冷重开草稿、播放并调用剪映原生导出。七个输出的导出对话框均显示“导出成功”，导出文件均可由 `ffprobe` 解码为 H.264 画面与 44.1 kHz 双声道 AAC：

| 输出 | 原生导出文件 | 时长 | 画幅 | SHA-256 |
|---|---|---:|---:|---|
| Vlog revision 2 | `/Users/wandl/Movies/workflow-vlog-real-binary-main(1).mov` | 3.000000 秒 | 1920×1080 | `cc2bc0d311b7df0c44882ad81e4cbcedd955f85620913056a51d71a3da3441fa` |
| COURSE-01 master | `/Users/wandl/Movies/COURSE-01-master(1).mov` | 120.047166 秒 | 1920×1080 | `4c5ebd5095eda6389e8e9f18e88861774d107db1324d1f78db345c3dbd1b3784` |
| COURSE-01 teaser-1 | `/Users/wandl/Movies/COURSE-01-teaser-1(1).mov` | 10.000000 秒 | 1080×1920 | `88463a1884485ccac89a2a99a9feff0c082d463f684bf85a4bc94b4c390df47b` |
| COURSE-01 teaser-2 | `/Users/wandl/Movies/COURSE-01-teaser-2(1).mov` | 10.000000 秒 | 1080×1920 | `575df7986853792043c2f73a9b3cd322bd9845fef9e6ff5c2cb8c5069ba4c715` |
| COURSE-01 teaser-3 | `/Users/wandl/Movies/COURSE-01-teaser-3(1).mov` | 10.000000 秒 | 1080×1920 | `5229f6780ff98be0acd9e138cc096da734ef120a432dc20992cf5a92ee500e7e` |
| WEDDING-01 ceremony | `/Users/wandl/Movies/WEDDING-01-ceremony(1).mov` | 60.046803 秒 | 1920×1080 | `84b72cc44664d27481422e3ecda3996592ad0e31080c1a4259f0bf114f79e814` |
| WEDDING-01 memory | `/Users/wandl/Movies/WEDDING-01-memory(1).mov` | 15.000000 秒 | 1920×1080 | `9ca60d01c05c68c0e00f32bed7b4d3a7ee54a57c7f462b4dd59327804e0c950d` |

Vlog revision 2、课程四输出、婚礼仪式与私人纪念的冷重开/播放/原生导出已不再是技术阻塞。课程界面可见“第一章”、“第二章”与“Chapter one”字幕文本，但这不等于课程负责人或双语专家终审。婚礼 `memory` 已从 `00:00:00:00` 连续播放到 `00:00:15:00`；`advertisement` 仍因未授予商业用途保持 `commercial_approval_required`，没有生成或导出。人工叙事、音画、教学语境、双语和婚礼情绪评审仍为 `pending`，因此 8.5、9.3 和 10.3 不提前勾选。

对上述七个原生文件进一步抽取代表帧后，不得将这批“导出成功”证据提升为内容验收：Vlog 仅有 3 秒真实屏幕录制，不足以证明完整 Vlog 叙事；课程母版为纯蓝占位，三个预告为占位画面加少量字幕，且 teaser-1 出现中英文字幕重叠；婚礼仪式和纪念片为纯紫占位。这些是可重复视觉证据所发现的确定性不合格，不要求人工审查者为占位媒体签署通过。

为排除占位素材假阳性，又从 Codex 正式安装的插件 `v0.22.0`、锁定发布 CLI `v1.6.18` 与已授权真实录屏 `/Users/wandl/Movies/ApowerREC/video/20260416_230441.mp4` 构建 `COURSE-REAL-01`。母版为 120 秒 1920×1080，三个预告为独立 10 秒 1080×1920 选段，并绑定不同中文字幕。四个 Harness 任务均经历 `intake/inventory/plan/approve/execute/verify/deliver`，终态为 `completed`、证据等级为 `editable_draft`；摘要和代理记录保存于 `/tmp/jianying-real-course-20260921/summary.json` 与 `proxies/`。真实剪映已冷重开母版并显示录屏画面及三处字幕轨；其完整播放、四输出原生导出与人工终审继续独立记账。

## 三代表链发布二进制证据

`/tmp/jianying-representative-v1.6.18/summary.json` 记录无 Cargo 路径、CLI `v1.6.18` 与锁定 Skills `v2.2.2` 的 VLOG-01、COURSE-01、WEDDING-01 黑盒运行。Vlog 12 秒代理 SHA-256 为 `39bb79401e494fa7a2cc17376ccb0124f829c887b1e7afe2cfe1442a89d66891`；课程母版 120 秒代理为 `1c15231317cb632bec22453060cfc6329531d58c459d5c5895027dbe9d1eccbc`，三个 10 秒竖版预告均生成；婚礼仪式 60 秒代理为 `60701dbb1a0735a38c71533f1d9daffa929ec64b8418d364132f9d7d09ea0de5`，私人纪念 15 秒代理为 `ad39274f0e2a9e2b934dc2f96e720bab2bb605b729ae6edbe52a1044b6e29a11`，商业广告因缺授权明确阻断。该证据证明发布二进制执行边界，不替代课程字幕/语境质量返工和婚礼人工质量验收。

### 课程多输出局部返工

`/tmp/jianying-multi-output-captioned.y3gn2X/quality-retry/summary.json` 使用 checksum 锁定的正式 CLI `v1.6.18`（SHA-256 `82f8ab74468c4864e6e426cda482f5f3c43dc53d59baedfb7e946011c54b41b6`）逐输出生成带烧录字幕的 Quality Proxy、媒体证据、字幕/语境记录和独立 verdict。第一轮只有 `teaser-2` 为 `revise`，父流程为 `revision_required`；`master`、`teaser-1`、`teaser-3` 保持通过但不晋级 completed。第二轮只变更 `teaser-2`：Job SHA-256 从 `e94af5474d727fb4ed2f2d4bab79fa2e7bf8219abadb1157184fb14cbbc8c8d1` 变为 `812466a5ebd85468fbc63202f6f6e9e0eb77911a41c20acd6be9eece420a5c65`，`captions_burned=1`，代理 SHA-256 从 `8b0fd1fdbac02617f74bfcfd19f7215d1984a28bac35ef7fef9b2e020c0d3772` 变为 `49332788cbedd217b9dd9a3453c904e6f1e58d8af629176e9da6560645a5bdeb`；三个兄弟输出摘要未变，四份输出独立通过后父流程才为 `completed`。该链为本地确定性课程策略验收，不替代课程负责人、双语专家或真实剪映人工终审。

同一证据记录婚礼私人用途仅授权 `ceremony`、`memory`，`advertisement` 继续以 `commercial_approval_required` 阻断；仪式连续性与私人纪念情绪人工评审仍为 `pending`，因此 9.3 保持未完成。

### 三宿主正式安装包质量循环

不可变插件 Release `v0.21.0`（source commit `ebd6923f1e249ea2980ca4122811dc64fc02b5ef`）经 GitHub Actions run `35600308154` 完成合同回归、macOS arm64、macOS x64、Windows x64 无 Cargo fresh-install、证据聚合与发布。Codex 原生插件管理器安装 `0.21.0+codex.20260921`，ZCode 从旧 `0.11.1` 原生升级到 `0.21.0`，Kimi 官方本机 REST 插件 API 从精确 GitHub tag 安装 `0.21.0` 并报告 `state=ok`、`hasErrors=false`、14 个技能、3 个命令和 1 个 hook。

`/tmp/jianying-host-v0210.OeJ1De` 从三个宿主各自安装缓存运行相同的目标/批准、局部返工、恢复/未知结果对账、取消停止确认和证据分层合同，每个宿主均为 33/33 通过。随后 `real-cross-host.log` 从三个真实安装根分别加载 Harness，并共同调用 checksum 锁定的正式 Rust CLI `v1.6.18` 创建同一真实草稿；1/1 通过，Job Schema、task ID、operation、verification、evidence level 和 verified stages 语义一致。测试未读取开发仓脚本，未调用宿主模型，也未把离线合同提升为真实剪映 GUI 证据。

插件不可变 `v0.20.4` 已发布，commit `9750085e68fae76c47389e45f86c9b2f16186f4d`，Release 归档 SHA-256 `def912a14e3c70e4b8c16cc448e1d272916d54cba8c796ece6895f33624e2af2`。发布工作流 `35597612574` 的合同、macOS ARM64、macOS Intel、Windows fresh-install、聚合证据和 publish 全部通过；三个 canary 均从正式 CLI Release 安装、校验并握手，`cargoAvailableInHandshakePath=false`。

随后把 `v0.20.4` Release 归档解压到 `/private/tmp/jianying-plugin-v0204-fresh.x9TVKa/jianying-draft-plugin`，确认无 `.git`、无 `Cargo.toml`，从归档内以独立 runtime home 重放：

- 真实素材两轮 Vlog：`/private/tmp/jianying-plugin-v0204-fresh.x9TVKa/vlog-two-revision/summary.json`；revision 1/2 代理摘要分别为 `b43e8321493e1bb911c16944d6771fc8a11b3fbe9b55aee8d875d04ff9d14159` 与 `20d4ed1e75a6e160b099b28486ba8a92c3b098d3b40eba56d7f29b6be391f10a`，批准重新绑定为真。
- 三代表链：`/private/tmp/jianying-plugin-v0204-fresh.x9TVKa/three-representative-chains/summary.json`；`no_cargo_path=true`，所有非商业输出摘要与前述发布二进制基线一致，婚礼商业广告仍以 `commercial_approval_required` 阻断。

因此 10.2 的干净发布包、无 Cargo、锁定 Skills/CLI 和三代表链门禁已完成；宿主 GUI 与人工质量仍按 10.3 至 10.5 独立记账。

## 远程 Provider 与故障恢复边界

远程 adapter 使用 OpenAI-compatible Chat Completions 请求体，并把 provider、model、输入/profile/资源摘要、币种、最高费用和版本化 rate card 摘要精确绑定到上传批准。provider 返回 usage 时，账本分别对账未缓存输入、缓存输入和输出 token；缺少可信费用或可重算 usage 时以 `model_cost_unreconciled` 失败关闭。当前验证使用本机回环 provider，没有上传真实媒体或消费外部额度，因此“获准真实远程模型调用”仍是未完成的部署验收，而不是实现缺失。

补充审计发现原实现只把工件摘要放入文本合同，未真正传输媒体。现已要求调用方显式列出 `resources`，逐项绑定 EvaluationInput 中的 `proxy_media`、SHA-256、字节数和 MIME；只接受常规文件，拒绝符号链接、重复/未声明资源、调用前替换和超过默认 7 MiB 的上传。通过校验的代理视频才会作为 OpenAI-compatible `video_url` Base64 Data URL 进入请求；本地路径、凭据和媒体正文均不写入 side-effect ledger。6 个远程 evaluator 测试覆盖纯文本兼容、真实请求体、费用对账、资源篡改、大小限制、超时不重提和非法响应。该能力依据阿里云百炼官方 Chat Completions 多模态合同实现，但仍未执行任何外部付费调用；真实供应商 request-id 与账单继续保持 pending。

上述上传修复已以不可变插件 `v0.22.0`（commit `e15de0ca46031be688ad9d046d02b36a77e63ae1`）发布，GitHub Actions run `35604018764` 的 Node/Python 回归、macOS ARM64、macOS Intel、Windows 无 Cargo fresh-install 与 publish 全部通过；市场清单同步提交为 `a1999c9`。Codex、ZCode、Kimi 的正式 `v0.22.0` 安装根分别通过 42/42 质量/远程/Harness 定向测试，并共同通过 1/1 发布 Rust CLI 跨宿主黑盒验收。这证明修复已进入正式安装包，仍不代替获准的真实供应商调用。

故障向量已保存为自动化测试：profile/批准摘要篡改、同路径素材替换、远程评估超时且禁止重复付费、代理缺失/空文件/符号链接/探测时替换、批准过期、三类副作用提交后崩溃进入 ambiguous、显式停止迭代。所有未知结果都要求显式对账，不会静默重试。

## 兼容回归

执行：

```text
node --test tests/open_workflow.test.mjs tests/workflow_compiler.test.mjs \
  tests/workflow_runtime.test.mjs tests/representative_workflows.test.mjs \
  tests/quality_contracts.test.mjs
```

结果：47/47 通过。包括旧 v1 的 108 场景、v2 的 1/109/1000 条目录、WorkflowPlan、编译器、批准/恢复状态机以及 VLOG-01、COURSE-01、WEDDING-01 离线代表链。

新增合同、步骤与三宿主目标测试为 15/15 通过：

```text
node --test tests/cross_host_contract.test.mjs \
  tests/quality_contracts.test.mjs tests/quality_workflow_steps.test.mjs
```

新增证据、返工过滤、计划 revision、迭代门禁与停滞检测测试为 8/8 通过：

```text
node --test tests/quality_iteration.test.mjs
```

扩展后的返工/停滞、批准绑定与质量状态机定向回归为 24/24 通过：

```text
node --test tests/quality_iteration.test.mjs tests/quality_runtime_binding.test.mjs \
  tests/quality_workflow_steps.test.mjs tests/workflow_runtime.test.mjs
```

独立 evaluator 合同测试为 5/5 通过：

```text
node --test tests/quality_evaluator.test.mjs
```

插件 Node 全量回归：261 项，其中 257 通过、4 项真实发布插件制品测试因尚未提供本轮插件 Release 资产环境而显式跳过、0 失败。插件 Python 发布/分发回归：68/68 通过。四项跳过保持为 10.2、10.5 和 10.6 的发布后门禁，不能由源码树测试替代。
插件 Python 发布/分发回归：68/68 通过；测试中出现的 fixture-skill 错误文本来自预期拒绝负例。

代理/技术证据定向回归扩展为 4/4；远程评估与三类副作用故障定向回归 7/7 通过：

```text
node --test tests/quality_proxy_evidence.test.mjs
node --test tests/remote_quality_evaluator.test.mjs tests/side_effect_ledger.test.mjs
```

## 尚未证明

- 获准真实远程模型的媒体上传、实际账单、provider 超时和供应商侧 request-id 对账尚未执行；当前只有本地协议、预算和故障注入证据。
- Vlog revision 2 已完成真实剪映冷重开、连续播放与原生导出；叙事/音画人工验收尚未签署。
- 课程四输出已完成独立 QualityProfile、字幕/语境本地评估、局部返工和真实剪映原生导出；课程负责人/双语专家终审尚未签署。婚礼仪式与私人纪念已原生导出，但两项人工情绪/连续性评审仍为 pending；商业输出继续因授权缺失保持 blocked。
- GitHub Windows Release 证明 Windows CLI 构建与测试，不证明 Windows 剪映 GUI。
- Codex、ZCode、Kimi 正式 `v0.22.0` 安装包的目标确认、批准、返工、恢复、停止与证据展示已验收；不再是剩余阻塞。
- 插件版本升级、不可变 `v0.22.0` Release、市场清单同步与 fresh-install 黑盒回归已完成；仍缺真实供应商费用/request-id 对账、Windows 剪映 GUI 和上述人工终审，因此 feature flag 仍不得默认开启。

## 2026-09-23：`v0.27.0` 默认关闭 Feature Gate 与三宿主发布后验收

- 不可变插件 Release `v0.27.0` 对应提交
  `71b7b7766357f59e06c375f331c4681a11ce5f1a`，源码归档 SHA-256 为
  `f67a6644bbb92b5541fdbd51e382ba8544a49f8070c496fbeca24b52af32b45d`；GitHub Actions
  run `35763916404` 的合同、macOS ARM64、macOS Intel、Windows x64 fresh-install、证据与
  publish 均通过，市场清单同步提交为 `b921d6b`。
- Codex `0.147.0`、ZCode `0.16.9` 和 Kimi `0.43.1` 从各自独立安装根加载正式
  `jianying-draft v0.27.0`。Codex、ZCode 的安装 checkout 均由 Git 证明精确位于
  `v0.27.0`/`71b7b77`；Kimi 通过已校验的 Immutable Release 归档导入。三个安装根均只调用
  同一发布 `jianying-cli v1.6.24` 二进制，SHA-256 为
  `4fbc5790c6c60b76d5489ed44825e2ffef42e6572be25fc20394e1f5f244e0b0`，并锁定
  `jianying-skills v2.3.0` 的 24 个技能。
- 每个宿主从自己的安装包直接加载 `runtime/feature-flags.json` 和
  `scripts/quality_feature_gate.mjs`：无 opt-in 均以 `quality_loop_disabled` 失败关闭，显式
  opt-in 均返回 `explicit_opt_in`，且共同绑定配置摘要
  `3f5ddb8974cb30dc040eb29e8cbd67d1dde16a0736f81b89d7eac4ea0e4010fb`。源码回归同时证明
  未知字段、preview 默认启用、缺失/过期 gate 被拒绝，关闭 gate 不会改写 ambiguous
  SideEffectLedger 或释放其占用。
- 三宿主分别执行 fresh install 身份、doctor、技能发现、单技能解析、13 分类、106 条动作路由、
  VG01 选择解释、批准失配拒绝、简单 Job、停止、冲突恢复、证据分层和原生导出目标级批准；
  每项 observation 都带时间戳、结构化工件和 canonical SHA-256。
- 三者运行同一 `jianying-job/v2`，Job 输入 SHA-256 均为
  `afde03f207f2026aeb172e345159bbeaad187c845530723864710450b3c484c7`，规范化结果 SHA-256
  均为 `328eb56f8716ad9e22deee15fa5ef84c6d2753e42bc505bf1391ca1bfcb27349`。
  `runtime/host-acceptance.json` 已由记录器提升为 `passed`；14 项宿主证据单测、发布分发校验、
  OpenSpec strict 和 release-readiness 均通过，后者在发布合同范围返回
  `ready=true`、`production_ready=true`。

以上完成任务 `7.9`。Feature Gate 仍保持 `default_enabled=false`：真实远程 Provider 费用与
request-id、Windows 剪映 GUI、Vlog/课程/婚礼人工签署以及商业婚礼授权仍未完成，故不提前完成
`8.5`、`9.3`、`10.3`、`10.4`、`10.6` 或 `10.7`。

## 2026-09-23：真实许可婚礼素材三用途发布二进制预验收

从 Mixkit 官方页面取得五段 1920×1080 H.264 婚礼素材与一段 44.1 kHz 双声道婚礼音乐，
同时保存来源页、视频/音乐许可页快照与 SHA-256。视频许可快照 SHA-256 为
`06ab8f1767d057815f0154ccfd8118348a51ff214aa51e70517d135fc731ad1b`，音乐许可快照
SHA-256 为 `723e4bd4673eeb125480d8d44c11eb591a0391332838485783c9e9928d487177`。
真实媒体摘要如下：

- 戒指：`bb631bfe468294d3bb06914e4737e44e4d89684ce2e8a205e57235c3fe860655`；
- 新人合影：`ca0632978b264365314b307012c7680389ce43a8fe9651a8f5f940ef4a6c7638`；
- 新娘、戒指与花束：`19aceda286f642288239dd451dfe7c3313fbd9d8b0e99099da2c252c8fe9253b`；
- 婚礼桌景：`a2f90734acecf4fce3c803ae1e440850995afbda655212db72300ee381bac7ed`；
- 新人花园步行：`e340b8fb52fa845636fbfb6609538f6e60203d05def1a76c26ce3932fea74b61`；
- `Wedding 01` 音乐：`90b462a5eb37eb3b2b21baa46a175510a39c9349f856e27796942d004d6e1a79`。

验收只从正式安装的插件 `v0.27.0`（commit
`71b7b7766357f59e06c375f331c4681a11ce5f1a`）加载 Runtime Adapter，并通过
`installed_fallback` 消费发布 CLI `v1.6.24`，二进制 SHA-256 为
`4fbc5790c6c60b76d5489ed44825e2ffef42e6572be25fc20394e1f5f244e0b0`；未读取开发仓
Rust 源码、未调用 Cargo、未回退 Python。第一次错误 Job 把 `materials` 放入 `timeline`，发布
CLI 以 task `jy-346c1038f87540568377a2a0ad3f1e25` 和 `invalid_job` 明确拒绝，证明 Schema
门禁没有静默接受错误信封。

修正验收输入后生成三套独立 CreativeTarget、Job、可编辑草稿、带字幕 Quality Proxy、
联系表和媒体证据：

| 输出 | 目的 | task ID | 时长 | Job 摘要 | Proxy SHA-256 | 技术证据 |
|---|---|---|---:|---|---|---|
| ceremony | 私人仪式摘要 | `jy-ab74b7760b1e435f9f6d4dc16e27f689` | 35.994966 秒 | `d851c2bed106d53f30bf29ebe044f8d0c7b7278bf15645e3969acf11e1e819df` | `b8d0c8e636af72b41ef8ae8adbd6521531e08e484a5d6e98ecedcd2aa53d4521` | 6 个关键帧，-31.9 LUFS，音视频可解码 |
| memory | 私人纪念 | `jy-2a720892e815409b94380d6437abe702` | 19.994966 秒 | `e159682e411fd3cade72d3f34db26661ff337144e9767d03884a834e773eac9c` | `efeb6935de13b57991efc01e725debda2274ed7e59941629201a86db26291992` | 4 个关键帧，-33.3 LUFS，音视频可解码 |
| advertisement | 商业广告预览 | `jy-a5f4840a98f34bc6bbf7006f99888dcc` | 13.994966 秒 | `cb9cfc7d44b90bc60076dc16907fdcf7457475cf6c64d7b47a4633d4ac8eef01` | `a9093f62c4dfaff09067b90ac1f77c1c700a37da159b3113409d63c74a72d7e4` | 4 个关键帧，-31.6 LUFS，音视频可解码 |

摘要位于 `/tmp/jianying-v0270-release.aTVP2U/wedding-real-acceptance/summary.json`，SHA-256 为
`e1d7089c3243b39fcd369a5310fa626169521b87844158e30769568020cfae49`。三个 target ID、Job
摘要、Proxy 摘要、输出目录和 task ID 均唯一；私人 `ceremony/memory` 共用
`private-06ab8f1767d05781`，商业预览使用独立 `commercial-969bbecfa2958a9e`，证明用途
授权与证据没有串线。

这里的批准只绑定 `local_acceptance_only`。Mixkit 视频与音乐许可允许本地技术预验收和相应
商业项目使用，但 `wedding.multi-purpose` 质量画像另行要求 `purpose_specific_release`、
`venue_permission` 和商业创意人工审校；三项仍缺，因此商业广告生产发布门禁保持 `blocked`，
不把通用素材许可冒充完整生产授权。

九宫格独立视觉检查确认三套输出使用了不同镜头顺序并非占位色块，但同时发现：字幕在
960×540 Quality Proxy 中偏小；音乐均有约 1.8 秒开头静音，综合响度仅 -31.6 至 -33.3 LUFS；
现有镜头是婚礼主题蒙太奇，不能证明真实仪式事件连续，也没有多机位同步证据。故技术状态只记
`passed`（可解码、时长、关键帧和音频分析），总体状态保持 `needs_human_review`：仪式负责人、
新人/授权代表和商业创意负责人仍须分别签署。任务 `9.3`、`10.3`、`10.6` 不勾选。

### 婚礼三用途 Dream Loop revision 2

独立九宫格与媒体证据把“字幕过小、开头约 1.8 秒静音、综合响度过低”转换为只包含
`caption_edit`、`adjust_volume`、`music_edit` 的局部返工。revision 2 仍使用相同正式插件与
发布 CLI，输出到新的隔离目录
`/tmp/jianying-v0270-release.aTVP2U/wedding-real-acceptance-revision-2`，并以旧摘要
`e1d7089c3243b39fcd369a5310fa626169521b87844158e30769568020cfae49` 作为 `supersedes`
绑定；没有覆盖 revision 1。

- 字幕字号从 8 调到 16，位置从 `y=-0.78` 调到 `y=-0.68`，增加粗体、白字、黑色描边；
- 音乐源起点从 0 调到 2 秒，私人输出音量从 0.22 调到 0.88，商业预览从 0.28 调到 1；
- ceremony task `jy-f94fec1c3d104af19ff3e74fce3eb6a4`，Proxy SHA-256
  `fc451b2b45f9aea1ffa9fdc568106857687b01c0e2f992f5ab1252e7498399f9`，-19.8 LUFS；
- memory task `jy-37bf70879f7c4f97b1c72dc0a844a4fc`，Proxy SHA-256
  `9df447a2d3d0fe6a2e789297cd9fa79be05fa3a445bcf668a36775585cd4595a`，-20.8 LUFS；
- advertisement task `jy-83ea0ed9605b40bdbe763566de2d0c33`，Proxy SHA-256
  `496d1312630c70724d5218ba15b94a69cbbbb8affc342813595d147145fcf4d0`，-20.4 LUFS。

三项时长均精确命中 36/20/14 秒，开头静音区间均变为空，Job 与 Proxy 摘要全部改变；原始
960×540 代表帧复核确认字幕可读性相对 revision 1 明显改善。revision 2 摘要 SHA-256 为
`81536ebe330afe16401441d9febb8e443b8297dcf10efc7bd74f1c3395abe525`。

该闭环证明发布二进制能够根据真实证据完成局部返工，但没有把自动改进提升为人工质量通过：
仪式事件连续性、新人情绪判断和商业创意评审仍为 `pending`；商业生产发布仍缺
`purpose_specific_release` 与 `venue_permission`，保持 `blocked`。因此任务计数仍为 `55/61`。

### 2026-09-23：CLI v1.6.25 锁升级与验收重置

不可变 CLI `v1.6.25` 已发布三平台资产，source commit
`eafb33587341800fd348e780240edab53a1033c3`；同步器只从正典 Release index
导入三平台摘要。插件锁升级前，旧三宿主 `passed` 证据明确绑定 CLI `v1.6.24`，不能
迁移到新锁。故 `runtime/host-acceptance.json` 重置为本候选版本、CLI `1.6.25`、
`status=pending`、`hosts=[]`，保留旧证据文件作为历史记录但不引用为当前通过证据。

插件候选版本升至 `0.27.1` 并同步 Codex/ZCode/Kimi 清单。隔离工作树验证：Python
78/78、Node 全量 321 通过（9 项依赖真实制品/宿主的测试按原合同跳过）、OpenSpec strict、
distribution 与 release readiness 通过；后者明确返回 `ready=true`、
`production_ready=false`。本轮未操作用户屏幕，未进行新版本三宿主 fresh-install、
真实剪映原生导出或人工叙事验收，因此 `10.3`、`10.4`、`10.6`、`10.7` 保持未勾选。

### 2026-09-23：CLI v1.6.26 锁与同步原子性修复

CLI `v1.6.26` 的不可变 Release 已发布三平台资产、SBOM 和 Release attestation，
source commit 为 `0a1affe71d27385f07663f5fe1c8a351d0cca3c8`。正式 arm64
发布二进制在隔离三秒合成草稿上执行 `timeline track-rename`，双镜像同名、属性位与
片段音量不变，`project verify` 无问题；真实剪映界面仍未验收，能力保持 `partial`。

插件 CLI 同步 PR #2 同时纳入三平台锁和 `runtime/host-acceptance.json` 失效记录，
合并后当前锁为 `v1.6.26`，宿主状态 `pending`、`hosts=[]`。发现同步工作流虽然让导入器
原子写入两文件，却只暂存锁文件；新增先 RED 后 GREEN 的回归断言，并修复工作流，使
`git diff` 与 `git add` 都同时覆盖锁和宿主验收记录，避免下次需人工补交失效文件。

插件候选升级至 `0.27.2`。隔离工作树执行 Python 78/78、Node 321 通过及 9 项
按原合同跳过、OpenSpec strict、distribution 与市场清单验证；readiness 返回
`ready=true`、`production_ready=false`。本次没有真实剪映原生导出、Windows GUI、
三宿主新包安装验收或人工质量签署，任务计数仍为 `55/61`，不默认启用质量循环。

### 2026-09-23：真实 Vlog 无音轨证据门禁（6.7）

发布 CLI `v1.6.28` 的 arm64 二进制重新读取真实素材 Vlog revision 2 代理
`/Users/wandl/Movies/JianYing-Acceptance/vlog-travel-2026-09-23/revision-2/proxy-v1628-released.mp4`：
SHA-256 `54ed0be1d2d046aa2cff8fd0772d5a8340f2603ee0bcce7dacba80c16c327a0b`，
13 秒、25 fps、单视频流、`audio.present=false`、响度与峰值为 `null`。新插件代码
`quality-evidence` 返回媒体探测与技术分析，但不生成 `audio_metrics`；锁定 Vlog
QualityProfile 的确定性评估返回 `blocked`、finding `audio_evidence_missing`、
`required_audio_evidence=false`。这只是技术阻断，不是人工叙事或音画验收。
反向黑盒样本使用婚礼 ceremony revision 2 有声代理与同一 CLI `v1.6.28`：
`audio.present=true`、-19.8 LUFS、-7.1 dBFS，生成与代理摘要绑定的
`audio-metrics-6eb2b7ccdd4e7a07b173` 技术证据；评估器还要求其摘要能由同一代理的
`media_quality` 技术证据与代理摘要确定性复算，单独伪造 `role=technical` 不能解锁。

TDD 首先得到 3 项预期失败（无音轨仍 pass、人工上下文声明仍 pass、有声 CLI 分析未形成
音频证据），随后目标测试 12/12 通过。Node 全量 324 通过、9 项按既有合同跳过，
OpenSpec strict 通过。单元测试也覆盖 context-only 伪证据不能解锁、有声发布 CLI
分析生成摘要绑定的 `audio_metrics`、完整技术证据仅使技术评估通过而不评分主观
`audio_visual_coherence`。真实 Vlog 的冷重开、播放、原生导出、人工音画评审仍未完成；
`8.5`、`10.3`、`10.6` 不因本项通过而勾选。
