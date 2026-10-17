---
name: effectcraft-cli
description: 查询 EffectCraft 原生命令和参数，或处理镜头跟踪、稳定与图形附着；首次使用安装固定 CLI。
license: Apache-2.0
---

# EffectCraft CLI 公共操作

本技能负责查询实际命令参数和能力，调用公开 CLI、MCP 与诊断。与同包技能按名称交接，单独安装即可使用，不读取兄弟目录。调用固定官方 effectcraft-cli，保留原生编辑工程。

## 输入与交付

输入为用户已确认的任务、素材、工程或对象、输出目录与修改范围；需要现有工程时先核对摘要。返回实际 CLI 结果、保存后的原生工程、需要的派生输出与核验记录。安装成功、命令目录存在与创作任务完成分别报告。

## 默认受管理入口

执行实现收敛在内置的 **effectcraft-harness** 技能（随插件捆绑安装；单独安装用 `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-harness`）。将 `HARNESS_DIR` 设置为该技能实际加载目录（绝对路径）；本技能的 `SKILL_DIR` 只用于读取自身的 `examples/` 与 `references/`。

从宿主实际加载的技能目录设置 `SKILL_DIR`。**创作写入默认使用 `launch.sh` / `launch.ps1`**，自动准备用户目录内的固定 Python 与 EffectCraft，不改全局 PATH。下文原始 Python/CLI 示例保留兼容与诊断用途，不能绕过任务恢复账本。完整操作合同见 [任务控制、评估与修订](references/managed-execution.md)。

```sh
/bin/sh "$HARNESS_DIR/scripts/launch.sh" plan --mode workflow --plan PLAN.json --output /absolute/new-result
/bin/sh "$HARNESS_DIR/scripts/launch.sh" run --mode workflow --plan PLAN.json --output /absolute/new-result
```

Windows PowerShell：`& "$HARNESS_DIR/scripts/launch.ps1" run --mode workflow --plan PLAN.json --output "C:\Users\me\result"`。
原生命令计划追加 `--mode commands`，自有桌面会话使用 `--mode desktop`。交付后必须 `review` 并实际查看媒体；只有技术验证与创作评估都通过才报告可验收，用户接受状态独立保留。需要自动修订时，在首次计划中声明 `revisionScope`；默认最多 2 轮、父子任务共用 30 分钟。未知任务只 inspect/reconcile，不换任务 ID 重做。

## 首次使用与公共入口

定位当前 SKILL.md 的真实目录。原生制品覆盖 macOS arm64/x86_64、Windows x86/x64/arm64、Linux x86_64/aarch64；无需预装 Python；固定 CLI 安装到用户数据目录。已有任务授权覆盖必要依赖时直接执行本技能安装器，不另造批准流程。

将 `SKILL_DIR` 设置为宿主实际加载的本 `SKILL.md` 所在目录（绝对路径）。用户级安装可能位于 `~/.agents/skills/effectcraft-cli`，项目级可能位于 `.agents/skills/effectcraft-cli`，插件可能位于其 `skills/effectcraft-cli` 或宿主缓存目录；以实际加载路径为准，不按当前工作目录猜测，也不搜索后随意选择重复版本。技能目录与 CLI 的用户数据安装目录是两个独立位置。

```bash
: "${SKILL_DIR:?请先设置为本 SKILL.md 的实际所在目录}"
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- --version
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- commands --json
```

CLI argv 在 `--` 后，原生子命令必须放首位。安装参数放分隔符前；`--runtime-home` 可隔离缓存。锁定制品摘要失败、损坏安装或不支持平台时停止；不改 PATH、不执行浮动升级。原生帮助入口是 `--help`；launcher 自身 `--help` 只说明启动参数。

## 场景操作

先查询当前版本与命令目录；只读和编辑调用分别记录。读当前工程状态与命令 enabled/params 后构造 argv；需要创建对象的连续步骤在同会话执行，不能猜测返回 ID。

`commands --filter <关键词> --json` 核对参数；属性读写用 props/get/set，命令用 `exec <id> --params <JSON>` 或成对的 `run <id> <JSON> ...`；用 --save-as 保留新工程。



原生组合与源工程修订使用 effectcraft-harness 技能的 `scripts/workflow.py`（由受管理启动器内部复用）；读取 [工作流合同](references/workflow.md)，模板在本技能 examples 内。只修改授权对象，原生工程和依赖素材保留，派生格式损失读取 [交换报告](references/exchange-loss.md)。

## 核验与恢复

命令非零退出不算完成；需要查看真实保存工程、导出、尺寸及媒体解码。超时结果标 unknown，先检查原任务/工程，不能自动重放编辑。现有原生工作流支持另存修订；对应项目摘要不符时拒绝覆盖。

## 按需参考与交接

- [实际命令证据](references/commands.json)：固定版本观察，仅作为路由与参数参考；实时结果优先，禁用项不执行。
- [工作流合同](references/workflow.md)：组合操作、原生保存、依赖收集与修订。
- 安装/诊断需要时交给 **effectcraft-cli-setup**，完整任务路由交给 **effectcraft-use**；缺少技能时使用 `npx skills add full-aigc-skills/effectcraft-skills --skill <skill-name>`。不通过相邻文件路径加载其他技能。

本技能不提供虚构的登录接口；本地 headless 不要求云账户。完整 GUI、跨编辑器保真与创作质量按实际证据陈述。

## 完整原生命令使用

下面的查询示例需要已有Python；未准备解释器时先用受管理启动器 `doctor` 诊断。写入示例通过启动器自动准备隔离依赖；Windows用 `& "$HARNESS_DIR/scripts/launch.ps1"` 替换 `/bin/sh "$HARNESS_DIR/scripts/launch.sh"`，保留相同模式和参数。当前技能自带完整目录的参数说明与同会话入口，不受创作模板白名单限制。读取 [完整使用指南](references/command-usage.md)，按需查询 [命令参考](references/command-reference.md)；每条指令有技能路由、前置观察及验收状态。

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter QUERY
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe COMMAND_ID
/bin/sh "$HARNESS_DIR/scripts/launch.sh" run --mode commands --plan "$SKILL_DIR/examples/commands-advanced.json" --output /absolute/new-command-result
/bin/sh "$HARNESS_DIR/scripts/launch.sh" run --mode desktop --plan "$SKILL_DIR/examples/desktop-first-use.json" --output /absolute/new-desktop-result
```

新入口执行前检查真实注册表与当前可执行状态，保留返回值引用和逐步回执；语义错误或超时不冒充成功。目录覆盖与直接原生使用不等于所有指令、GUI、交付或 Art 编排已验收。

完整工作流命令网关见 [使用说明](references/native-workflow.md)。固定 CLI 的版本与制品摘要以 effectcraft-harness 技能的 `scripts/runtime.lock.json` 为准；技能包版本以对应发布标签为准。独立安装复验与全量逐命令验收分别记录，不以发布替代验收。

父子图层、属性表达式、动态预览与源工程返工：使用当前技能的 [表达式父级指南](references/expression-parent.md)。

GUI任务可先使用本技能自带的 [固定桌面安装](references/desktop-install.md)；安装、启动与实际GUI编辑分别核验。

完整归属命令按命令族列于 [分类使用清单](references/scenario.md)，每项可通过本技能的 `commands.py describe` 查看参数；通用 CLI 清单也保留未归入专项技能的全部命令。

业务任务从 [场景操作手册](references/business-scenes.md) 开始，按输入检查、模板适配、原生交付、局部返工和结果核验执行。

安装失败时读取 [首次使用诊断](references/first-use-failures.md)，按回执定位当前技能自身的 setup 入口；安装失败与原生调用失败分别处理。

相关创作任务读取 [镜头跟踪场景](references/tracking-scene.md)，核对原生参数、对象上下文、局部返工与交付边界。

镜头跟踪前先读取本技能[跟踪首用与解码核验](references/motion-tracking.md)：核对源像素和实际关键帧，区分计划帧数与完成结果。

## 同目标执行保护

调用公开工作流前阅读本技能的 [执行登记与中断处理](references/output-execution.md)。竞争或未知状态不得删除登记、自动重放或换目标绕过核对。
