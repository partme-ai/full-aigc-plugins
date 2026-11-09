---
name: jianying-draft-templates
description: "Inspect, save, list, apply, duplicate, customize, import tracks from, and verify JianYing draft and text-style templates through released Rust template commands."
license: Apache-2.0
---

# JianYing Templates

用于剪映“模板”以及可复用草稿模板、文字样式预设。模板应用必须产出独立草稿，不保留对源模板的可变依赖。

## 什么时候使用

- 浏览、保存、复制或应用草稿模板。
- 替换模板文字/素材，导入模板轨道。
- 提取和应用文字样式预设，或检索官方模板。

## 能力边界

- ✅ 能做：模板检查、保存、应用、复制、内容替换、导轨和文字预设。
- ⚠️ 需要条件：画幅/fps/字体/素材需兼容；官方模板要权益；输出要冷重开。
- ❌ 不该用：不修改源模板、不静默删轨或换字体、不把缩略图当已下载模板。

## 快速开始

可以直接说：“把这个草稿保存为社媒模板”“从子草稿导入字幕轨”“应用模板后替换产品图和标题”。首次使用加载 [功能动线](references/workflow.md)。
批量个性化输出时加载 [Clone-first 合同](references/clone-first-batch-workflow.md)；每个输出独立验证，母模板保持只读。

## 运行契约

- 触发条件：用户要求模板库、套用模板、复用草稿结构、替换模板内容或文字样式预设。
- 所需 capability：`template.library`、`template.preset`、`template.duplicate`、`template.import_track`、`media.official_resource_apply`、`project.verify`。
- 最低 CLI 版本：`1.6.19`；本地模板命令 supported，官方在线模板仍受下载/应用 Adapter 门禁。
- 默认风险：`reversible_write`。
- 输入事实：模板/草稿绝对路径、画幅/fps、轨道和材料清单、替换表、用途、版型与权益。
- 确认点：保存到模板库、套用受限模板、批量替换和写入正式草稿库分别确认。
- 成功证据：`cold_reopen`；复制目录成功不等于模板素材可用。
- 禁止行为：不得修改源模板、保留外部可变素材引用、忽略画幅冲突或把在线模板缩略图当已下载资源。

## 工作流

### Step 1 — 检查模板
`template inspect/list` 读取模板结构和材料，检查画幅、fps 与缺失素材。

### Step 2 — 选择动作
按 [功能动线](references/workflow.md) 选择保存、应用、复制、替换、导轨或预设。

### Step 3 — 创建独立输出
事务性地创建独立输出并重定位本地素材。

### Step 4 — 验证
`project verify`、`project diff` 后冷重开检查布局、字体和资源。

### Step 5 — 恢复
失败时删除未注册输出或从快照恢复，不改源模板。

## Rules

- 模板输出必须独立于源草稿和源素材可变路径。
- 替换目标必须由名称或轨道/索引唯一定位。
- 画幅、fps、字体和许可冲突先报告再转换。
- 模板应用和草稿发布分开批准。
- Compound Clip 在发布二进制 capability 未为 `supported` 前保持 `plan_only`，不得以直接改 JSON 或 GUI 宏替代。

## Gotchas

1. **直接编辑源模板：** 始终创建独立输出。
2. **同名轨道选错：** inspect 后用唯一轨道身份。
3. **替换素材时长不匹配：** 先 probe 并说明裁切策略。
4. **字体回退破坏排版：** 冷重开检查字体和换行。
5. **官方模板缓存失效：** 权益与收据必须对应当前用途。

## 安全与数据

模板操作默认只读写用户指定本地目录，不上传素材；在线模板仅保存最小资源与权益证据。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
