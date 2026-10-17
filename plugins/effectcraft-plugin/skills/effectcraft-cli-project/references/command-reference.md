# 完整原生命令参考 / Complete native command reference

本参考逐项保留锁定参数原文与技能路由。命令执行必须满足当前工程、选择对象、素材或 GUI 前置状态。
This reference preserves each pinned parameter contract and skill owner. Query live state before invocation.

使用方法见 [完整调用指南](command-usage.md)。全部参数均为原生语法说明，不把它们假装成 JSON Schema。
每项 NOT_RUN 指本轮完整逐命令验收；既有代表任务证据仍单独保留。

## file.newProject

New Project

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.newProject`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.openDemoProject

Open Demo Project

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.openDemoProject`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.open

Open Project...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.open`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## file.save

Save

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.save`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?}
```

## file.saveAs

Save As...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.saveAs`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## file.incrementAndSave

Increment and Save

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project has not been saved yet。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.incrementAndSave`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.revert

Revert

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project has not been saved yet。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.revert`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.import

File...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.import`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{paths: [string], importAs?: footage|composition|compositionLayerSizes (Photoshop, PDF, Illustrator and EPS files), layer?: name|index (footage of one Photoshop layer), page?: number from 1 (PDF / Illustrator page), drag?: bool (dropped files: Settings ▸ Import ▸ Default Drag Import As), addToComp?: bool (also add them to the active comp, at time?, index?, position? as in layer.addItem)}
```

## file.projectSettings

Project Settings...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.projectSettings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{bitDepth?: 8|16|32, colorEngine?: adobe|ocio, workingSpace?: none|srgb|rec709|rec2020|p3|acescg|aces2065, linearize?, blendLinear?, hdr?: clip|compand|toneMap, outputSpace?: srgb|rec709|rec2020|p3|rec2100pq|rec2100hlg, renderer?: gpu|software, timeDisplay?: timecode|frames|feet35|feet16}
```

## file.cycleBitDepth

Cycle Project Bit Depth

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.cycleBitDepth`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## render.backend

Video Rendering and Effects

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe render.backend`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{backend?: gpu|cpu}
```

## roto.models

Roto Brush Models

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.models`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## roto.model.select

Use Roto Brush Model

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.model.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id: classical|mobilesam, wait?} (Roto Brush 2.0 / 3.0 use it; wait: loaded before returning)
```

## roto.model.install

Install Roto Brush Model

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.model.install`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path: weights file, id?, wait?} — verified against the registry's SHA-256
```

## roto.model.download

Download Roto Brush Model

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.model.download`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, wait?} — the official weights, verified (desktop; uses the system curl)
```

## roto.model.remove

Remove Roto Brush Model

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.model.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## face.models

Face Tracking Models

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe face.models`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## face.model.select

Use Face Tracking Model

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe face.model.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id: classical|mediapipe-face, wait?} (face tracking uses it; wait: loaded before returning)
```

## face.model.install

Install Face Tracking Model

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe face.model.install`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path: model file, id?, wait?} — verified against the registry's SHA-256
```

## face.model.download

Download Face Tracking Model

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe face.model.download`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, wait?} — the official model, verified (desktop; uses the system curl)
```

## face.model.remove

Remove Face Tracking Model

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe face.model.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## edit.undo

Undo

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: nothing to undo。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.undo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.redo

Redo

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: nothing to redo。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.redo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.cut

Cut

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.cut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?} (keyframes when keys are selected)
```

## edit.copy

Copy

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.copy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?} (keyframes when keys are selected)
```

## edit.copyWithPropertyLinks

Copy with Property Links

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.copyWithPropertyLinks`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?} (selected properties, or layers, as expressions linking to the originals)
```

## edit.copyWithRelativePropertyLinks

Copy with Relative Property Links

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.copyWithRelativePropertyLinks`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?} (like Copy with Property Links, using thisComp)
```

## edit.copyExpressionOnly

Copy Expression Only

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.copyExpressionOnly`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.paste

Paste

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.paste`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (layers, keyframes at the CTI, or property links / expressions)
```

## edit.pasteReversedKeyframes

Paste Reversed Keyframes

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.pasteReversedKeyframes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, prop?|path?, time?}
```

## edit.clear

Clear

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.clear`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## edit.duplicate

Duplicate

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.duplicate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## edit.splitLayer

Split Layer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.splitLayer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## edit.liftWorkArea

Lift Work Area

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.liftWorkArea`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## edit.extractWorkArea

Extract Work Area

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.extractWorkArea`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## edit.selectAll

Select All

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.selectAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.deselectAll

Deselect All

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.deselectAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.label

Label

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.label`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{label: Red|Yellow|Aqua|…, layers?, keys?, target?: layers}
```

## edit.selectLabelGroup

Select Label Group

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select layers or project items first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.selectLabelGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.purgeUndo

Undo

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.purgeUndo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.purge

Purge

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.purge`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{what?: all|memoryAndDisk|memory|disk|3d|image|snapshot}
```

## cache.diskStats

Disk Cache Statistics

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe cache.diskStats`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.editOriginal

Edit Original...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select a footage item or layer。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.editOriginal`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.history.list

History

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.history.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {states: [{index, id, label, parent, depth, current, line, future}], current, branches}
```

## edit.history.goto

Go to History State

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.history.goto`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index? (from edit.history.list) | id? | steps? (negative = back along the line)}
```

## comp.new

New Composition...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.new`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, width?, height?, frameRate?, duration? (s), startTime? (s) | startTimecode?, background? [r,g,b]|#hex, pixelAspect?, shutterAngle?, shutterPhase?, motionBlurSamples?, adaptiveSampleLimit? (16–256), preserveFrameRate?: bool, preserveResolution?: bool, renderer?: classic3D|advanced3D, anchor?, open?}
```

## comp.settings

Composition Settings...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.settings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, name?, width?, height?, anchor? 0-8 (resize anchor, 4 = center), frameRate?, duration?, startTime? (s) | startTimecode?, background?, shutterAngle?, shutterPhase?, motionBlurSamples?, adaptiveSampleLimit? (16–256), preserveFrameRate?: bool (nested or in the render queue it shows only its own frames), preserveResolution?: bool (nested, it renders at full size), pixelAspect?, renderer?: classic3D|advanced3D}
```

## comp.setPosterTime

Set Poster Time

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.setPosterTime`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## comp.trimToWorkArea

Trim Comp to Work Area

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.trimToWorkArea`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## comp.open

Open Composition

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.open`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp: id|name}
```

## comp.close

Close Composition

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.close`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## comp.workArea

Set Work Area

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.workArea`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{start?, end?, set?: begin|end (at CTI)}
```

## comp.setSwitch

Composition Switch

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.setSwitch`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{switch: hideShy|motionBlur|frameBlending|draft3d, value?}
```

## comp.addMarker

Add Marker

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.addMarker`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{time?, comment?}
```

## layer.newText

Text

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newText`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{text?, name? (layer name; default the text), position? [x,y], box? [x,y,w,h] (paragraph text, comp space), vertical?, edit? (start editing), font?, style?, size?, fill?, stroke?, applyFill?, applyStroke?, strokeWidth?, tracking?, leading?, baselineShift?, hScale?, vScale?, tsume?, fauxBold?, fauxItalic?, allCaps?, smallCaps?, baseline?, superscript?, subscript?, kerning?, ligatures?, justify?, indentLeft?, indentRight?, indentFirst?, spaceBefore?, spaceAfter?, direction?, composer?, hangingPunctuation?, strokeOverFill?} (attributes as layer.setText)
```

## layer.newSolid

Solid...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newSolid`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, color? #hex|[r,g,b], width?, height?, pixelAspect?}
```

## layer.newNull

Null Object

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newNull`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json)；前置条件见 [表达式父级](expression-parent.md)。

## layer.newShape

Shape Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newShape`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind?: rect|rounded|ellipse|star|polygon|none, name?, size?, fill?, stroke?, strokeWidth?, position?}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json)；前置条件见 [表达式父级](expression-parent.md)。

## layer.newAdjustment

Adjustment Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newAdjustment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?}
```

## layer.settings

Layer Settings...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.settings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, name?, color?, width?, height?, pixelAspect?, affectAll?: bool (default true; false gives this layer its own copy of a solid other layers use)} → {layer, solid?}
```

## layer.addItem

Add Footage to Comp

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addItem`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item: id|name, time? (s, the In point), index? (1-based stack position; default above the selected layer), position? ([x, y] comp px; default the centre), duration? (s, for a still)}
```

## layer.select

Select Layers

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers: [id|name|#n], add?, toggle?}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json), [examples/expression-parent-revise.json](../examples/expression-parent-revise.json)；前置条件见 [表达式父级](expression-parent.md)。

## layer.selectNext

Select Next Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.selectNext`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{add?}
```

## layer.selectPrevious

Select Previous Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.selectPrevious`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{add?}
```

## layer.setSwitch

Layer Switch

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setSwitch`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, switch: video|audio|solo|lock|shy|collapse|quality|fx|frameBlend|motionBlur|adjustment|threeD|guide|preserveTransparency, value?}
```

## layer.rename

Rename

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.rename`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, name}
```

## layer.setComment

Layer Comment

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setComment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, comment}
```

## layer.setBlendMode

Blending Mode

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setBlendMode`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, mode?: Normal|Multiply|Screen|…, step?: ±1}
```

## layer.setTrackMatte

Track Matte

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setTrackMatte`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, matte: layer|null, kind?: alpha|alphaInverted|luma|lumaInverted}
```

## layer.setParent

Parent

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setParent`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, parent: layer|null}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json)；前置条件见 [表达式父级](expression-parent.md)。

## layer.timing

Layer Timing

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.timing`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, op?: moveInToTime|moveOutToTime|trimInToTime|trimOutToTime, delta?, start?, in?, out?, merge?}
```

## layer.slip

Slip Edit

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.slip`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, delta? (seconds) | frames?, merge?}
```

## layer.slipBack

Slip Edit 1 Frame Earlier

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.slipBack`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.slipForward

Slip Edit 1 Frame Later

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.slipForward`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.arrange

Arrange

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.arrange`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, to: front|forward|backward|back, index?, above?: layer}
```

## layer.precompose

Pre-compose...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.precompose`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, name?, mode?: move|leave, adjustDuration?, open?}
```

## layer.addMask

New Mask

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addMask`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, shape?: rect|ellipse, rect? [x,y,w,h], mode?}
```

## layer.setMask

Mask Mode

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setMask`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask: index|uid|name, mode?, inverted?}
```

## layer.addShapeItem

Add (Shape)

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addShapeItem`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, kind: group|rect|ellipse|star|polygon|fill|stroke|gfill|trim|repeater|round|offset|pucker|twist|zigzag|wiggle|merge, group?: uid|path} → {uid, path}
```

## layer.setText

Edit Text

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setText`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, range?: [start, end] (characters; default all), text?, font?, style?, size?, fill?, stroke?, applyFill?, applyStroke?, strokeWidth?, tracking?, leading?: px|"auto", baselineShift? px, hScale? %, vScale? %, tsume? %, fauxBold?, fauxItalic?, allCaps?, smallCaps?, baseline?: normal|superscript|subscript, superscript?, subscript?, kerning?: metrics|optical|number, ligatures?, OpenType: discretionaryLigatures?, contextualAlternates?, stylisticAlternates?, stylisticSets?: [1–20], ss01…ss20?, swash?, titling?, ordinals?, fractions?, allSmallCaps?, figureStyle?: default|lining|oldStyle, figureWidth?: default|proportional|tabular, figures?, variations?: {tag: value} (variable font axes; null resets), justify?: left|center|right|justifyLeft|justifyCenter|justifyRight|justifyAll, indentLeft?, indentRight?, indentFirst?, spaceBefore?, spaceAfter?, direction?: ltr|rtl, composer?: everyLine|singleLine, hangingPunctuation?, strokeOverFill?, box?: [x,y,w,h]|null (layer space), vertical?}
```

## layer.transform

Transform

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.transform`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, op: reset|center|fit|fitWidth|fitHeight|flipH|flipV}
```

## layer.style.convertToEditable

Convert to Editable Styles

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.convertToEditable`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.showAll

Show All

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.showAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.removeAll

Remove All

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.removeAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.dropShadow

Drop Shadow

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.dropShadow`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.innerShadow

Inner Shadow

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.innerShadow`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.outerGlow

Outer Glow

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.outerGlow`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.innerGlow

Inner Glow

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.innerGlow`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.bevelEmboss

Bevel and Emboss

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.bevelEmboss`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.satin

Satin

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.satin`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.colorOverlay

Color Overlay

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.colorOverlay`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.gradientOverlay

Gradient Overlay

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.gradientOverlay`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.stroke

Stroke

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.stroke`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.style.add

Add Layer Style

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.add`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{style: dropShadow|innerShadow|outerGlow|innerGlow|bevelEmboss|satin|colorOverlay|gradientOverlay|stroke (or display name), layers?}
```

## layer.style.remove

Remove Layer Style

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, style: id|name|uid|layerStyles}
```

## layer.style.toggle

Toggle Layer Style

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.toggle`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, style: id|name|uid|layerStyles, value?}
```

## layer.style.globalLight

Global Light

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.globalLight`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, angle? (deg), altitude? (deg, 0..90), time? (s)} — no values returns the current setting
```

## layer.style.list

List Layer Styles

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## layer.autoOrient

Auto-Orient...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.autoOrient`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{mode: off|alongPath|towardsCamera|towardsPointOfInterest, layers?}
```

## layer.newLight

Light...

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newLight`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind?: Parallel|Spot|Point|Ambient (default Spot), name?, color?, intensity?, coneAngle?, coneFeather?, falloff?: None|Smooth|Inverse Square Clamped, radius?, falloffDistance?, castsShadows?, shadowDarkness?, shadowDiffusion?, position? [x,y,z], poi? [x,y,z]}
```

## layer.newCamera

Camera...

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newCamera`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, type?: oneNode|twoNode (default twoNode), preset?: 15mm|20mm|24mm|28mm|35mm|50mm|80mm|135mm|200mm, zoom?, focalLength? mm, angleOfView? deg, dof?, focusDistance?, aperture?, fStop?, blurLevel?, lockToZoom?, position? [x,y,z], poi? [x,y,z]}
```

## layer.cameraSettings

Camera Settings...

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.cameraSettings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, name?, type?, preset?, zoom?, focalLength?, angleOfView?, dof?, focusDistance?, aperture?, fStop?, blurLevel?, position?, poi?}
```

## layer.lightSettings

Light Settings...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.lightSettings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, name?, kind?, color?, intensity?, coneAngle?, coneFeather?, falloff?, radius?, falloffDistance?, castsShadows?, shadowDarkness?, shadowDiffusion?, position?, poi?}
```

## view.set3DView

Switch 3D View

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.set3DView`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{view: activeCamera|default|front|left|top|back|right|bottom|custom1|custom2|custom3, comp?}
```

## view.3d.activeCamera

Active Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.activeCamera`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.default

Default

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.default`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.front

Front

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.front`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.left

Left

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.left`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.top

Top

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.top`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.back

Back

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.back`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.right

Right

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.right`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.bottom

Bottom

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.bottom`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.custom1

Custom View 1

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.custom1`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.custom2

Custom View 2

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.custom2`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.custom3

Custom View 3

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.custom3`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.3d.last

Switch to Last 3D View

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.3d.last`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.lookAtSelected

Look at Selected Layers

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.lookAtSelected`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layers?}
```

## view.lookAtAll

Look at All Layers

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.lookAtAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## camera.fromView

Create Camera from 3D View

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.fromView`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.reset3DView

Reset 3D View

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.reset3DView`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.set3DViewCamera

Set 3D View Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.set3DViewCamera`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{view, eye? [x,y,z], poi? [x,y,z], zoom?}
```

## camera.orbit

Orbit Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.orbit`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{yaw|dx deg, pitch|dy deg, layer?, merge?} — current 3D view (camera layer in Active Camera)
```

## camera.pan

Pan Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.pan`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dx, dy (comp px), layer?, merge?}
```

## camera.dolly

Dolly Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.dolly`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{amount (px, + = forward), layer?, merge?}
```

## view.get3D

3D View State

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.get3D`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?} → current 3D view, view camera, active camera layer, lights
```

## layer.newModel

3D Model Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newModel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?: id or name of a 3D model footage item, path?: a .gltf, .glb or .obj file to import, name?, time? (s), index? (1-based stack position), position? ([x, y] comp px)}
```

## layer.new3dPrimitive

3D Primitive

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.new3dPrimitive`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: cube|sphere|plane|torus|cone|cylinder, name?, width?, height?, depth?, radius?, tubeRadius?, segments?, rings?, position? [x,y,z], baseColor?, metallic?, roughness?, emissive?, castsShadows?, acceptsShadows?, acceptsLights?}
```

## layer.newPrimitive

New 3D Primitive

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newPrimitive`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: cube|sphere|plane|torus|cone|cylinder, name?, width?, height?, depth?, radius?, tubeRadius?, segments?, rings?, position? [x,y,z], baseColor?, metallic?, roughness?, emissive?, castsShadows?, acceptsShadows?, acceptsLights?}
```

## comp.renderer

Renderer

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.renderer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{renderer?: advanced3d|classic3d (omit to read), value?}
```

## layer.environment

Environment Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.environment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, on?}
```

## material.set

Material Options

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe material.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, castsShadows?: off|on|only, acceptsShadows?: off|on|only, acceptsLights?, appearsInReflections?, lightTransmission?, ambient?, diffuse?, specularIntensity?, specularShininess?, metal?, baseColor?, metallic?, roughness?, emissive?, time?}
```

## material.revealSource

Reveal Material Source in Project

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe material.revealSource`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## material.reset

Reset Material

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe material.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## material.duplicateAssign

Duplicate and Assign Material

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe material.duplicateAssign`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers? (first = source)}
```

## camera.stereoRig

Create Stereo 3D Rig

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.stereoRig`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, configuration?: stereoPair|centerRight|centerLeft, sceneDepth? (% of comp width, default 3), convergence?: bool, convergenceOf?: poi|zoom, zOffset?, view3d?: 3D Glasses view index (default 5 Balanced Colored Red Blue)}
```

## camera.orbitNull

Create Orbit Null

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.orbitNull`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layer?: camera (default selected/active)}
```

## camera.fromModel

Create Cameras from 3D Model

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.fromModel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layers?: 3D model layers (default selected)}
```

## light.fromModel

Create Lights from 3D Model

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe light.fromModel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layers?: 3D model layers (default selected)}
```

## light.controlWithCamera

Control Light with Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe light.controlWithCamera`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layers?: lights (default selected), camera? (default active), on?: bool (default toggle)}
```

## light.environmentBackground

Create Environment Light Background Layer

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe light.environmentBackground`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layer?: environment light (default selected / first)}
```

## layer.addTextAnimator

Animate Text

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addTextAnimator`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, properties: [anchor|position|scale|skew|rotation|opacity|transformAll|lineAnchor|lineSpacing|characterOffset|characterValue|blur|fillColor|fillHue|fillSaturation|fillBrightness|fillOpacity|strokeColor|strokeHue|strokeSaturation|strokeBrightness|strokeOpacity|strokeWidth|tracking|perChar3d], name?}
```

## layer.addTextAnimatorProperty

Add Property

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addTextAnimatorProperty`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, animator?: uid|index, property: (see layer.addTextAnimator)}
```

## layer.addTextSelector

Add Text Selector

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addTextSelector`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, animator?: uid|index, kind: range|wiggly|expression}
```

## layer.enablePerChar3D

Enable Per-character 3D

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.enablePerChar3D`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, enabled?: bool, toggle?: bool}
```

## layer.applyTextPreset

Apply Text Animation Preset

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.applyTextPreset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, preset: typewriter|fadeUpCharacters|bounceInWords|trackingIn|scramble|blurIn|jitter|dropInLines}
```

## text.animatorFontAxes

Variable Font Axes

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.animatorFontAxes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, axis?: tag|name (omit to list the font's axes), animator?: uid|index}
```

## text.presets

Text Animation Presets

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.presets`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## text.animatorProperties

Text Animator Properties

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.animatorProperties`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## text.edit

Edit Text

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.edit`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, select?: [anchor, caret]|"none", caret?, created?} → {layer, anchor, caret}
```

## text.endEdit

Exit Text Editing

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.endEdit`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## text.fontFeatures

OpenType Features

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.fontFeatures`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, font?, style?} → {family, style, features: [tags], options: {smallCaps, superscript, stylisticSets: [n], fractions, …}} (what the font sets with its own glyphs)
```

## text.fonts

List Fonts

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.fonts`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{query?, rescan?} → {count, families: [{family, styles, origin: bundled|system|user, nativeName?}], added} (rescan picks up fonts installed since launch)
```

## text.setSelection

Set Text Selection

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.setSelection`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, start, end?} | {anchor, caret} | {select: "all"} (character indices)
```

## text.moveCaret

Move Text Caret

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: not editing text。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.moveCaret`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{to: left|right|wordLeft|wordRight|lineStart|lineEnd|up|down|paraStart|paraEnd|start|end, extend?}
```

## text.insert

Type Text

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.insert`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, text, range?: [start, end], merge?} (replaces the selection)
```

## text.delete

Delete Text

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.delete`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, direction?: backward|forward, word?, range?: [start, end], merge?}
```

## edit.pasteTextMatchFormatting

Paste Text and Match Formatting

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.pasteTextMatchFormatting`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{text?} (the clipboard's text in the style at the caret)
```

## edit.pasteTextFormattingOnly

Paste Text Formatting Only

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.pasteTextFormattingOnly`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?} (the copied text's formatting on the selected text or text layers)
```

## layer.timeStretch

Time Stretch...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.timeStretch`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, percent?|duration? (s), hold?: in|current|out, op?: reverse}
```

## layer.timeReverse

Time-Reverse Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.timeReverse`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.enableTimeRemap

Enable Time Remapping

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.enableTimeRemap`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, value?}
```

## layer.freezeFrame

Freeze Frame

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.freezeFrame`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.freezeOnLastFrame

Freeze On Last Frame

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.freezeOnLastFrame`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## prop.get

Get Property

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.get`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, time? (comp s)}
```

## prop.set

Set Property Value

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, value, time?, merge?}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json)；前置条件见 [表达式父级](expression-parent.md)。

## prop.toggleAnimation

Toggle Stopwatch

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.toggleAnimation`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, value?}
```

## prop.addKey

Add Keyframe

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.addKey`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, time?, value?}
```

## prop.toggleKey

Add or Remove Keyframe at Current Time

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.toggleKey`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop}
```

## keys.toggleTransform

Add or Remove Transform Keyframe

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.toggleTransform`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, prop: anchor|position|scale|rotation|opacity} (Alt+Shift+A/P/S/R/T)
```

## prop.setExpression

Add Expression

- 技能 / Owner: `effectcraft-cli-expressions`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-expressions`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.setExpression`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, expression?, enabled?}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json), [examples/expression-parent-revise.json](../examples/expression-parent-revise.json)；前置条件见 [表达式父级](expression-parent.md)。

## prop.reset

Reset Property

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, default?}
```

## prop.select

Select Property

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, add?, selectKeys?}
```

## prop.convertExpressionToKeyframes

Convert Expression to Keyframes

- 技能 / Owner: `effectcraft-cli-expressions`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-expressions`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.convertExpressionToKeyframes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop}
```

## keys.select

Select Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{keys: [{layer, prop: uid | path (or `path`), time (layer s)}], add?, toggle?: bool (Shift+click: in or out of the selection)}
```

## keys.move

Move Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.move`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{delta (s), merge?}
```

## keys.delete

Delete Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.delete`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.easyEase

Easy Ease

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.easyEase`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{which?: both|in|out}
```

## keys.easyEaseIn

Easy Ease In

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.easyEaseIn`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.easyEaseOut

Easy Ease Out

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.easyEaseOut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.toggleHold

Toggle Hold Keyframe

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.toggleHold`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.interpolation

Keyframe Interpolation...

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.interpolation`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{interpolation?: linear|bezier|continuousBezier|autoBezier|hold, in?|out?: linear|bezier|hold, autoBezier?, continuous?, spatial?: linear|bezier|continuousBezier|autoBezier, roving?}
```

## keys.velocity

Keyframe Velocity...

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.velocity`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{inSpeed?, inInfluence? %, outSpeed?, outInfluence? % (numbers or per-dimension arrays), continuous?}
```

## prop.renameGroup

Rename Property Group

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.renameGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop: uid, name}
```

## prop.setGroupEnabled

Enable Property Group

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.setGroupEnabled`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop: uid, value?}
```

## prop.removeGroup

Delete Property Group

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.removeGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop: uid}
```

## prop.duplicateGroup

Duplicate Property Group

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.duplicateGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop: uid} → {prop: new uid}
```

## prop.moveGroup

Reorder Property Group

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.moveGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop: uid, index (1-based among its siblings)}
```

## project.select

Select Project Items

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items: [id|name], add?}
```

## project.rename

Rename Item

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.rename`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?: id|name (default: selected), name}
```

## project.move

Move to Folder

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.move`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?: [id|name] (default: selected), folder: id|name|null (root)}
```

## project.setLabel

Item Label

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.setLabel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?, label: name|index}
```

## project.setComment

Item Comment

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.setComment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?, comment}
```

## project.delete

Delete Project Items

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.delete`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?: [id|name] (default: selected)} (folders with their contents; layers using the items go too)
```

## project.usage

Project Item Usage

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.usage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?: [id|name] (default: selected)} → {items, layers, comps} that deleting them removes
```

## project.duplicate

Duplicate Project Items

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.duplicate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?: [id|name] (default: selected)} → {items}
```

## keys.copy

Copy Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.copy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.paste

Paste Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.paste`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, prop?|path?, time?}
```

## keys.selectAll

Select All Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.selectAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, visible?: [{layer, prop}] (every key of these properties)}
```

## keys.nudge

Nudge Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.nudge`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{frames, merge?}
```

## keys.nudgeForward

Move Keyframes 1 Frame Later

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.nudgeForward`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.nudgeBackward

Move Keyframes 1 Frame Earlier

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.nudgeBackward`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.nudgeForward10

Move Keyframes 10 Frames Later

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.nudgeForward10`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.nudgeBackward10

Move Keyframes 10 Frames Earlier

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.nudgeBackward10`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.set

Edit Keyframe

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, time (layer s), newTime?, value?, merge?}
```

## keys.selectEqual

Select Equal Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.selectEqual`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.selectPrevious

Select Previous Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.selectPrevious`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.selectFollowing

Select Following Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.selectFollowing`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.setEase

Set Keyframe Ease

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.setEase`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, time (layer s), side: in|out, dim?, speed?, influence? %, merge?}
```

## keys.timeReverse

Time-Reverse Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.timeReverse`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.info

Keyframe Info

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.info`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{keys?: [{layer, prop, time}]}
```

## keys.wiggle

Wiggler

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.wiggle`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{apply?: spatial|temporal, noise?: smooth|jagged, dimensions?: one|same|independent, dimension? (index for `one`), frequency? (keys/s, 5), magnitude?, seed?}
```

## keys.smooth

Smoother

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.smooth`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{tolerance? (property units, 1)}
```

## motion.sketch

Motion Sketch

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe motion.sketch`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, points: [[t, x, y]…] (t = capture seconds) | [[x, y]…] (one per frame), start? (s, default current time), captureSpeed? (%, 100), smoothing? (px, 1)}
```

## prop.separateDimensions

Separate Dimensions

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.separateDimensions`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, value?}
```

## prop.pickWhip

Pick Whip (Link Property)

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prop.pickWhip`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, target: {layer, path|prop}} → sets an AE reference expression
```

## markers.list

List Markers

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe markers.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer? (omit for composition markers)}
```

## markers.nested

Nested Comp Markers

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe markers.nested`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer: a precomp layer, comp?} — its comp's markers at their times in this comp (as on the layer bar)
```

## markers.set

Marker Settings

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe markers.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer? (omit: comp marker), index? (0-based) | at? (comp s) | new?: true, time? (comp s), duration? (s), comment?, chapter?, url?, frameTarget?, cuePoint?: {name, navigation?, params?: [[name, value]…]} | null, protected?, label?}
```

## markers.delete

Delete Marker

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe markers.delete`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, index? | at? (comp s)}
```

## markers.convert

Convert Marker

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe markers.convert`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer? (layer marker → comp marker), index? | at?, toLayer? (comp marker → layer marker)}
```

## layer.updateMarkersFromSource

Update Markers From Source

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.updateMarkersFromSource`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## mask.new

New Mask from Points

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.new`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, vertices: [[x,y]…], inTangents?, outTangents?, closed?, mode?}
```

## mask.addVertex

Add Mask Vertex

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.addVertex`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask, point: [x,y], in?, out?, index?}
```

## mask.setVertex

Set Mask Vertex

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.setVertex`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask, index, point?, in?, out?, merge?}
```

## mask.setClosed

Closed

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.setClosed`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask, closed?}
```

## mask.selectVertices

Select Mask Vertices

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.selectVertices`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{vertices: [{layer, mask, index}], add?, toggle?}
```

## mask.moveVertices

Move Mask Vertices

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.moveVertices`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{vertices?: [{layer, mask, index}], delta: [dx,dy], merge?}
```

## mask.deleteVertices

Delete Mask Vertices

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.deleteVertices`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{vertices?}
```

## mask.convertVertex

Convert Vertex

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.convertVertex`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask: uid (mask or shape Path item), index, smooth?}
```

## mask.insertVertex

Add Vertex

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.insertVertex`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask: uid (mask or shape Path item), segment, t?: 0..1}
```

## mask.featherPoint.add

Add Mask Feather Point

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.featherPoint.add`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask, segment?, t?: 0..1, point?: [x,y] (layer space), radius? (px, negative = inner), tension? (%)} → {index}
```

## mask.featherPoint.set

Move Mask Feather Point

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.featherPoint.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask, index, segment?, t?, point? (slide along the path), radius?, toward?: [x,y] (radius from the drag point, layer space), tension? (%), merge?}
```

## mask.featherPoint.remove

Delete Mask Feather Point

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.featherPoint.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask, index? | all?}
```

## mask.featherPoint.list

Mask Feather Points

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.featherPoint.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask}
```

## mask.remove

Remove Mask

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask}
```

## mask.removeAll

Remove All Masks

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.removeAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## path.rotoBezier

RotoBezier

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe path.rotoBezier`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, value?}
```

## path.convertToBezier

Convert To Bezier Path

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe path.convertToBezier`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?}
```

## path.groupShapes

Group Shapes

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe path.groupShapes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, items?: [uid]}
```

## path.ungroupShapes

Ungroup Shapes

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe path.ungroupShapes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, items?: [group uid]}
```

## path.setFirstVertex

Set First Vertex

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe path.setFirstVertex`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?: uid, index?}
```

## path.freeTransform

Free Transform Points

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe path.freeTransform`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, scale?: % | [x%, y%], rotation?: deg, offset?: [dx, dy], anchor?: [x, y]}
```

## layer.mask.motionBlur

Motion Blur

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.motionBlur`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, mode: sameAsLayer|on|off}
```

## layer.mask.featherFalloff

Feather Falloff

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.featherFalloff`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, mode: smooth|linear}
```

## layer.mask.hideLocked

Hide Locked Masks

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.hideLocked`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## effect.apply

Apply Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.apply`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{effect: id|name (e.g. Gaussian Blur), layers?}
```

## effect.pickColor

Pick Effect Colour

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.pickColor`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?: index|uid|name, param: id (e.g. screenColour) | prop: uid, x, y (layer px), average?: bool (5×5), time?} — the colour of the effect's input there
```

## effect.applyLast

Last Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.applyLast`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## effect.removeAll

Remove All

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.removeAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## effect.remove

Remove Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect: index|uid|name}
```

## effect.toggle

Toggle Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.toggle`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect, value?}
```

## effect.reorder

Reorder Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.reorder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect, index}
```

## effect.duplicate

Duplicate Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.duplicate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect}
```

## effect.copy

Copy Effects

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.copy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect? | effects?: [uid|name|index]} (default: the selected effects)
```

## effect.paste

Paste Effects

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.paste`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?} — adds the copied effects to the layers
```

## effect.reset

Reset Effect

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect}
```

## effect.list

List Effects

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{filter?}
```

## effect.plugins.list

List Effect Plug-ins

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.plugins.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {api, wasm, plugins: [{id, name, category, version, author, source, params}]}
```

## effect.plugins.load

Load Effect Plug-in...

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.plugins.load`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.wasm / .wat plug-in, API v1) | folder (loads every .wasm in it)}
```

## time.set

Go to Time...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{time? (s) | frame? | timecode?}
```

## time.nextFrame

Next Frame

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.nextFrame`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.previousFrame

Previous Frame

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.previousFrame`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.forward10

Forward 10 Frames

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.forward10`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.back10

Back 10 Frames

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.back10`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.step

Step Frames

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.step`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{frames}
```

## time.start

Go to Start

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.start`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.end

Go to End

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.end`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.layerIn

Go to Layer In Point

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.layerIn`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.layerOut

Go to Layer Out Point

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.layerOut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## time.nextKey

Go to Next Keyframe or Marker

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.nextKey`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{visible?: [{layer, prop}] (only these properties' keys, as the Timeline shows them)}
```

## time.previousKey

Go to Previous Keyframe or Marker

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.previousKey`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{visible?: [{layer, prop}]}
```

## time.go

Go To

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe time.go`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{to: start|end|workStart|workEnd|layerIn|layerOut|nextKey|prevKey, prop?: uid, visible?: [{layer, prop}]}
```

## renderQueue.add

Add to Render Queue

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select or open a composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.add`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?: id|name, template?: Render Settings template, format?: h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|gif|wav|aiff, output?: path|template, log?: errorsOnly|plusSettings|plusPerFrameInfo, quality?: best|draft|1-100 (jpeg, webm), resolution?: full|half|third|quarter|scale, proxyUse?, effects?, solo?, guideLayers?, colorDepth?, frameBlending?, fieldRender?, pulldown?, motionBlur?, timeSpan?: workArea|comp|custom, start?: s, end?: s, duration?: s, frameRate?: fps|null, skipExisting?: bool, storageOverflow?: bool, channels?: rgb|rgba|alpha, color?, bitrate?: kbps, webmBitrate?, keyframeInterval?, proresProfile?, profile?, level?, rateControl?, webmCodec?, audioBitrate?, opusApplication?, crop?, resize?, includeProjectLink?, audio?: auto|on|off, sampleRate?, audioChannels?, audioFormat?, loop?: bool (values as in setRenderSettings / setOutputModule)}
```

## renderQueue.remove

Remove from Render Queue

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?: id, index?: n}
```

## renderQueue.setRender

Render Queue: Render Checkbox

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setRender`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, render?: bool (toggles)}
```

## renderQueue.setRenderSettings

Render Settings...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setRenderSettings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, template?: name, quality?: best|draft, resolution?: full|half|third|quarter|scale, proxyUse?: current|all|comp|none, effects?: current|allOn|allOff, solo?: current|allOff, guideLayers?: current|allOff, colorDepth?: current|8|16|32, frameBlending?: current|onForChecked|offForAll, fieldRender?: off|upper|lower, pulldown?: off|WSSWW|SSWWW|SWWWS|WWWSS|WWSSW, motionBlur?: bool|current|onForChecked|offForAll, timeSpan?: workArea|comp|custom, start?: s, end?: s, duration?: s, frameRate?: fps|null, skipExisting?: bool, storageOverflow?: bool}
```

## renderQueue.setOutputModule

Output Module Settings...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setOutputModule`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, module?: n (1 = first), template?: name, format?: h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|gif|wav|aiff, channels?: rgb|rgba|alpha, color?: straight|premultiplied, quality?: 1-100, bitrate?: kbps, webmBitrate?: bool, keyframeInterval?: frames (0 = auto), proresProfile?: proxy|lt|standard|hq|4444|4444xq, profile?: main|main10 (HEVC/AV1), level?: auto|4.1, rateControl?: bitrate|quality, webmCodec?: vp9|av1, audioBitrate?: Opus kbps, opusApplication?: audio|voice, crop?: bool|{useRoi?, roi?, top?, left?, bottom?, right?}, cropTop?, cropLeft?, cropBottom?, cropRight?, resize?: bool|{preset?, width?, height?, lockAspect?, quality?: low|high}, resizeWidth?, resizeHeight?, postRenderAction?: none|import|importAndReplace|setProxy, includeProjectLink?: bool, audio?: auto|on|off, sampleRate?, audioChannels?: mono|stereo, audioFormat?: 16|24|32, loop?: bool, output?}
```

## renderQueue.setOutput

Output To...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setOutput`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, module?: n, path: file path or template like [compName].[fileExtension]}
```

## render.addOutputModule

Add Output Module

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe render.addOutputModule`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index? (default: the last item), format?, output?, channels?, quality?, bitrate?, proresProfile?, audio?}
```

## render.preRender

Pre-render...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select or open a composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe render.preRender`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, output?: path|template, format?}
```

## render.saveCurrentPreview

Save Current Preview...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe render.saveCurrentPreview`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, path}
```

## renderQueue.move

Move in Render Queue

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.move`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, to: n (1-based)}
```

## renderQueue.duplicate

Duplicate Render Item

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.duplicate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?}
```

## renderQueue.render

Render

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: nothing is queued。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.render`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{wait?: bool (default true; the UI renders in the background)}
```

## renderQueue.stop

Stop Rendering

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: not rendering。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.stop`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## renderQueue.list

Render Queue Items

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## renderQueue.templates

Render Templates

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.templates`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## renderQueue.saveTemplate

Save Template...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.saveTemplate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: renderSettings|outputModule, name, item?|index? (save from this item), from?: template to copy, module?, params?: {setRenderSettings / setOutputModule keys}}
```

## renderQueue.deleteTemplate

Delete Template

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.deleteTemplate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: renderSettings|outputModule, name}
```

## renderQueue.setTemplateDefault

Set Template Default

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setTemplateDefault`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: renderSettings|outputModule, slot: movie|still|preRender|movieProxy|stillProxy, name}
```

## renderQueue.applyTemplate

Apply Template

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.applyTemplate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, renderSettings?: template name, outputModule?: template name, module?: n}
```

## renderQueue.setLog

Render Queue: Log

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the render queue is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setLog`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?|index?, log: errorsOnly|plusSettings|plusPerFrameInfo}
```

## renderQueue.setNotify

Notify When Done

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setNotify`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{notify?: bool (toggles)}
```

## renderQueue.setOverflowFolders

Storage Overflow Folders

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.setOverflowFolders`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folders: [path, …] (used in order when the output volume is full)}
```

## renderQueue.formats

Output Formats

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe renderQueue.formats`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.docs

EffectCraft Help...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.docs`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{page?: help|scripting|expressions|effects|agents}
```

## help.discord

Join the ArtCraft Discord...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.discord`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.website

ArtCraft Website

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.website`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.appPage

EffectCraft Home Page

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.appPage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.github

EffectCraft on GitHub

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.github`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.onlineTutorials

Online Tutorials...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.onlineTutorials`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.inAppTutorials

In-App Tutorials...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.inAppTutorials`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → the Home screen's Learn tab
```

## help.reportIssue

Provide Feedback...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.reportIssue`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.sibling

Other ArtCraft Apps

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.sibling`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{app: photocraft|vectorcraft|filmcraft|lightcraft|printcraft|designcraft, kind?: page|github}
```

## command.list

List Commands

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe command.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{filter?, enabledOnly?, schemas? (add each command's params JSON Schema)}
```

## command.describe

Describe Command

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe command.describe`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{command} → id, label, menu, shortcut, params doc, JSON `schema`, enabled
```

## app.capabilities

App Capabilities

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.capabilities`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → version, command/effect counts, export formats, parity summary
```

## project.summary

Project Summary

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.summary`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## comp.info

Composition Info

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.info`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## layer.tree

Layer Property Tree

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.tree`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, comp?, depth?, time? (comp s)} → nodes with `path`
```

## editor.state

Editor State

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe editor.state`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## engine.batch

Run Commands (Batch)

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe engine.batch`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{steps: [{command, params?}], label? (undo step name, default Batch), atomic?: bool (default true: a failing step rolls the whole batch back)} → {steps, results: [each step's result]}; a string param "$N" or "$N.key.0" is step N's result (1-based), e.g. {"layer": "$1.layer"}
```

## layer.quality

Quality

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.quality`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, quality: best|draft|wireframe}
```

## layer.sampling

Sampling

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.sampling`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, sampling: bilinear|bicubic}
```

## layer.frameBlending

Frame Blending

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.frameBlending`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, mode: off|frameMix|pixelMotion}
```

## layer.hideOtherVideo

Hide Other Video

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.hideOtherVideo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.showAllVideo

Show All Video

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.showAllVideo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## layer.unlockAll

Unlock All Layers

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.unlockAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## layer.expressions

Enable/Disable Expressions

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.expressions`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, enabled: bool}
```

场景 / Recipes: [examples/expression-parent-create.json](../examples/expression-parent-create.json)；前置条件见 [表达式父级](expression-parent.md)。

## layer.setTransform

Transform Value

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.setTransform`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, prop: anchor|position|scale|orientation|rotation|opacity, value}
```

## layer.centerAnchor

Center Anchor Point in Layer Content

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.centerAnchor`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.mask.shape

Mask Shape...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.shape`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, rect: [x, y, w, h], shape?: rect|ellipse}
```

## layer.mask.set

Mask Settings

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, field: feather|opacity|expansion, value}
```

## layer.mask.reset

Reset Mask

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?}
```

## layer.mask.remove

Remove Mask

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?}
```

## layer.mask.removeAll

Remove All Masks

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.removeAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.mask.mode

Mask Mode

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.mode`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, mode: None|Add|Subtract|Intersect|Lighten|Darken|Difference}
```

## layer.mask.invert

Inverted

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.invert`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, value?}
```

## layer.mask.lock

Locked

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.lock`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, value?}
```

## layer.mask.unlockAll

Unlock All Masks

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.unlockAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.mask.lockOthers

Lock Other Masks

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.mask.lockOthers`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?}
```

## layer.addMarker

Add Marker

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.addMarker`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, time?, comment?}
```

## layer.markersLock

Lock Markers

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.markersLock`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, value?}
```

## layer.deleteAllMarkers

Delete All Markers

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.deleteAllMarkers`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## layer.trackMatte

Track Matte

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.trackMatte`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?, op: none|alpha|alphaInverted|luma|lumaInverted|above|below}
```

## layer.openSource

Open Layer Source

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.openSource`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## layer.revealInFinder

Reveal in Finder

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.revealInFinder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## layer.revealSource

Reveal Layer Source in Project

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.revealSource`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## comp.revealInProject

Reveal Composition in Project

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.revealInProject`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## layer.revealExpressionErrors

Reveal Expression Errors

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.revealExpressionErrors`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## layer.sequence

Sequence Layers...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.sequence`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers? (in order), overlap?: bool, duration? (s), transition?: off|dissolveFront|crossDissolve}
```

## layer.create

Create

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.create`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{op: editableText|shapesFromText|masksFromText|shapesFromVector, layers?}
```

## anim.savePreset

Save Animation Preset...

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.savePreset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.ecpreset), name?} — saves the selected properties/effects
```

## anim.applyPreset

Apply Animation Preset...

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.applyPreset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path | preset, layers?}
```

## anim.addKeyframe

Add Keyframe

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.addKeyframe`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} — keys the selected properties at the CTI
```

## keys.exponentialScale

Exponential Scale

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.exponentialScale`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} — two selected Scale keys
```

## text.addSelector

Add Text Selector

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.addSelector`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, animator?: uid|index, kind: range|wiggly|expression}
```

## text.removeAllAnimators

Remove All Text Animators

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe text.removeAllAnimators`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## anim.reveal

Reveal Properties

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.reveal`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: keyframes|animation|modified}
```

## view.addGuide

Add Guide...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.addGuide`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{orientation?: vertical|horizontal, position? (comp px)}
```

## view.clearGuides

Clear Guides

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.clearGuides`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## view.importGuides

Import Guides...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.importGuides`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## view.exportGuides

Export Guides...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.exportGuides`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## view.layout

Switch View Layout

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.layout`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{views: 1|2|4}
```

## view.shareViewOptions

Share View Options

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.shareViewOptions`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.extendedViewer

Extended Viewer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.extendedViewer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.setRegionOfInterest

Region of Interest

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.setRegionOfInterest`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rect?: [x, y, w, h] | null}
```

## view.snapping

Snapping

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.snapping`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.displayColorManagement

Use Display Color Management

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.displayColorManagement`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.simulateOutput

Simulate Output

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.simulateOutput`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{profile: none|rec709|ntsc|pal|mac18|srgb|rec2020|p3|linear|myCustom|custom, preserveRgb?, space? (custom)}
```

## view.customRgb

My Custom RGB...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.customRgb`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, red?/green?/blue?/white?: [x, y] (CIE xy), gamma?, srgbCurve?: bool, icc?: path (RGB ICC profile, matrix/TRC or LUT-based A2B0: read when it changes, "" clears; a LUT profile simulates through its tables, `lutProfile` in the reply; typed-in numbers replace it), reload?, from?: a Simulate Output profile to start from, reset?, preserveRgb?, apply?: bool (default true: simulate it)} → the definition (kept in Settings)
```

## view.splitLockedViewer

Split with New Locked Viewer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.splitLockedViewer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, view?: 3D view id}
```

## view.closeLockedViewer

Close Locked Viewer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no locked viewer。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.closeLockedViewer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.displayColor

Viewer Color State

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.displayColor`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → display colour management, output simulation, display profile, locked viewer
```

## view.channel

Show Channel

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.channel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{channel: rgb|red|green|blue|alpha|rgbStraight, colorized?, toggle?}
```

## view.exposure

Adjust Exposure

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.exposure`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stops? | delta?}
```

## view.resetExposure

Reset Exposure

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.resetExposure`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.takeSnapshot

Take Snapshot

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.takeSnapshot`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, scale?: 0.05..1}
```

## view.showSnapshot

Show Snapshot

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: take a snapshot first (Shift+F5)。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.showSnapshot`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.fastPreviewMode

Fast Previews

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.fastPreviewMode`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{mode: off|adaptive|draft|fastDraft|wireframe}
```

## view.moveGuide

Move Guide

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.moveGuide`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, index, position (comp px), merge?}
```

## view.removeGuide

Remove Guide

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.removeGuide`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, index}
```

## shape.newPath

Pen Tool (Shape Path)

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shape.newPath`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, vertices: [[x,y]…], inTangents?, outTangents?, closed?, space?: comp|layer, fill?: [r,g,b]|#hex|false, stroke?, strokeWidth?, name?}
```

## shape.dashes.add

Add Dash or Gap

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shape.dashes.add`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop?: stroke uid}
```

## shape.dashes.remove

Remove Dash or Gap

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shape.dashes.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop?: stroke uid}
```

## shape.stroke.taper

Stroke Taper

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shape.stroke.taper`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop?: stroke uid, units?: pixels|percent, startLength?, endLength?, startWidth? (%), endWidth? (%), startEase? (%), endEase? (%)}
```

## shape.stroke.wave

Stroke Wave

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shape.stroke.wave`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, prop?: stroke uid, amount? (%), units?: pixels|cycles, wavelength?, cycles?, phase? (°)}
```

## camera.linkFocusToPoi

Link Focus Distance to Point of Interest

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.linkFocusToPoi`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, camera?}
```

## camera.linkFocusToLayer

Link Focus Distance to Layer

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.linkFocusToLayer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, camera?, layer?}
```

## camera.setFocusToLayer

Set Focus Distance to Layer

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.setFocusToLayer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, camera?, layer?}
```

## keys.setLabel

Keyframe Label

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.setLabel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{label: name|none|0–16}
```

## keys.selectLabelGroup

Select Keyframe Label Group

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.selectLabelGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{scope: selected|all|visibleSelected|visibleAll, visible?: [prop uid]}
```

## keys.transform

Transform Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.transform`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{timeScale?, timeAnchor? (comp s), timeOffset? (s), valueScale?, valueAnchor?, valueOffset?, dim? | dims?: [d…], merge?, fromStart?: bool (with merge: values are the whole transform since the drag started)}
```

## keys.setSpatialTangents

Edit Spatial Tangents

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.setSpatialTangents`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path|prop, time (layer s), in?: [dx,dy,dz?], out?, break?, merge?}
```

## project.newFolder

New Folder

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.newFolder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, parent?}
```

## file.close

Close

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.close`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## file.closeProject

Close Project

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.closeProject`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.saveCopy

Save a Copy...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.saveCopy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## file.importMultiple

Multiple Files...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importMultiple`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{paths: [string]}
```

## file.importPlaceholder

Placeholder...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importPlaceholder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, width?, height?, frameRate?, duration? (s)}
```

## file.importSolid

Solid...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importSolid`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, color?, width?, height?}
```

## file.newCompFromSelection

New Comp from Selection...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select an item in the Project panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.newCompFromSelection`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{duration? (s, for stills), single?: bool (one comp for all), dimensionsFrom?: index, sequence?: bool, overlap?: bool, overlapDuration? (s), transition?: off|dissolveFront|crossDissolve, addToRenderQueue?: bool} → {comps}
```

## file.collectFiles

Collect Files...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.collectFiles`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folder}
```

## file.consolidateFootage

Consolidate All Footage

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.consolidateFootage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.removeUnusedFootage

Remove Unused Footage

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.removeUnusedFootage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.reduceProject

Reduce Project

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select compositions in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.reduceProject`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (keeps the selected comps and what they use)
```

## file.findMissing

Find Missing

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.findMissing`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{what: footage|effects|fonts}
```

## footage.check

Check Footage

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project is empty。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.check`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?: [id], wait?} — look for every footage file (in the background unless `wait`) and flag missing items
```

## file.runScript

Run Script File...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.runScript`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.jsx/.js JavaScript, or a .jsonl/.json command script) | name (an installed or sample script, see file.scripts.list) | steps: [{command, params}]}
```

## script.run

Run Script

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe script.run`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{code (JavaScript: app, app.project, CompItem, Layer, Property… like After Effects scripting), name?, console? (Script Console context)} → {ok, result, output, error: {message, line, column} | null}
```

## file.interpretFootage

Main...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.interpretFootage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?, frameRate?: fps|"file", alpha?: straight|premultiplied|ignore|guess, guessAlpha?, matteColor?, invertAlpha?, loop?, pixelAspect?, fields?: off|upper|lower, colorProfile?: srgb|rec709|rec2020|p3|auto, linearLight?}
```

## file.rememberInterpretation

Remember Interpretation

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.rememberInterpretation`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?}
```

## file.applyInterpretation

Apply Interpretation

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.applyInterpretation`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?}
```

## file.replaceFootage

File...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.replaceFootage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path, item?}
```

## file.replaceWithPlaceholder

Placeholder...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.replaceWithPlaceholder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?, width?, height?, frameRate?, duration?}
```

## file.replaceWithSolid

Solid...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.replaceWithSolid`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?, color?, width?, height?}
```

## file.reloadFootage

Reload Footage

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.reloadFootage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?}
```

## file.revealInFinder

Reveal in Finder

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select footage in the Project panel。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.revealInFinder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?}
```

## file.exportLottie

Lottie JSON...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.exportLottie`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, path (.json or .lottie), includeExpressions?: bool, textAsShapes?: bool}
```

## file.importLottie

Lottie...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importLottie`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.json or .lottie)}
```

## file.importTimeline

Adobe Premiere Pro Project...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importTimeline`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.xml Final Cut Pro XML from Premiere Pro or .fcpxml .otio .edl .aaf .omf), format?: auto|xml|fcpxml|otio|edl|aaf|omf, edlFrameRate?: number}
```

## file.exportTimeline

Adobe Premiere Pro Project...

- 技能 / Owner: `effectcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.exportTimeline`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, path (Final Cut Pro XML .xml for Premiere Pro or .fcpxml .otio .edl .aaf .omf), format?: xml|fcpxml|otio|edl|aaf|omf, prerender?: none|unsupported|all, precomps?: nest|prerender}
```

## file.timelineFormats

Timeline Interchange Formats

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.timelineFormats`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## comp.cropToRegionOfInterest

Crop Comp to Region of Interest

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.cropToRegionOfInterest`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## comp.cropToLayerBounds

Crop Comp to Selected Layer(s) Bounds

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.cropToLayerBounds`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layers?}
```

## comp.saveFrameAs

File...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.saveFrameAs`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.png; with queue: an output path or template), time?, scale?, queue?: bool (add a Render Queue item from the Frame Default templates instead of writing now)}
```

## comp.responsiveTime

Responsive Design — Time

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.responsiveTime`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{op: intro|outro|workArea}
```

## comp.saveFrameAsPsd

Photoshop Layers...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.saveFrameAsPsd`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.psd), comp?, time?, scale?} → a layered PSD: one layer per visible comp layer (blend mode, opacity) + the merged frame
```

## comp.saveFrameAsExr

ProEXR...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.saveFrameAsExr`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.exr), comp?, time?, scale?} → a multi-layer OpenEXR: composite R,G,B,A + `<layer>.R/G/B/A` per layer (linear, premultiplied)
```

## file.watchFolder

Watch Folder...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.watchFolder`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folder, stop?: bool} → watches the folder for .ecproj files with queued renders, renders them and writes `<project>.status.json`
```

## file.watchFolder.poll

Poll Watch Folder

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no folder is being watched。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.watchFolder.poll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folder? (default: the watched one)} → renders new projects now: {watching, rendered: [{project, state: done|failed, items: [{comp, status, output}]}]}
```

## file.importVanishingPoint

Vanishing Point (.vpe)...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: Vanishing Point Exchange (.vpe) files can't be imported: the format has no public specification, and EffectCraft only implements documented formats。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importVanishingPoint`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (always disabled: undocumented format)
```

## paths.pointsFollowNulls

Points Follow Nulls

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paths.pointsFollowNulls`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path?|prop?, pins?: [uid | name…]} → a null per vertex (or Position / Advanced puppet pin); the path (pins) follow them (expressions)
```

## paths.nullsFollowPoints

Nulls Follow Points

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paths.nullsFollowPoints`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path?|prop?, pins?: [uid | name…]} → a null per vertex (or puppet pin) following it (Position expressions)
```

## paths.tracePath

Trace Path

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paths.tracePath`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, path?|prop?, loop?: bool} → a null moving along the path (Progress slider)
```

## comp.vr.environments

VR Environments

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.vr.environments`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [{output, name, cubeMap, faces: [{face, comp, camera}], view: [x, y, z]}]
```

## comp.vr.setView

VR View Orientation

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.vr.setView`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp? (an environment's output / cube map / face comp), orientation?: [x, y, z] degrees, pan?, tilt?, roll?} → turns the six face cameras together
```

## app.about

About EffectCraft...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.about`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## layer.style.options

Layer Style Options...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.style.options`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, style?: blendingOptions|dropShadow|…}
```

## app.settings

Settings...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.settings`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{page?: general|startup|project|composition|previews|appearance|grids|labels|type|import|export|audio|disk|memory|video|3d|scripting}
```

## app.gpuInfo

GPU Information...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.gpuInfo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## app.hide

Hide EffectCraft

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.hide`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## app.hideOthers

Hide Others

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.hideOthers`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## app.showAll

Show All

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.showAll`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## app.quit

Quit EffectCraft

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.quit`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## app.commandPalette

Quick Apply...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.commandPalette`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{query?}
```

## app.keyboardShortcuts

Keyboard Shortcuts

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.keyboardShortcuts`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## app.templates

Templates

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.templates`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: renderSettings|outputModule}
```

## app.find

Find

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe app.find`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{query?}
```

## playback.toggle

Play Current Preview

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe playback.toggle`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{shortcut?: spacebar|shiftSpacebar|numpad0|shiftNumpad0|altNumpad0 (whose Preview panel options to use; default spacebar)}
```

## playback.cacheWhenIdle

Cache Frames When Idle

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe playback.cacheWhenIdle`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## playback.audio

Audio

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe playback.audio`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?: include audio in previews}
```

## playback.scrubAudio

Scrub Audio

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe playback.scrubAudio`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{time? (s, default the current time)} — plays one frame of the comp's audio there (Ctrl/Cmd-drag the current time)
```

## view.zoomIn

Zoom In

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.zoomIn`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.zoomOut

Zoom Out

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.zoomOut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.res.full

Full

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.res.full`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.res.half

Half

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.res.half`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.res.third

Third

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.res.third`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.res.quarter

Quarter

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.res.quarter`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.res.custom

Custom...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.res.custom`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{factor?: 1..40 (render every n-th pixel)}
```

## view.rulers

Show Rulers

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.rulers`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.panelBackground

Panel Background Color

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.panelBackground`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{color?: black|darkGray|mediumGray|lightGray|white|custom|#hex, pick?: true}
```

## view.guides

Show Guides

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.guides`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.snapToGuides

Snap to Guides

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.snapToGuides`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.lockGuides

Lock Guides

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.lockGuides`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.grid

Show Grid

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.grid`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.snapToGrid

Snap to Grid

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.snapToGrid`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.options

View Options...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.options`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.layerControls

Show Layer Controls

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.layerControls`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?}
```

## view.fullScreen

Enter Full Screen

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.fullScreen`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## view.newViewer

New Viewer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.newViewer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} — another Composition viewer of the active comp; the one in use is locked
```

## window.panel

Show Panel

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.panel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{panel: project|effectControls|composition|layer|timeline|info|audio|preview|effectsPresets|properties|character|paragraph|align|tracker|wiggler|smoother|motionSketch|paint|brushes|renderQueue|flowchart|history|markers|tools|lumetriScopes|footage|mediaBrowser|metadata|progress|contentAwareFill|createNullsFromPaths|vrCompEditor}
```

## window.workspace

Workspace

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.workspace`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name: Default|Standard|Small Screen|Animation|Effects|Motion Tracking|Paint|Text|Minimal|All Panels}
```

## window.saveWorkspace

Save Changes to this Workspace

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.saveWorkspace`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## window.saveWorkspaceAs

Save as New Workspace...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.saveWorkspaceAs`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name}
```

## window.editWorkspaces

Edit Workspaces...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.editWorkspaces`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, rename?: new name, delete?: bool}
```

## window.resetWorkspace

Reset to Saved Layout

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.resetWorkspace`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## comp.flowchart

Composition Flowchart

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.flowchart`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## comp.miniFlowchart

Composition Mini-Flowchart

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.miniFlowchart`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## layer.openLayer

Open Layer

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.openLayer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## effect.manage

Manage Effects...

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.manage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## anim.browsePresets

Browse Presets...

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.browsePresets`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## track.motion

Track Motion

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.motion`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## track.stabilize

Stabilize Motion

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.stabilize`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?}
```

## track.new

New Tracker

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.new`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, kind?: transform|stabilize|affine|perspective|raw, position?, rotation?, scale?, target?: layer}
```

## track.property

Track this Property

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.property`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, source?: layer}
```

## track.select

Current Track

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.select`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?: uid|name|#n}
```

## track.setType

Track Type

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.setType`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?, kind?: transform|stabilize|affine|perspective|raw, position?, rotation?, scale?}
```

## track.setTarget

Edit Target

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.setTarget`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?, target: layer|null}
```

## track.options

Motion Tracker Options

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.options`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?, name?, channel?: rgb|luminance|saturation, blur? (px, 0 = off), enhance?, subpixel?, adaptEveryFrame?, threshold? (%), action?: continue|stop|extrapolate|adapt, trackShape?}
```

## track.setPoint

Move Track Point

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.setPoint`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?, point: n (1-based), center?: [x,y], featureSize?: [w,h], searchOffset?: [x,y], searchSize?: [w,h], attachOffset?: [x,y], move?: [dx,dy], time? (s)}
```

## track.analyze

Analyze

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.analyze`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?, direction?: forward|backward|frameForward|frameBackward, start? (s), end? (s), wait?: block until done}
```

## track.stop

Stop Analysis

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no track analysis is running。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.stop`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## track.apply

Apply

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.apply`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?, dimensions?: xy|x|y}
```

## track.reset

Reset

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?}
```

## track.delete

Delete Tracker

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.delete`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?}
```

## track.editTargetDialog

Edit Target...

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.editTargetDialog`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## track.optionsDialog

Options...

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no active composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.optionsDialog`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## track.status

Tracker Status

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.status`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, tracker?}
```

## track.mask

Track Mask

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.mask`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?: uid|index|name, method?: position|positionScale|positionScaleRotation|positionScaleRotationSkew|perspective|faceOutline|faceDetailed, direction?: forward|backward|frameForward|frameBackward, start? (s), end? (s), wait?: block until done}
```

## track.maskMethod

Mask Tracking Method

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.maskMethod`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{method: position|positionScale|positionScaleRotation|positionScaleRotationSkew|perspective|faceOutline|faceDetailed}
```

## track.extractFaceMeasurements

Extract & Copy Face Measurements

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.extractFaceMeasurements`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?} → keys a Face Measurements effect from the layer's Face Track Points (one key per tracked frame) and copies those keys
```

## mask.interpolate

Apply Mask Interpolation

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.interpolate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mask?, times?: [from, to] (s; default the selected Mask Path keys), keyframeRate?: n|auto, keyframeFields?, linearVertexPaths?, bendingResistance? (0-100), quality? (0-100), addVertices?: n|false, addVerticesUnit?: pixels|total|percent, matchingMethod?: auto|curve|polyline, oneToOne?, firstVerticesMatch?}
```

## mask.interpolationOptions

Mask Interpolation Options

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mask.interpolationOptions`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{keyframeRate?: n|auto, keyframeFields?, linearVertexPaths?, bendingResistance?, quality?, addVertices?: n|false, addVerticesUnit?: pixels|total|percent, matchingMethod?: auto|curve|polyline, oneToOne?, firstVerticesMatch?}
```

## track.warpStabilizer

Warp Stabilizer VFX

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.warpStabilizer`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, wait?}
```

## warp.analyze

Analyze

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe warp.analyze`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?: uid|name|index, wait?: block until done}
```

## warp.cancel

Cancel

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no Warp Stabilizer analysis is running。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe warp.cancel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## warp.status

Warp Stabilizer Status

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe warp.status`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?}
```

## track.camera

Track Camera

- 技能 / Owner: `effectcraft-cli-tracking`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-tracking`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe track.camera`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, shotType?: fixed|variable|specify, aov?: degrees, solveMethod?: auto|typical|flat|tripod, detailed?, lensDistortion?: solve k1/k2, undistort?: render undistorted, wait?}
```

## camera.analyze

Analyze

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.analyze`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?: uid|name|index, wait?: block until done}
```

## camera.cancel

Cancel

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no 3D Camera Tracker analysis is running。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.cancel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## camera.solveStatus

3D Camera Tracker Status

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.solveStatus`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?}
```

## camera.points

3D Camera Tracker Points

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.points`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?, time?: comp seconds} → visible solved points
```

## camera.selectPoints

Select Track Points

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.selectPoints`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [id], add?, toggle?}
```

## camera.createFromSolve

Create from Camera Solve

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.createFromSolve`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: text|solid|null|shadowCatcher|camera, points?: [id] (default: selected), target?: {center, normal, size?} (comp world), multiple?, layer?, effect?}
```

## camera.create

Create Camera

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.create`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?}
```

## camera.setGroundPlane

Set Ground Plane and Origin

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.setGroundPlane`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points?: [id] (default: selected), layer?, effect?}
```

## camera.deletePoints

Delete Selected Points

- 技能 / Owner: `effectcraft-cli-camera`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-camera`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe camera.deletePoints`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points?: [id] (default: selected), layer?, effect?, wait?}
```

## roto.stroke

Roto Brush Stroke

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.stroke`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, kind?: fg|bg|refine|refineErase, points: [[x, y], …] (layer pixels), frame? (layer frame; default current), radius? (layer px; default the tool's diameter / 2), effect?}
```

## roto.propagate

Propagate Roto Brush

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.propagate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?, direction?: forward|backward|both, to? (layer frame: extend the span), wait?: block until done}
```

## roto.span

Set Segmentation Span

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.span`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?, start?, end? (layer frames)}
```

## roto.freeze

Freeze

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.freeze`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?, wait?}
```

## roto.unfreeze

Unfreeze

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.unfreeze`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?}
```

## roto.clearStrokes

Remove Roto Brush Strokes

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.clearStrokes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?, frame? (only this layer frame), kind?}
```

## roto.cancel

Stop Roto Brush

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no Roto Brush job is running。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.cancel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## roto.options

Roto Brush Options

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.options`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{diameter?, refineDiameter?, view?: alphaBoundary|alpha|alphaOverlay|none, overlayColor?: [r,g,b], overlayOpacity?, boundaryColor?: [r,g,b], autoPropagate?}
```

## roto.status

Roto Brush Status

- 技能 / Owner: `effectcraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe roto.status`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?, frame? (layer frame: also report its matte), matte?: include the matte (RLE, base64), compute?: compute the frame if needed, compareTo?: RLE matte to report the IoU against}
```

## paint.stroke

Paint Stroke

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.stroke`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, kind?: brush|clone|eraser, points: [[x,y,pressure?],…] (layer space), time? (s) | frame?, duration? (s, drawing time for Write On), color?: [r,g,b,a], diameter?, angle?, hardness?, roundness?, spacing?, opacity?, flow?, mode?, channels?: RGBA|RGB|Alpha, durationMode?: constant|writeOn|singleFrame|custom, customFrames?, eraseMode?: layerSourceAndPaint|paintOnly|lastStrokeOnly, cloneSource?: layer id, clonePosition?: [x,y], cloneTimeShift? (s), lockSourceTime?, cloneTime? (s), sizePressure?, minSize?, opacityPressure?, flowPressure?}
```

## paint.options

Paint Options

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.options`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{color?, background?, opacity?, flow?, mode?, channels?, durationMode?, customFrames?, eraseMode?, diameter?, angle?, roundness?, hardness?, spacing?, preset?, sizePressure?, minSize?, opacityPressure?, flowPressure?, clonePreset?, cloneSource?, clonePoint?, cloneOffset?, aligned?, lockSourceTime?, cloneTimeShift?, cloneTime?, showOverlay?, overlayOpacity?, overlayDifference?, reset?}
```

## paint.brushPreset

Brush Preset

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.brushPreset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{preset?: index | name}
```

## paint.setCloneSource

Set Clone Source

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.setCloneSource`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, point: [x,y]}
```

## paint.removeStroke

Delete Paint Stroke

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.removeStroke`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, stroke: uid | name}
```

## paint.presets

Brush Presets

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.presets`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## puppet.addPin

Add Puppet Pin

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.addPin`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, kind?: position|advanced|bend|starch|overlap, position: [x,y] (layer space), time? (s) | frame?, mesh?: uid, newMesh?, density?, expansion?, triangles?}
```

## puppet.movePin

Move Puppet Pin

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.movePin`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, pin: uid | name, position: [x,y], time? | frame?, merge?}
```

## puppet.setPin

Edit Puppet Pin

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.setPin`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, pin: uid | name, position?, scale? (%), rotation? (°), amount? (%), extent? (px), inFront?, time? | frame?, merge?}
```

## puppet.removePin

Delete Puppet Pin

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.removePin`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, pin?: uid | name, pins?: [uid | name…]} (default: the selected pins)
```

## puppet.selectPins

Select Puppet Pins

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.selectPins`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, pins: [uid | name…] ([] deselects), add?, toggle?}
```

## puppet.mesh

Puppet Mesh Options

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.mesh`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mesh?: uid, density?, expansion?, triangles?, showMesh?, time?, merge?}
```

## puppet.info

Puppet Mesh Info

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.info`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, time? | frame?}
```

## puppet.recordPin

Record Puppet Pin

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.recordPin`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, pin: uid | name, samples: [[t, x, y]…] (t = seconds since the drag began, layer space), pins?: [uid | name…] (more pins that move by the same displacement), start? (s, default current time), speed? (%, Record Options), smoothing? (Record Options)}
```

## puppet.follow

Follow-Through...

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.follow`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, leader?: uid | name (default: the first selected pin), pins?: [uid | name…] (default: the other selected pins), delay? (s, 0.1), amount? (%, 100), cascade? (true: the k-th nearest pin trails k × delay)}
```

## puppet.recordOptions

Record Options...

- 技能 / Owner: `effectcraft-cli-puppet`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-puppet`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.recordOptions`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{speed? (%, 100), smoothing? (0-100), useDraftDeformation?, showMesh?}
```

## liquify.stroke

Liquify Stroke

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe liquify.stroke`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?: uid, tool?: warp|turbulence|twirlClockwise|twirlCounterclockwise|pucker|bloat|shiftPixels|reflection|clone|reconstruction|freeze|thaw, points: [[x,y],…] (layer space), size?, pressure? (1-100), jitter? (1-100), cloneOffset?: [dx,dy], time? (s) | frame?}
```

## liquify.clear

Clear Liquify Mesh

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe liquify.clear`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, effect?: uid}
```

## prefs.get

Get Setting

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prefs.get`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{key?: e.g. general.undoLevels (omit for all settings)}
```

## prefs.set

Change Setting

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prefs.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{key, value, values?: {key: value}}
```

## prefs.reset

Reset Settings

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prefs.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{page?: general|labels|project|…}
```

## prefs.open

Open Settings

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prefs.open`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{page?: general|startup|project|composition|previews|appearance|grids|labels|type|import|export|audio|disk|memory|video|3d|scripting}
```

## prefs.pages

Settings Pages

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe prefs.pages`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## shortcuts.list

List Keyboard Shortcuts

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{query?, keys?, assigned?: bool}
```

## shortcuts.set

Set Keyboard Shortcut

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{command, params?, keys: "Cmd+Shift+K" | [keys] | null}
```

## shortcuts.reset

Reset Keyboard Shortcuts

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.reset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{command?, params?}
```

## shortcuts.preset

Keyboard Shortcut Preset

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.preset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{op: select|new|duplicate|delete|rename, name?, from?, newName?}
```

## shortcuts.export

Export Keyboard Shortcuts

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.export`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{preset?, path?}
```

## shortcuts.import

Import Keyboard Shortcuts

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.import`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path? | preset?: exported document, name?}
```

## shortcuts.conflicts

Keyboard Shortcut Conflicts

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe shortcuts.conflicts`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.openRecent

Open Recent

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no recent projects。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.openRecent`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index? | path?}
```

## file.clearRecent

Clear Recent Projects

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no recent projects。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.clearRecent`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.autoSave

Auto-Save Now

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.autoSave`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.recoveryInfo

Auto-Save Status

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.recoveryInfo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## edit.history

History

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: nothing to undo。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe edit.history`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{steps?: n (undo n steps), redo?: n}
```

## file.importRecent

Import Recent Footage

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no recent footage。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.importRecent`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index? | path?}
```

## file.clearRecentFootage

Clear Recent Footage

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no recent footage。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.clearRecentFootage`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## anim.applyRecentPreset

Recent Animation Presets

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.applyRecentPreset`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index? | path?, layers?}
```

## anim.clearRecentPresets

Clear Recent Presets

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no recent animation presets。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe anim.clearRecentPresets`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.saveCopyAsXml

Save a Copy As XML...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.saveCopyAsXml`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path: .ecprojx}
```

## file.replaceWithLayeredComp

With Layered Comp

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select an item in the Project panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.replaceWithLayeredComp`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?}
```

## file.executeFile

Execute File

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.executeFile`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path, confirmed?}
```

## view.assign3dShortcut

Assign Shortcut to 3D View

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe view.assign3dShortcut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{slot: F10|F11|F12, comp?}
```

## window.assignWorkspaceShortcut

Assign Shortcut to Workspace

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.assignWorkspaceShortcut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{slot: Shift+F10|Shift+F11|Shift+F12, workspace?}
```

## help.enableLogging

Enable Logging

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.enableLogging`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?}
```

## help.revealLogFile

Reveal Logging File

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.revealLogFile`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## help.systemReport

System Compatibility Report...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.systemReport`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{quiet?}
```

## comp.vr.createEnvironment

Create VR Environment...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.vr.createEnvironment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, size?: face pixels (1024), position?: [x,y,z]}
```

## comp.vr.extractCubemap

Extract Cubemap...

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.vr.extractCubemap`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, faceSize?}
```

## help.systemInfo

System Information

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe help.systemInfo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## keys.audioToKeyframes

Convert Audio to Keyframes

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.audioToKeyframes`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?}
```

## keys.rpfCameraImport

RPF Camera Import

- 技能 / Owner: `effectcraft-cli-animation`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-animation`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe keys.rpfCameraImport`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path: .json|.csv camera data, comp?}
```

## essential.setPrimary

Primary Composition

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.setPrimary`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp}
```

## essential.setName

Essential Graphics Name

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.setName`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, name}
```

## essential.addProperty

Add Property to Essential Graphics

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.addProperty`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, layer?, path?|prop?: uid (default: the selected properties), name?, group?: control id, index?, as?: font (Source Text font family/style/size) | scale (uniform Scale), mirror?: bool (a property already present is added as a mirror; default true)}
```

## essential.addMirror

Add Mirror

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.addMirror`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, control, name?, group?, index?}
```

## essential.linkProperty

Link Property to Control

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.linkProperty`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, control, layer?, path?|prop? (default: the selected property)}
```

## essential.unlinkProperty

Unlink Property

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.unlinkProperty`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, control, layer?, path?|prop? (default: the selected property)}
```

## essential.addMedia

Add Media Replacement

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.addMedia`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer, name?, group?}
```

## essential.addGroup

Add Group

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.addGroup`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, name?, index?}
```

## essential.addComment

Add Comment

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.addComment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, text?, group?}
```

## essential.rename

Rename Control

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.rename`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, control, name}
```

## essential.remove

Remove Control

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.remove`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, control}
```

## essential.move

Move Control

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.move`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, control, group?: id (null = top level), index?}
```

## essential.soloSupported

Solo Supported Properties

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.soloSupported`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?}
```

## essential.exportTemplate

Essential Graphics Template...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.exportTemplate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, path (.ectemplate), name?}
```

## essential.importTemplate

Essential Graphics Template...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.importTemplate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.ectemplate), comp?, addToComp?: bool}
```

## essential.set

Set Essential Property

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer, control: id|name, value | item (media)}
```

## essential.pushToComp

Push Override Values to Source

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.pushToComp`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer, control? (default: all overridden)}
```

## essential.revert

Revert

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.revert`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer, control? (default: all overridden)}
```

## effect.editDropdown

Edit Dropdown Menu

- 技能 / Owner: `effectcraft-cli-effects`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-effects`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe effect.editDropdown`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer, path?|prop?, items: [string]}
```

## essential.list

Essential Graphics controls

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, supported?: bool}
```

## essential.canAdd

Can Add Property to Essential Graphics

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.canAdd`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer, path|prop, as?} → {ok, type?, reason?}
```

## comp.openInEssentialGraphics

Open in Essential Graphics

- 技能 / Owner: `effectcraft-cli-composition`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-composition`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe comp.openInEssentialGraphics`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?} → makes it the Essential Graphics panel's Primary composition and shows the panel
```

## essential.instance

Essential Properties of a precomp layer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.instance`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer}
```

## essential.templateInfo

Read a template's manifest

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe essential.templateInfo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## expr.errors

Expression errors (the error bar)

- 技能 / Owner: `effectcraft-cli-expressions`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-expressions`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe expr.errors`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, time? (s)}
```

## expr.languageMenu

Expression Language menu

- 技能 / Owner: `effectcraft-cli-expressions`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-expressions`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe expr.languageMenu`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## file.createProxy

Create Proxy

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select a composition。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.createProxy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: still|movie, comp?|item?, path?|output? (template), resolution? (default 0.5)}
```

## file.setProxy

File...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select an item in the Project panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.setProxy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path, items?|item?}
```

## file.setProxyNone

None

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select an item in the Project panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.setProxyNone`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?|item?}
```

## file.useProxy

Use Proxy

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select an item in the Project panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.useProxy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?|item?, on?}
```

## file.interpretProxy

Proxy...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: select an item in the Project panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.interpretProxy`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items?|item?, alpha?, matteColor?, invertAlpha?, frameRate?, loop?, pixelAspect?, fields?, colorProfile?, linearLight?}
```

## file.installScript

Install Script File...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.installScript`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.jsx / .js)} → copies it to the Scripts folder; it appears in File ▸ Scripts
```

## file.installScriptUIPanel

Install ScriptUI Panel...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.installScriptUIPanel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path (.jsx / .js)} → copies it to the ScriptUI Panels folder; it appears in the Window menu
```

## file.uninstallScript

Uninstall Script

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.uninstallScript`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name}
```

## file.scripts.list

List Scripts

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.scripts.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [{name, panel, source: installed|sample}]
```

## window.scriptPanel

ScriptUI Panel

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe window.scriptPanel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name (a script in the ScriptUI Panels folder, e.g. `Layer Tools.jsx`)} → opens it as a dockable panel
```

## scriptui.list

List Script Windows

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe scriptui.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [{window, title, kind: dialog|palette|window|panel, script, modal, size}]
```

## scriptui.get

Script Window Controls

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe scriptui.get`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{window?: id | title} → {id, title, kind, root: {id, type, name, text, value, checked, items, selection, bounds, enabled, draw (onDraw paint list), children…}}
```

## scriptui.click

Click Script Window Control

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe scriptui.click`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{window?: id | title, widget: id | "#id" | properties.name | text} (buttons, checkboxes, radio buttons, tabs)
```

## scriptui.set

Set Script Window Control

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe scriptui.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{window?, widget, value: text | number | bool | item index | item text, changing?: bool (a live update: each keystroke / slider step; fires onChanging only)} (edit text, sliders, checkboxes, lists) → fires onChanging / onChange
```

## scriptui.close

Close Script Window

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe scriptui.close`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{window?, result? (a dialog's show() returns it; default 2 = Cancel)}
```

## jobs.list

Background Jobs

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe jobs.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## jobs.cancel

Cancel Job

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe jobs.cancel`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{job?: render|track|maskTrack|warp|camera|roto|task:<n>|all}
```

## jobs.wait

Wait for Background Jobs

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe jobs.wait`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## mediaBrowser.list

List Folder

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, importableOnly?}
```

## mediaBrowser.go

Go to Folder

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.go`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?: folder | "..", importableOnly?}
```

## mediaBrowser.addFavorite

Add to Favorites

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.addFavorite`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?}
```

## mediaBrowser.removeFavorite

Remove from Favorites

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.removeFavorite`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?}
```

## mediaBrowser.import

Import

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.import`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{paths, addToComp?, time?, index?, position? (where the layers go, as in layer.addItem)}
```

## mediaBrowser.action

Media Browser Action

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.action`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{action}: an action from mediaBrowser.list's `actions` (web: openFolder, addFiles, uploadFolder)
```

## mediaBrowser.fileInfo

File Info

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe mediaBrowser.fileInfo`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path}
```

## item.metadata

Metadata

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe item.metadata`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?: id|name}
```

## project.setProjectComment

Project Comment

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe project.setProjectComment`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comment}
```

## scopes.analyze

Lumetri Scopes

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe scopes.analyze`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{comp?, time?|frame?, scope?: waveformRgb|waveformLuma|waveformYc|vectorscopeYuv|vectorscopeHls|histogram|paradeRgb|paradeYuv, standard?: rec601|rec709|rec2020, float?, clamp?, size?}
```

## footage.open

Open in Footage Panel

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.open`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item: id|name}
```

## footage.info

Footage Panel State

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.info`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## footage.setTime

Footage Panel Time

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: open footage in the Footage panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.setTime`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{time? (s, source) | frame?}
```

## footage.setIn

Set In Point

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: open footage in the Footage panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.setIn`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{time? | frame? (default: the panel's time)}
```

## footage.setOut

Set Out Point

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: open footage in the Footage panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.setOut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{time? | frame? (default: the panel's time)}
```

## footage.clearInOut

Clear In and Out

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: open footage in the Footage panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.clearInOut`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## footage.overlayEdit

Overlay Edit

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: open footage in the Footage panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.overlayEdit`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?, comp?, in? (s), out? (s), at? (comp s; default the current time)}
```

## footage.rippleInsertEdit

Ripple Insert Edit

- 技能 / Owner: `effectcraft-cli-footage`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-footage`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: open footage in the Footage panel first。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe footage.rippleInsertEdit`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?, comp?, in? (s), out? (s), at? (comp s; default the current time)}
```

## layer.autoTrace

Auto-trace...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.autoTrace`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, timeSpan?: currentFrame|workArea, channel?: alpha|red|green|blue|luminance, invert?, blur? (px, 1), tolerance? (px, 1), threshold? (%, 50), minimumArea? (px, 10), cornerRoundness? (%, 50), applyToNewLayer?}
```

## layer.sceneEditDetection

Scene Edit Detection...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.sceneEditDetection`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, mode?: markers|split|splitPrecompose, threshold? (0…1, 0.25), wait?: bool}
```

## layer.alignVideoToData

Align Video to Data

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.alignVideoToData`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, data?: data footage id|name, key?: time field, videoStart?: ISO date-time | hh:mm:ss | timecode | seconds (default: file creation time), dataStart? (comp s of the first sample, 0)}
```

## layer.align

Align Layers

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.align`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{edge: left|hcenter|right|top|vcenter|bottom, to?: composition|selection (default composition), layers?}
```

## layer.distribute

Distribute Layers

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.distribute`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{mode: left|hcenter|right|top|vcenter|bottom (edges or centres), layers?}
```

## contentFill.set

Content-Aware Fill Settings

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe contentFill.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{method?: object|surface|edgeBlend, range?: workArea|entire, alphaExpansion? (px), lightingCorrection?: none|subtle|moderate|strong, referenceLayer?: layer|null, referenceTime? (s)}
```

## contentFill.generate

Generate Fill Layer

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: no composition is open。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe contentFill.generate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, method?: object|surface|edgeBlend, range?: workArea|entire, alphaExpansion? (px), lightingCorrection?: none|subtle|moderate|strong, referenceLayer?, referenceTime? (s), outputDir?, wait?: bool}
```

## layer.newContentAwareFill

Content-Aware Fill Layer...

- 技能 / Owner: `effectcraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newContentAwareFill`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{layer?, method?: object|surface|edgeBlend, range?: workArea|entire, alphaExpansion? (px), lightingCorrection?: none|subtle|moderate|strong, referenceLayer?, referenceTime? (s), outputDir?, wait?: bool}
```

## storage.info

Browser Storage

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe storage.info`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {available, backend, usage, quota, persisted, files: {count, bytes, media, projects, autoSaves}, diskCache: {enabled, entries, bytes, maxBytes, hits, misses, writes, evictions}}
```

## storage.persist

Request Persistent Storage

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: browser storage is only managed in the web app。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe storage.persist`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {requested, persisted}
```

## storage.clear

Clear Browser Storage

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: browser storage is only managed in the web app。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe storage.clear`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{what: diskCache|media|projects|autoSaves|all} → {cleared, entries, bytes}
```

## learn.list

Learn Tutorials

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe learn.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [{id, title, summary, minutes, steps}]
```

## learn.state

Tutorial State

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe learn.state`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {tutorial, step, steps, done, current: {title, text, target, accepts}} | null
```

## learn.start

Start Tutorial

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe learn.start`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## learn.step

Tutorial Step

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe learn.step`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{action?: next|back|showMe|goto, index?}
```

## learn.stop

Close Tutorial

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe learn.stop`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (no parameter documentation in snapshot)
```

## templates.list

Project Templates

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe templates.list`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{thumbnails?: bool} → [{id, name, description, category, builtin, width, height, frameRate, duration, controls, thumbnail? (hex RGB 256×144)}]
```

## templates.thumbnail

Template Thumbnail

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe templates.thumbnail`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id} → {id, width, height, rgb (hex)}
```

## templates.create

New Project from Template

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe templates.create`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id (templates.list) | path (.ectemplate), projectPath? (save the new project there; embedded footage goes to `<stem> Footage/` next to it), footageDir?} → an untitled copy (embedded footage extracted: `footage` lists the files)
```

## templates.saveAs

Save as Template...

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: the project has no compositions。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe templates.saveAs`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, description?, category?, overwrite?: bool (default true), embedFootage?: bool (default true: the footage files go into the template), embedLimitMB? (default 256: footage beyond it stays linked, with a warning)} → {id, path, embedded, embeddedBytes, linked: [{item, name, reason}], warning?}
```

## templates.delete

Delete Template

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe templates.delete`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id: user/<file>}
```

## file.newFromTemplate

New Project from Template...

- 技能 / Owner: `effectcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe file.newFromTemplate`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → the Home screen's Templates tab
```

## playback.settings.get

Preview Settings

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe playback.settings.get`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{shortcut?: spacebar|shiftSpacebar|numpad0|shiftNumpad0|altNumpad0 (default: the one shown in the Preview panel)} → options + plan {start, end, first, step, fps}
```

## playback.settings.set

Change Preview Settings

- 技能 / Owner: `effectcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe playback.settings.set`；按原生参数构造计划后执行 run。
- 运行模式路由 / Mode routes: headless / owned desktop; live availability required, each NOT_RUN。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{shortcut?, current?: shortcut shown in the panel, reset?: bool, values?: {…}, includeVideo?, includeAudio?, includeOverlays?, includeLayerControls?, loop?, cacheBeforePlayback?, range?: workArea|workAreaExtended|entireDuration|aroundCurrentTime, preRoll?, postRoll?: seconds, playFrom?: rangeStart|currentTime, frameRate?: fps|"auto", skip?, resolution?: auto|full|half|third|quarter|custom, customResolution?, fullScreen?, playCachedFrames?, moveTimeToPreviewTime?}
```
