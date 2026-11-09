---
name: jianying-draft-text
description: "Create, edit, style, animate, template, inspect, and recover JianYing text elements through released Rust caption primitives and guarded official text-resource routes."
license: Apache-2.0
---

# JianYing Text

用于剪映“文本”面板中的默认文本、花字、气泡、动画、文字模板和样式操作。字幕批量时间轴工作交给字幕分类，本技能聚焦普通画面文字。

## 什么时候使用

- 新建标题、说明、角标、章节文字、花字或气泡。
- 调整字体、字号、颜色、字重、局部样式、入出场动画。
- 检索官方文字模板并将其应用到隔离草稿。

## 能力边界

- ✅ 能做：普通文本、基础/局部样式、气泡花字、动画和可验证文字模板计划。
- ⚠️ 需要条件：字体必须可用；官方资源需要权益；观感需要冷重开。
- ❌ 不该用：不处理批量字幕对齐、ASR 或翻译时间轴，也不在未知字体下声称像素一致。

## 快速开始

可以直接说：“0–2 秒加主标题”“把标题第二行改成黄色粗体”“给片尾文字加淡出动画”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求文本面板的新建文字、文字样式、花字、气泡、动画或文字模板。
- 所需 capability：`captions.edit`、`captions.style`、`captions.style_ranges`、`captions.bubble`、`captions.animation`、`media.official_resource_apply`。
- 最低 CLI 版本：`1.6.19`；官方文字模板应用 capability 未 supported 时停在预览/批准门禁。
- 默认风险：`reversible_write`。
- 输入事实：目标草稿副本、文字内容、时间范围、位置/安全区、字体可用性、样式和资源授权。
- 确认点：写入已有草稿、使用专业版/限免文字资源、替换品牌文案和原生播放分别确认。
- 成功证据：`cold_reopen`；仅 JSON 字段存在不能证明字体和换行观感。
- 禁止行为：不得把字幕批量时间估算当普通文本布局，不得伪造 effect/resource ID，不得在字体缺失时声称样式一致。

## 工作流

### Step 1 — 定位文字
列出现有文字并读取目标 segment ID。

### Step 2 — 选择动作
按 [功能动线](references/workflow.md) 选择新建、样式、花字/气泡、动画或模板路径。

### Step 3 — 隔离执行
对隔离副本执行固定 argv；官方资源先预览、校验权益并取得收据。

### Step 4 — 验证
`captions get/list` 与 `project verify` 检查结构；冷重开检查字体、换行、安全区和动画。

### Step 5 — 恢复
失败时恢复文字段快照或删除新增 segment。

## Rules

- 文字内容、范围、位置和样式必须绑定同一 segment ID。
- 字体缺失先报告替代候选，不静默替换。
- 官方模板和本地样式是不同路由，不能互相冒充。
- 品牌声明变更必须单独确认。

## Gotchas

1. **普通文字与字幕混用：** 叙事字幕用字幕技能，标题/角标才走本技能。
2. **UTF-16 范围越界：** 局部样式按代码单元校验，不能按肉眼字符数猜。
3. **字体只在本机存在：** 冷重开前检查字体资源与回退。
4. **气泡资源 ID 伪造：** 只使用目录或已验证草稿中的 ID。
5. **模板应用变成默认文本：** capability 不足时保持阻断，不降级伪装。

## 安全与数据

不上传文案或字体文件；联网模板、翻译或 Provider 仅在精确授权范围内调用，日志只保存摘要和资源身份。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
