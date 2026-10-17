# Commands、Hooks、Skills 与 MCP 边界

> 2026-10-09；这是插件组成合同，不是已实现 API。

| 能力 | Agent Plugins 1.0.0 位置 | 使用条件 | 验证 |
|---|---|---|---|
| Manifest | 根 `plugin.json` | 必需；`$schema` 与 `name` 合法 | 官方 Schema 与路径语义 |
| Skills | `skills/<name>/SKILL.md` | 有需要的操作知识，单技能资源自包含 | frontmatter、孤立安装、触发场景 |
| MCP server | 根 `mcp.json` | 连接已有 `deckcraft-cli mcp` | CLI 定位、握手、工具调用 |
| 用户命令 | 客户端扩展 | 目标客户端确有独立命令入口需要 | 该客户端实际加载 |
| Hooks | 客户端扩展 | 明确的事件和动作无法由 Skill/MCP 满足 | 该客户端事件回归 |

核心 manifest 不能增加自造的 `commands`、`hooks` 或 `mcpServers` 顶层字段；MCP 配置不能内嵌在 manifest。客户端专有数据置于 `extensions` 的反向域名命名空间，文件置于同名顶层目录。规范见 [组件发现](https://agent-plugins.org/specification) 与 [客户端扩展](https://agent-plugins.org/plugin-authors/client-extensions)。

## 现有能力的最短路径

`deckcraft-cli mcp` 已提供创建、编辑、inspect 和 render 等工具。插件只声明连接、携带必要 Skills；宿主处理权限与执行，DeckCraft 处理文稿。需要显式快捷入口时，可用已验证的客户端命令调用这些能力，不另建业务 API。

## 失败处理

CLI 缺失、MCP 握手失败或工具错误要按真实阶段报告。MCP 失效不应使合法 Skills 一同失效；客户端按规范处理组件故障边界。文件导出要核对返回、目标文件和重新打开的结果。
上游 Remote 会在传输错误后重发修改请求，因此断连后的状态可能不确定。此时先回读文稿并报告已确认内容和未知部分；不能声称插件已经提供自动去重、事务回滚或远端取消。若要补小型脚本，先提供复现、现成能力调查和行为回归。
