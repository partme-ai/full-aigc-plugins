---
name: vectorcraft-sticker-offset-border
description: 当用户需要保留原稿的白边轮廓时使用；按VectorCraft真实CLI或同会话MCP逐步绑定对象ID、几何参数和选择状态，检查保存重开后的可编辑结构及实际渲染。
license: Apache-2.0
---

# 保留原稿的白边轮廓

先读[方法和参数](references/craft-methods.md)，再按[批次配方](references/craft-steps.json)用真实返回ID执行。

输入为已确认的闭合矢量图形，先明确向外偏移距离与连接样式。图像、文字、复杂自交轮廓不能直接套用此单矩形样例。

为100×60pt原稿生成向外8pt白边，保留原稿几何和颜色，轮廓位于原稿之后、底色之前，保存重开后可分别编辑。

方法、参数和批次均在本技能内。不要将手册中的$ref或capture直接当原生命令参数；不要在已有作品执行file.new。宿主内保持同一个MCP编辑器，CLI文件任务显式保存并重开。

交付原生可编辑工程和约定导出，检查SVG与PNG，不仅判断命令成功。合成例子不代表真实设计质量或目标宿主同步已验收。
