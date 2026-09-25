<phase_instructions phase="2" document="Concept of Operations">

## What this document is for

The Concept of Operations describes, at the level of the organisation, how it intends to operate once this capability exists: the need, how the job is done today, what changes, who has a stake, the environment, the situations that define operation, the policies that bound it, the operational risks — and one Operational Concept Graphic that a stakeholder understands in thirty seconds. This is the organisation-level ConOps; system-level behaviour belongs to phase 3, and the graphic shows no internal components.

## What downstream must be able to derive from it

- Phase 3 (OpsCon) needs every operational situation stated with trigger, actors and outcome, so each can be refined into system-level scenarios with steps.
- Phase 4 (TechSpec) needs the environment and the external systems by name.
- Phase 5 (Requirements) needs the policies and the "must never" operational risks.
- Phase 7 (Approvals) needs the stakeholders.

## Read upstream this way

The PRD's problem, users, desired outcome and constraints seed the need, the stakeholders, the desired change and the policies. The idea's "what changes if it works" seeds the desired change. Draft those before asking anything.

## Material a ConOps commonly draws on

Mission and need · current operations walk-through · desired change as a delta · stakeholders (including non-users: approvers, payers, auditors, adjacent teams) · operational environment (physical, organisational, regulatory, connected systems) · operational scenarios: a routine one, a peak or urgent one, a failure or exception, an onboarding one · policies and constraints · risks and impacts with mitigation concept · the Operational Concept Graphic · assumptions · open questions.

## Question bank

1. Walk me through how the job is done today, start to finish — who touches it, where it hurts.
2. With the capability in place, the same walk: name only what changed.
3. Who else has a stake but is not a user.
4. Where this operates: setting, organisational unit, jurisdiction, connected systems by name.
5. The three to six situations that define operation; for each, trigger, actors, outcome.
6. What policy, law, standard or contract bounds how it may be operated.
7. What could go wrong operationally, for whom, and the mitigation concept.
8. Draw it: confirm the actors, the capability, the external systems, and the two or three flows that belong on the one picture.

## The Operational Concept Graphic

Produce it as a Mermaid `flowchart` in the document: actors who interact, the capability as one node, external systems, the operational environment as an enclosing subgraph, labelled edges for the principal flows. Twelve nodes or fewer; if it needs more, the boundary is wrong. Mermaid is the source of truth; note any export the user wants.

## Closure specifics

Finalise only when the current and desired walk-throughs both exist, at least three situations including one exception are stated with trigger/actors/outcome, the graphic renders as valid Mermaid, and every risk has a mitigation concept.

</phase_instructions>
