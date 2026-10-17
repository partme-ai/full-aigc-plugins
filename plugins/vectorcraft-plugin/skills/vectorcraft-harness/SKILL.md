---
name: vectorcraft-harness
description: VectorCraft 内置执行 harness——所有 vectorcraft 领域技能（vectorcraft-use、vectorcraft-cli 及各场景技能）的统一执行通道。首次安装固定 CLI、查询或执行原生命令、workflow 编排、桌面桥接或连续任务会话时，经由本技能的入口脚本执行；领域技能只提供场景知识、计划与示例，不自带脚本。
license: Apache-2.0
---

# VectorCraft Harness（内置执行通道）

本技能是 VectorCraft 技能套件的**唯一执行实现**：首次安装、原生命令调用、workflow 编排、桌面桥接与交付核验都收敛在本目录 `scripts/` 内。`vectorcraft-use`、`vectorcraft-cli` 及各领域技能是薄文档技能——它们提供场景指引、计划示例与参考契约，实际执行一律经由本技能的入口。**执行任何 VectorCraft 脚本前，先把 `HARNESS_DIR` 设为本 `SKILL.md` 所在目录（宿主实际加载的绝对路径），不要假设当前工作目录就是技能目录。** 用户级安装可能位于 `~/.agents/skills/vectorcraft-harness`，项目级可能位于 `.agents/skills/vectorcraft-harness`，插件可能位于其 `skills/vectorcraft-harness` 或宿主缓存目录；以宿主实际加载路径为准。领域技能文档中的 `SKILL_DIR` 指领域技能自身目录（用于读取其 `examples/`、`references/`），与本 harness 是两个位置。

## 入口

| 入口 | 用途 |
|---|---|
| `scripts/bootstrap.py` | 首次使用安装器：仅用标准库安装锁定的官方 CLI（`runtime.lock.json` 固定版本与摘要），返回 JSON `executable`。 |
| `scripts/cli.py` | 公开 CLI 通道：按 argv 调用固定二进制；`--` 后放原生子命令。 |
| `scripts/commands.py` | 原生命令单技能入口：`list` / `describe` / `run`，参数说明、实时前置检查、同会话调用及失败回执。 |
| `scripts/workflow.py` | 原生矢量操作助手：独立会话、限定读写目录和不可变修订交付；多画板导出与定向改色。 |
| `scripts/desktop.py` | 桌面桥接：按固定官方 DMG 安装桌面应用并执行桌面计划；与 CLI 缓存分离。 |

其余 `scripts/` 文件是上述入口的内部依赖（安全边界、会话与合同模块），不单独调用。

## 用法

场景指引、计划与示例文件取自对应领域技能目录（`SKILL_DIR/examples/`、`SKILL_DIR/references/`）；执行路径一律使用本目录 `HARNESS_DIR/scripts/`。

首次安装（无预装 CLI 时；安装范围是用户数据目录，不需要 sudo）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
```

安装器返回 JSON `executable`，后续将其作为 argv 的第一个元素。当前锁定平台为 macOS arm64；未支持的平台返回 `unsupported_platform`，不要安装别的平台制品。安装位置默认 `~/.local/share/craft-runtimes`，可用 `--runtime-home` 或 `CRAFT_RUNTIME_HOME` 指定；`--archive` 接受已下载的锁定 ZIP，但不跳过摘要检查。

原生命令直连与命令目录查询（cli.py 的原生子命令须放在 `--` 之后；commands.py 输出恒为 JSON）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- --version
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- commands
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter QUERY
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe COMMAND_ID
```

若使用 MCP，显式选择 `mcp --headless`，避免默认自动连接正在使用的桌面文档。桌面安装与 GUI 计划见领域技能的 [固定桌面安装] 参考，入口为 `scripts/desktop.py`。

## 领域技能与本 harness 的关系

- `vectorcraft-use`：完整任务路由与交付合同；执行仍走本 harness。
- `vectorcraft-cli` 与各场景技能（setup/project/paths/shapes/boolean/text/appearance/artboards/assets/export/selection）：场景知识与参数契约；执行仍走本 harness。
- 领域技能文档引用脚本时一律写作 `$HARNESS_DIR/scripts/<入口>`；`references/` 中的执行契约 JSON（command-coverage、native-command-snapshot）在本技能内与 `vectorcraft-use` 保持字节一致，领域技能各自保留其场景参考。
- 交付前重开工程并核对各画板与导出范围；只读检查无需安装运行时。

## 当前范围

固定 CLI 的版本与制品摘要以本技能 `scripts/runtime.lock.json` 为准；技能包版本以对应发布标签为准。独立安装复验与全量逐命令验收分别记录，不以发布替代验收。目录覆盖与直接原生使用不等于所有指令、GUI、交付或 Art 编排已验收。
