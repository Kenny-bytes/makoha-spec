# Design notes — docpipe

## Lever

**1 · Grant a capability**, stacked with 2 and 4. The hard part of the brief is not wording — it is that each phase must see exactly the finalised upstream documents (and, on re-iteration, exactly what changed in them), that the conversation must be free to shape the document, and that "update all documents" must be a command. The script assembles context, gates phases, hashes upstream bodies, diffs on change, records the conventions the interview chooses, and compiles; the prompts are the part it injects. Lever 2 is the assembly order (documents first in tagged blocks, then the conventions block, then instructions; in revise mode a unified body diff). Lever 4 is the orchestrator's build protocol.

## Non-obvious choices

1. **Greenfield means the script knows no scheme.** v1 shipped fixed skeletons and an identifier scheme (PRD-F, OPS-S, REQ-nnn…). Filed direction: strip it. Now the templates are title-only stubs, the phase prompts state purpose and what downstream must derive (with common material listed as material, not outline), and the orchestrator's first act is to propose an outline from purpose + upstream and confirm it. Conventions are decided in conversation and recorded in `docpipe.json` via `docpipe set`; every check is switched on by a recorded convention and does nothing otherwise.
2. **Identifier families instead of a scheme.** With only a regex to go on, the script cannot know which token is a definition and which a reference. The heuristic: a family is the identifier with digits removed; a family is homed in the earliest phase where it appears; a downstream token of an upstream family that upstream never defined is a dangling reference. This gives unresolved-reference detection, phase-6 coverage of phase-5 definitions, and the traceability export — without the script ever naming a prefix. Verified by S6, S8, S9.
3. **The document is the state, not the chat.** Every answer is written to disk before the next question; `run N` again resumes from the file; `update` has files to diff, not a conversation to replay.
4. **Body-only hashing.** Frontmatter status changes must not cascade staleness. Verified by S11.
5. **Restructure while draft, lock at final.** The conversation may reshape the outline until finalise; after that, iteration edits content and appends. Downstream derivations and approvals need stable targets; upstream freedom ends where a signature starts.
6. **Change requests instead of upstream edits.** A phase-3 answer that contradicts the PRD becomes a change request in phase 3's document. Upstream is only edited by a human, or by `update --apply` acting on a *downstream* document. `--apply` lands `revised`, never `final` — headless revision is proposal, not approval.
7. **Phase 5 is derivation-first.** It drafts the requirement set from OpsCon steps, modes, targets and "must never" lines and asks for confirmation in batches of ten; interviewing for requirements one at a time is the slowest way to produce a hundred of them.
8. **EARS is recommended, not imposed.** Phase 1 proposes it as the evidence-backed default for the "deterministic" requirement the brief asks for; the check runs only if `requirements_syntax` is recorded as `ears`.

## The one filed item I'd flag (once)

Technical Specifications (4) before Specific Requirements (5): V-model practice puts atomic requirements before design. Built as filed — 4 fixes the engineering numbers that 5 then quotes rather than recalls, and the phase-5 prompt still derives every requirement from OpsCon. Swapping is a two-line change in `PHASES` plus the upstream lists in prompts 04/05.

## Open questions (as questions)

1. Intended purpose for the first run — hand-off to coding agents (Optimus PRIME), regulatory submission, or both? Phase 1 asks; the answer shapes every outline.
2. Runner: keep `--bare` (API-key billing, reproducible) or drop it to use the subscription login for `update --apply`?
3. One `docpipe/` copy per repo (current), or a shared checkout referenced by `prompts_dir`/`templates_dir`?
4. Should `finalise` also `git commit` the document and snapshot? Not done — the script never touches git.
5. Confluence sync: one page per phase from `build`, or PSD.md as the sync unit? Current: PSD.md only.
6. Multi-approver sign-off — a table, or something stronger (signed tag)? Current: whatever phase 7's interview decides.
7. Additional phases for risk management (ISO 14971) and usability (IEC 62366) when the CDSS needs them? They fit between 5 and 6; not built.

## If the evals fail, change this first

- T02 weak (copies a template outline, or writes content instead of headings): add one worked `<example>` of an outline turn to the orchestrator. Examples beat rules for this.
- T03 weak (re-asks upstream): move "mine upstream before you ask" above "structure first" — order in the protocol is order of attention.
- T06 weak (imposes IDs after the user declined): make the identifier question explicitly two-sided in prompt 01 ("none" as a first-class option with its consequence stated).
- T07 weak (prose requirements): add three EARS examples drawn from the project's own OpsCon to prompt 05.
- Script layer: `evals/test_script.sh` is the regression suite; run it before changing `docpipe.py`.

## Escalation

When T01–T12 hold at ≥ 90 %, hand `prompts/` + `evals/` to DSPy/GEPA per phase; the per-phase prompts are separate files so they optimise independently.
