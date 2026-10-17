# EffectCraft 分段渲染架构

日期：2026-10-07。状态：独立技能源工作区候选；已发布技能 dev.9／插件 dev.10 内容不变。规格事实源为 EffectCraft 插件 `openspec/changes/establish-v1-plugin`，场景 EC-DM-005-SEGMENT，任务 4.25／4.26。

## 问题与目标

当前 v1 透明序列将全序列解码预算限制为 512 MiB。1080p／30 fps 约 64 帧，无法覆盖通常长度的片头。本增量建立有界分段生产器，保留逐帧尺寸、RGBA、透明度、文件与像素摘要检查；不通过提高原 v1 上限处理长序列。

## 结构与状态

```mermaid
flowchart TD
    Input[原生工程与合成设置] --> Plan[有理数帧率与半开帧范围]
    Plan --> Bind[工程及 CLI 摘要绑定检查点]
    Bind --> Lock[取得内核排他锁]
    Lock --> Inspect[重新核验已完成段]
    Inspect -->|有效| Reuse[复用原文件]
    Inspect -->|缺失或损坏| Render[原生渲染到临时目录]
    Render --> Pixels[连续编号与实际 RGBA 检查]
    Pixels --> Commit[发布段并记录清单摘要]
    Reuse --> Next[下一段]
    Commit --> Next
    Next --> Complete[全部完成后发布生产检查点]
```

每段按全局 firstFrame／frameCount 切分，start／end 保存约分后的有理数秒数。原生 CLI 使用全局帧编号；只在临时目录核对完整集合后改为段内编号。已有段不会重新编号。CLI 的时间参数边界最终由真实输出帧集合核验，缺帧或多帧立即拒绝。

`checkpoint.json` 绑定工程 SHA、CLI 二进制 SHA、合成设置、预算和分段范围；`verified.json` 记录各段清单摘要。恢复先核对绑定和摘要，再重新解码检查实际帧；即使同时修改帧与段清单，也不能当作原完成段复用。`render.lock` 使用 macOS／Linux 内核锁，进程退出自动释放；运行中的生产器不能被另一个调用抢占。

`segments.json` 使用内部 `craft-segmented-render-checkpoint/v1`，只有全段通过才标记 verified。各子段仍为原有 `craft-image-sequence/v1`。检查点不是现有 Film／Art 已支持的交付协议，尚不能直接导入其原 v1 路径。

## 资源与文件边界

| 项目 | 候选边界 |
| --- | --- |
| 单段解码预算 | 最大 512 MiB，按分辨率推算段长 |
| 单帧 | 超过单段预算时，安装或渲染前拒绝 |
| 总帧数／逻辑解码量 | 最大 10,000 帧／64 GiB，不代表同时驻留内存 |
| 已验证编码文件总量 | 最大 2 GiB；超过不发布完整检查点 |
| 原生段超时 | 每段 180 秒，失败保留此前已验证段 |
| 并行与路径 | 排他锁；拒绝符号链接与未登记额外文件 |

只修改调用指定的生产目录。源工程、技能目录及已验证的其他段保持不变；发现用户额外文件时拒绝，不删除它们。输入工程或 CLI 摘要变化必须使用新目录，不允许复用旧任务。当前默认平台仍为 macOS arm64；不能由内核锁代码推断 Linux 原生安装已验证。

## 首次使用入口

先通过现有工作流获得可重新打开的 `.ecproj`，从该工程的原生 `native.json` 中提取 composition 对象，另存为 composition.json。以实际加载的 SKILL.md 所在目录设置 SKILL_DIR。

```bash
python3 -I -B "$SKILL_DIR/scripts/segmented_sequence.py" \
  --project /absolute/input/project.ecproj \
  --composition /absolute/input/composition.json \
  --output /absolute/output/segments \
  --chunk-frames 60
```

入口按本技能锁自动安装及校验固定 CLI，不依赖兄弟技能或 PATH。chunk-frames 只缩小段长，不提高 512 MiB 上限。恢复使用相同工程、设置、目录和参数；修改文字后使用新工程版本和新生产目录。候选目前复用同一版本的完整段，不声称完成编辑后跨版本段级失效分析。

## 验证与后续

测试和实际结果记录在 [候选证据](evidence/segment-producer-candidate-20261007.json)。实际原生测试用 320×180、12 fps、12 帧，分成三个四帧段与一次性基准逐帧比对；这不能作为 1080p 长片头验收。

任务 4.26 保持开放：还需接入公开工作流交付、定义由 Art 持有的共享消费合同、实现 Film 的连续帧导入和 Art 的段级故障／移动包处理，再发布不可变源与插件，执行完整长片头、文字返工和首次使用验收。GUI、模型派发、创作质量及跨软件色彩保真不由本候选证明。

## 公开工作流联调候选

当前源码工作流支持 `exports: [{"format":"png-segmented","chunkFrames":60}]`，先保存和收集原生工程，再输出 rgba-segments，并记录完整 imageSequence 及嵌套 PNG 交换记录。chunkFrames 可省略，不能越过单段预算；无效字段／范围和多个导出在安装前拒绝。有界原生 Film 收集和 Art 编排已通过候选联调；4.26 仍等待 HD 与固定发行安装后首次使用。Art 分段架构文档及证据说明候选范围，历史生产器证据保留原源码身份。

[Art 候选联调证据](evidence/art-segment-adapter-candidate-20261007.json) 绑定真实公开分段导出、Film 连续收集和 Art 移动包返工／恢复；使用当前源码与已有核验原生执行器，固定安装后冷使用及 HD 保持开放。

## 当前固定发行补充验收（2026-10-08）

[固定版本证据](evidence/craft-fixed-segmented-hd-refresh-20261008.json)：实际安装的 Film40/source37、Effect38/source34 和 Art117/source89 完成验证。Art 单技能从空运行时公开安装四领域及 Node/core，交付 1920×1080、24 fps、5 秒、120 帧、四段动画；独立解码全部 120 帧。Logo 替换只重建受影响任务，损坏帧拒绝、原字节恢复不重复扣预算，五子工程移动包通过。另一个双领域冷安装用例验证十二帧分段交接、文字返工时非目标动画关键帧不变、移动工程重开和旧交付保全。两个原生用例分别耗时 255.657 秒与 26.797 秒。首次双领域尝试因磁盘满在安装阶段失败，保留诊断，清理关闭缓存后另建空目录成功。

以上补充了前文历史候选阶段缺失的固定发行和 HD 证据；前文未完成说明属于其当时版本。当前修改的指南尚待独立新发行安装验证；本报告不证明新版本、通用 Skills CLI、GUI、创意质量或完整 V1。
