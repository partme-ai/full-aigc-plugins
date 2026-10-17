# VectorCraft V1 — Release-Scope

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81VectorCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81VectorCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/VectorCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. V1 entrypoints

| Skill entry | Purpose | Status |
| :--- | :--- | :--- |
| vectorcraft-use | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-setup | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-inspect | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-paths | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-shapes | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-boolean | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-typography | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-artboards | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-variants | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-export | Maintained in independent skills; plugin pins snapshots | Planned |
| vectorcraft-recover | Maintained in independent skills; plugin pins snapshots | Planned |


## 2. Capabilities and gates

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Paths, shapes and coordinates | Define artboard coordinates, units, control points, path closure and strokes; preview pixels are not vector path authority. | Planned |
| Grouping and boolean operations | Record operand IDs, boolean operation and result identity with a pre-operation checkpoint; failure must not destroy source objects. | Planned |
| Brand colors and text | Bind brand colors using explicit tokens instead of global color replacement; retain text and font dependencies and report editability loss when outlining. | Planned |
| Artboards and variants | Give each artboard a stable ID, name, size and output mapping; define preview ordering and export ranges without index-base ambiguity. | Planned |
| Interchange fidelity scope | Validate native .vectorcraft, SVG, PDF and PNG separately; report rasterized effects and keep native sources when interchange cannot preserve them. | Planned |
| Brand variant revision | Update related variants from token and asset dependencies and verify that unrelated object properties and outputs remain unchanged. | Fixed56 six-scenario acceptance passed (macOS arm64; GUI/model separate) |


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

Actual public61/source43 installed on Codex0.153.4 macOS arm64 qualifies all three current VC-QA-001 scenarios and19 native boundaries. Three real decodes pass; maximal-score QA receipts cannot override corrupt PNG/PDF/SVG; real missing decoders stay NOT_RUN. File/checker drift, shared budget before snapshots, timeout stop and coordinator SIGKILL/restart without replay pass.13 skill digests remain unchanged.12 evidence tests reject11 rehashed omissions/tamper cases. Task6.3 closes;116/127 complete,11 open. Actual creative judgment,GUI,other platforms,6.6 and full V1 remain separate. [Evidence](../../../../docs/evidence/vectorcraft-quality-fixed61-20261009.json).
