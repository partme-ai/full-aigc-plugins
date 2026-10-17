# VectorCraft — Technical-Plan

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81VectorCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81VectorCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/VectorCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

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

`vectorcraft-skills` is an independent published knowledge repository. The plugin vendors source tag `v0.1.0-dev.3`, a fixed commit and the full skill digest recorded in `skills.lock.json`. SKILL.md, references and portable scripts remain owned by the skill repository. `python3 scripts/vendor/skill_vendor.py check --offline` verifies the packaged snapshot; a source release does not imply complete host or creative acceptance.

| Stage | Input | Failure rule |
| :--- | :--- | :--- |
| resolve | repository + immutable tag | Stop on unresolved tags or disallowed provenance |
| verify | commit + tree digests | Reject any content drift |
| package | skills inventory | Reject escaping links and duplicate names |
| audit | clean install fixture | Standalone skill installs must resolve public dependencies |

## 3. Domain plan compilation strategy

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Paths, shapes and coordinates | Define artboard coordinates, units, control points, path closure and strokes; preview pixels are not vector path authority. | Planned |
| Grouping and boolean operations | Record operand IDs, boolean operation and result identity with a pre-operation checkpoint; failure must not destroy source objects. | Planned |
| Brand colors and text | Bind brand colors using explicit tokens instead of global color replacement; retain text and font dependencies and report editability loss when outlining. | Planned |
| Artboards and variants | Give each artboard a stable ID, name, size and output mapping; define preview ordering and export ranges without index-base ambiguity. | Planned |
| Interchange fidelity scope | Validate native .vectorcraft, SVG, PDF and PNG separately; report rasterized effects and keep native sources when interchange cannot preserve them. | Planned |
| Brand variant revision | Update related variants from token and asset dependencies and verify that unrelated object properties and outputs remain unchanged. | Fixed56 six-scenario acceptance passed (macOS arm64; GUI/model separate) |

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
| native | Create logo and icon assets in .vectorcraft, SVG and PNG; change a brand color and update bound variants while preserving unrelated colors. | project reopen + output inspection |
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

Snapshot `0.1.0-dev.2` has scoped installation/discovery and installed-entrypoint evidence. See [verification contracts and exclusions](../../../docs/VectorCraft-Host-Verification-Architecture.md). Full release tasks remain open; target design sections do not constitute implementation evidence.

## CLI skill suite revision

[VectorCraft CLI / setup / task suite](../../../docs/VectorCraft-Skill-Suite-Architecture.md)


## Default runtime capability probing progress

Ordinary Harness execution now validates fixed installation, version/digest and command/tool schemas before editing. Same-version concurrent tasks reuse selection; original keys inspect receipts without replay. Different selections are not implicitly upgraded. See [runtime gate implementation](../../../docs/Runtime-Gate.md). Published plugin41 remains unchanged; full task2.6 different-version upgrades/rollback and desktop acceptance remain open.

Public plugin43/source37 completed all seven current VC-RT-002 scenarios and task2.6: real version/bridge drain, activation races, native upgrade/rollback reopen, cold default and schema3 old-reader budget preservation. See [fixed-install evidence](../../../docs/evidence/vectorcraft-runtime-upgrade-fixed43-20261008.json). This supersedes earlier candidate-stage2.6 open statements;33 other tasks and full V1 remain open.

Both VC-RL-001 scenarios pass. A readonly release-owner gate checks plugin structure,independent skill source,runtime,host load,real task and native delivery separately. Twelve target tests first fail for the missing behavior and then pass;four semantic evidence tests also pass. In an actual isolated package,documentation and OpenSpec pass while documentation-only attestations still fail the release gate,retaining prior bounded records. Unchanged public63/source43 installation,six native revisions and owned-desktop evidence are reused with current digest checks;this turn adds no native or model run. Tasks7.1–7.3 complete,120/127 complete and7 open;marketplaceEligible stays false and supportedPluginHosts stays empty. Permissions/secrets,all commands,model routing,full distribution and actual creative review remain separate. [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-release-gate-20261009.json).

Permissions and secrets remain in progress. A local candidate filters inherited environments at seven subprocess entry points,withholds raw child diagnostics,rejects extra asset instruction fields and explicitly named literal credential fields,and refuses to persist those credentials in rejected-review audit events. Eight targeted tests and132 Node regressions pass;146 Python tests pass. An actual native revision and subsequent technical check consume four shared attempts,and owned groups stop. This candidate has no new public fixed distribution or completed host secret-reference contract;tasks7.4–7.6 remain open,120/127 complete and7 open. Published63/source43 stay unchanged;old release evidence cannot authorize the modified worktree. The named-field check does not claim arbitrary secret detection in document text. [Evidence](../../../docs/evidence/vectorcraft-permissions-candidate-20261009.json).

Candidate64 pins public source44(e5f8e1bb8528),preserving immutable63/source43. Source44 passes183 regressions with30 skips,six target tests and13 real independent cold installs. Candidate plugin132 Node and146 Python regressions pass;actual native revision and subsequent technical checking consume four shared attempts and stop owned groups. Source44 main/tag CI pass. Plugin64 has no public fixed qualification yet;host secret references,complete permission entry-point audit and all VC-RL-002 scenarios remain pending. Tasks7.4–7.6 remain open,120/127 complete and7 open. [Evidence](../../../docs/evidence/vectorcraft-permissions-integration-candidate64-20261009.json).

Candidate64 now pins public source45(a4b1e624818f). Source45 passes28 permission targets,193 regressions with48 skips,13 real independent cold installs,and actual native revision/three exports/reopen,including signed GUI persistence and direct kernel refusals without Python prechecks. Current plugin132 Node/146 Python regressions and native revision/check pass within four shared attempts with all owned groups stopped. Original source44 snapshot and execution bytes are archived. Python asset preflight authorization,real host secret references and fixed64 permission acceptance remain open:120/127 complete,7 open,candidate64 unpublished,no V1 or marketplace qualification. [Evidence](../../../docs/evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json).

Source46 is now pinned in unpublished candidate64. Current tests cover trusted Python asset reads,descriptor-safe copies,13 standalone cold starts,28 native permission cases and actual managed asset create/inherit with six exports. Node parent preflight audit,host secret references and fixed64 release qualification remain open; no new task closes.

Node parent asset hashing now uses the pinned descriptor reader under frozen roots; an actual ancestor replacement first failed,then passed.133 Node/146 Python tests and managed native create/inherit pass. Remaining root audit,secrets and fixed qualification stay open.

VC-QA-003 both current scenarios and task9.21 are verified through current-conversation actual multi-size review,one native local revision and strict persisted rejection/restart guards.135 Node and154 Python regressions passed before the final evidence-only audit. Creative acceptance is pending; six tasks and fixed distribution remain open.

Review-read increment: authorize the technical manifest before content access; intersect frozen request and store roots during capture. The pinned descriptor reader returns bytes and a digest with the existing64MiB capture limit, while streaming review fingerprints add no input size limit. Checked identity includes asset_reader.py,asset_digest.py and authorized_file.ts; dependency drift invalidates old reviews. Complete parent read/write audit,host secret references and fixed distribution remain open.

Controller reads: authorized capture for plans/source manifests; descriptor-streamed fingerprints for source projects and guarded inputs without a new source-file size cap. Runtime freshness checks batch up to4096 paths per helper process. Content capture has an explicit64MiB limit; a65MiB source still hashes successfully. Source snapshot copying,delivery inspection,parent writes,host secret references and fixed release require separate acceptance.

Delivery verification captures the manifest within frozen roots and batches authorized artifact digests. Geometry uses JSON whose actual digest must still match the manifest. A process-local WeakMap binds the checked manifest bytes without adding a forgeable proof field; both new and resumed receipts safely recheck the manifest before acceptance. Source snapshots,parent writes and fixed release remain separate acceptance gates.


Source snapshot copy increment: stream pinned source descriptors within frozen roots and match the bound digest. Destination parents use O_NOFOLLOW; exclusive creation preserves existing files,failed copies remove only newly created files,and successful snapshots are readonly and fsynced. Projects above64MiB remain supported. Source swaps,digest drift and destination link/scope/existence guards pass. Remaining parent writes,host secret references and fixed distribution stay open;7.4–7.6 remain unchecked,121/127 tasks complete,6 open. [Evidence](../../../docs/evidence/vectorcraft-permissions-source-copy-candidate64-20261009.json).


Controller content-write increment: persist state,plan,event and control files through frozen directory descriptors,per-component O_NOFOLLOW,exclusive creation and fsync. State updates use random temporary names and atomic replacement relative to the same held directory; old.next links are not followed. Event identity and control digest bind held files/input bytes without path rereads. Two baseline failures,five new boundary tests,16 targeted tests,158 Node cases and actual native revision pass. Directory creation,skill tree copying,other parent writers,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](../../../docs/evidence/vectorcraft-permissions-state-write-candidate64-20261009.json).


Controller directory/tree increment: snapshot directory creation,pinned skill copying and source snapshot digests now hold directory descriptors with per-component O_NOFOLLOW. Creation stays inside frozen roots; exclusive targets preserve existing data. Digests bind copied bytes with compatible UTF-16 path sorting,binary content,executable modes and empty directories. Source changes,links,invalid types and digest drift are refused; partial files remain inside the private root for inspection. Two original external-effect failures are fixed;19 targeted tests,163 Node cases and actual native revision/four-attempt stop pass. Earlier race tests now inject at the same descriptor-operation boundary;original bytes are archived. Other parent/database writes,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](../../../docs/evidence/vectorcraft-permissions-tree-write-candidate64-20261009.json).


Technical-review write increment: freeze request data and write roots before decode. Output,delivery and checker snapshots use descriptor-bound directories and exclusive readonly writes;report receipts bind the verified write digest. Checker snapshot hashes use safe batch reads. Checker identity expands from6 to10 files with four write/directory adapters;dependency drift invalidates old receipts. Three external-write failures and one async request mutation failure are fixed;21 targeted tests,171 Node cases and actual native revision/four-attempt stop pass. Database/backup paths,launch boundaries,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](../../../docs/evidence/vectorcraft-permissions-technical-write-candidate64-20261009.json).


Ledger backup/read increment: VACUUM INTO writes a random host-private staging directory,then validates schema/digest and publishes an exclusive readonly400,fsynced backup through safe descriptors. The final digest is checked inside the frozen backup root. Cleanup ownership starts after exclusive directory creation;cleanup failures close the connection and stop migration. Ledger verification hashes only within the task frozen output. One external backup write and two external verification reads are fixed;11 targeted tests and176 Node cases pass,including real SQLite v1/v2,committed uncheckpointed WAL,budgets and runtime selection. Actual native revision/four-attempt stop passes on fresh schema3;this is not a legacy native-state migration. Primary database/SQLite scratch paths,launch boundaries,host secret references and fixed distribution remain open;7.4–7.6 stay unchecked,121/127 tasks complete,6 open. [Evidence](../../../docs/evidence/vectorcraft-permissions-backup-write-candidate64-20261009.json).
