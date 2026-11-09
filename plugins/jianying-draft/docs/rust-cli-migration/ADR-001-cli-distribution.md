# ADR-001：CLI 按平台制品分发

- 状态：Accepted
- 日期：2026-09-19
- 关联变更：`route-all-execution-to-rust-cli`

## 背景

插件需要同时支持 macOS arm64、macOS x64 与 Windows x64。当前三个宿主清单没有
声明“同一插件版本按操作系统/架构选择不同包体”的能力，因此把三个二进制全部塞进
插件会让每个用户下载两个永远不会执行的制品，也会扩大供应链检查面。

本地测量基线：

| 项目 | 大小 | 证据边界 |
|---|---:|---|
| 当前插件工作树 | 9,680 KiB | 含 Git 元数据和迁移期文件，不等于市场压缩包 |
| 迁移期 Python vendor | 5,708 KiB | 删除旧引擎后消失 |
| macOS arm64 release 二进制 | 15,700,864 bytes | 当前 1.6.0 工作树 canary，本机可执行并完成 fresh-install、云端 TTS、本地 ASR、Runtime discovery 与原生导出任务命令面握手 |
| macOS x64 release 二进制 | 17,088,096 bytes | 当前源码交叉编译、clippy 和全测试目标链接通过；当前主机无 Rosetta，未执行 |
| macOS arm64 完整压缩制品 | 6,562,815 bytes | 当前 1.6.0 工作树 canary；含 Schema、capability、许可证、236-package SBOM 和 checksums |
| Windows x64 交叉构建候选 | 10,928,640 bytes | 云端 HTTP 执行器接入前的历史 PE32+ x86-64 候选；当前主机不能执行，不能代表当前源码 |

Windows 压缩大小必须由 `windows-2025` runner 的真实制品补充，不能用 macOS
二进制改名估算为发布证据。

当前 x64 交叉编译产物 SHA-256 为
`3d06d9dff26d77875a6321dd2d10d592b178167e4679bfff26ec8926cb7475e8`；Mach-O 与 load
command 静态检查、完整 workspace x64 target clippy 均通过，
但在无 Rosetta 主机上执行返回 `Bad CPU type in executable`。因此不为该文件生成
release-entry，也不把交叉编译等同于 Intel runner 的 native 握手。

本轮 TTS 根命令接入之前的 Windows 候选 SHA-256 为
`d5c713a35adbbcc37657f761ea4850121929e32522d312d36d9c72d62ac82548`。当前主机使用 Zig
完成 release workspace 和 70 个测试目标的交叉链接，且 Windows target 的完整 workspace
`clippy --all-targets -- -D warnings` 通过；但没有 Wine/Windows Runtime，不能执行
version/capability/test，也不把该文件打包成可消费 release-entry。
该旧候选不再代表当前命令面，且此前隔离安装的 `cargo-zigbuild` 已不在当前环境；未静默重装。
当前源码必须由 `windows-2025` 工作流重新构建和执行后才能形成可消费证据。

## 决策

采用“薄插件 + 版本锁定的按平台 release artifact”，不在通用插件包中捆绑三个
平台二进制：

1. CLI 发布流水线生成三个独立制品及 archive checksum。
2. 插件 release lock 固定 URL、archive SHA-256、binary SHA-256、版本和 capability
   schema；缺少任一平台记录时不得切换正式运行路径。
3. 下载/解压由显式 `fetch_cli_artifact.mjs install|upgrade` 阶段负责，Runtime Adapter
   本身不联网；fetcher 只接受 lock 固定的官方仓库/tag URL，并验证 archive、binary、
   capability manifest 与 SBOM 四重 SHA-256，同时要求 capability 内嵌版本、released 状态、
   tag 和 source commit 与不可变 lock 完全一致。
4. `install_cli_bundle.mjs` 只消费已经解压的本地制品，完整验证 manifest 后原子安装。
5. 离线安装通过预先携带制品并指向 `--bundle` 完成，不要求 Cargo、Python 或网络。
6. upgrade 保存旧二进制到 checksum 命名的 rollback slot；显式 rollback 只交换两个
   已验证 Rust 制品，绝不恢复 Python 或外部 fork。

## 结果

- 优点：每台主机只安装一个制品；宿主清单保持一致；离线预置与在线下载共用同一
  校验/安装路径；Runtime Adapter 无下载副作用。
- 代价：首次安装需要宿主市场或安装器取得匹配制品；离线环境必须预置 artifact。
- 发布门禁：正式 release index 和三个平台的实际 CI 证据齐全前，插件保持
  `not-ready`，commands/hooks/skills 不切换默认路径。
- 发布恢复：GitHub attestation 可能在 Release 公开后延迟。重跑只接受同 tag、稳定、
  immutable 且远端证据资产集合与逐文件 SHA-256 完全匹配本次构建的 Release；此时只恢复
  `verify-asset` 轮询，不上传、不覆盖，任何差异都 fail closed。
- Draft 恢复：首次上传中断时，只允许名称、uploaded 状态、长度和 GitHub digest 完全匹配的
  既有资产子集；状态机只上传缺失证据，完整集合复核后才公开。额外或漂移资产在公开前失败，
  不使用 `--clobber`，不删除远端资产。
- 发布串行：同一 workflow/ref 不并发修改 Draft，且不取消已经进入发布流程的运行。完整 Draft
  快路径同样在公开前重新读取远端 assets 并执行状态机，避免初次规划与 immutable 锁定之间的
  竞态绕过。
- Tag 绑定：GitHub 在 Draft 公开前允许关联 tag 变化，因此状态机初次和最终规划都重新解析远端
  tag；lightweight tag 直接取 commit，annotated tag 使用 peeled commit，并要求等于插件发布
  checkout。tag 漂移或删除会在 immutable 锁定前失败。
- 发布保护：插件 tag workflow 使用仓库 secret `RELEASE_RULESET_READ_TOKEN` 读取插件仓库
  repository/organization ruleset 完整详情。该 fine-grained token 仅需插件仓库 Administration
  read；Release 创建和上传仍使用 `github.token`。如果 GitHub 明确返回私有仓当前套餐不提供
  ruleset，则使用项目所有者批准的 `runtime/release-protection-policy.json` 作为等价门禁：插件
  Immutable Releases 必须开启，并在创建 Draft 前、公开前和公开后精确三次重新解析远端
  lightweight/annotated tag 的 peeled commit，要求其等于发布 checkout。任何缺次、乱序、tag
  漂移、策略字段缺失或工作流摘要漂移都 fail closed。CLI 与 Skills 由各自发布 workflow 验证
  本仓保护，插件只消费已经公开且 immutable 的上游 Release，不要求跨仓管理权限。
- 发布预演：`workflow_dispatch` 不创建插件 Release，因此可在仓库 Immutable Releases 设置
  尚未开启或上游正式 Release 尚未就绪时运行正式锁校验和三平台 fresh-install；预检结果仍以
  独立 artifact 保存。tag 路径在完整测试与三平台矩阵前强制 CLI、Skills、插件三仓均启用
  Immutable Releases，并要求锁定的 CLI 与 Skills 稳定 immutable Release 已真实存在。
- 自动同步：CLI、Skills 与最终 cutover workflow 分别串行化；更新专用 PR 分支前重新读取远端
  SHA 并使用显式 `--force-with-lease=<ref>:<sha>`。这允许可审计地刷新自动化分支，同时在远端
  发生并发变化时拒绝覆盖。

## 已验证场景

- 本机 arm64 制品在无 Cargo 环境中 clean install 并完成 version/capability 握手。
- 被篡改制品在安装前被 SHA-256 拒绝。
- 缺文件模拟下载中断时，当前 active runtime 保持可用。
- 本地 bundle 离线安装不访问网络。
- release-layout archive 已通过模拟下载、archive 摘要校验、临时解压、成员摘要校验、
  原子安装和无 Cargo 握手全链路 canary。
- 1.6.0 → 1.7.0 → 1.6.0 rollback 只在校验通过的 Rust runtime 间切换。
