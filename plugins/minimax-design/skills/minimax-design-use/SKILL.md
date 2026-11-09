---
name: minimax-design-use
description: "Route MiniMax design requests: capability preflight first (mmx CLI login or MINIMAX_API_KEY), then H3 video generation (t2v, i2v, first/last-frame FL2VA), vendored h3-prompt-writing for prompt structure, or mmx toolkit for text, image, speech, and search."
---

# MiniMax Design Router

Use this as the entry point. Before any paid generation, run the capability
preflight (step 0) — MiniMax authenticates per region, and a missing credential
must surface as actionable guidance, never as a raw API error.

## Step 0 — capability preflight (always first)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/minimax_video.py" check
```

Read the output and act on it:

- `MINIMAX_API_KEY: 未设置` → tell the user exactly how to fix it: get a key at
  https://platform.minimax.cn (国内) / https://platform.minimax.io (国际) →
  用户中心 → 接口密钥, then `export MINIMAX_API_KEY=...` (shell config or
  project `.env`). Do not proceed to paid generation without it; do not ask the
  user to paste the key into chat.
- `mmx CLI: 未安装` → the general-purpose path (text/image/speech/vision/search)
  needs the official Token Plan CLI:
  `npm install -g mmx-cli && mmx auth login --api-key sk-xxx` (region
  auto-detected; if 401, `mmx config set --key region --value cn|global`).
  The v2 API path in `minimax-video-generation` works with just
  `MINIMAX_API_KEY` and no mmx login.
- Gateways: 国内 `https://api.minimax.cn`（默认，`MINIMAX_API_HOST` 可覆盖；
  旧账号 `api.minimaxi.com`）/ 国际 `https://api.minimax.io`. The key and the
  host must be from the same region or you get `Invalid API key`.

## Routing

- **H3 video generation** (t2v, i2v, first/last-frame FL2VA, reference-image) →
  `minimax-video-generation`. Prompt structure comes from the vendored
  `h3-prompt-writing` (T2VA/I2VA/FL2VA/L2VA/Ref2VA rewrite format) — always
  draft H3 prompts through it.
- **General generation via Token Plan CLI** (text chat, image generate, speech
  synthesize, vision describe, search) → vendored `minimax-multimodal-toolkit`.
- **Music / song generation** → `minimax-music-gen`; playlists →
  `minimax-music-playlist`. (mmx CLI itself has no music command; music goes
  through the API skills.)

## Credential setup (cross-platform)

`MINIMAX_API_KEY` resolution order: process env → project `.env` → plugin `.env` →
`~/.minimax-design/credentials.json`. Persist it on any OS with
`python3 scripts/minimax_video.py auth --api-key sk-...` (chmod 600); clear with
`auth --clear`. Windows session: PowerShell `$env:MINIMAX_API_KEY="sk-..."`;
persistent: `setx MINIMAX_API_KEY "sk-..."`. macOS/Linux persistent: append
`export MINIMAX_API_KEY=sk-...` to `~/.zshrc` / `~/.bashrc`.

## Never do

- Never run paid generation without the step-0 preflight passing.
- Never echo the API key value back into the conversation; show only the masked
  tail.
- Never mix gateways: 国内 (.cn / .minimaxi.com) and 国际 (.io) accounts are
  separate key spaces.
- Never resubmit a submitted v2 task id; `query` is the only resume path.
