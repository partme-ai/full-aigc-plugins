---
name: figcraft-prototype-flow
description: 当需要用 FigCraft 将多个页面连成可点击原型，设置入口、返回、弹层或交互状态时使用。
license: Apache-2.0
---

# 交互原型


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 连接与执行

先检查当前 MCP 的工具列表和 `editor_status`。有 `create_node`、`run_command`、`inspect_document` 时，使用实际工具 JSON schema；不猜测参数。通过 `list_commands` 找到本场景需要的命令及参数，再执行。

增强 Web 的 MCP 操作必须发生在已打开且就绪的同一页面。官方原版 Web 0.6.0 只有交互画面，文件服务尚未实现；没有这些 MCP 工具时不得假装已编辑或保存。独立原生 `figcraft-cli mcp` 是另一会话，切换必须明确告知。CLI 可用时用 `figcraft-cli commands --json` 检查命令；不自行安装缺失工具。

参考：[FigCraft v0.6.0 MCP](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)、[CLI](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)。命令以当前加载版本为准。

## 工作步骤

1. 先写出用户任务、入口、成功路径、取消和错误返回路径；确认当前页面是否覆盖这些状态。
2. 为页面与关键按钮命名，通过 inspect_document 获取节点 ID；使用 list_commands 查询 proto.interaction.add 和当前版本的 flow、transition 参数。
3. 逐个连接主要动作，明确目标 frame、触发方式、过渡与返回行为；不虚构尚未提供的后端响应。
4. 在内嵌页面实际运行原型，从入口逐步点击到成功及取消状态，检查返回栈和是否存在死路；静态连线存在不能代替点击验收。
5. 保存并重开验证连线；导出页面概览和交互说明，标注真实可点击路径与只作说明的状态。
