# Third-Party Notices

This plugin does not bundle third-party application binaries, proprietary SDKs,
credentials, generated media, model weights, pyJianYingDraft source, a
`jianying-cli` source checkout, or non-commercial headless source code.

## Rust CLI interoperability sources

The separately released `jianying-cli` records and enforces its own file-level
provenance. Its permitted interoperability inputs include:

- [GuanYixuan/pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft),
  Apache-2.0, fixed at the commit recorded by the CLI source manifest. License,
  copyright, modification, fixture, and generated-catalog obligations belong
  to the CLI release artifacts.
- [renezander030/capcut-cli](https://github.com/renezander030/capcut-cli), MIT,
  used at a fixed commit for observable command and behavior parity.

The plugin itself consumes only the released CLI executable, capability
manifest, checksums, SBOM, and licenses selected by `runtime/jianying-cli.lock.json`.

## Restricted methodology references

- [achimala/dream-loop](https://github.com/achimala/dream-loop), MIT,
  fixed at commit `9bddb901f7d071cfefdd21e264267c757177a9df`, is used only as a
  methodology reference for fixed visual targets, independent comparison and
  bounded macro replanning. No Dream Loop, FAL, Python helper, prompt text or
  checkout is bundled or required at runtime.
- [partme-ai/jianying-headless](https://github.com/partme-ai/jianying-headless)
  and its upstream are treated only as restricted capability targets and
  historical methodology references. Their source, tests, blueprints,
  resources, constants, and checkout are not plugin runtime inputs.
- [mcncarl/yichen-skills](https://github.com/mcncarl/yichen-skills) is a
  methodology reference only. No source or documentation text is bundled.

Changing implementation language does not remove upstream license obligations.
The CLI and plugin provenance gates must remain satisfied independently.

## Trademarks and application boundary

JianYing, 剪映, CapCut, and `com.lemon.lvpro` identify interoperability targets
and remain trademarks of their respective owners. This is not an official SDK.
The plugin never distributes the editor, its private resources, account data,
or membership-gated assets, and does not bypass product authorization controls.
