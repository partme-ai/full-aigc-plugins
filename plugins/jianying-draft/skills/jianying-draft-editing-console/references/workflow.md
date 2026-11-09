# 剪辑控制台操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `console.timeline.inspect` | 时间线 → 轨道/片段 | 草稿路径 | `timeline show/tracks/segments/get` | 轨道、segment、材料和范围一致 | 只读 |
| `console.segment.split` | 工具栏 → 分割 | segment ID、绝对切点、帧量化 | `timeline split` | 两段连续、无重叠/空段 | 快照恢复 |
| `console.segment.trim` | 片段边缘 → 裁剪 | segment ID、源窗口、句柄 | `timeline trim` / `timeline set` | 源/时间线范围合法 | 恢复原窗口 |
| `console.segment.move` | 片段 → 拖动 | segment ID、绝对目标或偏移、吸附策略 | `timeline move` / `move-all` | 起点读回、无非法重叠 | 反向移动或快照 |
| `console.segment.duplicate` | 工具栏/右键 → 复制 | segment ID、目标轨 | `timeline duplicate` | 新 ID、材料独立性 | 删除副本 |
| `console.segment.remove` | 工具栏/右键 → 删除 | 精确 segment ID、材料共享关系 | `timeline remove` | 片段消失、引用完整 | 快照恢复 |
| `console.track.add` | 时间线 → 添加轨道 | 轨道类型和名称 | `timeline add-track` | 新轨道 ID/类型 | 删除空轨或恢复快照 |
| `console.keyframe.add` | 工具栏 → 关键帧 | 属性、绝对时间、值、帧率 | `timeline keyframe` 单个或 JSONL | 点位、属性、量化漂移 | 恢复关键帧集合 |
| `console.session.undo` | 工具栏 → 撤销 | 插件拥有会话、状态可回读 | `runtime controls invoke timeline.session.undo` | 前后状态/草稿差分 | 必要时 redo；不能恢复并行编辑 |
| `console.session.redo` | 工具栏 → 重做 | 插件拥有会话、可重做状态 | `runtime controls invoke timeline.session.redo` | 状态回读 | undo |
| `console.session.snap` | 工具栏 → 吸附/磁吸/联动 | 精确版本、当前布尔状态 | `runtime controls set` 对应 semantic ID | 布尔状态回读 | 写回原状态 |
| `console.audio.record` | 工具栏 → 录音 | 麦克风权限、目标轨、明确批准 | `runtime controls invoke timeline.audio.record` | 录音任务、文件和轨道片段 | 停止并删除未接受录音 |
| `console.view.zoom` | 时间线右侧 → 缩放/适配 | 精确版本、当前视图状态 | `runtime controls invoke/set` | 缩放/适配状态回读 | 恢复原视图 |

## 执行路由

分割、裁剪、移动、删除、关键帧等优先编译为 Rust 草稿协议命令。撤销/重做、磁吸、吸附、联动、录音和缩放属于会话状态，只能使用 Control Catalog 中精确版本且具备 readback 的语义动作。

## 覆盖审计

Surface Inventory 中的下拉菜单、右键菜单、手势和 unresolved 入口必须保留为 coverage gap；未枚举子动作时不得宣称“每个按钮均已覆盖”。
