# 插件命名规范（AIGC）

## 规则

`displayName` 采用 **`代号 · 领域`** 两段式：

| 段 | 作用 | 示例 |
|---|---|---|
| 代号 | 产品识别与检索 | `PhotoCraft`、`FilmCraft`、`GridCraft` |
| 领域 | 中文用户一眼知道“干什么” | `图片编辑`、`视频剪辑`、`电子表格` |

约定：

1. **代号在前、领域在后**，中间固定 ` · `；不再使用任何括号对标，如 `WordCraft · 文档写作`。
2. 不使用 `Use`、`RC`、`类` 后缀；候选状态只保留在 `catalog.json` 的 `status` 字段，不进展示文案。
3. 英文同构：`Product · Domain`，同样不加对标括号。
4. `id`、`version`、安装命令、技能名一律不随语言变化。
5. **渠道单语**：GitHub 产物全英文，AtomGit/国内产物全中文；ZCode 的 `displayName_i18n` 只写当前渠道语言，不再混排。

## 双语事实源

`catalog.json` 中：

```json
{
  "displayName": "PhotoCraft · Image Editing",
  "shortDescription": "...",
  "description": "...",
  "localizations": {
    "zh-CN": { "displayName": "PhotoCraft · 图片编辑", "shortDescription": "...", "description": "..." }
  }
}
```

扁平字段只服务 GitHub 英文渠道；`localizations.zh-CN` 只服务 AtomGit/国内中文渠道。构建时用 `--locale=en|zh-CN` 二选一，产物中不允许出现另一种语言。

## 渠道语言矩阵

| 字段 | GitHub（英文） | AtomGit（中文） |
|---|---|---|
| `displayName` | `Product · Domain` | `代号 · 领域` |
| `shortDescription` | 英文一句话 | 中文一句话 |
| `description` | 英文 2–4 句 | 中文 2–4 句 |
| `displayName_i18n` | `{ "en": ... }` | `{ "zh-CN": ... }` |
| Codex / ZCode / Kimi / Claude 清单 | 全部英文 | 全部中文 |

`name` / `id` / `version` / 安装命令 / 技能名两个渠道完全一致；代号、品牌名、URL 保持原文，不算混排。

## 校验

```bash
node --test scripts/plugin-naming.test.mjs
node scripts/verify-channel-parity.mjs
```

命名 lint 会拒绝：缺中文、缺 ` · `、代号不在前、含 `对标`/`alternative`、含 `Use`/`RC`/`类）`、超长（>60 字符）、中英文名相同、英文含 CJK、中文缺 CJK、同字段中英混排、`shortDescription` 与 `description` 职责重叠、两渠道 id/version 不一致。

生成两套清单：

```bash
node scripts/sync-plugin-configs.mjs --locale=en
node scripts/sync-plugin-configs.mjs --locale=zh-CN --workspace=<AtomGit checkout>
```
