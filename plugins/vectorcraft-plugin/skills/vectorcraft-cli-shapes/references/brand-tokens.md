# 原生品牌 token 与变体更新

VectorCraft 的全局色板是原生品牌色 token。创建 `swatch.new` 时设 `global: true`，通过 `paint.setFill` 的 `swatch` 和明确的 `ids` 将 Logo、字标、画板变体绑定到该色板。`swatch.edit` 修改全局颜色后，原生引擎更新所有关联填充／文字；无关联图标不参与更新。

所有命令属于现有原生 CLI。技能的 `workflow.py` 支持 `swatch.new/edit/list`，不创建同名的新 CLI。以实际加载 SKILL.md 目录定位脚本，单独安装本技能即可首次安装与使用。

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/brand-token-assets.json" --output "$FIRST_DELIVERY"
```

示例保留三个画板：Logo／字标、独立橙色图标、与品牌色关联的另一变体。交付包含 `.vectorcraft`、原生模型、操作回执、素材与导出摘要和交换报告。

修改色板时使用新输出目录及此前保存的原工程摘要；`primary.name` 来自原生创建回执，避免猜测发生重名后的真实色板名称。示例修订计划如下，替换摘要后保存为 JSON，可以显式指定导出配置；省略 exports 时，swatch.edit 修订会核对原 plan.json 摘要并沿用其变体导出清单，不能信任被修改的清单。示例如下：

```json
{
  "expectedProjectSha256": "此前保存的原 project.vectorcraft 摘要",
  "operations": [{
    "command": "swatch.edit",
    "params": {"name": {"$ref": "primary.name"}, "color": "#175cce"}
  }],
  "exports": [
    {"format": "svg", "artboard": 0}, {"format": "png", "artboard": 0},
    {"format": "png", "artboard": 1},
    {"format": "svg", "artboard": 2}, {"format": "png", "artboard": 2}
  ]
}
```

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" "$REVISION_PLAN" \
  --source "$FIRST_DELIVERY" --output "$NEXT_DELIVERY"
```

原生项目重新打开后仍保留关联关系；默认填充、非全局色板、直接写入 RGB 的对象不应被当作关联对象。缺少色板、错误摘要或既有输出目录应停止，不自动重放未知结果。当前验证覆盖 RGB 全局色板、路径及文字关联、两关联画板的 SVG／PNG 更新、独立图标和旧工程不变。其他颜色模型、tint／gradient／spot、跨编辑器色板保真、跨文件消费者与完整创作接受仍须单独验证。

## 工作流执行时依赖守卫

通过 vectorcraft-harness 技能的 `scripts/workflow.py` 执行 `swatch.edit`，或通过该工作流的 `native.command` 调用同一原生命令时，先保存原生修改前检查点，再读取同一会话的修改前后模型。只有显式 `swatch` 引用是消费者，同 RGB 颜色不构成消费关系。非消费者自身属性、对象身份、容器成员顺序和画板范围必须保持。

成功交付在 `manifest.json` 中登记 `brandDependencyReport`，指向已摘要绑定的 `brand-dependencies.json`；每项检查记录消费者 ID、受影响对象 ID、错误依赖边和前后模型摘要。检查点仅用于失败恢复：成功时移除临时检查点、保留摘要并记录 `checkpointRetained: false`；不要把该记录当成可打开的额外交付工程。

发现误改时返回 `brand_dependency_violation`，不发布成功 manifest。读取失败目录的 `failure.json`，按其原始 stage 路径和摘要查验 `brand-dependencies.json` 及检查点；`checkpointRetained: true` 时检查点留在原暂存位置，以避免移动工程破坏绝对素材链接。检查点是色板操作前的中间状态，不自动回写源工程、不自动重放。

色板检查适用于公开工作流的上述色板操作；独立 `commands.py` 完整原生命令入口不会因此新增创作验收承诺。登记素材替换按下节核验；其他颜色模型、外部编辑器及像素质量单独核验。源码候选与固定发行／实际安装验收分开，不以当前分支替代不可变版本。


## 已登记素材的品牌变体替换

`asset.replace` 使用当前源交付 `manifest.json` 中已登记素材的全部实例 ID；`replacement` 用 `--asset replacement=绝对路径` 登记新素材并核验摘要。参见 [替换示例](../examples/brand-asset-revise.json)。在新修订中替换，不能覆盖源工程。

未提供 `exports` 时继承摘要核验后的原变体清单；显式 `exports: []` 只交付原生工程。每次替换前保存检查点，记录原生子树映射、未关联对象属性、层次顺序及画板保全。栅格实例保留 ID；SVG 按真实回执替换子树 ID，并按原生实例边界校正导入尺寸。报告包含 `asset`、`consumerIds`、`replacementIds`、`replacementMapping`、边界失配及错误依赖边。

误改返回 `brand_dependency_violation`，成功清单不会发布；按 `failure.json` 找到原位置检查点和回执。独立原生命令入口的任意 `file.place`／`links.relink` 不自动拥有此登记依赖合同。跨文件消费者、全部素材格式、外部编辑器往返和视觉创作质量仍须分别验收。

Registered `asset.replace` revisions inherit the verified source export list when omitted; explicit empty exports remain native-only. Real consumer subtree mappings, native instance bounds and unrelated object/stacking/artboard preservation are checked before delivery. Raster IDs may remain; SVG subtree IDs follow native replies. Failures retain the checkpoint and receipts without replay. Arbitrary native file commands and cross-file dependencies remain separate.
