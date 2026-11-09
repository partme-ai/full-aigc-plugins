# 调节操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `adjustment.inspect.parameters` | 调节 → 当前参数 | 精确编辑器版本、目标片段/范围 | `runtime controls list/get` + Adapter readback | 参数名、绝对值、作用范围 | 只读 |
| `adjustment.basic.set` | 调节 → 基础 | exposure/brightness/contrast 等支持项、绝对目标值 | supported 草稿协议；否则版本绑定 Runtime/Accessibility Adapter | 参数回读 + 前后画面 | 恢复原参数快照 |
| `adjustment.color.set` | 调节 → 色彩 | saturation/temperature/tint 等支持项 | 同上，禁止转换为滤镜 | 参数回读、肤色和品牌色比较 | 恢复原参数 |
| `adjustment.detail.set` | 调节 → 细节 | sharpen/clarity/fade/vignette/grain 等支持项 | 同上 | 参数与噪点/边缘画面检查 | 恢复原参数 |
| `adjustment.scope.copy` | 调节 → 复制到片段/全片 | 来源参数、目标片段集合、排除片段 | 版本绑定 Adapter 批量绝对写入 | 每个目标逐项回读 | 逐目标恢复 |
| `adjustment.reset.parameters` | 调节 → 重置 | 当前参数快照、明确目标范围 | supported reset 动作或 Adapter | 全部目标参数回到基线 | 恢复重置前快照 |

## 执行路由

只有控制目录返回稳定语义 ID、精确版本匹配、绝对参数合同和应用后 readback 时才执行。任何只有视觉位置、相对拖动或未知刻度的入口均保持 `BLOCKED`。

## 验证与恢复

验证同时要求参数读回和画面比较。Adapter 超时属于 ambiguous：先检查当前参数和草稿，不自动再拖一次滑杆；恢复使用应用前绝对值或草稿快照。
