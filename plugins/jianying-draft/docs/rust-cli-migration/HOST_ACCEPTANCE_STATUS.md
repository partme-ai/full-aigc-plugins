# 三宿主真实验收状态（2026-09-20）

本文只记录实际执行证据，不把 manifest fixture 或本地契约测试冒充真实宿主验收。

## 当前主机清点

| 宿主/应用 | 实际证据 | 状态 |
|---|---|---|
| Codex CLI | `codex-cli 0.153.4`，支持 `plugin marketplace add` 与 `plugin add` | 已完成隔离临时快照安装和真实 Rust CLI 草稿构建；正式发布安装仍待完成 |
| ZCode | `/Applications/ZCode.app` 3.14.0，内置 `zcode 0.16.9` CLI | 已完成隔离临时快照安装、宿主发现和真实 Rust CLI 草稿构建；正式发布安装仍待完成 |
| Kimi Code | `kimi 0.43.1`，提供隔离 `KIMI_CODE_HOME` 与本地 REST 插件 API | 已完成隔离本地路径安装、宿主发现和真实 Rust CLI 草稿/恢复/审批测试；未调用模型 |
| 剪映专业版 | `/Applications`、`~/Applications` 与 Spotlight 均未发现 | 真实冷重开、播放、原生导出不可执行 |

## Codex 隔离 fresh-install 证据

使用新的临时 `CODEX_HOME`，未读取或改写用户现有插件安装状态：

```bash
CODEX_HOME="$ISOLATED_CODEX_HOME" \
  codex plugin marketplace add \
  /Users/wandl/workspaces/workspace-agent-skills/full-aigc-plugins --json

CODEX_HOME="$ISOLATED_CODEX_HOME" \
  codex plugin add jianying-draft@full-aigc-plugins --json
```

Marketplace 注册成功，插件安装在解析 `v0.17.1` 时失败：

```text
Error: git checkout v0.17.1 failed
error: pathspec 'v0.17.1' did not match any file(s) known to git
```

这是正确的 fail-closed 结果：当前插件工作树没有提交、tag 或 GitHub Release，不能把
`main` 或脏工作树冒充可安装发布版。随后使用隔离的本机临时 tag 完成了宿主功能验收；
正式发布门禁仍保持未完成。

## Codex 临时快照执行证据

为验证安装缓存内的插件，而不是工作区脚本，另建临时 Git 仓库并对当前工作树快照创建
仅本机可见的 `v0.17.1` tag；通过 Git `url.insteadOf` 将 canonical repository 临时映射
到该仓库。该操作没有提交、推送或发布用户仓库，也不构成正式 release 证据。

隔离 `CODEX_HOME` 中的真实 `codex plugin add` 成功安装
`jianying-draft@full-aigc-plugins`，随后从安装缓存执行 `tests/real_cli_harness.test.mjs`：

- 使用 `jianying 1.6.0` release-mode 本地二进制及精确 SHA-256；
- ffmpeg 生成 320×240、30fps、1 秒的真实 H.264 测试媒体；
- 完成 probe inventory、Job v2 编译、任务级批准、`job run --json`、草稿验证和 resume；
- 生成 `draft_content.json` 与 `draft_meta_info.json`，CLI verification 返回 `ok=true`；
- resume 读取 completed 检查点，没有重复执行副作用。

该验收发现并修复了旧 Harness 把 `project` 编译成空对象的问题。现在 `project` 是 v1
计划的强类型领域投影，`compatibility.payload` 继续保存完整编辑语义。由于正式三平台
CLI 制品与真实剪映仍未验收，OpenSpec `5.4`、`9.2` 继续保持未完成。

## ZCode 隔离安装与执行证据

使用 `ZCODE_STORAGE_DIR` 创建独立存储根，通过 ZCode 内置的原生插件命令完成：

```text
zcode plugins marketplace add <local-marketplace> --scope user --json
zcode plugins install jianying-draft@full-aigc-plugins --scope user --json
zcode plugins list --json
```

ZCode 从临时 tagged Git 快照安装 `jianying-draft 0.17.1`，识别到 13 个技能、1 个命令根和
可执行的 SessionStart Harness hook。从安装缓存执行真实 CLI 测试后，草稿创建、验证与
resume 全部通过。

首次验收发现 `.zcode-plugin/plugin.json` 显式声明 hooks 会与 ZCode 对
`hooks/hooks.json` 的自动发现重复，产生 `plugin_hook_invalid`。删除重复声明后重新隔离
安装，`plugins list --json` 的 diagnostics 为空，hook 仍被正确发现。该临时快照未提交、
推送或发布，因此仍不等同于正式 fresh-install 发布证据。

## Kimi 隔离安装与执行证据

使用独立 `KIMI_CODE_HOME` 启动只绑定 `127.0.0.1` 的临时 Kimi Web Server，通过官方
`POST /api/v1/plugins` 从本地插件目录安装，并用 `GET /api/v1/plugins` 读取宿主解析结果。
Kimi 报告插件 `state=ok`、`hasErrors=false`、13 个技能、3 个命令、1 个 hook，并识别
`sessionStart.skill=jianying-use`。整个过程没有提交 prompt 或调用模型。

从 Kimi 的 `plugins/managed/jianying-draft` 安装目录执行真实 Rust CLI 测试，验证了：

- doctor、素材 probe 和强类型 Job v2 编译；
- 错误目标批准返回 `approval_scope_mismatch`，正确批准只能消费一次；
- 已存在输出目录导致真实 CLI 失败，retry 清空旧批准并保留 inventory/checkpoint；
- 移除临时冲突后重新批准，草稿构建与验证成功；
- completed resume 不重复执行，审计历史不增长。

同一更新后的测试也从 Codex 与 ZCode 的新鲜安装缓存再次通过。因此插件 OpenSpec `9.1`
已有三宿主黑盒证据并已勾选。所有临时宿主根和 Kimi Server 均隔离；Kimi Server 已通过
`POST /api/v1/shutdown` 正常终止。

随后 `tests/real_cross_host_cli.test.mjs` 从三个宿主各自的实际安装目录加载 Harness，针对
同一素材、Plan 和输出目标依次运行。三者生成相同 `jianying-job/v2`、相同确定性插件
task ID、相同 evidence level/verified stages，并均由 Rust CLI 返回 `operation=create`、
`verification.ok=true`。因此 CLI OpenSpec `9.4` 已具备真实跨宿主差分证据并已勾选。

## 工作树真实 Rust edit 回归

在未修改三个宿主安装缓存的前提下，`tests/real_cli_harness.test.mjs` 已直接绑定当前
checksum-pinned Rust CLI 工作树二进制，先生成带本地视频 assets 的可编辑草稿，再由
Harness 编译 `job.run.edit`：

- edit Job 明确携带源草稿、全新输出和 `move_segment` 强类型操作；
- 批准 command 为 `job.run.edit`，精确绑定 Job 摘要、源目录、输出目录和任务；
- Runtime Adapter 没有向 edit 重复传入 create 专用 `--out`；
- CLI 先将源素材路径重定位到临时副本，操作完成后再重定位到最终输出；
- 输出草稿结构校验通过，源 `draft_content.json` SHA-256 保持不变。

该证据证明工作树插件到工作树 Rust CLI 的真实隔离 edit 链路，不等同于三宿主正式
发布制品验收，也不满足真实剪映冷重开/播放/原生导出门禁。

同一 canary 现已扩展为所有已支持工作流的实际 Runtime Adapter 调用：创建草稿后通过
Rust CLI 导入 SRT、修改音频音量、从 MutationPlan snapshot 恢复、生成真实 ffmpeg 代理
MP4，并执行包含两个 create 子作业的原子 Job v2 batch；随后继续完成隔离 edit 和失败后
重新批准的 retry。测试使用当前二进制的精确 SHA-256，所有调用均经过 capability handshake，
没有 Python、外部 headless 或同目标双写。因此插件任务 `8.1` 的已支持工作流 Rust canary
与唯一执行路径门禁已满足；原生导出继续按 `external_dependency` 阻止，不作降级。

运行期 `scripts/jydraft_run.py`、`scripts/jydraft_check.py`、`hooks/env_check.py` 以及 vendored
pyJianYingDraft 已从候选工作树删除。全量分发测试与 readiness 现在报告
`runtime.legacy_engines_removed=ready`，因此插件任务 `8.2` 已完成。不可变 `v0.26.2` 完成
三宿主 fresh-install 后，Node Harness 中最后的 `JIANYING_HEADLESS_ROOT` 迁移诊断与一次性
`rust-cutover` workflow 也已删除；运行时不会读取外部 checkout，也不存在 fork-first 回退。

## 真实制品布局安装 canary

当前 `1.6.0` arm64 工作树 canary 已通过与正式制品相同的安装路径：

- 生成包含 236 个 Cargo package 的 SPDX SBOM；
- 打包二进制、Schema、capability manifest、许可证、逐文件 manifest 与 checksums；
- 安装到空目录时重新校验每个声明文件；
- 从 `PATH` 移除 Cargo 与 Homebrew；
- Runtime Adapter 从 `installed_fallback` 完成握手，确认 `capabilities`、
  `schema.job_v2` 和 `job.run` 均为 `supported`。

最新复验绑定源码提交 `60eae921acd4fb8161eaa69c85b31d8c2267332c`，内嵌身份明确为
`working_tree_unreleased` 且 `release_ref=null`。本次 archive SHA-256 为
`78d07db9764fcdbc306d87371ab50fcf366a914807c7b690dfa335a95ebbd976`，二进制 SHA-256 为
`a92a23a5394477dd373e301cb5eaffcb24b7ad44c06742e6657e924167c76a0e`，SPDX SBOM SHA-256 为
`90bc8291ecd92a099ad9e0bf1b4c34f0f6b6b71e9c7b2a53c18130157abb7240`，capability manifest
SHA-256 为 `a7cf23c82c7fa0a27544794c35356f57707952c025dc91649bcb0319968b73c6`。插件安装器重新验证
全部声明文件后原子安装，随后在 `PATH=/usr/bin:/bin` 下完成 version/capability 握手，
证明该路径没有借用 Cargo、Homebrew 或源码构建。

`tests/real_cli_bundle_install.test.mjs` 将本地 bundle 安装路径固化为条件式黑盒测试；当前
`working_tree_unreleased` 候选已通过该路径，并实际验证 `media.audio`、
`timeline.quantization_report` 及量化命令输出。`tests/real_cli_archive_fetch.test.mjs` 则只用于真实
不可变 Release：把当前工作树 tarball 注入该路径时会按预期以
`release_capability_identity_mismatch` 拒绝，因为其不是 `contract_state=released` 且没有 tag。
正式 Release 后仍须用原测试完成下载、解包、校验、安装和握手，不能以本地 bundle 测试替代。
当前 bundle 包含 `project.compile` 与 `schema.compile_v1_compat` 能力。
bundle 安装测试还直接执行已安装二进制的 `media tts --help`，验证本地命令、macOS/Windows
系统 TTS、loopback HTTP、本地进程和 Edge TTS 六种 provider 均实际存在于制品命令面。
同一黑盒检查还验证小米、火山、阿里、百度、腾讯、MiniMax 与智谱七种云端审批计划 provider；
并从安装后的二进制实际执行 MiniMax 与火山 V3 `--plan`，确认无需秘密环境变量即可生成哈希化费用审批
绑定、不会泄露原文且不会修改草稿。当前制品还公开 `--approval-id`、`--approval-root` 与
`--tts-state-root`；火山命令面明确公开 `--resource-id`、`--uid` 并返回官方 V3 SSE endpoint。
新候选还必须由同一安装式黑盒验证 `media.asr_whisper_cpp=supported`，并执行安装后二进制的
`media transcribe --help`，确认 executable/model 身份、格式、语言、翻译、segment 时间戳、
plan 零执行、state root 和显式 retry 参数全部存在。此处只证明离线 Runtime Adapter/CLI 契约，
不等同于真实模型转写质量或剪映字幕写回验收。
安装式黑盒还要求 `runtime.discovery=supported`，实际执行 `runtime discover --json` 并验证
`automatic_routing=false` 与 `support_status=unverified`；发现应用或草稿根均不能替代真实
Runtime Profile、app-open、playback 或 native-export canary。
制品包含七个云端 provider 的审批后真实 HTTP 执行器；协议形状、ledger、
幂等复用和失败/不确定状态已由 CLI 的 loopback 黑盒测试覆盖。安装后的 `render --help` 还必须
公开 `native-task` 生命周期；未调用真实付费服务，也未把合成生命周期证据冒充真实剪映导出。
这仍只是发布前证据：
内嵌状态为 `working_tree_unreleased`，因此任务 5.1、5.4 继续保持未完成。正式发布后必须以
`JIANYING_EXPECT_BUNDLE_STATE=released` 对不可变下载制品重跑同一测试。

正式安装 canary 现已进一步要求已安装二进制满足 `skills.lock.json` 的完整能力下界，并把 Skills
版本、最低 CLI 版本、完整能力列表和 supported 断言写入三平台证据。聚合器会再次绑定当前技能锁。
以当前候选 manifest 对现有技能锁执行该门禁时，会按预期拒绝
`captions.verify`、`render.native`、`runtime.status` 和 `runtime.profile`，因为它们仍为
`partial` 或 `external_dependency`；`media.audio` 命名漂移和 `timeline.quantization_report`
缺少黑盒命令的问题已补齐真实契约测试并提升为 supported。这证明旧的“三个核心能力通过”
不能再被误认为完整技能运行面生产就绪。对应真实能力和宿主验收完成前，任务 5.4 与 9.4 保持未完成。

## Skills v2 不可变发布导入证据

`jianying-skills v2.0.2` 已作为非草稿、非预发布的 GitHub Immutable Release 发布。
`jianying-skills.manifest.json` 已通过 `gh release verify-asset` 验证，Release 资产摘要为
`a80df2c2a58b0989e94d51bce7aed7c5c32d98575acbd64b981a1d44687e8665`，manifest 固定：

- release ref：`v2.0.2`；
- source commit：`e26e6b1c483a435479dadd87130da93ad2e5aaa1`；
- 13 个技能聚合摘要：`d59e926ddefae73d04f4cbae209ab4267413969dd12b559d25110beaf4f04fa5`。

插件只通过 `scripts/import_skill_release_manifest.py` 原子导入该 tag，并重新验证远端 peeled
commit、manifest 正典仓库、13 个目录摘要和 CLI capability 下界。导入后全量扫描确认
`skills/`、`commands/` 与 `hooks/hooks.json` 不再包含 Python、pyJianYingDraft 或外部
headless 执行路径；因此 Skills OpenSpec `8.3`、`8.4` 和插件 OpenSpec `2.4` 已有实际
发布与消费证据并勾选。

后续源码复核发现 `jianying-harness/references/plan-format.md` 仍把退休的外部 headless plan
描述为活动输入契约。修复已随稳定 immutable `jianying-skills v2.0.4` 发布；插件现锁定 tag
`v2.0.4`、提交 `7917242f39349484e6785ae759c79381e934e15a` 和 manifest SHA-256
`21345983c877772303f5d21c9d16dfaebe17e8646db9f18a50a167d493864ea4`。13 个技能已原子导入并
通过逐目录摘要、版本和 readiness 复核，技能发布不再阻塞最终 Rust-only cutover。

2026-09-21 的 CLI 隔离发布演练把当前候选复制到临时 Git 仓，以本地 `v1.6.0` tag 和提交
`18f2fc2632c2044987eb89f3863a6aa20507de20` 重新编译、生成严格 SPDX SBOM 并确定性打包。
archive SHA-256 为 `7f206eb0172c3550f766cd13814d580bddeb861ecfa5887de26f0e63e72f2deb`；正式 fetcher 与 bundle
installer 在无 Cargo PATH 下均完成安装和 capability 握手。该演练不属于 GitHub Release 或
三平台正式制品，`5.1`、`5.4` 仍保持未完成。

发布前隔离演练已把当前候选复制到临时 Git 仓，建立并推送本地 `v2.0.3` tag，由正式
`skill_manifest.py release` 生成 `released` manifest；13 个技能聚合摘要保持为
`6198259b50845b1b4f28ac0668c112a303a19199966a14efe58499de8af905d4`。插件导入器在 CLI
模式下正确拒绝非 GitHub 正典远端；通过仅供离线测试的已解析 commit 注入点后，真实原子替换、
本地来源复核、逐技能摘要和 readiness 全部通过，`skills.immutable_release` 与
`skills.content_digests` 均转为 ready。该演练证明候选发布与消费链兼容，但不是实际 GitHub
Release，不能代替任务 7.5 或 Skills 8.6。

## 继续验收所需外部证据

1. 补齐 `captions.verify`、`render.native`、`runtime.status`、`runtime.profile` 的真实宿主能力，
   使正式无 Cargo 安装 canary 满足 Skills 完整能力下界。
2. 发布插件 `v0.17.2`，在全新 Codex、ZCode、Kimi 配置中执行 doctor、草稿构建、
   恢复和目标级审批。
3. 安装受支持剪映版本后执行冷重开、播放检查及独立批准的原生导出。

Kimi 的实际 prompt 会调用模型，原生导出可能启动外部应用；在获得相应授权和运行环境
前不执行，也不以静态 manifest 测试替代。

## CLI v1.6.13 正式消费结果

2026-09-21，插件从正典 immutable `jianying-cli v1.6.13` 下载并验证 release index；Release
为稳定、非草稿、非预发布且 `isImmutable=true`，10 个资产均带 GitHub SHA-256。index 大小
1,861 bytes，SHA-256 为
`92681d802e1362945d95ab9643d92d44d7060a136718a0f686f204b869e7a497`，release 与 asset
attestation 均通过。导入器把 `runtime/jianying-cli.lock.json` 原子更新到 source commit
`c9ba52ad8a359b6938275438c1e41a11b31f1765`，并锁定三个平台的 archive、binary、capability
manifest 与 SBOM 摘要；readiness 的三个 CLI 制品检查全部转为 ready，因此 OpenSpec `5.1`
完成。

本机 arm64 随后从 Release 下载并安装真实 archive，在受限 `PATH=/usr/bin:/bin`、无 Cargo
握手路径下成功验证 released identity、archive/binary/capability manifest/SBOM 摘要与
`installed_fallback`。最终 Skills 契约检查按设计拒绝四项尚非 `supported` 的能力：
`captions.verify`、`render.native`、`runtime.status`、`runtime.profile`。因此这次结果证明发布消费
链已完成，也证明完整能力矩阵仍不满足；OpenSpec `5.4`、`9.4` 继续保持未完成。

手工 GitHub release gate run `35536303352` 又在 `macos-15` arm64、`macos-15-intel` x64 和
`windows-2025` x64 三个平台重新下载同一锁定 Release、验证摘要并执行无 Cargo 安装。三份 canary
均到达 Skills 完整能力检查，并以相同的 `skill_capability_contract_incomplete` 失败；版本兼容均为
true，唯一拒绝项仍是上述四项 partial/external capability。contract job、归档审计和非发布态
distribution gate 已通过，publish 按设计跳过。该结果排除了平台下载、解压、二进制身份和基础握手
差异，但不是成功 canary，不能勾选 `5.4` 或绕过真实剪映门禁。

最终 cutover 现已增加机器可读的 `runtime/host-acceptance.json` 门禁，当前状态明确为
`pending`。证据格式、版本绑定、原始文件摘要和跨宿主语义等价规则见
`docs/rust-cli-migration/HOST_RELEASE_EVIDENCE.md`。在三份真实宿主证据齐全前，readiness 会报告
`hosts.release_acceptance=blocked`，`rust-cutover` 不会移除迁移期变量诊断。

`rust-cutover` 还必须在删除迁移诊断前完成 macOS arm64、macOS x64、Windows x64 三个平台
的真实锁定制品下载、无 Cargo 安装和 capability 握手，并用统一 evidence verifier 聚合。
cutover 专用模式只能暂时接受 `runtime.release_surface_rust_only` 这一项阻塞；任何 CLI/Skills
身份、摘要、宿主验收、兼容矩阵或许可证阻塞都会 fail closed。删除迁移诊断后还会重新运行完整
release readiness、distribution gate 和测试集。

2026-09-20 的只读远端复核显示：`full-aigc-plugins/jianying-draft` 仍无 GitHub Release；
`full-aigc-skills/jianying-skills` 最新不可变 Release 仍为 `v2.0.2`，远端没有 `v2.0.3` tag。
因此三平台 canary 与最终 cutover 尚无可执行的正典输入，本记录不把本地候选演练升级为正式证据。
同次复核还确认插件仓只有 GitHub 默认 labels，原工作流要求的 `skills-sync`、`cli-sync` 和
`rust-cutover` labels 均不存在。三个 PR 创建路径已移除该非必要强依赖，避免正式 Release 出现
“同步分支已成功推送、PR 却因标签缺失而无法建立”的半完成状态。

候选分发审计进一步覆盖 README、docs、scripts、commands、hooks 和 workflows：历史来源记录可以
保留旧项目名称，但任何可执行旧 Python runner、外部 headless clone/checkout、迁移变量赋值或
vendored Rust 源码启动命令都会同时阻断 distribution validator 与结构化 readiness。中英文
README 的包版本也已从漂移的 `0.17.1+codex.20260919` 对齐到 manifest 的
`0.17.2+codex.20260920`，并由回归测试持续约束。最终 Release 包仍未生成，因此任务 8.5 不提前
标记完成。

归档级审计已补齐源码树扫描的盲点：release gate 从待发布 commit 生成源码归档后，直接验证成员
路径/类型、必要清单、13 个技能入口及 Rust-only 表面，并保存 `jianying-plugin-archive-audit/v1`
证据。本地当前工作树候选归档含 212 个文件，审计结果为 `passed`、
`pythonDraftEngine=false`、`externalHeadlessRuntime=false`；恶意链接、退休 Python runner、外部
headless clone 指令、Python 缓存和技能缺项均有负向测试。该证据仍是本地候选，不替代正式不可变
Release 的归档审计。
三平台 evidence verifier 现要求恰好一份通过的归档审计，并把归档名称、文件数、技能数和
Rust-only 状态绑定最终 verification JSON；因此 workflow 上传审计文件后不会被当作未知 JSON，
也不能用缺失、重复或伪造的审计记录拼出绿色发布证据。
归档本体现在与审计 JSON 一起进入 workflow artifact 和不可变 Release asset；审计新增
`archiveSha256`、`pluginVersion` 与 `pluginSourceCommit`，聚合器从实际归档重新计算摘要并与当前
release checkout commit、插件 manifest 版本绑定。发布后的下载回检和 GitHub asset attestation
同时覆盖归档与 JSON，避免只发布“通过声明”而遗漏被审计的插件包。

版本漂移的根因也已修复：市场仓发版工具与插件内副本现在会在 bump 时同步 README 完整 Codex
版本，并把 `runtime/host-acceptance.json` 重置为新基础版本的 `pending`、清空 hosts。市场主工具
已通过隔离临时 catalog/插件仓的真实 patch bump 测试，不会改动当前工作仓版本。
工具完成提示也已改为“发版候选已生成”，并明确 tag workflow、Immutable Release、制品校验和
真实市场安装仍待完成；普通 commit/push 不再被描述为正式发布。
剪映插件内工具副本现已与市场主本逐字节一致，并使用 `--plugin=jianying-draft` 定向生成/校验市场
清单；`sync-release-tooling --dry-run` 对剪映仓只剩自定义 `AGENTS.md` 差异，本轮没有覆盖该文件。
市场同步工具现已默认保留所有仓库既有 `AGENTS.md`，只有显式 `--refresh-agents` 才允许更新；策略
单元测试覆盖缺失文件创建、自定义文件保留和显式刷新。新的 dry-run 中剪映工具链显示“已同步”，
自定义项目指令仅记录为保留项，不再进入写入计划。

新增的只读远端发布预检已在真实 GitHub 状态执行。当前结果为：Skills 仓 Immutable Releases
已开启；CLI 与插件仓仍为关闭；预期 CLI `v1.6.0`、Skills `v2.0.3`、插件 `v0.17.2`
Release 均不存在。报告的 `prerequisitesReady=false`、`releaseComplete=false` 与本地 readiness
阻塞一致，且执行过程中没有创建或修改任何远端对象。
该预检现已接入 `release-gate.yml` 的 contract 首段：手工 `workflow_dispatch` 会保留
`jianying-plugin-remote-preflight` artifact 后继续候选验证；tag 路径则依据
`prerequisitesReady` 在三平台 runner 启动前 fail closed。插件自身 Release 不属于该前置集合，
避免要求工作流在创建 Release 前先看到同一 Release；正式发布完成后的 `releaseComplete` 仍用于
终态复核。预检 artifact 使用独立名称，不会混入四文件 release evidence 集合。
