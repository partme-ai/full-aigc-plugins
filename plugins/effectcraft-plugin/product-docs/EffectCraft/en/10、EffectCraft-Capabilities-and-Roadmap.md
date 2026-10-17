# EffectCraft — Capabilities-and-Roadmap

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81EffectCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81EffectCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/EffectCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Capability entrypoints

| Entry | Purpose | Version |
| :--- | :--- | :--- |
| effectcraft-use | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-setup | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-inspect | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-composition | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-layers | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-animation | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-effects | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-masks | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-preview | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-export | Domain knowledge or workflow entry; currently planned | V1 |
| effectcraft-recover | Domain knowledge or workflow entry; currently planned | V1 |


## 2. Functional scope

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Composition creation and range | Set composition dimensions, frame rate, duration and work area explicitly; convert time units according to the verified adapter contract. | Planned |
| Layers and footage dependencies | Maintain layer IDs, order, parenting, footage references and visibility; detect parent cycles and missing footage. | Planned |
| Text, graphics and keyframes | Record text, transforms and keyframes by property path with interpolation; text revision must not rebuild unrelated animation. | Planned |
| Effect and mask capability matching | Discover commands and parameter schemas before applying effects or masks; reject unsupported parameters before execution rather than skipping them. | Planned |
| Alpha and color handoff | Record color space, bit depth, alpha interpretation and codec during handoff; verify transparency from actual pixels or channel inspection. | Planned |
| Project and render delivery | Reopen .ecproj to inspect layers and keyframes; bind renders to composition revisions and report editability lost by baking. | Planned |


## 3. Navigation and routing

Route single-domain requests directly and mixed scenarios to ArtCraft. Inspect before execution and return bounded availability when capabilities are missing. Choose executors by requested native format, not silent substitution. Lifecycle operations are shared; concrete commands are adapter-specific.

## 4. Release cadence

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |




---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
