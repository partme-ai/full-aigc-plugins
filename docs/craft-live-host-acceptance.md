# Craft 真实宿主验收（2026-10-16）

13 个编辑器已在 Codex 内置浏览器和 ZCode 侧栏显示真实 MCP 操作产生的变化。Kimi 0.43.1 Web 的原生工具调用可用，但此次没有加载编辑器，`attached:false`，内嵌验收未通过。三宿主整体任务仍未完成。

## 验证方式与边界

- Codex 0.162.1：原生安装器安装，实际 `codex app-server` 的 `mcpServer/tool/call` 调用安装包，Codex 桌面内置浏览器加载同会话地址；逐项检查可见截图。没有用 MCP SDK 代替。此项证明原生工具路由与浏览器同步，不证明模型自动选技能、自动打开浏览器或全部场景技能质量。
- ZCode CLI 0.16.9 对应本机桌面：聊天中由真实 Agent 调用 MCP，宿主打开 MCP App 侧栏，再检查画面。Design 热更新期间出现 Not connected 和旧 WASM CSP 错误；修复构建、更新安装、重新加载面板并重试 open_editor 后通过。这不是所有冷启动都无需重试的证明。
- Kimi 0.43.1 Web：真实 K2.8 Preview 会话调用 WordCraft 的 open_editor、editor_status、open_browser_editor。服务返回地址，但始终未附着，未执行创建、输入和保存；没有用外部浏览器绕过。其余 12 个插件仅保留原生安装/发现证据，未宣称 Kimi 编辑通过。结论仅限本次测试版本和会话。

## 最小可见用例

下列通过仅指对应最小用例，不代表全部场景技能通过。

| 插件 | 实际可见变化 | Codex | ZCode |
| --- | --- | --- | --- |
| CADCraft | 圆形、缩放、DXF 文件名 | 通过 | 恢复后通过 |
| DesignCraft | 新文本框及测试文字 | 通过 | 更新与重连后通过 |
| PhotoCraft | 白底文档与命名图层 | 通过 | 恢复后通过 |
| FigCraft | 命名的蓝色矩形 | 通过 | 通过 |
| PrintCraft / PdfCraft | 从文本创建的 PDF，页面文字可见 | 通过 | 恢复后通过 |
| VectorCraft | 彩色矩形 | 通过 | 通过 |
| DeckCraft | 幻灯片标题、正文或图形 | 通过 | 通过 |
| SoundCraft | 音频轨道与片段 | 通过 | 通过 |
| GridCraft | A1 单元格文字 | 通过 | 通过 |
| WordCraft | 文档正文，自动离开起始页 | 通过 | 通过 |
| EffectCraft | 蓝色色块与对应合成图层 | 通过 | 兼容渲染修复后通过 |
| FilmCraft | 时间线片段与 Program 图像 | 通过 | 兼容渲染修复后通过 |
| LightCraft | 测试图片与缩略图更新 | 通过 | 通过 |

## 修复与回归

1. HTML 资源携带 WASM 能力元数据；宿主专属键保留在协议文件，产品运行代码使用通用元数据配置。
2. Effect/Film/Light 面板通过 MCP 读取资源，避免依赖宿主禁止的 localhost iframe 导航。分块校验 SHA-256，限制路径穿越和符号链接越界。
3. 只改写 ESM 引用，不改写同名 WASM import-object 键；保留 classic bootstrap。官方磁盘资源保持原字节，适配发生在插件加载层。
4. Effect 面板使用兼容 WebGL/无 worker 路径，Film 面板使用 WebGL，修复嵌入渲染问题。
5. Word 创建/打开后关闭起始页；WebGL 截图保留 drawing buffer，修复黑屏。
6. Design 候选适配器与源码不同步，重新构建并通过原生安装器更新。
7. Effect、Film、Light、Word 的 npm test 原先指向不存在的 tests 目录，运行 0 项；修正后分别运行 4、4、4、2 项，全部通过。13 组宿主清单版本检查与便携入口检查通过。

## 产物与证据

最终本地市场：`.local/Craft Recovered Final Market/`。13 个 ZIP 和 SHA-256 清单：`.local/craft-host-recovered-final/index.json`。候选包含运行资源，可以搬迁。

最终逐文件复核：13 个包共 786 个运行资源，与 Codex、ZCode 安装缓存均一致，差异数为 0。此项是产物一致性检查，不替代前述画面验收；后续刷新了六个已通过 ZCode 用例的截图缓冲修复版本，没有把刷新安装本身计作新的画面用例。

本机证据不随插件发布：

- `.local/live-host-acceptance/screenshots/`：前期真实宿主面板截图；旧 CAD/Design/Photo/Print 空白或加载截图不计通过，由恢复截图替代。
- `.local/live-host-recovery/`：Codex 全 13 项原生 RPC、产物与截图，四项 ZCode 恢复截图，Kimi 未附着截图。
- `.local/live-host-final-recovery/`：最新安装后的 Design、Print、Vector、Effect、Film、Light 的 Codex 原生调用、产物与截图，以及候选和安装资源摘要核对。
- `.local/live-host-retest/`、`.local/live-host-final/`：清理或浏览器中断导致的失败记录，不能作为通过证据。

部分最新版下载返回 HTTP 403/404，本次实际使用内置版本，不声称成功取得最新版。没有运行 CI，没有提交、推送或发布。

Kimi 当前会话缺少实际加载编辑器的宿主入口。仅返回 URL 不能建立同会话编辑器，插件不能单靠 stdio 强制宿主渲染页面。三宿主任务保持未勾选；需要 Kimi 可用的内嵌入口或 MCP Apps 支持后再完成可见编辑验收。Windows/Linux、全部场景技能、复杂创作质量不包含在通过结论内。
