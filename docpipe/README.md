# docpipe

Phase-gated, interview-driven design documentation for a repo. Greenfield by design: the script prescribes no document structure and no identifier scheme. Each phase's conversation builds its document's structure for the set's intended purpose; phase 1 fixes the conventions the set will use; the script gates phases, injects finalised upstream documents into each interview, tracks staleness by content hash, diffs on change, and compiles the set into one Product Specification Document.

```
IDEA ──► 1 PRD ──► 2 ConOps ──► 3 OpsCon ──► 4 TechSpec ──► 5 Requirements ──► 6 Validation ──► 7 Approvals ──► PSD.md
                                  ▲                                                   │
                                  └────────────────── change requests ◄───────────────┘
```

## Install

```bash
cp -r docpipe/ <repo>/docpipe/
cd <repo>
python3 docpipe/docpipe.py init          # docs/spec/00-idea.md … 07-approvals.md (bare stubs), docpipe.json
# optional: /docpipe <n> inside Claude Code
mkdir -p .claude/commands && cp docpipe/claude-commands/docpipe.md .claude/commands/
```

## Run a phase

```bash
vim docs/spec/00-idea.md                  # one paragraph, in your own words
python3 docpipe/docpipe.py run 1          # opens Claude with the phase-1 prompt as system prompt
#   …or inside a Claude Code session in the repo:   /docpipe 1
#   …or anywhere:  python3 docpipe/docpipe.py prompt 1 --stdout | pbcopy   and paste
```

Phase 1 first establishes the set's **intended purpose** and its **conventions** (whether to use identifiers and what shape; whether phase 5 uses a controlled requirement syntax), recording each with `docpipe set`. Every phase then proposes an outline derived from its purpose and the upstream documents, confirms it, and fills it one question at a time, writing to the file as it goes. Nothing is pre-drawn.

```bash
python3 docpipe/docpipe.py check 1        # open markers; and only if conventions are set: unresolved references, coverage, syntax
python3 docpipe/docpipe.py finalise 1     # status=final, upstream snapshot + hash, phase 2 unlocked
python3 docpipe/docpipe.py run 2
```

## Re-iterate

Any body edit to a finalised document makes everything downstream stale:

```bash
python3 docpipe/docpipe.py update          # marks stale phases, rebuilds PSD.md — no model call
python3 docpipe/docpipe.py update --apply  # + runs `claude -p` on each stale phase with the exact upstream
                                           #   body diff injected; lands as status=revised for human review
python3 docpipe/docpipe.py finalise 3      # after review, re-lock; repeat down the chain
```

Both forms are idempotent. Structure is free to change while a document is draft and locked once final, so downstream derivations and approvals keep their targets.

## Compile

```bash
python3 docpipe/docpipe.py build           # docs/spec/PSD.md + docs/spec/traceability.csv
python3 docpipe/docpipe.py status
```

`PSD.md` is generated — edit the phase documents, never the PSD. `traceability.csv` is produced only when an identifier pattern is set: for every identifier, the phase that defines it, the phases that reference it, and the count.

## Conventions (`docpipe.json`)

| key | set by | effect |
|---|---|---|
| `intended_purpose` | phase 1 | injected into every prompt; the test every structural decision is judged by |
| `project_name`, `system_name` | phase 1 | naming in prompts |
| `id_pattern` | phase 1 (or never) | regex for identifiers; enables unresolved-reference and coverage checks and the traceability export. Identifier *families* (the pattern with digits removed) are homed in the phase where they first appear; a downstream token of an upstream family that upstream never defined is flagged |
| `requirements_syntax` | phase 1 or 5 | `ears` enables the EARS shape check on phase 5 (keyword start, exactly one "shall", every requirement row has one) |
| `coverage` | default `{"6": 5}` | phase 6 must reference every identifier phase 5 defines |
| `runner_interactive`, `runner_headless` | you | shell templates with `{prompt}` and `{message}`; defaults target Claude Code |
| `open_marker` | default `{{TBD` | what counts as an open item |

`python3 docpipe/docpipe.py set <key> "<value>"` writes one; the interview calls it.

## Layout

```
docpipe/
  docpipe.py            the script (stdlib only)
  prompts/              00-orchestrator (build protocol), 01–07 (purpose, what downstream needs, question bank), revise
  templates/            title-only stubs
  claude-commands/      /docpipe slash command
  evals/                test_script.sh (script layer), promptfooconfig.yaml + cases.md (prompt layer)
  EVIDENCE.md           standards the design leans on, with sources
  DESIGN_NOTES.md       choices, open questions, what to change first
docs/spec/              (created by init) 00-idea … 07-approvals, PSD.md, traceability.csv
.docpipe/               prompts (gitignored) and upstream snapshots (commit these)
docpipe.json            purpose, conventions, runners
```
