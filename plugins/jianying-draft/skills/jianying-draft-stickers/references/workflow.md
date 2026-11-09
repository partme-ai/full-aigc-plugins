# 贴纸操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `sticker.catalog.search` | 贴纸 → 分类/搜索 | 关键词、类别、风格、画幅、用途 | Harness 原生资源查询与筛选 | 保存候选、入选/拒绝理由 | 只读 |
| `sticker.resource.preview` | 贴纸卡片 → 预览 | 候选资源 ID、当前版型 | 版本绑定 Adapter 预览 | 预览证据绑定资源 ID | 关闭预览 |
| `sticker.resource.download` | 贴纸卡片 → 下载 | 权益、用途、渠道、费用上限 | Adapter 下载 → `media official register/preflight` | 本地文件哈希与官方收据 | ambiguous 时查询，不重复下载 |
| `sticker.timeline.add` | 贴纸 → 添加到时间线 | 资源 ID、起点、时长、位置、缩放、旋转 | `media add-sticker` | sticker 轨、材料 ID、范围和变换读回 | `timeline remove` |
| `sticker.timeline.move` | 时间线贴纸 → 移动 | segment ID、新起点 | `timeline move` / `timeline set` | 范围未越界 | 恢复原起点 |
| `sticker.timeline.duplicate` | 时间线贴纸 → 复制 | segment ID、目标轨/位置 | `timeline duplicate` 后移动 | 新 ID、独立材料状态 | 删除副本 |
| `sticker.timeline.remove` | 时间线贴纸 → 删除 | 精确 segment ID、共享材料关系 | `timeline remove` | 无片段和悬空材料 | 快照恢复 |
| `sticker.timeline.inspect` | 时间线贴纸 → 属性 | 草稿和 segment ID | `timeline get` + `media material` | 资源、范围、变换完整 | 只读 |

## 筛选与布局

先排除授权和版型不满足的候选，再按语义匹配、风格和节奏排序。贴纸不得遮挡字幕安全区、主体面部、商品关键信息或品牌声明；同屏贴纸数量由创作简报约束。
