# VectorCraft Boolean Geometry First-use Acceptance

The pinned VectorCraft plugin dev.8 / skill source dev.7 was used. The installed `vectorcraft-cli-boolean` was copied alone into `.agents/skills/`, and CLI 0.2.0 was downloaded into an empty runtime home using the default public lock. The single skill performed native operations and SVG, PNG and PDF export without sibling resources.

The fixture checks unite, minusFront, intersect and exclude on nested rectangular contours. MinusFront and exclude save a `NonZero` compound path with two closed contours, opposite winding, areas 6400 and 1024, and a transparent center. Unite retains the center; intersect retains only the inner contour. An independent native MCP session reopens the saved project to inspect geometry.

PNG is decoded directly. SVG and PDF are independently rendered using the existing PyMuPDF installation, checking outer-only, center, outside and unselected-shape pixels. SVG has no image nodes; PDF contains vector drawings and no raster images. Unselected native properties are unchanged, and every original delivery file digest is preserved after each revision. Invalid selection fails without publishing a delivery directory. All 12 installed skill hashes still match the original host receipt.

One actual target test passed, covering four positive operations and invalid-selection rejection, in 9.625 seconds. The default source regression had 43 tests: 28 passed and 15 opt-in tests skipped. Skips do not constitute acceptance. See [evidence](evidence/codex-vectorcraft8-boolean-geometry-first-use-20261006.json).

The initial test incorrectly expected a single path for a hole. Native output showed a compound path; assertions now check its actual closure, area, winding and decoded transparency. No product code was changed. These rectangular fixtures do not prove arbitrary curved/self-intersecting geometry, divide/trim, external-editor round trips, GUI/model execution or full creative acceptance.
