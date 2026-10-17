# EffectCraft — Technical-Plan

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81EffectCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81EffectCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/EffectCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Technical decisions and alternatives

| ADR | Decision and rationale | Alternative and reversal condition |
| :--- | :--- | :--- |
| ADR-001 | Independent skills repositories with immutable snapshots inside plugin packages | Reject sibling symlinks; add host dependency resolution only after it is verified |
| ADR-002 | Reuse official Rust CLIs through controlled MCP/argv | Do not rewrite editors; surface missing APIs before adding adapters |
| ADR-003 | Target TypeScript and Node.js 24 LTS for orchestration, matching ecosystem experience | Pin patch versions and dependencies during implementation; design is not compatibility proof |
| ADR-004 | SQLite ledger and content-addressed files for a local single-user workspace | Revisit service storage only when multi-machine collaboration is required |
| ADR-005 | ArtCraft OpenSpec owns shared task and artifact protocols | Domain repositories own mappings and consumer tests, not competing field definitions |
| ADR-006 | Separate technical gates from creative review; preserve valid existing authorization | Do not require approval per call; obtain new authority only when scope changes |

## 2. Independent skill supply chain

`effectcraft-skills` is an independent published knowledge repository. The plugin vendors source tag `v0.1.0-dev.3`, a fixed commit and the full skill digest recorded in `skills.lock.json`. SKILL.md, references and portable scripts remain owned by the skill repository. `python3 scripts/vendor/skill_vendor.py check --offline` verifies the packaged snapshot; a source release does not imply complete host or creative acceptance.

| Stage | Input | Failure rule |
| :--- | :--- | :--- |
| resolve | repository + immutable tag | Stop on unresolved tags or disallowed provenance |
| verify | commit + tree digests | Reject any content drift |
| package | skills inventory | Reject escaping links and duplicate names |
| audit | clean install fixture | Standalone skill installs must resolve public dependencies |

## 3. Domain plan compilation strategy

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Composition creation and range | Set composition dimensions, frame rate, duration and work area explicitly; convert time units according to the verified adapter contract. | Planned |
| Layers and footage dependencies | Maintain layer IDs, order, parenting, footage references and visibility; detect parent cycles and missing footage. | Planned |
| Text, graphics and keyframes | Record text, transforms and keyframes by property path with interpolation; text revision must not rebuild unrelated animation. | Planned |
| Effect and mask capability matching | Discover commands and parameter schemas before applying effects or masks; reject unsupported parameters before execution rather than skipping them. | Planned |
| Alpha and color handoff | Record color space, bit depth, alpha interpretation and codec during handoff; verify transparency from actual pixels or channel inspection. | Planned |
| Project and render delivery | Reopen .ecproj to inspect layers and keyframes; bind renders to composition revisions and report editability lost by baking. | Planned |

The planner emits a declarative plan. The compiler validates command availability, fields, units and bounds, then emits typed operations. Inspect source objects to obtain real IDs first. Compilation records planHash and capabilitySnapshotHash and returns unsupported_mapping for unsupported operations; only verified mappings reach submission.

## 4. Runtime installation and management

Runtime management separates discover, verify, install, probe, activate, upgrade and rollback. Reuse compatible existing installs after verification. Pin download URLs and digests, reject archive traversal and escaping symlinks, and verify before execution. Versioned installs do not overwrite active binaries and preserve prior receipts. An untested platform is unverified; a universal ZIP does not prove every architecture works.

## 5. Submission, recovery and artifact protocol

Use persisted intent, idempotency keys and single-writer leases. Even synchronous CLIs without external task IDs require attempt IDs, process identity, checkpoints and expected outputs. After process failure, inspect projects and files rather than blindly rerunning. Reconciliation handles the gap between file creation and ledger registration. Validate native projects and exports separately; list non-redistributable dependencies and fonts with verifiable acquisition instructions.

## 6. Test plan and acceptance assets

| Layer | Required coverage | Evidence |
| :--- | :--- | :--- |
| contract | Missing/unknown fields, idempotency and revision conflicts | schema + fixture results |
| adapter | Real command discovery, mode differences and error mapping | runtime identity + transcript |
| recovery | Disconnect after submit, late results and unconfirmed cancellation | ledger before/after + duplicate count |
| native | Create a brand intro with a reopenable .ecproj and editor-ready render; edit its text while preserving other layers and animation curves. | project reopen + output inspection |
| host | Clean host install, upgrade and user-data preserving uninstall | host/version/platform + logs |

## 7. Implementation route

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |

Use dependency order without invented dates or effort estimates. Each OpenSpec task carries a requirement ID, owner role, output and validation. Start with failing behavior tests, implement minimally, and leave tasks unchecked until evidence exists.

## 8. Operations, upgrade and release

Plugin, skills, upstream CLI and protocol versions evolve independently. Release matrices pin their combinations; host manifests and marketplace metadata must match verified commits and locks. The documentation baseline ships no installable plugin package; M4 gates the first installable release. Roll back to a previously verified plugin/skills/CLI combination; restore backups when state migrations are incompatible.

---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.

Exchange delivery now includes exchange-loss.json binding native, reopened inspection and exports by digest. Derivatives never substitute for native projects; cross-editor font, effect and mask fidelity remains explicitly unknown until separate acceptance.

## Current host acceptance

Snapshot `0.1.0-dev.2` has scoped installation/discovery and installed-entrypoint evidence. See [verification contracts and exclusions](../../../docs/EffectCraft-Host-Verification-Architecture.md). Full release tasks remain open; target design sections do not constitute implementation evidence.

## CLI skill suite revision

[EffectCraft CLI / setup / task suite](../../../docs/EffectCraft-Skill-Suite-Architecture.md)
