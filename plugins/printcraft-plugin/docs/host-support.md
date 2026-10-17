# 宿主支持矩阵

| 宿主 | 打包 | 当前证据 | 限制 |
|---|---|---|---|
| Codex CLI 0.153.4 | portable + 生成 `.codex-plugin/plugin.json` | 含中文/空格的隔离 marketplace 安装；plugin/read 实际加载 7 项技能/界面元数据 | gpt-6-astra 要求更新版 CLI；可用 gpt-5.6-sol 单独测试 |
| Claude Code | portable 结构 | NOT_RUN | 没有实际安装/模型验收，不宣称支持已通过 |
| Gemini/OpenCode/其他 | portable 结构 | NOT_RUN | 不凭 manifest 推导实际支持 |
| Codex CLI 0.147.0 | dev.5 portable + 生成 Codex 清单 | 公开 tag / 公开市场安装；七项技能；gpt-5.6-sol 实际 PDF 保存重开 | 当前实测，范围为原创夹具 |
| Claude Code | .claude-plugin/plugin.json + .mcp.json | 本地 CLI 清单校验 | 原生加载/模型 NOT_RUN |
| Kimi Code | 生成 kimi.plugin.json | 打包身份校验 | 加载/模型 NOT_RUN |

Codex `skills/list` 不等同插件组件列表；以 `plugin/read` 查看插件七项技能，加载名为 `printcraft:<技能名>`。界面清单由 scripts/generate_host_manifest.py 从根清单生成；不可手工漂移。

本地验收使用临时 CODEX_HOME，现有登录以临时文件链接复用并在测试结束移除，没有复制/归档凭据。当前正式用户配置未修改。实际模型命令与结果见 verification/；模型列出技能不代替运行技能脚本。

0.153.4 为此前 dev.3 的历史环境；dev.5 当前公开安装使用 0.147.0，不把两者混同。
