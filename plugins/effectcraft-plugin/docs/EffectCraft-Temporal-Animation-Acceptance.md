# EffectCraft temporal animation acceptance

Fixed plugin dev.7 / skills dev.6 / native CLI 0.2.0. One installed animation skill is copied alone to `.agents/skills`; an empty runtime uses default public installation with no archive overrides.

The 320×180, 12 fps, one-second brand intro adds badge opacity keys at 0 s / 0 and 0.5 s / 100. Native reopened key records match; RGBA alpha at 0, 0.25, 0.5 and 0.75 s is 0, 128, 255 and 255. Existing ffmpeg decodes all 12 H.264 frames, checks increasing badge intensity and verifies video timing.

Changing NOVA to NOVA PLUS preserves the entire badge layer and title opacity property. The expanded title can cover new pixels, so unchanged animation is sampled at (45,75), outside both title extents, with an H.264 tolerance of 3 RGB levels. The hidden opening frame is identical and the visible title frame differs. Every original delivery file and all 13 installed skill digests remain unchanged.

One real test passed in 9.398 seconds. Source regression: 24 passed, 17 skipped; plugin regression: four passed. [Evidence](evidence/codex-effectcraft7-temporal-animation-first-use-20261006.json). Reproduce with `CRAFT_TEMPORAL_FIRST_USE=1`, `CRAFT_INSTALLED_ANIMATION_SKILL` pointing to the actual installed animation skill and optional fresh `CRAFT_TEMPORAL_EVIDENCE`; run `python3 -B -m unittest discover -s tests -p test_animation_temporal_first_use.py` from the independent skill repository with existing Pillow and ffmpeg.

This does not establish animated transparent video, all interpolation modes, GUI/model dispatch or creative acceptance. Original full OpenSpec tasks remain open; only the bounded temporal verification task is complete.
