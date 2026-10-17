---
name: vectorcraft-sticker-grid
description: 当用户需要可调整行列的贴纸阵列时使用；按VectorCraft真实CLI或同会话MCP逐步绑定对象ID、几何参数和选择状态，检查保存重开后的可编辑结构及实际渲染。
license: Apache-2.0
---

# 可调整行列的贴纸阵列

先读[方法和参数](references/craft-methods.md)，再按[批次配方](references/craft-steps.json)用真实返回ID执行。

确认单个贴纸尺寸、行列数、水平/垂直净间距和画板范围。例子是30×30pt源图、20pt净间距、3行4列，不是自动填满纸张或印刷拼版。

保存为可编辑Grid Repeat，原稿仅有一个源图；重开可改行列、改源图颜色并同步实例，另存展开副本得到12个真实独立图形。

方法、参数和批次均在本技能内。不要将手册中的$ref或capture直接当原生命令参数；不要在已有作品执行file.new。宿主内保持同一个MCP编辑器，CLI文件任务显式保存并重开。

交付原生可编辑工程和约定导出，检查SVG与PNG，不仅判断命令成功。合成例子不代表真实设计质量或目标宿主同步已验收。
