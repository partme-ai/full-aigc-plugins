# Rust Runtime Adapter

`scripts/runtime_adapter.mjs` 是插件调用 `jianying-cli` 的唯一新运行时边界。
当前阶段只建立并验证 Adapter，不切换 commands、hooks 或技能的默认执行路径。

## 开发模式

开发模式必须同时指定二进制和 SHA-256，不能只提供路径：

```bash
export JIANYING_CLI_PATH=/absolute/path/to/jianying
export JIANYING_CLI_SHA256=<64-character-sha256>
node scripts/runtime_adapter.mjs handshake
node scripts/runtime_adapter.mjs job run ./job.json --out ./draft
```

## 握手门禁

Adapter 在每次作业执行前验证：

1. 平台对应的二进制位置或显式开发覆盖路径。
2. 文件 SHA-256 与发布锁、已验证制品 manifest 或开发环境声明相同。
3. `jianying --version` 不低于锁定最低版本。
4. `jianying capabilities --json` 返回 `jianying-capabilities/v1`。
5. `capabilities`、`schema.job_v2`、`job.run` 均为 `supported`。

任何一步失败都会返回 `type`、`message`、`details`、`recovery`，且禁止回退到
Python runner 或外部 headless checkout。

## 分发边界

`runtime/jianying-cli.lock.json` 目前尚无发布制品条目，因此正式安装仍是
not-ready。后续发布流程必须为 macOS arm64/x64 与 Windows x64 写入下载制品和
SHA-256，完成 fresh-install 验证后才能切换默认执行路径。

已解压制品通过 Node 安装器消费；安装器逐项验证 `manifest.json` 中的路径、
大小和 SHA-256，拒绝路径逃逸和原地覆盖：

```bash
node scripts/install_cli_bundle.mjs \
  install \
  --bundle /absolute/path/to/jianying-cli-1.4.0-darwin-arm64 \
  --install-root /absolute/runtime/root
```

升级与回滚必须显式执行，且 rollback target 使用旧二进制 SHA-256 标识：

```bash
node scripts/install_cli_bundle.mjs upgrade --bundle /absolute/new-bundle --install-root /absolute/runtime/root
node scripts/install_cli_bundle.mjs rollback --install-root /absolute/runtime/root \
  --platform darwin-arm64 --sha256 <previous-binary-sha256>
```

安装式 fallback 固定读取以下位置，也可以用 `JIANYING_CLI_INSTALL_ROOT` 覆盖
根目录：

- macOS：`~/Library/Application Support/PartMe/jianying-draft/runtime/<platform-arch>/`
- Windows：`%LOCALAPPDATA%\PartMe\jianying-draft\runtime\<platform-arch>\`

目录必须同时包含 `jianying`（Windows 为 `jianying.exe`）和相邻的
`jianying.sha256`（Windows 为 `jianying.exe.sha256`）。缺少 checksum、文件被
修改或平台不是 macOS arm64/x64、Windows x64 时，Adapter 明确返回 not-ready，
不会现场执行 Cargo 构建。

当前已用本机 arm64 release bundle 在清空环境变量、仅保留系统 `PATH` 的条件下
完成安装后 `--version` 与 capability 握手。该证据只覆盖 macOS arm64；另外两个
平台仍必须由各自 CI runner 产生和验证真实二进制。

正式发布取得三平台 release index 后，使用以下命令原子写入 CLI lock。任何平台
缺失、URL 非 HTTPS、checksum 缺失、source commit 非法或 capability schema 不兼容
时都会拒绝更新。导入成功后，lock 同时固定 `resolvedVersion`、`sourceCommit` 与三个
平台的 archive/binary/capability/SBOM 摘要：

```bash
node scripts/import_cli_release_index.mjs \
  --index /absolute/release-index.json \
  --lock runtime/jianying-cli.lock.json
```

导入 lock 后，在线安装或升级必须由用户显式运行独立 fetcher；doctor、SessionStart、
Runtime Adapter 和 Job 执行均不会自动下载：

```bash
node scripts/fetch_cli_artifact.mjs install \
  --lock runtime/jianying-cli.lock.json \
  --install-root /absolute/runtime/root
```

fetcher 只选择当前平台，限制 archive 为 256 MiB，固定官方仓库/tag/文件名，验证 archive、
binary、capability manifest 和 SBOM 摘要，并在临时目录解压后交给原子安装器。网络失败、
摘要不符或不安全成员不会触及当前 active runtime。
下载前还必须确认 lock 同时具有合法 source commit 与 `jianying-capabilities/v1`；解压后再将
capability manifest 的 `cli_version`、`contract_state=released`、`release_ref` 和
`source_commit` 与 lock 逐字段比较。即使 archive 和成员摘要本身有效，身份分裂也不得安装。
三平台 release canary 会把 archive、binary、capability manifest、SBOM 四个摘要全部写入
证据，并深度比较已安装二进制的 `capabilities --json` 与包内 capability manifest。
最终汇总器逐项与平台 lock 对比，同时要求 `capabilityManifestMatchesRuntime=true`；任何摘要
缺失、漂移或二进制与 manifest 内容分裂都会拒绝发布证明。
正式 canary 还读取插件自身的 `skills.lock.json`，要求已安装 CLI 版本不低于技能锁下界，且锁中
每个 `minimumCapabilities` 都在二进制 manifest 中精确标记为 `supported`。成功证据固定
`skillsVersion`、`skillMinimumCliVersion`、完整 `skillRequiredCapabilities` 与
`skillCapabilitiesSupported=true`；三平台汇总器重新绑定当前技能锁，拒绝缺项、顺序漂移、旧技能
版本或伪造的 supported 断言。该门禁覆盖完整技能运行面，不再只凭插件启动所需的三个核心能力
判断正式制品可用。
`release-gate.yml` 的独立 evidence job 在 tag 和手工 `workflow_dispatch` 两条路径都会下载
readiness 与三个 canary，生成 `release-evidence-verification.json`；只有 tag 路径在此之后继续
创建 Release，手工预演也不会停留在三个互不关联的 action artifacts。
即使 contract 或任一平台 fresh-install 失败，evidence job 也会运行：它先建立空证据目录、容忍
下载步骤缺少上游 artifact，再由同一汇总器 fail closed，并上传包含稳定错误类型的结构化
verification JSON。平台失败因此不会把最终诊断连同被跳过的 job 一起丢失。
汇总器只接受上述四个基础 JSON 和至多一个自身生成的 verification JSON；未知文件、重复汇总、
旧 source commit、不同平台集合或基础文件清单漂移都会失败。传入的 CLI lock 即使位于同一临时
目录也被作为输入排除，不会被误当作发布证据资产。
readiness 也不能只是 `ready=true` 的空壳：汇总器要求 11 个固定且唯一的检查全部 ready，并把
顶层插件版本、CLI 版本/ref/source commit、Skills 版本/ref/commit 分别绑定当前插件清单与锁文件。
市场事实源与插件仓的 bump 工具会同步 catalog、三宿主 manifest 和中英文 README 的完整 Codex
版本，并把 `runtime/host-acceptance.json` 重置为新基础版本的 `pending` 空宿主集合。隔离 fixture
会真实执行一次 patch bump；distribution validator 另行拒绝 README/manifest 版本漂移，避免新
版本复用旧宿主证据或再次发布错误版本说明。
Bump 命令的成功状态只表示“发版候选已生成”，输出会明确指出尚未提交、推送、打 tag 或发布；
只有 tag workflow、GitHub Immutable Release、制品校验和真实市场安装均取得证据后才能称为发布
完成。版本文件写入或普通 Git push 不再被工具误报为正式 Release。
`python3 scripts/remote_release_preflight.py` 补充本地 readiness：它通过 `gh` 只读查询 CLI、Skills
和插件三仓的 Immutable Releases 设置与预期 Release，输出
`jianying-remote-release-preflight/v2`。`repository.plugin.release_protection` 优先验证覆盖
`refs/tags/v*` 的安全 ruleset；当 GitHub 明确返回私有仓套餐不提供该功能时，只接受仓库内经
项目所有者批准的 `runtime/release-protection-policy.json`。该等价策略同时要求插件仓库已开启
Immutable Releases，且发布工作流在创建 Draft 前、公开前和公开后精确执行三次远端 tag peeled
commit 与当前 checkout 的绑定复核；次数、顺序或工作流摘要发生漂移都会 fail closed。
`prerequisitesReady` 不要求插件 Release 已存在，
`releaseComplete` 则必须包含当前插件稳定 immutable Release；查询失败只会形成结构化 blocked，
`blockedPrerequisites` 只列出会阻断 tag 构建的上游 Release 与三仓设置，`blocked` 还会包含尚待
本工作流创建的插件 Release。脚本不创建 tag、Release、PR，也不修改仓库设置。
Release 存在本身不足以通过：预检要求 CLI 精确包含三平台 archive、checksum、release entry 与
index 共 10 个资产，Skills 精确包含 release manifest，插件精确包含归档、归档审计、readiness、
三平台 canary 和最终 verification 共 7 个资产。每项还必须是非空 `uploaded` 资产、具有 GitHub
`sha256:` digest，并使用相应仓库/tag 的正典下载 URL；空壳、缺项、额外资产、摘要或 URL 漂移
均保持 blocked。该校验已对真实 immutable `jianying-skills v2.0.2` 响应通过。
`release-gate.yml` 会在 contract 的其他门禁前运行该检查并始终上传
`jianying-plugin-remote-preflight`。手工 `workflow_dispatch` 只采集证据并继续候选验证；tag 路径只看
`prerequisitesReady`，因此不会循环要求尚待本次工作流创建的插件 Release，但会在三平台 runner
启动前拒绝缺失的 CLI/Skills Release 或任一仓库 Immutable Releases 设置。
剪映插件内的 `scripts/bump-plugin.mjs` 已与 `full-aigc-plugins` 市场事实源逐字节一致，包含可选
`plugin.json`、结构化 marketplace ref/icon/logo 更新和 `--plugin=jianying-draft` 定向同步。
因此剪映 bump 不会再被其他插件的独立元数据漂移阻断；全量 release-tooling 同步仍会尝试重写
各仓自定义 `AGENTS.md`，本次未执行该范围外写入。
正式 release contract job 使用 `node --test tests/*.test.mjs` 执行完整 Node 契约集；新增安装、
证据或真实制品条件测试无需再手工加入工作流列表，避免本地已覆盖而发布门禁漏跑。

最终 Rust-only cutover 不再仅凭 lock/readiness 的静态形状删除迁移变量。`rust-cutover.yml` 先要求
readiness 的唯一阻塞项精确等于 `runtime.release_surface_rust_only`，再分别在 macOS arm64、
macOS x64 和 Windows x64 下载锁定制品、完成无 Cargo 安装与 capability 握手。聚合器只有在三个
canary 均完整、且 readiness 没有延后任何其他门禁时，才接受 `--allow-cutover-pending`；随后删除
迁移诊断并重新执行全绿 release readiness、distribution gate 和完整测试集。这样三平台
fresh-install 证据发生在 cutover 之前，也不会与“最终发布面必须已经 Rust-only”的门禁形成循环。

CLI 正式 Release 会发送 `cli-released` 通知；`.github/workflows/cli-sync.yml` 只从
`full-aigc-plugins/jianying-draft` 的精确 tag 下载 index，交叉验证通知携带的 index 摘要与
source commit，再原子更新 lock 并创建 PR。每日定时任务用于通知 token 缺失或投递失败时的
补偿，不会绕过同一正典仓库、tag、三平台和摘要校验。
CLI、Skills 与 cutover 自动化创建 PR 时不依赖未预创建的专用 label；远端只存在默认标签也不会
出现“分支已推送但 PR 永久创建失败”。并发安全仍由 workflow concurrency 与显式 lease 保证。
同步流程只接受 `isImmutable=true`、非 draft、非 prerelease 的 CLI Release；定时发现也显式
排除草稿与预发布版本。插件自身正式 tag 的 release gate 同样要求仓库已启用 GitHub 原生
Immutable Releases。
下载 release index 或 Skills manifest 后，流程先保存同一稳定 immutable Release 的完整 GitHub
资产元数据，并用 `scripts/verify_github_release_asset.py` 要求目标文件名唯一、状态为 uploaded、
大小为正、携带 `sha256:` 摘要且 URL 精确属于对应仓库/tag；验证器重新计算本地下载字节的
大小与 SHA-256。随后还必须通过 `gh release verify-asset` 校验 GitHub 自动生成的签名
attestation，两个独立门禁都通过后才允许进入本地 schema、仓库、tag、commit 和逐制品摘要检查。

运行期 Python runner、Python SessionStart shim 和 vendored Python 引擎已经从候选工作树删除；
SessionStart 只调用 Node Harness。CLI 三平台锁和 Skills v2 不可变锁均合并、readiness 只剩
迁移变量残留后，`rust-cutover.yml` 才会创建最终 PR：精确删除旧变量迁移测试和 Harness 中的
外部 checkout 环境变量兼容。删除后必须同时通过 readiness、`--release` 分发校验和完整契约
回归；其他任何阻塞项存在时 workflow 只报告等待，不修改文件。

Rust-only 分发审计覆盖 README、`docs/`、`scripts/`、`commands/`、`hooks/` 与 GitHub
workflows。它允许来源基线和迁移记录以历史语态提及旧项目，但会拒绝可执行的旧 Python runner、
外部 headless clone/checkout、`JIANYING_HEADLESS_ROOT` 赋值或 vendored Rust 源码启动命令。
命中结果同时进入 `runtime.release_surface_rust_only` readiness evidence，避免只扫描宿主入口而漏掉
runbook 或 CI 中仍然活动的旁路。

release gate 还会用 `git archive` 从待发布 commit 生成精确源码归档，并通过
`scripts/validate_plugin_archive.py` 直接审计成员。审计不会解压或执行归档内容：它要求单一根目录、
仅普通文件/目录、完整法律与宿主清单、13 个技能入口，并拒绝路径穿越、链接/特殊文件、Python
缓存、退休引擎路径和活动外部 fork 命令。结果写入 `jianying-plugin-archive-audit/v1` JSON，随其余
release evidence 保存；归档本体也作为显式 Release asset 保存。审计记录绑定归档 SHA-256、插件
版本和插件源码 commit，发布证据聚合器会读取实际归档重新计算 SHA-256，并拒绝缺失、篡改、身份
漂移和未声明资产。
三平台 evidence verifier 将该归档审计作为必需且唯一的输入，重新验证 `passed`、13 个技能、
Rust-only、无 Python 草稿引擎和无外部 headless runtime，并把摘要绑定进最终 verification JSON；
未知或重复 JSON 仍然 fail closed。
