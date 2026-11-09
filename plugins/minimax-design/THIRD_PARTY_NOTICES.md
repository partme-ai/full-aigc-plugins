# Third-Party Notices

This plugin does not bundle third-party application binaries, proprietary SDKs, credentials, generated media, or vendor source code beyond the vendored skills declared below.

## Vendored skills (verbatim, content-pinned)

Six skills under `skills/` are vendored verbatim from two upstream sources,
pinned per skill by SHA-256 in `skills.lock.json`; the `check` gate fails on
any drift.

From [full-aigc-skills/minimax-skills](https://github.com/full-aigc-skills/minimax-skills)
(vendored at commit `0b72343a8d5674aa430d42ba8c72d575cadbba8a`, Apache-2.0):

- `minimax-multimodal-toolkit`
- `minimax-music-gen`
- `minimax-music-playlist`

From [MiniMax-AI/MiniMax-H3](https://github.com/MiniMax-AI/MiniMax-H3)
(vendored at commit `d21241f0a4b3acbb34c97dae47fa417b7065e438`):

- `h3-prompt-writing` — the official H3 prompt-structure skill
  (T2VA / I2VA / FL2VA / L2VA / Ref2VA); upstream license is published with
  the MiniMax-H3 model on Hugging Face.

The other eight MiniMax-H3 repository skills are bound to the MiniMax Hub
canvas workflow and are intentionally not vendored (not portable to generic
agent harnesses, per the upstream README).

## Interoperability references

References to MiniMax, Hailuo, H3, 海螺, mmx, Codex, ZCode, Kimi, and other product names
identify interoperability targets. Their trademarks and software remain the
property of their respective owners.

MiniMax API access requires the user's own API key configured via the
`MINIMAX_API_KEY` environment variable (or an `mmx` CLI Token Plan login,
`mmx auth login --api-key`); nothing here ships credentials, and no paid call
is made without the user's explicit request. The mmx CLI
(github.com/MiniMax-AI/cli) is a third-party binary installed separately by
the user; this plugin does not bundle or distribute it.
