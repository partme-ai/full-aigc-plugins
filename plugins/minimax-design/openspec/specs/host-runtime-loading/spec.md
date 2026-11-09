# host-runtime-loading Specification

## Purpose
Define how each supported host launches the plugin with portable, repository-owned runtime commands and validated dependencies.
## Requirements
### Requirement: ZCode loads MiniMax hooks once

The ZCode distribution SHALL rely on standard hook auto-discovery and SHALL NOT explicitly point to the same default hooks file.

#### Scenario: Discover hooks

- **WHEN** ZCode loads the plugin
- **THEN** each hook is registered exactly once
