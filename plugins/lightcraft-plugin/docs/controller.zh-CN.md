# 显式任务控制器

本资料说明当前接口，不是宿主加载或原生验收记录。控制器通过插件根目录的 `scripts/controller.py` 调用；任务目录与照片库由调用者明确指定，不能猜测宿主缓存路径。运行可能安装原生依赖，只能在已有相应授权时使用；纯诊断使用技能自己的 doctor。

## 建立与执行任务

`init` 的 `--payload` JSON 对应以下字段；本例仅展示只读照片库查询计划，不是可交付照片编辑闭环。

```json
{
  "goal": {"request": "检查指定照片库"},
  "plan": {"domain": "lightcraft", "steps": [{"command": "library.info", "params": {}}]},
  "inputs": ["/absolute/originals"],
  "library": "/absolute/library",
  "output_root": "/absolute/exports",
  "max_revisions": 3
}
```

inputs 必须已存在且指向要保全的原片；library 是可修改持久库，output_root 是导出目标根；任务目录必须是新目录。已有任务不能再次 init。实际编辑计划须根据当前目录选择照片，包含 photo.inspect、develop.get 与导出步骤，不能把示例中的库查询当作完成编辑。

```bash
python3 -I -B scripts/controller.py init /absolute/new-task --payload /absolute/init.json
python3 -I -B scripts/controller.py run /absolute/new-task --runtime-home /absolute/runtime
python3 -I -B scripts/controller.py status /absolute/new-task
python3 -I -B scripts/controller.py reconcile /absolute/new-task
```

run 只接受 PLANNED 状态并持有任务锁；开始状态先落盘。status/inspect/reconcile 不启动 Lightcraft、不推进状态。UNKNOWN 不可重新 run；先核对回执与进程事实，不把目录中的导出文件当作执行成功。

## 停止与剩余步骤

stop 发布停止请求，即使运行控制器持锁也能请求；只有原始监督器能终止它启动的进程组，不能用 PID 文件向别的进程发送信号。请求成功不等于原生已取消。

remaining 仅在可信 FAILED_OR_PARTIAL 回执中提取明确 NOT_EXECUTED 的步骤。它还核对 run、计划、资源和输入身份，只输出建议片段；新会话须恢复库与照片选择，并重新确认执行范围。该接口不修改原任务或自动执行。

## 审阅与修订

review-request 的 payload 字段：

| 字段 | 内容 |
|---|---|
| candidates | 每个对象包含真实 path，可用 expected 声明 format/width/height/bitDepth/colorSpace/iccSha256 |
| settings | 执行回执中成功 develop.get 返回的完整设置对象，不能手填期望值或只提供局部补丁 |
| rubric_version | 非空审阅规则版本 |
| reopen_evidence | 可选 `{ "receiptPath": "/absolute/independent-run/receipt.json" }`；最终 deliver 时必需 |

候选必须可解码且符合目标，并且执行回执中有成功 photo.inspect 提供照片 ID 与源身份。请求绑定目标、原片、候选、设置、规则和修订次数。review 的 payload 遵循 `schemas/review-receipt.schema.json`：schemaVersion、requestId、bindingSha256、source（human/host-model）、reviewer、verdict（PASS/FAIL）和非空 observations 数组。它必须来自实际审阅；包校验不得自行生成视觉 PASS。候选变化或重复回执均拒绝。

失败审阅后用 revise 提交 `{plan, issue, scope}`，明确问题与允许调整范围。次数和历史保留在任务中；达到 max_revisions 后拒绝，不因重启重置。修改计划须指定新导出路径，不能覆盖既有候选。

## 最终交付

deliver 要求当前视觉 PASS、候选与原片未变，以及同一库在不同 runId 的独立会话重开回执。设置与照片源身份必须一致，library.info 明确 persistent=true、unsavedOps=0，库摘要不能在重开后变化。只满足其中一层时不能完成。

成功后保留 state.json、delivery.json、执行日志、审阅请求/回执和修订历史；交付回执分列执行、持久化、文件、重开、视觉及未验证项。真实宿主/原生/视觉验收与发行状态见 [实施证据](verification/implementation-evidence.md)。

## 发行来源校验

候选来源仅校验候选身份和摘要。切换为正式发行锁后，需要调用者提供实际技能源 Git 检出以核验 tag、commit 与文件 blob：

```bash
python3 -I -B scripts/validate_package.py --source-git /absolute/lightcraft-skills
python3 -I -B scripts/release_preflight.py docs/verification/local-report.json --source-git /absolute/lightcraft-skills
```

CI 使用 `LIGHTCRAFT_SOURCE_GIT` 指向受检来源；工作流只从固定官方来源仓库检出锁内 commit，并拉取 tag。检查入口不会自动克隆或安装，缺少 Git 来源仍拒绝正式发行校验。通过来源检查不等于宿主、视觉或公开发行通过。

## 只读 MCP 会话观察

```bash
python3 -I -B scripts/controller.py session-inspect /absolute/probe/receipt.json
```

输入必须是上游 `session_probe.py` 生成的 v1 只读探测回执。适配器核对固定请求、计划、原生版本与摘要、模式、端点和步骤，不启动原生程序或写入任务。`sourceSnapshotMatches=false` 表示观察来自其他技能源资源；只能只读查看，不得用来恢复任务或交付照片。原生协议未提供桌面会话 UUID，不能把客户端 runId 当成桌面身份。

initialize 成功只说明协议启动；实际库查询失败仍是 FAILED_OR_PARTIAL 或 UNKNOWN。任何探测都返回 taskExecutionAllowed=false、deliveryAllowed=false、automaticReplay=false。插件受保护技能快照仍锁定公开 v0.1.0-dev.1，此接口不代表已安装快照支持新增 MCP 执行。

## 结构化批量范围

init payload 可提供 batch_scope：`{"targetIds":[2,3],"observedIds":[1,2,3],"allowedFields":["light.exposure"]}`。observedIds 包含目标和需保全的对照照片。develop.set 必须明确提供 ids 与 values，不允许当前选择式 control/value、全量 reset 或其他写命令。每张观测照片须在全部写入之前和之后各 photo.inspect 一次，完整前后设置和原片身份必须一致，只有授权字段可改变。

批量 revise 的 scope 必须为 `{"targetIds":[3],"allowedFields":["light.exposure"]}`，且为初始合同子集；run 会重新校验。批量 review-request 的 settings 改为按照片 ID 的对象，例如 `{"2":完整实际设置,"3":完整实际设置}`，不能用单张设置替代整个批量。每张 target 的实际 photo.inspect 必须出现在独立重开回执中，并与审阅绑定的完整设置一致。

该能力是显式 opt-in；旧任务不自动推导批量范围。实际测试见 [批量验收](verification/batch-20261008/README.md)。

## RAW 逐样本结果观察

```bash
python3 -I -B scripts/controller.py raw-inspect /absolute/raw-evidence.json
```

入口只读核对 manifest、原片/目录条目、每次原生回执、相机身份、解码标记、设置重开和导出文件；不会下载、安装或启动 Lightcraft，图像技术检查可调用已有系统解码器。原始文件/回执不可用时，不能声明当前结果已验证。旧格式仅兼容只读历史，不能转换成执行许可。

返回 taskExecutionAllowed=false、deliveryAllowed=false、automaticReplay=false。FULL_RAW_REPORTED 是固定运行时报告，PREVIEW_FALLBACK 不是完整 RAW；UNSUPPORTED 必须来自完整原生导入回执的明确错误，环境失败不能代替。结果只涵盖每个 make/model/variant/SHA256，不按扩展名或品牌泛化。sourceSnapshotMatches=false 只允许查看外来源事实，不代表已升级受保护快照。

## SAM 只读评估报告

`python3 scripts/controller.py sam-inspect /明确的/sam-assessment.json` 复核 `sam_contract.py` 的观察输出。它核对固定模型身份及当前文件，拒绝权限提升；不启动原生程序或模型，不接受许可，不下载。命令缺失记为 UNKNOWN；报告不是原生证明，不能交付或重放。详见 `docs/verification/sam-20261008/README.md`。

## 三领域协议只读前检

`python3 scripts/controller.py craft-inspect /明确的/bundle.json` 调用随插件分发的 craft_exchange.ts，需要已有 Node 24+。操作 task/artifact/invalidate 的结构见 [协议接口](craft-exchange.zh-CN.md)。输出不允许任务执行或重放；真实 ArtCraft 宿主路由仍未验收。
