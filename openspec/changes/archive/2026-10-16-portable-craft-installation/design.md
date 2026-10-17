# 设计
标准 mcp.json 使用 PLUGIN_ROOT，Claude Code 使用 CLAUDE_PLUGIN_ROOT，Codex 兼容清单指向独立 MCP 配置，以插件根为 cwd。三个入口启动同一个包内 adapter。

包安装目录与任务工作区分开；Agent 打开编辑器时传递工作区。MCP Apps 资源与内置浏览器保持同会话。旧宿主专用环境变量、CSP 扩展及 CDN 更新入口退出当前实现。

重新构建含旧运行时描述的 WASM 和 JavaScript，产物输出到独立目录以保护活动会话。第三方许可证与真实来源保持；历史记录不改写、不进入新分发包。通过含空格的搬迁目录与不同工作目录验证启动。
