# 工程与素材管理操作指南

## 目标与前置

建立、保存和重开 ecproj 工程，整理项目项目项。CLI 调用之间不共享会话；修改必须 save-as 或同一批次保存，另存原生检查点。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `file.newProject` | New Project |
| `file.openDemoProject` | Open Demo Project |
| `file.open` | Open Project... |
| `file.save` | Save |
| `file.saveAs` | Save As... |
| `file.incrementAndSave` | Increment and Save |
| `file.revert` | Revert |
| `file.import` | File... |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 67 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `file` — 56

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `file.newProject` | New Project | `describe file.newProject` |
| `file.openDemoProject` | Open Demo Project | `describe file.openDemoProject` |
| `file.open` | Open Project... | `describe file.open` |
| `file.save` | Save | `describe file.save` |
| `file.saveAs` | Save As... | `describe file.saveAs` |
| `file.incrementAndSave` | Increment and Save | `describe file.incrementAndSave` |
| `file.revert` | Revert | `describe file.revert` |
| `file.import` | File... | `describe file.import` |
| `file.projectSettings` | Project Settings... | `describe file.projectSettings` |
| `file.cycleBitDepth` | Cycle Project Bit Depth | `describe file.cycleBitDepth` |
| `file.close` | Close | `describe file.close` |
| `file.closeProject` | Close Project | `describe file.closeProject` |
| `file.saveCopy` | Save a Copy... | `describe file.saveCopy` |
| `file.importMultiple` | Multiple Files... | `describe file.importMultiple` |
| `file.importPlaceholder` | Placeholder... | `describe file.importPlaceholder` |
| `file.importSolid` | Solid... | `describe file.importSolid` |
| `file.newCompFromSelection` | New Comp from Selection... | `describe file.newCompFromSelection` |
| `file.collectFiles` | Collect Files... | `describe file.collectFiles` |
| `file.consolidateFootage` | Consolidate All Footage | `describe file.consolidateFootage` |
| `file.removeUnusedFootage` | Remove Unused Footage | `describe file.removeUnusedFootage` |
| `file.reduceProject` | Reduce Project | `describe file.reduceProject` |
| `file.findMissing` | Find Missing | `describe file.findMissing` |
| `file.runScript` | Run Script File... | `describe file.runScript` |
| `file.interpretFootage` | Main... | `describe file.interpretFootage` |
| `file.rememberInterpretation` | Remember Interpretation | `describe file.rememberInterpretation` |
| `file.applyInterpretation` | Apply Interpretation | `describe file.applyInterpretation` |
| `file.replaceFootage` | File... | `describe file.replaceFootage` |
| `file.replaceWithPlaceholder` | Placeholder... | `describe file.replaceWithPlaceholder` |
| `file.replaceWithSolid` | Solid... | `describe file.replaceWithSolid` |
| `file.reloadFootage` | Reload Footage | `describe file.reloadFootage` |
| `file.revealInFinder` | Reveal in Finder | `describe file.revealInFinder` |
| `file.importLottie` | Lottie... | `describe file.importLottie` |
| `file.importTimeline` | Adobe Premiere Pro Project... | `describe file.importTimeline` |
| `file.timelineFormats` | Timeline Interchange Formats | `describe file.timelineFormats` |
| `file.watchFolder` | Watch Folder... | `describe file.watchFolder` |
| `file.watchFolder.poll` | Poll Watch Folder | `describe file.watchFolder.poll` |
| `file.importVanishingPoint` | Vanishing Point (.vpe)... | `describe file.importVanishingPoint` |
| `file.openRecent` | Open Recent | `describe file.openRecent` |
| `file.clearRecent` | Clear Recent Projects | `describe file.clearRecent` |
| `file.autoSave` | Auto-Save Now | `describe file.autoSave` |
| `file.recoveryInfo` | Auto-Save Status | `describe file.recoveryInfo` |
| `file.importRecent` | Import Recent Footage | `describe file.importRecent` |
| `file.clearRecentFootage` | Clear Recent Footage | `describe file.clearRecentFootage` |
| `file.saveCopyAsXml` | Save a Copy As XML... | `describe file.saveCopyAsXml` |
| `file.replaceWithLayeredComp` | With Layered Comp | `describe file.replaceWithLayeredComp` |
| `file.executeFile` | Execute File | `describe file.executeFile` |
| `file.createProxy` | Create Proxy | `describe file.createProxy` |
| `file.setProxy` | File... | `describe file.setProxy` |
| `file.setProxyNone` | None | `describe file.setProxyNone` |
| `file.useProxy` | Use Proxy | `describe file.useProxy` |
| `file.interpretProxy` | Proxy... | `describe file.interpretProxy` |
| `file.installScript` | Install Script File... | `describe file.installScript` |
| `file.installScriptUIPanel` | Install ScriptUI Panel... | `describe file.installScriptUIPanel` |
| `file.uninstallScript` | Uninstall Script | `describe file.uninstallScript` |
| `file.scripts.list` | List Scripts | `describe file.scripts.list` |
| `file.newFromTemplate` | New Project from Template... | `describe file.newFromTemplate` |

### `project` — 11

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `project.select` | Select Project Items | `describe project.select` |
| `project.rename` | Rename Item | `describe project.rename` |
| `project.move` | Move to Folder | `describe project.move` |
| `project.setLabel` | Item Label | `describe project.setLabel` |
| `project.setComment` | Item Comment | `describe project.setComment` |
| `project.delete` | Delete Project Items | `describe project.delete` |
| `project.usage` | Project Item Usage | `describe project.usage` |
| `project.duplicate` | Duplicate Project Items | `describe project.duplicate` |
| `project.summary` | Project Summary | `describe project.summary` |
| `project.newFolder` | New Folder | `describe project.newFolder` |
| `project.setProjectComment` | Project Comment | `describe project.setProjectComment` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
