# jianying-draft namespace migration (2026-10)

Three repositories describe three layers: the engine, the shared skill library
and the host plugin. Two product lines share the skill library — the headless
draft line and the visible `jianyingcraft` editor — so a bare `jianying-` prefix
no longer said which line a skill belonged to. This page records what moved and
how each step was verified.

| Layer | Before | After |
|---|---|---|
| Skills package | `jianying-skills` (24 skills, `jianying-<x>`) | `jianying-skills` (24 skills, `jianying-draft-<x>`) |
| Engine | `full-aigc-plugins/jianying-cli` | `full-aigc-plugins/jianying-draft` |
| Plugin | `full-aigc-plugins/jianying-edit-plugin`, id `jianying-edit` | `full-aigc-plugins/jianying-draft-plugin`, id `jianying-draft` |

Binary, crate names and release asset names are unchanged (`jianying`,
`jianying-cli-<version>-<platform>`), so existing installs keep working.

## A — skills 2.4.0

Commits: `6066018` (rename), `32a6eda` + `ee6d09c` (cross-platform digest),
`f3a235b`/`ebfd915` (consumer dispatch target).

- 24 skill directories renamed in place; `jianying-draft` (schema skill) became
  `jianying-draft-schema`, `jianying-use` became `jianying-draft-use`
- 204 files, 2396/2396 lines — symmetric churn, nothing but names moved
- the frozen v1 baseline (`tests/fixtures/legacy_planning_v1.json`) re-froze 110
  of 113 entries, because those files embed skill names
- manifest re-rendered, `content_sha256` recomputed, version 2.4.0

Two defects were found while getting this through CI:

1. `hash_skill_dir` digested raw bytes, so a CRLF checkout and an LF checkout of
   the same commit produced different digests → normalise `\r\n` first.
2. the same function sorted `Path` objects. Windows compares casefolded, POSIX
   compares bytes, so `SKILL.md` landed in a different position on each platform
   → sort by the relative POSIX path string instead.

The second one is proven by parity: after the fix the local digest `5e476c71…`
equals the value the Linux runner had been computing all along.

Gates (re-runnable):

```bash
python scripts/lint_skills.py
python -m unittest discover -s tests -q
python scripts/skill_manifest.py check
```

Result: 24 skills, 0 lint errors, 85 tests pass (2 skipped), `skill-lint` green
on `main`; `v2.4.0` published with `jianying-skills.manifest.json`.

## B — plugin 0.29.0

Commits: `95d2c0a` (rename + re-vendor), `491e317`/`fe51c3b` (distribution and
gates), `66c5f0b` (hook), `7394720` (skill paths), `907d442` (planner digest),
`c8997cd` (v1 baseline), `3b00df9`/`44fc2d6` (catalog schema), `023f1ef`
(name literals), `02973ad` (local entry skill).

- id and repository renamed; marketplace entry, dsh identifiers and README
  badges follow
- `skills.lock.json` moved to v2.4.0; 23 skills are vendored and
  `jianying-draft-use` is declared in `localSkills` and owned by the plugin
- the vendor gate accepts local skills and rejects a name that is declared both
  locally and by a source package (that would silently shadow content)
- the session hook runs the documented `doctor` handshake
- release readiness hashes skill content with the canonical rule
- version 0.29.0; host acceptance reset to pending for 0.29.0

Gates (re-runnable):

```bash
python scripts/validate_distribution.py
python -m unittest discover -s tests -q
python scripts/vendor/skill_vendor.py check --offline
python scripts/release_readiness.py
```

Result: `ci`, `skills-check` and `Partme Agent Plugin Architecture v1` all green
on `main`; readiness `ready: true` with `production_ready: false` (pending host
acceptance, unchanged from before the migration).

## C — engine 1.7.0

Commits: `c8cc505` (version + repository constants + SBOM locale),
`76d0271` (plugin follows the rename), `08ebd37` (lock 1.7.0).

- repository renamed to `full-aigc-plugins/jianying-draft`
- canonical repository constant, release index/preflight tools and docs updated
- `generate_sbom.py` decodes cargo output as UTF-8 explicitly: the previous
  locale default made the SBOM step fail on a GBK console
- version 1.7.0 carries the tim sign parsing and draft text-effect fixes

Gates (re-runnable):

```bash
cargo test -j 2
python -m unittest tests.test_release_tools -q
```

Result: `ci` green, `release-artifacts` green for the three platforms, `v1.7.0`
published; the plugin imported its release index (`resolvedVersion 1.7.0`,
`sourceCommit c8cc505`) and its own `ci` is green again.

## Residual work

- The skills package still ships `jianying-draft-use`. The next skills release
  must drop it; until then the vendor gate fails on the duplicate declaration,
  which is the intended safety net.
- Host acceptance stays `pending`: it needs a real JianYing/Codex/ZCode/Kimi
  install, which this environment cannot provide.

## D — the entry skill changes hands (skills 2.5.0, plugin 0.29.4)

Phase A left `jianying-draft-use` in the package as a transition ("暂留包内").
Once the plugin owned its own copy, both declaring the same name would shadow
each other, and the vendor gate refused to import while that was true. So the
package dropped it.

Commits: `22d20d3` (skills 2.5.0), `48d51f0` (plugin 0.29.1 import),
`d053a25` (archive audit), `4e80600` (evidence count), `d43f2d9` (evidence test
fixture).

- package: 23 product skills; contract matrix drops the entry row; the other
  skills keep their "route to jianying-draft-use" guidance, which the host
  resolves
- importer: stages `localSkills` from the current tree before swapping `skills/`
  - without this the 2.5.0 import deleted the entry skill, because only upstream
  names were staged
- archive audit, release readiness and the evidence verifier now all count
  vendored + local skills (23 + 1 = 24)

Gates (re-runnable):

```bash
python scripts/lint_skills.py            # skills repo: 23 skills, 0 errors
python -m unittest discover -s tests -q  # 85 pass
python scripts/skill_manifest.py check   # 23 skills, digest verified
python scripts/validate_distribution.py  # plugin: 24 skills
python scripts/vendor/skill_vendor.py check --offline
python scripts/release_readiness.py     # ready: true
node --test tests/release_evidence.test.mjs  # 16/16
```

Result: skills `v2.5.0` published; plugin `v0.29.4` published with the full
release evidence (archive audit, three platform install canaries, readiness,
verification); marketplace catalog at 0.29.4.

Known residual: the skills `release-skills` workflow still ends red on its final
consumer-dispatch step — `FULL_AIGC_SKILLS_SYNC_TOKEN` gets HTTP 404 when
dispatching to `full-aigc-plugins/jianying-draft-plugin`, so the token needs
access to that repository. The release assets themselves are published (the
dispatch step runs after the upload).
