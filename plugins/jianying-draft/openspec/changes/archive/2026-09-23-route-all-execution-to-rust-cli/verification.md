# Verification

## 2026-09-22 — real-host evidence hardening

- Added a fail-closed requirement that the thirteen production host checks cannot be represented by booleans alone.
- Every check now binds an evidence kind, timezone-aware observation timestamp, embedded host/command artifact, and canonical JSON SHA-256.
- The strengthened observation and run evidence contracts are versioned as v2; published v1 schema files remain byte-compatible historical definitions and are not accepted by the current recorder.
- The recorder and final validator both recompute every embedded artifact digest; missing, extra, malformed, or tampered check evidence is rejected.
- TDD RED evidence: three new tests showed the previous implementation accepted boolean-only and tampered check records.
- TDD GREEN evidence: targeted host evidence tests passed 13/13; complete Python regression passed 73/73.
- Published-bundle Node regression passed 311 with four explicitly conditional real-host/release skips and zero failures.
- `openspec validate route-all-execution-to-rust-cli --strict` and `git diff --check` passed.

This does not satisfy tasks 9.2 or 9.6. No Codex/ZCode/Kimi host is promoted until its formal installation produces all thirteen digest-bound observations; no JianYing GUI evidence was created in this increment.

## 2026-09-22 — v0.26.0 release candidate boundary

- Because v2 is a new public distribution contract, the repository-owned bump tool generated a local `v0.26.0` candidate instead of mutating the already published `v0.25.0` identity.
- Catalog, Codex/ZCode/Kimi manifests, repository marketplace, bilingual README and the pending host-acceptance identity were synchronized; no commit, push, tag or Release was created.
- Candidate verification: Python 74/74; Node 311 pass with four explicit real-host/release skips; distribution, marketplace synchronization, strict OpenSpec and diff checks pass.
- Readiness reports `ready=true`, `production_ready=false`, plugin identity `0.26.0+codex.20260922`, and host acceptance `pending`. This is a release candidate, not a published or installed production version.

## 2026-09-22 — remote prerequisite replay

- Read-only GitHub replay proves immutable CLI `v1.6.19` and Skills `v2.3.0` Releases and exact asset sets remain ready.
- Plugin immutable releases are enabled, but the private repository's tag ruleset API returns HTTP 403 because the current plan does not provide the feature; expected plugin `v0.26.0` is not published.
- The preflight now reports stable `feature_unavailable_for_plan` and `release_not_found` codes with explicit remediation options instead of opaque error text. TDD RED/GREEN passed; Python regression is 75/75.
- The release gate remains fail closed. No repository setting, tag, Release, commit or push was changed.

## 2026-09-22 — approved equivalent release protection

- The project owner explicitly approved `Immutable Release + tag commit verification before and after publication` as the equivalent gate when the private-repository plan does not expose tag rulesets.
- `runtime/release-protection-policy.json` records that approval and requires plugin Immutable Releases plus exact tag/checkout checks before Draft creation, before publication and after publication.
- The preflight validates the policy, the exact three workflow invocations and their order; missing, duplicate or reordered checks fail with `equivalent_policy_invalid`.
- Read-only remote replay now reports `prerequisitesReady=true`. The only remaining remote release item is `release.plugin.expected`, because immutable plugin `v0.26.0` has not been published.
- This supersedes the ruleset-plan blocker above; it does not satisfy real Release, installation, JianYing GUI or host-acceptance tasks. No remote state changed.

## 2026-09-22 — real JianYing cold reopen, playback and native export

- The owner had explicitly approved an isolated JianYing draft, cold reopen, continuous playback and native export.
- JianYing Pro `11.5.13243` (`11.6.0-beta2`) reopened `园区招商概念验收样片-20260922` after a real editor close; the timeline remained 13 seconds with its video, text, music and transition state.
- Playback ran from `00:00:00:00` to `00:00:13:00` and stopped naturally.
- Local native export was invoked through `File -> Export`, not the title-bar cloud-share action. JianYing reported success and produced a new MOV plus MP3 under `.../final/园区招商概念验收样片-20260922(2)`.
- Independent `ffprobe` verification reports H.264 + AAC, 1080x1920, 30 fps, 13.000 seconds. The MOV SHA-256 is `1febdad07d2e82a44fe74b0ce7c6825b4b3d1d3b9812d859278e083c2c9c0608`.
- Detailed GUI operation evidence and remaining fail-closed boundaries are recorded in `docs/video-harness/JIANYING_GUI_OPERATION_ACCEPTANCE_20260922.md`.

This satisfies task 9.2. It does not satisfy task 9.6, human narrative/audio approval, Windows JianYing, remote paid providers, or formal three-host installation evidence.

## 2026-09-23 — immutable v0.26.1 formal host acceptance

- Codex 0.153.4, ZCode 0.16.9 and Kimi 0.43.1 loaded formal `jianying-draft v0.26.1` packages in isolated host homes. Kimi consumed the exact immutable GitHub Release archive after verifying SHA-256; no development checkout or model call was used.
- All three hosts used the checksum-pinned `jianying-cli v1.6.24` release binary and `jianying-skills v2.3.0` lock. A shared real CLI Job first passed the existing cross-host black-box test, then each host independently produced all thirteen digest-bound v2 observations.
- The canonical Job input SHA-256 is `0d6e504997e2e4d5e61bb29d81a0f8234ca5547fb2301b5e6fdc25d6d8e4703b`; the normalized semantic result SHA-256 is `328eb56f8716ad9e22deee15fa5ef84c6d2753e42bc505bf1391ca1bfcb27349` for every host.
- `runtime/host-acceptance.json` is now `passed`; the host validator, release readiness (`production_ready=true`) and release distribution validator pass. The test that formerly assumed the runtime summary was permanently pending now validates both legal states and fully revalidates current passed evidence.

This clears the formal three-host prerequisite for task 9.6. Removing the final migration-only `JIANYING_HEADLESS_ROOT` diagnostic remains a separate code change and is not claimed by this evidence alone.

## 2026-09-23 — immutable v0.26.2 Rust-only cutover acceptance

- GitHub Actions run `35759849290` completed successfully across contract, Windows x64, macOS ARM64, macOS Intel, aggregate evidence and publish jobs.
- Release `v0.26.2` is immutable. Its GitHub release attestation validates the tag object and all seven assets; the annotated tag peels to source commit `7b699cd9c009fd1e8f55234cfb3fab3d8dfafd53`.
- Codex installed `0.26.2+codex.20260923` from the published marketplace ref `v0.26.2`; ZCode installed `0.26.2` from the same marketplace; Kimi imported the exact immutable source archive after verifying SHA-256 `0120572a68509b482c0b789a6f6fbdd756eb92d6f0b2d4614fc8dbeb583be09f`.
- Each isolated host installation independently passed doctor, 24-skill discovery, single-skill resolution, 13-category/106-action routing, VG01 planning explanation, exact approval, Job v2 execution, stop, conflict recovery, evidence display and native-export target approval without performing export.
- The installed-host cross-check executed the same released binary and Job through all three plugin roots and confirmed equivalent semantics. Canonical Job input SHA-256 is `e51cda22bc2be0034d04e59a301a56b58f0472f6f29e1cba746b02a3c44d9dfc`; result semantic SHA-256 is `328eb56f8716ad9e22deee15fa5ef84c6d2753e42bc505bf1391ca1bfcb27349`.
- `runtime/host-acceptance.json` is `passed`; host validation and release readiness report `production_ready=true` with no blockers.
- The runtime compatibility helpers and one-time cutover workflow were removed before this release. Active scripts contain no `JIANYING_HEADLESS_ROOT` read and no Python/external-fork execution route; remaining names occur only in negative validators, tests, legal notices or historical migration records.

This satisfies tasks 8.3 and 9.6. It does not promote separate smart-package, paid digital-human/provider, Windows JianYing GUI, course or wedding human-review gates in other OpenSpec changes.
