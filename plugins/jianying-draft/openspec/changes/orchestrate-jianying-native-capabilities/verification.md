# 验证记录

## 2026-09-22：面板分类技能族锁定消费

- 不可变上游：`jianying-skills v2.3.0`，commit `23e6ce195f5e3ef3c003d58bf262620f8603735a`，Release manifest SHA-256 `889504f710c5b31c8ecfcee0f06bf947fcb070556aaa8c2f2b3a9a851b1341ce`，GitHub asset attestation 验证通过。
- 导入结果：插件锁定 24 个技能，其中 13 个面板分类技能均为独立目录；vendored 内容与锁文件逐目录摘要一致。
- 动线覆盖：13 类共 106 个唯一语义动作，每类至少 6 个；自动测试要求入口、执行路由、验证和恢复字段，并拒绝坐标型生产合同。
- CLI 边界：技能候选使用不可变 `jianying-cli v1.6.19` 发布命令目录和 capability manifest 校验；插件最低 CLI 基线同步提升到 `1.6.19`。`partial`、`external_dependency` 和 GUI-only 路由仍会 fail closed。
- 定向回归：`tests.test_skill_release_gates` 7/7 通过；分发校验报告 24 skills；离线 vendor check 通过。

未完成：Codex、ZCode、Kimi 正式 `v0.25.0` 安装包的 13 分类发现、路由、停止、恢复和证据展示验收尚未执行，任务 `7.5` 保持未勾选。

### `v0.25.0` 当前宿主安装审计

- Codex：正式安装缓存
  `/Users/wandl/.codex/plugins/cache/full-aigc-plugins/jianying-draft/0.25.0+codex.20260922`
  存在，三宿主 manifest 版本、`jianying-cli v1.6.19` 锁与 `jianying-skills v2.3.0` 的 24 个技能
  摘要一致。直接从该安装根、注入摘要锁定的发布 CLI bundle 运行资源、控制、工作流状态机和
  跨宿主合同测试，33/33 通过；覆盖普通资源域发现/筛选/预检、控制路由、批准、停止占用、恢复、
  证据分层和三宿主 manifest 语义一致性。
- ZCode：本机缓存最高只有 `0.22.0`，活动 data 目录没有 `v0.25.0` 安装记录。
- Kimi：正式 managed 安装仍为 `0.1.0`，不是本轮发布身份。
- `runtime/host-acceptance.json` 正确保持 `status=pending`、`hosts=[]`。Codex 包内测试不能冒充
  ZCode/Kimi 的真实安装，也不能把共享 manifest fixture 提升为三个 `real_host` observation。

因此 `6.3` 和 `7.5` 继续未勾选。完成它们需要先经用户确认把 ZCode 与 Kimi 升级到正式
`v0.25.0`，随后从三个各自安装根运行相同验收并生成带摘要的 host evidence；不得复用旧版证据。

宿主证据合同同时完成了失败关闭加固：原先只要求 fresh install、doctor、简单 Job、恢复和
原生导出授权五项，无法充分证明本变更的交互要求。现在 observation/evidence Schema 与运行时
验证器统一要求 13 项：fresh install、doctor、技能发现、单技能安装、分类发现、分类路由、
选择解释、批准、简单 Job、停止、恢复、证据展示和原生导出授权。RED 测试先暴露旧集合少 8 项；
实现后 Schema/记录器/汇总器/readiness 定向回归 13/13 通过。旧证据不会被静默提升。

## 2026-09-22：官方资源取得合同与不可变发布消费

- CLI `v1.6.19`：<https://github.com/full-aigc-plugins/jianying-draft/releases/tag/v1.6.19>
  - GitHub Immutable Release 已启用且 Release 为不可变状态。
  - macOS arm64、macOS x64、Windows x64 制品、能力清单、Schema、SBOM 和发布索引均由发布工作流生成。
- 插件 `v0.23.0`：<https://github.com/full-aigc-plugins/jianying-draft-plugin/releases/tag/v0.23.0>
  - 发布门禁运行：<https://github.com/full-aigc-plugins/jianying-draft-plugin/actions/runs/35623485065>
  - 三平台均从锁定 Release 下载 `jianying-cli v1.6.19`，完成摘要校验、无 Cargo 安装和能力握手。
  - 汇总证据验证和不可变插件 Release 发布成功。
- 本地发布包黑盒：
  - 发布布局安装与握手通过。
  - `not_downloaded` 官方音乐经 Fake GUI 触发下载、物化文件、生成资源收据，再由发布 Rust CLI 完成登记和权益预检。
- 回归：Python `68/68`；Node `274` 通过、`5` 个仅在制品/真实宿主环境启用的条件测试跳过；OpenSpec strict 校验通过。

## 保留门禁

- 本记录不证明真实剪映 GUI 已完成资源搜索、预览和下载。
- 真实剪映应用、移除、恢复、冷重开、播放和原生导出尚未完成，对应任务保持未勾选。

## 2026-09-22：生活 Vlog 五域组合计划发布二进制黑盒

- 黑盒先计算实际可执行文件 SHA-256，并与插件锁中的 macOS arm64 `v1.6.19` 摘要
  `3582b57e471b206c068bb1fb304c41dd79ef65a62317946bba69bef8852deee2`
  精确比较；随后只调用二进制 `capabilities --json`，没有读取 Rust 源码。
- 发布身份固定 source commit `81684a952ccfad9d1cff98d4c470dd500e74e57b`；
  `media.official_resource`、`media.audio` 为 `supported`，
  `media.official_resource_apply` 仍为 `partial`。
- 生活 Vlog 计划同时绑定 `media`、`music`、`sticker`、`transition`、`caption`
  五个独立查询，形成 15 个 search/filter/acquire 步骤；WorkflowPlan 严格校验通过，
  不含屏幕坐标、脚本或自由命令。
- 条件黑盒在真实发布二进制下 1/1 通过。该证据只完成组合计划与能力门禁，
  不把尚未支持的自动应用、移除和恢复冒充完成，因此任务 `3.2`、`3.4` 保持未勾选。

## 2026-09-22：Surface Inventory 与时间线控制编译

- 发布二进制事实源：锁定的 `jianying-cli v1.6.19`，通过 `runtime controls list` 与 `runtime controls surfaces` 的结构化 JSON 输出取得控制目录和 Surface Inventory；插件未读取 Rust 源码。
- Inventory 校验：50 个入口，逐区域计数为 `edit_toolbar=12`、`timeline_canvas=9`、`timeline_tabs=4`、`track_headers=9`、`view_settings_popover=4`、`view_toolbar=12`；校验精确编辑器身份、截图 SHA-256、重复语义实例和父子入口。
- 草稿协议编译：发布目录中 14 个 `draft_protocol + supported` 控件均有固定 argv 映射，包括素材加入、分割、三类修剪、复制、加轨、移动、删除、关键帧、滤镜、特效、转场和封面；禁止解析目录中的自由文本命令。
- Runtime Control：会话级控制编译时强制精确版本 Canary、稳定语义 ID 和 `state_contract`；执行验证强制读取前态、执行、读取后态，并对 set/invoke 分别检查目标值或状态变化。
- fail-closed：任何屏幕坐标字段、未知/未解析控件、不可用 Adapter、缺失 Canary、缺失状态回读或 CLI 已支持但编译器缺少固定映射均结构化失败。
- 覆盖报告：当前真实发布目录保留 5 个 `unresolved` 入口和 6 个未展开父菜单，共 11 个 gap，`can_claim_complete=false`；因此没有宣称“剪映全部按钮已覆盖”。
- 后续 CLI source candidate 已把展开状态升级为显式合同：7 个父入口、0 个完整枚举；更多设置的
  4 个截图子项保持 `partial`，其余保持 `pending_accessibility`。插件兼容旧发布清单，但新合同
  存在时不再按命名猜测完成状态；缺少可访问性名称的父入口始终输出 `unexpanded_parent`。
- 自动验证：
  - `tests/native_control_orchestration.test.mjs`：7/7 通过，覆盖 14 个直达控件、会话前后态、坐标拒绝、缺口报告和 WorkflowPlan 绑定。
  - `tests/real_cli_bundle_install.test.mjs`：3/3 通过；从真实 `v1.6.19` 发布布局完成无 Cargo 安装、资源取得闭环和 Surface Inventory 黑盒编译。

### 仍未解除的边界

- Runtime Control 的状态回读由可注入 Adapter 完成了确定性测试，但真实剪映 GUI 精确版本 Canary 尚未执行；这属于任务 `6.2`，不由本轮单元证据替代。
- 5 个未知入口和 6 个未展开菜单必须继续枚举；coverage 报告会持续阻止完整覆盖声明。

### 不可变插件发布

- 插件 `v0.24.0`：<https://github.com/full-aigc-plugins/jianying-draft-plugin/releases/tag/v0.24.0>，GitHub 返回 `isImmutable=true`。
- 发布门禁：<https://github.com/full-aigc-plugins/jianying-draft-plugin/actions/runs/35627300411>，contract、Windows x64、macOS x64、macOS arm64、聚合 evidence 和 publish 全部成功。
- 三个平台均从锁定的 `jianying-cli v1.6.19` Release 下载、校验并完成无 Cargo 安装及能力握手。
- Release 含源码包、归档审计、聚合证据、三平台 canary 和 readiness 共 7 个带 SHA-256 摘要的资产。

## 2026-09-22：普通资源目录、逐域预检与版型矩阵

- 十域只读目录：`media/music/text/sticker/effect/transition/caption/filter/adjustment/template` 均进入
  `jianying-native-resource-catalog/v1`；快照绑定编辑器与 Adapter 身份，隐藏/未知域不伪装可用，候选中不持久化本地路径或账号秘密。
- `jianying-native-resource-use-preflight/v1` 已实现：转场相邻片段与切点、音乐用途/渠道/范围、效果范围与受保护片段、模板画幅、限免有效期及资源身份均在 Job 编译前校验。
- 真实 `jianying-cli v1.6.19` 发布布局黑盒 `4/4`：无 Cargo 安装、未下载资源取得、基础版/专业版/限免过期/用途冲突矩阵，以及 Surface Inventory 控件编译全部通过。基础版与专业版进入 Rust CLI register/preflight；限免过期与用途冲突在下载和 CLI 调用前被拒绝。
- 全量回归：Node `284` 通过、`7` 个仅在制品/真实宿主条件下启用的测试跳过；Python `68/68`；分发校验与 OpenSpec strict 通过。
- 任务 `3.2` 和 `3.4` 仍未完成：真实预览/应用 Adapter、应用前快照、草稿差分、局部移除与恢复不能由 Fake GUI 目录证据替代。

## 2026-09-22：智能包装与智能 B-Roll 子计划

- `jianying-smart-package-request/v1` 冻结六类风格映射、输入素材、允许轨道、受保护对白/品牌声明/镜头、预算、最大时长、预览与人工批准边界。
- WorkflowPlan 编译为 preview、human review、apply、independent verify 四步；apply 要求 `runtime.smart_package`、人工批准、单次尝试和 `inspect_before_retry`。
- `jianying-smart-package-proposal/v1` 将结果拆为 B-Roll、字幕、花字、音效、特效和转场变更；未解释变更或超预算提案不能申请执行。
- 故障注入验证：删除受保护对白、修改品牌声明、时间范围越界和 apply 结果不明确均触发快照恢复，且要求恢复回读为 `restored`。
- 请求现在显式区分智能包装、智能 B-Roll、智能粗剪和文案粗剪，并固化
  `plan -> preview -> approve -> apply -> verify` 生命周期。成功证据输出五阶段状态轨迹；
  不明确 apply 和独立验证失败输出带 `recover=restored` 的恢复轨迹。为保持冻结 WorkflowPlan
  兼容，请求构建承担 plan 阶段，human review 的强类型输出承担 approve 阶段，四步 DAG 不改名；
  成功状态轨迹与请求、批准、快照、预览、应用和检查结果一起进入 evidence SHA-256。
- 聚焦测试 `5/5`；全量 Node `289` 通过、`7` 条条件测试跳过；Python `68/68`；分发校验、OpenSpec strict 和差异检查通过。
- 真实剪映智能包装预览/批准/应用/冷重开仍属于任务 `4.5`，保持未勾选。

## 2026-09-22：数字人安全合同与远程恢复

- 已定义库存目录、请求、预览计划、远程任务、产物和独立证据 Schema；请求绑定形象、声音、脚本摘要、背景、类别、权益、用途、渠道、费用和 Provider。
- 库存搜索分别保留形象/声音的接受与拒绝理由，并按类别、语言、声音风格、版型、用途和预算选择；预览计划明确禁止提交。
- 自定义真人素材必须同时具备精确素材范围的肖像权或声音权批准，以及绑定目标 Provider 和用途的上传批准；专业版权益不能替代授权。
- 稳定请求 ID 作为 Provider 幂等键。账本已有远程任务时只恢复；提交或状态不明确时持久化 ambiguous 并拒绝重提。估算与实际费用均受批准上限约束。
- 完成任务仍需验证本地产物文件类型、长度和 SHA-256 后才生成证据；供应商成功提示不单独满足完成门禁。
- 聚焦测试 `6/6`；全量 Node `295` 通过、`7` 条条件测试跳过；Python `68/68`；分发校验、OpenSpec strict 和差异检查通过。
- 真实获准数字人 Provider/剪映 Canary 涉及上传和费用，属于任务 `5.5`，本轮没有触发且保持未勾选。

## 2026-09-22：三类执行测试矩阵

定向运行普通资源、智能包装与数字人三类执行测试，结果 24/24 通过、0 跳过：

- 普通资源：严格 Schema、十域目录、组合筛选、逐域预检、发布 CLI 取得链、
  下载失败、许可/用途/期限负例，以及五域 Vlog 计划黑盒。
- 智能包装：六风格路由、请求/提案/证据 Schema、WorkflowPlan 子图、批准和预算，
  受保护对白/品牌/范围漂移与模糊 apply 均恢复应用前快照。
- 数字人：库存筛选、请求/预览/产物/证据 Schema、WorkflowPlan 子图，
  肖像/声音/上传批准、稳定 request-id、费用上限、模糊提交/状态与禁止静默重提。

该矩阵完成任务 `6.1` 的插件级 Schema、单元、E2E、故障注入与安全门禁；
真实付费 Provider、真实剪映 GUI 和正式三宿主仍分别由 `5.5`、`6.2`、`6.3` 验收。

## 2026-09-22：资源应用、检查、局部移除与恢复合同

- 新增 `jianying-native-resource-application/v1` 与 `jianying-native-resource-removal/v1` 严格 Schema。
- 应用链强制执行预览、应用前快照、应用、独立草稿资源/时间线回读；模糊应用或回读漂移都会恢复快照，不得报告成功。
- 移除链只接受摘要一致的已验证应用证据；移除后必须读回 `absent`，模糊移除或资源仍存在时恢复移除前快照。
- Adapter 身份和所有持久化输入/输出都递归拒绝 Token、Cookie、密码、凭据与 Authorization 字段；CLI 交接保存取得摘要、收据摘要、登记状态和预检状态，不保存账号秘密。
- WorkflowPlan 现在把已取得的 `ResourceReceipt` 编译为需要精确人工批准和 `media.official_resource_apply` 的 `native_resource_apply`，再把其 `NativeActionEvidence` 交给独立 `native_resource_inspect`；绕过取得或检查依赖会被图校验拒绝。
- TDD 证据：缺少 `attachNativeResourceApplicationWorkflow` 导出时定向测试失败；实现后 `tests/native_resource_application.test.mjs` 4/4 通过。
- 完整回归：Node 309 项中 302 通过、7 项真实制品/宿主条件测试跳过、0 失败；Python 70/70；分发校验与三个相关 OpenSpec strict 校验通过。

该实现完成了任务 `3.2`、`3.4` 的插件侧可注入 Adapter、CLI 收据交接、失败恢复和计划编排合同。真实运行仍受发布 capability 门禁：锁定 CLI `v1.6.19` 的 `media.official_resource_apply` 为 `partial`，且尚未用真实剪映 Adapter 对应用/局部移除/恢复做版本绑定 Canary；这些生产证据继续由任务 `6.2` 阻止默认启用，不能由 Fake Adapter 或 Schema 证据替代。

## 2026-09-22：版型观察与 Harness 路由

- 新增严格 `jianying-native-edition-observation/v1`：应用显示名、登录状态、账号版型、权益状态、能力集合、观察时间和可选失效时间彼此独立并绑定 SHA-256。
- 只读 Adapter 即使观察到“剪映专业版”显示名，也不会把未知账号提升为专业版；资源目录始终使用现场观察而不是旧目录声明。
- 新增 Harness `native-resource-route QUERY.json EDITION_OBSERVATION.json`：基础账号会把 `any` 收紧为 `basic`；显式专业请求、未登录、未知/过期权益或能力缺失均结构化暂停，不静默替换素材。
- 候选、目录证据、Adapter 身份、取得证据和最终持久化结果递归拒绝 Token、Cookie、密码、凭据、Authorization 与 API Key 字段。
- TDD 先观察到缺少版型 API、缺少 Harness 命令和聚合目录 Schema 可注入字段，再逐项转绿；定向资源套件 15/15（另 1 条发布二进制条件测试在全量运行中执行）。
- 完成门禁：Node 312 项中 305 通过、7 条真实制品/宿主条件测试跳过、0 失败；锁定 `v1.6.19` 真 bundle 4/4；Python 70/70；分发校验、三个相关 OpenSpec strict 与 `git diff --check` 通过。

后续扩展将取得身份分为 `downloaded_file` 与 `draft_resource`：文件型音乐继续绑定文件摘要；内嵌画面特效要求草稿节点唯一并绑定节点/草稿双摘要，使用发布 CLI 的 `--draft` 登记和预检。真实 bundle 测试现为 5/5，并在版型矩阵内部覆盖基础、专业、限免过期、用途冲突、未知版型、仅预览、下载失败与真实过期权益。

## 2026-09-22：真实剪映 13 分类与控制台逐项操作审计

在笔记本内置屏幕使用剪映专业版 `11.5.13243`（`11.6.0-beta2`）完成 13 分类入口、
搜索/筛选/下载/预览、多个本地落轨/撤销操作、轨道状态、片段分割/撤销、片段右键菜单、
真实关闭后冷重开、13 秒连续播放和本地原生导出。新导出 MOV 经独立 `ffprobe` 复核为
H.264 + AAC、1080x1920、30fps、13.000 秒，SHA-256 为
`1febdad07d2e82a44fe74b0ce7c6825b4b3d1d3b9812d859278e083c2c9c0608`。

完整矩阵见 `docs/video-harness/JIANYING_GUI_OPERATION_ACCEPTANCE_20260922.md`。本轮同时确认三个
生产缺口：普通官方素材/贴纸/滤镜的卡片“＋”与拖拽没有形成可验证轨道；智能包装与数字人下一步
涉及上传或扣点而未获精确范围批准；页签/选择/联动/预览轴/更多设置/轨道右键尚未递归枚举完成。
因此 `4.5`、`5.5`、`6.2`、`6.3`、`6.5`、`7.5` 全部保持未勾选，不能把本次真实导出误报为
“全部原生能力已通过”。

## 2026-09-22：真实剪映主页功能审计

补验主页快捷创作、侧栏云空间、本地草稿管理、订阅/团队、帮助/消息、全局设置、网络检测、
版本和第三方版权。真实操作通过网格/列表切换、排序切换与恢复、云草稿刷新、空文件夹创建、
最近删除查看和网络检测；AI 文字成片、营销成片、AI 切片、视频翻译与智能裁剪均到达配置或
上传门禁，未提交生成、上传、邀请、开票、账号变更或费用动作。

完整矩阵见 `docs/video-harness/JIANYING_HOME_OPERATION_ACCEPTANCE_20260922.md`。版本检查还暴露
宿主漂移：当前进程为 `11.6.0-beta2`，检查更新后自动下载 `11.6.0 内测版 3`，本轮停在重启安装
之前。图片设计、创作脚本、小云雀和模板 GPU 页面仍缺稳定工作台证据；新建的空文件夹需要
删除确认才能恢复。因此真实宿主任务继续保持未完成，不用主页入口存在替代端到端能力证据。

## 2026-09-22：首页本地文件夹 Harness 路由

新增 `jianying-home-folder-operation/v1` 严格请求合同与 Harness
`home-folder-plan` / `home-folder-execute`。计划只生成固定
`home folder list/create/recycle/list-recycled/restore` argv，明确声明
`home.folder_lifecycle` capability，且 `fallback=null`；坐标、未知字段和任意 argv
注入均在编译时被拒绝。

- create/recycle/restore 要求 `approved=true`，未批准时不进行 CLI handshake 或任何写入。
- 执行只通过校验过的 Runtime Adapter；发布 capability 为 `partial` 时返回
  `missing_capability`，状态 fixture 逐字节不变，不转向 GUI、Python 或外部 fork。
- 写入响应必须包含快照路径；随后重新调用 list/list-recycled，同时证明目标 ID
  在预期列表中唯一存在，并从反向列表消失。
- 故障注入中 CLI 声称 recycle 成功但回收站回读缺失；Harness 返回
  `home_folder_verification_failed`、保留 `/snapshot/recycle`，且不自动重试。
- 定向 TDD 5/5 通过；全量 Node 328 项中 319 通过、9 条真实制品/宿主条件测试跳过、
  0 失败；分发校验和 OpenSpec strict 通过。

这些证据完成任务 `2.10`，但不提升真实宿主任务：当前插件锁定的不可变 CLI
发布仍未把 `home.folder_lifecycle` 标记为 `supported`，因此默认执行保持 fail closed。

## 2026-09-23：首页文件夹发布二进制消费闭环

- `jianying-cli v1.6.24` 已发布为 GitHub Immutable Release，绑定 source commit
  `4ef331110422a7f3de60cb8637af89b84d848602`；发布工作流 `35748614167` 的来源一致性、
  macOS arm64、macOS x64、Windows x64、SBOM、发布和 Release attestation 全部通过。
- 正式导入器从 `jianying-cli-release-index.json` 原子更新插件锁；三平台归档、二进制、
  capability manifest 和 SBOM 摘要均进入 `runtime/jianying-cli.lock.json`，宿主验收按合同
  重置为 `pending`，没有复用旧版本证据。
- 全新临时安装目录在受限 PATH 下下载并安装 macOS arm64 发布资产，运行源为
  `installed_fallback`，`cargoAvailableInHandshakePath=false`；二进制握手、包内 capability
  manifest、source commit、Release ref 和 `jianying-skills v2.3.0` 最低能力合同全部一致。
- 插件 Harness 仅通过 `home-folder-execute` 调用该发布二进制，对真实剪映
  `LocalDraftFolder` 执行只读 list；结果精确回读 1 个活动文件夹，执行前后配置目录聚合
  SHA-256 均为 `fb8e9f582c2aa465d000b5c8508168349fa23c0531e51bd052de4e4d94651cbd`。
  本次没有使用 GUI、屏幕坐标、图像识别、Python 引擎、外部 fork 或 Rust 源码。
- `home.folder_lifecycle` 已由真实发布 manifest 标记为 `supported`。写路径的
  recycle/restore 已在 CLI 发布前使用同一发布二进制完成真实剪映停止写入、冷重开和精确 ID
  回读；插件层仍强制 `approved=true`、恢复快照和写后双向回读。

这组证据刷新了任务 `6.4` 的不可变发布消费证明，并解除 `2.10` 末尾记录的发布 capability
阻塞；它不替代真实普通资源、智能包装、数字人、Windows GUI 或三宿主验收，因此
`4.5`、`5.5`、`6.2`、`6.3`、`6.5` 和 `7.5` 继续保持未勾选。

## 2026-09-23：`v0.26.1` 三宿主十三项正式门禁

- Codex `0.153.4` 从 `partme-ai/full-aigc-plugins` 正式市场安装
  `jianying-draft v0.26.1`；ZCode `0.16.9` 从同一市场和精确 `v0.26.1` tag 安装；Kimi
  `0.43.1` 通过官方本机插件 API 导入 GitHub Immutable Release 源码制品，制品 SHA-256 为
  `738c90489e5c9a1ea2a153b0eeff5a191abd8580c47de6248f5ce8c39554a5d8`。
- 三个安装根均只绑定发布 `jianying-cli v1.6.24` 二进制，二进制 SHA-256 为
  `4fbc5790c6c60b76d5489ed44825e2ffef42e6572be25fc20394e1f5f244e0b0`，并锁定
  `jianying-skills v2.3.0` 的 24 个目录摘要。
- 每个宿主分别执行 fresh install、doctor、技能发现、单技能解析、13 分类发现、106 条动作路由、
  VG01 选择解释、目标绑定批准、简单 Job、停止、冲突恢复、证据展示和原生导出目标级授权；
  每项均写入带时间戳和 canonical SHA-256 的 `checkEvidence`，未执行真实原生导出副作用。
- 三宿主使用同一 `jianying-job/v2` 输入，输入摘要均为
  `0d6e504997e2e4d5e61bb29d81a0f8234ca5547fb2301b5e6fdc25d6d8e4703b`；规范化结果摘要均为
  `328eb56f8716ad9e22deee15fa5ef84c6d2753e42bc505bf1391ca1bfcb27349`。
- `runtime/host-acceptance.json` 已由记录器和汇总器原子提升为 `passed`；readiness 返回
  `ready=true`、`production_ready=true`，分发校验和 OpenSpec strict 均通过。

这些证据完成任务 `6.3` 与 `7.5`。它们不替代普通资源、智能包装和数字人的真实剪映端到端验收，
因此 `4.5`、`5.5`、`6.2` 与 `6.5` 仍保持未勾选。

## 2026-09-23：不可变 Release 证明读取令牌修复

- 插件 `v0.26.0` 的合同、三平台无 Cargo fresh-install、证据聚合和不可变 Release 创建均成功；
  Release attestation 随后生成，7 个资产摘要与发布身份也可由仓库配置的只读令牌验证。
- 发布任务暴露了令牌边界错误：写入使用的短期 `github.token` 被继续用于
  `gh release verify` / `verify-asset`，在工作流内只能得到 `no attestations`，即使同一时刻
  `RELEASE_RULESET_READ_TOKEN` 已能读取完整证明。
- `v0.26.1` 候选保持发布写入令牌不变，仅让不可变证明读取显式使用
  `RELEASE_RULESET_READ_TOKEN`；新增分发回归断言，防止以后再次退回短期令牌。
- `v0.26.0` 保持不可变且不改写。只有 `v0.26.1` 的 tag workflow、Release attestation、
  全资产 `verify-asset` 和市场同步都通过后，才把本次发布门禁判定为完成。
