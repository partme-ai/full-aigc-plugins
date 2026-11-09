## ADDED Requirements

### Requirement: Versioned visual references

The Harness SHALL validate a `jianying-visual-reference-set/v1` contract that binds each reference to one workflow output, revision, CreativeTarget digest, content digest, source type, usage, license status and allowed deviations. The contract MUST NOT carry commands, handlers, execution approval or local-path authority.

#### Scenario: Reference content changes

- **WHEN** a reference artifact, target digest or allowed-deviation rule changes
- **THEN** the reference-set digest changes and every context, approval, verdict and evidence bound to the old digest becomes unusable

### Requirement: Comparative read-only evaluation

The Harness SHALL construct a `jianying-comparative-evaluation-context/v1` containing the target references, current revision evidence, previous revision evidence and previous verdict. A Critic context MUST be fresh, have a unique session identity, declare `write_access=false`, and expose only registered read-only tools.

#### Scenario: Critic asks for execution authority

- **WHEN** a context lists CLI, GUI, shell, draft-write, export or approval tools, or declares a reused/non-fresh session
- **THEN** validation fails before evaluation begins

#### Scenario: Previous revision is supplied

- **WHEN** revision N is compared with revision N-1
- **THEN** both inputs, both proxy digests and the previous verdict digest are bound, and the context requires absolute quality, target gap and prior delta comparisons

### Requirement: At most one macro revision

The Harness SHALL generate a `jianying-macro-revision-request/v1` only from a validated stalled comparison. The request MUST use registered macro strategies, require explicit human approval and MUST be rejected if the output already has a prior macro-revision request.

#### Scenario: Repeated stagnation after macro revision

- **WHEN** an output stalls after its one permitted macro revision
- **THEN** the Harness returns human-review required and does not generate another macro request

### Requirement: Human-approved retarget

The Harness SHALL represent a proposed target change as `jianying-retarget-proposal/v1`. Applying it MUST require an exact, unexpired human approval bound to the proposal digest and MUST invalidate old target-bound approvals, contexts, verdicts and evidence.

#### Scenario: Model attempts to lower the target

- **WHEN** a proposal has no exact human approval, has an expired approval, or the approval digest differs
- **THEN** the proposal remains non-effective and no target or workflow state changes

### Requirement: No Dream Loop runtime dependency

The plugin SHALL NOT import or execute Dream Loop, FAL helpers or unrestricted Judge/Worker prompts. All editing remains routed through the existing WorkflowPlan and released Rust CLI boundary.

#### Scenario: Distribution validation

- **WHEN** the plugin distribution is inspected
- **THEN** no Dream Loop checkout, Python/FAL helper or research path is required for contract validation or runtime execution
