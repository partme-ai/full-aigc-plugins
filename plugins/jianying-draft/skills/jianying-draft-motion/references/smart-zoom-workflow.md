# 交互事件到智能缩放计划

## 数据流

```text
interaction-events/v1
→ 校验录屏摘要与坐标映射
→ 点击去抖和 session 分组
→ 计算安全视口与 reduced-motion 约束
→ smart-zoom-plan/v1
→ 项目帧量化
→ capability 门禁
→ WorkflowPlan / jianying-job/v2
→ 发布 Rust CLI
→ 播放验收
```

事件账本见 [Schema](interaction-events-v1.schema.json) 和 [有效示例](../examples/interaction-events-v1.json)；计划见 [Schema](smart-zoom-plan-v1.schema.json) 和 [有效示例](../examples/smart-zoom-plan-v1.json)。

## 捕获门禁

- 精确声明 screen、window 或 region；记录显示器缩放、捕获区域和窗口偏移。
- 录系统音频、点击和原始录屏分别授权。`keyboard_content_captured` 必须为 `false`。
- 录制前做隐私检查，录制后先人工预览；事件坐标只能是捕获区域内归一化值。
- 账本与录屏用内容 SHA-256 绑定；路径、文件名和窗口标题不能作为素材身份。

## 规划规则

- 分组间隔、去抖、最大缩放和边缘余量是每个计划的显式参数，不沿用研究样例默认值。
- 关键帧时间严格递增、位于片段范围，并量化到项目 FPS；不安全偏移必须阻塞。
- 平移不得露出画布边缘；高频点击需要合并，避免镜头追逐鼠标。
- `reduced_motion` 降低缩放幅度和次数；每个 session 保留人工删除入口。
- 计划不包含 CLI 命令。只有 `timeline.keyframe` 与 `timeline.quantization_report` 为 `supported`，且目标草稿已隔离时，Harness 才能编译执行。

## 验收

结构校验只检查时间、数值和引用。最终至少播放检查聚焦对象、黑边、眩晕、误缩放、字幕遮挡和转场冲突；没有播放证据时不得称智能缩放完成。
