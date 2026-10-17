# 中文文字创建与原生定点修订

本技能自带 `examples/chinese-text.json`，在 macOS arm64 上使用已安装的 `Songti SC` 字体创建中文标题和独立英文页脚。以实际加载的 `SKILL.md` 所在绝对目录为 `SKILL_DIR`，无需兄弟技能：

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/chinese-text.json" --output "$FIRST_DELIVERY"
```

示例保留可编辑 `.vectorcraft`，并导出 Unicode SVG 和 PNG。字体名称属于工程依赖，不表示 SVG 内嵌字体；其他机器打开 SVG 或原生工程仍需相同字体或明确批准的替代字体。工作流在保存前调用原生 `text.fonts`，任何 missing 字体都停止交付，成功清单记录 fontDependencies；仍需检查实际字形，字体查询与画面验收分开报告。

## 只修改指定文字

将以下 JSON 的 expectedProjectSha256 替换为此前单独保存的原工程摘要，另存为修订计划，使用本技能 workflow.py 的 `--source "$FIRST_DELIVERY"` 和新的 `--output` 执行：

```json
{
  "expectedProjectSha256": "<原 project.vectorcraft 的 SHA-256>",
  "operations": [
    {"command": "text.setText", "params": {
      "id": {"$ref": "headline.id"}, "text": "品牌焕新"
    }}
  ],
  "exports": [
    {"format": "png", "artboard": 0},
    {"format": "svg", "artboard": 0}
  ]
}
```

此工作流要求显式 id 或 ids，不沿用隐式选择。未知对象、空目标列表、同时指定 id 和 ids、非法参数或非字符串文字均停止，失败不发布成功交付。

`text.setText` 是原生整段替换，保留第一个文本 run 的样式；多样式段落会合并为首段样式。需要保留富文本分段样式时，先查询原生范围编辑能力并使用对应公开 CLI，不能把本入口当作无损富文本替换。

验收应同时核对原生 Unicode 内容与首样式、SVG 文本和字体声明、同长度中文词组的实际不同字形、无关页脚和旧工程字节。当前证据覆盖此单一样式案例，未证明全部 CJK 字体、复杂排版、跨机器字体保真或人工创作接受。
