# VectorCraft V1 — Requirements-Analysis

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81VectorCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81VectorCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/VectorCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. User stories

| Role | Need | Completion condition |
| :--- | :--- | :--- |
| Creator | Editable vector brand assets and multi-artboard design | Create logo and icon assets in .vectorcraft, SVG and PNG; change a brand color and update bound variants while preserving unrelated colors. |
| Reviewer | Inspect the current revision and localized findings | Every finding points to an object or frame |
| Maintainer | Diagnose and recover failures | Runtime identity, state ledger and reusable checkpoints exist |


## 2. Requirement analysis and acceptance mapping

| ID | Requirement | Behavior summary | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| VC-SK-001 | Canonical independent skills | Only immutable skill snapshots may be packaged. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| VC-SK-002 | Standalone skills and dependencies | Standalone distribution must declare executable dependencies. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| VC-RT-001 | Runtime provenance and integrity | Install verified, versioned runtime artifacts atomically. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| VC-RT-002 | Capabilities and isolated upgrades | Version, commands and execution mode are distinct compatibility gates. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| VC-TX-001 | Revision binding and single writer | Reject stale plans and concurrent native-project writers. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| VC-TX-002 | Idempotency and unknown outcome recovery | An acknowledgement or timeout does not establish completion or failure. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| VC-TX-003 | Cancellation and bounded execution | Cancellation requests require execution-side confirmation. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| VC-AR-001 | Artifact lineage and bundle integrity | Paths alone are insufficient evidence of artifact identity. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| VC-AR-002 | Native editability and interchange loss | Preview success cannot prove native editability. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| VC-QA-001 | Separate technical and creative evidence | Each quality claim must identify its evidence and scope. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| VC-QA-002 | Bounded targeted revision | Revisions must target evidence-backed findings within a bounded budget. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| VC-RL-001 | Host and release evidence | Release readiness requires actual host and task evidence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| VC-RL-002 | Permissions and secret boundaries | Reject path escape, unsafe arguments and secret persistence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| VC-DM-001 | Paths, shapes and coordinates | Define artboard coordinates, units, control points, path closure and strokes; preview pixels are not vector path authority. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-002 | Grouping and boolean operations | Record operand IDs, boolean operation and result identity with a pre-operation checkpoint; failure must not destroy source objects. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-003 | Brand colors and text | Bind brand colors using explicit tokens instead of global color replacement; retain text and font dependencies and report editability loss when outlining. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-004 | Artboards and variants | Give each artboard a stable ID, name, size and output mapping; define preview ordering and export ranges without index-base ambiguity. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-005 | Interchange fidelity scope | Validate native .vectorcraft, SVG, PDF and PNG separately; report rasterized effects and keep native sources when interchange cannot preserve them. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| VC-DM-006 | Brand variant revision | Update related variants from token and asset dependencies and verify that unrelated object properties and outputs remain unchanged. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. Conflict handling

When format, budget or asset permissions conflict, preserve explicit user constraints and block dependent steps while allowing independent inspection. Changes create new revisions and compute invalidation, rather than overwriting old plans and acceptance.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.


VC-AR-001 qualification: all current three scenarios passed on public58/source43, Codex0.153.4 macOS arm64. Native move/reopen, parent revision, registered dependencies and tamper refusals are verified; external editor fidelity, creative and other platforms are separate. [Evidence](../../../../docs/evidence/vectorcraft-lineage-fixed58-20261009.json).


VC-AR-002 qualification: all current three scenarios pass on actual public59/source43 Codex0.153.4 macOS arm64. Native text and freeform gradients remain editable; SVG/PDF/PNG losses and20 refusals are verified. GUI,creative and external editor fidelity remain separate. [Evidence](../../../../docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json).
