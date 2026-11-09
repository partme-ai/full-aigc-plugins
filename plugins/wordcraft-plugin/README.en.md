# WordCraft (Document Writing)

> Draft, lay out, and deliver editable Word documents from an agent session. Keep real section structures, native tables, and page numbers, then reopen the file before handoff.

**Version**: 0.1.0-dev.20261109.4 · **License**: Apache-2.0 · **Skills**: 16 · **MCP server**: 1

[简体中文](README.md) · [Install](#installation) · [Quick start](#quick-start) · [Project layout](#project-layout)

## Positioning

WordCraft is for users who need an editable Word document, not Markdown or plain text. It collects and checks facts, builds a section and field structure, lays the result out with native headings, tables, page numbers, and headers, then reopens the file to check what the reader will see.

Use it for:

- Weekly reports, meeting minutes, project briefs
- Business proposals, acceptance reports, requirements
- Resumes, training material, research reports
- Consistent TOC, page numbers, captions, and styles
- Local edits and version comparison

Do not use it for:

- Concatenating a long document into one text block
- Inventing business data without a source
- Replacing an editable document with screenshots

## At a glance

```text
interviews / notes / data / old drafts
        │
        ▼
WordCraft skill (collect → structure → layout → read back)
        │
        ├── wordcraft-cli (native document operations)
        └── MCP editor (in-browser review and local edits)
        │
        ▼
DOCX + reopen check + delivery notes
```

## Capabilities and boundaries

| Capability | What it does | Boundary |
|---|---|---|
| Draft | Build sections for the audience and goal | Facts must come from input or be labeled |
| Structure | Heading levels, TOC, page numbers, headers | Long-document pagination needs a real open |
| Tables | Native tables, merged cells, captions | Complex formulas and charts need separate checks |
| Styles | Consistent paragraphs, fonts, numbering, spacing | Not a brand-design system |
| Local edits | Change only the requested scope | Reopen after every edit |
| Version comparison | Text and structural differences | Does not decide which version is business-correct |
| Export | DOCX, and PDF when needed | PDF needs font-embedding checks |

## Architecture and core flow

```text
Host / agent
   │  invokes a skill
   ▼
skills/wordcraft-*  ──►  MCP editor / wordcraft-cli
                              │
                              ▼
                     DOCX + structure check
                              │
                              ▼
                     reopen, page review, delivery
```

Rules:

1. Confirm goal, audience, length, and delivery format first.
2. Build structure before content; unify layout last.
3. Keep a rollback version for every edit.
4. Exit code 0 is not proof of correct layout; reopen and check.

## Compatibility

| Item | Status |
|---|---|
| Host | Codex has full evidence; other hosts are NOT_RUN |
| Node.js | 24+ (editor) |
| Native engine | WordCraft 0.7.0 / wordcraft-cli |
| Platforms | Follow the actual package and release notes |
| Windows Git | Enable longpaths |

## Installation

```bash
codex plugin marketplace add partme-ai/full-aigc-plugins
codex plugin add wordcraft@full-aigc-plugins
```

Restart the host and start read-only:

> Open this document and report its section structure, page count, and current styles. Do not modify it.

## Quick start

1. **Confirm the goal**: type, audience, length, required sections.
2. **Collect facts**: notes, data, old drafts, brand rules.
3. **Build structure**: TOC and sections first, then content.
4. **Unify layout**: headings, body, tables, page numbers, headers.
5. **Reopen**: check pagination, TOC, table breaks, and fonts.
6. **Deliver**: DOCX, plus PDF when required.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `CRAFT_WORKSPACE_ROOT` | Workspace bound to the editor | current project |
| `CRAFT_EDITOR_UPDATE` | Set to `off` to skip the enhanced editor download | enabled |

Never write secrets, tokens, or private paths into documents or configuration.

## Extension contract

When adding a skill:

- Use the `wordcraft-` prefix
- Declare triggers and boundaries in `SKILL.md`
- Operate on a real document through MCP or the pinned CLI
- Reopen and verify structure after every edit
- Never describe generation as completed delivery

## Retry, idempotency, and recovery

- Save a version or copy before editing.
- After a failure, inspect the current document; do not replay writes.
- Retry with a new output path.
- Mark uncertain results for review.

## Data and state

- Source material is read-only.
- Outputs and temporary files are separate.
- Keep edit history and the final version.
- Confirm the deliverable is saved before deleting temporary files.

## Security

- Do not upload unauthorized material to third-party services.
- Redact sensitive fields before delivery.
- Explicitly confirm macros, external links, and embedded objects.
- On a suspected leak, rotate credentials before cleaning documents.

## Observability and operation

- Record command, output file, page count, and structure checks.
- Before delivery, confirm the file opens, the TOC updates, and page numbers are correct.
- For long documents, sample the first, middle, and last pages.

## Development and verification

```bash
node --test
python3 -m pytest
```

Before committing, confirm the skill inventory, directories, and README agree.

## Packaging and release

- Version matches `plugin.json`, marketplace manifests, and the tag.
- The ZIP root is `wordcraft-plugin`.
- After release, reinstall and run one read-only inspection.

## Upgrade and migration

- Back up workspace documents before upgrading.
- Files from older versions must remain openable.
- Recheck templates, page numbers, and TOC after migration.

## Troubleshooting

| Symptom | Check |
|---|---|
| Document will not open | File integrity or file lock |
| TOC is stale | Update fields in Word |
| Page numbers wrong | Section breaks and page-number start |
| Table breaks badly | Row properties and repeat-header |
| Missing fonts | Embed or substitute fonts |

## Project layout

```text
wordcraft-plugin/
├── .zcode-plugin/      # ZCode manifest and UI surface
├── .codex-plugin/      # Codex manifest
├── .claude-plugin/     # Claude manifest
├── skills/             # 16 skills
├── ui/                 # MCP Apps editor
├── commands/open.md    # open-editor command
├── docs/               # architecture and verification records
└── assets/             # icons and templates
```

## Deep links

- [Architecture](docs/architecture.md)
- [Scene skills](docs/scene-skills.md)
- [Task receipts](docs/task-receipts.md)

## Contributing and support

Include plugin version, host, document type, command, output file, and expected result. Do not attach sensitive documents.

## License

Apache-2.0. See [LICENSE](LICENSE).
