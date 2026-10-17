# Runtime capability and isolated selection

Public installed plugin43/source37 passed all seven current VC-RT-002 scenarios and task2.6 on declared macOS arm64. See [fixed-install evidence](evidence/vectorcraft-runtime-upgrade-fixed43-20261008.json). Unsupported platforms are refused; creative GUI, model routing, individual command execution and full V1 remain separate gates.

Selection belongs to one Harness ledger and does not take over user desktops or other ledgers. Controller executes headless by default: plan validation, pinned installation and actual schema probing precede editing intent. Different selections are never implicitly upgraded. Same-version tasks may initialize concurrently; existing keys inspect original receipts without replay. Ledger supports explicit executionMode=bridge bindings; Controller cannot substitute bridge for headless.

Use `node src/cli.ts runtime-probe DATABASE REQUEST.json`, `runtime-activate` for a fresh probe/selection or `runtime-status` with `{}`. Requests bind skill, expectedSkillSha256, executable, platform, python, requirements and stateSchemas for activation. Requirements fix mode, complete command params signatures and tool inputSchema. Missing capabilities and changed schemas are distinct refusals; expectations must not follow drift. Bridge requires explicit loopback. State compatibility is an explicit policy, never inferred from the native binary; current schema is3. Empty-document enabled flags never substitute for signatures; pinned skills still check current-session preconditions. The readonly process group is bounded by the task deadline and180 seconds, with no editing replay. Legacy ready tasks lacking capability fingerprints require reconciliation instead of automatic continuation.

Activation and task claim share SQLite write transactions. Ready/running/reconciling/cancel_requested tasks and unconfirmed registered groups block switching. Identical selection preserves rollback history. Opening schema1/2 first saves a readonly VACUUM INTO snapshot containing committed WAL, original schema and SHA256, then migrates atomically to schema3; backup failure prevents migration. Previous policies lacking schema3 must drain before reactivation. The previous reader refuses new schema3 connections; selected_runtime_writer also enforces mode/digest/state policy for already-open old connections. Refused transactions leave no new task or budget.

| Current scenario | Fixed-install evidence |
| --- | --- |
| Success and missing capabilities | Two actual CLI versions, drained upgrade/compatible rollback, native save/reopen, old selection retained on refusal |
| Download recovery and final errors | Actual public empty-cache installation; injected failure classification,15 installed bootstrap tests, identical bytes across13 skills |
| Mode/schema | Real headless and owned signed bridge, same-session command/tool signatures, version/digest and drift/substitution refusals |
| Drain/races | Live old CLI/registered bridge/unconfirmed groups refuse;8 two-process rounds cover both winning orders |
| Default entry | Plan-before-install, parallel tasks, readonly original key, drift refusal and complete artifact digests |
| State migration | Explicit schema1/2 fixtures preserve tasks and committed WAL selection/steps/budgets; old-reader new budget rolls back, linked backup destination refused |

Actual installed copies passed54 Node,43 Python and15 bootstrap tests;11 native cases,5 registered bridge cases,8 race rounds,5 default cases and a retained-open-reader budget fixture also passed. Constructed fixtures are not historical production database migrations. Native, injected-fault, host-discovery and creative assessment levels remain distinct. The [Chinese diagram](Runtime-Gate.zh-CN.md) describes the same flow.

Plugin42 and earlier reports retain their execution bytes and original conclusions. Archived source snapshots preserve their inputs; affected index entries are historical instead of rebound to new code.
