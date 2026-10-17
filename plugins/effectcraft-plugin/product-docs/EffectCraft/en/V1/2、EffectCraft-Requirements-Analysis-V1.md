# EffectCraft V1 — Requirements-Analysis

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81EffectCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81EffectCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/EffectCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. User stories

| Role | Need | Completion condition |
| :--- | :--- | :--- |
| Creator | Layer compositing, motion graphics and shot effects | Create a brand intro with a reopenable .ecproj and editor-ready render; edit its text while preserving other layers and animation curves. |
| Reviewer | Inspect the current revision and localized findings | Every finding points to an object or frame |
| Maintainer | Diagnose and recover failures | Runtime identity, state ledger and reusable checkpoints exist |


## 2. Requirement analysis and acceptance mapping

| ID | Requirement | Behavior summary | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| EC-SK-001 | Canonical independent skills | Only immutable skill snapshots may be packaged. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| EC-SK-002 | Standalone skills and dependencies | Standalone distribution must declare executable dependencies. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| EC-RT-001 | Runtime provenance and integrity | Install verified, versioned runtime artifacts atomically. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| EC-RT-002 | Capabilities and isolated upgrades | Version, commands and execution mode are distinct compatibility gates. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| EC-TX-001 | Revision binding and single writer | Reject stale plans and concurrent native-project writers. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| EC-TX-002 | Idempotency and unknown outcome recovery | An acknowledgement or timeout does not establish completion or failure. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| EC-TX-003 | Cancellation and bounded execution | Cancellation requests require execution-side confirmation. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| EC-AR-001 | Artifact lineage and bundle integrity | Paths alone are insufficient evidence of artifact identity. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| EC-AR-002 | Native editability and interchange loss | Preview success cannot prove native editability. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| EC-QA-001 | Separate technical and creative evidence | Each quality claim must identify its evidence and scope. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| EC-QA-002 | Bounded targeted revision | Revisions must target evidence-backed findings within a bounded budget. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| EC-RL-001 | Host and release evidence | Release readiness requires actual host and task evidence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| EC-RL-002 | Permissions and secret boundaries | Reject path escape, unsafe arguments and secret persistence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| EC-DM-001 | Composition creation and range | Set composition dimensions, frame rate, duration and work area explicitly; convert time units according to the verified adapter contract. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-002 | Layers and footage dependencies | Maintain layer IDs, order, parenting, footage references and visibility; detect parent cycles and missing footage. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-003 | Text, graphics and keyframes | Record text, transforms and keyframes by property path with interpolation; text revision must not rebuild unrelated animation. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-004 | Effect and mask capability matching | Discover commands and parameter schemas before applying effects or masks; reject unsupported parameters before execution rather than skipping them. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-005 | Alpha and color handoff | Record color space, bit depth, alpha interpretation and codec during handoff; verify transparency from actual pixels or channel inspection. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| EC-DM-006 | Project and render delivery | Reopen .ecproj to inspect layers and keyframes; bind renders to composition revisions and report editability lost by baking. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. Conflict handling

When format, budget or asset permissions conflict, preserve explicit user constraints and block dependent steps while allowing independent inspection. Changes create new revisions and compute invalidation, rather than overwriting old plans and acceptance.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
