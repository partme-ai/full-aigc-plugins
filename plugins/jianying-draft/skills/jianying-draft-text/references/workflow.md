# 文本操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `text.create.default` | 文本 → 新建文本 → 默认文本 | 文案、起点、时长、轨道 | `captions add` 写入独立文字轨 | `captions get/list` + 冷重开 | `timeline remove` |
| `text.create.template` | 文本 → 文字模板 | 查询词、用途、版型、资源权益 | Harness 候选 → 预览/下载 → 官方收据 → Adapter 应用 | 资源 ID、文字内容、时间范围 | 删除段并恢复快照 |
| `text.style.base` | 文本 → 基础样式 | segment ID、字体/字号/颜色 | `captions style` | 读回基础样式，冷重开检查字体 | 恢复原样式快照 |
| `text.style.ranges` | 文本 → 局部样式 | UTF-16 范围、文本未变 | `captions style-ranges` | 范围不越界且读回一致 | 恢复原 ranges |
| `text.decorate.bubble` | 文本 → 气泡/花字 | 目录 slug 或显式资源 ID、授权 | `captions bubble` | 材料 `text_shape` 与文字段关联 | 清除或恢复旧资源 |
| `text.animate.segment` | 文本 → 动画 | intro/outro、时长、剪映/CapCut 命名空间 | `captions animation` | 动画材料、持续时间、播放检查 | 恢复旧动画 |
| `text.edit.content` | 文本 → 编辑内容 | 精确 segment ID、品牌保护规则 | `captions set` | 文案精确读回 | 恢复原文案 |
| `text.remove.segment` | 时间线文字 → 删除 | 精确 segment ID | `timeline remove` | 段和孤立材料均处理 | 快照恢复 |

## 选择规则

普通标题优先使用本地可表达样式；只有明确需要官方模板外观时才进入资源下载动线。字幕文件、ASR 对齐和多语言字幕不在本技能内展开。

## GUI 门禁

文字模板的预览/下载/应用依赖当前版本 Adapter。`media.official_resource_apply` 未 supported 时，只能给候选与预览计划，不能把 `captions add` 冒充模板应用。
