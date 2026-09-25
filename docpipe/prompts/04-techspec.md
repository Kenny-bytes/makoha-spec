<phase_instructions phase="4" document="Technical Specifications">

## What this document is for

The Technical Specifications say how the system is built to deliver the Operations Concept: architecture, components, interfaces, data, stack, security, engineering-level targets, deployment, standards mapping, and the design decisions with the alternatives they beat. Phase 5 quotes this document's numbers rather than recalling them, and validation measures against its targets.

## What downstream must be able to derive from it

- Phase 5 (Requirements) needs every engineering target as a number with a measurement method, every technical interface's contract, and every decision that constrains implementation.
- Phase 6 (Validation) needs the measurement method per target and the environments tests run in.
- Phase 7 (Approvals) needs the standards mapping.

## Read upstream this way

The OpsCon boundary is the architecture boundary — if they differ, raise a change request rather than redrawing silently. Walk the OpsCon scenarios to draft the components (every step served by at least one). Every OpsCon interface is realised by at least one technical interface. Every user-facing expectation becomes a measurable engineering target. PRD constraints and ConOps policies drive the standards mapping and security. The OpsCon data concept drives the data model.

## Material a technical specification commonly draws on

Architecture overview with one diagram · components with responsibility and technology · interfaces and APIs with protocol, contract, auth, versioning · data model, storage, retention, migration · stack with version pins and reasons · security and privacy (identity, authorisation, classification, encryption, audit, secrets) · engineering targets (p95 latency, availability, throughput, RPO/RTO) each with a measurement method · deployment, environments, CI/CD, rollback · standards and compliance mapping · design decisions with alternatives, reason, reversibility · assumptions · open questions.

## Question bank

1. Architecture shape, drawn from the OpsCon boundary; confirm the diagram.
2. Components: for each scenario, what does the work.
3. Interfaces: protocol, contract, auth, versioning for each OpsCon interface.
4. Data: entities, ownership, storage engine, retention, migration from anything existing.
5. Stack with version pins and the reason for each choice.
6. Security and privacy, item by item.
7. Engineering targets: for each user-facing expectation, the number and how it is measured.
8. Environments, CI/CD, rollback.
9. Which standards or regulations apply and where each is addressed.
10. Decisions: alternatives considered, reason, reversibility.

## Closure specifics

Finalise only when the diagram renders, every OpsCon interface and expectation has its technical counterpart, security covers identity, authorisation, encryption and audit, every stack row has a pin or an explicit TBD, and every regulatory constraint from the PRD appears in the standards mapping.

</phase_instructions>
