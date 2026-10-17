---
name: effectcraft-harness
description: EffectCraft 内置执行 harness——所有 effectcraft 领域技能（effectcraft-use、effectcraft-cli 及各场景技能）的统一执行通道。执行 plan/run/inspect、原生命令调用、workflow 编排或首次安装 EffectCraft CLI 时，经由本技能的入口脚本执行；领域技能只提供场景知识、计划与示例，不自带脚本。
license: Apache-2.0
---

# EffectCraft Harness（内置执行通道）

本技能是 EffectCraft 技能套件的**唯一执行实现**：任务恢复账本、隔离 Python 准备、原生命令会话、评审与修订都收敛在本目录 `scripts/` 内。`effectcraft-use`、`effectcraft-cli` 及各领域技能是薄文档技能——它们提供场景指引、计划示例与参考契约，实际执行一律经由本技能的入口。**执行任何 EffectCraft 命令前，先把 `HARNESS_DIR` 设为本 `SKILL.md` 所在目录（宿主实际加载的绝对路径），不要假设当前工作目录就是技能目录。** 用户级安装可能位于 `~/.agents/skills/effectcraft-harness`，项目级可能位于 `.agents/skills/effectcraft-harness`，插件可能位于其 `skills/effectcraft-harness` 或宿主缓存目录；以宿主实际加载路径为准。

## 六个入口

| 入口 | 用途 |
|---|---|
| `scripts/launch.sh` | POSIX 受管理入口（推荐）。自动准备用户目录内的固定 Python 与 EffectCraft，不改全局 PATH；覆盖 plan / run / inspect / resume / review / revise / cancel 等任务动作。 |
| `scripts/launch.ps1` | Windows PowerShell 受管理入口，语义与 `launch.sh` 一致。 |
| `scripts/cli.py` | 已隔离 Python 就绪时的直接 CLI 通道（诊断与兼容用途，不绕过任务账本合同）。 |
| `scripts/commands.py` | 原生命令单技能入口：`list_commands` / `execute_command` / 参数目录与实时前置检查。 |
| `scripts/workflow.py` | 原生合成计划执行器，被 `launch.sh`/`launch.ps1` 的 workflow 模式内部复用；一般不直接调用。 |
| `scripts/bootstrap.py` | 首次使用安装器：准备锁定的隔离 Python 3.13 并下载校验官方 EffectCraft 制品，返回 JSON `executable`。 |

## 用法

创作写入默认使用受管理入口（以 `effectcraft-use` 等领域技能中的场景指引为准，计划与示例文件取自对应领域技能目录）：

```sh
HARNESS_DIR=/absolute/path/to/effectcraft-harness
/bin/sh "$HARNESS_DIR/scripts/launch.sh" plan --mode workflow --plan PLAN.json --output /absolute/new-result
/bin/sh "$HARNESS_DIR/scripts/launch.sh" run --mode workflow --plan PLAN.json --output /absolute/new-result
```

Windows PowerShell：`& "$HARNESS_DIR/scripts/launch.ps1" run --mode workflow --plan PLAN.json --output "C:\Users\me\result"`。
原生命令计划追加 `--mode commands`，自有桌面会话使用 `--mode desktop`。

首次安装（无预装 Python；安装范围是用户数据目录，不需要 sudo）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
```

原生命令直连与命令目录查询（cli.py 的原生子命令须放在 `--` 之后；commands.py 输出恒为 JSON）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- info --json
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter <关键词>
```

## 领域技能与本 harness 的关系

- `effectcraft-use`：完整任务路由与交付合同；执行仍走本 harness。
- `effectcraft-cli` 与各场景技能（project/footage/composition/layers/animation/effects/masks/expressions/camera/export/tracking/puppet/setup）：场景知识与参数契约；执行仍走本 harness。
- 领域技能文档中的 `SKILL_DIR` 指领域技能自身目录（用于读取其 `examples/`、`references/`）；脚本执行路径一律换成本目录 `HARNESS_DIR/scripts/`。
- 执行合同（任务恢复账本、评审、修订、资源预算）见 `effectcraft-use` 技能的 `references/managed-execution.md`。
