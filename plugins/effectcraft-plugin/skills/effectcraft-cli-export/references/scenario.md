# 渲染与透明输出操作指南

## 目标与前置

预览关键帧、渲染序列或视频和透明交接片段。透明交接核对 rgba 与格式支持；MP4 不代替保留 alpha 的素材，保存 ecproj 和渲染参数。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `render.backend` | Video Rendering and Effects |
| `renderQueue.add` | Add to Render Queue |
| `renderQueue.remove` | Remove from Render Queue |
| `renderQueue.setRender` | Render Queue: Render Checkbox |
| `renderQueue.setRenderSettings` | Render Settings... |
| `renderQueue.setOutputModule` | Output Module Settings... |
| `renderQueue.setOutput` | Output To... |
| `render.addOutputModule` | Add Output Module |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

## 已验证的透明输出与目标合成选择

官方 0.2.0 CLI 的 `render-frame` 写出 RGB 预览 PNG，没有 Alpha 通道。透明交付使用 `render --format png --channels rgba`；H.264 只作为不透明视频派生物，不代替透明素材。`render` 的 `--comp` 取实际合成名称，不能照搬 props/get/render-frame 支持的数字 ID。先用 info 读取目标合成名称、帧率、时长。

以下示例针对名为 NOVA intro 的 12 fps 合成，导出第 6 帧的 RGBA PNG：

以下 `SKILL_DIR` 沿用本技能 `SKILL.md` 的实际加载目录，脚本和示例均来自同一技能。

```bash
python3 "$HARNESS_DIR/scripts/cli.py" -- render \
  --comp "NOVA intro" --out /absolute/path/frame.png \
  --format png --channels rgba --start 0.5 --end 0.5833333333333334 --fps 12 \
  --project /absolute/path/source.ecproj --json
```

实际文件带帧号，此示例为 frame_00006.png；使用回执的 rendered[].output，不猜测输出路径。解码文件确认 RGBA 和 Alpha 极值；仍交付原生 ecproj 与引用素材。合成名称、时间范围、帧率和工程路径必须替换成当前项目真实值。所有编码格式和通道组合尚未逐项验收。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 26 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `file` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `file.exportLottie` | Lottie JSON... | `describe file.exportLottie` |
| `file.exportTimeline` | Adobe Premiere Pro Project... | `describe file.exportTimeline` |

### `render` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `render.backend` | Video Rendering and Effects | `describe render.backend` |
| `render.addOutputModule` | Add Output Module | `describe render.addOutputModule` |
| `render.preRender` | Pre-render... | `describe render.preRender` |
| `render.saveCurrentPreview` | Save Current Preview... | `describe render.saveCurrentPreview` |

### `renderQueue` — 20

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `renderQueue.add` | Add to Render Queue | `describe renderQueue.add` |
| `renderQueue.remove` | Remove from Render Queue | `describe renderQueue.remove` |
| `renderQueue.setRender` | Render Queue: Render Checkbox | `describe renderQueue.setRender` |
| `renderQueue.setRenderSettings` | Render Settings... | `describe renderQueue.setRenderSettings` |
| `renderQueue.setOutputModule` | Output Module Settings... | `describe renderQueue.setOutputModule` |
| `renderQueue.setOutput` | Output To... | `describe renderQueue.setOutput` |
| `renderQueue.move` | Move in Render Queue | `describe renderQueue.move` |
| `renderQueue.duplicate` | Duplicate Render Item | `describe renderQueue.duplicate` |
| `renderQueue.render` | Render | `describe renderQueue.render` |
| `renderQueue.stop` | Stop Rendering | `describe renderQueue.stop` |
| `renderQueue.list` | Render Queue Items | `describe renderQueue.list` |
| `renderQueue.templates` | Render Templates | `describe renderQueue.templates` |
| `renderQueue.saveTemplate` | Save Template... | `describe renderQueue.saveTemplate` |
| `renderQueue.deleteTemplate` | Delete Template | `describe renderQueue.deleteTemplate` |
| `renderQueue.setTemplateDefault` | Set Template Default | `describe renderQueue.setTemplateDefault` |
| `renderQueue.applyTemplate` | Apply Template | `describe renderQueue.applyTemplate` |
| `renderQueue.setLog` | Render Queue: Log | `describe renderQueue.setLog` |
| `renderQueue.setNotify` | Notify When Done | `describe renderQueue.setNotify` |
| `renderQueue.setOverflowFolders` | Storage Overflow Folders | `describe renderQueue.setOverflowFolders` |
| `renderQueue.formats` | Output Formats | `describe renderQueue.formats` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
