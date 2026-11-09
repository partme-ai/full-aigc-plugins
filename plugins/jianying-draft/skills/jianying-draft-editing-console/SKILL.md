---
name: jianying-draft-editing-console
description: "Operate JianYing timeline, track, segment, keyframe, session, recording, snapping, linkage, and zoom controls through semantic Rust commands and version-bound runtime controls."
license: Apache-2.0
---

# JianYing Editing Console

用于剪映时间线和剪辑控制台：轨道、片段、播放头、分割、裁剪、移动、复制、删除、关键帧，以及撤销/重做、磁吸、吸附、联动、录音和缩放。

## 什么时候使用

- 操作时间线片段和轨道，或读取精确控制台状态。
- 使用关键帧、裁剪、速度、音量、透明度、画中画和组合模式。
- 控制会话级撤销/重做、磁吸、吸附、联动、录音或视图缩放。

## 能力边界

- ✅ 能做：轨道/片段检查、分割、裁剪、移动、复制、删除、关键帧和受控会话动作。
- ⚠️ 需要条件：草稿写入要快照；会话动作要精确版本、所有权和前后 readback。
- ❌ 不该用：不恢复用户并行编辑、不使用固定界面位置、不在无状态回读时重复按钮动作。

## 快速开始

可以直接说：“在 2.4 秒分割当前片段”“把 B-Roll 移到 5 秒”“打开磁吸并验证状态”“时间线适配全部片段”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求剪辑控制台、时间线、轨道、片段、关键帧或会话级控制。
- 所需 capability：`timeline.edit`、`timeline.show`、`timeline.duplicate`、`timeline.remove`、`timeline.keyframe`、`runtime.control_catalog`、`runtime.controls`。
- 最低 CLI 版本：`1.6.19`；草稿协议动作可直接执行，会话控制需精确编辑器版本和状态回读。
- 默认风险：`reversible_write`。
- 输入事实：草稿隔离副本、轨道/segment ID、帧率、时间范围、目标参数、编辑器版本和当前会话所有权。
- 确认点：删除/批量移动、录音、影响当前 GUI 会话和覆盖已有关键帧分别确认。
- 成功证据：`playback`；命令返回成功不等于节奏、画面和会话状态正确。
- 禁止行为：不得用撤销恢复用户并行编辑、使用固定界面位置、把相对拖动当绝对状态或在无回读时重复会话动作。

## 工作流

### Step 1 — 建立时间线事实
`timeline show/tracks/segments/get` 建立事实；运行控制目录/Surface Inventory 审计界面入口。

### Step 2 — 选择路由
按 [功能动线](references/workflow.md) 选择草稿协议或 Runtime Control 路由。

### Step 3 — 快照与执行
草稿写入前创建快照；会话控制前后读取状态并确认由插件拥有的会话。

### Step 4 — 验证
运行结构检查和差分；需要观感结论时播放验证。

### Step 5 — 恢复
草稿动作从快照恢复；会话动作只在状态可验证时执行逆向操作。

## Rules

- 草稿协议动作始终优先于 GUI 会话控制。
- 时间使用绝对值并按项目帧率量化。
- 会话控制只作用于插件拥有的剪映进程/会话。
- Surface Inventory 的 unresolved 项保持覆盖缺口。

## Gotchas

1. **撤销影响用户并行编辑：** 不用会话 undo 代替草稿快照。
2. **相对拖动无法复现：** 计划保存绝对目标和 segment ID。
3. **切点落在帧间：** 先运行量化报告。
4. **删除共享材料：** 检查材料引用再决定保留策略。
5. **按钮可见就声称可控：** 必须有语义 ID、状态和版本证据。

## 安全与数据

控制台操作只访问用户指定草稿与插件启动/拥有的会话；不读取无关窗口、账号信息或其他应用内容。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
