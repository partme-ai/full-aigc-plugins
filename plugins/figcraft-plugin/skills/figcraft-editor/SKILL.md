---
name: figcraft-editor
description: 当需要在智能体宿主内打开 FigCraft、检查当前界面是否与 MCP 同会话、或诊断 Web 文件保存能力时使用。
license: Apache-2.0
---

# FigCraft 内嵌编辑器

1. 调用当前插件的 `open_editor`，首次传入任务工作区绝对路径。支持 MCP Apps 的宿主渲染返回的 UI 资源。
2. 未自动呈现时调用 `open_browser_editor`，用宿主内置浏览器打开实际返回的 `editorUrl`。Codex Desktop 可使用 `open_in_codex` 的 browser target；不要猜端口。
3. 调用 `editor_status` 并核对页面实际就绪。不能把返回 URL、HTTP 200 当成画面已打开。
4. 只使用当前同一服务列出的编辑工具，先检查工具 schema。官方原版 Web 与增强 Web 的命令、文件能力不同，按返回的能力和版本处理。
5. 增强版完成编辑后保存到工作区新路径，重开并检查结构及画面。官方 Web 0.6.0 没有文件 Services，不能承诺原版页面可保存；原生 CLI 会话与页面是独立的。
6. 宿主仅支持 stdio MCP 而不支持 MCP Apps/内置浏览器时，明确无法在其内部显示；外部浏览器不能算内部打开验收。

[上游 Web 实现](https://github.com/storytold/figcraft/blob/v0.6.0/apps/figcraft-web/src/web.rs)。插件本地候选需先构建 `ui/dist/adapter.mjs`。不安装、升级或更改宿主设置来绕过缺失能力。
