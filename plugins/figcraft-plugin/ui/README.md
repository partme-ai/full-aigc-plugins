# 源码增强编辑器

`source.lock.json` 固定上游源码提交。`runtime/prepare-automation.py` 向该提交的 UI 线程接入原有 MCP dispatcher，并将明确暂存的工作区文件交给引擎读写。原始源码检出不会被修改。

已有 Rust、wasm32-unknown-unknown、匹配 Cargo.lock 的 wasm-bindgen、Node.js 24、esbuild/MCP SDK 依赖与 Chrome 时：

```sh
python3 ui/build-source.py --output /new/build-dir --target-dir /existing/cargo-target
```

脚本不安装工具，不覆盖输出，也不自动替换内置版本。先对生成的 editor 制品执行 `ui/tests/editor-smoke.mjs` 同类回归，通过后再更新 `ui/dist/editor` 与锁文件。`ui/build.mjs` 构建跨宿主适配器。

运行时更新只接受本插件 Release 中 `figcraft-editor-VERSION.zip` 的 `editor/` 目录，校验官方发行摘要及工具接口。没有兼容发行时回退内置。官方原版 Web 缺少自动化接口，不能作为等价运行时更新。

许可与改动归属保留在 `runtime/LICENSE-UPSTREAM`、`runtime/NOTICE.md` 和 editor/licenses 中。

### 源码字体输入

`build-source.py` 按 `fonts.lock.json` 下载并校验 Inter、BIZ UDPGothic、LXGW WenKai，自动应用字体桥接并编入 WASM；无需安装系统字体。字体来源、SHA-256 和 OFL 文本随制品保存。下载失败时源码构建明确失败，不产出缺字体的替代包；运行时更新失败仍使用已经验证的内置编辑器。

## 插件安装与界面

优先通过插件市场安装完整发布包，不需要手工填写每个 MCP 的绝对路径。开发仓必须先构建编辑器资源；仅克隆源码不等于已安装运行包。

| 入口 | 配置 | 路径基准 |
| --- | --- | --- |
| 标准 Agent Plugins | `plugin.json`、`mcp.json` | `${PLUGIN_ROOT}` 由支持该规范的宿主展开 |
| Codex | `.codex-plugin/plugin.json`、`.codex-plugin/mcp.json` | 相对 `cwd` 由宿主定位到插件根目录 |
| Claude Code | `.claude-plugin/plugin.json`、根 `.mcp.json` | `${CLAUDE_PLUGIN_ROOT}` 由宿主展开 |

连接后调用 `open_editor` 或 `open_browser_editor`，显式传入本次任务目录 `workspace`。这是用户文件的位置，不是插件安装位置，不写死在安装清单中。

支持 MCP Apps 的宿主可呈现工具关联的 UI 资源；支持内置浏览器的桌面宿主可打开 `open_browser_editor` 返回的地址。Claude Code 终端本身不提供浏览器面板。支持插件或 stdio MCP 并不自动意味着支持内嵌 UI；缺少 UI 能力时只能在浏览器打开同一会话，不能宣称宿主内嵌已通过。

stdio 负责 Agent 与插件通信，本地 HTTP 负责页面和同会话编辑桥接。Agent 指令作用于当前页面的编辑器状态；等待 `editor_status` 就绪后再执行编辑。保存源工程后重开检查，关闭 MCP 进程前先保存。

本轮优先验证标准插件入口、Codex 和 Claude Code 清单。仅支持 MCP 的工具不属于当前安装交付范围。

### main 开发候选构建

main 字体后备表改为定长数组，源码构建补丁已兼容旧行内列表与新数组，并同步增加数组长度；中文字体输入保持不变。此为构建兼容修复，不代表 main 已完成宿主验收。
