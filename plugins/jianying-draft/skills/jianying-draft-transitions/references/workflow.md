# 转场工作流参考

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `transition.catalog.search` | 转场 → 分类/搜索 | 叙事目的、关键词、VIP 策略 | `catalog --domain transitions` / `media enums transitions` | 候选 slug、资源 ID、授权 | 只读 |
| `transition.resource.preview` | 转场卡片 → 预览 | 候选、编辑器版本、相邻片段 | 本地预览或版本绑定 Adapter | 预览绑定资源和切点 | 丢弃预览 |
| `transition.resource.download` | 转场卡片 → 下载 | 权益、用途、费用 | Adapter 下载 → 官方收据 | 资源身份和收据一致 | ambiguous 时查询 |
| `transition.timeline.apply` | 两片段切点 → 添加转场 | 出段/入段相邻、handle、持续时间 | `timeline transition` | transition 材料、出段绑定、时长 | 清除转场或快照恢复 |
| `transition.timeline.replace` | 时间线转场 → 替换 | 旧转场和新候选 | 同一事务替换 transition | 仅新资源存在、播放无黑帧 | 恢复旧资源 |
| `transition.timeline.remove` | 时间线转场 → 删除 | 出段 segment ID | 清除 transition 或恢复无转场段 | 硬切恢复、无孤立材料 | 快照恢复 |
| `transition.timeline.inspect` | 时间线转场 → 属性 | 草稿与出段 ID | `timeline get` + materials | 资源、时长、切点和相邻关系 | 只读 |

## 执行路由

固定目录资源使用 Rust `timeline transition`；需要在线预览/下载的官方转场先经过 Adapter 与收据。任何未验证的资源身份或非相邻片段均不得应用。

## 选择原则

- 叙事视频默认硬切；章节边界才考虑轻量转场。
- 卡点视频根据已探测音频节拍选择持续时间。
- resource catalogue 的会员或商业限制必须保留，不能因资源缓存存在而忽略。

## 边界检查

- 出段必须存在后继段。
- 转场窗口不能超过片段或源素材可用 handle。
- 变速、裁剪和量化后重新计算窗口。
- 不支持的 edge policy 直接失败，不静默改成另一效果。

## 恢复

资源缺失、版本不兼容或播放黑帧时恢复 mutation snapshot，保留无转场版本，再选择已验证资源或硬切。
