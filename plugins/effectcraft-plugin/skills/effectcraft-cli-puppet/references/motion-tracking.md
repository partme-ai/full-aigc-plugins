# 镜头跟踪首用 / Motion tracking first use

先核对输入能否被固定原生 CLI 解码，再建立跟踪点；命令返回的计划帧数不能证明分析完成。当前原生 0.2.0 已验证普通 H.264 High／yuv420p 的位置跟踪。libx264 的 `-crf 0` 会生成含 transform bypass 的无损编码，当前解码器不支持；导入元数据成功可能仍无法产生源像素。

Check actual source pixels before configuring a tracker. Native 0.2.0 has passed position tracking with ordinary H.264 High / yuv420p. The lossless transform-bypass stream produced by libx264 `-crf 0` is unsupported. Metadata import alone does not prove decoding. This case does not establish acceptance of every codec or tracking mode.

## 输入与预览 / Input and preview

使用 effectcraft-harness 技能的 `scripts/cli.py`，首次调用自动安装锁定 CLI。用 `file.import` 回执取得素材 item，再通过 `layer.addItem` 回执取得源 layer。检查 `info` 的宽高、帧率、时长、合成和图层，渲染至少两个已知时间点，核对源纹理、位置和尺寸。不能只检查图片非空或“有颜色”：已有图形透过缺失的视频图层出现时会误报成功。已有独立解码工具可提供参考帧，但其成功不能替代原生预览。

Use this skill's own launcher and actual native receipt IDs. Inspect footage and render at least two known times. Compare the expected source texture, placement and dimensions; a colored picture may show unrelated layers beneath an undecoded video. An independently decoded reference cannot replace the native preview.

不覆盖原素材，不因解码失败自动转码。确需受支持代理时，在授权范围内另存派生素材，记录原素材与代理摘要、编码参数及对应关系，再验证原生解码。

Preserve the original asset. An authorized proxy is a separate derivative with source/proxy hashes and encoding parameters; validate native decoding again.

## 配置、分析与实际结果 / Configure and verify

本技能携带 `examples/tracking-create.json` 和 `examples/tracking-reopen.json`。创建模板绑定 `shot` 输入，其中 128×96、12fps、中心 [20,40] 是示例条件。真实镜头按实际素材重设合成、中心、搜索窗口、起止时间和目标 layer，不能盲用模板坐标。

The local examples bind `shot`. Their composition and feature coordinates are fixture settings; adjust them to the actual footage and target.

顺序：`track.new` → `track.setPoint` → `track.analyze`（`wait:true`）→ `track.status` → `track.apply` → 保存 → 独立进程重开。命令绑定实际源 layer，目标由 `track.new.target` 指定。

Configure, analyze with `wait:true`, inspect status, apply, save and reopen independently. Bind the source layer explicitly and set the intended target.

- `track.analyze.frames` 是请求步数，`running:false` 也不能独立证明成功，完成后的 `progress` 可以为 null。
- 从 `track.status.tracker.points[].keys` 核对实际关键帧、点位置和区间。覆盖12帧的测试产生12个实际关键帧；0个关键帧属于失败。
- 应用后通过 `get` 检查目标 `transform/position` 的 keys 和多个时间点 value；核对其他文字、透明度、图形及原工程摘要保全。
- 未得到预期结果时检查源像素、配置和原生回执，不降低验收帧数，不盲目重放编辑。

`frames` is planned work; stopped execution and null finished progress are insufficient. Inspect actual point keys and positions, then target position keys and evaluated values after reopening. Zero keys is failure. Preserve unrelated content and the original project; diagnose rather than weaken expectations or replay edits blindly.

## 验收边界 / Acceptance boundary

固定安装用例验证独立空缓存安装、12帧纹理视频、独立参考帧、位置跟踪、实际关键帧、原生重开、终点位置和非目标保全。摄像机求解、变形稳定、每种编码、模型、GUI和全部22条跟踪命令完整验收仍需各自证据。

The fixed-installed case covers cold installation, textured footage, reference pixels, position tracking, actual keys, native reopen, endpoints and preservation. Camera solving, warp stabilization, every codec, models, GUI and all 22 tracking commands require separate evidence.
