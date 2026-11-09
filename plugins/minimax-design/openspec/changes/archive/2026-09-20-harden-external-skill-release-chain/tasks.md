## 1. Supply-chain implementation

- [x] 1.1 Add vendor v2 with immutable tag, peeled SHA and digest validation
- [x] 1.2 Add `plugin-local-skills.json` for the two plugin-only skills
- [x] 1.3 Update skills-check and skills-sync workflows to validate dispatch tag and commit

## 2. Distribution correctness

- [x] 2.1 Collapse public skills onto `minimax-skills v1.1.1`
- [x] 2.2 Repair base-version, skill-count and ZCode `userConfig` assertions
- [x] 2.3 Verify unit tests plus online and offline vendor checks

## 3. Publication

- [x] 3.1 Validate OpenSpec artifacts and archive the completed change
- [x] 3.2 Commit and push the plugin, then confirm remote CI at the release commit
- [x] 3.3 Create the immutable plugin tag and GitHub Release
- [x] 3.4 Update and verify the catalog entry without including unrelated user changes
