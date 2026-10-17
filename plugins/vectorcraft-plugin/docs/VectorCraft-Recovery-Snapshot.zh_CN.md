# 中断恢复的快照身份

当前状态：公开固定50／实际宿主源38已通过VC-TX-002全部七个当前场景，任务3.6完成；13组真实场景、109项Node与43项Python通过，13技能摘要保持、30个登记组停止。当前96项完成／31项开放，3.9与完整V1继续开放。下文保留各早期版本当时的证据边界，不改写历史报告。[逐场景验收](evidence/vectorcraft-task-recovery-fixed50-20261009.json)。

插件 dev.45 在副作用意图中持久化控制文件 SHA-256。恢复在启动任何原生检查进程前，核对完整技能目录摘要、计划快照摘要与控制文件摘要；更换脚本、修改计划或授权、以符号链接替换快照均拒绝。计划与技能摘要同时与任务绑定核对。摘要缺失的旧任务返回 recovery_identity_missing，继续保留工程占用；不得用当前文件生成“原摘要”。这是旧未完成任务的兼容性限制，已完成交付与固定技能快照不改变。

[合同](../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md)的事实源仍为 establish-v1-plugin。恢复只读取原位置工程、素材依赖和回执，不迁移失败目录，不重放未知编辑，不把中断工程提升为成功交付。取消结束为 cancelled；未知崩溃结束为 interrupted_verified；两者均推进epoch。

候选原生证据覆盖真实检查点保存后的取消、三个保留快照误改拒绝、父进程SIGKILL后存活原生组、重启无重放、原文件只读重开、交接及迟到原生回复记录隔离。SIGSTOP仅为本用例登记的原生组冻结故障现场，SIGKILL仅终止本用例的协调器和确认归属的进程组。没有模拟原生保存或用文件存在替代重开。任务3.3已由固定47关闭；完整3.6、3.9仍需各自全部场景；GUI竞争、非空链接依赖与预算矩阵不由本证据代替。

```mermaid
stateDiagram-v2
 [*] --> running
 running --> reconciling: 协调器崩溃且结果未知
 running --> cancel_requested: 请求取消
 reconciling --> reconciling: 原生进程未停或快照身份不符
 cancel_requested --> cancel_requested: 原生进程未停或快照身份不符
 reconciling --> interrupted_verified: 停止确认且原文件只读核验通过
 cancel_requested --> cancelled: 停止确认且原文件只读核验通过
 interrupted_verified --> [*]
 cancelled --> [*]
```

插件48同时核对源工程依赖快照的完整摘要；快照文件改动、增删、链接替换或目录丢失在原生检查前拒绝。源任务缺少原快照摘要时报告 recovery_identity_missing，保持占用。候选新增6个失败用例与1个有效快照用例；真实取消恢复同时覆盖技能、计划、控制与源快照4种误改拒绝。

新增保存后回执丢失验收：真实原生保存与9项导出、交付摘要验证均完成后，测试在账本receipt入口终止自己的协调进程。重启确认步骤仍submitted且没有result，原生组已停止；保留原输出inode并只读重开，不增加attempts或bytes，不换路径重试。结果为interrupted_verified，实际丢失回执随后按旧epoch隔离，不提升为成功交付。该次证据未覆盖原生调用前崩溃与非空链接依赖；后者的新增原位置验收见下文，3.6保持开放。

公开固定插件48及其实际宿主加载的源37已通过上述取消／快照与保存后回执丢失场景，以及84项Node、43项Python回归；13技能摘要不变。仅覆盖macOS arm64，不关闭3.6。[固定证据](evidence/vectorcraft-source-recovery-fixed48-20261008.json)。

2026-10-09使用当前仓库验收脚本，调用公开安装的固定48实现及该宿主实际加载的源37，创建带1个真实链接PNG的自有合成工程。协调器在已保存检查点后停止，原生进程组确认退出；素材缺失与修改均使原生links.check拒绝恢复且保留源占用。健康只读核验之后再次改动素材，settle拒绝结算；恢复原字节并再次只读核验后结算为interrupted_verified。多个检查点的非空链接均指向原失败暂存目录，工程／素材inode、原源工程及事件摘要保持不变，全部自有检查进程停止。15项恢复回归通过，13技能摘要保持。验收脚本不是原tag48的内置文件，实际执行的src字节逐项匹配已安装tag48。原生调用前重启及完成回执绑定等矩阵仍开放。[非空链接证据](evidence/vectorcraft-linked-recovery-fixed48-20261009.json)。

插件49／源38补齐完成回执与交付目录身份：检查前将已收到的步骤回执绑定到运行时、原源修订、清单和逐文件摘要；检查后对同一intent／state／result摘要复核，变动时拒绝结算。旧pending检查证明缺少步骤摘要时返回recovery_receipt_identity_missing，需要重新只读检查，不改变已完成任务。源38在最终重命名前fsync登记实际交付目录的device、inode、原位置、目标及清单摘要；带链接素材的打包子目录不再被初始暂存目录inode代替。旧源37缺少该记录的已打包未知任务仍保留占用，不能补造旧身份。普通／真实链接工程的回执前后四种协调器崩溃候选均通过；运行时回执、清单、文件及核验后回执误改拒绝。固定49验收另行记录；原生调用前重启与完整3.6仍开放。

公开固定插件49／实际宿主源38已完成上述四种真实崩溃复验；13技能摘要保持，97项Node、43项Python回归通过，原生调用前重启仍开放。源38已有176项源码测试，其中146通过、30原生／宿主门禁跳过；不能将跳过计为通过。[固定49证据](evidence/vectorcraft-receipt-recovery-fixed49-20261009.json)。

候选插件50新增registered-go/v1：任务登记事务建立prepared门禁；步骤与启动器身份持久登记后，GO授权事务才可转换为authorized，提交后才发送stdin。恢复事务将未授权门禁封存为sealed，迟到步骤与GO均拒绝。新建任务无原工程时明确没有可重开产物；有源工程则原位置只读重开及links.check，结算前复核步骤、原输入、目录／文件身份和检查进程停止。部分准备快照保留，预算不重置，epoch推进，不自动重放。表是schema3的兼容扩展；旧任务不补造门禁。已有ready任务也不自动重复准备。六个候选真实检查点通过，固定50与完整3.6仍开放。

```mermaid
flowchart LR
  A[prepared] -->|registered intent and launcher| B[authorized]
  B -->|commit before stdin| C[GO]
  A -->|recovery transaction| D[sealed]
  D --> E[readonly original input check]
  E --> F[epoch advances; no replay]
```
