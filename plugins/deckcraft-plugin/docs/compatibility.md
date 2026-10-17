# 兼容性与能力边界

> 2026-10-09；含固定源码的本地 headless 冒烟测试；宿主与完整格式兼容性未验证。

## 1. 固定参考

| 来源 | 固定版本 / 提交 | 本轮证据 |
|---|---|---|
| DeckCraft | 0.3.0 / d0e57d7e25f9852179cc66be12dd6188f1c05535 | 当前本地源码 |
| dreamina-skills | 1.7.1 / 42f0e38ab114d271e2f999483ef83a6ebbddc4f3 | README、技能资源与验证文档 |
| dreamina-canvas-plugin | 0.4.3 / 3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b | 控制器、manifest、锁和验证记录 |

DeckCraft 编译清单声明 Rust 1.90、edition 2024。这属于上游工具链要求，不是本仓已交付 Rust 程序。[来源](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/Cargo.toml)

## 2. 模式

| 操作 | Headless | Remote | 本项目验证 |
|---|---|---|---|
| 命令发现、编辑、文档检查 | 上游存在 | 上游存在 | Headless 本地冒烟 PASS；Remote NOT_RUN |
| 幻灯片渲染 | CPU 渲染 | 可通过控制接口渲染 | Headless 单页 PNG 冒烟 PASS；Remote NOT_RUN |
| 整窗截图、真实菜单点击 | 不支持 | 需要运行中的桌面应用 | NOT_RUN |
| 放映、媒体输出 | 不应承诺完整宿主行为 | 依赖 UI 和音频设备 | NOT_RUN |
| Web 文件打开/保存 | 浏览器选择与下载 | 不提供本机 TCP 宿主 | NOT_RUN |

[CLI](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/apps/deckcraft-cli/src/main.rs)、[Headless](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/crates/mcp/src/headless.rs)、[Web](https://github.com/storytold/deckcraft/blob/d0e57d7e25f9852179cc66be12dd6188f1c05535/apps/deckcraft-web/src/web.rs) 是接口证据。

## 3. 格式

`.deckcraft` 是 ZIP+JSON 与媒体；PPTX 采用宽容导入，跳过未知或损坏部分时可能丢失内容；PDF 图稿为栅格加真实文本层；PNG/JPEG 是视觉产物，不能代替可编辑文稿。
需要分别验证导入、导出、重开、文本、母版、媒体、动画和视觉差异。外部 PPTX 测试没有 `DECKCRAFT_PPTX_IN` 时返回，不代表真实语料已验证。

## 4. 宿主与分发

本项目没有 Codex、Claude Code、Craft、Kimi 或其他宿主的已验证版本范围。manifest 校验通过将只证明结构合法；加载、执行、卸载和恢复需要真实宿主验证。禁止复制 Dreamina 的兼容表作为本项目结论。
