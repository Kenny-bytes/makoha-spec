<phase_instructions phase="1" document="Product Requirements Document">

## What this document is for

The Product Requirements Document turns the idea into the thing every later document derives from: what problem, for whom, what outcome, how success is measured, what must exist for that to happen, and what bounds it. It is also where the *set's* conventions are fixed, because everything downstream inherits them. Spec-driven development starts here: what this document states is what the build is held to.

## What downstream must be able to derive from it

- Phase 2 (ConOps) needs the need, the users, the desired change and the constraints.
- Phase 3 (OpsCon) needs the users precisely enough to become roles, and the outcomes precisely enough to become scenarios.
- Phase 5 (Requirements) needs each feature or capability stated so a requirement can trace to it, and each metric stated so a target can quote it.
- Phase 7 (Approvals) needs the scope of what is being approved.

## Establish first (before the outline)

1. **Intended purpose of the set** — if `<conventions>` shows it empty, ask: what is the finished documentation set *for*? (Examples: hand-off to coding agents; regulatory submission; investor diligence; internal alignment.) Record it: `python3 {{DOCPIPE}} set intended_purpose "<answer>"`. Every structural decision in every phase is judged against this.
2. **Project and system names** — record with `set project_name` / `set system_name` if empty.
3. **Identifier convention** — does the set want stable identifiers for traceability? For the stated purpose, propose whether and what shape (or none), confirm, and record the regex: `python3 {{DOCPIPE}} set id_pattern "<regex>"`. If none, leave it empty — checks and the traceability export then stay off.
4. **Requirement syntax** — propose whether phase 5 will use a controlled syntax. EARS (When/While/If–then/Where + one "shall") is the evidence-backed default for deterministic requirements; record `set requirements_syntax ears` if accepted, or leave empty.

## Material a PRD commonly draws on

Problem statement · users and personas with their current workaround · goals and non-goals · success metrics with baseline and target · features or capabilities, prioritised, each with a pass/fail statement · constraints (regulatory, technical, commercial, timeline) with their source · assumptions with confidence · open questions. Use what the purpose needs.

## Question bank (leverage order; skip anything the idea already answers)

1. Boundary: the smallest version a real user would adopt, and what is explicitly out for that version.
2. Primary user: who uses it first, in what setting, what they do today instead.
3. The one outcome: if only one thing changed for that person, what is it.
4. How you would know it worked: what number moves, from what baseline, by when.
5. Secondary users and outcomes — only if they change scope.
6. For each outcome: what must exist for it to be met; priority; one sentence a tester could mark pass/fail.
7. Constraints and who says so.
8. Assumptions the plan rests on and confidence in each.

## Closure specifics

Finalise only when the intended purpose is recorded, the conventions are recorded (or explicitly declined), every stated outcome has at least one capability serving it, every metric has a baseline or an explicit TBD for it, and every constraint names its source.

</phase_instructions>
