# 特效操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `effect.catalog.search` | 特效 → 分类/搜索 | scene/character/audio 类别、关键词、VIP 策略 | `catalog` / `media enums`，在线资源走 Harness 查询 | 候选资源 ID、参数定义和授权状态 | 只读 |
| `effect.resource.preview` | 特效卡片 → 预览 | 资源 ID、编辑器版本 | 版本绑定 Adapter | 预览证据绑定资源 | 关闭预览 |
| `effect.resource.download` | 特效卡片 → 下载 | 权益、用途、费用、渠道 | Adapter 下载 → 官方收据登记/预检 | 文件/缓存身份与收据一致 | ambiguous 时查询状态 |
| `effect.timeline.add_scene` | 画面特效 → 添加 | slug、起点、时长、参数 | `timeline add-effect` 场景特效 | effect 轨、范围、材料参数 | 删除 effect 段或快照恢复 |
| `effect.timeline.add_character` | 人物特效 → 添加 | 人物检测适用、slug、范围 | `timeline add-effect` 人物特效 | 目标类型、范围和播放结果 | 删除 effect 段 |
| `effect.audio.add` | 音频 → 音效 | 音效 slug、起点、时长/音量 | `media sfx` 或音频效果命令 | 音频轨、资源和试听 | 删除音频段 |
| `effect.timeline.inspect` | 时间线特效 → 属性 | 草稿路径和目标范围 | `timeline segments/get` + `media materials` | 资源、参数、范围完整 | 只读 |
| `effect.timeline.remove` | 时间线特效 → 删除 | 精确 effect segment ID | `timeline remove` | 目标特效消失，无悬空材料 | 快照恢复 |

## 参数规则

只使用目录声明的参数名和范围。没有显式作用范围时先请求用户或由 WorkflowPlan 给出可审阅范围，不能默认覆盖整片。
