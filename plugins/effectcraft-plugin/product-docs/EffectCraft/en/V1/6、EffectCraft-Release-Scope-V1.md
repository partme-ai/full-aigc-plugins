# EffectCraft V1 — Release-Scope

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81EffectCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81EffectCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/EffectCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. V1 entrypoints

| Skill entry | Purpose | Status |
| :--- | :--- | :--- |
| effectcraft-use | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-setup | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-inspect | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-composition | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-layers | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-animation | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-effects | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-masks | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-preview | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-export | Maintained in independent skills; plugin pins snapshots | Planned |
| effectcraft-recover | Maintained in independent skills; plugin pins snapshots | Planned |


## 2. Capabilities and gates

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Composition creation and range | Set composition dimensions, frame rate, duration and work area explicitly; convert time units according to the verified adapter contract. | Planned |
| Layers and footage dependencies | Maintain layer IDs, order, parenting, footage references and visibility; detect parent cycles and missing footage. | Planned |
| Text, graphics and keyframes | Record text, transforms and keyframes by property path with interpolation; text revision must not rebuild unrelated animation. | Planned |
| Effect and mask capability matching | Discover commands and parameter schemas before applying effects or masks; reject unsupported parameters before execution rather than skipping them. | Planned |
| Alpha and color handoff | Record color space, bit depth, alpha interpretation and codec during handoff; verify transparency from actual pixels or channel inspection. | Planned |
| Project and render delivery | Reopen .ecproj to inspect layers and keyframes; bind renders to composition revisions and report editability lost by baking. | Planned |


## 3. Release partition

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |


## 4. Scope change rule

Add capability rows, risks and acceptance fixtures before specifying more effects, formats, platforms or providers. Changing export formats cannot bypass required native delivery.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
