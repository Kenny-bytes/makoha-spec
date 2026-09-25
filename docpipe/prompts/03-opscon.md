<phase_instructions phase="3" document="Operations Concept">

## What this document is for

The Operations Concept takes the ConOps and turns it into system-level specifics: what the system does, for which roles, in which modes, through which scenarios step by step, across which interfaces, to what user-facing performance, and what it does when things fail. It says what, not how. It is the document phase 5 mines for requirements, so every scenario step must be concrete enough to write a requirement against.

## What downstream must be able to derive from it

- Phase 4 (TechSpec) needs the system boundary, every interface, every user-facing performance expectation, and the data concept.
- Phase 5 (Requirements) needs numbered scenario steps (each with one actor and one observable action or response), modes with entry/exit conditions, and every "must never".
- Phase 6 (Validation) needs the scenarios as the source of end-to-end validation activities.

## Read upstream this way

Each ConOps situation becomes at least one scenario here with numbered steps — draft all of them from the ConOps text first and confirm one at a time. PRD users become roles (a user may map to several roles). ConOps environment and connected systems become interfaces. PRD metrics and pass/fail statements become user-facing expectations. PRD constraints and ConOps risks become failure behaviour and "must never".

## Material an OpsCon commonly draws on

System overview and boundary · roles with permissions · modes of operation (normal, degraded, offline, training, maintenance, read-only) with entry and exit · scenarios with preconditions, trigger, numbered steps, outcome, variations and exceptions · external interfaces with direction and owner · data concept (principal objects, origin, persistence, retention) · user-facing performance expectations per scenario · failure, degraded and recovery behaviour · support, maintenance and operations concept · assumptions · open questions.

## Question bank

1. Boundary check: given the ConOps, what is inside the system and what stays with people or other systems.
2. Roles: who logs in, administers, reviews, receives the output; permissions in one line each.
3. Modes beyond normal, and what triggers each.
4. For each ConOps situation, the steps as the user experiences them: what they see, what they do, what the system does, what they see next.
5. For each scenario: what varies, what goes wrong, what the user does then.
6. What crosses each boundary, in which direction, who owns the other side.
7. Principal data objects: where born, where persisted, for how long.
8. "Fast enough", "available enough", "accurate enough" per scenario, as a user would state it.
9. What the system must never do, and who runs it.

## Closure specifics

Finalise only when every ConOps situation is refined by at least one scenario, every scenario has numbered steps and an exceptions line, modes beyond normal are stated or explicitly ruled out, every interface has an owner, and at least one "must never" is stated with the consequence it prevents.

</phase_instructions>
