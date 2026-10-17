# VectorCraft 优化实施与验收边界

本轮实施对应 establish-v1-plugin 的第9节及其依赖。插件当前源码为dev.43，继续固定消费已发布技能源dev.37；公开插件43已通过固定安装逐场景复验，任务2.6完成。独立技能源未改动，历史候选报告保持各自执行身份。

## 已实施模块

| 所属仓库 | 模块 | 验证边界 |
| :--- | :--- | :--- |
| vectorcraft-skills | workflow、commands、mcp_session 的统一严格 JSON 与错误分类 | 自动化失败／通过测试；原生保存后故障与重开另验 |
| vectorcraft-skills | brand_variants 字段允许清单、请求值、色板及消费者检查 | 路径／文字／几何／非目标外观拒绝；RGB 原生案例，其他作者模型与 tint 单元语义 |
| vectorcraft-skills | 13项操作合同、use 隐式路由与专项显式调用 | 确定性生成、自包含与单技能入口；宿主实际派发另验 |
| vectorcraft-plugin | current_identity、evidence_index | 固定版本、报告与依赖摘要；保持历史层级和 NOT_RUN |
| vectorcraft-plugin | SQLite Ledger 与 Controller | 持久意图、工程占用、epoch、预算、取消状态和已固定技能调用；完整异常／宿主验收仍逐项推进 |
| vectorcraft-plugin | ReviewStore、领域 schema、矢量 rubric | 单轮请求／回执、陈旧与重复拒绝、技术门禁及局部修订提案 |

## 本地入口

需要 Node.js 24；TypeScript 由 Node 原生类型剥离执行，无 npm 依赖安装。Python执行仍由固定的自包含技能持有。插件模块不会联网调用模型或自行开启下一轮。

```bash
npm test
python3 -I -B scripts/current_identity.py --check
python3 -I -B scripts/evidence_index.py --check
node src/cli.ts run STATE.sqlite REQUEST.json
node src/cli.ts review-request REVIEWS.sqlite INPUT.json
node src/cli.ts review-import REVIEWS.sqlite RECEIPT.json
node src/cli.ts revision REVIEWS.sqlite CHANGES.json
```

run 请求包含 key、skill、expectedSkillSha256、plan、output、runtimeHome、estimatedBytes 和 authorization；返工还含 source。授权记录明确 objects、fields、绝对截止时间 deadline、maxAttempts、maxBytes、可选共享 budgetId、readRoots 与 writeRoots。技能整树摘要与 `scripts/vendor/skill_vendor.py` 算法一致；固定插件请求应使用其技能锁里的摘要，不使用浮动 main 作为身份。

Controller 仅协调公开 workflow 计划；完整命令计划继续通过独立技能的 commands 入口执行。完成文件核验仅进入 review_ready。未知执行保留占用与原文件，不自动重放；父进程退出不证明原生子进程已停止。取消确认和恢复观察必须来自实际原生检查，不能把调用 API 的布尔值当作现场证明。

## 单轮评审

请求绑定源修订、运行身份、可编辑原生文件、候选预览／导出、目标与 rubric 的摘要。targets 中 target 是实际任务目标，judge-reference 只供评审；至少一个 target。technicalStatus 为 PASS／FAIL／NOT_RUN；技术失败或未执行不能被高视觉评分覆盖。

评审请求及回执 schema 位于 schemas；默认 rubric 位于 docs/vector-review-rubric.json。回执包含 reviewer 的身份与上下文来源，五项0–4评分和定位到对象／字段的问题。未核验宿主上下文证据时 independent 始终为 false；自报独立性不会成为事实。人工或当前宿主模型均可评审，但应如实记录同一上下文及未验证项。

revision 仅生成提案，重新核对当前文件指纹、有效授权及已评审的问题，不执行任意模型命令。预算、取消、停滞和跨重启完整合同仍由第3／6节验收；不能以单轮存储测试宣称完整自动循环完成。

## 发行与证据

两仓 CI 均有本地等价检查入口。源码候选、GitHub CI、不可变公开标签／制品、固定安装副本、宿主派发、GUI 和模型分别记录。插件 skills 目录保持原固定快照；新技能源仅在发布后经 vendor 同步。实际 Skills CLI 安装、Art 内置领域包升级、完整 GUI／模型、逐命令与 V1 门禁继续按原范围验收。

## 当前验收与未完成门禁

上一轮独立源候选通过159项默认回归中的129项，30项原生／GUI检查按条件跳过，未作为通过计数。另行显式执行的13技能独立冷启动、10个场景创建／返工、两入口8个真实消费者／非消费者误改故障、6类保存后异常与三画板九导出均通过。默认回归与这些显式原生验收分别记录。

上一轮插件通过28项Python回归和11项Node测试；真实原生单轮评审／返工使用外部提供的当前会话回执，独立性为false。评审绑定交换损失文件并持久保存拒绝原因。执行前持久化计划及已复核技能快照，缓存回用会核对原回执中的manifest摘要。共享budgetId的调用原子扣除同一预算，不将子进程退出当作原生停止证明。

可复现原生单轮：`node scripts/acceptance/single_round.ts CONFIG.json`。CONFIG显式提供skill/source/runtimeHome/output/receipt/python/brief/targetColor/authorization/changes；仅适用于Brand Primary夹具，评分来自已提供回执，不自动评审或发起下一轮。

9.3、9.6、9.9、9.18尚需新的不可变公开发行、固定安装与宿主验收；9.21已有真实单轮局部证据，但3.x／6.x的完整取消、恢复、授权执行与停滞合同未全验收，保持开放。当前插件固定技能仍为dev.33，不能把候选dev.34测试用于证明安装副本已更新。GitHub CI未在本轮运行；未提交、推送、打标签或发布。


## 执行控制增量（2026-10-08）

当前源候选加入可选的 execution_control：原生每次请求前检查撤销、截止时间、epoch、源工程摘要和累计输出预算，先fsync调用意图；原生子进程受单文件大小上限约束。托管返工按真实对象及字段授权核验，全球色板的每个消费者均需授权；未分类返工命令拒绝。几何、文字、其他色板及画板保持严格比较，原生保存产生的metadata.modified单独核验。

插件的独立进程组在启动门禁放行前记录PID／PGID／启动时间／任务nonce。进程组身份不能确认时保留占用，父进程退出后仍检查后代；TERM无效才对已验证归属的进程组升级KILL。cancel只请求撤销，reconcile必须观察原生停止、原位置目录inode、全部文件摘要，并用固定原生引擎只读重开工程和检查链接后，才能转为cancelled或interrupted_verified。未知结果不会升级为review_ready，不自动重放。恢复后的旧epoch回执单独审计隔离。

```bash
node src/cli.ts cancel STATE.sqlite TASK.json
node src/cli.ts reconcile STATE.sqlite TASK.json
node scripts/acceptance/managed_cancel.ts CONFIG.json
```

TASK含taskId与epoch。CONFIG沿用单轮品牌夹具的skill/source/runtimeHome/output/python/targetColor/authorization；原生取消测试在真实检查点保存后撤销，没有模拟原生写盘。当前固定dev.33技能尚无控制模块，因此托管执行会明确拒绝；独立公开入口仍保持原合同，发布dev.34后再固定同步和安装验证。

当前回归为独立源162项（132通过、30条件跳过），插件15项Node测试。原生候选验证覆盖单轮授权返工、真实检查点后的取消、监督器重启、原位置工程和依赖核验、epoch隔离；不代表完整3.x／6.x、固定安装或完整V1。OpenSpec已勾选3.1／3.2／3.4／3.5／3.7／3.8，完整验收3.3／3.6／3.9继续开放；总表81完成、46开放。

插件42补充schema3迁移前只读备份与明确模式绑定；实际旧阅读器拒绝新schema。当前跨版本原生局部证据与完整2.6验收边界见[运行时门禁](Runtime-Gate.zh-CN.md)。技能源仍固定dev.37。

当前状态（公开插件43／固定源37）：任务2.6全部7个运行时场景完成，证据见[运行门禁](Runtime-Gate.zh-CN.md)；上文候选／开放描述保留为原阶段记录，不作为当前完成判断。其他33项任务、完整V1及创意GUI／模型门禁仍开放。


公开提交固定副本验收：从远端main的完整不可变提交`11a49e9d1d5f471d1c4cbf93551bdb1c87abe3d1`安装dev.64/source46到独立、含空格的Codex0.153.4配置；13技能发现与身份匹配，13次独立HTTPS空缓存启动、12组原生创建／返工通过，setup-only单独标记，不计作跳过。实际安装Harness完成原生返工、三格式重新解码、4次共享额度停止及源／文本保全；回执评分为显式QA夹具。5项引用守卫及161项Python回归通过。新脚本默认仍要求公开版本标签；显式候选只允许与远端main相同的完整SHA，并记录publicTagVerified=false。旧脚本原字节已归档，旧报告不重签。此证据推进9.9／9.18的安装与冷启动部分，不关闭模型默认路由、公开标签复验、六层发行门禁、全命令GUI或秘密边界；121/127完成、6项开放。 [Evidence](evidence/vectorcraft-public-commit64-install-20261009.json).


当前固定副本四场景复验：dev.64/source46公开提交安装上，6次原生修订、15项守卫及拥有签名桌面的源工程修改／保存／重开后陈旧建议拒绝通过；最佳候选、轮数、停滞、额度与文本保全按VC-QA-002核验。桌面初次夹具越界被正确拒绝，调整为测试拥有的GUI根内工程后通过，产品权限未放宽。证据v2解析已绑定checker_bundle.ts的完整10文件身份；发布门禁核验所选当前报告，旧v1三文件证据与原脚本归档保留。当前六层开发发行门禁通过，市场资格仍为false；公开标签后的安装复验、模型路由、权限／秘密完整边界及逐命令GUI仍开放，121/127完成、6项开放。回执评分为QA夹具，不代表真实创意评审。 [Evidence](evidence/vectorcraft-revision-commit64-20261009.json).


公开标签发布后复验：插件v0.1.0-dev.64已发布，标签指向6763caa1f0e6596fc01d298304794d0e9c139dc3，固定独立技能源v0.1.0-dev.46。从公开标签安装到全新Codex0.153.4隔离配置，13技能身份一致；13次独立HTTPS空缓存启动、12组原生创建／返工通过，setup-only单列，零跳过。安装产品源码与发行前四场景副本逐文件一致，main／tag共4个CI运行通过。已完成且无句柄的13个测试运行时缓存被清理，原生工程和执行记录保留。此结果补齐9.18的公开发行及实际安装／冷启动部分；其9.9真实模型默认路由等前置仍未完成，不关闭9.18。权限／秘密完整边界、全命令GUI、其他平台与完整V1不提升；121/127完成、6项开放。 [Evidence](evidence/vectorcraft-public-tag64-install-20261009.json).


逐命令固定安装增量：公开插件dev.64／源46的实际安装副本在拥有的签名桌面会话中完成22条paint命令、44轮原生保存／重开和88项SVG／PNG解码。逐条检查实时enabled、原始参数、目标颜色／渐变／自由渐变、控制文字、源工程和前次交付保全；自由渐变分线按固定上游Catmull-Rom曲线核验。初次QA的注册表数量、RGB读回形式、选择状态及线性位置假设错误已保留并修正，不属于产品修复。外置全目录矩阵明确22/585已验、563项NOT_RUN；固定技能快照不改写。画布图像来自原生工具，不是操作系统窗口截图或创意评审。任务8.3仍开放，121/127完成、6项开放。 [Evidence](evidence/vectorcraft-command-matrix-fixed64-20261009.json).


色板逐命令固定验收：公开插件dev.64／源46实际安装副本在拥有的签名桌面中完成全部22条swatch命令、44轮原生保存／重开和88项SVG／PNG解码。全局色更新、删除保色解绑、合并重联、组编辑／排序／移动、Lab专色选项及色库保存／加载均有逐条语义断言，控制文字、源工程、前次交付保全；13个实际安装技能前后摘要一致。首次色库加载触发QA字段访问错误，原失败记录保留，修复验收器后全族复验通过，产品和固定技能源未修改。复用原paint22条证据，汇总44/585已验、541项NOT_RUN、88轮保存重开及176项导出解码；25项命令目标回归通过。原生画布图像不提升为系统窗口截图或创意评审。任务8.3仍开放，121/127完成、6项开放。 [Evidence](evidence/vectorcraft-command-families-fixed64-20261009.json).


```mermaid
flowchart LR
  A[公开固定安装与13技能摘要] --> B[拥有的签名桌面与局部工程]
  B --> C[实时上下文及原始参数]
  C --> D[命令执行与逐条语义断言]
  D --> E[原生保存与导出解码]
  E --> F[重开比对及源与前次交付保全]
  F --> G[第二轮修改与固定证据]
  G --> H[全585条矩阵保留未验项]
  C -->|禁用或未知| X[停止并保留失败记录]
  D -->|未知结果或断言失败| X
```


描边逐命令固定验收：公开插件dev.64／源46实际安装副本完成全部10条stroke命令、20轮原生保存／重开及40项SVG／PNG解码；13个安装技能摘要一致。箭头、高级轮廓及宽度点使用开放路径，内外对齐使用封闭路径；按半宽系数核对pt宽度点、箭头缩放交换、沿线／跨线轮廓翻转以及自定义轮廓增删重置。填充、控制文字、几何、源文件和前次交付保全。5类样式修改的10组原生画布／PNG比较均有142–1189个像素变化，43项命令目标回归通过。空列表reset与重复轮廓add被原生禁用的QA失败保留，夹具修正后复验通过；产品及固定技能不修改。自定义轮廓名称仅验拥有的私有桌面会话内行为，跨应用重启的偏好持久化NOT_RUN，不提升为系统窗口截图或创意评审。保留原44条汇总及校验器原字节，当前汇总54/585已验、531项NOT_RUN、108轮保存重开与216项导出解码。任务8.3仍开放，121/127完成、6项开放。 [Evidence](evidence/vectorcraft-command-families54-fixed64-20261009.json).


| 描边输入 | 验收计算 | 保全范围 |
| :--- | :--- | :--- |
| 宽度点left/right（pt） | 原生系数 = 2 × 侧宽 / 描边weight | 其余宽度点、填充与几何 |
| swapArrows和arrowScale | 起终箭头及缩放成对交换 | 颜色与非描边外观 |
| flipProfile | along：t变为1−t并重排；across：左右宽度交换 | 点值与排序的精确对应 |
| 自定义轮廓名称 | 私有会话内的增删重置及列表 | 不声明跨应用重启偏好持久化 |


逐命令透明度固定安装增量：公开dev.64/source46实际安装副本在拥有的签名桌面中完成全部17条transparency命令、34轮原生保存重开及68份解码SVG/PNG导出。逐命令核验对象百分比与混合／挖空选项、顶层蒙版移动与释放后重新编号、启停／链接选项、页面标志、默认值对新建蒙版的实际影响，以及编辑层进入／退出和查看开关的原生返回状态。临时编辑层不进入保存工程，蒙版艺术与控制文本保全；13技能身份不变。三种修订的6次实际画布／PNG比较有1208–2160像素变化。初次夹具错误（无效描边颜色、默认false省略字段、新探针文档未保存）已保留并修正，全族从新拥有会话复验通过，产品及锁定技能未改动。默认值只覆盖私有会话，应用重启后的偏好持久化仍NOT_RUN；普通screenshot是艺术板渲染，不能证明蒙版灰度查看或完整窗口GUI。原54命令矩阵与校验器原字节保留；当前71/585通过、514 NOT_RUN，142次保存重开、284份解码导出。任务8.3保持开放，121/127完成、6项开放。 [Evidence](evidence/vectorcraft-command-families71-fixed64-20261009.json).


另补充viewOpacityMask单命令真实窗口验收：两张1440×900原生窗口及各三个画布内部灰度／彩色像素样本，关闭查看仍编辑蒙版。不能扩展为585命令全部GUI通过。 [Evidence](evidence/vectorcraft-mask-window-fixed64-20261009.json).


逐命令形状固定安装增量：公开dev.64/source46实际安装副本在拥有的签名桌面中完成全部10条shape命令、20次原生保存重开、40份解码SVG/PNG及20张真实应用窗口。独立公式核验矩形圆角、椭圆／弧线曲线手柄、多边形／星形旋转及顶点、螺旋反向和衰减、网格线序与分隔数、确定性光晕子树和径向渐变；第二轮仅调整前轮真实返回对象的透明度，再创建参数不同的同类对象，原艺术／控制文本、未授权字段、源工程及前轮交付文件保全。30组画布／PNG／窗口像素比较均有变化（244–165235像素），13安装技能身份不变。窗口原始物理像素比例1×／2×均保留，窗口差异分析显式归一至1440×900；首次只读窗口捕获错误保留，最多三次纯读取尝试，编辑请求不重放。初次QA字段假设和白底光晕不可见夹具已修正，加入自有深色背板后全族新会话复验。旧71命令矩阵及校验器原字节保留；当前81/585通过、504 NOT_RUN，162次保存重开、324份解码导出。此窗口证据只覆盖形状10命令，不推广为全命令／创意／模型／V1通过。8.3仍开放，121/127完成、6项开放。 [Evidence](evidence/vectorcraft-command-families81-fixed64-20261009.json).

```mermaid
flowchart LR
    A[Actual owned app window] --> B[Decode original PNG and bind digest]
    B --> C[Record physical pixel scale 1x or 2x]
    C --> D[Normalize analysis to 1440x900]
    D --> E[Compare revision pixels]
    B --> F[Preserve original captures and native projects]
```


逐命令图层固定安装增量：公开dev.64/source46实际安装副本完成全部11条layer命令、22轮原生保存重开、44份解码SVG/PNG及22张真实拥有应用窗口。独立完整树断言核验当前层上方插入、嵌套子层、删除及当前层回退、复制子树全新前序ID、隐藏／锁定选择清理、绘制顺序收集、仅直接可选子节点、剪切路径移底并去除画笔及释放后保留无画笔路径、文档粘贴选项持久化。当前层／选择／目标用原生会话读回，不虚称随工程持久化。第二轮先修改自有图层名称，完整保全控制对象、其他字段、源文件及前轮交付。33组实际画布／PNG／窗口比较完成：可见性与剪切的4组画布／PNG比较分别变化964和419像素，其余按显式保全或只记录契约核对；窗口变化不单独作为命令语义证明。13安装技能身份不变，22项新增断言／证据回归通过。旧81命令矩阵及校验器原字节保留，当前92/585通过、493 NOT_RUN、184轮保存重开及368份解码导出。任务8.3仍开放；121/127完成、6项开放，不提升全命令GUI、创意／模型、权限秘密边界、市场资格或完整V1。 [Evidence](evidence/vectorcraft-command-families92-fixed64-20261009.json).

```mermaid
flowchart LR
    Before[自有夹具与原生会话读回] --> Execute[执行一次图层命令]
    Execute --> Tree[独立完整树与重开断言]
    Execute --> State[当前层选择及目标读回]
    Execute --> Images[画布PNG及真实应用窗口]
    Images --> Contract{预定像素契约}
    Contract --> Equal[状态命令交付保全艺术]
    Contract --> Different[可见性与剪切改变艺术]
    Contract --> Measured[窗口变化单独记录]
    Tree --> Evidence[摘要绑定固定安装证据]
    State --> Evidence
    Equal --> Evidence
    Different --> Evidence
    Measured --> Evidence
```


逐命令图形样式固定安装增量：公开dev.64/source46实际安装副本完成全部18条graphicStyle命令、36轮原生保存重开、72份解码SVG/PNG及36张真实拥有应用窗口。独立完整树断言核验不同尺寸矩形的单位框渐变映射、替换与追加外观／透明度保全、唯一名称与稳定ID、删除保色解绑、仍同步对象重定义跟随与已改外观对象保全解绑、合并堆栈顺序、排序／移动、未使用及绑定读回、内置目录和自有样式库保存／加载／名称冲突编号／再次导入复用。第二轮先修改自有源对象名称，原控制文字及其他字段、源工程与前轮交付保全。54组实际画布／PNG／窗口比较按显式变化／保全／测量契约核验；两轮删除预置不同外观，跨轮像素仅测量，每轮删除保色由执行前后完整树证明，不能把窗口差异独立当作语义验收。13安装技能身份不变；23项新增断言／证据回归通过。Override Character Color仅验证私有会话偏好及列表读回，跨应用重启持久化NOT_RUN。旧92命令矩阵及校验器原字节保留，当前110/585通过、475 NOT_RUN、220轮保存重开及440份解码导出。任务8.3仍开放，121/127完成、6项开放，不提升全命令GUI、创意／模型、权限秘密边界、市场资格或完整V1。 [Evidence](evidence/vectorcraft-command-families110-fixed64-20261009.json).

```mermaid
stateDiagram-v2
    state "未绑定外观" as Unlinked
    state "外观同步的样式绑定" as Linked
    state "已改外观但保留上次样式身份" as Edited
    [*] --> Unlinked
    Unlinked --> Linked: new or apply
    Linked --> Linked: redefine updates synchronized objects
    Linked --> Edited: change appearance
    Edited --> Unlinked: redefine preserves edited look
    Linked --> Unlinked: breakLink or delete preserves look
    Unlinked --> Unlinked: add appends appearance
```


外观验收诊断检查点：新增16条appearance命令的候选驱动、图像检查器和独立堆栈断言；尚未形成通过证据。a2在setActiveItem探针的内存undo恢复后，保存／重开缺少目标对象2；a3在effect.apply调用处结果未知并停止，所有自有进程停止，未自动重放。原因仍待隔离，不归因为产品缺陷。候选改为从原生保存快照恢复探针，但该修改尚未验收。缺少固定通过报告的18项正向证据测试保留在scripts/qa/pending/，不冒充已通过回归；CI执行堆栈单元测试及真实失败记录的断言。通过覆盖仍为110/585，475 NOT_RUN，任务121/127完成、6项开放，8.3不勾选。产品标签dev.64与技能源46保持不变。 [诊断](VectorCraft-Appearance-Diagnostic.zh-CN.md)。


逐命令外观固定安装增量：公开dev.64/source46实际安装副本完成全部16条appearance命令、32轮原生保存重开、64份解码SVG/PNG及32张真实拥有应用窗口（实际1440×900，1x）。独立完整树断言核验仅复制画笔的新填充／描边、清空／基本化、逐行属性与效果、去重删除、完整复制及Contents槽移动、不同边界渐变拾取与反向追加、隐藏恢复、锁定过滤的内容选择，以及带蒙版源对象的复制／移动转移及清源保全。活动外观行与新艺术偏好由实际编辑／创建探针证明，再从自有原生保存快照重开恢复，不提升undo链或应用重启偏好验收。第二轮先修改自有控制对象名称；原文字、其他字段、源文件及前轮交付保全，13安装技能身份不变。48组实际画布／PNG／窗口比较按显式变化／保全／测量契约核验；4类变化命令的8组画布／PNG比较变化722–2062像素，窗口差异不单独作为语义证明。此前undo／重开、未知回复与跨层蒙版顺序夹具失败保留；源层和显式ID准备已修正，全族新会话通过，产品／技能未修改。18项原待执行证据测试已纳入常规回归，另补2项证据篡改和2项夹具失败测试。原110命令矩阵、原校验器及诊断候选字节保留；当前126/585通过、459 NOT_RUN，252轮保存重开、504份解码导出。8.3仍开放，121/127完成、6项开放，不提升全命令GUI、undo、创意／模型、秘密边界、市场或完整V1。 [Evidence](evidence/vectorcraft-command-families126-fixed64-20261009.json)。
