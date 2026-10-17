# VectorCraft V1 — PRD

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81VectorCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81VectorCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/VectorCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. Release goals and non-goals

Create logo and icon assets in .vectorcraft, SVG and PNG; change a brand color and update bound variants while preserving unrelated colors.

This PRD is a reading view; linked OpenSpec is the behavioral authority. Unimplemented features remain planned. V1 does not build a new editor or multi-tenant cloud.

## 2. Functional requirements

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


## 3. Non-functional requirements

Enforce one project writer, no added side effects for idempotent duplicates, no secrets in receipts, artifact-bound acceptance and detection of plan/GUI changes. Initial limits of three revision rounds and one render per project are unmeasured defaults, not performance results.

## 4. End-to-end acceptance procedure

1. Install locked runtimes and skills in a clean environment.
2. Register fixture assets and expected outputs.
3. Execute and verify native projects and exports.
4. Close and reopen native projects to inspect editability.
5. Apply the representative local change and compare untouched objects.
6. Inject interruption, recover and check for duplicate side effects.
7. Repeat in the target host and record its version.

## 5. Release gates

Every P0 requirement needs positive and negative evidence; unexecuted cases are NOT_RUN. Technical failures, native corruption, digest drift and duplicate submissions block release.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.


VC-AR-001 qualification: all current three scenarios passed on public58/source43, Codex0.153.4 macOS arm64. Native move/reopen, parent revision, registered dependencies and tamper refusals are verified; external editor fidelity, creative and other platforms are separate. [Evidence](../../../../docs/evidence/vectorcraft-lineage-fixed58-20261009.json).


VC-AR-002 qualification: all current three scenarios pass on actual public59/source43 Codex0.153.4 macOS arm64. Native text and freeform gradients remain editable; SVG/PDF/PNG losses and20 refusals are verified. GUI,creative and external editor fidelity remain separate. [Evidence](../../../../docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json).

Permissions and secrets remain in progress. A local candidate filters inherited environments at seven subprocess entry points,withholds raw child diagnostics,rejects extra asset instruction fields and explicitly named literal credential fields,and refuses to persist those credentials in rejected-review audit events. Eight targeted tests and132 Node regressions pass;146 Python tests pass. An actual native revision and subsequent technical check consume four shared attempts,and owned groups stop. This candidate has no new public fixed distribution or completed host secret-reference contract;tasks7.4–7.6 remain open,120/127 complete and7 open. Published63/source43 stay unchanged;old release evidence cannot authorize the modified worktree. The named-field check does not claim arbitrary secret detection in document text. [Evidence](../../../../docs/evidence/vectorcraft-permissions-candidate-20261009.json).

Candidate64 pins public source44(e5f8e1bb8528),preserving immutable63/source43. Source44 passes183 regressions with30 skips,six target tests and13 real independent cold installs. Candidate plugin132 Node and146 Python regressions pass;actual native revision and subsequent technical checking consume four shared attempts and stop owned groups. Source44 main/tag CI pass. Plugin64 has no public fixed qualification yet;host secret references,complete permission entry-point audit and all VC-RL-002 scenarios remain pending. Tasks7.4–7.6 remain open,120/127 complete and7 open. [Evidence](../../../../docs/evidence/vectorcraft-permissions-integration-candidate64-20261009.json).

Candidate64 now pins public source45(a4b1e624818f). Source45 passes28 permission targets,193 regressions with48 skips,13 real independent cold installs,and actual native revision/three exports/reopen,including signed GUI persistence and direct kernel refusals without Python prechecks. Current plugin132 Node/146 Python regressions and native revision/check pass within four shared attempts with all owned groups stopped. Original source44 snapshot and execution bytes are archived. Python asset preflight authorization,real host secret references and fixed64 permission acceptance remain open:120/127 complete,7 open,candidate64 unpublished,no V1 or marketplace qualification. [Evidence](../../../../docs/evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json).

Current candidate64/source46 verifies Python asset-root boundaries and actual native/managed asset creation and inherited revision. This is partial VC-RL-002 progress; Node parent audit,host secrets and fixed distribution remain pending.120/127 tasks complete,7 open; no V1 or marketplace qualification.

The parent initial asset read-after-check gap is fixed and verified by native managed creation/rework. VC-RL-002 remains partial; no additional tasks close or marketplace eligibility follows.

Task9.21 complete: actual current-agent review and one explicit native revision,with separate technical and creative conclusions. The green target passes but small text remains unresolved.121/127 tasks complete,6 open; no independent review,automatic loop,fixed installation,V1 or marketplace claim.
