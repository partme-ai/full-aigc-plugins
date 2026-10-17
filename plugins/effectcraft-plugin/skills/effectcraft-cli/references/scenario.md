# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 199 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `app` — 12

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `app.capabilities` | App Capabilities | `describe app.capabilities` |
| `app.about` | About EffectCraft... | `describe app.about` |
| `app.settings` | Settings... | `describe app.settings` |
| `app.gpuInfo` | GPU Information... | `describe app.gpuInfo` |
| `app.hide` | Hide EffectCraft | `describe app.hide` |
| `app.hideOthers` | Hide Others | `describe app.hideOthers` |
| `app.showAll` | Show All | `describe app.showAll` |
| `app.quit` | Quit EffectCraft | `describe app.quit` |
| `app.commandPalette` | Quick Apply... | `describe app.commandPalette` |
| `app.keyboardShortcuts` | Keyboard Shortcuts | `describe app.keyboardShortcuts` |
| `app.templates` | Templates | `describe app.templates` |
| `app.find` | Find | `describe app.find` |

### `cache` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `cache.diskStats` | Disk Cache Statistics | `describe cache.diskStats` |

### `command` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `command.list` | List Commands | `describe command.list` |
| `command.describe` | Describe Command | `describe command.describe` |

### `contentFill` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `contentFill.set` | Content-Aware Fill Settings | `describe contentFill.set` |
| `contentFill.generate` | Generate Fill Layer | `describe contentFill.generate` |

### `edit` — 26

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `edit.undo` | Undo | `describe edit.undo` |
| `edit.redo` | Redo | `describe edit.redo` |
| `edit.cut` | Cut | `describe edit.cut` |
| `edit.copy` | Copy | `describe edit.copy` |
| `edit.copyWithPropertyLinks` | Copy with Property Links | `describe edit.copyWithPropertyLinks` |
| `edit.copyWithRelativePropertyLinks` | Copy with Relative Property Links | `describe edit.copyWithRelativePropertyLinks` |
| `edit.copyExpressionOnly` | Copy Expression Only | `describe edit.copyExpressionOnly` |
| `edit.paste` | Paste | `describe edit.paste` |
| `edit.pasteReversedKeyframes` | Paste Reversed Keyframes | `describe edit.pasteReversedKeyframes` |
| `edit.clear` | Clear | `describe edit.clear` |
| `edit.duplicate` | Duplicate | `describe edit.duplicate` |
| `edit.splitLayer` | Split Layer | `describe edit.splitLayer` |
| `edit.liftWorkArea` | Lift Work Area | `describe edit.liftWorkArea` |
| `edit.extractWorkArea` | Extract Work Area | `describe edit.extractWorkArea` |
| `edit.selectAll` | Select All | `describe edit.selectAll` |
| `edit.deselectAll` | Deselect All | `describe edit.deselectAll` |
| `edit.label` | Label | `describe edit.label` |
| `edit.selectLabelGroup` | Select Label Group | `describe edit.selectLabelGroup` |
| `edit.purgeUndo` | Undo | `describe edit.purgeUndo` |
| `edit.purge` | Purge | `describe edit.purge` |
| `edit.editOriginal` | Edit Original... | `describe edit.editOriginal` |
| `edit.history.list` | History | `describe edit.history.list` |
| `edit.history.goto` | Go to History State | `describe edit.history.goto` |
| `edit.pasteTextMatchFormatting` | Paste Text and Match Formatting | `describe edit.pasteTextMatchFormatting` |
| `edit.pasteTextFormattingOnly` | Paste Text Formatting Only | `describe edit.pasteTextFormattingOnly` |
| `edit.history` | History | `describe edit.history` |

### `editor` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `editor.state` | Editor State | `describe editor.state` |

### `engine` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `engine.batch` | Run Commands (Batch) | `describe engine.batch` |

### `essential` — 22

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `essential.setPrimary` | Primary Composition | `describe essential.setPrimary` |
| `essential.setName` | Essential Graphics Name | `describe essential.setName` |
| `essential.addProperty` | Add Property to Essential Graphics | `describe essential.addProperty` |
| `essential.addMirror` | Add Mirror | `describe essential.addMirror` |
| `essential.linkProperty` | Link Property to Control | `describe essential.linkProperty` |
| `essential.unlinkProperty` | Unlink Property | `describe essential.unlinkProperty` |
| `essential.addMedia` | Add Media Replacement | `describe essential.addMedia` |
| `essential.addGroup` | Add Group | `describe essential.addGroup` |
| `essential.addComment` | Add Comment | `describe essential.addComment` |
| `essential.rename` | Rename Control | `describe essential.rename` |
| `essential.remove` | Remove Control | `describe essential.remove` |
| `essential.move` | Move Control | `describe essential.move` |
| `essential.soloSupported` | Solo Supported Properties | `describe essential.soloSupported` |
| `essential.exportTemplate` | Essential Graphics Template... | `describe essential.exportTemplate` |
| `essential.importTemplate` | Essential Graphics Template... | `describe essential.importTemplate` |
| `essential.set` | Set Essential Property | `describe essential.set` |
| `essential.pushToComp` | Push Override Values to Source | `describe essential.pushToComp` |
| `essential.revert` | Revert | `describe essential.revert` |
| `essential.list` | Essential Graphics controls | `describe essential.list` |
| `essential.canAdd` | Can Add Property to Essential Graphics | `describe essential.canAdd` |
| `essential.instance` | Essential Properties of a precomp layer | `describe essential.instance` |
| `essential.templateInfo` | Read a template's manifest | `describe essential.templateInfo` |

### `face` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `face.models` | Face Tracking Models | `describe face.models` |
| `face.model.select` | Use Face Tracking Model | `describe face.model.select` |
| `face.model.install` | Install Face Tracking Model | `describe face.model.install` |
| `face.model.download` | Download Face Tracking Model | `describe face.model.download` |
| `face.model.remove` | Remove Face Tracking Model | `describe face.model.remove` |

### `help` — 13

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `help.docs` | EffectCraft Help... | `describe help.docs` |
| `help.discord` | Join the ArtCraft Discord... | `describe help.discord` |
| `help.website` | ArtCraft Website | `describe help.website` |
| `help.appPage` | EffectCraft Home Page | `describe help.appPage` |
| `help.github` | EffectCraft on GitHub | `describe help.github` |
| `help.onlineTutorials` | Online Tutorials... | `describe help.onlineTutorials` |
| `help.inAppTutorials` | In-App Tutorials... | `describe help.inAppTutorials` |
| `help.reportIssue` | Provide Feedback... | `describe help.reportIssue` |
| `help.sibling` | Other ArtCraft Apps | `describe help.sibling` |
| `help.enableLogging` | Enable Logging | `describe help.enableLogging` |
| `help.revealLogFile` | Reveal Logging File | `describe help.revealLogFile` |
| `help.systemReport` | System Compatibility Report... | `describe help.systemReport` |
| `help.systemInfo` | System Information | `describe help.systemInfo` |

### `item` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `item.metadata` | Metadata | `describe item.metadata` |

### `jobs` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `jobs.list` | Background Jobs | `describe jobs.list` |
| `jobs.cancel` | Cancel Job | `describe jobs.cancel` |
| `jobs.wait` | Wait for Background Jobs | `describe jobs.wait` |

### `learn` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `learn.list` | Learn Tutorials | `describe learn.list` |
| `learn.state` | Tutorial State | `describe learn.state` |
| `learn.start` | Start Tutorial | `describe learn.start` |
| `learn.step` | Tutorial Step | `describe learn.step` |
| `learn.stop` | Close Tutorial | `describe learn.stop` |

### `liquify` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `liquify.stroke` | Liquify Stroke | `describe liquify.stroke` |
| `liquify.clear` | Clear Liquify Mesh | `describe liquify.clear` |

### `markers` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `markers.list` | List Markers | `describe markers.list` |
| `markers.nested` | Nested Comp Markers | `describe markers.nested` |
| `markers.set` | Marker Settings | `describe markers.set` |
| `markers.delete` | Delete Marker | `describe markers.delete` |
| `markers.convert` | Convert Marker | `describe markers.convert` |

### `motion` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `motion.sketch` | Motion Sketch | `describe motion.sketch` |

### `paint` — 6

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `paint.stroke` | Paint Stroke | `describe paint.stroke` |
| `paint.options` | Paint Options | `describe paint.options` |
| `paint.brushPreset` | Brush Preset | `describe paint.brushPreset` |
| `paint.setCloneSource` | Set Clone Source | `describe paint.setCloneSource` |
| `paint.removeStroke` | Delete Paint Stroke | `describe paint.removeStroke` |
| `paint.presets` | Brush Presets | `describe paint.presets` |

### `paths` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `paths.pointsFollowNulls` | Points Follow Nulls | `describe paths.pointsFollowNulls` |
| `paths.nullsFollowPoints` | Nulls Follow Points | `describe paths.nullsFollowPoints` |
| `paths.tracePath` | Trace Path | `describe paths.tracePath` |

### `playback` — 6

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `playback.toggle` | Play Current Preview | `describe playback.toggle` |
| `playback.cacheWhenIdle` | Cache Frames When Idle | `describe playback.cacheWhenIdle` |
| `playback.audio` | Audio | `describe playback.audio` |
| `playback.scrubAudio` | Scrub Audio | `describe playback.scrubAudio` |
| `playback.settings.get` | Preview Settings | `describe playback.settings.get` |
| `playback.settings.set` | Change Preview Settings | `describe playback.settings.set` |

### `prefs` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `prefs.get` | Get Setting | `describe prefs.get` |
| `prefs.set` | Change Setting | `describe prefs.set` |
| `prefs.reset` | Reset Settings | `describe prefs.reset` |
| `prefs.open` | Open Settings | `describe prefs.open` |
| `prefs.pages` | Settings Pages | `describe prefs.pages` |

### `scopes` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `scopes.analyze` | Lumetri Scopes | `describe scopes.analyze` |

### `script` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `script.run` | Run Script | `describe script.run` |

### `scriptui` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `scriptui.list` | List Script Windows | `describe scriptui.list` |
| `scriptui.get` | Script Window Controls | `describe scriptui.get` |
| `scriptui.click` | Click Script Window Control | `describe scriptui.click` |
| `scriptui.set` | Set Script Window Control | `describe scriptui.set` |
| `scriptui.close` | Close Script Window | `describe scriptui.close` |

### `shortcuts` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `shortcuts.list` | List Keyboard Shortcuts | `describe shortcuts.list` |
| `shortcuts.set` | Set Keyboard Shortcut | `describe shortcuts.set` |
| `shortcuts.reset` | Reset Keyboard Shortcuts | `describe shortcuts.reset` |
| `shortcuts.preset` | Keyboard Shortcut Preset | `describe shortcuts.preset` |
| `shortcuts.export` | Export Keyboard Shortcuts | `describe shortcuts.export` |
| `shortcuts.import` | Import Keyboard Shortcuts | `describe shortcuts.import` |
| `shortcuts.conflicts` | Keyboard Shortcut Conflicts | `describe shortcuts.conflicts` |

### `storage` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `storage.info` | Browser Storage | `describe storage.info` |
| `storage.persist` | Request Persistent Storage | `describe storage.persist` |
| `storage.clear` | Clear Browser Storage | `describe storage.clear` |

### `templates` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `templates.list` | Project Templates | `describe templates.list` |
| `templates.thumbnail` | Template Thumbnail | `describe templates.thumbnail` |
| `templates.create` | New Project from Template | `describe templates.create` |
| `templates.saveAs` | Save as Template... | `describe templates.saveAs` |
| `templates.delete` | Delete Template | `describe templates.delete` |

### `view` — 44

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `view.lookAtSelected` | Look at Selected Layers | `describe view.lookAtSelected` |
| `view.lookAtAll` | Look at All Layers | `describe view.lookAtAll` |
| `view.addGuide` | Add Guide... | `describe view.addGuide` |
| `view.clearGuides` | Clear Guides | `describe view.clearGuides` |
| `view.importGuides` | Import Guides... | `describe view.importGuides` |
| `view.exportGuides` | Export Guides... | `describe view.exportGuides` |
| `view.layout` | Switch View Layout | `describe view.layout` |
| `view.shareViewOptions` | Share View Options | `describe view.shareViewOptions` |
| `view.extendedViewer` | Extended Viewer | `describe view.extendedViewer` |
| `view.setRegionOfInterest` | Region of Interest | `describe view.setRegionOfInterest` |
| `view.snapping` | Snapping | `describe view.snapping` |
| `view.displayColorManagement` | Use Display Color Management | `describe view.displayColorManagement` |
| `view.simulateOutput` | Simulate Output | `describe view.simulateOutput` |
| `view.customRgb` | My Custom RGB... | `describe view.customRgb` |
| `view.splitLockedViewer` | Split with New Locked Viewer | `describe view.splitLockedViewer` |
| `view.closeLockedViewer` | Close Locked Viewer | `describe view.closeLockedViewer` |
| `view.displayColor` | Viewer Color State | `describe view.displayColor` |
| `view.channel` | Show Channel | `describe view.channel` |
| `view.exposure` | Adjust Exposure | `describe view.exposure` |
| `view.resetExposure` | Reset Exposure | `describe view.resetExposure` |
| `view.takeSnapshot` | Take Snapshot | `describe view.takeSnapshot` |
| `view.showSnapshot` | Show Snapshot | `describe view.showSnapshot` |
| `view.fastPreviewMode` | Fast Previews | `describe view.fastPreviewMode` |
| `view.moveGuide` | Move Guide | `describe view.moveGuide` |
| `view.removeGuide` | Remove Guide | `describe view.removeGuide` |
| `view.zoomIn` | Zoom In | `describe view.zoomIn` |
| `view.zoomOut` | Zoom Out | `describe view.zoomOut` |
| `view.res.full` | Full | `describe view.res.full` |
| `view.res.half` | Half | `describe view.res.half` |
| `view.res.third` | Third | `describe view.res.third` |
| `view.res.quarter` | Quarter | `describe view.res.quarter` |
| `view.res.custom` | Custom... | `describe view.res.custom` |
| `view.rulers` | Show Rulers | `describe view.rulers` |
| `view.panelBackground` | Panel Background Color | `describe view.panelBackground` |
| `view.guides` | Show Guides | `describe view.guides` |
| `view.snapToGuides` | Snap to Guides | `describe view.snapToGuides` |
| `view.lockGuides` | Lock Guides | `describe view.lockGuides` |
| `view.grid` | Show Grid | `describe view.grid` |
| `view.snapToGrid` | Snap to Grid | `describe view.snapToGrid` |
| `view.options` | View Options... | `describe view.options` |
| `view.layerControls` | Show Layer Controls | `describe view.layerControls` |
| `view.fullScreen` | Enter Full Screen | `describe view.fullScreen` |
| `view.newViewer` | New Viewer | `describe view.newViewer` |
| `view.assign3dShortcut` | Assign Shortcut to 3D View | `describe view.assign3dShortcut` |

### `warp` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `warp.analyze` | Analyze | `describe warp.analyze` |
| `warp.cancel` | Cancel | `describe warp.cancel` |
| `warp.status` | Warp Stabilizer Status | `describe warp.status` |

### `window` — 8

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `window.panel` | Show Panel | `describe window.panel` |
| `window.workspace` | Workspace | `describe window.workspace` |
| `window.saveWorkspace` | Save Changes to this Workspace | `describe window.saveWorkspace` |
| `window.saveWorkspaceAs` | Save as New Workspace... | `describe window.saveWorkspaceAs` |
| `window.editWorkspaces` | Edit Workspaces... | `describe window.editWorkspaces` |
| `window.resetWorkspace` | Reset to Saved Layout | `describe window.resetWorkspace` |
| `window.assignWorkspaceShortcut` | Assign Shortcut to Workspace | `describe window.assignWorkspaceShortcut` |
| `window.scriptPanel` | ScriptUI Panel | `describe window.scriptPanel` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
