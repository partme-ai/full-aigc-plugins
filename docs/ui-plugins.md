# 内容创作插件：UI 与产品线

> 本文件只描述内容创作线（`full-aigc`）。全栈开发线使用同名结构，值为 `full-stack`。

## 产品线

`catalog.json` 的每个插件条目必须声明：

```json
{
  "line": "full-aigc"
}
```

市场按 `line` 分成两个入口：

| 产品线 | 仓库 | 入口 |
| --- | --- | --- |
| 全栈开发 | `full-stack-plugins` | 开发工具、代码质量、研发流程、设计交付、运维面板 |
| 内容创作 | `full-aigc-plugins` | 图像、设计排版、文档、表格演示、音视频、3D、AIGC 平台 |

`Xuanji` 属于内容创作线，但使用独立 `category: "Entertainment"`，不与生产力工具混排。

## 需要界面的插件

判定标准：

```text
需要看、画、拖、排、预览、校对  → MCP Apps UI 插件
纯命令、纯数据、纯审查          → Skills + stdio MCP 插件
```

UI 插件在 catalog 中声明：

```json
{
  "componentTypes": ["ui"],
  "ui": {
    "surface": "editor",
    "icon": "image",
    "availability": "session"
  }
}
```

ZCode 清单由 `scripts/sync-plugin-configs.mjs` 生成，核心字段：

```json
{
  "ui": {
    "surfaces": [{
      "id": "editor",
      "title": { "en-US": "PhotoCraft · Image Editing", "zh-CN": "PhotoCraft · 图片编辑" },
      "icon": "image",
      "server": "photocraft-editor",
      "resourceUri": "ui://photocraft/panel.html",
      "availability": "session"
    }]
  },
  "commands": "commands",
  "mcpServers": {
    "photocraft-editor": {
      "type": "stdio",
      "command": "node",
      "args": ["${ZCODE_PLUGIN_ROOT}/ui/bootstrap.mjs"],
      "cwd": "${ZCODE_PROJECT_DIR}",
      "env": {
        "CRAFT_PANEL_METADATA_FILE": "${ZCODE_PLUGIN_ROOT}/.zcode-plugin/panel-meta.json",
        "CRAFT_WORKSPACE_ROOT": "${ZCODE_PROJECT_DIR}"
      }
    }
  }
}
```

`server` 必须与 `mcpServers` 的键一致；`resourceUri` 必须由该 MCP 服务提供，当前统一为 `ui://<plugin-id>/panel.html`。

## 内容创作线 UI 插件（13）

### Craft（9）

```text
cadcraft     CADCraft · 二维制图      ui://cadcraft/panel.html
deckcraft    DeckCraft · 演示文稿     ui://deckcraft/panel.html
designcraft  DesignCraft · 页面排版   ui://designcraft/panel.html
gridcraft    GridCraft · 电子表格     ui://gridcraft/panel.html
photocraft   PhotoCraft · 图片编辑    ui://photocraft/panel.html
pdfcraft     PdfCraft · PDF 处理      ui://pdfcraft/panel.html
soundcraft   SoundCraft · 音频处理    ui://soundcraft/panel.html
vectorcraft  VectorCraft · 矢量设计   ui://vectorcraft/panel.html
wordcraft    WordCraft · 文档写作     ui://wordcraft/panel.html
```

### 编辑器（4）

```text
effectcraft  EffectCraft · 动态图形   ui://effectcraft/panel.html
figcraft     FigCraft · 设计稿编辑    ui://figcraft/panel.html
filmcraft    FilmCraft · 视频剪辑    ui://filmcraft/panel.html
lightcraft   LightCraft · 照片调色   ui://lightcraft/panel.html
```

每个插件同时生成 `commands/open.md`，ZCode 侧为 `/<plugin-id>:open`。

## PdfCraft 与 PrintCraft

之前把它们当成两个产品是错的。`PrintCraft` 是 `PdfCraft` 的 fork/rebrand：

- 上游：`https://github.com/storytold/pdfcraft`
- `ui/source.lock.json` 记录 `name: pdfcraft`、`repository: full-aigc-plugins/printcraft`、`sourceStatus: fork`
- 插件 id / 仓库已迁移为 `pdfcraft` / `pdfcraft-plugin`；源码 fork 仓库仍是 `full-aigc-plugins/printcraft`

发行 ZIP 的根目录仍是 `printcraft-plugin`，市场用 `archiveRoot` 保持兼容；tag 与运行时资源名暂不重发。

## 生成与校验

```bash
# GitHub 英文
node scripts/sync-plugin-configs.mjs --locale=en --no-version --include-candidates --plugin=photocraft

# AtomGit 中文
node scripts/sync-plugin-configs.mjs --locale=zh-CN --no-version --include-candidates --plugin=photocraft --workspace=/path/to/clone
```

回归测试检查：

- 9 个 UI 插件都有 `ui.surfaces`、匹配的 `mcpServers`、`commands/open.md`；
- `line` 只能是 `full-aigc` 或 `full-stack`；
- 市场条目保留 `line` / `componentTypes`。
