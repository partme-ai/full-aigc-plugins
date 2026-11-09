# 滤镜操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `filter.catalog.search` | 滤镜 → 分类/搜索 | 风格、关键词、画幅、用途、VIP 策略 | `catalog --domain filters` / `media enums filters` | 候选 slug、资源 ID、VIP 状态 | 只读 |
| `filter.resource.preview` | 滤镜卡片 → 预览 | 候选和强度 | 本地代理预览或版本绑定 Adapter | 预览与候选/强度绑定 | 丢弃预览 |
| `filter.resource.download` | 滤镜卡片 → 下载 | 权益、用途和费用 | Adapter 下载 → 官方收据 | 资源身份与收据一致 | ambiguous 时查询 |
| `filter.timeline.apply` | 滤镜 → 添加 | slug、显式范围、强度 | `timeline add-filter` | filter 轨、范围和强度读回 | 删除新增 filter 段 |
| `filter.timeline.replace` | 时间线滤镜 → 替换 | 旧 filter segment、新候选 | 删除旧段后应用新段，单事务/快照 | 仅新滤镜存在 | 恢复旧段快照 |
| `filter.timeline.inspect` | 时间线滤镜 → 属性 | 草稿路径和目标范围 | `timeline segments/get` + materials | slug/resource、强度、范围 | 只读 |
| `filter.timeline.remove` | 时间线滤镜 → 删除 | 精确 segment ID | `timeline remove` | 目标滤镜和孤立材料清理 | 快照恢复 |

## 选择规则

优先保护肤色、商品色和品牌色。需要精确曝光、对比度、饱和度、色温或 HSL 时转入调节动线，并重新检查 capability。
