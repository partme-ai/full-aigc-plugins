# 模板操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `template.library.inspect` | 模板 → 本地模板库 | 模板根或草稿路径 | `template list` / `template inspect` | 清单、轨道、材料和 schema | 只读 |
| `template.library.save` | 草稿 → 保存为模板 | 草稿通过验证、模板名安全 | `template save` | 独立模板、manifest 和材料完整 | 删除新模板条目 |
| `template.library.apply` | 模板 → 应用 | 画幅/fps、目标名、输出根 | `template apply` | 新草稿独立、ID 重建、材料可用 | 删除新草稿 |
| `template.draft.duplicate` | 模板草稿 → 创建副本 | 新名称和目标根 | `template duplicate` | 副本 ID、路径和结构 | 删除副本 |
| `template.content.replace_text` | 模板 → 替换文字 | 轨道名、索引、文案 | `template replace-text` | 精确文案读回 | 恢复原文案 |
| `template.content.replace_material` | 模板 → 替换素材 | 新素材探测、name 或 track/index 唯一 | `template replace-material` | 新材料路径、时长和引用 | 恢复原素材 |
| `template.track.import` | 模板/子草稿 → 导入轨道 | 来源草稿、轨道、插入位置 | `template import-track` | 轨道和材料 ID 无冲突 | 删除导入轨道或快照恢复 |
| `template.preset.apply` | 文本 → 样式预设 | preset schema、目标字幕集合 | `template make-preset` / `template apply-preset` | 每个目标样式读回 | 恢复应用前样式 |
| `template.official.acquire` | 模板 → 官方模板 | 候选、画幅、用途、权益 | Harness 预览/下载/收据 → Adapter 应用 | 模板身份、输出草稿和冷重开 | 删除输出；ambiguous 查询状态 |

## 冲突处理

画幅、fps、字体或素材许可不匹配时先返回冲突列表。除非用户批准可解释转换，否则不得拉伸画面、替换字体或删除缺失轨道来强行套用。
