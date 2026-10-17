# 可执行原生计划

`scripts/workflow.py` 是 vectorcraft-harness 技能自带的原生矢量操作助手，运行在单个 headless MCP 会话中；插件级任务账本与跨插件调度仍在实现。需要 Python 3.11+。首次调用自动复用或安装锁定 CLI，安装范围见技能入口。

以下 `SKILL_DIR` 沿用本技能 `SKILL.md` 的实际加载目录，脚本和示例均来自同一技能。

```bash
python3 "$HARNESS_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/brand-assets.json" \
  --output /absolute/project/brand-v1
```

按实际挂载位置替换技能根。输出目录必须是新的修订目录，已有目录不会被覆盖。

计划字段：

| 字段 | 用法 |
| --- | --- |
| document | 首次创建设置 name、width、height、units（Pixels/Points）；尺寸大于 0 且不超过 16384 |
| operations | 按顺序执行 `{command, params, as?}`；只允许脚本 ALLOWED 集中的原生编辑命令 |
| as | 把实际命令结果绑定为稳定业务名称，例如 logo；不猜上游对象 ID |
| `$ref` | `{"$ref":"logo.ids.0"}` 解析布尔结果的第一个 ID；普通文字不做替换 |
| exports | `{format: "svg"/"png"/"pdf", artboard: 0}`；零基索引，或用 `artboardId` 指定稳定ID（含显式 `$ref`） |
| expectedProjectSha256 | 修改既有交付时必须匹配源工程和 manifest 中的摘要 |

支持的命令范围见脚本 `ALLOWED`：基础形状、路径、文字创建、填充与描边、选择、组合、变换、四种布尔操作、添加与调整画板。其他命令通过原生 CLI/MCP 单独执行并验证，不能假定此助手已支持。

## 登记素材、链接和替换

通过 `--asset product=/absolute/input.png --asset logo=/absolute/logo.svg` 登记输入，脚本按文件内容识别 PNG／JPEG／SVG并计算摘要，不以扩展名判定格式。单独安装本技能即可安装锁定 CLI 并执行。`asset.place` 参数为 `{asset, at?:[x,y], rect?:[x,y,w,h], link?:true}`；at 和 rect 不可同时提供。一个别名可置入多个实例；所有实例写入交付清单。SVG 保持原生矢量组嵌入；栅格默认链接，显式 link=false 可嵌入。混用同别名的链接和嵌入状态拒绝成功交付。

新建模板见 `examples/provided-assets.json`。有效 SVG 必须自包含；外部 href、脚本、foreignObject、DTD／实体、外部 CSS URL 不在此公开素材合同内，不允许隐式读取额外文件。每项输入限 64 MiB。未消费素材、摘要冲突和非法路径不发布交付；预检可确定的错误在安装前拒绝。

修订计划使用 `asset.replace` 参数 `{asset:"product",replacement:"updated"}`，再加 `--asset updated=/absolute/new.jpg --source /absolute/project/v1`。替换栅格通过 links.relink 保留 ID、边界和堆叠；矢量组通过原生 file.place 逐实例置换，更新回执 ID，不冒充旧身份。替换后新素材归入原别名，禁止依赖旧组 ID 编写后续指令，应从更新后的 `$ref` 取得真实 ID。

有素材的工程调用原生 file.package 收集 Links 和许可允许嵌入的 Fonts。矢量／嵌入输入源文件仍在 Assets 保留摘要；无法打包字体记录到 skippedFonts，不声称跨机器字体可用。独立会话重开收集工程并核对链接，随后才导出和发布新目录。manifest.files 递归覆盖依赖文件，manifest.assets 记录 path、sha256、format、ids、linked。迁移交付目录可直接重开；部分原生链接元数据含引擎保存的原路径，但包内相对引用用于重新定位，不能把原路径当作新的读取授权。

## 局部改色

读取 `brand-v1/manifest.json` 的 `files.project.vectorcraft` 和 `bindings`，创建以下修订计划，将示意摘要替换为实际值：

```json
{
  "expectedProjectSha256": "源工程的实际 SHA-256",
  "operations": [{
    "command": "paint.setFill",
    "params": {
      "ids": [{"$ref": "logo.ids.0"}, {"$ref": "wordmark.id"}],
      "color": "#175cce"
    }
  }],
  "exports": [{"format": "png", "artboard": 0}]
}
```

执行时加 `--source /absolute/project/brand-v1 --output /absolute/project/brand-v2`。源目录保留不动；先核对摘要，再进入暂存工程编辑。命令失败不会发布目标目录。副作用超时不自动重试。

交付包含原生工程、各画板导出、重开后的对象模型、操作结果、计划和内容摘要。导出警告保留在 manifest；单画板 PDF 的 preserve-editing 警告不能忽略。`acceptance` 默认为需要领域与视觉复核，文件存在不是完整验收。

示例的两画板为 Logo/文字和未绑定的独立图标。修改 Logo 颜色时，第二画板应保持相同像素与文件摘要；原生对象的其他属性也应保持。此示例用于功能回归，不代表通用品牌设计质量验收。

## 失败暂存的原生恢复

公开工作流已经进入暂存后失败时，保留输出 `failure.json` 指向的 `stage`、该原位置的工程与素材，以及 `recovery-operations.json`。核对 `files` 中全部摘要及 `lastAttempt`，未知请求可能已经执行；不能自动重跑计划、移动暂存或删除失败目录。输出已有时会拒绝再次运行，成功交付才清理未使用暂存。

先用本技能 `commands.py` 的新会话执行打开／检查计划，并显式登记恢复工程作为 `--input project=原暂存工程绝对路径`；按真实对象状态建立新的修改计划。`failure.json` 不是交付 manifest，不能把失败输出直接传给 `workflow.py --source`。成功保存、重开、依赖收集及派生输出检查后才形成新的交付。诊断写入权限不足时仍保留暂存并返回原异常，不能假定失败输出目录一定存在。

After staged failure, retain both the output recovery record and its original sibling stage. Verify all file hashes and the last submitted attempt; an unknown reply may follow a successful native operation. Open/inspect the retained project in a fresh commands.py session before an explicit new revision. Do not replay the original plan, move the stage or pass the failed directory as a successful workflow source package.


## 两条品牌入口的变体导出

基于 source 修订时，普通 swatch.edit 与等价 native.command 均支持省略 exports：先按原 manifest 核验 plan.json 摘要，再沿用原清单内全部 SVG／PNG／PDF 和画板范围。不能把省略清单解释为无需导出。显式 `"exports": []` 则表示只交付原生工程，必须保留该意图。

网关操作写成 `{"command":"native.command","params":{"command":"swatch.edit","params":{"name":{"$ref":"primary.name"},"color":"#175cce"}}}`。expectedProjectSha256 取原 manifest 中 project.vectorcraft 的摘要；源目录仍由公开 --source 参数传入。旧 plan.json 摘要不符或为符号链接时，在安装与原生编辑前拒绝，不创建新交付。完成后比较所有输出路径、关联颜色及无关画板 SVG／PNG／PDF 字节，保留旧交付。

Both direct swatch.edit and its native.command equivalent inherit the verified source export list when exports is omitted. An explicit empty list remains an intentional native-only delivery. Verify source-plan integrity before installation, and check affected variants plus byte-identical unrelated SVG/PNG/PDF outputs after native reopening.

## 分组与布尔事务候选

普通工作流、`native.command` 和完整命令计划中的 `object.group`、`object.ungroup` 与 Pathfinder 操作在当前源码候选中登记实时参与对象ID、运算、真实结果ID和修改前检查点。成功回执位于 `boolean-transactions.json`；检查点进入交付清单。素材收集改变交付根时，检查点通过原生 package 独立收集依赖，并验证重开及链接，防止丢失或保留失效路径。

明确失败且原生文档已改变时，在同一仍有效的会话重开检查点并核对文档与参与ID，报告 `non_atomic_operation_defect`；不会重放运算。回复丢失、撤销、超时或恢复失败保持unknown／原位置现场，需只读核验后另行决定。未选子树、祖先属性和对象顺序变化不能由成功回执豁免。

此为未发布源码增量；发布标签dev.36和固定插件dev.40的旧快照保持不变。四类布尔运算、分组／解组、带链接素材迁移与显式故障注入有候选原生证据，不代表所有Pathfinder上下文、GUI或创作验收。

### Harness 结构修改授权

受控源修订的分组／解组／布尔操作要求授权 `fields:["structure"]`。`select.set` 仅能选择已授权ID，且实际选择必须一致；结构操作使用同会话实时选择，整个参与子树的ID均须在objects中。`kind`或路径字段授权不能替代structure。结果ID、未选子树、祖先／堆叠和文档属性仍由统一守卫核验。未知、撤销、截止时间和版本冲突的原有停止语义不变。该能力纳入技能源开发版37，旧dev.36标签不变。

## SVG文字模式与可编辑性

`native.command` 调用 `document.setup`，参数 `{"exportText":"appearance"}` 可选择SVG轮廓文字；`editable`保留可导出的文字元素。工作流从实际导出会话只读查询模式，并在绑定摘要的 `exchange-loss.json` 中记录 `live-text-editability`。appearance模式输出的文字丢失文字编辑语义，保留独立原生工程；未知模式不得由path数量或预览推断已轮廓化。报告的原生文字ID是文档依赖，不说明哪些文字进入单画板输出。

普通、`native.command`及完整命令入口的`text.setText`统一要求显式`id`或`ids`及字符串`text`，不沿用隐式选择。原生整段替换采用首个样式；多段富文本样式不能宣称全部保留。字体可移植性与跨编辑器版式保真继续标为未知。

## 画板稳定身份与输出顺序

`exports`支持`{"format":"png","artboardId":42}`，ID来自当前原生画板或`artboard.new`绑定回执（原生只返回索引时，助手立即查询同会话真实画板ID后补充绑定，不把索引当ID），也可写`{"$ref":"variant.id"}`；不要猜测ID。仅给稳定ID时按当前原生顺序解析；同时给`artboard`零基索引时两者必须一致。首次创建可沿用旧索引计划。返工旧索引先从实际打开的源工程绑定原ID，操作后该索引改变身份则拒绝成功交付并报告原ID、实际ID和原ID的新索引；要跟随重排，应显式改用稳定ID。新增且原源工程无对应索引的画板可按当前索引导出，建议使用创建回执ID。

全部输出映射在第一份导出前校验；未知ID、冲突索引和解析后重复输出均拒绝，不发布成功清单。已开始原生操作时保留原位置失败暂存，原交付不改。交付`artboards`记录原生ID、名称、矩形、尺寸和当前索引，`artboardOrder`为原生ID顺序，`outputs`保持请求顺序并附实际索引／ID，`previewOrder`仅列PNG输出的相同请求顺序。文件名`artboard-N`仍以当前零基索引加一命名，不能当成跨版本稳定身份。

Stable IDs identify native artboards; indices describe their current zero-based order. Export by `artboardId` to follow reordering; supplying both ID and index requires agreement. Legacy revision indices bind to actual pre-operation source IDs and refuse identity shifts. The complete mapping is checked before any export. Manifest artboards and output records expose names, dimensions and actual indices; PNG previewOrder follows requested output order. File-name numbers are not stable IDs.

## SVG 栅格范围与交换声明 / SVG image scope

exchange-loss.json按实际image／feImage元素记录局部x／y／width／height、元素及祖先变换、引用摘要和内嵌载荷摘要。内嵌栅格、内嵌SVG与未知引用分别披露，不联网解析外部资源。局部框不等于完整绘制范围；原生素材与效果展开的来源关系保持未知，滤镜存在不证明栅格化。vectorOnly仅表示未发现图像或foreignObject元素；losslessVectorClaimAllowed始终为false，不能据此宣称语义无损往返。可编辑原生工程单独保留。

Actual image/feImage elements expose local geometry, element/ancestor transforms and reference/payload digests. Embedded raster, embedded SVG and unresolved references remain distinct. No external fetch, complete paint-bounds or effect-origin claim. vectorOnly describes observed element structure; losslessVectorClaimAllowed stays false because semantic round-trip fidelity is unverified. Retain the editable native project.
