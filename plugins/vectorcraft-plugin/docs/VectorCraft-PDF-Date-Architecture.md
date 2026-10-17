# VectorCraft stable PDF export dates

ArtCraft's real mixed brand revision exposed a remaining first-use gap after SVG isolation: the unrelated SVG/PNG stayed identical, but PDF CreationDate/ModDate changed with the export clock. The old single-domain identity gate did not span different seconds. [Actual failure](evidence/mixed-pdf-date-failure-20261006.json).

```mermaid
flowchart TD
 A[Native document creation date] --> B{Date exists?}
 B -->|Yes| C[Bind native date]
 B -->|No| D{Verified previous date record?}
 D -->|Yes| E[Reuse hash-bound date]
 D -->|No| F[Record first delivery date]
 C --> G[Native PDF created option]
 E --> G
 F --> G
 G --> H[Stable PDF bytes when board content unchanged]
 G --> I[Source document and selection preserved]
```

The candidate CLI 0.2.0-craft.2 exposes the PDF encoder's existing `created` option as integer Unix seconds or null; invalid types fail and omitted/null retain legacy current-time defaults. The workflow records `pdf-export-date.json`, binds its digest into the delivery manifest and includes date/binding in PDF output records. A future revision verifies the prior date record and rejects tampering or a native-date binding mismatch. Native project creation dates and actual revision history remain in the editable project.

956 engine library tests pass, including explicit 2000-01-01 PDF date, identical repeated PDF bytes and invalid-type/source-preservation cases. The source suite passes 33 tests with 16 deliberate skips. The candidate single export skill installs an explicitly supplied local archive; revisions separated by 2.1 seconds preserve all unrelated SVG/PNG/PDF bytes and independently decoded PDF dates in 3.329 seconds. [Candidate evidence](evidence/pdf-export-date-candidate-20261006.json). This is not public CLI download or fixed new plugin evidence.

Public maintained runtime craft.1 and plugin dev.9 remain immutable. At candidate time, tasks 4.23 and ArtCraft 6.33 remained open pending distribution and installed mixed acceptance; the latest result below supersedes that pending status. Reproduction uses `tests/test_artboard_exports_first_use.py` and `tests/test_brand_token_mixed_first_use.py`; no normalization of PDF bytes replaces the identity gate.

Maintained runtime craft.2 is now published. Current working-tree skill installers pin it, and the single export skill passes actual public HTTPS cold installation plus cross-second/date-decoding gates in 7.228 seconds. Twelve CLI integration tests pass. At that working-tree verification stage, immutable skill/plugin and ArtCraft integration were still pending; the fixed released result below completes this bounded verification. [Public native evidence](evidence/pdf-export-date-public-runtime-20261006.json).

The fixed released acceptance now passes: ArtCraft dev.50 / skill dev.37 and VectorCraft dev.10 / skill dev.9 with native CLI 0.2.0-craft.2. All 58 installed hashes are preserved; actual cross-second PDF date binding and five-node mixed brand revision pass. Tasks 4.23 / 6.33 close at this bounded scope. [Evidence](evidence/codex-release50-vector10-stable-export-first-use-20261006.json). Historical candidate/failure evidence retains its original scope; complete V1 remains unfinished.
