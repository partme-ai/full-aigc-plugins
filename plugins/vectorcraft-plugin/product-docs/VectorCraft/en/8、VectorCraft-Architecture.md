# VectorCraft — Architecture

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81VectorCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81VectorCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/VectorCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Cross-version architecture constraints

Dependencies flow from Skills through Harness and Runtime Adapter to Native CLI. Creative knowledge, execution state, native projects and cross-plugin projects have distinct owners. Upstream responses, model suggestions and user assets cannot directly advance acceptance state.

## 2. Layers and boundaries

| Component | Authoritative data | Must not own |
| :--- | :--- | :--- |
| Skills | Procedural knowledge, triggers and domain methods | Task state or secrets |
| Domain Harness | Domain plans, project revisions and child task ledger | Other plugins’ internal state |
| Runtime Adapter | Command mappings and capability snapshots | Changing creative goals |
| Native CLI | Native objects, edits and rendering | Cross-plugin project authority |
| ArtCraft | Brief, DAG, asset versions and aggregate delivery | Fabricating child success |


## 3. Deployment and data

V1 uses a local single-user workspace: read-only plugin packages, versioned runtimes and user-managed project state and assets. JSON receipts isolate language and host differences. SaaS, message brokers and distributed transactions are not dependencies.

## 4. Detailed design ownership

[Complete runtime architecture](../../../docs/VectorCraft-Runtime-Architecture.md)

The detailed architecture owns processes, states, interfaces, recovery, upgrade, resource budgets and operations. V1 architecture records only release scope and deltas. Change OpenSpec before external behavior; narrative documentation cannot silently alter contracts.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.


Actual public56/source42 isolated Codex0.153.4 installation qualifies all six current VC-DM-006 scenarios with13 unchanged skill digests. Two swatch routes,eight erroneous-update refusals,two raster and two SVG consumers,nine asset export decodes,three unchanged unrelated SVG/PDF/PNG outputs,unknown-token refusal and both linked-plan refusals pass. Failed checkpoints reopen independently without replay. Task4.18 closes:111 complete/16 open. GUI,model creative quality,other platforms,all formats,cross-file/external-editor behavior,Art bundled distribution and full V1 remain unverified.

Technical review freezes request and store read roots, captures files through the pinned descriptor reader within their intersection, and parses the manifest only after authorized access. Checked identity includes reader and adapter code. Other parent writes and host secret references remain separate acceptance gates.

```mermaid
flowchart LR
  A[Trusted read roots] --> B[Frozen root intersection]
  B --> C[Pinned descriptor reader]
  C --> D[Bytes and digest]
  D --> E[Technical decoder]
  C -->|Outside root or identity changed| F[Refuse before external bytes]
```
