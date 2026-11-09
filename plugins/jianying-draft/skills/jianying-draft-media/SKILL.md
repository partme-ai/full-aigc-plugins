---
name: jianying-draft-media
description: "Import, inspect, replace, relink, concatenate, select, download, and verify JianYing video or image materials through released Rust CLI commands and approval-gated native resource adapters."
license: Apache-2.0
---

# JianYing Media

用于剪映“素材”面板及素材轨道操作。先取得真实媒体事实，再决定本地导入、子草稿导入、官方素材下载或替换路径。

## 什么时候使用

- 导入视频、图片、素材文件或另一个草稿/轨道。
- 检索并下载剪映官方素材，或替换、重链、删除已有素材。
- 分析场景切点、重复拍摄、素材流或资源权益。

## 能力边界

- ✅ 能做：本地视频/图片导入、整草稿或指定轨道导入、替换/重链/删除和素材事实检查。
- ⚠️ 需要条件：官方素材下载要权益与用途证据；写入要隔离副本；完成结论要冷重开。
- ❌ 不该用：不处理字幕排版、数字人生成或未建模的界面入口；这些请求改由对应分类技能或保持阻断。

## 快速开始

可以直接说：“把 `/素材/开场.mp4` 加到 0 秒”“把子草稿 B 接到主草稿末尾”“从官方素材找可商用的 9:16 科技园航拍”。首次使用先加载 [功能动线](references/workflow.md)，再选择唯一动作 ID。
遇到 WebM、透明 Web VFX、异常尺寸/帧率或兼容性未知素材时，加载
[媒体预检合同](references/media-preflight-workflow.md)，先形成可对账的派生媒体关系，再决定是否导入。

## 执行边界

- 本地素材优先使用固定 Rust argv；官方素材必须经过候选筛选、权益校验、下载收据和应用后检查。
- 标准化由受控 Provider 创建派生媒体；技能不静默转码，Provider 也不能直接修改草稿。
- 整个子草稿用 `project concat`；仅导入一条轨道用 `template inspect` + `template import-track`。
- 不把素材面板可见、下载图标消失或 GUI 提示当作加入草稿成功。

## 运行契约

- 触发条件：用户提出素材导入、子草稿、素材库、替换、重链、删除或素材分析。
- 所需 capability：`media.probe`、`media.add`、`project.edit_isolated`、`project.verify`、`template.import_track`、`media.replace`、`media.relink`、`media.official_resource`、`media.official_resource_apply`；`project concat` 另以发布命令目录的 supported 状态为准。
- 最低 CLI 版本：`1.6.19`；`media.official_resource_apply` 为 partial 时，官方素材只执行到已验证收据或版本绑定 Adapter 门禁。
- 默认风险：`reversible_write`。
- 输入事实：绝对素材/草稿路径、媒体探测结果、目标草稿隔离副本、时间范围、用途、渠道和权益证据。
- 确认点：下载官方资源、写入已有草稿、合并子草稿、删除片段和调用原生应用分别确认。
- 成功证据：`cold_reopen`；结构校验不等于剪映冷重开后资源可用。
- 禁止行为：不得伪造资源 ID、跳过探测、覆盖源草稿、把坐标当动作 ID，或用 Rust 源码代替发布二进制能力证明。

## 工作流

### Step 1 — 读取事实
运行 `doctor`、`capabilities`，并用 `media probe` 或 `project inspect` 读取事实。

### Step 2 — 选择动作
选择 [功能动线](references/workflow.md) 中唯一匹配的语义动作。

### Step 3 — 隔离与执行
先快照/隔离输出；固定 argv 写入，官方素材先登记权益与下载收据。

### Step 4 — 验证
运行 `project verify`、`project diff`；要求完成时冷重开并检查素材身份、时长和画面。

### Step 5 — 恢复
失败时局部删除或恢复快照；ambiguous 下载/应用不自动重试。

## Rules

- 媒体时长、尺寸、流和哈希只来自探测结果。
- 语义动作必须绑定绝对路径、目标范围和固定 argv。
- 官方素材先许可和收据，后应用。
- 验证等级按实际证据报告，不以计划代替完成。

## Gotchas

1. **整草稿与轨道混淆：** 整体追加用 `project concat`，单轨导入用 `template import-track`。
2. **图片被当视频：** 先 probe，再为图片明确目标时长。
3. **同名资源误选：** 使用稳定资源 ID 和哈希，不按标题猜测。
4. **下载后直接宣称完成：** 下载收据不等于已加入草稿。
5. **应用超时后重试：** 先检查草稿和任务状态，避免重复片段。

## 安全与数据

只读取用户授权路径，不上传本地素材，除非用户对精确文件、Provider、用途和有效期另行批准；凭据不进入技能、命令参数或日志。

最小隔离编辑合同见 [examples/minimal-job.json](examples/minimal-job.json)。
