# VectorCraft Asset Handoff Architecture

## Authority and current stage

Behavior is owned by `VC-DM-007` in the existing OpenSpec change. Independent `vectorcraft-skills` owns implementation. Plugin dev.11 vendors immutable skill source dev.10, which includes the implemented candidate. Installed-host repetition and the ArtCraft distribution upgrade are separate acceptance steps; the historical candidate evidence is retained.

## Problem and native boundaries

The public helper previously could create shapes but could not consume registered media. ArtCraft rejected every VectorCraft asset binding. The pinned maintained CLI `0.2.0-craft.2` already exposes file.place, links.relink, links.placementOptions and file.package; the new workflow uses those native commands.

Supported inputs are bounded PNG, JPEG and self-contained SVG, detected by content. SVG becomes editable embedded vector groups. Raster inputs default to linked image objects; explicit link=false embeds pixels. External SVG references, DTD/entities, scripts, foreignObject and external CSS URLs are rejected, rather than consumed without registration. Each input is at most 64 MiB. This does not claim every format that upstream file.place can read.

## Installation and execution

Each skill carries its own scripts, examples and references. Resolve SKILL_DIR from the actual host-loaded skill. No sibling installation or hard-coded mount is needed.

```mermaid
flowchart LR
    I[Registered input and digest] --> P[Preflight before installation]
    P --> B[Pinned native CLI bootstrap]
    B --> C[Copy and rehash input]
    C --> N[Native place or relink]
    N --> K[Native package: Links and Fonts]
    K --> O[Independent reopen and link check]
    O --> E[Export and hash delivery]
    E --> A[ArtCraft dependency verification]
```

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/provided-assets.json" \
  --asset product=/absolute/product.png \
  --asset logo=/absolute/logo.svg \
  --output /absolute/brand-v1
```

## Operation contract

| Operation | Parameters | Native behavior |
| --- | --- | --- |
| asset.place | asset; optional at, rect, link | file.place with an internally resolved collected path |
| asset.replace | asset, replacement | links.relink for raster-to-raster; file.place replace for vector groups |

at and rect are mutually exclusive. Dimensions must be positive; coordinates finite. Arbitrary path, folder or base64 parameters are not accepted. The same alias may be placed multiple times; IDs are accumulated. A single alias cannot mix linked and embedded instances.

Raster replacement sets preserve=bounds and keeps image IDs. Embedded raster remains embedded. Each SVG group instance is separately replaced in its existing stacking position and bounds; new IDs are explicit and existing $ref bindings are updated. Consumers must use current bindings rather than stale hard-coded group IDs.

## Delivery and relocation

file.package collects linked files into Links and embeddable fonts into Fonts. Original embedded inputs are retained in Assets. Missing links fail publication. Unavailable or non-embeddable fonts are recorded as skippedFonts; a font record is not a promise that the font will work on another machine.

manifest.assets contains path, sha256, format, ids, linked and warnings. manifest.files recursively covers dependency files. Source revisions inherit and rehash registered dependencies before native editing. Export takes place from the collected project, after independent reopen and links.check.

Native links can retain an engine-generated original path as metadata; package-relative paths support relocation. Public JSON records redact input and staging paths. The original path is not new filesystem authority. Hashes are checked again before publication. Failure publishes no new successful delivery and preserves the old source directory; no automatic replay follows ambiguous native failures.

## ArtCraft integration

The public adapter accepts logical assetBindings, derives --asset arguments from verified artifacts and checks collected file hashes. For asset.replace it verifies the new input under the explicit original alias. Retained assets must match the verified source manifest. The adapter does not accept model-supplied host paths or manufacture source lineage for unused inputs.

## Validation and remaining gates

`tests/test_asset_first_use.py` copies only the asset skill, downloads the pinned CLI into an empty runtime, places linked PNG and embedded SVG twice, replaces them with JPEG/SVG, checks output pixels, preserves unrelated objects and old files, moves the delivery and directly reopens native links. ArtCraft's `test/vector_asset_workflow.test.ts` checks Vector-to-Photo input, source replacement and selective reuse.

Fixed domain acceptance: plugin dev.11 / source dev.10 now passes installed single-skill native asset replacement and relocation, the multi-artboard export regression, and all 12 independent empty-runtime CLI starts. All 58 installed hashes are preserved. [Version-bound evidence](evidence/codex-vectorcraft11-assets-first-use-20261006.json). This closes the domain installation repetition only; ArtCraft distribution/mixed acceptance, model dispatch, GUI, full creative acceptance, other native input formats and cross-machine font fidelity remain open.

Fixed ArtCraft plugin dev.63 / skill source dev.43 / runtime dev.62 passes isolated Codex discovery (five plugins, 58 skills, zero errors), installed PNG/JPEG and SVG mixed first use (2 tests, 76.574s), four-domain regression (3 tests, 116.076s), and ten Art independent cold CLI starts (133.395s). All 58 installed digests remain unchanged, five locked bundles rebuild identically and both public release archives match their file hashes. SVG rejection preserves its domain code; replacement changes only consumers, retains non-target pixels and independently verified PNG/PSD composites, and packages relocate. This closes the bounded fixed SVG handoff gate; SVG type metadata, dynamic transparent sequence and full V1/creative/model/GUI remain open. [Fixed evidence](evidence/codex-release63-svg-first-use-20261006.json).
