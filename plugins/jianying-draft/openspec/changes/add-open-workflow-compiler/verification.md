# 开放工作流首批实现验证

核对日期：2026-09-23。当前记账 33/37，覆盖目录、简报、WorkflowPlan、多输出编译、批准/恢复、
结构验证、正式 Skills 消费，以及发布 CLI 的三条代表链黑盒执行。
不是全平台生产验收完成；Vlog 叙事审校、课程专业审校、婚礼商业授权与三宿主仍未完成。

## 环境与合同

- Node v24.18.0；OpenSpec 1.8.0；插件候选 `0.19.0+codex.20260921`。
- 开发目录来自 Skills `2.2.0-candidate`；正式技能锁仍指向旧包，不因开发测试修改。
- 目录 Schema 的唯一来源为 Skills 配套变更 `evolve-open-scenario-catalog`。
- 插件 Schema 测试快照 SHA-256：`b06c91befdf38b37b527ed1fadaa977aa65678b83e7351627f24ea85a8a31377`。
- 测试目录 SHA-256：`084ed9a37893f04a0314a11f63c38414c05d319671b23a51e45ea8b50c26f374`。
- 旧基线 fixture SHA-256：`538f406e88b15202b449b9616c857cd91a160d602b1d3708f3c9880e77185337`。

三份测试快照均与 Skills 来源文件逐字节核对一致；不得将快照作为另一套可独立修改的规范。

## 实现与回归

`scripts/open_workflow.mjs`、`workflow_plan.mjs`、`workflow_compiler.mjs` 和 `workflow_runtime.mjs`
实现显式目录加载、计划、编译、批准、单写、恢复与独立结构验证；旧 `plan-video` 合同不变。

<!-- markdownlint-disable MD013 -->

| 任务 | `tests/open_workflow.test.mjs` 证据 |
| --- | --- |
| 1.1 | v1 113 资源摘要、全部 108 路由语义及无效 Schema；旧入口黑盒不创建状态 |
| 1.2 | 1/109/1000 完整读取；缺 v2、未知版本、摘要篡改拒绝；保留运行时缺失断言 |
| 1.3 | 路径/链接/资源限额/重复键/引用/身份负例；不兼容 consumer contract 拒绝；解析字节与摘要绑定 |
| 1.4 | 双资源旧入口仍见 108，新入口可选第 109 项；正式锁不变，失败不回退开发目录 |
| 2.2 | known/composed/proposed、未知场景无正式 ID、全景交付能力阻断、独立 readiness |
| 2.3 | 硬约束优先、未知值不被偏好遮蔽、空查询最多三项；109 项分页无丢失/重复，版本变化拒绝旧游标 |
| 2.4 | 黑盒在不可用 CLI/PATH 与不存在媒体路径下成功规划，不创建任务状态；结果不可执行 |
| 2.1 | observed/human 等事实来源、观测时间、用途冲突、未知值和缺素材澄清 |
| 3.1 至 3.5 | 严格步骤合同、注册表、类型端口、DAG、独立输出、能力/权限、同路径替换与有界修订失效 |
| 4.1 至 4.6 | 等速半开选段、显式位置、按语言字幕分轨、母版/派生隔离、CLI 身份/能力、摘要及黑盒回执 |
| 5.1 | 双执行者、授予后过期、撤回、输入变化及执行返回后落盘前崩溃的显式故障先行证据 |
| 5.2 至 5.7 | 持久状态、epoch/单写、精确批准、撤回、未知结果对账、取消确认、幂等及分支失败策略 |
| 6.1 | 缺失/损坏/时长不符草稿拒绝；结构证据由独立读取与摘要生成，不采信执行器自报等级 |
| 7.1 | Immutable Skills `v2.2.0`、commit `ed6275c08ab47a25552ccaaa4a70da640cdc948b`、14 技能正式导入；v1/v2 20/20 |
| 6.2 至 6.4 | VLOG-01 12 秒、COURSE-01 四输出、WEDDING-01 三用途的模拟执行、独立读取、替换/许可/多机位负例 |
| 7.2 | 发布 CLI `v1.6.14` 在无 Cargo PATH 下执行三链；完整输入、Job、回执、草稿和代理证据保存于 `/tmp/jianying-representative-v1.6.14-run2` |
| 7.7 | `tests/open_workflow_rollback.test.mjs` 在隔离包执行当前锁到旧锁回退：新入口返回 `catalog_v2_unavailable`，v1 规划剔除 provenance 后与当前输出一致；`reconciling` 的任务状态、执行占用锁和原生导出副作用账本保持，重复提交拒绝。普通 CI 使用 v1-only fixture；本机另用不可变 Skills `v2.1.0` 的真实 tag 内容复跑通过。 |

<!-- markdownlint-enable MD013 -->

本轮重新执行：

```sh
node --test tests/*.test.mjs
node scripts/harness.mjs workflow-plan examples/workflows/vlog_brief.json \
  --development-skill-root /Users/wandl/workspaces/workspace-agent-skills/full-aigc-skills-repositories/jianying-skills/skills/jianying-draft-video-planning
markdownlint-cli2 'openspec/changes/add-open-workflow-compiler/**/*.md'
openspec validate add-open-workflow-compiler --strict
git diff --check
```

5.1 先只加入授予后过期和“执行器成功返回、结果尚未持久化”两条故障测试。旧实现目标运行
为 0/2：前者继续执行并进入未配置 verifier，后者未触发预期异常，证明旧语义无法稳定模拟和
守住这两个门禁。最小实现注入可控时钟和 `execution.returned_before_persist` 生命周期检查点；
检查点异常统一视为未知副作用，保留 execution lock 并进入 `reconciling`。新增测试转绿 2/2，
并与既有双执行者、撤回、revision 输入变化、未知结果和副作用账本测试合跑为 15/15。

本轮全量 Node 回归为 304 项：297 通过、7 跳过、0 失败；Python 测试 70/70。跳过项是
真实归档安装、真实发布布局安装、真实官方资源跨 GUI、专业版资源矩阵、发布 CLI 全表面清单、
真实 Rust 草稿生成和 Codex/ZCode/Kimi 真实安装执行。
模拟锁定安装的摘要验证不替代上述任何真实制品证据。

Vlog 黑盒实际返回：`route=known`、`readiness=needs_input`、`scene.d01.vg01` / `R01`；
`evidence_level=plan`、`executable=false`、`production_ready=false`、`capability_check=not_performed`。
开发目录摘要为 `85951a0d0123a658fca4aa83b6672e87d1fa56e660111b512969a142144177d3`。
输出明确请求素材清单；未读取媒体、调用模型、启动 GUI 或生成草稿。

## v1.6.14 发布二进制与真实剪映证据

- Release 源 commit：`1f8a405ac6cc6185f64b20d8f62df8c6180d6103`；macOS ARM64 二进制摘要：
  `093d81daf9d9b86d935499182a9965ca486dc2e55e1d933749ffafbf92861d24`。
- 三链在不含 Cargo 的 PATH 中运行，`summary.json` 记录 `no_cargo_path=true`。
- VLOG-01：四份 6 秒合成输入各取 `[1s,4s)`；发布二进制生成草稿和 12.000000 秒代理。
- COURSE-01：120.000000 秒代理母版和三个 10.000000 秒竖屏代理；中英确认字幕分轨，待审英文不写入 Job。
- WEDDING-01：60.000000 秒仪式代理和 15.000000 秒纪念代理；广告分支以
  `commercial_approval_required` 阻断，多机位以 `unsupported_edit_mapping` 拒绝。
- 此前真实视频 3 秒 canary 已完成剪映 11.5.13239 冷重开、播放和原生导出；这不替代 12 秒 VLOG-01 的叙事审校。
- 真实剪映已生成课程四份原生 MOV：母版 `120.047166s`、三个预告均 `10.000000s`；母版 1920×1080，
  预告 1080×1920，均为 H.264 + AAC。
- 真实剪映已生成婚礼仪式 `60.046803s` 和纪念 `15.000000s` 原生 MOV，均为 1920×1080 H.264 + AAC；
  商业广告未越权生成。
- 课程教学语境/双语专业审校、婚礼用途审核以及完整 Vlog 叙事验收没有独立人工审校人，因此 7.3 至 7.5 保持未勾选。
- 用户要求不再占用当前屏幕后，已停止所有 GUI 操作；后续 GUI 只可在明确确认的内置屏幕继续。

## 未完成边界与执行顺序

余下 4 项按已有依赖执行：

1. 在不打扰用户主屏的条件下完成 VLOG-01 叙事/音画独立验收、课程专业双语/教学语境审校和婚礼用途审核。
2. 完成 Windows 与 Codex/ZCode/Kimi；全部真实验收完成后再同步与归档，不把回滚测试当作宿主通过。

## 旧锁回滚复核（2026-09-23）

- GitHub `full-aigc-skills/jianying-skills` Release `v2.1.0` 为 immutable；远端 tag 对象
  `0a63cc5b79088906407f41583747c2b0d2980664` 与本地一致，解引用 commit 为
  `686e5e0b68e7b8cc31b853bc43b759d2c6e29ddc`。
- Release manifest 资产 SHA-256 为 `d1122fa4e829283cea17ed1130bf5c9da51526facb738775a30d4d7a7a5f4eea`；
  解包的 `jianying-video-planning` 摘要为 `3b3285b45604d29e76d19f6db8df0dc722404a5d272bb67229908a13f633a6af`，
  与正式 manifest 一致。隔离目录 `/tmp/jy-rollback-v210.xO80L7` 未进入宿主安装路径。
- 普通 fixture 和真实 tag 内容分别执行回滚黑盒，均 1/1 通过；全量 Node 回归 325 通过、9 跳过、0 失败。
  `openspec validate add-open-workflow-compiler --strict` 与 `git diff --check` 通过。
- `JIANYING_OPEN_WORKFLOW_DISABLED=1` 阻断新规划和恢复，旧 `plan-video` 仍能规划；清除开关并切旧锁后，
  `workflow-plan` 明确报 `catalog_v2_unavailable`，占用中的 `workflow-resume` 仍要求人工对账。
  持久状态不删除，未知副作用不重跑。宿主实际设置开关与安装路径仍归 7.6 验收。

只检查用户实际收到的二进制能力；不读取 Rust 源码推断安装端支持。
这些任务暂未完成并不全是外部阻塞；专业审校与目标宿主仍需独立验收。
本次核对尚未提交或推送插件变更，不归档未完成变更。
