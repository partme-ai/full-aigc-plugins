## 1. 契约与迁移基线

- [x] 1.1 锁定依赖的 `jianying-cli` schema、capability 和最低版本，建立插件工作流到 CLI 能力矩阵
- [x] 1.2 清点 Python runner、vendored pyJianYingDraft、`pymediainfo`、外部 headless fork、环境变量和宿主入口
- [x] 1.3 冻结 Codex、ZCode、Kimi 当前可观察行为和失败诊断，建立迁移回归 fixture
- [x] 1.4 定义 intake、inventory、plan、approve、execute、verify、deliver 状态机及 blocked/recoverable/failed 终态

## 2. 单一 Rust Runtime Adapter

- [x] 2.1 实现按平台定位 CLI、开发覆盖路径、版本读取和 SHA-256 校验
- [x] 2.2 实现 `--json` 调用、stdout/stderr 分离、退出码、错误信封和 task ID 的无损适配
- [x] 2.3 实现 version/schema/capability 握手，并对缺失能力输出最低兼容版本与恢复建议
- [x] 2.4 将 commands、hooks 和技能执行统一接入 Runtime Adapter，禁止直接拼装多套执行命令
- [x] 2.5 增加 CLI 缺失、哈希错误、版本过旧、schema 不兼容和可恢复失败的契约测试

## 3. Job 编译与 Harness 编排

- [x] 3.1 实现素材 inventory，先通过 CLI probe 获取时长、流、尺寸、哈希和路径事实
- [x] 3.2 实现用户意图到 `jianying-job/v2` 的确定性编译，不再生成临时 Python 脚本
- [x] 3.3 保存输入摘要、素材哈希、计划路径、CLI task ID、批准范围和验证等级
- [x] 3.4 实现从最后已验证检查点恢复，避免重复付费 ASR 和已完成副作用
- [x] 3.5 实现代理预览、可编辑草稿与原生导出的分级交付判断
- [x] 3.6 为创建、编辑、字幕、音频、批处理、恢复和导出建立端到端 Harness 测试
- [x] 3.7 纠正伪 edit 覆盖：Harness 编译并执行真实 `jianying-job/v2` edit，按源/输出/操作绑定高风险批准，并用真实 Rust CLI 黑盒证明隔离副本编辑

## 4. 审批、任务与诊断

- [x] 4.1 建立只读、可逆写入、高风险写入和外部/原生执行四级风险策略
- [x] 4.2 实现批准对 command、arguments、cwd/target、任务和有效期的精确绑定及拒绝路径
- [x] 4.3 暴露 job list/show/cancel/retry/audit，并在三宿主保持任务状态和终态原因一致
- [x] 4.4 实现 doctor 对 CLI、Schema、技能锁、媒体工具、草稿根和剪映 Runtime Profile 的只读检查
- [x] 4.5 将修复动作与 doctor 检查分离，确保未授权时不安装、不改配置、不启动剪映
- [x] 4.6 验证环境没有 Python、pyJianYingDraft 或 `pymediainfo` 时 doctor 仍可通过 Rust 依赖检查

## 5. CLI 制品分发

- [x] 5.1 建立 macOS arm64/x64 与 Windows x64 制品、checksums 和 capability manifest 的发布消费流程
  - 正式消费证据（2026-09-21）：稳定 immutable `jianying-cli v1.6.13` 已从正典仓发布 10 个资产；release 与 index asset attestation 均通过，index SHA-256 为 `92681d802e1362945d95ab9643d92d44d7060a136718a0f686f204b869e7a497`。插件导入器原子锁定 source commit `c9ba52ad8a359b6938275438c1e41a11b31f1765` 及 macOS arm64/x64、Windows x64 的 archive/binary/capability manifest/SBOM 四重摘要，readiness 中 `cli.platform_artifacts`、`cli.immutable_identity`、`cli.artifact_integrity` 全部 ready。
  - 本地门禁证据（2026-09-20）：fetcher 已在网络前验证 lock 身份，在安装前逐字段绑定 released capability 身份；三平台 canary 证据已固定 archive、binary、capability manifest、SBOM 四重摘要。真实三平台 Release 尚未取得，任务保持未完成。
  - Draft 恢复门禁（2026-09-21）：插件 publish 状态机现安全恢复只上传部分 evidence 的 Draft；已有资产必须按名称、uploaded 状态、长度和 GitHub digest 构成本次完整集合的逐字节相同子集，状态机只上传缺失文件，额外或漂移资产在公开前 fail closed 且不使用 `--clobber`。真实插件不可变 Release 尚未取得，任务保持未完成。
  - 发布竞态门禁（2026-09-21）：同一 workflow/ref 现串行且不取消在先运行；所有公开 Draft 的路径均在最终 `draft=false` 前重新读取远端 evidence assets 并执行完整状态机，避免完整 Draft 快路径绕过最终集合复核。真实插件不可变 Release 尚未取得，任务保持未完成。
  - Tag 绑定门禁（2026-09-21）：初次与最终 publication plan 都重新解析远端 lightweight/annotated tag，并要求直接或 peeled commit 等于插件 checkout；Draft 阶段 tag 移动、删除或异常解析均在 immutable 锁定前 fail closed。真实插件不可变 Release 尚未取得，任务保持未完成。
  - 防篡改与证明门禁（2026-09-22）：优先接受覆盖 `refs/tags/v*` 的安全 ruleset；项目所有者已批准在私有仓套餐明确不提供 ruleset 时使用“Immutable Release＋发布前后 tag commit 复核”作为等价门禁。仓库策略文件要求插件 Immutable Releases 开启，并把创建 Draft 前、公开前、公开后三次 peeled tag commit 与发布 checkout 的绑定固化为精确测试；缺次、乱序或工作流漂移均 fail closed。真实只读远端重放现为 `prerequisitesReady=true`，仅 `release.plugin.expected` 因 `v0.26.0` 尚未发布而保持 blocked；本项不据此冒充真实 Release 或宿主安装完成。
- [x] 5.2 用市场包体、离线安装和宿主限制测试比较随包分发与按平台下载，并用 ADR 确定正式方案
- [x] 5.3 实现确定性的安装式 fallback；不支持或未安装的平台必须报告 not-ready
- [x] 5.4 实现 fresh-install 后无需 Cargo 构建即可完成 CLI version/capability 握手的验证
  - 本地门禁证据（2026-09-20）：手工与 tag 工作流已共用三平台 evidence 汇总 job，拒绝未知/过期 evidence JSON 和缺项/身份漂移的 readiness；contract 或矩阵失败时汇总仍执行并落盘结构化失败 JSON；正式 canary 还把 Skills 版本、CLI 下界和完整 `minimumCapabilities` 绑定已安装二进制，仅接受全部 `supported`，三平台汇总器重新绑定当前技能锁。门禁先暴露 `media.audio` 缺失与 `timeline.quantization_report` 只有领域测试，现均已补齐；当前候选继续按预期拒绝 4 个仍为 partial/external 的真实宿主能力。最终 cutover 也必须先执行同一三平台无 Cargo 安装 canary，且只允许最后的 Rust-only 发布面暂时阻塞。无正式制品/宿主，不能替代三平台 fresh-install，任务保持未完成。
  - 隔离 released 演练（2026-09-21）：CLI 当前候选在临时 Git 仓以本地 `v1.6.0` tag 重编译，archive 携带 `released`、tag 和隔离 source commit，严格 SBOM/归档门禁通过。插件以该 archive 和解压 bundle 分别执行真实 fetch/install/handshake，在 `PATH=/usr/bin:/bin` 下 2/2 通过；同一 fetcher 也正确拒绝了 `working_tree_unreleased` archive 冒充正式 tag。该证据证明无 Cargo 消费合同，不替代尚缺的 macOS x64、Windows x64 和 GitHub Release canary，任务保持未完成。
  - 正式三平台证据（2026-09-22）：不可变插件 `v0.24.0` 的 macOS arm64、macOS x64、Windows x64 三份 Release canary 均从不可变 `jianying-cli v1.6.19` 安装，绑定 source commit `81684a952ccfad9d1cff98d4c470dd500e74e57b`，逐份证明包内 capability manifest 与二进制握手完全一致、Skills 所需能力全部 supported、运行源为 `installed_fallback` 且 `cargoAvailableInHandshakePath=false`。聚合 evidence 为 ready；当前 `v0.25.0` tag 归档也在隔离目录以同一发布 CLI 完成无 Cargo fresh-install 和握手。
- [x] 5.5 增加被篡改制品、下载中断、离线环境和回滚旧版本的测试

## 6. 三宿主一致性

- [x] 6.1 将核心 prompt、风险策略、命令 schema 和结果呈现提取为共享数据
- [x] 6.2 更新 Codex manifest/commands/hooks，使其仅通过共享 Harness 调用 Rust CLI
- [x] 6.3 更新 ZCode manifest/commands/hooks，使其仅通过共享 Harness 调用 Rust CLI
- [x] 6.4 更新 Kimi manifest/commands/hooks，使其仅通过共享 Harness 调用 Rust CLI
- [x] 6.5 用相同 fixture 在三宿主验证核心工作流、授权、错误、恢复和结构化结果等价

## 7. 技能锁与单向同步

- [x] 7.1 定义 `skills.lock.json`，记录 `jianying-skills` 版本 ref、commit、完整清单、逐技能摘要和最低 capability
- [x] 7.2 实现仅从技能仓覆盖 vendor 的同步脚本，并阻止反向或局部手工同步
- [x] 7.3 增加缺失技能、内容漂移、版本不匹配和 CLI capability 不满足的 CI 门禁
- [x] 7.4 验证插件运行脚本、宿主适配和配置不会被技能同步覆盖
- [x] 7.5 锁定消费修复退休 headless plan supporting reference 的 `jianying-skills >= 2.0.3`，并验证 13 个目录摘要与新 manifest
  - 本地门禁证据（2026-09-20）：导入器、attestation、正典 tag/commit、13 个目录摘要和最低版本门禁均已就绪；远端审计发现自动 PR 原先依赖不存在的 `skills-sync` label，现已移除该非必要阻塞。真实 `v2.0.3` Release 与锁定同步尚未发生，任务保持未完成。
  - 下载字节门禁（2026-09-21）：Skills 同步现将同一 immutable Release 的 GitHub asset 元数据落盘，在 attestation 与导入前验证唯一文件名、uploaded 状态、正典 URL、正大小，并重新计算本地 manifest 大小和 SHA-256 与 GitHub `digest` 对齐；缺失、重复、篡改或元数据漂移均 fail closed。该验证器已对真实 immutable `v2.0.2` Release 下载的 4,878 字节 manifest 通过，实际 SHA-256 与 GitHub digest 同为 `a80df2c2a58b0989e94d51bce7aed7c5c32d98575acbd64b981a1d44687e8665`；随后真实 `gh release verify-asset` attestation 也通过并将 tag 解析到 `336dc9e57c6ede6b3b7efe923823f7b2209dbb2e`。真实 `v2.0.3` 仍未发布，任务保持未完成。
  - 来源目录边界（2026-09-21）：导入器现在拒绝技能目录或内容中的 symlink/特殊文件，并在原子替换前保留旧 lock 与技能树；不会跟随链接把 checkout 外内容复制进插件。当前锁定 `v2.0.2` 的 13 个真实目录摘要复核继续通过；真实 `v2.0.3` 仍未发布，任务保持未完成。
  - 正式锁定消费证据（2026-09-21）：`jianying-skills v2.0.4` 已发布为稳定 immutable Release；下载 manifest 的 5,048 字节与 GitHub `sha256:21345983c877772303f5d21c9d16dfaebe17e8646db9f18a50a167d493864ea4` 一致，release 与 asset attestation 均验证通过。导入器锁定提交 `7917242f39349484e6785ae759c79381e934e15a`，原子导入并复核 13 个技能目录摘要；`skill_vendor.py check`、完整 Python 测试和 release readiness 中的 `skills.immutable_release`、`skills.content_digests` 全部通过。

## 8. 删除旧引擎与强依赖

- [x] 8.1 在每项工作流 Rust canary 达标后逐项切换唯一执行路径，禁止对同一目标双写
- [x] 8.2 删除 Python runner、vendored pyJianYingDraft 和相关 Python 依赖、测试及安装步骤
- [x] 8.3 删除外部 headless checkout、`JIANYING_HEADLESS_ROOT` 和 fork-first 路由
- [x] 8.4 对旧环境变量和旧命令返回明确迁移诊断，不提供静默 Python/fork 回退
- [x] 8.5 扫描发布包、文档、脚本和 CI，证明不存在 Python 引擎或外部 fork 运行依赖
  - 本地门禁证据（2026-09-21）：distribution validator 与 release readiness 已覆盖 README、docs、scripts、commands、hooks 和 workflows，允许历史来源记录但拒绝可执行旧 runner、fork checkout、环境变量赋值和 vendored 源码启动命令。归档级门禁直接读取而不执行/解压候选包，拒绝多根、路径穿越、链接/特殊文件、Python 缓存和退休运行路径；当前工作树生成的 212 文件、13 技能候选归档已通过并证明 `pythonDraftEngine=false`、`externalHeadlessRuntime=false`。tag workflow 现同时保存并发布归档本体与 JSON 审计，审计绑定归档 SHA-256、插件版本和插件 commit，聚合器会重新计算实际归档摘要并拒绝缺失、篡改、身份漂移或额外资产。真实最终 Release 包尚未生成，因此任务保持未完成。
  - 正式归档证据（2026-09-22）：不可变插件 `v0.24.0` 的 437 文件 Release 归档审计绑定 archive SHA-256 `8c9d7a05b28775bbaa5c1002503ba61c00b88089ae48012e99fc4f26090077f9` 与 source commit `9ec761f4653aaad413c72b200c77da13d22b24f7`，明确为 `rustOnlyRuntime=true`、`externalHeadlessRuntime=false`、`pythonDraftEngine=false`；当前 `v0.25.0` 的 24 技能候选再次通过 distribution validator、离线 vendor check、归档审计和完整测试。保留的 `JIANYING_HEADLESS_ROOT` 只产生“已忽略”迁移诊断，不构成运行依赖；其最终删除仍由 8.3/9.6 单独门禁。

## 9. 全链路验收与发布

- [x] 9.1 在 Codex、ZCode、Kimi 分别执行新鲜安装、doctor、草稿构建、任务恢复和审批测试
- [x] 9.2 在真实剪映执行可编辑草稿冷重开、播放检查和经独立批准的原生导出
- [x] 9.3 验证插件只报告实际达到的证据等级，不以代理预览替代最终 MP4
- [x] 9.4 验证 CLI、技能和插件版本兼容矩阵、checksums 与许可证材料完整
  - 本地门禁证据（2026-09-21）：插件版本 bump 已同步 catalog、三宿主 manifest、中英文 README，并强制使旧宿主验收失效；隔离 fixture 与 distribution validator 均已覆盖版本漂移。发布 canary/汇总器现已从只验证三个核心能力提升为绑定技能锁的完整能力矩阵，修复两个本地契约缺口后，当前准确暴露 4 个仍依赖真实剪映宿主的未 supported 能力。只读远端预检当前确认 CLI/插件 Immutable Releases 未开启，CLI v1.6.0、Skills v2.0.3 与插件 v0.17.2 Release 均不存在；它现在精确校验 CLI 10 个发布资产、Skills manifest，以及插件归档/审计/readiness/三平台 canary/verification 7 个资产，并要求每项非空、uploaded、具有 GitHub `sha256:` digest 和对应仓库/tag 的正典 URL。真实 `jianying-skills v2.0.2` 已证明该查询/校验路径可用；空壳、缺项、额外资产、摘要或 URL 漂移不会标记 ready。该预检已进入 release gate，手工预演保留 JSON 但不中断，tag 路径会在三平台矩阵前强制真实上游 Release 与三仓设置。真实三平台摘要与最终许可证包仍未同时取得，任务保持未完成。
  - 消费链加固（2026-09-21）：CLI index 与 Skills manifest 两条同步 workflow 现在都把下载文件实际字节绑定 GitHub Release API 的 size/digest/state/canonical URL，再独立验证 GitHub attestation，最后才调用原子导入器；该改动补齐了远端资产元数据、下载字节和导入内容之间的证据闭环，但不替代尚缺的真实 Release 与三平台验收。
  - 当前兼容矩阵（2026-09-22）：`v0.25.0` 的 Codex/ZCode/Kimi/marketplace 版本一致；CLI 锁固定 `v1.6.19`、source commit `81684a952ccfad9d1cff98d4c470dd500e74e57b` 及三平台 archive/binary/capability/SBOM 摘要；Skills 锁固定不可变 `v2.3.0`、commit `23e6ce195f5e3ef3c003d58bf262620f8603735a`、24 个技能摘要和 manifest SHA-256 `889504f710c5b31c8ecfcee0f06bf947fcb070556aaa8c2f2b3a9a851b1341ce`。readiness 的版本、制品、兼容矩阵和法律材料检查全部 ready，`LICENSE`、`NOTICE`、`PRIVACY.md`、`TERMS.md`、`THIRD_PARTY_NOTICES.md` 均为非空分发文件。最终 `v0.25.0` 三宿主发布/安装仍属于 9.6，不由本项替代。
- [x] 9.5 演练插件/CLI 制品回滚和草稿快照恢复，确认不恢复 Python 自动回退
- [x] 9.6 完成三宿主发布门禁后再移除迁移期变量兼容并标记变更可归档
  - 宿主证据加固（2026-09-22）：十三项生产检查现在逐项要求带时间戳的宿主/命令证据对象及 canonical SHA-256；纯布尔声明、缺项、额外项和内嵌证据篡改均被记录器与最终汇总器拒绝。加强合同已提升为 v2，并生成未提交、未发布的 `v0.26.0` 候选；已发布 v1 定义保持不变。三宿主尚未安装该候选并产生真实观察，本任务保持未勾选。
  - 正式 Rust-only cutover（2026-09-23）：不可变 `v0.26.2` Release、签名 attestation 与 tag peeled commit 复核通过；Codex、ZCode、Kimi 从正式市场或该 Release 归档完成隔离 fresh install，并分别用校验和锁定的 `jianying-cli v1.6.24` 执行 13 项 observation。三宿主 Job 输入摘要为 `e51cda22bc2be0034d04e59a301a56b58f0472f6f29e1cba746b02a3c44d9dfc`，语义结果摘要同为 `328eb56f8716ad9e22deee15fa5ef84c6d2753e42bc505bf1391ca1bfcb27349`；readiness 为 `production_ready=true`。运行期已不存在 `JIANYING_HEADLESS_ROOT` 读取、外部 checkout 或 fork-first 分支。
