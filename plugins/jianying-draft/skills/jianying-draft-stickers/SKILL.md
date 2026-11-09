---
name: jianying-draft-stickers
description: "Search, filter, preview, download, place, transform, duplicate, remove, and verify JianYing stickers with resource receipts and released Rust timeline commands."
license: Apache-2.0
---

# JianYing Stickers

用于剪映“贴纸”面板。贴纸必须先获得稳定资源身份和授权，再按时间、位置、缩放和旋转加入草稿。

## 什么时候使用

- 查找热门、Vlog、互动、遮挡、节日、电商或品牌贴纸。
- 下载并添加官方贴纸，或移动、复制、删除已有贴纸。
- 对贴纸的时间范围、层级和安全区进行验证。

## 能力边界

- ✅ 能做：贴纸候选检索、预览/下载计划、时间线添加、移动、复制、删除和检查。
- ⚠️ 需要条件：官方贴纸要权益收据；写入要隔离草稿；布局结论要播放。
- ❌ 不该用：不生成新贴纸图像、不猜资源 ID、不把贴纸用于未授权商标或肖像。

## 快速开始

可以直接说：“找一个 Vlog 旅行箭头贴纸”“在 3–5 秒加数据图表贴纸”“删除遮挡字幕的贴纸”。首次使用加载 [功能动线](references/workflow.md)。

## 运行契约

- 触发条件：用户要求贴纸搜索、筛选、下载、添加、调整、复制或删除。
- 所需 capability：`media.sticker`、`media.official_resource`、`media.official_resource_apply`、`timeline.edit`、`timeline.duplicate`、`timeline.remove`。
- 最低 CLI 版本：`1.6.19`；本地已知资源可走 `media add-sticker`，官方下载/应用仍以 capability 和 Adapter 为准。
- 默认风险：`reversible_write`。
- 输入事实：资源 ID、版型和授权、起点/时长、位置、缩放、旋转、轨道层级与画面安全区。
- 确认点：下载受限资源、写入草稿、覆盖品牌元素或原生播放分别确认。
- 成功证据：`playback`；缩略图和材料条目不能证明贴纸在正确画面位置。
- 禁止行为：不得凭名称猜资源 ID、把会员标识当商业授权、遮挡受保护字幕/人脸或在无状态回读时重复下载。

## 工作流

### Step 1 — 检索候选
根据目的、风格、画幅、权益和用途检索候选并预览。

### Step 2 — 取得资源
下载后登记官方资源收据，或确认本地资源 ID 已存在。

### Step 3 — 添加与变换
按 [功能动线](references/workflow.md) 加入隔离草稿并调整时间/变换。

### Step 4 — 验证
验证材料、轨道、时间范围，再播放检查遮挡、边缘和节奏。

### Step 5 — 恢复
不通过时局部删除/移动；下载或应用 ambiguous 时查询而非重提。

## Rules

- 候选先过授权、版型和用途门禁，再按风格排序。
- 贴纸必须绑定明确时间范围和安全区。
- 所有变换使用绝对值和 segment ID。
- 下载、应用和播放是三种不同证据。

## Gotchas

1. **会员图标被当许可证：** 专业版权益不自动覆盖商业发布权。
2. **贴纸遮挡字幕：** 应用前检查安全区和受保护对象。
3. **同屏堆叠过多：** 按简报限制密度，不因候选多而全用。
4. **复制共享状态：** 验证副本材料和变换是否独立。
5. **下载超时重复点击：** 先查询资源状态和本地缓存身份。

## 安全与数据

不收集账号秘密；官方资源只保存最小权益快照、资源 ID、文件摘要和用途，避免记录无关账户信息。

最小 Job 见 [examples/minimal-job.json](examples/minimal-job.json)。
