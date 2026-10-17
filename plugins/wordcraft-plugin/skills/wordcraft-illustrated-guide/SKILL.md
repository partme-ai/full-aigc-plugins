---
name: wordcraft-illustrated-guide
description: 当用户需要带图片题注的操作指南时使用；按WordCraft真实CLI或当前MCP实例组织具体方法、参数和光标状态，保存并检查可编辑结构与实际页面。
license: Apache-2.0
---

# 带图片题注的操作指南

先读[方法与参数](references/craft-methods.md)及[步骤配方](references/craft-steps.json)。

input/config.png与input/connect.png是用户批准的截图，先核对顺序、内容及像素尺寸。单位为pt，不能将像素宽度直接当打印尺寸。

按步骤插图并立即添加连续编号题注；保留图片比例与替代文本，检查两幅嵌入图片、SEQ编号1/2和题注位置，逐页看图文是否分离。

同会话MCP逐条执行且检查返回；独立CLI全部操作保持同进程。光标/选择变动后重新核对，不将另一个CLI工程当作已打开编辑器状态。

输出新的可编辑DOCX并重开，导出PDF逐页检查。具体参数只是技术例子，按真实素材和文档改写；来源固定提交、命令观察与边界都在本技能内，无兄弟技能依赖。
