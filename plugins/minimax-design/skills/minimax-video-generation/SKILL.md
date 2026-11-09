---
name: minimax-video-generation
description: "Generate videos with MiniMax H3 via the v2 API: t2v, i2v, first/last-frame FL2VA anchored by white-model previs frames, and reference-image mode. Deterministic client, resumable queries, verified download. Prompts are drafted through the vendored h3-prompt-writing skill."
---

# MiniMax Video Generation (H3 v2)

Deterministic client: `scripts/minimax_video.py`. Every paid call needs the
step-0 preflight from `minimax-design-use` to pass first. Model:
`MiniMax-H3`（480P/768P/2K，4~15s）or `MiniMax-H3-Max`（极速，480P/768P，5~15s）.

## Prompt discipline (h3-prompt-writing first)

H3 prompts are not free prose. Draft every prompt through the vendored
`h3-prompt-writing` skill, which fixes the structure per input mode:

- **T2VA** (text only): full audiovisual timeline —
  `integrated_multimodal_description` → `overall_soundscape` →
  `non_diegetic_music` (see `h3-prompt-writing/references/base-en.txt`).
- **I2VA** (first frame): start from the frame, develop forward.
- **FL2VA** (first + last frame): describe the continuous path BETWEEN the two
  frames — this is the white-model previs anchoring mode.
- **Ref2VA** (reference images/video/audio): six-section rewrite format
  (`references/ref-en.txt`).
- Duration 4–15s: the description must match the requested length exactly.
- Keep reference labels (`<Picture 1>` …) consistent; concrete details beat
  words like "cinematic".

## Modes via the client

1. **t2v** — text only (ratio required, not adaptive):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/minimax_video.py" generate \
  --prompt "<h3-prompt-writing T2VA structure>" --ratio 16:9 \
  --duration 8 --resolution 768P --out generated/shot-01.mp4
```

2. **i2v** — first frame anchors composition:

```bash
python3 "${CLAUDE_PROJECT_DIR}/scripts/minimax_video.py" generate \
  --first-frame renders/shot-01_first.png \
  --prompt "<I2VA structure>" --out generated/shot-01.mp4
```

3. **first/last-frame (FL2VA)** — the white-model previs anchor (preferred for
   storyboarded work): render each shot's first and last frame from the Blender
   white model, then describe the continuous path between them:

```bash
python3 "${CLAUDE_PROJECT_DIR}/scripts/minimax_video.py" generate \
  --first-frame renders/shot-01_first.png --last-frame renders/shot-01_last.png \
  --prompt "<FL2VA structure>" --duration 6 --out generated/shot-01.mp4
```

4. **reference-image** — subject-consistent generation (S2V family; mutually
   exclusive with first/last frames): `--reference-image a.png --reference-image
   b.png`.

Local frames are embedded as data URLs automatically; `mm_file://{file_id}` and
public URLs pass through.

## Parameters

- `--duration 4..15` (H3-Max 5..15), `--resolution 480P|768P|2K`,
  `--ratio` (required for t2v; `adaptive` allowed for i2v/fl2v),
  `--model MiniMax-H3|MiniMax-H3-Max` (default env `MINIMAX_MODEL`).
- `--wait <seconds>` caps polling; a timeout prints the `task_id` — resume with
  `query --task-id <id>` (add `--out` to download on success). Never resubmit.
- `list` / `cancel --task-id` for task management.

## Style-leak discipline (white-model frames)

The white-model frame is gray primitives; i2v may keep that style. Run one A/B
shot before a batch: (a) white-model frame directly + an FL2VA restyle prompt;
(b) restyle the frame through an image model first (keep composition). Fix the
winning path into the episode's convention before spending on all shots.

## Never do

- Never submit paid generation without the preflight and the user's intent.
- Never resubmit a submitted task id; `query` is the only resume path.
- Never treat a polling timeout as failure — it is a resume state.
- Never mix first/last-frame mode with reference-image mode in one request.
- Never invent video facts in the prompt beyond what the frames and the user's
  brief support; h3-prompt-writing's retention rules apply to Ref2VA rewrites.
