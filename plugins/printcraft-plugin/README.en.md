# PdfCraft (PDF Toolkit)

> Inspect, edit, OCR, and deliver PDFs from a coding agent. Keep the original, then verify page order, geometry, and searchable text.

**Version**: 0.1.0-dev.20261109.4 · **License**: Apache-2.0 · **Skills**: 20 · **MCP server**: 1

[简体中文](README.md) · [Install](#installation) · [Quick start](#quick-start) · [Project layout](#project-layout)

## Positioning

PdfCraft is for users who need a PDF actually processed, not a generated script. It does not reimplement a PDF engine. It pins and verifies `pdfcraft-cli` 0.2.1 and combines 20 skills with a thin Harness for inspection, page operations, forms, redaction, OCR, bookmarks, print preflight, and an embedded editor.

Use it for:

- Reordering, rotating, deleting, splitting, and merging pages
- OCR and searchable-text checks for scans
- Filling, exporting, and reading back form fields
- Redaction, watermarks, and review copies
- Bookmarks, internal links, and tables of contents
- Print preflight and delivery verification

Do not use it for:

- Replacing professional layout software for complex design
- Editing documents without the original or explicit authorization
- Treating exit code 0 as delivery completion

## At a glance

```text
PDF / scans / forms
        │
        ▼
PdfCraft skill (inspect → plan → execute → read back)
        │
        ├── pdfcraft-cli (pinned native PDF operations)
        ├── OCR / Tesseract (scans only)
        └── MCP editor (in-browser review and local adjustment)
        │
        ▼
new file + receipt + page-level review
```

## Capabilities and boundaries

| Capability | What it does | Boundary |
|---|---|---|
| Inspect | Pages, metadata, text, scan/OCR state | Empty text is not a blank page |
| Page operations | Rotate, reorder, delete, split, merge | Write a new file; keep the original |
| Forms | Fill, export, read back values | Stop on missing or mismatched fields |
| Redaction | Remove specified regions or text | Exact scope and review required |
| OCR | Add a searchable text layer | Chinese OCR needs an explicit Tesseract backend |
| Bookmarks/links | TOC, bookmarks, internal jumps | Rebuild after page numbers change |
| Preflight | Page boxes, fonts, images, bleed | Not a substitute for the printer's final check |
| Editor | Open the workspace in a browser | Reopen and verify after saving |

## Architecture and core flow

```text
Host / agent
   │  invokes a skill
   ▼
skills/pdfcraft-*  ──►  skills/pdfcraft-harness
                              │
                              ▼
                     pdfcraft-cli 0.2.1
                              │
                              ▼
                     PDF output + receipt.json
                              │
                              ▼
                     reopen, page review, human check
```

Rules:

1. Inspect read-only, then plan, then execute.
2. Every write produces a new file; the original stays unchanged.
3. Exit code 0 means the command finished, not that delivery is complete; the state remains `REVIEW_REQUIRED`.
4. When the result is uncertain, mark it `UNKNOWN` and reconcile read-only; never replay automatically.

## Compatibility

| Item | Status |
|---|---|
| Verified installer | macOS arm64 |
| Upstream CLI native runs | Linux x64/arm64, Windows x64, macOS Intel/arm64 |
| Hosts | Codex has full install and model evidence; Claude Code, Gemini, OpenCode, and Kimi are NOT_RUN |
| Python | 3.11+ |
| Node.js | 24+ (editor) |
| Chinese OCR | Tesseract 5.5.3 + tessdata_fast 4.1.0 (recorded on macOS arm64) |

## Installation

### Prerequisites

- Python 3.11 or newer
- Node.js 24 or newer (editor only)
- Access to GitHub Releases for the pinned CLI

### From the marketplace

```bash
codex plugin marketplace add partme-ai/full-aigc-plugins
codex plugin add pdfcraft@full-aigc-plugins
```

Restart the host and start with a read-only request:

> Inspect this PDF: page count, metadata, text, and OCR status. Do not modify it.

## Quick start

1. **Inspect**: confirm pages, sizes, text layer, and scan state.
2. **One bounded edit**: for example, “Rotate page 2, reorder to 3, 1, 2, save as a new file, reopen, and verify page order and geometry.”
3. **Read the receipt**: output file, size, digest, and page-level results.
4. **Reopen**: read it back in a new process to prove the change is on disk.
5. **Visual review**: check layout, occlusion, fonts, and readability.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `CRAFT_EDITOR_UPDATE` | Set to `off` to skip the enhanced editor download | enabled |
| `CRAFT_WORKSPACE_ROOT` | Workspace bound to the editor | current project |
| `CRAFT_PANEL_METADATA_FILE` | Editor panel metadata | bundled |

Never write secrets, tokens, or private paths into plans or receipts.

## Extension contract

When adding a skill:

- Use the `pdfcraft-` prefix after migration
- Declare triggers and boundaries in `SKILL.md`
- Call the pinned CLI through the Harness, not ad-hoc shell
- Read back after every write and report verifiable results
- Never describe a successful command as a completed delivery

## Retry, idempotency, and recovery

- Read `receipt.json` first; determine what already happened.
- Do not replay operations that already had side effects.
- Retry with a new output path and keep the old receipt.
- For `UNKNOWN`, reconcile read-only; do not re-execute.

## Data and state

- Inputs are read-only.
- Outputs, receipts, and temporary directories are separate.
- A receipt records command, input, output, digest, and state.
- Confirm receipts are saved before deleting temporary files.

## Security

- Redaction results require human review; a successful command is not proof.
- Do not upload documents to third-party services without authorization.
- Use OCR language packs and external binaries from trusted sources.
- On a suspected secret leak, rotate the credential before cleaning files.

## Observability and operation

- Keep command, exit code, stdout/stderr, and receipt for every operation.
- Record page number, size, and text state at page level.
- Before delivery, confirm the output exists, opens, and has the expected page count.

## Development and verification

```bash
node --test
python3 -m pytest
```

Before committing, verify:

- Skill inventory matches directories
- CLI version and digest are pinned
- The installer runs on supported platforms
- README commands match actual entry points

## Packaging and release

- Version matches `plugin.json`, marketplace manifests, and the release tag.
- The ZIP root is `pdfcraft-plugin`.
- After release, reinstall and run one read-only inspection.

## Upgrade and migration

- Migrating from `pdfcraft`: uninstall the old plugin, then install `pdfcraft`.
- Keep old task directories and receipts; do not overwrite them.
- After the skill migration, old `pdfcraft-*` names are no longer entry points.

## Troubleshooting

| Symptom | Check |
|---|---|
| Command not found | Plugin installed, host restarted |
| OCR produces no text | Tesseract and language pack |
| Blank editor | Node.js version and workspace permissions |
| Wrong page order | Reopen the output and check page-level receipts |
| Garbled Chinese | Fonts and OCR language pack |

## Project layout

```text
pdfcraft-plugin/
├── .zcode-plugin/        # ZCode manifest and UI surface
├── .codex-plugin/        # Codex manifest
├── .claude-plugin/       # Claude manifest
├── skills/               # 20 skills
├── ui/                   # MCP Apps editor
├── commands/open.md      # open-editor command
├── docs/                 # architecture, receipts, host support
└── assets/               # icons and static assets
```

## Deep links

- [Architecture](docs/architecture.md)
- [Task receipts](docs/task-receipts.md)
- [Editor integration](docs/editor-integration.md)
- [Host support](docs/host-support.md)

## Contributing and support

Include plugin version, host, OS, input type, command, receipt, and expected result. Do not attach sensitive documents.

## License

Apache-2.0. See [LICENSE](LICENSE).
