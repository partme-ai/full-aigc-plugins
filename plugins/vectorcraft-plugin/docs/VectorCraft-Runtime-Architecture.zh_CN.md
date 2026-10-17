# VectorCraft Runtime Architecture

> **文档说明**：进程、数据、协议、故障恢复及验收的完整目标设计。
>
> **版本**：1.0.0
> **最后更新**：2026-10-09
> **状态**：目标设计与有界实现并存；当前源码和固定验收范围以 OpenSpec 任务及绑定版本的证据为准。

关联文档：[品牌边界](../product-docs/VectorCraft/1%E3%80%81VectorCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](../product-docs/VectorCraft/5%E3%80%81VectorCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](VectorCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../openspec/changes/establish-v1-plugin/proposal.md) · [证据](evidence/runtime-baseline.json)

## 1. 定位与证据边界

VectorCraft 负责可编辑矢量品牌资产与多画板设计。当前仓库已有 `src/` Harness 实现、13 项固定技能源副本及有界运行证据；完整宿主路由、全命令与权限秘密验收仍开放。下文描述目标体系，不能把已存在的模块或局部测试等同于完整交付。

### Agent Plugin 发行目录与开发仓

Agent Plugins 1.0 宿主从根 `plugin.json`、`skills/` 及可选 `mcp.json` 发现可移植组件。当前发行目录只抽取 `plugin.json`、13 项锁定技能和 `LICENSE`；`src/`、`scripts/`、`tests/`、`docs/`、`openspec/` 留在开发仓，不会仅因文件存在而被规范宿主加载。命令与钩子须依具体宿主的扩展协议提供，不能宣称为跨宿主能力。若未来将 Harness 作为插件可调用服务，必须提供并验证真实 MCP 或宿主扩展入口；静态包检查不能替代该运行验收。

## 2. 驱动与非目标

必须保留原生可编辑工程、独立技能分发、可恢复执行和可证实交付。V1 使用本地工作区；不建设 SaaS、多租户、账户计费、Web 管理台或新的桌面编辑器。不承诺自动跨软件无损动态链接。

## 3. 组件与依赖方向

```mermaid
flowchart TB
    H[Host and user intent] --> S[Versioned Skills]
    S --> P[Planner and schema validation]
    P --> K[Harness and authorization scope]
    K --> L[(Task ledger and artifact index)]
    K --> A[Runtime Adapter]
    A --> C[Verified CLI or child plugin]
    C --> O[Native project and rendered outputs]
    O --> V[Evidence collector and reviewer]
    V --> L
    V --> H
```

| 组件 | 权威数据 | 禁止承担 |
| :--- | :--- | :--- |
| Skills | 操作知识、触发条件、领域方法 | 任务状态和秘密 |
| Domain Harness | 领域计划、工程修订、子任务账本 | 其他插件内部状态 |
| Runtime Adapter | 命令映射与能力快照 | 自行改变创作目标 |
| Native CLI | 原生对象、编辑与渲染 | 跨插件项目真相 |
| ArtCraft | Brief、DAG、资产版本与聚合交付 | 伪造子任务成功 |


## 4. 仓库与模块边界

| 规划模块 | 责任 | 输入与输出 |
| :--- | :--- | :--- |
| src/planning/ | 规范化目标与编辑计划 | Brief → DomainPlan |
| scripts/harness/ | 状态机、授权、预算、恢复 | DomainPlan → TaskReceipt |
| src/adapters/ | 上游命令与结果映射 | TaskRequest → native command |
| src/artifacts/ | 登记哈希、引用与交付 | files → ArtifactManifest |
| src/evaluation/ | 技术检查与创作问题 | artifacts → QualityVerdict |
| skills/ | 构建时锁定同步的技能 | skills.lock.json → packaged knowledge |
| runtime/ | 发行锁文件与兼容矩阵 | artifact metadata → verified executable |

以上路径为拟建模块，不代表源码已存在。

## 5. 原生领域边界

| 能力 | 行为边界 | 状态 |
| :--- | :--- | :--- |
| 路径形状与坐标 | 定义画板坐标、单位、路径控制点、闭合性与描边；不可把预览像素当成路径事实。 | 计划中 |
| 组合与布尔操作 | 记录参与对象 ID、布尔运算与结果对象身份，保留修改前检查点；操作失败不丢失原对象。 | 计划中 |
| 品牌色与文字 | 以显式 token 绑定品牌色而非全文件颜色替换；保留文本内容与字体依赖，轮廓化输出记录可编辑性损失。 | 计划中 |
| 画板与变体 | 每个画板有稳定 ID、名称、尺寸和输出映射；预览顺序与导出范围明确，避免索引基准混淆。 | 计划中 |
| 交换格式能力范围 | 原生 .vectorcraft 与 SVG、PDF、PNG 分别验证；遇到不可交换效果时报告栅格化范围并保留原工程。 | 计划中 |
| 品牌变体更新 | 根据 token 与素材依赖更新相关变体，核对无关对象属性与输出没有变化。 | 计划中 |


领域对象：`VectorDesignPlan`, `Document`, `PathObject`, `Artboard`, `BrandToken`.

## 6. 进程、会话与并发

宿主加载知识并调用插件入口；Harness 在本地进程中运行，通过 stdio MCP 子进程或已验证 CLI argv 调用上游。需要连续编辑时维持同一原生会话；一次 CLI 命令结束不意味着下一命令拥有相同内存状态。每个工程持有独占写入租约与 epoch；读操作只读取稳定快照。用户 GUI 修改通过 expectedRevision 校验发现。ArtCraft 只并行调度没有共同写入资源的节点。

## 7. 成功路径与副作用边界

```mermaid
sequenceDiagram
    participant U as Host
    participant H as Harness
    participant J as Ledger
    participant R as Runtime
    participant V as Verifier
    U->>H: plan + authorization scope
    H->>H: validate hashes, revision, capabilities
    H->>J: persist intent and idempotency key
    H->>R: execute bounded operation
    alt result returned
        R-->>H: task identity and outputs
        H->>V: verify actual files and project
        V-->>H: evidence-bound verdict
        H->>J: persist receipt and next state
        H-->>U: reviewable delivery
    else outcome unknown
        H->>J: reconciling, retain ownership
        H->>R: query original task or inspect output
        R-->>H: existing result or confirmed not executed
    end
```

## 8. 状态机与合法转换

```mermaid
stateDiagram-v2
    [*] --> planned
    planned --> blocked: missing prerequisites
    blocked --> ready: prerequisites resolved
    planned --> ready: inputs and authority valid
    ready --> running: persist intent and acquire lease
    running --> verifying: execution result available
    running --> reconciling: outcome unknown
    reconciling --> verifying: artifact recovered
    reconciling --> ready: confirmed not executed
    running --> cancel_requested
    cancel_requested --> cancelled: stop confirmed
    verifying --> review_ready: technical gates pass
    verifying --> failed: required gate fails
    review_ready --> completed: accepted current evidence
    review_ready --> planned: new revision
```
取消后迟到结果可登记为孤立产物，不得恢复已取消任务为完成。未知结果不通过释放租约假装失败；人工核对也需留下证据。

## 9. 持久化、恢复与记忆

目标采用 SQLite 事务记录任务、事件、资产索引与授权引用；大文件存于内容哈希目录。副作用意图提交后才能启动进程；文件先写暂存，核验后原子更名，再登记可消费产物。崩溃后的孤立文件通过 reconcile 登记或隔离。不能宣称 SQLite 与原生应用具有分布式原子事务。会话摘要只辅助规划；工程状态、任务账本和验收记录分别是权威来源。长期用户偏好仅按授权保存，不把推断写成项目事实。

## 10. 接口与公共契约

插件适配接口为 capabilities、validate、estimate、submit、status、cancel、reconcile、collect、verify。它们是拟建公共接口，不是上游 CLI 同名命令。ArtCraft 的 OpenSpec 拥有 craft-task/v1 与 craft-artifact/v1；领域插件只定义命令映射与领域 payload。交付前应将跨仓引用固定到经过联调的提交。

| Field | 语义 |
| :--- | :--- |
| idempotencyKey | 同输入返回原任务；不同输入冲突 |
| expectedRevision | 保护用户或其他运行造成的修改 |
| authorizationRef | 引用已有授权范围；不要求每次重新确认 |
| inputRefs | 包含资产版本与摘要，不只有路径 |
| runtimeIdentity | 绑定运行时版本、摘要、模式和能力快照 |
| deadline / budget | 父子任务共享上限，不重复计账 |


## 11. 错误语义

| Code | 何时出现 | 恢复动作 |
| :--- | :--- | :--- |
| runtime_missing | 没有兼容运行时 | 执行显式 setup；不自动编译来源不明代码 |
| capability_missing | 命令、参数或模式未支持 | 修订计划或固定受支持版本 |
| revision_conflict | 工程已被修改 | 重新检查与规划，不覆盖 |
| outcome_unknown | 副作用结果未知 | reconcile |
| artifact_invalid | 产物哈希、解码或工程检查失败 | 保留失败证据，局部返工 |
| budget_exhausted | 达到成本或修订上限 | 停止新增工作并交付状态 |


## 12. 配置、权限与输入信任

配置优先级：已授权任务参数 → 项目配置 → 用户配置 → 默认值；秘密只传引用。显式 CLI 路径仍需校验身份。V1 默认本地文件，读写根目录独立，解析真实路径后拒绝越界、符号链接逃逸和覆盖非目标文件。执行 argv 数组而非拼接 shell。素材名、图层文字、上游返回与参考文档都是数据，不能修改执行策略。专业编辑默认不上传素材，云端调用由适配器检查授权范围与预算。

## 13. 质量与评估

技术评估器执行确定性检查：结构、哈希、尺寸、时长、音轨、alpha 与工程重开。创作评估器读取固定参考与产物，只产生带位置的缺陷建议，无权直接编辑或把任务标为完成。Planner/Executor/Evaluator 为逻辑职责，可在单宿主内实现，不强制多 Agent 运行。人工接受绑定当前证据摘要。固定离线 fixture 覆盖成功、缺失依赖、损坏输出、旧版本证据与对抗元数据；审美评价记录模型、提示词与量表版本，不能用单次评分证明稳定。

## 14. 资源与性能目标

以下是待测目标：每工程最大并发写入数 1；每项目默认同时渲染 1 个节点；创作修订默认最多 3 轮。metadata 请求截止时间 10 秒，渲染截止时间按计划显式设置，超时不等于失败。渲染速度、内存和磁盘需求必须按尺寸、时长、效果与硬件测量；本阶段没有吞吐或实时性能承诺。磁盘预算覆盖输入、源工程、检查点、输出与最大临时峰值；空间不足时在副作用前阻止新任务。

## 15. 安装、升级与回退

用户级版本目录保存 CLI、许可、摘要与回执，插件缓存只保存只读包。优先使用官方制品，安装前检查平台与摘要，在暂存目录验证后原子激活。升级时等待活动会话排空，保留旧版本，启动探测通过才切换；状态 schema 迁移需备份与回退兼容性检查。独立技能也能通过公开安装入口发现运行时。禁止在每次普通任务中重新下载、升级或编译 CLI。

## 16. 可观测性与运维

日志以 projectId、taskId、attemptId、runtimeIdentity、planHash、artifactHash 关联，记录状态变更、队列等待、执行时长、重试和验收门禁；不记录凭据或完整隐私素材。doctor 区分安装、版本、能力、宿主、原生交付五个层面。备份先停止写入并保存账本一致性快照，同时记录资产清单；恢复后重算哈希并核对未终结任务。清理只处理已确认无引用的缓存，工程、证据与用户素材保留。

## 17. 兼容、验收与演进

已观察：macOS arm64 上四款官方 CLI 0.2.0 能启动并完成基础 MCP 调用。未验证：完整创作流程、宿主插件安装、桌面桥接、macOS x64、Windows、Linux。兼容矩阵每行对应版本、平台、模式和真实用例证据。V1 先验收本地原生链路，后增加跨插件与生成服务。

制作 Logo 与图标资产，交付 .vectorcraft、SVG 和 PNG；修改品牌色后更新所有绑定的变体，并保留无关颜色。

## 18. 与 ArtCraft 的交接

专业插件可独立使用，无需启动 ArtCraft。被 ArtCraft 调用时沿用同一领域执行路径，传入父任务身份、输入版本与预算；产物收集后只返回公开回执。重试责任由子执行器负责，父级负责查询与依赖协调。交接成功需核对输入引用、输出摘要、损失报告和原生工程，而不是只看 exit code。

## 19. 风险与决策反转条件

| 风险 | 发现方式 | 处理与责任人 |
| :--- | :--- | :--- |
| R1 | 上游命令或格式变化 | Runtime owner：固定版本，比较 schema，重跑 fixture；未通过保持旧版 |
| R2 | 文字、透明或颜色交接损失 | Domain owner：保存源工程，生成 loss report，使用像素与对象检查 |
| R3 | 断线导致重复提交 | Harness owner：持久化意图与幂等键，先 reconcile，再决定重试 |
| R4 | 文档被误读为已实现 | Release owner：功能状态为 planned；无技能和运行时入口不得进市场 |
| R5 | ArtCraft 商标和受限许可代码边界 | Maintainer：独立实现；不复制上游 ArtCraft/Services 代码；品牌授权在发行前核对 |


如果真实并行或跨机器需求超过本地账本能力，再通过新 OpenSpec 变更评估服务化；如果上游命令长期缺失，则缩减明确能力范围或新增受验收的适配，不悄悄改写原生交付要求。

---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。

当前实现：原生交付包含 exchange-loss.json，公开工作流保留原生源与重开检查摘要，记录格式损失、SVG/PSD 实际结构观察及未知字体/效果保真。报告进入 manifest.files，由 ArtCraft 接管与打包时重新核验；完整交换保真验收仍待完成。

## 当前宿主验收

快照 `0.1.0-dev.2` 已有安装、发现及安装后公开入口的限定范围证据。参见[验证合同与未验证范围](VectorCraft-Host-Verification-Architecture.zh_CN.md)。完整发布任务仍保持未完成，目标设计段落不作为实现证明。

## CLI 技能体系增量

[VectorCraft CLI / setup / task suite](VectorCraft-Skill-Suite-Architecture.zh_CN.md)


## 默认首用能力门禁实现增量

Controller新任务现已先进行固定技能计划验证、可信版本目录安装与只读schema探测，再初始化同账本选择并登记编辑意图。固定技能命令签名及插件固定MCP工具schema共同约束运行时；已有不同选择不被隐式升级。同版本并发首用允许复用选择，选择竞争由SQLite事务及登记时摘要／模式校验拒绝。原任务读取不重放探测或编辑，旧ready记录无能力指纹时需恢复核验。见[入口与候选证据](Runtime-Gate.zh-CN.md)；2.6不同版本及desktop／迁移仍开放。

插件42补充schema3迁移前只读备份与明确模式绑定；实际旧阅读器拒绝新schema。当前跨版本原生局部证据与完整2.6验收边界见[运行时门禁](Runtime-Gate.zh-CN.md)。技能源仍固定dev.37。

插件43的数据库插入触发器使升级前已打开的旧连接也必须遵守模式／摘要／状态策略，失败事务不消耗新预算。当前候选包含真实登记bridge排空及双进程激活竞争，见[运行门禁](Runtime-Gate.zh-CN.md)。

当前状态（公开插件43／固定源37）：任务2.6全部7个运行时场景完成，证据见[运行门禁](Runtime-Gate.zh-CN.md)；上文候选／开放描述保留为原阶段记录，不作为当前完成判断。其他33项任务、完整V1及创意GUI／模型门禁仍开放。

公开回执入口重启时只恢复已持久化技术检查的只读授权。解码器、启动器和交换损失依赖使用摘要绑定的只读执行副本；创作回执不能覆盖技术失败，也不提升原生重开状态。公开插件61／源43实际安装于Codex0.153.4 macOS arm64，通过VC-QA-001当前三个场景与19项真实原生边界。三输出解码通过；QA注入满分回执不能覆盖损坏PNG／PDF／SVG，真实缺少解码器保持NOT_RUN。文件／检查器漂移、预算先于只读副本、超时停止及协调器SIGKILL重启不重放均通过；13技能摘要保持。12项证据测试含11项重签后缺失／篡改拒绝通过。6.3关闭；116/127完成，11项开放。真实创作判断、GUI、其他平台、6.6及完整V1分别未验。 [Evidence](evidence/vectorcraft-quality-fixed61-20261009.json).

插件62修复评审到达时预算已耗尽的状态：持久停止并保留最佳可验证候选；无法再次支付封存时，核验身份和只读权限后复用已付费的技术检查副本。已复现公开61真实原生缺口，候选62以相同四次共享尝试保留更高分原生修订；122项Node通过，含三项新增回归。评分明确为QA注入；任务6.6完整验收仍开放，116/127完成、11项开放。 [Evidence](evidence/vectorcraft-revision-budget-candidate62-20261009.json).

## 发布者证据门禁

VC-RL-001两场景完成：发布者只读门禁分别核验插件结构、独立技能源、运行时、宿主加载、真实任务和原生交付。12项门禁测试先因缺少目标行为失败，最小实现后通过；另4项证据校验通过。实际隔离包中文档与OpenSpec均通过时，仅文档证明仍被门禁拒绝；原有有界记录保持原范围。复用未变化的公开63／源43实际安装、6次原生修订与独占桌面证据，并重新校验当前摘要，本轮没有新增原生或模型运行。7.1–7.3完成，120/127完成、7项开放；marketplaceEligible仍false，supportedPluginHosts仍空。权限与秘密、全命令、模型路由、完整分发和真实创作仍待独立验收。 [Evidence](evidence/vectorcraft-release-gate-20261009.json).

`python3 -I -B scripts/release_gate.py --require development`

`python3 -I -B scripts/release_gate.py --require marketplace`

```mermaid
flowchart LR
 B[Fixed release evidence bundle] --> S[Structure and skill source]
 B --> R[Runtime and host load]
 B --> N[Real task and native delivery]
 S --> G[Readonly release gate]
 R --> G
 N --> G
 G --> D[Scoped development evidence]
 G --> M[Full task and host approval gates]
 M --> P[Marketplace approval remains blocked]
```

权限与秘密边界正在实施：本地候选已限制七类子进程入口的环境继承、禁止向错误输出转发原始子进程诊断、拒绝素材附加指令字段及明确命名的字面凭据；失败评审回执也不得将此类凭据写入审计表。8项定向测试和132项Node回归通过，146项Python测试通过；实际原生修订及后续技术检查消耗4次共享预算，相关进程组停止。本候选尚未公开固定分发或完成宿主秘密引用合同，7.4–7.6继续开放，当前仍120/127完成、7项开放。原发布63／源43不变；旧发布证据不得为改动后的工作树放行。该校验不声称识别任意正文中的秘密。 [Evidence](evidence/vectorcraft-permissions-candidate-20261009.json).

候选64已锁定公开技能源44（e5f8e1bb8528），旧63／源43保持不可变。源44的183项回归通过、30项跳过、6项目标测试及13项真实独立冷安装通过；候选插件132项Node与146项Python回归通过，实际原生修订和后续技术检查消耗4次共享预算并停止相关进程组。源44主分支和标签CI通过；插件64仍未公开固定分发，宿主秘密引用、完整权限入口审计与VC-RL-002全部场景尚待完成，7.4–7.6继续开放，总体120/127完成、7项开放。 [Evidence](evidence/vectorcraft-permissions-integration-candidate64-20261009.json).

候选插件64现锁定公开源45（a4b1e624818f）。源45的28项权限测试、193项回归（48跳过）、13项真实独立冷安装及原生修订／三导出／独立重开通过，包含真实GUI保存重开和绕过Python预检后的内核拒绝。当前插件132项Node／146项Python回归及原生修订检查通过，4次共享预算内停止所有拥有的进程组。旧源44快照与执行记录按原始字节归档。Python素材预检授权、实际宿主秘密引用与固定插件64权限验收仍开放；120/127完成、7项开放，候选64未发布，V1及市场资格未获得。 [Evidence](evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json).

当前未发布插件64已接收不可变源46。可信Python素材根与安全复制已由实际受管创建、继承返工验证；原生／冷启动证据与固定宿主／秘密引用验收分别记录。
