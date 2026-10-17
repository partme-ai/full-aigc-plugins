# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 明确工作范围 | `comp.workArea` | `{"start":0,"end":3}` |
| 2. 读取工程合成与图层结构 | `project.summary` | `{}` |
| 3. 另存可编辑工程副本 | `file.saveCopy` | `{"path":"output/motion.ecproj"}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "comp.workArea", "params": {"start": 0, "end": 3}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

effectcraft-cli run --project input.ecproj prop.set '{"path":"transform/opacity","value":90}' --save-as output.ecproj。多个 id JSON 成对放同一批次；新工程显式 --empty，避免默认demo。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

先渲染短片段，完整输出后独立检查时长、帧率、音频与alpha。

### 可直接执行的序列帧导出

先建立一个新的 `output` 目录，在现有合成中执行上表三个方法并确认 `output/motion.ecproj` 已保存。将 `craft-steps.json` 的 `cliExport` 中 argv 数组逐项作为参数传给同一官方 CLI：

```text
effectcraft-cli render --project output/motion.ecproj --out output/motion-frames --format png --work-area --resolution quarter --channels rgba --audio off
```

此例以已有3秒、25fps的工作区间生成75张 `motion-frames_*.png`，输出尺寸是原合成的1/4；按帧号排序，全部解码并检查首、中、尾画面。实际任务先读取帧率、合成尺寸与workArea，计算预期帧数；不要强套75帧。`--out` 是序列文件前缀，不是一个PNG文件。PNG序列没有音轨，不能作为含音频视频交付。正式尺寸使用 `--resolution full`；先检查短区间，再按用户要求编码成片，并独立检查视频和音频。

在已打开的宿主编辑器内，先用当前会话保存目标工程，再针对这个已保存副本调用CLI导出；该新进程不会回写编辑器，也不证明界面同步。不要另建headless工程冒充当前编辑器作品。

边界：此处仅验证PNG序列，视频编码、音轨与真实镜头的最终效果须另验收。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
