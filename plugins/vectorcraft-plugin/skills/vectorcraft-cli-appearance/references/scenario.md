# 配色与外观操作指南

## 目标与前置

修改品牌色、填充描边、透明与外观变体。按稳定对象/色板 ID 改色；保留无关对象，区分 RGB/CMYK 和视觉效果的格式差异。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands` 返回 JSON 参数目录；`run --in <工程> --cmd <id> --params <JSON> ... --export <新工程.vectorcraft>`，同批次解析对象 ID；convert 按扩展名输出。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `recolor.colors` | Artwork Colors |
| `recolor.apply` | Recolor Artwork |
| `recolor.reduce` | Reduce Colors |
| `recolor.randomize` | Randomize Colors |
| `paint.setFill` | Fill |
| `paint.setStroke` | Stroke |
| `paint.swap` | Swap Fill and Stroke |
| `paint.default` | Default Fill and Stroke |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 91 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `appearance` — 16

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `appearance.addFill` | Add New Fill | `describe appearance.addFill` |
| `appearance.addStroke` | Add New Stroke | `describe appearance.addStroke` |
| `appearance.clear` | Clear Appearance | `describe appearance.clear` |
| `appearance.reduceToBasic` | Reduce to Basic Appearance | `describe appearance.reduceToBasic` |
| `appearance.setItem` | Appearance Item | `describe appearance.setItem` |
| `appearance.removeItem` | Remove Item | `describe appearance.removeItem` |
| `appearance.addEffect` | Add Effect | `describe appearance.addEffect` |
| `appearance.duplicateItem` | Duplicate Item | `describe appearance.duplicateItem` |
| `appearance.moveItem` | Reorder Appearance Item | `describe appearance.moveItem` |
| `appearance.copyFrom` | Eyedropper | `describe appearance.copyFrom` |
| `appearance.setActiveItem` | Select Appearance Item | `describe appearance.setActiveItem` |
| `appearance.showAllHidden` | Show All Hidden Attributes | `describe appearance.showAllHidden` |
| `appearance.targetContents` | Target Contents | `describe appearance.targetContents` |
| `appearance.transfer` | Move Appearance | `describe appearance.transfer` |
| `appearance.setNewArtBasic` | New Art Has Basic Appearance | `describe appearance.setNewArtBasic` |
| `appearance.newArt` | New Art Appearance | `describe appearance.newArt` |

### `paint` — 22

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `paint.setFill` | Fill | `describe paint.setFill` |
| `paint.setStroke` | Stroke | `describe paint.setStroke` |
| `paint.swap` | Swap Fill and Stroke | `describe paint.swap` |
| `paint.default` | Default Fill and Stroke | `describe paint.default` |
| `paint.toggleActive` | Toggle Fill/Stroke Focus | `describe paint.toggleActive` |
| `paint.none` | None | `describe paint.none` |
| `paint.editGradient` | Gradient | `describe paint.editGradient` |
| `paint.setGradientGeom` | Gradient Vector | `describe paint.setGradientGeom` |
| `paint.sampleColor` | Sample Color | `describe paint.sampleColor` |
| `paint.invert` | Invert | `describe paint.invert` |
| `paint.complement` | Complement | `describe paint.complement` |
| `paint.lastColor` | Apply Last Color | `describe paint.lastColor` |
| `paint.lastGradient` | Apply Last Gradient | `describe paint.lastGradient` |
| `paint.recent` | Recent Colors | `describe paint.recent` |
| `paint.proxies` | Fill and Stroke | `describe paint.proxies` |
| `paint.freeform.addPoint` | Add Freeform Point | `describe paint.freeform.addPoint` |
| `paint.freeform.setPoint` | Edit Freeform Point | `describe paint.freeform.setPoint` |
| `paint.freeform.deletePoint` | Delete Freeform Point | `describe paint.freeform.deletePoint` |
| `paint.freeform.addLine` | Add Freeform Line | `describe paint.freeform.addLine` |
| `paint.freeform.splitLine` | Split Freeform Line | `describe paint.freeform.splitLine` |
| `paint.freeform.selectPoint` | Select Freeform Point | `describe paint.freeform.selectPoint` |
| `paint.freeform.get` | Freeform Gradient | `describe paint.freeform.get` |

### `recolor` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `recolor.colors` | Artwork Colors | `describe recolor.colors` |
| `recolor.apply` | Recolor Artwork | `describe recolor.apply` |
| `recolor.reduce` | Reduce Colors | `describe recolor.reduce` |
| `recolor.randomize` | Randomize Colors | `describe recolor.randomize` |

### `stroke` — 10

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `stroke.set` | Stroke Options | `describe stroke.set` |
| `stroke.setAdvanced` | Stroke Options | `describe stroke.setAdvanced` |
| `stroke.widthProfile.add` | Add to Profiles | `describe stroke.widthProfile.add` |
| `stroke.widthProfile.delete` | Delete Profile | `describe stroke.widthProfile.delete` |
| `stroke.widthProfile.reset` | Reset Profiles | `describe stroke.widthProfile.reset` |
| `stroke.widthProfile.list` | Width Profiles | `describe stroke.widthProfile.list` |
| `stroke.widthPoint.set` | Width Point | `describe stroke.widthPoint.set` |
| `stroke.widthPoint.remove` | Delete Width Point | `describe stroke.widthPoint.remove` |
| `stroke.widthPoint.copy` | Copy Width Point | `describe stroke.widthPoint.copy` |
| `stroke.widthProfile.set` | Width Profile | `describe stroke.widthProfile.set` |

### `swatch` — 22

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `swatch.new` | New Swatch | `describe swatch.new` |
| `swatch.delete` | Delete Swatch | `describe swatch.delete` |
| `swatch.newGroup` | New Color Group | `describe swatch.newGroup` |
| `swatch.duplicate` | Duplicate Swatch | `describe swatch.duplicate` |
| `swatch.sortByName` | Sort by Name | `describe swatch.sortByName` |
| `swatch.edit` | Swatch Options | `describe swatch.edit` |
| `swatch.list` | Swatches | `describe swatch.list` |
| `swatch.move` | Move Swatch | `describe swatch.move` |
| `swatch.addUsedColors` | Add Used Colors | `describe swatch.addUsedColors` |
| `swatch.unused` | Select All Unused | `describe swatch.unused` |
| `swatch.merge` | Merge Swatches | `describe swatch.merge` |
| `swatch.ungroup` | Ungroup Color Group | `describe swatch.ungroup` |
| `swatch.sortByKind` | Sort by Kind | `describe swatch.sortByKind` |
| `swatch.spotOptions` | Spot Colors | `describe swatch.spotOptions` |
| `swatch.editGroup` | Edit Color Group | `describe swatch.editGroup` |
| `swatch.setSpot` | Spot Color | `describe swatch.setSpot` |
| `swatch.library.list` | Swatch Libraries | `describe swatch.library.list` |
| `swatch.library.get` | Swatch Library | `describe swatch.library.get` |
| `swatch.library.add` | Add to Swatches | `describe swatch.library.add` |
| `swatch.resetDefaults` | Default Swatches | `describe swatch.resetDefaults` |
| `swatch.library.save` | Save Swatch Library… | `describe swatch.library.save` |
| `swatch.library.load` | Other Library… | `describe swatch.library.load` |

### `transparency` — 17

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `transparency.set` | Transparency | `describe transparency.set` |
| `transparency.makeOpacityMask` | Make Opacity Mask | `describe transparency.makeOpacityMask` |
| `transparency.releaseOpacityMask` | Release Opacity Mask | `describe transparency.releaseOpacityMask` |
| `transparency.disableOpacityMask` | Disable Opacity Mask | `describe transparency.disableOpacityMask` |
| `transparency.enableOpacityMask` | Enable Opacity Mask | `describe transparency.enableOpacityMask` |
| `transparency.unlinkOpacityMask` | Unlink Opacity Mask | `describe transparency.unlinkOpacityMask` |
| `transparency.linkOpacityMask` | Link Opacity Mask | `describe transparency.linkOpacityMask` |
| `transparency.setOpacityMask` | Opacity Mask Options | `describe transparency.setOpacityMask` |
| `transparency.toggleNewMasksClipping` | New Opacity Masks Are Clipping | `describe transparency.toggleNewMasksClipping` |
| `transparency.toggleNewMasksInverted` | New Opacity Masks Are Inverted | `describe transparency.toggleNewMasksInverted` |
| `transparency.opacityMaskInfo` | Opacity Mask Info | `describe transparency.opacityMaskInfo` |
| `transparency.info` | Transparency Info | `describe transparency.info` |
| `transparency.togglePageIsolatedBlending` | Page Isolated Blending | `describe transparency.togglePageIsolatedBlending` |
| `transparency.togglePageKnockoutGroup` | Page Knockout Group | `describe transparency.togglePageKnockoutGroup` |
| `transparency.editOpacityMask` | Edit Opacity Mask | `describe transparency.editOpacityMask` |
| `transparency.stopEditingOpacityMask` | Stop Editing Opacity Mask | `describe transparency.stopEditingOpacityMask` |
| `transparency.viewOpacityMask` | View Opacity Mask | `describe transparency.viewOpacityMask` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
