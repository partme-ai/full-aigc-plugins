# VectorCraft — Capabilities-and-Roadmap

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81VectorCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81VectorCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/VectorCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Capability entrypoints

| Entry | Purpose | Version |
| :--- | :--- | :--- |
| vectorcraft-use | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-setup | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-inspect | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-paths | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-shapes | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-boolean | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-typography | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-artboards | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-variants | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-export | Domain knowledge or workflow entry; currently planned | V1 |
| vectorcraft-recover | Domain knowledge or workflow entry; currently planned | V1 |


## 2. Functional scope

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Paths, shapes and coordinates | Define artboard coordinates, units, control points, path closure and strokes; preview pixels are not vector path authority. | Planned |
| Grouping and boolean operations | Record operand IDs, boolean operation and result identity with a pre-operation checkpoint; failure must not destroy source objects. | Planned |
| Brand colors and text | Bind brand colors using explicit tokens instead of global color replacement; retain text and font dependencies and report editability loss when outlining. | Planned |
| Artboards and variants | Give each artboard a stable ID, name, size and output mapping; define preview ordering and export ranges without index-base ambiguity. | Planned |
| Interchange fidelity scope | Validate native .vectorcraft, SVG, PDF and PNG separately; report rasterized effects and keep native sources when interchange cannot preserve them. | Planned |
| Brand variant revision | Update related variants from token and asset dependencies and verify that unrelated object properties and outputs remain unchanged. | Fixed56 six-scenario acceptance passed (macOS arm64; GUI/model separate) |


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
