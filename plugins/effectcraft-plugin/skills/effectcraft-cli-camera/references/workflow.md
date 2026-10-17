# 原生合成计划 / Native composition plans

`workflow.py` 首次调用安装器，然后在持续 MCP 会话中创建或修改合成。它保存原生 `.ecproj`、重新打开检查属性，并调用原生渲染器输出透明 PNG 和可选 H.264 视频。公开 launch.sh／launch.ps1 入口准备锁定的隔离 Python；平台制品以 runtime.lock.json 为准，原生任务验收按平台独立记录。

The helper bootstraps the pinned runtime, executes a bounded plan in a persistent MCP session, saves and reopens the native project, then renders transparent PNG frames and optional H.264 video. Public launchers prepare pinned isolated Python; runtime.lock.json defines platform artifacts, while native acceptance remains platform-specific.

以下 `SKILL_DIR` 沿用本技能 `SKILL.md` 的实际加载目录，脚本和示例均来自同一技能。

```bash
python3 "$HARNESS_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/brand-intro.json" \
  --output /absolute/path/intro-v1
```

技能安装在其他位置时替换技能根路径。输出目录必须不存在；不含外部素材时原子发布新目录；有外部素材时原生收集器需要稳定的最终目录，失败目录包含 `failure.json` 且没有成功清单，不可作为完成交付。安装目录不存放工程。

Replace the skill root with its actual loaded location. The output directory must not exist. Asset-free work is published by atomic rename. Native media collection needs the final directory to remain stable; a failed collection leaves failure.json without a successful manifest and is not a completed delivery.

## 计划与修订 / Plans and revisions

- `document`：新合成的名称、宽高、帧率、时长；时长及采样时间单位为秒。
- `operations`：原生命令及参数；`as` 将返回值保存为别名，`{"$ref":"title.layer"}` 引用原生图层 ID。命令以运行时注册表为准。
- `frames`：透明 PNG 的采样时刻，不得超出合成范围。
- `exports`：可选 `[{"format":"mp4"}]`；MP4 为不带透明通道的 H.264，不能当作透明视频交付。

`document` creates a composition. `operations` contains native commands and parameters; aliases reference returned IDs. `frames` selects transparent PNG samples. Optional MP4 export uses H.264 without alpha.

修订时读取上次 `manifest.json`，将 `files["project.ecproj"]` 写入新计划的 `expectedProjectSha256`，通过 `--source /absolute/path/intro-v1` 和新的 `--output` 调用。省略 `document`，仅传目标修改。摘要不一致立即报 `revision_conflict`，不覆盖用户修改。禁止并发写入同一输出路径。

For revisions, copy the prior manifest's project digest into `expectedProjectSha256`, pass `--source`, omit `document`, and use a new output directory. A digest mismatch stops the revision. Do not run concurrent writers against the same output path.

当前 CLI 的 `--comp` 使用合成名称；MCP 使用数字 ID。视频导出前检查名称唯一，避免选错同名合成。时间线、效果和关键帧保存在原生工程中；`native.json` 用于核对，不替代原生工程。

The pinned CLI requires the composition name for `--comp`, whereas MCP accepts numeric IDs. Video export checks name uniqueness. The editable project remains authoritative; `native.json` is inspection evidence.

## 交付与验证 / Delivery and verification

交付包含工程、`plan.json`、`operations.json`、`native.json`、透明预览、可选 MP4，以及带文件摘要的 `manifest.json`。示例仅包含内建图形和系统字体。外部素材通过下述注册入口导入并由原生收集器打包，清单核对收集后文件摘要。

The delivery contains the project, plan, operation receipts, inspection snapshot, previews, optional MP4 and a hashed manifest. The example uses built-in shapes and a system font. Registered external media is packaged by the native collector and checked against its declared digest.

已验证：原生往返、两关键帧透明度动画、效果参数保留、PNG alpha、MP4 解码帧数，以及修改文字后其他图层与关键帧不变。真实品牌视觉验收、蒙版覆盖、完整 Harness、插件宿主安装仍需单独验收。

Verified coverage includes native round trips, two-key opacity animation, retained effect parameters, PNG alpha, decoded MP4 frame count, and text revisions preserving other layers and animation. Brand-level visual review, mask coverage, the full Harness and plugin-host installation still require separate acceptance.

## 外部素材与替换 / External media and replacement

用 `--asset logo=/absolute/path/logo.png` 注册文件；计划内 `asset.import` 参数为 `{"asset":"logo"}`，例如 `as: "logoItem"`；随后 `layer.addItem` 的 `item` 参数引用 `{"$ref":"logoItem.item"}`。禁止导入未注册的项目项。安装目录不参与素材交付。

Register a file with `--asset logo=/absolute/path/logo.png`. Use `asset.import` with `{"asset":"logo"}` and alias `logoItem`, then reference `{"$ref":"logoItem.item"}` from `layer.addItem`. Unregistered project dependencies are rejected.

收集后的 `.ecproj` 引用 `(Footage)` 内的绝对路径。移动整个交付目录后，通过 `--source` 修订会先核对继承素材摘要、复制到新工作目录并重新链接。直接在其他应用打开已移动的工程可能需要重新链接，不能宣称原生工程完全使用相对路径。

Collected projects contain absolute paths into `(Footage)`. Revising a moved delivery through `--source` verifies inherited hashes, copies media and relinks it. Opening a moved project directly in another application may require relinking.

替换素材时先导入新的注册素材，再用 `asset.replace` 参数 `{"asset":"logo","replacement":"newLogo"}`。该操作保留原项目项 ID，已有图层、时长和关键帧继续引用同一个项目项；新交付保留最新依赖摘要，原交付不覆盖。

Import the replacement first, then use `asset.replace` with `{"asset":"logo","replacement":"newLogo"}`. The existing project item ID and layer animation remain intact. A new delivery records the replacement digest and preserves the source delivery.

15 项完整测试通过，其中素材用例检查原生收集、移动后修订、PNG 替换像素、图层与关键帧保持以及错误摘要拒绝。素材样本为程序生成的 PNG，不构成品牌视觉验收。

All 15 tests passed, including native collection, moved-delivery revision, replacement PNG pixels, preserved layers and keyframes, and digest rejection. Procedural PNG fixtures do not establish brand-level visual acceptance.

## 效果／蒙版参数错误 / Effect and mask parameter errors

固定原生引擎拒绝未知命令字段，工作流将 effect.apply／remove／toggle 和 mask.new／setVertex／remove 的匹配参数校验错误归类为 unsupported_mapping，并保留命令与原生诊断。不会省略未知字段重试；失败新建不发布交付，失败源工程修订保留原文件。效果数值通过对应属性路径设置，例如 effects/#1/blurriness；不能把 blurriness 当作 effect.apply 参数。蒙版羽化需使用原生支持的属性或命令，不虚构 mask.new feather 字段。cli.py 原始调用仍由原生 CLI 明确校验。

The pinned engine rejects unknown command fields. Matching validation failures for six effect/mask plan commands become unsupported_mapping, retaining the command and native diagnostic. No field-stripping retry occurs. Failed creation publishes no delivery; failed source revision preserves prior files. Use prop.set with the supported effect property path instead of invented effect.apply fields; use actual native mask properties/commands for feather controls. Raw cli.py calls retain native validation.

## Dynamic transparent sequence candidate / 动态透明序列候选

`exports: [{"format":"png-sequence"}]` requests the fixed native RGBA PNG renderer. The workflow retains `project.ecproj`, previews and a `rgba-sequence/sequence.json` manifest (`craft-image-sequence/v1`) with ordered frame paths, byte/pixel hashes, rational frame rate and duration, dimensions, bit depth and actual alpha extrema. No MP4 is produced for this export. Each frame must be RGBA8 with visible transparency, continuous numbering and identical dimensions. Requests are bounded to 10,000 frames and 512 MiB decoded RGBA pixels before native launch. Color space is recorded as unknown; encoding representation is straight PNG, not proof of cross-editor color fidelity.

`png-sequence` 为动态透明序列候选导出。交付保留原生工程，逐帧清单记录摘要、实际通道、帧率与持续时间。缺帧、多余帧、损坏、尺寸不一致或全不透明帧拒绝；导出前限制帧数和总解码像素预算。导入端必须核验全部帧及显式帧率，不能当作静态首帧。Film 默认图片序列媒体时间基与合成帧率可能不同；当前固定 Film 运行时未完成显式帧率修复，因此端到端动态交接及新版固定插件验收仍开放。

## 执行前字段合同 / Before-edit field contract

六条效果／蒙版命令会在整份计划开始时检查未知和必填字段；错误返回 unsupported_mapping，不读取源工程、不安装 CLI、不发布目录。固定合同绑定本技能内 runtime.lock.json 的 0.2.0 版本及二进制摘要。安装后的 describe_command 必须与合同一致；parameter_schema_mismatch 阻止打开／创建工程。原生对象、效果名、属性路径和数值检查仍在会话内执行。

All six effect/mask plan commands are checked for unknown and required fields before source reads, runtime installation or output creation. The local reflection contract binds the pinned binary/version. Live describe_command must match before opening/creating a project; drift blocks editing. Object existence, effect names, property paths and values remain native checks.

## 分段导出候选 / Segmented export candidate

当前源码公开工作流支持 `exports: [{"format":"png-segmented","chunkFrames":60}]`，省略 chunkFrames 时按预算分段；范围为整数 1–10000，每段仍受 512 MiB 上限约束。未知字段、其他格式携带 chunkFrames、无效范围或多个导出在安装／原生执行前拒绝。交付为原生工程、预览、`rgba-segments/segments.json`、全部子清单与帧、逐帧交换记录；具体边界见本技能 references/segmented-render.md。

The current source workflow accepts the explicit png-segmented format and optional integer chunkFrames. It retains the native project, previews and complete segmented delivery. Candidate Film consumption and Art scheduling pass bounded native fixtures; released Effect source dev.9 / plugin dev.10 do not contain this change. HD long rendering, immutable publication and installed cold use remain open.

## 失败暂存的原生恢复

公开工作流已经进入暂存后失败时，保留输出 `failure.json` 指向的 `stage`、该原位置的工程与素材，以及 `recovery-operations.json`。核对 `files` 中全部摘要及 `lastAttempt`，未知请求可能已经执行；不能自动重跑计划、移动暂存或删除失败目录。输出已有时会拒绝再次运行，成功交付才清理未使用暂存。

先用本技能 `commands.py` 的新会话执行打开／检查计划，并显式登记恢复工程作为 `--input project=原暂存工程绝对路径`；按真实对象状态建立新的修改计划。`failure.json` 不是交付 manifest，不能把失败输出直接传给 `workflow.py --source`。成功保存、重开、依赖收集及派生输出检查后才形成新的交付。诊断写入权限不足时仍保留暂存并返回原异常，不能假定失败输出目录一定存在。

After staged failure, retain both the output recovery record and its original sibling stage. Verify all file hashes and the last submitted attempt; an unknown reply may follow a successful native operation. Open/inspect the retained project in a fresh commands.py session before an explicit new revision. Do not replay the original plan, move the stage or pass the failed directory as a successful workflow source package.

## 合成配置门禁 / Composition configuration gate

`workArea: [start, end]` 使用秒，必须在有效时长内且至少包含一帧。新合成默认显式设置完整工作区；修订默认保留来源范围。锁定上游使用254016000000 ticks/秒，标准帧率与整帧时长按原生规则归一化。工作流在保存前和重开后核对宽、高、帧率、时长、工作区；差异返回 `composition_config_mismatch` 并停止渲染。成功交付增加 `composition-validation.json`，保留有效预期与原生观察值。原生命令 `comp.workArea` 的当前时间快捷方式及边界裁剪继续支持；原始 commands/desktop 入口的完整领域计划验收保持开放。

`workArea` uses seconds. New compositions explicitly use the complete effective range by default; revisions preserve the source range. The workflow checks dimensions, frame rate, duration and work area before saving and after reopening. Differences stop rendering. `composition-validation.json` records normalized expectations and actual observations. Native work-area shortcuts remain supported. Complete domain qualification for raw command/desktop plans remains open.
