# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 211 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `attributes` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `attributes.info` | Attributes | `describe attributes.info` |
| `attributes.set` | Attributes | `describe attributes.set` |

### `brush` — 10

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `brush.list` | Brushes | `describe brush.list` |
| `brush.get` | Brush Definition | `describe brush.get` |
| `brush.apply` | Apply Brush | `describe brush.apply` |
| `brush.remove` | Remove Brush Stroke | `describe brush.remove` |
| `brush.setCurrent` | Current Brush | `describe brush.setCurrent` |
| `brush.new` | New Brush… | `describe brush.new` |
| `brush.delete` | Delete Brush | `describe brush.delete` |
| `brush.duplicate` | Duplicate Brush | `describe brush.duplicate` |
| `brush.options` | Brush Options… | `describe brush.options` |
| `brush.freehand` | Paintbrush | `describe brush.freehand` |

### `clipboard` — 10

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `clipboard.exportSvg` | Clipboard as SVG | `describe clipboard.exportSvg` |
| `clipboard.importSvg` | Load SVG into Clipboard | `describe clipboard.importSvg` |
| `clipboard.conflicts` | Swatch Conflicts | `describe clipboard.conflicts` |
| `clipboard.exportPng` | Clipboard as PNG | `describe clipboard.exportPng` |
| `clipboard.exportPdf` | Clipboard as PDF | `describe clipboard.exportPdf` |
| `clipboard.exportText` | Clipboard as Text | `describe clipboard.exportText` |
| `clipboard.flavours` | Clipboard Formats | `describe clipboard.flavours` |
| `clipboard.importImage` | Load Image into Clipboard | `describe clipboard.importImage` |
| `clipboard.importText` | Load Text into Clipboard | `describe clipboard.importText` |
| `clipboard.importPdf` | Load PDF into Clipboard | `describe clipboard.importPdf` |

### `color` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `color.harmony` | Color Guide | `describe color.harmony` |
| `color.loadProfile` | Load Color Profile… | `describe color.loadProfile` |
| `color.convert` | Convert Color | `describe color.convert` |
| `color.gamutCheck` | Gamut Warning | `describe color.gamutCheck` |
| `color.plates` | Plates | `describe color.plates` |

### `colorTheme` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `colorTheme.list` | Color Themes | `describe colorTheme.list` |
| `colorTheme.save` | Save Theme | `describe colorTheme.save` |
| `colorTheme.delete` | Delete Theme | `describe colorTheme.delete` |
| `colorTheme.addToSwatches` | Add to Swatches | `describe colorTheme.addToSwatches` |

### `command` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `command.batch` | Batch | `describe command.batch` |

### `edit` — 26

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `edit.undo` | Undo | `describe edit.undo` |
| `edit.redo` | Redo | `describe edit.redo` |
| `edit.cut` | Cut | `describe edit.cut` |
| `edit.copy` | Copy | `describe edit.copy` |
| `edit.paste` | Paste | `describe edit.paste` |
| `edit.pasteInFront` | Paste in Front | `describe edit.pasteInFront` |
| `edit.pasteInBack` | Paste in Back | `describe edit.pasteInBack` |
| `edit.pasteInPlace` | Paste in Place | `describe edit.pasteInPlace` |
| `edit.pasteOnAllArtboards` | Paste on All Artboards | `describe edit.pasteOnAllArtboards` |
| `edit.clear` | Clear | `describe edit.clear` |
| `edit.duplicate` | Duplicate | `describe edit.duplicate` |
| `edit.colors.invert` | Invert Colors | `describe edit.colors.invert` |
| `edit.colors.toCMYK` | Convert to CMYK | `describe edit.colors.toCMYK` |
| `edit.colors.toGrayscale` | Convert to Grayscale | `describe edit.colors.toGrayscale` |
| `edit.colors.toRGB` | Convert to RGB | `describe edit.colors.toRGB` |
| `edit.colors.saturate` | Saturate… | `describe edit.colors.saturate` |
| `edit.colors.adjustBalance` | Adjust Color Balance… | `describe edit.colors.adjustBalance` |
| `edit.colors.blendFrontToBack` | Blend Front to Back | `describe edit.colors.blendFrontToBack` |
| `edit.colors.blendHorizontally` | Blend Horizontally | `describe edit.colors.blendHorizontally` |
| `edit.colors.blendVertically` | Blend Vertically | `describe edit.colors.blendVertically` |
| `edit.colorSettings` | Color Settings… | `describe edit.colorSettings` |
| `edit.assignProfile` | Assign Profile… | `describe edit.assignProfile` |
| `edit.colors.overprintBlack` | Overprint Black… | `describe edit.colors.overprintBlack` |
| `edit.findReplace` | Find and Replace… | `describe edit.findReplace` |
| `edit.findNext` | Find Next | `describe edit.findNext` |
| `edit.pasteWithoutFormatting` | Paste without Formatting | `describe edit.pasteWithoutFormatting` |

### `effect` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `effect.apply` | Apply Effect | `describe effect.apply` |
| `effect.list` | Effects | `describe effect.list` |
| `effect.remove` | Remove Effect | `describe effect.remove` |
| `effect.setParams` | Effect Options | `describe effect.setParams` |
| `effect.expandAppearance` | Expand Appearance | `describe effect.expandAppearance` |
| `effect.duplicate` | Duplicate Effect | `describe effect.duplicate` |
| `effect.move` | Move Effect | `describe effect.move` |

### `eyedropper` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `eyedropper.setOptions` | Eyedropper Options | `describe eyedropper.setOptions` |

### `flattener` — 6

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `flattener.presets.list` | Transparency Flattener Presets | `describe flattener.presets.list` |
| `flattener.presets.save` | Save Transparency Flattener Preset | `describe flattener.presets.save` |
| `flattener.presets.delete` | Delete Transparency Flattener Preset | `describe flattener.presets.delete` |
| `flattener.presets.import` | Import Transparency Flattener Presets | `describe flattener.presets.import` |
| `flattener.presets.export` | Export Transparency Flattener Presets | `describe flattener.presets.export` |
| `flattener.preview` | Flattener Preview | `describe flattener.preview` |

### `gradient` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `gradient.selectStop` | Select Gradient Stop | `describe gradient.selectStop` |

### `graph` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `graph.create` | Create Graph | `describe graph.create` |
| `graph.setData` | Data… | `describe graph.setData` |
| `graph.setType` | Type… | `describe graph.setType` |

### `graphicStyle` — 18

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `graphicStyle.apply` | Apply Graphic Style | `describe graphicStyle.apply` |
| `graphicStyle.new` | New Graphic Style | `describe graphicStyle.new` |
| `graphicStyle.delete` | Delete Graphic Style | `describe graphicStyle.delete` |
| `graphicStyle.duplicate` | Duplicate Graphic Style | `describe graphicStyle.duplicate` |
| `graphicStyle.list` | List Graphic Styles | `describe graphicStyle.list` |
| `graphicStyle.redefine` | Redefine Graphic Style | `describe graphicStyle.redefine` |
| `graphicStyle.breakLink` | Break Link to Graphic Style | `describe graphicStyle.breakLink` |
| `graphicStyle.rename` | Rename Graphic Style | `describe graphicStyle.rename` |
| `graphicStyle.unused` | Select All Unused | `describe graphicStyle.unused` |
| `graphicStyle.sortByName` | Sort by Name | `describe graphicStyle.sortByName` |
| `graphicStyle.merge` | Merge Graphic Styles | `describe graphicStyle.merge` |
| `graphicStyle.move` | Move Graphic Style | `describe graphicStyle.move` |
| `graphicStyle.setOptions` | Graphic Styles Options | `describe graphicStyle.setOptions` |
| `graphicStyle.libraries` | Graphic Style Libraries | `describe graphicStyle.libraries` |
| `graphicStyle.library` | Graphic Style Library | `describe graphicStyle.library` |
| `graphicStyle.addFromLibrary` | Add to Graphic Styles | `describe graphicStyle.addFromLibrary` |
| `graphicStyle.saveLibrary` | Save Graphic Style Library… | `describe graphicStyle.saveLibrary` |
| `graphicStyle.loadLibrary` | Other Library… | `describe graphicStyle.loadLibrary` |

### `guide` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `guide.add` | Add Guide | `describe guide.add` |
| `guide.remove` | Remove Guide | `describe guide.remove` |
| `guide.move` | Move Guide | `describe guide.move` |

### `help` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `help.discord` | Join Our Discord | `describe help.discord` |
| `help.website` | ArtCraft Website | `describe help.website` |
| `help.appPage` | VectorCraft on getartcraft.com | `describe help.appPage` |
| `help.github` | VectorCraft on GitHub | `describe help.github` |
| `help.links` | Links | `describe help.links` |

### `image` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `image.info` | Image Info | `describe image.info` |

### `livePaint` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `livePaint.make` | Make | `describe livePaint.make` |
| `livePaint.merge` | Merge | `describe livePaint.merge` |
| `livePaint.release` | Release | `describe livePaint.release` |
| `livePaint.expand` | Expand | `describe livePaint.expand` |
| `livePaint.fill` | Live Paint Bucket | `describe livePaint.fill` |
| `livePaint.strokeEdge` | Live Paint Bucket (Stroke) | `describe livePaint.strokeEdge` |
| `livePaint.info` | Live Paint Info | `describe livePaint.info` |

### `magicWand` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `magicWand.set` | Magic Wand Options | `describe magicWand.set` |
| `magicWand.options` | Magic Wand Settings | `describe magicWand.options` |

### `object` — 66

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `object.clippingMask.make` | Make | `describe object.clippingMask.make` |
| `object.clippingMask.release` | Release | `describe object.clippingMask.release` |
| `object.clippingMask.editContents` | Edit Contents | `describe object.clippingMask.editContents` |
| `object.clippingMask.editMask` | Edit Clipping Path | `describe object.clippingMask.editMask` |
| `object.rasterize` | Rasterize… | `describe object.rasterize` |
| `object.createObjectMosaic` | Create Object Mosaic… | `describe object.createObjectMosaic` |
| `object.cropImage` | Crop Image | `describe object.cropImage` |
| `object.createTrimMarks` | Create Trim Marks | `describe object.createTrimMarks` |
| `object.blend.make` | Make | `describe object.blend.make` |
| `object.blend.release` | Release | `describe object.blend.release` |
| `object.blend.options` | Blend Options… | `describe object.blend.options` |
| `object.blend.expand` | Expand | `describe object.blend.expand` |
| `object.blend.replaceSpine` | Replace Spine | `describe object.blend.replaceSpine` |
| `object.blend.reverseSpine` | Reverse Spine | `describe object.blend.reverseSpine` |
| `object.blend.reverseFrontToBack` | Reverse Front to Back | `describe object.blend.reverseFrontToBack` |
| `object.envelope.makeWithWarp` | Make with Warp… | `describe object.envelope.makeWithWarp` |
| `object.envelope.makeWithMesh` | Make with Mesh… | `describe object.envelope.makeWithMesh` |
| `object.envelope.makeWithTopObject` | Make with Top Object | `describe object.envelope.makeWithTopObject` |
| `object.envelope.release` | Release | `describe object.envelope.release` |
| `object.envelope.options` | Envelope Options… | `describe object.envelope.options` |
| `object.envelope.expand` | Expand | `describe object.envelope.expand` |
| `object.envelope.editContents` | Edit Contents | `describe object.envelope.editContents` |
| `object.envelope.setMeshPoint` | Move Envelope Mesh Point | `describe object.envelope.setMeshPoint` |
| `object.mesh.create` | Create Gradient Mesh… | `describe object.mesh.create` |
| `object.mesh.setPointColor` | Set Mesh Point Color | `describe object.mesh.setPointColor` |
| `object.mesh.movePoint` | Move Mesh Point | `describe object.mesh.movePoint` |
| `object.mesh.addLine` | Add Mesh Line | `describe object.mesh.addLine` |
| `object.mesh.deletePoint` | Delete Mesh Point | `describe object.mesh.deletePoint` |
| `object.mesh.expand` | Expand Gradient Mesh | `describe object.mesh.expand` |
| `object.textWrap.make` | Make | `describe object.textWrap.make` |
| `object.textWrap.release` | Release | `describe object.textWrap.release` |
| `object.textWrap.options` | Text Wrap Options… | `describe object.textWrap.options` |
| `object.makePixelPerfect` | Make Pixel Perfect | `describe object.makePixelPerfect` |
| `object.expandBrush` | Expand Brush Strokes | `describe object.expandBrush` |
| `object.pattern.make` | Make | `describe object.pattern.make` |
| `object.pattern.edit` | Edit Pattern | `describe object.pattern.edit` |
| `object.pattern.done` | Done | `describe object.pattern.done` |
| `object.pattern.cancel` | Cancel | `describe object.pattern.cancel` |
| `object.pattern.saveCopy` | Save a Copy | `describe object.pattern.saveCopy` |
| `object.repeat.radial` | Radial | `describe object.repeat.radial` |
| `object.repeat.grid` | Grid | `describe object.repeat.grid` |
| `object.repeat.mirror` | Mirror | `describe object.repeat.mirror` |
| `object.repeat.release` | Release | `describe object.repeat.release` |
| `object.repeat.options` | Options… | `describe object.repeat.options` |
| `object.repeat.expand` | Expand Repeat | `describe object.repeat.expand` |
| `object.liquify` | Liquify | `describe object.liquify` |
| `object.puppetWarp` | Puppet Warp | `describe object.puppetWarp` |
| `object.setOverprint` | Overprint | `describe object.setOverprint` |
| `object.flattenTransparency` | Flatten Transparency… | `describe object.flattenTransparency` |
| `object.expand` | Expand… | `describe object.expand` |
| `object.expand.info` | Expand Options | `describe object.expand.info` |
| `object.slice.make` | Make | `describe object.slice.make` |
| `object.slice.release` | Release | `describe object.slice.release` |
| `object.slice.fromGuides` | Create from Guides | `describe object.slice.fromGuides` |
| `object.slice.fromSelection` | Create from Selection | `describe object.slice.fromSelection` |
| `object.slice.duplicate` | Duplicate Slice | `describe object.slice.duplicate` |
| `object.slice.combine` | Combine Slices | `describe object.slice.combine` |
| `object.slice.divide` | Divide Slices… | `describe object.slice.divide` |
| `object.slice.deleteAll` | Delete All | `describe object.slice.deleteAll` |
| `object.slice.options` | Slice Options… | `describe object.slice.options` |
| `object.slice.clipToArtboard` | Clip to Artboard | `describe object.slice.clipToArtboard` |
| `object.slice.create` | Create Slice | `describe object.slice.create` |
| `object.slice.setRect` | Set Slice Rectangle | `describe object.slice.setRect` |
| `object.slice.move` | Move Slices | `describe object.slice.move` |
| `object.slice.delete` | Delete Slices | `describe object.slice.delete` |
| `object.slice.select` | Select Slices | `describe object.slice.select` |

### `pattern` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `pattern.options` | Pattern Options | `describe pattern.options` |
| `pattern.delete` | Delete Pattern | `describe pattern.delete` |
| `pattern.list` | List Patterns | `describe pattern.list` |
| `pattern.transform` | Transform Patterns | `describe pattern.transform` |

### `perspective` — 8

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `perspective.grid.set` | Define Perspective Grid | `describe perspective.grid.set` |
| `perspective.grid.preset` | Perspective Grid Preset | `describe perspective.grid.preset` |
| `perspective.grid.show` | Show Perspective Grid | `describe perspective.grid.show` |
| `perspective.plane.set` | Active Perspective Plane | `describe perspective.plane.set` |
| `perspective.attach` | Attach to Active Plane | `describe perspective.attach` |
| `perspective.release` | Release with Perspective | `describe perspective.release` |
| `perspective.move` | Move in Perspective | `describe perspective.move` |
| `perspective.draw` | Draw in Perspective | `describe perspective.draw` |

### `prefs` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `prefs.get` | Get Preferences | `describe prefs.get` |
| `prefs.set` | Set Preference | `describe prefs.set` |
| `prefs.reset` | Reset Preferences | `describe prefs.reset` |
| `prefs.list` | List Preferences | `describe prefs.list` |

### `slice` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `slice.list` | List Slices | `describe slice.list` |

### `tool` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `tool.select` | Select Tool | `describe tool.select` |

### `view` — 15

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `view.drawMode` | Drawing Mode | `describe view.drawMode` |
| `view.proofSetup` | Proof Setup | `describe view.proofSetup` |
| `view.proofColors` | Proof Colors | `describe view.proofColors` |
| `view.overprintPreview` | Overprint Preview | `describe view.overprintPreview` |
| `view.separationsPreview` | Separations Preview | `describe view.separationsPreview` |
| `view.saved.new` | New View… | `describe view.saved.new` |
| `view.saved.edit` | Edit Views… | `describe view.saved.edit` |
| `view.saved.list` | Saved Views | `describe view.saved.list` |
| `view.transparencyGrid` | Show Transparency Grid | `describe view.transparencyGrid` |
| `view.guides.make` | Make Guides | `describe view.guides.make` |
| `view.guides.release` | Release Guides | `describe view.guides.release` |
| `view.guides.lock` | Lock Guides | `describe view.guides.lock` |
| `view.guides.clear` | Clear Guides | `describe view.guides.clear` |
| `view.slices.hide` | Hide Slices | `describe view.slices.hide` |
| `view.slices.lock` | Lock Slices | `describe view.slices.lock` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
