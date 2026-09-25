# docpipe eval pack — cases and rubric

Two layers. The **script layer** is deterministic and runs in seconds (`evals/test_script.sh`). The **prompt layer** scores one model turn per case and lifts into promptfoo (`promptfooconfig.yaml`).

The script imposes nothing. Every script-layer check is switched on by a convention the phase-1 interview records with `docpipe set`; with none recorded, the only check is "has structure, no open markers".

## Script layer

| # | Case | Pass criterion |
|---|---|---|
| S1 | `init` twice | second run reports "nothing to do"; no file changes |
| S2 | `prompt 2` before phase 1 final | exits non-zero with gate message |
| S3 | `check 1` on a fresh stub | reports "no structure yet" and nothing else — no identifier or syntax finding |
| S4 | `check 1` on a structured PRD with no conventions set | clean, even though the text contains identifier-like tokens |
| S5 | `set id_pattern '['` | refused as invalid regex; valid `set` calls persist to `docpipe.json` |
| S6 | `check 5` with conventions set | flags a reference to an identifier of an upstream family that upstream never defined; flags a requirement row with no "shall", a non-EARS shape, and a two-"shall" sentence — nothing else |
| S7 | `check 5` after removing those rows | clean |
| S8 | `check 6` | reports each phase-5 identifier that phase 6 never references |
| S9 | `build` traceability.csv | for each identifier: defining phase, referencing phases, count — derived from the pattern alone |
| S10 | `update` twice with no changes | "no status changes"; PSD/traceability unchanged |
| S11 | frontmatter-only change to a finalised upstream doc | downstream **not** stale (body-only hash) |
| S12 | body edit to finalised PRD | every finalised dependant stale; register shows STALE; revise prompt carries body-only diff and the conventions block; no unresolved placeholders |

## Prompt layer — scoring rubric (per case, ≤ 1 minute by a person)

| # | Case | Pass if | Expected failure mode |
|---|---|---|---|
| T01 | phase 1 from a one-paragraph idea, no conventions set | first turn asks for the intended purpose (or records it if the idea states it) before anything else | starts drafting sections |
| T02 | phase 1, purpose recorded | proposes an outline — headings with one line each naming what it establishes and what upstream it derives from — then one question (add/cut/reorder); no template headings copied from anywhere | writes a full PRD; or asks a questionnaire |
| T03 | phase 3 when the PRD names users | proposes roles derived from the PRD's users, citing the section, and asks to confirm | re-asks "who are the users" |
| T04 | answer contradicts finalised PRD | says so once, cites the PRD section/item, records a change request in the current document; PRD untouched | silently rewrites; edits the PRD |
| T05 | user doesn't know a number | `{{TBD: <question>}}` in place, listed under open questions, moves on | invents a plausible value |
| T06 | phase 1 asked about identifiers, user says "no IDs, just headings" | records nothing for `id_pattern`, structures references as section links, proceeds | imposes an ID scheme anyway |
| T07 | phase 5, EARS recorded | derived set ≥ 3 requirements, all EARS-shaped, each tracing to an OpsCon item; batches ≤ 10 with confirm ask | prose requirements; traces to PRD only |
| T08 | phase 5, compound answer | split into two requirements | one with "and" |
| T09 | phase 6, validation fails on a target | modification = yes, change request names the TechSpec target, no direct upstream edit | edits TechSpec in place |
| T10 | "finalise" with undeferred TBDs | lists them, asks deferred-or-answer; not finalised | declares final |
| T11 | "skip the questions, write it all" | full draft from upstream with proposed/TBD marking; one confirm question | fabricates as if stated |
| T12 | headless revise | minimal edits derived from the diff; existing structure kept; TBD where undecidable; counts reported | renumbers or restructures |

Global asserts on every turn: no praise; ≤ 1 question per turn.

## Fixtures

`evals/fixtures/<name>/` is a mini repo (`docpipe.json` + `docs/spec/`). Build them by running the pipeline with `--force` where needed:

| fixture | state |
|---|---|
| idea-only | 00-idea.md one paragraph; `docpipe.json` with empty purpose and conventions |
| purpose-set | as above plus `intended_purpose` recorded |
| prd-final | phase 1 final; PRD structured by an interview; conventions recorded |
| prd-no-ids | phase 1 final; user declined identifiers |
| opscon-final | phases 1–3 final |
| reqs-final | phases 1–5 final, EARS recorded |
| prd-changed | phases 1–3 final, then PRD body edited |

Graduation: when T01–T12 pass at ≥ 90 % over 5 runs each, the orchestrator is a seed for DSPy/GEPA optimisation per phase.
