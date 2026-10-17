# VectorCraft Host Verification Architecture

> Date: 2026-10-05. Development snapshot: 0.1.0-dev.2. This document explains scoped technical acceptance; OpenSpec remains the sole behavioral authority.

## 1. Boundaries and ownership

The plugin owns manifest, immutable skill snapshot, documentation and release evidence. The independent skill repository owns the public install/workflow scripts. ArtCraft owns the shared host verifier and `host-acceptance.lock.json`; domain repositories consume its evidence without redefining public protocols. Host tests use a new isolated configuration and never modify the user's normal Codex installation or credentials.

## 2. Verification flow

```mermaid
flowchart LR
 L[Fixed public tags and digests] --> V[Validate release lock]
 V --> H[New isolated host configuration]
 H --> I[Install five plugins]
 I --> D[Real app-server skills/list]
 D --> C[Manifest, source commit and whole-skill hash]
 C --> W[Installed public workflow tests]
 W --> E[Scoped evidence and exclusions]
```

## 3. Contracts and failure behavior

Each installed manifest digest, plugin version, skill source ref/commit and skill tree hash must match the lock. A matching skill name alone is insufficient. Invalid locks fail before creating host configuration. Existing output directories are refused. Load errors, disabled or duplicate skills, out-of-cache paths, symlinks and content drift fail verification. RPC waits are bounded; the verifier terminates its own app-server. Private cache paths and raw host state remain local; published evidence contains identities and scoped outcomes.

## 4. Evidence matrix

| Check | Codex 0.147.0 | Codex 0.153.4 |
| :--- | :--- | :--- |
| Five fixed-release installs and skill discovery | Passed | Passed |
| Installed ArtCraft first-use, revision, scheduler recovery and moved package | Passed | Passed |
| Four standalone native representative tasks | Passed | Not run separately |
| Agent model dispatch / desktop GUI | Not verified | Not verified |

ArtCraft workflows retain four native projects, update dependent outputs after Logo revision, preserve old native projects/audio, enforce revision budgets, adopt original attempts after scheduler termination and verify relocated delivery packages. Standalone tests cover the specific tasks recorded in the evidence. Derivatives retain hash-bound exchange-loss reports; counts and hashes do not prove visual fidelity or creative quality.

## 5. Repeatable verification and release gate

From the ArtCraft plugin checkout, choose an already installed Codex executable and a new output directory:

```bash
python3 -B scripts/verify_codex_host.py --codex <absolute-codex> \
  --lock <absolute-host-acceptance.lock.json> --output <absolute-new-directory>
CRAFT_HOST_TEST=1 CRAFT_CODEX_CLI=<absolute-codex> \
  python3 -B -m unittest discover -s tests -p test_codex_host.py -v
```

The online check downloads public releases. Six verifier tests passed, including content/manifest/source tampering and refusal to overwrite existing output. Native tests require the declared Python media dependencies and pinned official CLIs. `CRAFT_INSTALLED_SKILL_ROOT` selects a real installed skill cache in the independent repository's native test; imports disable bytecode writes to preserve snapshot identity.

At the recorded 0.1.0-dev.2 QA snapshot,runtime bundles,skill content and immutable tags were unchanged and RL-001 prerequisites remained unmet. Current task status follows the six-layer verification section below;`marketplaceEligible` remains false and `supportedPluginHosts` remains empty until full release requirements pass. See [evidence](evidence/codex-current-release.json) and [tasks](../openspec/changes/establish-v1-plugin/tasks.md).

## Current six-layer release verification

Both VC-RL-001 scenarios pass. A readonly release-owner gate checks plugin structure,independent skill source,runtime,host load,real task and native delivery separately. Twelve target tests first fail for the missing behavior and then pass;four semantic evidence tests also pass. In an actual isolated package,documentation and OpenSpec pass while documentation-only attestations still fail the release gate,retaining prior bounded records. Unchanged public63/source43 installation,six native revisions and owned-desktop evidence are reused with current digest checks;this turn adds no native or model run. Tasks7.1–7.3 complete,120/127 complete and7 open;marketplaceEligible stays false and supportedPluginHosts stays empty. Permissions/secrets,all commands,model routing,full distribution and actual creative review remain separate. [Evidence](evidence/vectorcraft-release-gate-20261009.json).

`python3 -I -B scripts/release_gate.py --require development`

`python3 -I -B scripts/release_gate.py --require marketplace`
