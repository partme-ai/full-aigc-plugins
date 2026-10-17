# Craft Use 便携插件安装

当前已增加 Codex、ZCode、Kimi 原生适配及真实安装检查；参见 [三宿主安装说明](craft-three-host-installation.md) 和 [验证结果](craft-three-host-validation.md)。本页下方保留早期标准/Codex/Claude 路径测试说明。WorkBuddy 的逐项绝对路径配置不作为本轮安装交付。

## 包结构

完整市场包包含 plugins/ 下的 13 个独立插件，以及根目录的 .agents/plugins/marketplace.json 和 .claude-plugin/marketplace.json。两个市场清单均相对本市场根目录引用插件，因此可以整体复制到其他位置。

| 宿主 | 插件清单 | MCP 路径基准 |
| --- | --- | --- |
| 标准规范宿主 | plugin.json | mcp.json 的 PLUGIN_ROOT |
| Codex | .codex-plugin/plugin.json | 独立 MCP 清单中的相对 cwd 解析为插件根 |
| Claude Code | .claude-plugin/plugin.json | 根 .mcp.json 的 CLAUDE_PLUGIN_ROOT |

在 Claude Code 使用 `/plugin marketplace add` 添加市场目录，然后使用 `/plugin install photocraft@craft-use-local` 安装目标插件。Codex 使用本地插件市场入口添加该市场目录，再选择插件。目录只登记一次，不需要手写每个 MCP 的绝对路径。运行需要 Node.js 24+，不需要 Rust 或 node_modules。开发源码检出本身不包含忽略的运行制品，安装必须使用完整构建包。

## 同会话操作

打开工具时显式传入本次任务 workspace。任务目录与插件安装目录分离；不要写死进插件清单。支持 MCP Apps 的宿主可以渲染 UI 资源；支持内置浏览器的宿主可打开 open_browser_editor 返回地址。Claude Code 终端没有内嵌浏览器，stdio 也不提供界面容器。

等待 editor_status 就绪后执行编辑，保存源工程并重开检查。编辑器更新只选择兼容发行，失败回退内置包，活动会话保持固定版本。

## 验证边界

早期便携性检查执行官方 Claude Code 清单校验、含空格搬迁目录的三种入口 stdio 启动测试，以及同会话编辑回归。入口测试按宿主公开路径规则解析清单，不冒充原生安装验收；当时未全局安装或发布。具体结果见 craft-portable-validation.json。

产品配置、源码和安装文档使用自己的命名。第三方许可与来源不得伪造；历史测试记录保留原始信息但不进入新分发包。research 参考资料不属于产品改写范围。
