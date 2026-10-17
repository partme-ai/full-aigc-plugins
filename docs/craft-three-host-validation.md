# 三宿主安装与 MCP 验证（2026-10-16）

> 本文保留早期安装与 SDK 边界检查。后续真实宿主调用、内嵌修复和当前阻塞以 [真实宿主验收](craft-live-host-acceptance.md) 为准；下文未执行项和缓存清理描述属于早期阶段。

13 个插件均已补齐原生入口，所有主体/宿主清单版本一致。完整候选通过 Agent Plugins 1.0.0 的 26 项官方 plugin/mcp Schema 检查。逐插件版本、技能数量与适配器摘要见 [机器可读结果](craft-three-host-validation.json)。安装方法见 [三宿主安装说明](craft-three-host-installation.md)。

| 实际检查 | Codex 0.162.1 | ZCode CLI 0.16.9 | Kimi 0.43.1 |
| --- | --- | --- | --- |
| 原生安装器安装完整包 | 13/13 | 13/13 | 13/13 |
| 宿主发现本市场技能 | 173 | 173 | 173 |
| 原生 MCP 连接/发现 | 13/13 | 13/13 | 13/13 |
| 实际 editor_status + open_browser_editor | 26 次，通过原生 app-server 调用 | 26 次，SDK 启动真实安装缓存中的配置 | 26 次，SDK 使用原生安装包及 Kimi Node 兼容入口 |
| 完整桌面内嵌交互验收 | 本轮未执行 | 无界面 app-server 返回 MCP App connection is unavailable | 本轮未执行 |

共 39 个原生安装实例及 78 次实际工具调用。SDK 测试不模拟返回值，但不能替代宿主 Agent 的模型调度或桌面面板交互；只有 Codex 的调用记录经过原生 app-server 工具路由。ZCode/Kimi 原生握手与工具发现由宿主自身完成，工具调用另测安装包。

本轮修复了两项动态缺陷：Kimi 内置运行方式下 `process.execPath` 指向宿主可执行文件，子编辑器因此启动失败，现改为显式 `node`；CAD/Deck 的外部 CLI MCP 移至可选 `hosts/native-cli/mcp.json`，默认安装只启动包内编辑器，不再出现缺少 CLI 的启动失败。

产品运行包 HTML/JavaScript/CSS 全量检查未发现外部宿主品牌字符串。宿主协议文件名与宿主安装说明保留原名，第三方许可不篡改。15 项更新/安全回归和 6 项 PrintCraft manifest 回归通过。WASM 内容沿用前次已验证的运行包，本轮没有改写官方源码或重新编译 WASM。

Codex、Kimi 安装使用独立数据目录。ZCode 的数据目录环境变量没有隔离 CLI 插件缓存，因而本轮安装落在用户 CLI 缓存的独立 craft-use-local 市场；该市场与本轮 13 个安装项在验证后清理，不触及其他市场插件。原生宿主输出、失败记录及最终回归保存在本机 `.local/host-acceptance/`，不随插件发布。

完整候选位于 `.local/Craft Use Three Hosts/`，13 个 ZIP 位于 `.local/craft-three-host-final/`。安装后的核心清单与适配器与最终候选逐字节核对。候选尚未发布、提交或推送；Windows/Linux、本轮未验证的桌面呈现、模型自动选择技能和全部场景创作质量不包含在通过结论中。
