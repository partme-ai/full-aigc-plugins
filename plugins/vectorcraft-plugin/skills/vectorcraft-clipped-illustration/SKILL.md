---
name: vectorcraft-clipped-illustration
description: 当用户需要可释放的裁切蒙版插画时使用；按VectorCraft真实CLI或同会话MCP逐步绑定对象ID、几何参数和选择状态，检查保存重开后的可编辑结构及实际渲染。
license: Apache-2.0
---

# 可释放的裁切蒙版插画

先读[方法和参数](references/craft-methods.md)，再按[批次配方](references/craft-steps.json)用真实返回ID执行。

新建独立矢量插画样例；真实任务先明确保留范围、哪些对象参与蒙版和最上层遮罩路径。已有作品只选择获授权的对象，不select.all。

用圆形蒙版显示两块色面，原始矩形不被裁掉；保存重开后仍有Clip Group和完整子对象，另存副本释放蒙版后恢复外围内容。

方法、参数和批次均在本技能内。不要将手册中的$ref或capture直接当原生命令参数；不要在已有作品执行file.new。宿主内保持同一个MCP编辑器，CLI文件任务显式保存并重开。

交付原生可编辑工程和约定导出，检查SVG与PNG，不仅判断命令成功。合成例子不代表真实设计质量或目标宿主同步已验收。
