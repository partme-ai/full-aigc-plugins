# 完整原生命令参考 / Complete native command reference

本参考逐项保留锁定参数原文与技能路由。命令执行必须满足当前工程、选择对象、素材或 GUI 前置状态。
This reference preserves each pinned parameter contract and skill owner. Query live state before invocation.

使用方法见 [完整调用指南](command-usage.md)。全部参数均为原生语法说明，不把它们假装成 JSON Schema。
每项 NOT_RUN 指本轮完整逐命令验收；既有代表任务证据仍单独保留。

## file.new

New…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{preset?: a name from file.newPresets (start from it; the other params change it), name?|title?: document name (default Untitled-N), width?: pt=612|"210 mm", height?: pt=792, units?: "Pixels"|"Points"|"Picas"|"Inches"|"Millimeters"|"Centimeters"|"Feet"|"Yards"|"Meters"|"Feet & Inches" (default: prefs unitsGeneral, as print presets; screen presets: Pixels), orientation?: "portrait"|"landscape" (swaps width and height to match), artboards?: n (1–1000), artboardLayout?: {layout?: "gridByRow"|"gridByColumn"|"row"|"column", columns?: n (default: all in one row), spacing?: pt=20, rightToLeft?: bool}, bleed?: pt|[top, bottom, left, right]|{top?, …} (0–72 pt), backgroundContents?: "transparent"|"white" (a white artboard background, not an object), colorMode?: "rgb"|"cmyk" (a CMYK document starts with CMYK swatches and stores the colours applied to it as CMYK), rasterEffectsPpi?: 72|150|300 (1–2400), previewMode?: "default"|"pixel"|"overprint" (overprint turns Overprint Preview on, pixel Pixel Preview in the app; default leaves both), created?: Unix seconds|null (File Info's created date; default now, recorded in the journal so a replay matches)} → {index, previewMode}; the size is remembered in file.newPresets' Recent
```

## file.close

Close

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.close`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index?}
```

## document.activate

Activate Document

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.activate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index}
```

## document.inspect

Inspect Document

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → layer tree, artboards, selection, history
```

## document.node

Inspect Object

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.node`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id} → full object JSON
```

## document.json

Document JSON

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.json`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → complete document model
```

## document.setUnits

Units

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.setUnits`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{units: "Points"|"Picas"|"Inches"|"Millimeters"|"Centimeters"|"Pixels"|"Feet & Inches"|"Meters"|"Yards"|"Feet"} the document's units: every length the UI shows and reads (General)
```

## edit.undo

Undo

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.undo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.redo

Redo

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.redo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.cut

Cut

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.cut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.copy

Copy

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.copy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.paste

Paste

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.paste`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{center?: [x, y], dx?, dy?, swatchConflict?} paste centred on `center` (the app passes the view centre), else offset by dx/dy (default: the Paste Offset preference). Pasting brings the image blobs, symbols, patterns, global and spot swatches (with the tint swatches of the tints used), gradient swatches, graphic styles, character and paragraph styles and brushes the objects use; one of the same name that differs comes in renamed. swatchConflict, for a swatch whose name the document gives another colour (clipboard.conflicts): "merge" (default: the objects take the document's swatch) | "add" (the pasted swatch comes in renamed) | {name: "merge"|"add"}. With Paste Remembers Layers on (layer.pasteRemembersLayers), objects go back into the layers they came from (by name; made when missing) → {ids, added: resources added, merged: conflicts merged, renamed: [{kind, from, to}]}
```

## edit.pasteInFront

Paste in Front

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteInFront`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{swatchConflict?} paste in place just above the top selected object, or on top of the current layer when nothing is selected (resources and layers as edit.paste) → {ids, added, merged, renamed}
```

## edit.pasteInBack

Paste in Back

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteInBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{swatchConflict?} paste in place just below the bottom selected object, or at the bottom of the current layer when nothing is selected (resources and layers as edit.paste) → {ids, added, merged, renamed}
```

## edit.pasteInPlace

Paste in Place

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteInPlace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{swatchConflict?} paste where the objects were copied (resources and layers as edit.paste) → {ids, added, merged, renamed}
```

## edit.pasteOnAllArtboards

Paste on All Artboards

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteOnAllArtboards`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{swatchConflict?} paste a copy on every artboard at the offset the objects had to the artboard they were copied from (resources and layers as edit.paste) → {ids, added, merged, renamed}
```

## edit.clear

Clear

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?}
```

## edit.duplicate

Duplicate

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dx?, dy?} duplicate the selection in place (offset optional)
```

## clipboard.exportSvg

Clipboard as SVG

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.exportSvg`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {svg} the copied objects as standalone SVG (null when the clipboard is empty)
```

## clipboard.importSvg

Load SVG into Clipboard

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.importSvg`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{svg | dataBase64 (SVG or SVGZ bytes), center?: [x, y]} replace the clipboard with the SVG's objects (and the images, patterns and symbols they use), centred on `center` (default: the first artboard) → {count}; then run edit.pasteInPlace
```

## clipboard.conflicts

Swatch Conflicts

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.conflicts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {swatches: [{name, document, clipboard, spot}]} the global or spot swatches the copied objects use whose name the active document gives another colour (`document`/`clipboard`: #rrggbb): Paste asks Merge or Add for each (pass the answer as edit.paste* {swatchConflict}). Pasting back into the document the objects came from raises none
```

## clipboard.exportPng

Clipboard as PNG

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.exportPng`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{scale?: 1 (pixels per point, up to 64)} → {dataBase64, width, height (px)} the copied objects cropped to their visual bounds, transparent around them (dataBase64 null when the clipboard is empty)
```

## clipboard.exportPdf

Clipboard as PDF

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.exportPdf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {dataBase64} a one-page PDF of the copied objects, the page their visual bounds (null when the clipboard is empty)
```

## clipboard.exportText

Clipboard as Text

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.exportText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {text} the copied type objects' text, one object per line (null unless every copied object is type, or a group of type)
```

## clipboard.flavours

Clipboard Formats

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.flavours`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {flavours: [mime…]} what Copy offers other apps for the current clipboard, best first, by the Clipboard Handling preferences: text/plain (a type-only copy's text, else the SVG markup with copyAsSvg), image/svg+xml (copyAsSvg), application/pdf (copyAsPdf), image/png (always; PDF and PNG only for objects with an area); the app publishes them on Copy and Cut
```

## clipboard.importImage

Load Image into Clipboard

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.importImage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dataBase64 (PNG, JPEG, GIF, WebP, TIFF or BMP bytes), mime?: the type the system clipboard gave (an image/… type; the format is read from the bytes), center?: [x, y]} replace the clipboard with the image, embedded at 100% of its physical size (its resolution, else 72 ppi), centred on `center` (default: the first artboard) → {count, width, height (pt), pixelWidth, pixelHeight}; then run edit.paste
```

## clipboard.importText

Load Text into Clipboard

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.importText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{text, center?: [x, y]} replace the clipboard with point text of `text` (one paragraph per line; trailing line breaks dropped) in the default type style, centred on `center` (default: the first artboard) → {count}; then run edit.paste
```

## clipboard.importPdf

Load PDF into Clipboard

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipboard.importPdf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dataBase64, page?: 1, password? (an encrypted PDF), center?: [x, y]} replace the clipboard with the objects of one PDF page (with the images, patterns and swatches they use), centred on `center` (default: the first artboard) → {count, warnings}; then run edit.paste
```

## recolor.colors

Artwork Colors

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe recolor.colors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {colors: [{key: colour identity ("rgb 255 0 0", "cmyk 0 100 100 0", "gray 40", "lab 55 60 -40"), hex, count, swatch?: the global swatch it is linked to}]} unique colours used by the selection (fills, strokes, gradient stops, text, mesh points and the tiles of pattern fills and strokes), most used first
```

## recolor.apply

Recolor Artwork

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe recolor.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{map: rows [{from: [colour keys (recolor.colors) or "#rrggbb" (every colour shown as that hex)], to: colour (hex, key, {c,m,y,k} or {l,a,b}) | null, exclude?: false (the row's colours are kept)}] | {"key or #rrggbb": colour, …} (one row per colour), method?: "exact" (default)|"preserveTints"|"scaleTints"|"tintsShades"|"hueShift" (how a row's colours take its new colour, relative to the row's darkest, average or most saturated colour), limitTo?: swatch library id or name, or "document" (the document's swatches): new colours snap to its nearest colour, group?: colour group rewritten with groupColors?: [colour] (default: the rows' new colours, in order, excluded rows left out), rename?: the group's new name, includeImages?: true, includePatterns?: true} recolour the selection (gradients, text, meshes, image pixels and pattern tiles included; each new colour keeps the model of the one it replaces) and the group, as one undo step → {changed}
```

## recolor.reduce

Reduce Colors

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe recolor.reduce`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{colors?: n (rows; default: one per colour, with the tints of a global swatch in its row), method?: as recolor.apply, default scaleTints (picks each row's colour), preserve?: {white?: true, black?: true, grays?: false} (left out of the rows), limitTo?: as recolor.apply (new colours snap to it)} group the selection's colours into rows of similar colours (k-means in Lab, weighted by use) → {map: [{from: [keys, the row's colour first], to: key}], preserved: [keys], method}
```

## recolor.randomize

Randomize Colors

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe recolor.randomize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{map: rows as recolor.apply, order?: true (shuffle the new colours among the rows that aren't excluded), saturationBrightness?: false (random saturation and brightness, hue kept), seed?: 0} → {map: the rows with their new colours as keys}
```

## document.open

Open Document

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.open`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path} or {name, dataBase64}, PDF/.ai: pages?: "2-3, 5" (1-based, default all; one artboard each) | page?: n, cropTo?: bounding|art|crop (default)|trim|bleed|media (the box each artboard gets; bounding: the art's bounds), password? (encrypted PDFs; see document.pdfInfo), textAs?: text (default: point type per line, in the file's fonts by name; missing ones are listed in warnings) | outlines (glyph paths), layers?: true (default: optional content groups become layers with their visibility, print state and lock — art that is off comes in as a hidden layer; other art goes to a layer per page) | false (one layer per page, without the art that is off; Save then asks for a name), colorMode?: rgb|cmyk (the mode the document opens in, its colours converted as file.documentColorMode does; default: the file's — a PDF keeps CMYK, Gray and spot inks (spot swatches at a tint) and opens in CMYK when painted mostly in CMYK) → {index, title, format, warnings, restored, missingLinks, modifiedLinks, updatedLinks: [{name, path, ids}]}; any readable format (see document.formats): .vectorcraft/.drawcraft, .svg/.svgz, .pdf/.ai, .ait, PNG/JPEG/GIF/WebP/TIFF/BMP (an image opens as a document of its pixel size). A PDF/.ai/.ait or SVG saved with Preserve Editing restores the native document it carries (restored: true; a PDF only when no pages are picked), unless the file was changed elsewhere since or the data can't be read: then its artwork is imported and the first warning says why. Templates (native templates, .ait) open as a new untitled document; a restored .ai keeps its path (Save writes .ai again). Linked images are read from their files (looked for at their path, then relative to the document): missing ones show their saved preview (links.relink), modified ones are read again only with Preferences › Update Links: Automatically (else links.update). An SVG's <image> files (relative links from the SVG's folder) stay linked, SVG files become art, missing ones a placeholder in their box (a warning and missingLinks)
```

## document.serialize

Serialize Document

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.serialize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{format?: vectorcraft (default)|template|svg|svgz|pdf|png|jpg|webp|gif|png8|txt|dxf, …the format's options (see document.formats; SVG ones also as svg: {…}), selectedOnly?: false (the selected objects alone, in their layers), artboardContentOnly?: false (SVG/SVGZ: isolate one explicit artboard using native paint bounds; preserve locked content and whole dependency containers)} → {text, warnings} for svg (plus dataBase64, the file, when its encoding isn't UTF-8), else {dataBase64, warnings}; an SVG of several artboards also gives files: [{name, text}], linked images linked: [{name, dataBase64}]
```

## document.export

Export Document

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?: svg|svgz|pdf|png|jpg|webp|gif|png8|txt|dxf|vectorcraft|template (default: from the path's extension, else png; png8 writes an indexed .png), selectedOnly?: false (the selected objects alone, in their layers), artboardContentOnly?: false (SVG/SVGZ: isolate one explicit artboard using native paint bounds; preserve locked content and whole dependency containers), artboard?: 0, artboards?: [i…], range?: "1-3, 5" | "all" (1-based; PDF writes one page per artboard, default all; SVG writes one file per artboard, {stem}-{artboard}.svg; raster formats write one artboard), useArtboards?: true (raster: one file per chosen artboard, default all, {stem}-{artboard}.{ext}; pdf: every page) | false (pdf/raster: the bounds of the visible art; SVG has it as an SVG option), raster: ppi?: 72 (pixels per inch, stored in the file; wins over scale), scale?: 1 (pixels per point), background?: transparent|white|black|"#rrggbb" (jpg: white when transparent), antiAlias?: none|art (default)|type (text snapped to pixels), interlaced?: false (png, Adam7), jpg: quality?: 90 (0–100), colorModel?: rgb|cmyk|gray, method?: baseline|optimized|progressive, scans?: 3 (3–5, progressive), embedIcc?: true, imageMap?: none|client|server (an HTML or NCSA map of the objects with a URL, written as <stem>.html / <stem>.map), gif/png8: colors?: 256 (2–256), reduction?: perceptual|selective (default)|adaptive|web|blackWhite|gray, dither?: none|diffusion (default)|pattern|noise, ditherAmount?: 100, transparency?: true, matte?: white|"#rrggbb"|none, interlaced?, webp: lossless?: true (lossy WebP isn't available yet: written lossless, with a warning), txt: the stories in stacking order (back to front; a thread once), encoding?: utf8|utf16 (with a byte order mark), lineEndings?: lf|crlf, selectionOnly?: false; SVG options flat or as svg: {styling, outlineText, images, objectIds, decimals, minify, responsive, useArtboards, preserveEditing, metadata, fewerTspans, hiddenLayers, encoding, profile, embedFonts} (see document.formats), …the PDF options of document.exportPdf, …the DXF options of document.exportDxf (useArtboards: one drawing per artboard)} → {path, format, bytes, warnings, files?: [path…] (several), linked?: [path…] (linked images, image maps)}; no path → {dataBase64, format, bytes, warnings, files?: [{name, dataBase64}], linked?: [{name, dataBase64}]}. Never changes the document's path
```

## document.exportSelection

Export Selection…

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.exportSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?: png|jpg|webp|svg|svgz|pdf (default: from the extension, else png), scale?: 1, …the format's options} the selected objects cropped to their bounds (template layers left out) → {path, bytes, bounds} (no path → {dataBase64, bounds})
```

## document.exportForScreens

Export for Screens

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.exportForScreens`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folder?, zip?: false (one store-only .zip of every file: no folder → {name, dataBase64, bytes, files: [name…]}; with a folder it is written there → {path, bytes, files}), artboards?: [index…] | range?: "1-3" (default all), fullDocument?: false (one file per format instead: a PDF of every artboard, other formats the bounds of all visible art, named after the document), includeBleed?: false (artboards grown by the document's bleed), subfolders?: false (each row's files in a sub-folder: its folder, else its size for raster (1x, 2x, 100w…) or its format (SVG, PDF)), preset?: mobile (PNG 1x, 2x, 3x) | density (PNG 0.75x–4x in ldpi…xxxhdpi sub-folders) instead of formats (turns subfolders on), formats?: [{format: png|png8|jpg|webp|gif|svg|svgz|pdf, scale?: 1 | "2x" | "100w" | "100h" | "72ppi", width?: px | height?: px | ppi? (raster only; width, then height, then ppi win over scale), suffix?: (raster default: @2x, @100w, @100h, none at 1x; vector formats drop size suffixes), folder?: (its sub-folder), quality?: (jpg 0–100), …the format's options (antiAlias, background, preset (pdf)…)}], settings?: {png|png8|jpg|webp|gif|svg|pdf: {…options for every row of that format}} (rows' own options win), prefix?, antiAlias?: none|art|type (raster rows without their own), openLocation?: (remembered; the app shows the files after exporting)} one file per artboard and format (a PDF holds its artboard alone; artboards with the same name, in any case, get -2, -3…; an unnamed one is Artboard-N) → {files: [path…]}; no folder → {files: [{name, dataBase64}]} (names include sub-folders: 2x/Icon@2x.png). The params are remembered in the document (document.exportSettings; not an undo step)
```

## command.batch

Batch

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe command.batch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{label?, commands: [{command, params}]} run several commands as ONE undo step; stops at the first error and rolls back
```

## document.formats

File Formats

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.formats`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {formats: [{id, label, extensions, mime, read, write, raster, options: {name: {type, default, description}}}], readable: [id…], writable: [id…], openExtensions: [ext…], unsupported: [{id, label, extensions, hint}] (formats asked for that can be neither opened nor written, such as DWG and PICT, with what to use instead)}
```

## document.pdfInfo

PDF Info

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.pdfInfo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path} or {name?, dataBase64}, password?, thumbnail?: page (1-based), thumbnailSize?: 160 (px, longest side), cropTo?: crop (the thumbnail's box) → {pages, needsPassword, wrongPassword?, pageInfo: [{width, height (pt, as shown), rotation, boxes: {media, crop, bleed, trim, art: [x0, y0, x1, y1] (PDF space, pt)}}], thumbnail?: PNG dataBase64}; an encrypted PDF without its password → {pages: 0, needsPassword: true}
```

## document.exportForOffice

Save for Office Documents…

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.exportForOffice`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, ppi?: 150 (72, 150, 300… pixels per inch), transparent?: false (else on white), artboard?: 0} the artboard as a PNG for office documents and slides → {path, bytes, width, height} (pixels); no path → {dataBase64, bytes, width, height}
```

## document.exportSettings

Export for Screens Settings

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.exportSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {settings}: the document.exportForScreens params the document last exported with ({} when never; saved with the document, the dialog reopens on them)
```

## document.save

Save Document

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?: vectorcraft|template|pdf|svg|svgz|ai (default: the path's extension, else the document's own format), options?: {…the format's options, see file.formatOptions; default: as last saved}, svg?: {…SVG options} (SVG options may also be given flat; an SVG save keeps hidden layers, display:none, unless hiddenLayers is false), native (also flat): compress?: bool (gzip; default: the useCompression preference), version?: 3 (2 or 1: for older VectorCraft versions, never compressed), preview?: false (embed a PNG of the first artboard, at most 256 px), modified?: Unix seconds|null (the File Info modified date, and created date when there is none, a save to a file stamps; default now, recorded in the journal so a replay matches; null: leave the dates)} → {path, format, bytes, warnings, linked?: [path…] (images an SVG links to)}. Save writes one artboard, except a .ai file: a PDF-compatible file of every artboard carrying the native document (preserveEditing always on; PDF options flat or in options), which document.open restores exactly. Without a path it writes the document's own file in its own format: a document opened from or saved as SVG/PDF saves as that again (warnings name what the format loses). No path known (never saved, converted from an older version, or another format) → {dataBase64, format, name, folder?, warnings} and the document stays modified
```

## file.saveAs

Save As…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveAs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?: vectorcraft|template|pdf|svg|svgz|ai (default: the path's extension, else the document's own), options?, svg?, modified? (as document.save)} the document takes on the new path, name and format (except a template, which is always a copy) → {path, format, bytes, warnings}; no path → {dataBase64, format, name, folder?, warnings}
```

## file.saveCopy

Save a Copy…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveCopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?, options?} (as file.saveAs) write a copy; the document keeps its path, title and modified state → {path, format, bytes, warnings}; no path → {dataBase64, format, name: "<name> copy.<ext>", folder?, warnings}
```

## file.saveAsTemplate

Save as Template…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveAsTemplate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, compress?, version?, preview? (as document.save)} a native template (.vctemplate) that opens as a new untitled document; the document is unchanged → {path, format, bytes, warnings}; no path → {dataBase64, format, name: "<name> template.vctemplate", folder: the Templates folder (preference templatesFolder), warnings}
```

## file.newFromTemplate

New from Template…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newFromTemplate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path} or {name, dataBase64}: open a template (or any readable file) as a new untitled document → {index, title, format, warnings}
```

## file.revert

Revert

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.revert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} discard the changes: reload the saved file into the same tab (history cleared; the tab keeps its place and view). Saved, modified documents only; if the file can't be read the document is left as it is → {path}. The app asks first (a confirm dialog) unless confirmed: true
```

## file.formatOptions

Format Options

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.formatOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{format?: a writable format id (default: the document's own)} → {id, label, extensions, mime, read, write, raster, options: {name: {type, default, description, value}}, saveFormats: [{id, label, extensions}]}; value = the document's option as last saved in that format, else the default
```

## shape.rectangle

Rectangle

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.rectangle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x, y, width, height, radius?: pt} → {id}
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## shape.ellipse

Ellipse

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.ellipse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x, y, width, height} → {id}
```

## shape.polygon

Polygon

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.polygon`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{cx, cy, radius, sides=6, rotation?: deg} → {id}
```

## shape.star

Star

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.star`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{cx, cy, radius1, radius2, points=5, rotation?: deg} → {id}
```

## shape.flare

Flare

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.flare`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{cx, cy, diameter=100, opacity=50 (%), brightness=30 (%), growth=20 (%), fuzziness=50 (%), rays=15, longest=300 (%), rayFuzziness=100 (%), x2?, y2? (ring end; else pathLength at direction), pathLength=300, rings=10, largest=50 (%), direction=45 (deg), seed?} → {id}
```

## shape.line

Line Segment

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.line`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x1, y1, x2, y2} → {id}
```

## shape.spiral

Spiral

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.spiral`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{cx, cy, radius, decay=80 (%), segments=10, clockwise?} → {id}
```

## shape.arc

Arc

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.arc`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x1, y1, x2, y2, closed?} → {id}
```

## shape.rectangularGrid

Rectangular Grid

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.rectangularGrid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x, y, width, height, rows=5, columns=5} → {id}
```

## shape.polarGrid

Polar Grid

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.polarGrid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x, y, width, height, concentric=5, radial=5} → {id}
```

## path.create

Create Path

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{anchors: [{x, y, in?: [x,y], out?: [x,y]}], closed?: bool, d?: SVG path data} → {id}
```

## view.drawMode

Drawing Mode

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.drawMode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{mode?: normal|behind|inside} (no param cycles; inside needs one selected path)
```

## text.create

Create Text

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x, y, text, size?: pt, font?: family, style?, color?, area?: {width, height}} → {id}
```

## object.transform

Transform

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.transform`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{matrix: [a,b,c,d,e,f], copy?: bool, ids?, strokes?: bool, corners?: bool} apply an affine to the selection (or ids); strokes/corners: Scale Strokes & Effects / Scale Corners (default: the preferences)
```

## object.move

Move…

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dx, dy, copy?}
```

## object.rotate

Rotate…

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.rotate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{angle: deg (counter-clockwise), origin?: [x,y], copy?}
```

## object.scale

Scale…

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.scale`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{sx: %, sy?: %, origin?: [x,y], copy?, strokes?: bool (Scale Strokes & Effects: stroke weights, dashes and effect distances scale; off keeps them, type strokes included), corners?: bool (Scale Corners: live corner radii scale)} (strokes/corners default to the preferences)
```

## object.reflect

Reflect…

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.reflect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{axis: "vertical"|"horizontal"|deg, origin?, copy?}
```

## object.shear

Shear…

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.shear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{angle: deg, axis?: "horizontal"|"vertical", origin?, copy?}
```

## object.transformAgain

Transform Again

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.transformAgain`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.nudge

Nudge

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.nudge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dx: -1|0|1, dy: -1|0|1, big?: bool (×10), copy?: bool} arrow-key nudge by the keyboard increment
```

## object.arrange.bringToFront

Bring to Front

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.arrange.bringToFront`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.arrange.bringForward

Bring Forward

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.arrange.bringForward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.arrange.sendBackward

Send Backward

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.arrange.sendBackward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.arrange.sendToBack

Send to Back

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.arrange.sendToBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.arrange.sendToCurrentLayer

Send to Current Layer

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.arrange.sendToCurrentLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.group

Group

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.group`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {id}
```

## object.ungroup

Ungroup

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.ungroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.lock

Selection

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.lock`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.unlockAll

Unlock All

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.unlockAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.hide

Selection

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.hide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.showAll

Show All

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.showAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.compoundPath.make

Make

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.compoundPath.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.compoundPath.release

Release

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.compoundPath.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.clippingMask.make

Make

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.clippingMask.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} the topmost selected object (a path, compound path or text, which loses its paint) clips the others: compound holes, even-odd fills and glyph outlines clip as drawn. Paint given to the clipping path later (paint commands with its id) shows: its fill behind the clipped art, its stroke over it → {id} of the clip group
```

## object.clippingMask.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.clippingMask.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} the selected clip groups become plain groups; their clipping path (path, compound path or text) stays, with the paint it has (none unless painted after Make)
```

## object.clippingMask.editContents

Edit Contents

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.clippingMask.editContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} select the clipped art of the selected clip groups → {count}
```

## object.clippingMask.editMask

Edit Clipping Path

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.clippingMask.editMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} select the clipping paths of the selected clip groups → {count}
```

## object.isolate

Enter Isolation Mode

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.isolate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## object.exitIsolation

Exit Isolation Mode

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.exitIsolation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## object.setProps

Object Properties

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.setProps`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?|id?, name?, visible?, locked?, opacity?: 0..100, blend?: "Multiply"…, isolate?, knockout?: "on"|"off"|"neutral"|bool (true = on, false = neutral), knockoutShape?: bool}
```

## object.align

Align

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.align`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{horizontal?: "left"|"center"|"right", vertical?: "top"|"center"|"bottom", to?: "selection"|"artboard"|"key", bounds?: "preview"|"geometric" (default: the Use Preview Bounds preference; preview bounds take in strokes)}
```

## object.distribute

Distribute

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.distribute`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{horizontal?: "left"|"center"|"right", vertical?: "top"|"center"|"bottom", bounds?: "preview"|"geometric" (default: the Use Preview Bounds preference; preview bounds take in strokes)}
```

## object.distributeSpacing

Distribute Spacing

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.distributeSpacing`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{axis: "horizontal"|"vertical", spacing?: pt, bounds?: "preview"|"geometric" (default: the Use Preview Bounds preference; preview bounds take in strokes)}
```

## object.setBounds

Set Bounds

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.setBounds`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x?, y?, width?, height?, reference?: 0..8 (9-point grid), proportional?, strokes?, corners?} (Transform panel; with Use Preview Bounds the values measure the visual bounds; strokes/corners as object.scale)
```

## object.expandShape

Expand Shape

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.expandShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} convert live shapes to plain paths
```

## object.setLiveShape

Live Shape Properties

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.setLiveShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?, radius?: pt (all corners), sides?: n}
```

## path.appendAnchor

Add Anchor (Pen)

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.appendAnchor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, x, y, in?: [x,y], out?: [x,y]} append to the end of the last open subpath
```

## path.close

Close Path

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.close`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, in?: [x,y] (handle into the first anchor), independent?: bool}
```

## path.moveAnchors

Move Anchors

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.moveAnchors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dx, dy} move direct-selected anchors (whole paths if fully selected)
```

## path.setHandle

Move Direction Handle

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.setHandle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpath, anchor, which: "in"|"out", x, y, independent?: bool}
```

## path.setAnchors

Set Anchors

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.setAnchors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpaths: [{anchors: [{x,y,in?,out?}], closed}]} replace a path's geometry
```

## path.reverse

Reverse Path Direction

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.reverse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, reversed?: bool (true: every subpath runs counter-clockwise on screen, false: clockwise, the Attributes panel's Reverse Path Direction On / Off; omitted: flip each path)} the paths in ids or the selection (groups and compound paths: the paths inside), as one undo step → {changed: paths}
```

## path.join

Join

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.join`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} join two open paths' nearest endpoints, or close a single open path
```

## path.average

Average…

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.average`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{axis?: "horizontal"|"vertical"|"both"}
```

## path.convertAnchors

Convert Anchor Points

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.convertAnchors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{to: "corner"|"smooth"} (Control bar convert buttons)
```

## path.deleteAnchors

Remove Anchor Points

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.deleteAnchors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} delete direct-selected anchors
```

## path.reshape

Reshape

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.reshape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, x, y, dx, dy, tol=3, radius?} Reshape tool: grab the path at (x, y) (adding an anchor there unless one is within tol) and drag it by (dx, dy); nearby anchors follow with a smooth falloff over radius (default: half the subpath's size)
```

## path.insertAnchor

Add Anchor Point

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.insertAnchor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpath, segment, t: 0..1}
```

## path.cutAtAnchors

Cut Path at Selected Anchor Points

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.cutAtAnchors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.all

All

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.all`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.allOnArtboard

All on Active Artboard

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.allOnArtboard`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{artboard?: index}
```

## select.none

Deselect

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.none`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.reselect

Reselect

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.reselect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.inverse

Inverse

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.inverse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.nextAbove

Next Object Above

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.nextAbove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.nextBelow

Next Object Below

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.nextBelow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.set

Select Objects

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids: [id…]}
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json) · [appearance-gradient-revise.json](../examples/appearance-gradient-revise.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## select.add

Add to Selection

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids: [id…]}
```

## select.toggle

Toggle Selection

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.toggle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## select.key

Set Key Object

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.key`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} (none clears)
```

## select.anchors

Select Anchors

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.anchors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, anchors: [[subpath, anchor]…], mode: "set"|"add"|"toggle"}
```

## select.anchorsMany

Select Anchors

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.anchorsMany`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{items: [{id, anchors}], add?: bool}
```

## select.same.fillColor

Fill Color

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.fillColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.strokeColor

Stroke Color

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.strokeColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.strokeWeight

Stroke Weight

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.strokeWeight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.fillAndStroke

Fill & Stroke

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.fillAndStroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.opacity

Opacity

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.opacity`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.blendingMode

Blending Mode

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.blendingMode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.appearance

Appearance

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.appearance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.shapeType

Shape

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.shapeType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.object.allOnSameLayers

All on Same Layers

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.allOnSameLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.object.clippingMasks

Clipping Masks

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.clippingMasks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.object.textObjects

All Text Objects

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.textObjects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.object.strayPoints

Stray Points

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.strayPoints`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.object.openPaths

Open Paths

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.openPaths`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.same.graphicStyle

Graphic Style

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.graphicStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} the objects linked to the graphic style the first selected object is linked to
```

## select.same.appearanceAttribute

Appearance Attribute

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.appearanceAttribute`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{item?: appearance item index} the objects sharing an appearance attribute of the first selected object: its fill or stroke `item` (default: the Appearance panel's active item), else its first effect, else its topmost fill
```

## select.magicWand

Magic Wand

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.magicWand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, mode?: set|add|subtract} select objects similar to `id` by the Magic Wand settings → {count}
```

## magicWand.set

Magic Wand Options

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe magicWand.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fillColor?, fillTolerance?: 0-255, strokeColor?, strokeTolerance?: 0-255, strokeWeight?, weightTolerance?: pt, opacity?, opacityTolerance?: %, blendingMode?, reset?: bool} → the settings
```

## magicWand.options

Magic Wand Settings

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe magicWand.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → the Magic Wand settings
```

## paint.setFill

Fill

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.setFill`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{color?: "#rrggbb"|[r,g,b]|{c,m,y,k}|{gray}|{l,a,b} (CIE Lab), none?: true, swatch?: name (a global or spot colour stays linked, so swatch edits recolour it; a tint swatch links to its base at its tint; a gradient swatch is recorded as the gradient's swatch and fits each object, keeping its aspect; the built-in "[Registration]" prints on every plate), tint?: 0..100 (% of a global or spot `swatch`; default 100, or a tint swatch's own), gradient?: {kind?: linear|radial|freeform, stops?: [{offset 0..1, color, opacity? 0..1 (or 0..100), midpoint? 0.13..0.87, swatch?: global or spot colour (or tint) swatch the stop links to (its colour comes from the swatch), tint?: 0..100}] (at least 2; default white→black), angle?: deg, start?: [x,y], end?: [x,y] (the vector in document coordinates, both or neither; type objects keep it in text space), aspect?: % (radial; without start/end the gradient is placed on each object's bounds), focal?: [x,y] (radial, with start/end: the focal point, where the first stop sits), swatch?: linked gradient swatch name}, item?: appearance item index|null (omitted: the Appearance panel's active item if it is a fill, else the top fill), ids?, focus?: true (false keeps the active proxy), keepModel?: false (in a CMYK document, RGB colours and gradient stops are stored as CMYK unless true; Gray stays Gray)} sets the selection's fill and the default (new art fits a gradient to itself)
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## paint.setStroke

Stroke

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.setStroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
same as paint.setFill, for the stroke (item?: the stroke item to set)
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## paint.swap

Swap Fill and Stroke

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.swap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} swap the fill and stroke of the selection (type too) and of the defaults
```

## paint.default

Default Fill and Stroke

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.default`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} white fill and 1 pt black stroke for the selection and the defaults; type gets black fill and no stroke
```

## paint.toggleActive

Toggle Fill/Stroke Focus

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.toggleActive`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fill?: bool (true: bring the Fill proxy forward, false: the Stroke proxy; omitted: swap which is in front)} → {fillActive}
```

## paint.none

None

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.none`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} set the active proxy (fill or stroke) to None
```

## transparency.set

Transparency

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?|id?, opacity?: 0..100, blend?: name, isolate?, knockout?: "on"|"off"|"neutral"|bool (true = on, false = neutral), knockoutShape?: bool, item?: appearance item index|null} for `ids`, the selection, or the object whose opacity mask is being edited; opacity and blend go to the targeted fill/stroke item (omitted: the Appearance panel's active item, else the objects)
```

## stroke.set

Stroke Options

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{weight?: pt, cap?: butt|round|square, join?: miter|round|bevel, miterLimit?, align?: center|inside|outside, dash?: [d,g,…]|null (a 0 dash with a round or projecting cap draws dots or squares; a new pattern keeps the current offset and alignment), dashOffset? (exact dashes only), alignDashes?: bool (true: dashes fitted to corners and path ends, every run between them holding whole periods with a dash centred on each corner and end; false, the default for a new pattern: exact lengths), startArrow?, endArrow?: Arrow|ArrowOpen|Barbed|Concave|DoubleArrow|HalfArrowLeft|HalfArrowRight|Chevron|Feather|Swallowtail|Triangle|TriangleOpen|TriangleReverse|TriangleBar|Kite|Leaf|Drop|Circle|CircleOpen|HalfCircle|Oval|Target|Square|SquareOpen|Tag|TagOpen|Diamond|DiamondOpen|Hexagon|HexagonOpen|Star|Cross|Plus|Bar|DoubleBar|DotOnBar|Slash|DoubleSlash|Bracket|Fork|null (HalfArrowLeft/Right: one barb, left or right of the direction the head points), arrowAlign?: "extend" (tip past the end point, default)|"tip" (tip on the end point; the stroke is shortened), profile?: "uniform"|"lens"|"taperStart"|"taperEnd"|"pinch"|"teardrop"|"wave"|a saved profile's name (stroke.widthProfile.list), item?: stroke item index|null (omitted: the Appearance panel's active item if it is a stroke, else the top stroke, created when missing), ids?} Without a stroke item, type takes weight, cap, join, miterLimit and the dash options as its characters' stroke (every run; text.setRangeStyle `strokeOptions` styles a range), and images and symbol instances (also in groups) are left alone. With nothing selected (and no ids) they set up the next object drawn (appearance.newArt; weight always does)
```

## stroke.setAdvanced

Stroke Options

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.setAdvanced`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{arrowScale?: [start %, end %], swapArrows?: bool, flipProfile?: "along"|"across", brush?: name|null, item?: stroke item index|null, ids?} Stroke panel extras (with nothing selected, all but brush set up the next object drawn)
```

## stroke.widthProfile.add

Add to Profiles

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthProfile.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?} save the selected stroke's variable width to the Profile list (kept with the preferences) under `name` (default "Width Profile N"; unique, not a built-in's) → {name}
```

## stroke.widthProfile.delete

Delete Profile

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthProfile.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?} remove a saved profile from the Profile list (default: the selected stroke's); built-in profiles can't be deleted, and strokes keep their widths → {deleted}
```

## stroke.widthProfile.reset

Reset Profiles

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthProfile.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} remove every saved profile, leaving the built-ins → {removed: count}
```

## stroke.widthProfile.list

Width Profiles

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthProfile.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {profiles: [{id (stroke.set `profile`), label, builtIn, points: [[t, left, right]…]}], current: the selected stroke's profile id or name (nothing selected: the next object drawn's), "custom" when it isn't listed, null without a stroke}
```

## appearance.addFill

Add New Fill

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.addFill`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, target?: "object"|"contents"} add a fill on top of each selected object's own stack (a copy of its top fill; type without one: its characters' fill; else the default fill)
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## appearance.addStroke

Add New Stroke

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.addStroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, target?} add a stroke on top of each selected object's own stack (a copy of its top stroke, else the default stroke)
```

## appearance.clear

Clear Appearance

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, target?} leave each object one empty fill and stroke (None; a group none of its own) and reset its opacity and blend mode
```

## appearance.reduceToBasic

Reduce to Basic Appearance

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.reduceToBasic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, target?} keep only the topmost visible fill and stroke, without their own opacity, blend mode or effects (a group keeps no rows it lacked), and drop the object's effects
```

## appearance.setItem

Appearance Item

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.setItem`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: paint-order item index, ids? (default: the selection), target?: "object"|"contents", opacity?: 0..100, blend?: name, visible?: bool, weight?: pt (strokes), color?|none?|swatch?|gradient? (as paint.setFill)} edit one fill/stroke of each target object's own appearance stack
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## appearance.removeItem

Remove Item

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.removeItem`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index | indices: [..] (paint-order item indices), ids?, target?} remove those fills/strokes from each target object's own stack
```

## appearance.addEffect

Add Effect

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.addEffect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
same as effect.apply (an alias): {effect: id, params?: {…}, item?: appearance item index|null, ids?, target?} → {ids, index, item}
```

## appearance.duplicateItem

Duplicate Item

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.duplicateItem`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index | indices: [..] (paint-order item indices), to?: paint-order index of the copy (one `index` only; default: right above it, as Alt-dragging a row places it), ids?, target?} copy fills/strokes with their effects
```

## appearance.moveItem

Reorder Appearance Item

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.moveItem`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{from: paint-order item index | "contents", to, contents?: count, ids?, target?} move fill/stroke `from` to paint-order index `to`; on a group, layer or type the Contents (Characters) row stays between the same items (a moved item landing next to it keeps its side) unless `contents` says how many items paint below it afterwards. from "contents": move that row so `to` items paint below the members (characters) and the rest above → {index: where the item landed | contents: the row's slot}
```

## appearance.copyFrom

Eyedropper

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.copyFrom`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{source: id, ids?, pickUp?, apply? (trees as eyedropper.setOptions, merged over the Eyedropper Options for this call), reverse?: bool, append?: bool} copy the attributes both picked up and applied (by default the whole appearance stack, opacity and blend mode, and from type to type the character and paragraph attributes) from `source` to ids (default: the selection), the fill, stroke and weight also to the paint defaults; `reverse` (Alt-click) copies from the first selected object (or ids) onto `source` instead; `append` (Shift+Alt-click) adds the source's fills, strokes and effects on top of each target's stack; placed gradients land at the same place relative to each target's bounds (defaults: fitted to new art) → {ids}
```

## appearance.setActiveItem

Select Appearance Item

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.setActiveItem`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: paint-order item index in the first selected object's stack | null} make that fill/stroke row the target of the paint.setFill/setStroke, stroke.set/setAdvanced, paint.editGradient/setGradientGeom, transparency.set and effect.* calls that omit `item` (a fill row brings the Fill proxy forward, a stroke row the Stroke proxy); null or any selection change clears it → {index}
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json) · [appearance-gradient-revise.json](../examples/appearance-gradient-revise.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## appearance.showAllHidden

Show All Hidden Attributes

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.showAllHidden`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, target?} make every hidden fill, stroke and effect (the object's and each item's) of each selected object visible again; errors when nothing is hidden → {ids}
```

## appearance.targetContents

Target Contents

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.targetContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} select the members of the selected groups and layers (or `ids`), as double-clicking the Appearance panel's Contents row does: the panel then lists, and appearance edits change, their own appearance; errors when none has members → {ids}
```

## appearance.transfer

Move Appearance

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.transfer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{source: id, target: id, copy?: bool} give `target` (a layer, group or object) the appearance (fills, strokes, effects) and transparency (opacity, blend mode, isolation, knockout) of `source`, as dragging a target circle onto another in the Layers panel does; the source is left with a cleared appearance (as appearance.clear) unless `copy` (Alt-drag). Opacity masks stay; placed gradients keep their place relative to each object's bounds → {source, target}
```

## graphicStyle.apply

Apply Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, add?: bool, ids? (layers too), target?: "object"|"contents"} give the objects (default: the selection; a group or layer itself, its fills and strokes painting its members and its effects applying to them as one piece; target contents: the objects inside instead) the style's appearance, opacity, blend mode, isolate and knockout, and link them to it (placed gradients land at the same place relative to each object's bounds); add: true (Alt-click) adds its fills, strokes and effects on top of the existing appearance instead and unlinks. With nothing selected (and no ids) the next object drawn takes the style instead (see appearance.newArt) → {newArt: true}
```

## graphicStyle.new

New Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, id?} a style from object `id` or the first selected object: its appearance, opacity, blend mode, isolate and knockout (a group without fills or strokes of its own lends its topmost object's, type its characters'; placed gradients are kept relative to its bounds); links the object. Names are made unique → {name}
```

## graphicStyle.delete

Delete Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} | {names: [name…]} delete styles; their objects keep their look but are unlinked
```

## graphicStyle.duplicate

Duplicate Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} → {name}
```

## graphicStyle.list

List Graphic Styles

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {styles: [{id, name, fill, stroke, strokeWidth, fills, strokes, effects: [effect id…], opacity: 0..100, blend, isolate, knockout: "on"|"off"|"neutral", linked: [object ids]}], selected: the style the first selected object is linked to, or null, overrideCharColor}
```

## graphicStyle.redefine

Redefine Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.redefine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, id?} replace the style (default: the one the object was last linked to) with the look of object `id` or the first selected object; the objects still linked to it update, and that object becomes linked → {name}
```

## graphicStyle.breakLink

Break Link to Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.breakLink`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} unlink the objects (default: the selection) from their graphic style; they keep their look
```

## graphicStyle.rename

Rename Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, to} (Graphic Style Options; names are unique and linked objects stay linked) → {name}
```

## graphicStyle.unused

Select All Unused

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.unused`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {names: [the styles no object is linked to]} (the panel selects them)
```

## graphicStyle.sortByName

Sort by Name

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.sortByName`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} sort the styles by name (the Default Graphic Style stays first)
```

## graphicStyle.merge

Merge Graphic Styles

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{names: [name…] (two or more), name?} add a style combining the styles' fills, strokes and effects (each style's on top of the ones before it) with the first one's opacity, blend mode, isolate and knockout → {name}
```

## graphicStyle.move

Move Graphic Style

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, to: index} move the style to position `to` of the list (0 = first, clamped), as dragging it in the Graphic Styles panel does
```

## graphicStyle.setOptions

Graphic Styles Options

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.setOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{overrideCharColor?: bool} Override Character Color (the preference `overrideCharColor`, on by default): applying a style to type replaces its characters' fill and stroke with the style's fills and strokes → {overrideCharColor}
```

## swatch.new

New Swatch

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, color? | colors?: [colour] (one swatch each, in one undo step) | swatch? | gradient? | pattern?: name (default: the current fill), tint?: 0..100 (% of the global or spot `swatch`, or of the one the current fill links to), mode?: "gray"|"rgb"|"hsb"|"lab"|"cmyk"|"web" (convert the colour; lab: CIE L*a*b*, how spot colours are usually defined), global?, spot? (a spot colour, always global), group?: colour group name (solid colours only; default: ungrouped)} save a colour, gradient or pattern as a swatch. A tint of a global or spot colour (below 100%, without mode, global or spot) becomes a tint swatch, "Name 40%", linked to its base: it follows edits to the base and applies as that tint of it. Names are unique ("Sky 2"); a colour's default name is its values ("C=10 M=20 Y=30 K=0", "R=255 G=128 B=0", "Gray K=40", "L=55 a=60 b=40") → {name, names: [every new swatch]}
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## swatch.delete

Delete Swatch

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name? | names?: [swatch or colour group names] (a group goes with its swatches), unlink?: true (art using a deleted global swatch keeps its colour, unlinked; false keeps the stale link)} delete in one undo step → {deleted, unlinked: paints unlinked}
```

## swatch.newGroup

New Color Group

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.newGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, swatches?: [names] (solid colours move into the group; gradients, patterns and None stay), colors?: [colour] (added as new swatches), fromArtwork?: false (add the unique colours of the selected art: fills, strokes, text, gradient stops and mesh points; a colour linked to a global swatch moves that swatch into the group), toGlobal?: true (with fromArtwork: the new swatches are global and the selected art's matching unlinked colours link to them), includeTints?: false (with fromArtwork: tints of global swatches also get swatches of their own)} → {name, swatches: [names in the group], linked: paints linked}
```

## swatch.duplicate

Duplicate Swatch

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name}
```

## swatch.sortByName

Sort by Name

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.sortByName`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## swatch.edit

Swatch Options

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, newName?, color? (e.g. {l, a, b} for a Lab colour), mode?: "gray"|"rgb"|"hsb"|"lab"|"cmyk"|"web" (convert the colour), global?, spot? (spot colours are always global), paint?: paint.setFill params ({color}, {gradient}, {swatch} or {pattern}) replacing the swatch's colour, gradient or pattern with one of the same kind} edit a swatch in any colour group, as one undo step. Fills, strokes, text, gradient stops and tint swatches linked to a global swatch take its new colour (at their own tint) and name; turning Global off unlinks them (they keep their colour). Colour, mode and spot apply to solid colours only; a tint swatch only takes a new name (edit its base) → {name, relinked: paints changed}
```

- 可执行场景 / Executable recipes: [appearance-gradient-revise.json](../examples/appearance-gradient-revise.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## swatch.list

Swatches

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{group?: name (only that colour group's swatches)} → {swatches: [{name, kind: "none"|"color"|"gradient"|"pattern", group, global, spot, color?, hex?, tintOf?: base swatch of a tint swatch, tint?: its %, gradient?, pattern?}] (the built-in [Registration] after None: it prints on every plate and can't be edited, moved or deleted), groups: [{name, swatches: [names]}]}
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json) · [appearance-gradient-revise.json](../examples/appearance-gradient-revise.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## swatch.move

Move Swatch

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name? | names?: [swatch names, in order; or colour group names to reorder the groups], to?: index in the destination (they go before the swatch or group now there; default: the end), group?: destination colour group (default: the ungrouped swatches; groups hold solid colours only)} reorder swatches or move them into or out of colour groups, as one undo step → {moved}
```

## swatch.addUsedColors

Add Used Colors

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.addUsedColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{selection?: false (only the selected art's colours; default: all the art's), global?: false (the new swatches are global and the matching unlinked colours in that art link to them)} add a swatch for each colour used (fills, strokes, text, gradient stops, mesh points) that no solid swatch has yet, as one undo step → {added: [names], linked}
```

## swatch.unused

Select All Unused

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.unused`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {names: [the swatches nothing uses, in panel order]}: a colour is used when a paint links to it or an unlinked paint, gradient stop or mesh point has its colour; a gradient when a gradient links to it or has its stops; a pattern when it fills or strokes anything (art, symbols, pattern tiles and graphic styles count). None is never listed
```

## swatch.merge

Merge Swatches

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{names: [two or more solid-colour swatches]} keep the first (its name and colour) and delete the others; paints linked to them take its colour and link to it (or unlink when it isn't global), as one undo step → {name, merged: [deleted names], relinked}
```

## swatch.ungroup

Ungroup Color Group

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.ungroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name: colour group} move its swatches to the end of the ungrouped swatches and remove the group, as one undo step → {swatches: [names]}
```

## swatch.sortByKind

Sort by Kind

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.sortByKind`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} order the swatches of each list by kind (None first, then process colours, spot colours, gradients, patterns; colour groups stay after them), keeping their order within a kind, as one undo step
```

## swatch.spotOptions

Spot Colors

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.spotOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{useLab?: bool (omitted: unchanged)} the document's Spot Colors options: spot colours defined in Lab show, print and export from their Lab values (true, the default: PDF Separation spaces get a Lab alternate) or from their working-CMYK equivalents (false: a DeviceCMYK alternate, matching older files). Art, gradient stops and tint swatches linked to Lab spot swatches take the chosen colour at their tint, as one undo step → {useLab, relinked: paints changed}
```

## swatch.editGroup

Edit Color Group

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.editGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{group: colour group, colors: [colour] (hex, key, {c,m,y,k} or {l,a,b}; the group's swatches take them in order, extra colours become new swatches, swatches past the end are removed; built-in swatches can't change), rename?: new group name} rewrite a colour group as one undo step; art linked to its global swatches takes their new colours (and keeps its colour, unlinked, when its swatch goes) → {name, swatches: [names], relinked}
```

## paint.editGradient

Gradient

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.editGradient`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stroke?: bool (default: the targeted item's kind, else the active proxy), kind?: linear|radial|freeform (freeform places points on each object, coloured along the stops), mode?: points|lines (freeform: how the Gradient tool adds points), stops?: [{offset 0..1, color? (needed without swatch), opacity? 0..1 (or 0..100), midpoint? 0.13..0.87, swatch?: colour swatch name (a global or spot colour or tint swatch links the stop, so swatch edits recolour it and a spot stop prints on its plate; a process colour just gives its colour), tint?: 0..100 (% of the linked swatch; default 100, or a tint swatch's own)}] (at least 2; a freeform gradient's points are recoloured along them), angle?: deg, aspect?: %, reverse?: bool, item?: fill/stroke item index|null (omitted: the Appearance panel's active item when it is of the edited kind), ids?, strokeMode?: within|along|across (strokes only: the gradient lies on the page and shows through the stroke, runs from the start of each subpath to its end, or runs from the stroke's left edge to its right all along it; with nothing selected, for the next object drawn; type characters' own strokes always paint within)} edit the gradient in place (keeps its placement); solid/none paints become the default gradient
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## paint.setGradientGeom

Gradient Vector

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.setGradientGeom`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{start?: [x,y], end?: [x,y] (document coordinates; both or neither: omitted, the vector stays), aspect?: % (radial: the extent ellipse's height / width; default: kept), focal?: [x,y] (document coordinates) | null (radial: the focal point, where the first stop sits, pulled inside the extent ellipse; null centres it; default: it keeps its place in the ellipse), ids?, stroke?: bool (default: the targeted item's kind, else the active proxy), item?: fill/stroke item index|null (alias: index; omitted: the Appearance panel's active item when it is of the edited kind)} set the gradient vector, aspect ratio and focal point (solid paints become the default gradient; type objects set it on their runs, in text space)
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## gradient.selectStop

Select Gradient Stop

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.selectStop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: stop index (0 = the start) | null to clear} select a stop of the gradient behind the active proxy (the first selected object's, else the default paint): the stop the Gradient tool's annotator, the Gradient and Color panels and Delete/arrow keys act on → {index}
```

- 可执行场景 / Executable recipes: [appearance-gradient-create.json](../examples/appearance-gradient-create.json) · [appearance-gradient-revise.json](../examples/appearance-gradient-revise.json)；前置条件与范围见 [外观指南](appearance-gradient.md)。样例通过不等于完整逐命令验收。

## transparency.makeOpacityMask

Make Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.makeOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, clip?, invert?} the topmost of the selected objects (or of `ids`) becomes the mask of the others (grouped if several). One object gets an empty mask and enters mask editing: draw the mask, then transparency.stopEditingOpacityMask → {id, editing}
```

## transparency.releaseOpacityMask

Release Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.releaseOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?} put the mask art back above each masked object (default: the selection, or the object whose mask is being edited, which leaves mask editing)
```

## transparency.disableOpacityMask

Disable Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.disableOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?} keep the mask but stop applying it
```

## transparency.enableOpacityMask

Enable Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.enableOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?}
```

## transparency.unlinkOpacityMask

Unlink Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.unlinkOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?} the object moves without its mask
```

## transparency.linkOpacityMask

Link Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.linkOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?}
```

## transparency.setOpacityMask

Opacity Mask Options

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.setOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?, clip?, invert?, disabled?, linked?} change the opacity masks of `ids`, the selection, or the object whose mask is being edited
```

## transparency.toggleNewMasksClipping

New Opacity Masks Are Clipping

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.toggleNewMasksClipping`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?} → {value}
```

## transparency.toggleNewMasksInverted

New Opacity Masks Are Inverted

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.toggleNewMasksInverted`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?} → {value}
```

## transparency.opacityMaskInfo

Opacity Mask Info

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.opacityMaskInfo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?} → [{id, clip, invert, disabled, linked, art}] the opacity masks of `ids`, the selection, or the object whose mask is being edited
```

## transparency.info

Transparency Info

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?} → {ids, opacity: 0..100, blend, isolate, knockout: "on"|"off"|"neutral", knockoutShape, editingMask, pageIsolatedBlending, pageKnockoutGroup} the Transparency panel's values for `ids`, the selection, or the object whose mask is being edited. A value is null where those objects differ (or there are none); editingMask is the id of the object whose mask is being edited, or null; the page values are the document's
```

## transparency.togglePageIsolatedBlending

Page Isolated Blending

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.togglePageIsolatedBlending`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?} make the page an isolated group (default: toggle): blend modes of top-level objects don't blend with what lies under the page; saved with the document and written to PDF → {value}
```

## transparency.togglePageKnockoutGroup

Page Knockout Group

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.togglePageKnockoutGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{value?} make the page a knockout group (default: toggle): its layers (the contents of neutral layers) hide what they cover instead of showing it through their transparency; saved with the document and written to PDF → {value}
```

## layer.new

New Layer…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?} → {id} (above the current layer)
```

## layer.newSublayer

New Sublayer…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newSublayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{parent?: id, name?} → {id}
```

## layer.delete

Delete Layer

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} (default: current layer)
```

## layer.duplicate

Duplicate Layer

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?}
```

## layer.setCurrent

Set Current Layer

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.setCurrent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## layer.setProps

Layer Options…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.setProps`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, name?, visible?, locked?, template?, printable?, color?: index 0..26}
```

## layer.collectInNew

Collect in New Layer

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.collectInNew`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.selectAll

Select All Art on Layer

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.selectAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id}
```

## node.move

Reorder

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe node.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, parent?: id (null = top level), index} drag-reorder in the Layers panel
```

## artboard.new

New Artboard

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x?, y?, width?, height?, name?} (default: right of the last)
```

## artboard.delete

Delete Artboard

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index}
```

## artboard.setProps

Artboard Options…

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.setProps`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index, name?, x?, y?, width?, height?}
```

## artboard.fitToArt

Fit to Artwork Bounds

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.fitToArt`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index?}
```

## artboard.fitToSelection

Fit to Selected Art

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.fitToSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index?}
```

## layer.clippingMask.toggle

Make/Release Clipping Mask

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.clippingMask.toggle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?: layer or group (default: the one selected group, else the current layer)} make: its top object (a path, compound path or text, which loses its paint) clips the rest and moves to the bottom (new art added on top is clipped); release: it stops clipping, the clipping path stays unpainted → {clip}
```

## layer.target

Target

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.target`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id} target a layer, group or object as clicking its target circle in the Layers panel does: a layer gets its visible, unlocked art selected and becomes the current layer, and appearance.*, effect.*, transparency.* and the opacity-mask commands without `ids` then act on the layer itself; anything else is selected. Any other selection change ends the targeting (`document.inspect` → target) → {id, selected: [..]}
```

## layer.pasteRemembersLayers

Paste Remembers Layers

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.pasteRemembersLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?} (default: toggle) the document option: on, the Paste commands put objects back into the layers they were copied from (by name; a missing one is made on top), off into the current layer; one undo step when it changes (document.inspect → pasteRemembersLayers) → {on}
```

## path.freehand

Pencil

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.freehand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], fidelity?: pt (1.5), closed?, style?: "pencil"|"brush", fill?: bool, extend?: {id, end: "start"|"end"}} fit a freehand stroke → {id}
```

## path.curvature

Curvature

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.curvature`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [{x, y, corner?}], closed?, id?} create (or with id: replace) a path curving through the points → {id}
```

## path.removeAnchor

Delete Anchor Point

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.removeAnchor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpath, anchor} remove one anchor, re-fitting the curve
```

## path.convertAnchor

Convert Anchor Point

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.convertAnchor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpath, anchor, to: "corner"|"smooth", x?, y?} (smooth with x/y: out handle there, in handle mirrored)
```

## path.reshapeSegment

Reshape Segment

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.reshapeSegment`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpath, segment, t, dx, dy} bend a segment so the point at t moves by (dx, dy)
```

## path.split

Split Path

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.split`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, subpath, segment, t} or {id, subpath, anchor}: closed paths open there, open paths become two → {ids}
```

## path.knife

Knife

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.knife`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…]} cut closed shapes (selected, or all when nothing is selected) along the polyline → {ids}
```

## path.eraseRegion

Eraser

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.eraseRegion`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], size?: pt (10)} erase a round-brush stroke from paths (selected, or all) → {ids}
```

## path.eraseSegments

Path Eraser

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.eraseSegments`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], width?: pt (8)} erase the parts of selected paths under the drag → {ids}
```

## path.smoothRegion

Smooth

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.smoothRegion`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], radius?: pt (12), fidelity?: pt (2.5)} smooth selected paths near the drag → {ids, before, after}
```

## path.joinScrub

Join

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.joinScrub`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], tolerance?: pt (12)} join the open-path endpoints scrubbed over → {id}
```

## path.blob

Blob Brush

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.blob`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], size?: pt (10), merge?: true} filled brush shape, merged with touching same-colour blobs → {id}
```

## object.distort

Free Distort

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.distort`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{corners: [[x,y]×4] (TL, TR, BR, BL), from?: [x0,y0,x1,y1] (default: selection bounds), ids?} projective warp of anchors and handles
```

## paint.sampleColor

Sample Color

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.sampleColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{color, stroke?: bool (default: whichever proxy is active), ids?, stop?: index} sample a colour into the active fill/stroke (and the selection); with `stop`, recolour that stop of the gradient behind the proxy instead (paint.editGradient)
```

## eyedropper.setOptions

Eyedropper Options

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe eyedropper.setOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{sampleSize?: 1|3|5 (pixels square averaged when sampling an image: point, 3×3, 5×5), pickUp?, apply?: {appearance?: {transparency?, fill?: {color?, transparency?, overprint?}, stroke?: {color?, transparency?, overprint?, weight?, cap?, join?, miter?, dash?}}, character?, paragraph?} (bools; a bool for a branch sets all of it)} Eyedropper Options, kept in the preferences: what appearance.copyFrom picks up from the clicked object and applies (only attributes in both trees are copied; every fill and stroke attribute copies the whole appearance stack); {} reads them → the options
```

## artboard.move

Move Artboard

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index, dx, dy, moveArt?: bool} move an artboard (and the unlocked art fully inside it)
```

## effect.apply

Apply Effect

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{effect: id (see effect.list, e.g. "stylize.dropShadow", "distort.roughen", "warp.arc"), params?: {…} (missing keys take the dialog defaults), item?: appearance item index|null (apply to that fill/stroke only; omitted: the Appearance panel's active item, else the whole object), ids?: [..] (layers too), target?: "object"|"contents" (contents: the objects inside groups and layers)} append a live effect to each selected object's appearance (a group's or layer's apply to its members as one piece: one combined shadow) → {ids, index, item}
```

## effect.list

Effects

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {catalog: [{id, label, menu, params, defaults, raster, lengths: {always, absolute (while relative is false)} (distance params Scale Strokes & Effects scales)}], applied: [{id, effects, items: [{index, kind: fill|stroke, effects}]}], activeItem} for the selection
```

## effect.remove

Remove Effect

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: int (position in the effect list), item?: appearance item index|null (that fill/stroke's effects; omitted: the active item, else the object's), ids?: [..]} → {ids}
```

## effect.setParams

Effect Options

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.setParams`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: int, params?: {…} (merged into the current parameters), visible?: bool, item?: appearance item index|null (as effect.remove), ids?: [..]} → {ids}
```

## effect.expandAppearance

Expand Appearance

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.expandAppearance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [..], target?} turn each object's appearance into objects: every fill and stroke becomes an object of its own (strokes outlined, brushed strokes their brush art) grouped in paint order under the object's id and transparency, geometry effects are baked, raster effects become an embedded image (shadows and outer glows below the art; blur, feather and inner glow replace it), type with effects or fills of its own is outlined; Crop Marks become a group of the object and its marks; a group's or layer's own fills and strokes become objects among its members, which are expanded too. Hidden fills, strokes and effects are dropped. Enabled when a selected or targeted object's appearance isn't basic (`ids` then pick which objects) → {ids}
```

## effect.duplicate

Duplicate Effect

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: int, item?: appearance item index|null (as effect.remove), ids?: [..]} insert a copy of the effect right after it → {ids}
```

## effect.move

Move Effect

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effect.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{from: int (position in the source list), to: int (its position in the destination list afterwards), fromItem?: appearance item index|null (the source list: that fill/stroke's effects, null the object's; omitted: the active item, else the object's), toItem?: item index|null (the destination list; default: the source list), copy?: bool (copy instead of move, as Alt-dragging the row), ids?: [..]} reorder an effect or move it between the object and its fills/strokes, as one undo step → {ids, index, item}
```

## object.pathfinder.unite

Unite

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.unite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.minusFront

Minus Front

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.minusFront`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.intersect

Intersect

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.intersect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.exclude

Exclude

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.exclude`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.divide

Divide

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.divide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.trim

Trim

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.trim`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.merge

Merge

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.crop

Crop

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.crop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.outline

Outline

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.outline`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.pathfinder.minusBack

Minus Back

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pathfinder.minusBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} operate on the selected objects (back → front) → {ids}
```

## object.path.outlineStroke

Outline Stroke

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.outlineStroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace stroked paths with filled outlines → {ids}
```

## object.path.offsetPath

Offset Path…

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.offsetPath`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{offset: pt (negative insets), joins?: "miter"|"round"|"bevel", miterLimit?: 4} → {ids} (new objects above the originals)
```

## object.path.simplify

Simplify…

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.simplify`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{tolerance?: pt (1), cornerAngle?: deg (30), straightLines?: bool} → {ids, before, after} anchor counts
```

## object.path.addAnchorPoints

Add Anchor Points

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.addAnchorPoints`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {ids}
```

## object.path.divideObjectsBelow

Divide Objects Below

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.divideObjectsBelow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} cut the objects below with the selected path (which is removed) → {ids}
```

## object.path.splitIntoGrid

Split Into Grid…

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.splitIntoGrid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rows?: 2, columns?: 2, gutter?: pt (12)} → {ids}
```

## object.path.cleanUp

Clean Up…

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.path.cleanUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{strayPoints?: true, unpaintedObjects?: true, emptyTextPaths?: true} → {removed}
```

## type.createOutlines

Create Outlines

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.createOutlines`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} convert the selected text to groups of compound paths (one per glyph) → {ids}
```

## text.setText

Set Text

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.setText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids?, text} replace the contents of text objects (keeps the first run's style)
```

## text.areaOptions

Area Type Options…

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.areaOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, rows?, columns?, gutter?: pt, inset?: pt, firstBaseline?: ascent|capHeight|xHeight|leading|fixed, firstBaselineMin?: pt} set the selected area type's options (none given: query) → the first object's options
```

## text.fitHeadline

Fit Headline

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.fitHeadline`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} track the first line of area type so it fills the frame width → {tracking}
```

## text.setStyle

Character

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.setStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?|id?, font?, style?, size?: pt, leading?: pt|"auto", tracking?: 1/1000 em, justify?: "left"|"center"|"right"|"justifyAll", fill?: colour, features?: ["dlig", "-liga", …] OpenType}
```

## object.lock.above

All Artwork Above

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.lock.above`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} lock objects in the same layer that are above and overlap the selection → {count}
```

## object.lock.otherLayers

Other Layers

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.lock.otherLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} lock every layer that holds no selected object → {count}
```

## object.hide.above

All Artwork Above

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.hide.above`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} hide objects in the same layer that are above and overlap the selection → {count}
```

## object.hide.otherLayers

Other Layers

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.hide.otherLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} hide every layer that holds no selected object → {count}
```

## object.transformEach

Transform Each…

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.transformEach`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{scaleH?: % (100), scaleV?: % (100), moveH?: pt, moveV?: pt (down = +), rotate?: deg (counter-clockwise), reflectX?: bool (flip vertically), reflectY?: bool (flip horizontally), random?: bool, seed?: n, reference?: 0..8 (9-point grid, 4 = centre), copy?: bool, strokes?: bool (Scale Strokes & Effects), corners?: bool (Scale Corners; both default to the preferences)} transform every selected object about its own reference point → {ids}
```

## object.resetBoundingBox

Reset Bounding Box

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.resetBoundingBox`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} no-op: VectorCraft bounding boxes are always axis-aligned to the document → {changed: 0}
```

## object.rasterize

Rasterize…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.rasterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ppi?, background?: transparent|white|black|"#rrggbb", antiAlias?: none|art|type (text snapped to pixels)|bool, padding?|addAround?: pt (0–1000), colorModel?: "rgb"|"cmyk"|"grayscale"|"bitmap", clippingMask?: bool (a clip group with the art's outline)} replace the selection with an embedded PNG image; each defaults to document.rasterEffectsSettings → {id (the image, or its clip group), width, height}
```

## object.createObjectMosaic

Create Object Mosaic…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.createObjectMosaic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{columns=10, rows=10, width?, height? (new size in pt; default the image's), spacingX=0, spacingY=0 (pt between tiles), gray?: bool, deleteRaster?: bool} a group of rectangles coloured by the selected image's average tile colours → {id, tiles}
```

## object.cropImage

Crop Image

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.cropImage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rect?: [x, y, width, height]} crop the selected image (default: to the artboard it sits on) → {id, width, height}
```

## object.createTrimMarks

Create Trim Marks

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.createTrimMarks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{style?: "roman"|"japanese" (default: the japaneseCropMarks preference; japanese: double lines at the trim and bleed edges plus centre marks), allArtboards?: bool (default: true when nothing is selected), offset?: pt (9, roman), length?: pt (18), bleed?: pt (8.5, japanese), weight?: pt (0.3)} trim marks stroked in [Registration] (printing on every plate) around the selection, or around every artboard, one group each, as one undo step → {id: the first group, ids}
```

## object.shape.convertToShape

Convert to Shape

- 技能 / Owner: `vectorcraft-cli-shapes`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-shapes`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.shape.convertToShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} turn paths that are rectangles (any rotation) or axis-aligned ellipses into live shapes → {converted}
```

## artboard.convertToArtboards

Convert to Artboards

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.convertToArtboards`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} turn each selected object's bounds into a new artboard (the objects are removed) → {artboards}
```

## artboard.rearrange

Rearrange All Artboards…

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.rearrange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{columns?: n (2), spacing?: pt (20), byColumn?: false, moveArtwork?: true} lay artboards out in a grid
```

## object.blend.make

Make

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, steps?: n | distance?: pt | smooth?: bool (default smooth colour), orientation?: page|path} blend the selected objects (paint order) into a live blend → {id}
```

## object.blend.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} release the selected blends, keeping the key objects → {ids}
```

## object.blend.options

Blend Options…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{spacing?: smooth|steps|distance, value?: n, steps?: n, distance?: pt, orientation?: page|path} set the options of the selected blends
```

## object.blend.expand

Expand

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace the selected blends by groups of their steps → {ids}
```

## object.blend.replaceSpine

Replace Spine

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.replaceSpine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} use the selected path as the spine of the selected blend (the path is consumed)
```

## object.blend.reverseSpine

Reverse Spine

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.reverseSpine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} reverse the order of the key objects along the spine
```

## object.blend.reverseFrontToBack

Reverse Front to Back

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.blend.reverseFrontToBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} reverse the stacking order of the selected blends
```

## object.envelope.makeWithWarp

Make with Warp…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.makeWithWarp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, style?: arc|arcLower|…|twist (arc), bend?: % (50), h?: %, v?: %, horizontal?: bool (true)} envelope the selected objects with a warp → {id}
```

## object.envelope.makeWithMesh

Make with Mesh…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.makeWithMesh`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, rows?: n (4), cols?: n (4)} envelope the selected objects with a point mesh → {id}
```

## object.envelope.makeWithTopObject

Make with Top Object

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.makeWithTopObject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} the topmost selected path becomes the envelope of the others → {id}
```

## object.envelope.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} release the selected envelopes → {ids}
```

## object.envelope.options

Envelope Options…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fidelity?: 0..100, style?, bend?, h?, v?, horizontal?} set envelope options (warp params for warp envelopes)
```

## object.envelope.expand

Expand

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace the selected envelopes by their distorted content → {ids}
```

## object.envelope.editContents

Edit Contents

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.editContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{editing?: bool} toggle Edit Contents / Edit Envelope → {editing}
```

## object.envelope.setMeshPoint

Move Envelope Mesh Point

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.envelope.setMeshPoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, index, x, y} move one point of a mesh envelope
```

## object.mesh.create

Create Gradient Mesh…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.mesh.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, rows?: n (4), cols?: n (4), appearance?: flat|center|edge, highlight?: % (100), at?: [x,y]} convert filled paths into gradient meshes in their fill colour (a gradient fill: the colour it paints at each point), lightened per `appearance` (with `at`: 1×1 mesh plus lines through that point) → {ids, index?}
```

## object.mesh.setPointColor

Set Mesh Point Color

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.mesh.setPointColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, index, color, opacity?: 0..1} colour of one mesh point
```

## object.mesh.movePoint

Move Mesh Point

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.mesh.movePoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, index, x, y, handle?: 0 right|1 left|2 down|3 up} move a mesh point (its handles follow), or with `handle` place that handle end at (x, y)
```

## object.mesh.addLine

Add Mesh Line

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.mesh.addLine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, x, y, color?} add a mesh row and column through (x, y) → {index}
```

## object.mesh.deletePoint

Delete Mesh Point

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.mesh.deletePoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, index} delete the mesh lines through a point
```

## object.mesh.expand

Expand Gradient Mesh

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.mesh.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace the selected meshes by groups of flat-coloured pieces → {ids}
```

## edit.colors.invert

Invert Colors

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.invert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fill?: true, stroke?: true, includeImages?: true, includePatterns?: true, ids?} replace each colour by its RGB inverse (keeps the colour model) in fills, strokes, text, gradient meshes (with fills), embedded images (a recoloured copy) and pattern tiles (a new pattern swatch; the original stays), as one undo step → {changed}
```

## edit.colors.toCMYK

Convert to CMYK

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.toCMYK`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fill?, stroke?, includeImages?, includePatterns?, ids?} (as edit.colors.invert) → {changed}
```

## edit.colors.toGrayscale

Convert to Grayscale

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.toGrayscale`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fill?, stroke?, includeImages?, includePatterns?, ids?} (as edit.colors.invert) → {changed}
```

## edit.colors.toRGB

Convert to RGB

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.toRGB`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fill?, stroke?, includeImages?, includePatterns?, ids?} (as edit.colors.invert) → {changed}
```

## edit.colors.saturate

Saturate…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.saturate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{intensity: -100..100 (%), fill?, stroke?, includeImages?, includePatterns?, ids?} scale saturation by (1 + intensity/100), reaching what edit.colors.invert does → {changed}
```

## edit.colors.adjustBalance

Adjust Color Balance…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.adjustBalance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{mode?: "rgb"|"cmyk"|"gray"|"global" (default: from the channels given), r?, g?, b? | c?, m?, y?, k? | gray? | tint?: -100..100 (% added per channel, default 0; `tint` is global mode: it shifts the tints of colours and gradient stops linked to global and spot swatches, which stay linked, and leaves other colours and images alone), convert?: false (true: the results stay in the adjusted model; false: each colour keeps its own), fill?, stroke?, includeImages?, includePatterns?, ids?} reaching what edit.colors.invert does → {changed}
```

## edit.colors.blendFrontToBack

Blend Front to Back

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.blendFrontToBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} ≥3 filled objects (solid fills or gradient meshes, which keep their shading): intermediate fills graded between the frontmost and backmost fill → {changed}
```

## edit.colors.blendHorizontally

Blend Horizontally

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.blendHorizontally`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} ≥3 filled objects or meshes: fills graded between the leftmost and rightmost → {changed}
```

## edit.colors.blendVertically

Blend Vertically

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.blendVertically`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} ≥3 filled objects or meshes: fills graded between the topmost and bottommost → {changed}
```

## color.harmony

Color Guide

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.harmony`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{color, rule: complementary|complementary2|splitComplementary|leftComplement|rightComplement|analogous|analogous2|monochromatic|shades|triad|triad2|triad3|tetrad|tetrad2|tetrad3|compound|compound2|highContrast|highContrast2|highContrast3|pentagram (or its label), steps?: 1..20 (4), variation?: "tintsShades"|"warmCool"|"vividMuted", amount?: 0..100 (50; how far the outermost steps go), limitTo?: swatch library id or name, or "document" (the document's swatches): every colour snaps to its nearest colour there (ΔE 2000)} the Color Guide for a base colour → {rule, colors: ["#rrggbb", the base first], grid: [per colour, 2·steps+1 variations from shades/cool/muted to tints/warm/vivid with the colour itself in the centre]}
```

## edit.colorSettings

Color Settings…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colorSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rgb?: profile, cmyk?: profile, intent?: "perceptual"|"relative"|"saturation"|"absolute", bpc?: bool} set the working spaces → {rgb, cmyk, intent, bpc, profiles: [{name, kind, builtin}]}
```

## color.loadProfile

Load Color Profile…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.loadProfile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path: .icc/.icm file} register an ICC profile (native only) → {name, kind}
```

## edit.assignProfile

Assign Profile…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.assignProfile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rgb?: profile|null, cmyk?: profile|null} tag the document with profiles (colour numbers are kept) → {rgb, cmyk}
```

## object.convertDocumentColorMode

Convert Document Color Mode

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.convertDocumentColorMode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
same as file.documentColorMode: {mode: "cmyk"|"rgb", convert?: true, intent?} → {changed} (an alias kept for older scripts; the command palette leaves it out)
```

## color.convert

Convert Color

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.convert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{color, to: "rgb"|"cmyk"|"gray"|"lab", intent?} → {model, values, hex, lab: [L,a,b], outOfGamut, deltaE}
```

## color.gamutCheck

Gamut Warning

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.gamutCheck`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, colors?: [color]} colours that can't be printed in the working CMYK (selection, or the whole document when nothing is selected) → {checked, outOfGamut: [{hex, deltaE, count}]}
```

## view.proofSetup

Proof Setup

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{target?: "workingCmyk"|"cmyk:<profile>"|"legacyMacRgb"|"srgb"|"monitorRgb"|"protanopia"|"deuteranopia", intent?, simulatePaper?, proof?: bool (also turn Proof Colors on)} → proof state
```

## view.proofColors

Proof Colors

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool (default: toggle)} → proof state
```

## view.overprintPreview

Overprint Preview

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.overprintPreview`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool (default: toggle)} → proof state
```

## view.separationsPreview

Separations Preview

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.separationsPreview`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool, plates?: [names], toggle?: plate, only?: plate} Separations Preview: show the chosen plates (one plate = greyscale ink coverage) → {on, plates: [{name, spot, visible, rgb}]}
```

## color.plates

Plates

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.plates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {on, plates: [{name, spot, visible, rgb}]}
```

## edit.colors.overprintBlack

Overprint Black…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colors.overprintBlack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{remove?: false, percentage?: 100, fill?: true, stroke?: true, includeCmyBlacks?: false, includeSpotBlacks?: false, ids?} make the black fills and/or strokes of the selection (or ids; groups: their contents; type: its characters) overprint, or stop (remove). Black: K ≥ percentage with no C, M or Y (any with includeCmyBlacks), not linked to a spot swatch (unless includeSpotBlacks); a gradient is black when every stop is → {changed: objects}
```

## swatch.setSpot

Spot Color

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.setSpot`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, spot?: true} make a swatch a spot colour (prints on its own plate; spot swatches are global) → {name, spot}
```

## type.changeCase

Change Case

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.changeCase`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{case: "upper"|"lower"|"title"|"sentence", ids?} → {ids}
```

## type.smartPunctuation

Smart Punctuation…

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.smartPunctuation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{quotes?: true (straight quotes become the Document Setup quotes), dashes?: true (-- → en dash, --- → em dash), ellipsis?: true (... → …), scope?: "selection"|"document"} → {changed}
```

## type.convertToAreaType

Convert To Area Type

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.convertToAreaType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} point type → area type framed by its current layout bounds → {ids}
```

## type.convertToPointType

Convert To Point Type

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.convertToPointType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} area type → point type; soft line wraps become line breaks → {ids}
```

## type.pathOptions

Type on a Path Options…

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.pathOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{start?: 0..1 (fraction of the path length), flip?: bool (reverse the path), effect?: rainbow|skew|3dRibbon|stairStep|gravity, ids?}
```

## type.fillPlaceholder

Fill with Placeholder Text

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.fillPlaceholder`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} replace selected text with placeholder text (area type is filled to its frame) → {ids}
```

## type.insert

Insert Character

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.insert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{char: "bullet"|"copyright"|"ellipsis"|"paragraph"|"registered"|"section"|"trademark"|"emDash"|"enDash"|"discretionaryHyphen"|"nonBreakingHyphen"|"doubleLeftQuote"|"doubleRightQuote"|"singleLeftQuote"|"singleRightQuote"|"emSpace"|"enSpace"|"hairSpace"|"sixthSpace"|"thinSpace"|"nonBreakingSpace"|"figureSpace"|"punctuationSpace"|"thirdSpace"|"quarterSpace"|"tab"|"forcedLineBreak"|"paragraphReturn" | text: string} append to the selected text objects
```

## edit.findReplace

Find and Replace…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.findReplace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{find, replace?: "", matchCase?: false, wholeWord?: false, ids?} replace in every text object (or ids) → {count}. Matches never span style runs.
```

## edit.findNext

Find Next

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.findNext`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{find, matchCase?, wholeWord?} select the next text object (after the selected one, wrapping) containing `find` → {id|null}
```

## edit.pasteWithoutFormatting

Paste without Formatting

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteWithoutFormatting`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{center?, dx?, dy?, swatchConflict?} paste as edit.paste; pasted text takes the default character style (one run) and leaves its character and paragraph styles behind → {ids, added, merged, renamed}
```

## text.editRange

Edit Text

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.editRange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, start: byte, end: byte, insert?: string, runs?: [{text, style}]} replace bytes start..end of the plain text (inserted text takes the replaced text's style unless styled `runs` are given) → {id, caret}
```

## text.setRangeStyle

Character

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.setRangeStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, start?: byte, end?: byte (default: all text), font?, style?, size?: pt, leading?: pt|"auto", tracking?, kerning?: 1/1000 em|"auto", baselineShift?: pt, hScale?: %, vScale?: %, rotation?: deg, fill?: colour|"none", stroke?: colour|"none", strokeWidth?: pt, strokeOptions?: {weight?, cap?, join?, miterLimit?, dash?, dashOffset?, alignDashes?} (as stroke.set: the character stroke), underline?, strikethrough?, allCaps?: bool, smallCaps?: bool, position?: "normal"|"superscript"|"subscript" (sizes from Document Setup), features?: ["dlig", "-liga", …]} style a character range (runs are split at the range ends) → {id, runs}
```

## text.getRange

Get Text Range

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.getRange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, start?, end?} → {text, runs: [{text, style}], length}
```

## text.createInPath

Area / Path Type

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.createInPath`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path: id, mode: "area"|"onPath", text?: "", at?: [x, y] (on-path start: nearest point), size?, font?} turn a path into an area-type frame or a type-on-a-path baseline (the path's paint is dropped) → {id}
```

## type.fitHeadline

Fit Headline

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.fitHeadline`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} track the first line of area type so it fills the frame width → {ids, tracking}
```

## charStyle.list

Character Styles

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {styles: [{name, attrs, uses}]}
```

## charStyle.new

New Character Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, attrs?: {…}} (default attrs: the selected text's) → {name}
```

## charStyle.apply

Apply Character Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, clearOverrides?, ids?|id + start?/end? (a Type tool range)} → {count}
```

## charStyle.redefine

Redefine Character Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.redefine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, id?, start?} from the selected text; users keep their overrides
```

## charStyle.setAttrs

Character Style Options

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.setAttrs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, attrs: {…}} replace the style's attributes; users keep their overrides
```

## charStyle.duplicate

Duplicate Character Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} → {name}
```

## charStyle.rename

Rename Character Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, to}
```

## charStyle.delete

Delete Character Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe charStyle.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} (text keeps its look)
```

## paraStyle.list

Paragraph Styles

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {styles: [{name, attrs, uses}]}
```

## paraStyle.new

New Paragraph Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, attrs?: {…}} (default attrs: the selected text's) → {name}
```

## paraStyle.apply

Apply Paragraph Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, clearOverrides?, ids?|id + start?/end? (a Type tool range)} → {count}
```

## paraStyle.redefine

Redefine Paragraph Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.redefine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, id?, start?} from the selected text; users keep their overrides
```

## paraStyle.setAttrs

Paragraph Style Options

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.setAttrs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, attrs: {…}} replace the style's attributes; users keep their overrides
```

## paraStyle.duplicate

Duplicate Paragraph Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} → {name}
```

## paraStyle.rename

Rename Paragraph Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, to}
```

## paraStyle.delete

Delete Paragraph Style

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paraStyle.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} (text keeps its look)
```

## text.fonts

Fonts in Document

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.fonts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{selectionOnly?} → [{family, style, runs, objects, missing}] sorted by name
```

## text.replaceFont

Replace Font

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.replaceFont`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{from: {family, style?}, to: {family, style?}, selectionOnly?} (style omitted: every style of the family / keep the closest style) → {runs}
```

## select.font

Select Text by Font

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.font`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{family, style?} select the text objects using the font → {count}
```

## help.discord

Join Our Discord

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe help.discord`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {url} the ArtCraft community Discord
```

## help.website

ArtCraft Website

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe help.website`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {url}
```

## help.appPage

VectorCraft on getartcraft.com

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe help.appPage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {url} this app's page
```

## help.github

VectorCraft on GitHub

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe help.github`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {url} source code, issues and releases
```

## help.links

Links

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe help.links`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {discord, website, appPage, github}
```

## text.thread.create

Create

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.thread.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} thread the selected area type (and closed paths, which become frames) in stacking order → {ids}
```

## text.thread.releaseSelection

Release Selection

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.thread.releaseSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} take the selected frames out of their threads (the story re-flows through the rest)
```

## text.thread.remove

Remove Threading

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.thread.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} break the selected frames' threads; each frame keeps the text it shows
```

## text.thread.info

Threads

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.thread.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [[id…]] every thread in order
```

## object.textWrap.make

Make

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.textWrap.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{offset?: pt (6), invert?: bool, ids?} area type below the selected objects (same layer) wraps around them → {ids}
```

## object.textWrap.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.textWrap.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} → {ids}
```

## object.textWrap.options

Text Wrap Options…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.textWrap.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{offset?: pt, invert?: bool, ids?} set the options of the selected wrap objects; no options → the current {offset, invert}
```

## graph.create

Create Graph

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graph.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{type: column|stackedColumn|bar|stackedBar|line|area|scatter|pie|radar, x, y, width, height, series?: [..], categories?: [..], rows?: [[..]], csv?} → {id}
```

## graph.setData

Data…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graph.setData`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?, series?, categories?, rows?, csv?: first row = series labels (first cell empty), then one row per category: label, values…} replace the graph's data; no data → the current {csv, series, categories, rows}
```

## graph.setType

Type…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graph.setType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?, type?, columnWidth?: %, clusterWidth?: %, legend?: bool, markPoints?: bool, connectPoints?: bool, ticks?: n, axisMin?, axisMax?} change the graph type and options; no options → the current ones
```

## document.rasterEffectsSettings

Document Raster Effects Settings…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.rasterEffectsSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{resolution?: ppi (1–2400) | "screen" (72) | "medium" (150) | "high" (300), colorModel?: "rgb"|"cmyk" (the document's mode)|"grayscale"|"bitmap", background?: "transparent"|"white", antiAlias?: bool (off: hard edges), clippingMask?: bool (white background only under the art; Rasterize clips to the art), addAround?: pt (0–1000, room around the art), preserveSpotColors?: bool (stored)} how raster effects (shadows, glows, blurs, feathers) become images in PDF export and Expand Appearance, and the defaults of object.rasterize; one undo step; always → the settings
```

## view.saved.new

New View…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.saved.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, center: [x, y], zoom: (1 = 100%), rotation?: deg} save a view (the app fills in the current one) → {name, index}
```

## view.saved.edit

Edit Views…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.saved.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, newName?, delete?: bool} rename or delete a saved view; no params → {views}
```

## view.saved.list

Saved Views

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.saved.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {views: [{name, center, zoom, rotation}]}
```

## view.transparencyGrid

Show Transparency Grid

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.transparencyGrid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool (default: toggle)} show the transparency grid behind the active document's artboards (each document has its own setting) → {on}
```

## transparency.editOpacityMask

Edit Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.editOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} edit the mask art of `id` (default: the first selected object with a mask) in place, as clicking the mask thumbnail in the Transparency panel does → {layer}
```

## transparency.stopEditingOpacityMask

Stop Editing Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.stopEditingOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} leave mask editing (the object thumbnail) → {id}
```

## transparency.viewOpacityMask

View Opacity Mask

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transparency.viewOpacityMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool (default: toggle), id?} show only the opacity mask of `id` (default: the object whose mask is edited, else the first selected object with a mask) on the canvas, as greyscale coverage, and edit it, as Alt-clicking the mask thumbnail does; off shows the artwork again (still editing) → {on, id}
```

## text.tabs.set

Set Tab Stops

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.tabs.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stops: [{position: pt, align?: left|center|right|decimal, leader?: ". ", alignOn?: "."}], ids?} replace the tab stops of the selected text
```

## text.tabs.get

Tab Stops

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.tabs.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} → {stops} of the first selected text object
```

## text.tabs.clear

Clear All Tabs

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.tabs.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?}
```

## select.same.symbolInstance

Symbol Instance

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.symbolInstance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.same.fontFamily

Font Family

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.fontFamily`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.same.fontFamilyStyle

Font Family & Style

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.fontFamilyStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.same.fontFamilyStyleSize

Font Family, Style & Size

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.fontFamilyStyleSize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.same.fontSize

Font Size

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.fontSize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.same.textFillColor

Text Fill Color

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.textFillColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.same.textStrokeColor

Text Stroke Color

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.same.textStrokeColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.object.directionHandles

Direction Handles

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.directionHandles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} direct-select every anchor (showing all handles) of the selected paths → {anchors}
```

## select.object.pointText

Point Text Objects

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.pointText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.object.areaText

Area Text Objects

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.areaText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.object.brushStrokes

Brush Strokes

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.brushStrokes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {count}
```

## select.object.bristleBrushStrokes

Bristle Brush Strokes

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.bristleBrushStrokes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} objects whose brush name contains "bristle" → {count}
```

## select.save

Save Selection…

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?} remember the current selection for this session (default name "Selection N") → {name}
```

## select.recall

Recall Selection

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.recall`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} → {count}
```

## select.editSaved

Edit Selection…

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.editSaved`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, newName?: rename, delete?: bool}
```

## select.savedList

Saved Selections

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.savedList`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [name…] for the active document
```

## view.guides.make

Make Guides

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.guides.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} turn the selected paths into guides → {count}
```

## view.guides.release

Release Guides

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.guides.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} turn the selected guides (or, with none selected, all guide paths) back into paths → {count}
```

## view.guides.lock

Lock Guides

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.guides.lock`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{locked?: bool} toggle (or set) the session's guide lock → {locked}
```

## view.guides.clear

Clear Guides

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.guides.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} delete all ruler guides and guide paths → {count}
```

## guide.add

Add Guide

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe guide.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{vertical: bool, pos: pt (x for vertical, y for horizontal)} → {index}
```

## guide.remove

Remove Guide

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe guide.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index}
```

## guide.move

Move Guide

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe guide.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index, pos: pt}
```

## file.closeAll

Close All

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.closeAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {closed}
```

## file.documentColorMode

Document Color Mode

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.documentColorMode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{mode: "cmyk"|"rgb", convert?: true (convert every colour of the art, symbols and swatches through the colour settings; swatch links kept; greys stay greys), intent?} → {changed}
```

## file.info

File Info…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{title?, author?, authorTitle?, description?, keywords?: [string…]|"a, b" (each once), rating?: 0–5, copyrightStatus?: "unknown"|"copyrighted"|"publicDomain", copyrightNotice?, copyrightUrl?} set the File Info in one undo step (SVG with metadata, PDF and PNG exports carry it); no params → {title, author, authorTitle, description, keywords, rating, copyrightStatus, copyrightNotice, copyrightUrl, created, modified (ISO 8601 UTC or null; read-only), colorMode, units, artboards, objects}
```

## document.info

Document Info

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{selectionOnly?, category?: document|objects|graphicStyles|spotColors|patterns|gradients|symbols|fonts|fontDetails|linkedImages|embeddedImages (only that one in sections and the text), format?: "text" (→ {text}: the report Document Info › Save… and Package write)} → {document, objects: {paths, compoundPaths, groups, …}, fonts, images, swatches, graphicStyleNames (with selectionOnly: the styles the selected objects are linked to), …, sections: [{id, title, rows: [[label, value]]}] (the panel's categories; fontDetails: each font's file and whether its licence lets it be embedded)}
```

## object.makePixelPerfect

Make Pixel Perfect

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.makePixelPerfect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} snap each object's edges to the pixel grid (odd stroke weights on half pixels) and round stroke weights
```

## artboard.reorder

Move Artboard Up/Down

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.reorder`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index, to} change an artboard's number
```

## artboard.duplicate

Duplicate Artboard

- 技能 / Owner: `vectorcraft-cli-artboards`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-artboards`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe artboard.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index} copy placed right of the last artboard
```

## text.setFormat

Character / Paragraph

- 技能 / Owner: `vectorcraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe text.setFormat`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?|id?, kerning?: 1/1000 em|"auto", baselineShift?: pt, hScale?: %, vScale?: %, rotation?: deg, underline?, strikethrough?, allCaps?, smallCaps?: bool, position?: "normal"|"superscript"|"subscript" (sizes from Document Setup), leftIndent?, rightIndent?, firstLineIndent?, spaceBefore?, spaceAfter?: pt, hyphenate?: bool}
```

## shapeBuilder.merge

Shape Builder

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shapeBuilder.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [id…] (default: selection), points: [[x,y]…] (drag path; one point = click), erase?: bool (Alt-drag deletes the regions), fill?: "#rrggbb" | {color|swatch|gradient|none} (default: the fill of the object under the first point)} → {ids, merged, regions}
```

## shapeBuilder.regions

Shape Builder Regions

- 技能 / Owner: `vectorcraft-cli-boolean`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-boolean`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shapeBuilder.regions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} → {regions: [{bounds: [x0,y0,x1,y1], area, sources: [id…]}]} faces of the planar arrangement
```

## livePaint.make

Make

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} build a Live Paint group from the selected paths → {id, faces, edges}
```

## livePaint.merge

Merge

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} add the other selected paths (and Live Paint groups) to the first Live Paint group, keeping its paint → {id, faces, edges}
```

## livePaint.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} replace Live Paint groups with their original paths → {ids}
```

## livePaint.expand

Expand

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} turn Live Paint groups into plain groups of their painted faces and edges → {ids}
```

## livePaint.fill

Live Paint Bucket

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.fill`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{group?: id | ids?: [id…] (paths to make live first), point: [x,y], color?|swatch?|gradient?|none? (default: current fill)} fill the face containing point → {group, face}
```

## livePaint.strokeEdge

Live Paint Bucket (Stroke)

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.strokeEdge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{group: id, point: [x,y], color?|swatch?|none? (default: current stroke), width?: pt (default: current weight), tolerance?: pt (4)} paint the edge nearest point → {group, edge}
```

## livePaint.info

Live Paint Info

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe livePaint.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{group} → {faces: [{id, fill, bounds}], edges: [{id, stroke, width}], sources}
```

## imageTrace.make

Make

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe imageTrace.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?: image or Image Trace group (default: selection), preset?: name (imageTrace.presets), params?: {mode: "blackAndWhite"|"grayscale"|"color", threshold: 0-255, colors: 2-256, paths: 0-100, corners: 0-100, noise: px, method: "abutting"|"overlapping", ignoreWhite, snapCurvesToLines}} → {id, paths, anchors, colors}
```

## imageTrace.makeAndExpand

Make and Expand

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe imageTrace.makeAndExpand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
same as imageTrace.make, then expand → {id, paths, anchors, colors}
```

## imageTrace.release

Release

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe imageTrace.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} put the source image back in place of Image Trace groups → {ids}
```

## imageTrace.expand

Expand

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe imageTrace.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} keep only the traced paths (drop the source image) → {ids}
```

## imageTrace.presets

Image Trace Presets

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe imageTrace.presets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {presets: [{name, params}]}
```

## brush.list

Brushes

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {brushes: [{name, type}], current}
```

## brush.get

Brush Definition

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} → the brush definition (JSON)
```

## brush.apply

Apply Brush

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, ids?} apply a brush to the strokes of the selected paths (adds a stroke if missing) and make it current → {ids}
```

## brush.remove

Remove Brush Stroke

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} remove brushes from the selected strokes → {ids}
```

## brush.setCurrent

Current Brush

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.setCurrent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name: string|null} the brush the Paintbrush tool paints with (not an undo step)
```

## brush.new

New Brush…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{type: calligraphic|scatter|art|pattern|bristle, name?, params?: {…definition fields}, ids?} new brush; art/scatter/pattern brushes take the selected art (pattern: side tile) unless params give it → {name}
```

## brush.delete

Delete Brush

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} delete a brush; strokes using it become plain strokes
```

## brush.duplicate

Duplicate Brush

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, newName?} → {name}
```

## brush.options

Brush Options…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, params?: {…fields to change}, newName?} edit a brush definition (strokes using it update) → {name}
```

## object.expandBrush

Expand Brush Strokes

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.expandBrush`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} replace brushed paths (in the selection) with groups of the brush art → {ids}
```

## brush.freehand

Paintbrush

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.freehand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{…path.freehand params, brush} paint a freehand stroke with a brush → {id}
```

## symbol.list

Symbols

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {symbols: [{name, instances, size: [w,h]}], current}
```

## symbol.new

New Symbol…

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, ids?} make a symbol from the selection and replace it with an instance → {name, id}
```

## symbol.place

Place Symbol Instance

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.place`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?, x?, y?} place an instance centred at (x, y) (default: artboard centre; name default: current) → {id}
```

## symbol.breakLink

Break Link to Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.breakLink`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} expand selected instances into plain art → {ids}
```

## symbol.edit

Edit Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} break the link of the selected instance so its art can be edited; finish with symbol.update → {name, ids}
```

## symbol.update

Redefine Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.update`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, ids?} replace the symbol's art with the selection (instances update; the selection becomes an instance) → {name, id}
```

## symbol.delete

Delete Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, expandInstances?: true} delete a symbol; its instances are expanded (or deleted with false)
```

## symbol.duplicate

Duplicate Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, newName?} → {name}
```

## symbol.replace

Replace Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.replace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, ids?} swap the symbol of the selected instances → {ids}
```

## symbol.setCurrent

Current Symbol

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.setCurrent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} the symbol the symbolism tools spray (not an undo step)
```

## symbol.selectInstances

Select All Instances

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.selectInstances`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} select every instance of a symbol → {count}
```

## symbol.spray

Symbol Sprayer

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.spray`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [[x,y]…], name?, radius?: 40, density?: 1..10 (5), scale?: 1, alt?: bool (remove instances)} spray instances into a symbol set → {id, count}
```

## symbol.adjust

Symbolism Tool

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe symbol.adjust`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{tool: shift|scrunch|size|spin|stain|screen|style, points: [[x,y]…], radius?: 40, intensity?: 1..10 (5), alt?: bool, color?, style?: name} adjust instances near the points (selection, else all) → {count}
```

## object.pattern.make

Make

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pattern.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, name?, tileType?: grid|brickByRow|brickByColumn|hexByColumn|hexByRow, brickOffset?: 0..1 (0.5), width?, height?, edit?: bool (true)} make a pattern swatch from the selection and enter pattern editing mode → {name}
```

## object.pattern.edit

Edit Pattern

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pattern.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?} edit a pattern (default: the selected object's fill pattern) in pattern editing mode
```

## object.pattern.done

Done

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pattern.done`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} leave pattern editing mode, saving the tile art into the pattern
```

## object.pattern.cancel

Cancel

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pattern.cancel`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} leave pattern editing mode, discarding changes
```

## object.pattern.saveCopy

Save a Copy

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.pattern.saveCopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?} while editing, save the current tile as a new pattern swatch → {name}
```

## pattern.options

Pattern Options

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name? (default: the pattern being edited), newName?, tileType?, brickOffset?, width?, height?, hSpacing?, vSpacing?, sizeTileToArt?: bool, overlap?: {h: left|right, v: top|bottom}, copies?: 3|5|7|9, dimCopies?: %, showTileEdge?: bool, showSwatchBounds?: bool (outline the part of the tiling the swatch repeats, dashed)}
```

## pattern.delete

Delete Pattern

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} delete a pattern swatch (objects painted with it lose that paint)
```

## pattern.list

List Patterns

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {patterns: [{name, tileType, width, height, ...}], editing?}
```

## pattern.transform

Transform Patterns

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.transform`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, matrix: [a,b,c,d,e,f]} transform only the pattern placement of the objects' pattern paints (Transform Patterns)
```

## object.repeat.radial

Radial

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.repeat.radial`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, instances?: n (8), radius?: pt} radial repeat of the selection (or switch the selected repeat to radial) → {id}
```

## object.repeat.grid

Grid

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.repeat.grid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, hSpacing?: pt, vSpacing?: pt (¼ of the art size), rows?: n (3), cols?: n (3)} grid repeat of the selection → {id}
```

## object.repeat.mirror

Mirror

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.repeat.mirror`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, angle?: deg (90 = vertical axis), offset?: pt (10)} mirror repeat of the selection → {id}
```

## object.repeat.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.repeat.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} release the selected repeats back to their source art → {ids}
```

## object.repeat.options

Options…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.repeat.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{instances?, radius?, reverseOverlap?, startAngle?, endAngle?, center?: [x,y] | hSpacing?, vSpacing?, rows?, cols?, gridType?, flipRows?, flipCols? | angle?} set the options of the selected repeats
```

## object.repeat.expand

Expand Repeat

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.repeat.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace the selected repeats by groups of their instances → {ids}
```

## prefs.get

Get Preferences

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{key?} → the value of one preference (or preference group: eyedropper), or {prefs: {…all…}}
```

## prefs.set

Set Preference

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{key, value} or {values: {key: value, …}} set preferences (validated; see prefs.list; lengths in pt or strings with a unit; unitsGeneral also sets the active document's units, one undo step; the eyedropper group takes a partial object, as eyedropper.setOptions)
```

## prefs.reset

Reset Preferences

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{category?} reset one category (or everything) to defaults
```

## prefs.list

List Preferences

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [{key, category, section, label, kind, value, …}] every preference
```

## stroke.widthPoint.set

Width Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthPoint.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, t: 0..1 (fraction of the path length), left, right: side widths in pt, index?: width point to edit or move, adjustAdjoining?: bool (with index: the nearest points either side change their widths in proportion)} → {index}. Without index a point already at t is replaced; a point moved onto another one's t joins it as a discontinuous point (on the side it came from), so the width steps there. Creates a uniform profile first if needed
```

## stroke.widthPoint.remove

Delete Width Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthPoint.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, index | indices: [..]} remove width points (removing the last one leaves a uniform stroke)
```

## stroke.widthPoint.copy

Copy Width Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthPoint.copy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id, index: the width point to copy, t: 0..1 where the copy goes} → {index} (Alt-drag with the Width tool). Landing on another point makes a discontinuous point, as a stroke.widthPoint.set move does
```

## stroke.widthProfile.set

Width Profile

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe stroke.widthProfile.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?|id?, points: [[t, left, right]…] (width factors, 1 = the stroke weight) | null = uniform}
```

## object.liquify

Liquify

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.liquify`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{tool: warp|twirl|pucker|bloat|scallop|crystallize|wrinkle, points: [[x,y]…] (the brush stroke), diameter?|width?, height? (pt, default 100), angle?, intensity? (0..1 or %), detail? (1..10), simplify? (0..100), rate? (twirl °), complexity?, horizontal?, vertical?, affectAnchors?, affectIn?, affectOut?, ids? (default: selection, else every path the brush touches)}
```

## object.puppetWarp

Puppet Warp

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.puppetWarp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?|ids? (default: selection), pins: [[x,y]…] (current pin positions), moved: [[x,y]…] (targets, same length), expand?: pt} as-rigid-as-possible mesh warp of anchors and handles
```

## perspective.grid.set

Define Perspective Grid

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.grid.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind?: 1|2|3, origin?: [x,y], horizon?, vpLeft?, vpRight?, vpVertical?: [x,y], distance?, cell?, extent?, height?, visible?, plane?} merge into the document's grid
```

## perspective.grid.preset

Perspective Grid Preset

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.grid.preset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind: 1|2|3} reset the grid to the one/two/three-point preset for the first artboard (and show it)
```

## perspective.grid.show

Show Perspective Grid

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.grid.show`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{visible?: bool} (no param toggles). View state: not an undo step
```

## perspective.plane.set

Active Perspective Plane

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.plane.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{plane: left|right|ground|none} Plane Switching widget. View state: not an undo step
```

## perspective.attach

Attach to Active Plane

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.attach`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, plane?: left|right|ground (default: the active plane)} project the objects onto the plane
```

## perspective.release

Release with Perspective

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} detach from the grid (geometry unchanged)
```

## perspective.move

Move in Perspective

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, from: [x,y], to: [x,y], plane?} slide objects within their plane (unattached objects attach to `plane`/the active plane first)
```

## perspective.draw

Draw in Perspective

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perspective.draw`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{command: shape.* id, params, plane?} run a shape command and attach the result to the plane
```

## paint.invert

Invert

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.invert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stroke?: bool (default: the active proxy), ids?} invert the active proxy's colours of the selection (or ids; groups recolour their contents) keeping each colour's model, as edit.colors.invert does; the Appearance panel's active fill/stroke item (appearance.setActiveItem) is inverted instead when it is of that kind and no ids are given; with nothing selected, invert the default → {changed}
```

## paint.complement

Complement

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.complement`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stroke?: bool (default: the active proxy), ids?} replace the active proxy's colours by their complements ((highest + lowest) − each component, over RGB or CMY; grey unchanged) keeping each colour's model; honours the Appearance panel's active item as paint.invert does; with nothing selected, the default → {changed}
```

## paint.lastColor

Apply Last Color

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.lastColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stroke?: bool (default: the active proxy), ids?} apply the last solid colour used (paint.recent lastColor) to the active proxy of the selection and the default
```

## paint.lastGradient

Apply Last Gradient

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.lastGradient`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stroke?: bool (default: the active proxy), ids?} apply the last gradient used (paint.recent lastGradient), fitted to each object, to the active proxy of the selection and the default
```

## paint.recent

Recent Colors

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.recent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {colors: [{hex, color}] newest first (fed by every paint command and the eyedropper), lastColor: {hex, color}, lastGradient: gradient paint}
```

## paint.proxies

Fill and Stroke

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.proxies`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {fill, stroke: the paints the Fill/Stroke proxies show (the Appearance panel's active item for the proxy of its kind, else the first selected object's, a group's first painted object's, type: its first run's; else the defaults for new art), fillActive, fillMixed, strokeMixed: the selected objects' (or a selected group's contents') fills (strokes) differ, shown as a "?" proxy}
```

## object.setOverprint

Overprint

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.setOverprint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fill?: bool, stroke?: bool, item?: appearance item index|null, ids?} make fills and/or strokes overprint (Overprint Preview, Separations Preview) or knock out: item's, else every fill or stroke of the painted objects (groups: their contents; type: its characters too). Without item and ids, the Appearance panel's active item stands in when it is of that kind → {changed: objects}
```

## attributes.info

Attributes

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe attributes.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?, item?} → {ids, overprintFill, overprintStroke, showCenter, imageMap: "none"|"rectangle"|"polygon", url, note, fillRule: "nonZero"|"evenOdd" (of the paths and compound paths in them), reversed (their subpaths run counter-clockwise on screen: Reverse Path Direction On), recentUrls: [newest first]} the Attributes panel's values for `ids` or the selection, overprint aimed as object.setOverprint aims; a value is null where they differ (or nothing has a fill, stroke or path)
```

## swatch.library.list

Swatch Libraries

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.library.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {libraries: [{id, name, category: "builtIn"|"gradients"|"user" (User Defined: the library files in the user library folder, rescanned now)|"loaded" (swatch.library.load), count, path?}], userFolder} every library the library panel opens, in menu order
```

## swatch.library.get

Swatch Library

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.library.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{library: id or name} → {id, name, category, swatches: [{name, kind, group, global, spot, color?, hex?, gradient?}] (as swatch.list), groups: [{name, swatches: [names]}]}
```

## swatch.library.add

Add to Swatches

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.library.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{library: id or name, names?: [swatch or colour group names in the library] (default: all of it; a group comes as a colour group, a single swatch ungrouped), apply?: "fill"|"stroke" (also apply the first one to the selection and the defaults, as paint.setFill / paint.setStroke), focus?: true (with apply: false keeps the active proxy)} copy library swatches into the document as one undo step. A swatch the document already has (same name and paint) isn't added again; a name taken by another swatch gets a number ("Clay 1 2") → {library, added: [names in the document], existing: [names already there], applied?: name}
```

## swatch.resetDefaults

Default Swatches

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.resetDefaults`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{replace?: false} bring back the default swatches and colour groups of the document's colour mode that are missing (by name), as one undo step; replace: true makes the swatches exactly the defaults (art linked to a removed global swatch keeps its colour, unlinked) → {added: [names]}
```

## swatch.library.save

Save Swatch Library…

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.library.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?: "vcswatches" (lossless JSON: colour models, global, spot, gradients, groups) | "gpl" (8-bit RGB palette; groups as `# Group:` comments) | "css" (custom properties on :root) (default: the path's extension, else vcswatches), names?: [swatch or colour group names] (default: all; None and patterns are never saved), name?: library name (default: the document's), user?: false (save into the user library folder, listed under User Defined)} save the document's swatches as a library → {path, format, count, library?: id when saved to the user folder}; without path or user → {data: the file's text, format, count}
```

## swatch.library.load

Other Library…

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe swatch.library.load`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path? | data?: file text | dataBase64?, name?: file name (default: the path's)} load a .vcswatches or .gpl library, or the swatches of any document VectorCraft opens (see document.formats), for the library panel (Window → Swatch Libraries lists it until the app quits) → {library: id, name, count}
```

## paint.freeform.addPoint

Add Freeform Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.addPoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{at: [x,y] (document coordinates), color? (default: the gradient's colour there), opacity? 0..1 (or 0..100), spread? 0..1 (or 0..100 %; the radius of pure colour around the point, a fraction of half the object's larger side; default 0), line?: true (join it to the selected point: extends the line ending there, else starts one), ids?, stroke?: bool (default: the targeted item's kind, else the active proxy), item?: fill/stroke item index|null (omitted: the Appearance panel's active item when it is of the edited kind)} add a point to the freeform gradient (an unplaced one keeps its automatic points first) and select it → {index}
```

## paint.freeform.setPoint

Edit Freeform Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.setPoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index? (default: the selected point), at?: [x,y] (document coordinates), color?, opacity? 0..1 (or 0..100), spread? 0..1 (or 0..100 %), ids?, stroke?: bool (default: the targeted item's kind, else the active proxy), item?: fill/stroke item index|null (omitted: the Appearance panel's active item when it is of the edited kind)} move or recolour a point of the freeform gradient → {index}
```

## paint.freeform.deletePoint

Delete Freeform Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.deletePoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index? (default: the selected point), ids?, stroke?: bool (default: the targeted item's kind, else the active proxy), item?: fill/stroke item index|null (omitted: the Appearance panel's active item when it is of the edited kind)} remove a point (never the last one); lines through it close up around it and lines left with one point go → {index}
```

## paint.freeform.addLine

Add Freeform Line

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.addLine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{points: [index, …] (at least two), ids?, stroke?: bool (default: the targeted item's kind, else the active proxy), item?: fill/stroke item index|null (omitted: the Appearance panel's active item when it is of the edited kind)} join points with a smooth line through them, in order → {line}
```

## paint.freeform.splitLine

Split Freeform Line

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.splitLine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{line: line index, segment: the segment from the line's point `segment` to the next, t?: 0..1 along it (default 0.5), ids?, stroke?: bool (default: the targeted item's kind, else the active proxy), item?: fill/stroke item index|null (omitted: the Appearance panel's active item when it is of the edited kind)} add a point on a line there (colour, opacity and spread between the segment's ends) and select it → {index}
```

## paint.freeform.selectPoint

Select Freeform Point

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.selectPoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{index: point index | null to clear} select a point of the freeform gradient behind the active proxy (the first selected object's): the point the Gradient tool, the Gradient and Color panels and Delete act on → {index}
```

## paint.freeform.get

Freeform Gradient

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.freeform.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{stroke?: bool (default: the active proxy)} the freeform gradient behind the proxy of the first selected object → {mode: points|lines, points: [{at: [x,y] (document coordinates), color, opacity, spread}], lines: [[index, …]], selected: index|null}
```

## object.flattenTransparency

Flatten Transparency…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.flattenTransparency`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{preset?: "high"|"medium"|"low" or a saved preset's name (see flattener.presets.list; default medium), balance?: 0..100 (raster/vector balance; 0 rasterizes everything), lineArtPpi?: 1..2400, gradientPpi?: 1..2400 (areas only gradients and meshes reach), textToOutlines?, strokesToOutlines?, clipComplexRegions? (clip images to the region outlines, else rectangles), antiAlias?, preserveAlpha? (composite over nothing instead of white), preserveOverprints? (areas showing one paint keep its colour and overprint; false clears overprints), options?: {the same keys}, ids?} overlapping transparent objects become one group of flat-colour regions (CMYK colours composited ink by ink in CMYK documents), plus an image where gradients, patterns, images, masks or raster effects reach; objects without transparency stay → {ids, rasterized: images made, vector: regions made, options}
```

## flattener.presets.list

Transparency Flattener Presets

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe flattener.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {presets: [{name, builtIn, options}]} the built-in presets (High, Medium and Low Resolution), then the saved ones; any of these names works as `preset` wherever flattener options are taken
```

## flattener.presets.save

Save Transparency Flattener Preset

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe flattener.presets.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?: (default: a new "Flattener Preset N"), newName?: rename it, preset?: the preset to start from (default: the saved preset `name`, else medium), …options (the keys of object.flattenTransparency, at the top level or in `options`)} create or change a saved preset (built-in ones can't change) → {name, options, created}
```

## flattener.presets.delete

Delete Transparency Flattener Preset

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe flattener.presets.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} delete a saved preset (built-in ones stay) → {deleted: name}
```

## flattener.presets.import

Import Transparency Flattener Presets

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe flattener.presets.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path? | data?: file text | dataBase64?, replace?: false (replace saved presets of the same names; else the imported ones get a number)} add the presets of a .vcflattener file (as flattener.presets.export writes) to the saved ones → {imported: [names]}
```

## flattener.presets.export

Export Transparency Flattener Presets

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe flattener.presets.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{names?: [preset names, built-in ones too] (default: every saved preset), path?} write the presets as a .vcflattener file (JSON) → {path, count}; without path → {data: the file's text, count}
```

## flattener.preview

Flattener Preview

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe flattener.preview`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{highlight?: "none"|"rasterizedRegions" (areas the raster/vector balance rasterizes whole)|"transparentObjects"|"allAffected"|"expandedPatterns" (pattern art taking part)|"outlinedStrokes"|"outlinedText"|"allRasterized" (default none), overprints?: "preserve"|"simulate"|"discard" (simulate and discard flatten without preserveOverprints), preset?, …options (as object.flattenTransparency), ids?: (default: the whole document)} what flattening would do, without changing anything → {highlight, regions: [{bounds: {x, y, width, height}, id?}] (the highlighted objects, or areas), counts: {transparentObjects, allAffected, expandedPatterns, outlinedStrokes, outlinedText, rasterizedRegions, allRasterized, vectorRegions}, options}
```

## graphicStyle.libraries

Graphic Style Libraries

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.libraries`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {libraries: [{id, name, category: "builtIn"|"user" (User Defined: the .vcstyles files in the user library folder, rescanned now)|"loaded" (graphicStyle.loadLibrary), count, path?}], userFolder} every graphic style library the library panel opens, in menu order
```

## graphicStyle.library

Graphic Style Library

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.library`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{library: id or name} → {id, name, category, styles: [{name, fill, stroke, strokeWidth, fills, strokes, effects: [effect id…], opacity, blend, isolate, knockout}] (as graphicStyle.list)}
```

## graphicStyle.addFromLibrary

Add to Graphic Styles

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.addFromLibrary`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{library: id or name, name? | names?: [style names in the library] (default: all of it), apply?: false (also apply the first one to `ids` or the selection, if any, as graphicStyle.apply), add?: false (with apply: add its appearance on top, as Alt-click), ids?} copy library styles into the document's Graphic Styles as one undo step (with the apply). A style the document already has (same name and look) isn't added again; a name taken by another style gets a number ("Halo 2"). The patterns they paint with come along (a name taken by another pattern or swatch gets a number) → {library, added: [names in the document], existing: [names already there], applied?: name}
```

## graphicStyle.saveLibrary

Save Graphic Style Library…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.saveLibrary`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, names?: [style names] (default: all), name?: library name (default: the document's), user?: false (save into the user library folder, listed under User Defined)} save the document's graphic styles as a .vcstyles library (JSON: the styles, unlinked from swatches, and the patterns they paint with) → {path, count, library?: id when saved to the user folder}; without path or user → {data: the file's text, count}
```

## graphicStyle.loadLibrary

Other Library…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphicStyle.loadLibrary`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path? | data?: file text | dataBase64?, name?: file name (default: the path's)} load a .vcstyles library, or the graphic styles of any document VectorCraft opens (see document.formats), for the library panel (Window → Graphic Style Libraries lists it until the app quits) → {library: id, name, count}
```

## object.expand

Expand…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{object?: true (type → outlines, live shapes → paths, effects baked), fill?: true (gradient fills → `gradient` art), stroke?: true (strokes → filled outlines), gradient?: "objects" (default: `steps` solid strips, concentric ellipses for radial gradients) | "mesh" (a gradient mesh), both in a clip group shaped like the object (freeform gradients always become a mesh shaped like it), steps?: 1..1000 (255)} one undo step → {ids}
```

## object.expand.info

Expand Options

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.expand.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} what each Expand option would change in the selection → {object, fill, stroke} (true: something to expand)
```

## attributes.set

Attributes

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe attributes.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{overprintFill?: bool, overprintStroke?: bool (aimed as object.setOverprint's fill and stroke, item? too), showCenter?: bool (the canvas shows the selected object's centre point), imageMap?: "none"|"rectangle"|"polygon", url?: string ("" removes it; SVG export links the object), note?: string, ids?} set the Attributes panel's values on ids or the selection, as one undo step; a URL given joins the recent URLs (attributes.info) → {changed: objects}
```

## path.setFillRule

Fill Rule

- 技能 / Owner: `vectorcraft-cli-paths`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-paths`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.setFillRule`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rule: "nonZero"|"evenOdd", ids?} the fill rule of the paths and compound paths in ids or the selection (groups: those inside), as one undo step → {changed}
```

## appearance.setNewArtBasic

New Art Has Basic Appearance

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.setNewArtBasic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool (omitted: toggle)} the Appearance panel option (the preference newArtBasic, on by default): on, new art takes one fill and stroke (with the Stroke panel's options); off, the whole appearance of the last selected object (every fill, stroke and effect, opacity and blend mode) → {on}
```

## appearance.newArt

New Art Appearance

- 技能 / Owner: `vectorcraft-cli-appearance`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-appearance`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe appearance.newArt`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} what the next object drawn gets → {basic: New Art Has Basic Appearance, appearance: {items, effects} (the model's JSON; placed gradients relative to the unit box), opacity: 0..100, blend, graphicStyle: the style it is linked to or null, inherited: taken from the last selection}
```

## colorTheme.list

Color Themes

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe colorTheme.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} the saved colour themes, in order → {themes: [{name, colors: ["#rrggbb"], keys: [colour keys, exact in each colour's model], rule?}]}
```

## colorTheme.save

Save Theme

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe colorTheme.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{colors: [1–5 colours] | color + rule (a harmony rule id or label, see color.harmony: its 5-colour theme from that base colour, base first), rule?: the rule it was made with, name?: (default "Theme N"), replace?: a saved theme's name (overwrite that theme in place, e.g. after editing it; it may be renamed)} save a colour theme to the local theme library (the preferences) → {name, count: themes saved}
```

## colorTheme.delete

Delete Theme

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe colorTheme.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} delete a saved colour theme → {deleted}
```

## colorTheme.addToSwatches

Add to Swatches

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe colorTheme.addToSwatches`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} add a saved theme's colours to the Swatches panel as a colour group named after it (as swatch.newGroup), as one undo step → {name: the group's, swatches: [names]}
```

## document.exportPdf

Export PDF

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.exportPdf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, preset?: "VectorCraft Default" (built-in or saved: pdf.preset.list), created?: integer Unix seconds|null (PDF metadata date; null/default uses current export time), artboard? | artboards?: [i…] | range?: "1-3, 5" (1-based; default all, one page each), standard?: none|pdfA2b|pdfX1a|pdfX3|pdfX4, compatibility?: 1.4|1.5|1.6|1.7 (default)|2.0, preserveEditing? (on in VectorCraft Default: the native document as an embedded file, which document.open restores; choosing a standard turns it off, PDF/A refuses it), thumbnails?, fastWebView?, viewAfterSaving? (the app opens the written file), createLayers?, includeNonPrinting? (keep layers whose Print option is off; left out by default unless createLayers), compression?: {color?, gray?: {downsample: none|average|subsample|bicubic, ppi: 300, abovePpi: 450, compression: none|zip|jpeg|jpeg2000|auto, quality: minimum|low|medium|high|maximum}, mono?: {downsample, ppi: 1200, abovePpi: 1800, compression: none|ccittG3|ccittG4|zip|runLength} (black-and-white images), compressText?: true} (images above abovePpi are resampled to ppi; auto keeps JPEGs JPEG, the others lossless; JPEG needs opaque images; none, jpeg2000, CCITT and runLength are written as ZIP with a warning), marks?: {trim, registration, colorBars, pageInfo, kind: roman|japanese, weight: 0.25 (trim marks and targets), offset: 6 (pt from the artboard, at least the bleed)} (printer's marks in [Registration], every plate: trim marks, registration targets mid-side, CMYK/spot/black-tint colour bars on top, page information (title, artboard, date UTC) below), bleed?: {useDocument (the document's bleed, document.setup), top, bottom, left, right} (pt; art in the bleed is kept). Each page: TrimBox = artboard, BleedBox = artboard + bleed, MediaBox = that + the marks' room (art clipped to the BleedBox), output?: {conversion: none|destination|preserveNumbers, destination, profiles: none|all|destination|taggedSource, outputIntent, outputCondition, outputConditionId, registry, trapped}, advanced?: {fontSubsetPercent: 100, outlineText: true, overprint: preserve|discard}, security?: {openPassword, permissionsPassword, printing: none|low|high, changes: none|pages|forms|comments|any, copy, screenReader, plaintextMetadata}} → {path, bytes, warnings}; no path → {dataBase64, bytes, warnings}. The options apply over the preset (null keeps its value); options accepted but not applied yet come back as warnings; PDF/X, passwords and PDF/A-2b at 2.0 are refused. document.export {format: pdf} takes the same options
```

## document.pdfSettings

PDF Settings

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.pdfSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{preset?, includeDocument?: false, …document.exportPdf options} → {settings (the preset with the options applied), presets: [name…], changed: [{option: "compression.compressText", value}] (what differs from the preset), warnings}; includeDocument also exports the active document in memory and adds its warnings (knockout groups approximated, effects left out…)
```

## document.setup

Document Setup

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.setup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{units?: "Points"|"Inches"|"Millimeters"|…, bleed?: pt (all sides)|[top, bottom, left, right]|{top?, bottom?, left?, right?} (0–72 pt), outlineImages?: bool (show images in Outline mode), highlightSubstitutedFonts?: bool, highlightSubstitutedGlyphs?: bool, gridSize?: "small"|"medium"|"large", gridColors?: "Light"|"Medium"|"Dark"|"Red"|"Orange"|"Green"|"Blue"|"Purple"|[colour, colour] (transparency grid; the first is also the paper colour), simulatePaper?: bool, flattenerPreset?: "High Resolution"|"Medium Resolution"|"Low Resolution"|a saved preset (flattener.presets.list), discardWhiteOverprint?: bool, language?: "English: USA"|"German"|"French"|… (also picks its quotes), quotes?: {double?: "“”", single?: "‘’"} (beside a language: only if they differ from the current ones), typographersQuotes?: bool (typed straight quotes become the document's quotes), superscript?: {size?: %, position?: %}, subscript?: {size?: %, position?: %}, smallCapsSize?: %, exportText?: "editable"|"appearance" (SVG text as text or as outlines), backgroundContents?: "transparent"|"white" (white: raster exports are white behind the art)} change the document setup in one undo step; no params → the current setup
```

## file.newPresets

New Document Presets

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newPresets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{category?: "Recent"|"Saved"|"Mobile"|"Web"|"Print"|"Film & Video"|"Art & Illustration"|"Branding"|"Social"} the New Document presets by category (Recent: the last sizes used; Saved: the user's presets) → {categories: [{name, presets: [{name, size: "1920 × 1080 px", width: pt, height: pt, units, orientation, artboards, artboardLayout: {layout, columns, spacing, rightToLeft}, bleed, backgroundContents, colorMode, rasterEffectsPpi, previewMode}]}]}; file.new {preset: name} starts from one
```

## file.newPresets.save

Save Preset

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newPresets.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name, preset?: start from this preset, …settings as file.new (default: Letter in prefs unitsGeneral)} save New Document settings as a user preset (the Saved category; same name = replace) in the preferences → {name, count}
```

## file.newPresets.delete

Delete Preset

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newPresets.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} delete a saved New Document preset → {deleted}
```

## file.place

Place…

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.place`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path | name+dataBase64, link?: true (a raster image keeps its file's path; other files are embedded), text?: {characterSet?: "unicode" (UTF-8, or UTF-16 with a byte-order mark; other bytes as the platform's 8-bit set) | "ansi" (the platform's 8-bit set), platform?: "windows" (Windows-1252) | "mac" (Mac Roman), removeLineReturns?: false (each block of lines becomes one paragraph; blank lines end paragraphs), removeParagraphReturns?: false (drop blank lines), replaceSpaces?: n (runs of n ≥ 2 spaces become a tab)} (a .txt file, placed as area type filling rect, the replaced object's bounds, or else the artboard less a 36 pt margin), template?: false (onto a new locked template layer below the current layer), replace?: false (swap the one selected object, keeping its stacking place and transform; no at/rect), at?: [x, y] centre (default: the first artboard's centre), rect?: [x, y, width, height] fit inside, aspect kept (wins over at), page?: 1 (PDF/.ai page, or a native document's artboard), crop?: "crop" (clipped to that page or artboard, default) | "bounding" (the art's bounds) | "art" | "trim" | "bleed" | "media" (a PDF page's boxes), password? (an encrypted PDF)} → {ids, name, format, linked, width, height, warnings}. Raster images come in at 100% of their physical size (the file's ppi, else 72); SVG, PDF/.ai and native documents as one group, with the images, symbols, patterns and swatches they use. One undo step; selects what it placed (unless on a template layer); never touches the clipboard
```

## file.place.info

Placed File Info

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.place.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path | name+dataBase64, page?, crop?, password?, thumbnail?: px} what file.place would place, without placing it → {name, format, width, height (pt at 100%), pixelWidth?, pixelHeight?, ppi?: [x, y], colorMode?: RGB|Grayscale|CMYK (raster images), warnings, thumbnailBase64?: PNG of at most `thumbnail` (≤ 512) px on its longer side}
```

## image.info

Image Info

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} an image object (default: the one selected) → {id, name, linked, link, colorMode: RGB|Grayscale|CMYK, pixelWidth, pixelHeight, ppi: [x, y] at its placed size, width, height}
```

## file.place.queue

Load Place Cursor

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.place.queue`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{paths?: [path…], files?: [{name, dataBase64}…], link?, template?, page?, crop?, text?, thumbnail?: px} load the place cursor (the `place` tool) with up to 100 files (as file.place reads them): a click places the current file at 100% with its top-left corner there, a drag places it at the dragged size (aspect kept), ←/→ and ↑/↓ cycle the files, Esc discards the current one; each placement is a file.place, and the previous tool returns after the last → {count, files: [{name, format, width, height, thumbnailBase64?}], skipped: [{name, error}]}
```

## links.check

Check Links

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.check`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [image ids] (default: every linked image)} where each linked file is and whether it changed since it was read → {links: [{name, path, status: ok|modified|missing, ids, found?: path (found away from its path: relative to the document, or by name in its folder), preview: true (showing the low-resolution preview, not the file)}], missing, modified}
```

## links.update

Update Links

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.update`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [image ids] (default: the linked images whose file was modified or is showing its preview)} read their linked files again; each image keeps its bounds. One undo step → {updated: [ids], missing: [ids]}
```

## links.relink

Relink

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.relink`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [image ids] (default: the selected images; with folder and nothing selected, every missing link), path | folder} link images to the file at path, or each to the file of its link's name in folder; embedded images become linked; each keeps its bounds. One undo step → {relinked: [ids], notFound: [file names]}
```

## links.list

Links

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{show?: all (default)|missing|modified|embedded, sort?: name|kind (file format)|status (missing, modified, ok, embedded); default: stacking order, top first} every image object in the layers, as the Links panel lists them → {links: [{id, name, linked, status: ok|modified|missing|embedded, format, pixelWidth, pixelHeight, path?, found?: path (found away from its path), page?, preview?: true (showing the saved preview)}], missing, modified, embedded}
```

## links.goTo

Go To Link

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.goTo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} select image `id` (default: the first selected image); the Links panel scrolls it into view → {id, bounds: [x0, y0, x1, y1]}
```

## links.embed

Embed Image

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.embed`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [image ids] (default: the selected linked images)} keep the linked files' pixels in the document and drop the links (an image whose file can't be found and that shows the saved preview stays linked: relink it first). One undo step → {embedded: [ids], missing: [ids]}
```

## links.unembed

Unembed

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.unembed`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?: an embedded image (default: the one selected), path?} write the image's pixels to the file at path (PNG, JPEG, GIF or WebP as stored, other images as PNG; a path ending in .png/.jpg/.jpeg/.gif/.webp/.tif/.tiff/.bmp converts them) and link the image to it, keeping its bounds. One undo step → {id, path}; no path → {name, dataBase64} (nothing changes: there is no file to link to)
```

## links.info

Link Info

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id?} an image's Link Info (default: the one selected) → image.info's fields (id, name, linked, link, colorMode, pixelWidth, pixelHeight, width, height) and status: ok|modified|missing|embedded, format, ppi: [x, y] (the file's), effectivePpi: [x, y] (at its placed size), scale: [x%, y%] (of its 100% size), rotation (degrees, counter-clockwise), placement: {preserve, align, clip}; linked images also fileName, location (its folder), page?, fileSize? (bytes), modified?, created? (ms since the Unix epoch)
```

## links.placementOptions

Placement Options

- 技能 / Owner: `vectorcraft-cli-assets`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-assets`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe links.placementOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?: [image ids] (default: the selected images), preserve?: transforms|bounds (default)|fileDimensions|fit|fill, align?: topLeft|top|topRight|left|center (default)|right|bottomLeft|bottom|bottomRight (where the new art sits; not for bounds), clip?: false (clip it to the old bounds where it is larger)} how a file read again (links.relink, links.update) takes each image's place: transforms keeps its scale (relative to each file's 100% size), rotation and position; bounds stretches it into the old bounds; fileDimensions puts it at 100%, unrotated; fit and fill scale it proportionally to fit inside or cover the old bounds. Without options → {placement} of the first image; else one undo step → {ids, placement}
```

## pdf.preset.list

PDF Presets

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pdf.preset.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {presets: [{name, builtIn, supported (the writer produces its standard), description, settings (as document.pdfSettings)}]} the built-in presets (VectorCraft Default first), then the saved ones; any of these names works as `preset` wherever PDF options are taken
```

## pdf.preset.save

Save PDF Preset

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pdf.preset.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name?: (default: a new "PDF Preset N"), newName?: rename it, description?, preset?: the preset to start from (default: the saved preset `name`, else VectorCraft Default), …document.exportPdf options} create or change a saved preset (built-in presets are read-only; passwords are never stored) → {name, created, settings}
```

## pdf.preset.delete

Delete PDF Preset

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pdf.preset.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name} delete a saved preset (built-in ones stay) → {deleted: name}
```

## pdf.preset.export

Export PDF Presets

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pdf.preset.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{names?: [preset names, built-in ones too] (default: every saved preset), path?} write the presets as a .vcpdfpresets file (JSON) → {path, count}; without path → {data: the file's text, count}
```

## pdf.preset.import

Import PDF Presets

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pdf.preset.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path? | data?: file text | dataBase64?, replace?: false (replace saved presets of the same names; else imported ones whose name is taken get a number)} add the presets of a .vcpdfpresets file (as pdf.preset.export writes) to the saved ones → {imported: [names]}
```

## document.exportDxf

Export DXF

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.exportDxf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, version?: R12|R13|R14|2000|2004|2007|2010|2013|2018 (default), unit?: mm (default; any unit name: pt, in, cm…), scale?: 1 (drawing units per unit), scaleLineweights?: false, colors?: 8|16|256|true (default; true colour needs 2004+, else 256), rasterFormat?: png (default)|jpeg (placed images, written next to the file), preserve?: appearance (default: type as outlines; strokes a CAD line can't draw as filled outlines; brush art)|editability (type as text; every stroke a line with its lineweight and dashes), alterPaths?: false (every stroke as its filled outline), outlineText?: false, selectedOnly?: false (the selected objects, in their layers), artboard?: 0 (the origin is its bottom-left corner), useArtboards?: true (one drawing per chosen artboard, artboards?/range?, holding the art over it: {stem}-{artboard}.dxf) | false (the origin at the art's bounds)} → {path, bytes, warnings, files?, linked?: [image files]}; no path → {dataBase64, …, linked?: [{name, dataBase64}]}. Layers become DXF layers (hidden: off; locked; non-printing: not plotted); paths become polylines and splines, fills solid hatches. Same as document.export {format: dxf}
```

## file.package

Package

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.package`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folder?, name?: (default: "<document> Folder"), copyLinks?: true, linksFolder?: true (the linked files go in Links/, else next to the document), relink?: true (the packaged document links to the copies), copyFonts?: true (the fonts its type uses go in Fonts/; fonts whose licence doesn't allow embedding are left out), report?: true (<document> Report.txt)} copy the saved document as it is now into folder/name as <document>.vectorcraft with its linked files and fonts; the open document doesn't change → {folder, files: [paths relative to folder/name], links, fonts (counts copied), missingLinks: [file names not found], skippedFonts: [{font, reason}]}; no folder → the same with {name: "<name>.zip", dataBase64} (a zip of the files in <name>/) instead of folder
```

## object.slice.make

Make

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.make`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} make each selected object (or ids) an object slice: its slice follows the object's bounds → {ids: the new object slices}
```

## object.slice.release

Release

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} release the selected slices: an object slice leaves its object as it was, a user slice becomes an unpainted rectangle; the objects end up selected → {ids}
```

## object.slice.fromGuides

Create from Guides

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.fromGuides`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace the user slices with the grid the ruler guides cut the artboards into (two vertical and two horizontal guides give 9) → {ids}
```

## object.slice.fromSelection

Create from Selection

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.fromSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{ids?} a user slice over the visual bounds of the selected objects (or ids), selected → {id}
```

## object.slice.duplicate

Duplicate Slice

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dx?: pt (default 10), dy?: pt (default 10)} copy the selected slices as user slices with their options, offset by dx, dy; the copies are selected → {ids}
```

## object.slice.combine

Combine Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.combine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} replace the two or more selected slices with one user slice over their bounds (the first one's options; object slices are released) → {id}
```

## object.slice.divide

Divide Slices…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.divide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{rows?: slices down, rowHeight?: pt per slice, columns?: slices across, columnWidth?: pt per slice} cut each selected slice into a grid of user slices (evenly by count, or by size with a smaller last one; an object slice is released); the pieces are selected → {ids}
```

## object.slice.deleteAll

Delete All

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.deleteAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} delete every user slice and release every object slice → {count}
```

## object.slice.options

Slice Options…

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{kind?: "image"|"noImage"|"htmlText" (object slices of type only), name?, url?, target?, message?, alt?: (image), text?: cell text, HTML allowed (noImage), background?: ""|"matte"|"#rrggbb", hAlign?: "default"|"left"|"center"|"right", vAlign?: "default"|"top"|"middle"|"baseline"|"bottom"} set the selected slices' options as one undo step; no options: read them → the first slice's {kind, name, url, target, message, alt, text, background, hAlign, vAlign, htmlText: whether HTML Text applies}
```

## object.slice.clipToArtboard

Clip to Artboard

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.clipToArtboard`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{on?: bool} toggle (or set) Clip to Artboard: on, slices are clipped to the artboards and auto slices fill them; off, auto slices cover the art and the slices → {on}
```

## view.slices.hide

Hide Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.slices.hide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{hidden?: bool} toggle (or set) whether the canvas hides the slices (session view state) → {hidden}
```

## view.slices.lock

Lock Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.slices.lock`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{locked?: bool} toggle (or set) the slice lock: locked slices can't be selected or edited with the Slice Selection tool → {locked}
```

## slice.list

List Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} the slices as laid out, numbered left to right and top to bottom → {slices: [{number, id (null for auto slices), source: "user"|"object"|"auto", name, x, y, width, height, options, selected}], clipToArtboard, hidden, locked}
```

## select.object.slices

Slices

- 技能 / Owner: `vectorcraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object.slices`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} select every user and object slice → {count}
```

## object.slice.create

Create Slice

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{x, y, width, height} a user slice over that rectangle, selected (the Slice tool's drag) → {id}
```

## object.slice.setRect

Set Slice Rectangle

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.setRect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{id: user slice, x, y, width, height} move or resize a user slice (an object slice follows its object) → {id}
```

## object.slice.move

Move Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{slices?: [id…] (default: the selected slices), dx, dy} move the slices: user slices move, object slices move their objects → {ids}
```

## object.slice.delete

Delete Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{slices?: [id…] (default: the selected slices)} delete the user slices and release the object slices (their objects stay) → {count}
```

## object.slice.select

Select Slices

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe object.slice.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{slices?: [id…] (user slice ids or ids of objects with an object slice; none: deselect the slices), toggle?: bool (Shift: add the unselected ones, drop the selected ones)} select slices as the Slice Selection tool does; the objects are deselected → {selected: [id…]}
```

## file.open

Open…

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.open`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path} open any readable file (see document.formats) as a new document; templates open untitled
```

## file.save

Save

- 技能 / Owner: `vectorcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?, options?, svg?: {…SVG options}} = document.save: .vectorcraft, .ai (a PDF that reopens editable), .pdf, .svg or .svgz (default: the document's own path and format)
```

## file.export

Export…

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path?, format?, artboard?, range?, scale?, …} = document.export (no path → dataBase64)
```

## file.exportForScreens

Export for Screens…

- 技能 / Owner: `vectorcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportForScreens`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{folder?, zip?, artboards? | range? | fullDocument?, includeBleed?, subfolders?, preset?, formats?, settings?, prefix?} = document.exportForScreens (no folder → the files, or one zip, as dataBase64)
```

## tool.select

Select Tool

- 技能 / Owner: `vectorcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/vectorcraft-skills --skill vectorcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tool.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{tool} e.g. selection, directSelection, pen, rectangle, ellipse, polygon, star, lineSegment
```
