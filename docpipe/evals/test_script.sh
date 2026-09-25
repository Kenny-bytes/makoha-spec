#!/usr/bin/env bash
# Script-layer tests S1–S12 (see cases.md). Stdlib python + git only. Exit non-zero on first failure.
# The script must impose nothing: every check is driven by conventions the phase-1 interview records.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cd "$T" && git init -q && cp -r "$HERE" docpipe
DP="python3 docpipe/docpipe.py"
fail() { echo "FAIL $1"; exit 1; }
ok() { echo "ok   $1"; }

$DP init >/dev/null
$DP init | grep -q "nothing to do" && ok S1 || fail S1
out=$($DP prompt 2 2>&1 || true); grep -q "gate:" <<<"$out" && ok S2 || fail S2

# S3: templates carry no structure and no identifiers; check flags the missing structure, nothing else
out=$($DP check 1 2>&1 || true); grep -q "no structure yet" <<<"$out" && ! grep -qi "unresolved\|EARS" <<<"$out" && ok S3 || fail S3

body() { python3 - "$1" "$2" <<'EOF'
import re,sys,pathlib
p=pathlib.Path(sys.argv[1]); t=p.read_text(); m=re.match(r"^---\n.*?\n---\n",t,re.S)
p.write_text(m.group(0)+pathlib.Path(sys.argv[2]).read_text())
EOF
}
echo "A GP-facing checker that flags drug interactions when a script is saved." > docs/spec/00-idea.md

# S4: with no conventions set, identifiers in text are just text; no reference checks run
cat > b1.md <<'EOF'
# PRD
## Users
GP in clinic (U-01).
## Outcomes
Fewer missed interactions (G-01).
## Capabilities
Alert on save (F-01) serves G-01.
## Constraints
AU vocabulary only (C-01), source TGA.
EOF
body docs/spec/01-prd.md b1.md
$DP check 1 && ok S4 || fail S4

# S5: the interview sets the conventions via `set`; an invalid regex is refused
out=$($DP set id_pattern '[' 2>&1 || true); grep -q "not a valid regex" <<<"$out" && ok S5 || fail S5
$DP set intended_purpose "hand-off to coding agents" >/dev/null
$DP set id_pattern '\b[A-Z]{1,3}-\d{2,3}\b' >/dev/null
$DP set requirements_syntax ears >/dev/null
grep -q '"requirements_syntax": "ears"' docpipe.json || fail "S5 config write"

cat > b2.md <<'EOF'
# ConOps
## Situations
Prescribe (S-01): GP saves script → alert. Actors U-01. Outcome G-01.
EOF
cat > b3.md <<'EOF'
# OpsCon
## Modes
Normal (M-01); Degraded (M-02) when the interaction table is unreachable.
## Scenarios
Prescribe (SC-01), refines S-01: 1. GP saves script 2. system checks interactions 3. alert shown.
## Interfaces
Practice management system (I-01), owner vendor.
## Expectations
Alert within 2 s of save (P-01).
EOF
cat > b4.md <<'EOF'
# TechSpec
## Targets
Latency p95 < 2 s (N-01) from P-01, measured by k6.
## Interfaces
FHIR REST (TI-01) realises I-01.
EOF
cat > b5.md <<'EOF'
# Requirements
## Functional
| Ref | Requirement | Traces | Verify | Accept |
|---|---|---|---|---|
| R-001 | When a script is saved, the CDSS shall check it against the interaction table | SC-01; F-01 | Test | alert row present |
| R-101 | The CDSS shall return an interaction result within 2 s p95 | P-01; N-01 | Test | k6 p95 < 2 s |
| R-301 | If the interaction table is unavailable, then the CDSS shall show a degraded banner | M-02; C-01 | Test | banner visible |
| R-302 | The system must be fast | SC-01 | Test | n/a |
| R-303 | When x, the CDSS shall y and shall z | SC-99 | Test | z |
EOF
for n in 2 3 4 5; do body docs/spec/0$n-*.md b$n.md; done

# S6: with conventions set — unresolved reference and EARS shape both caught, only those
out=$($DP check 5 2>&1 || true)
grep -q "unresolved references: SC-99" <<<"$out" && ok S6a || fail "S6a: $out"
grep -q "not EARS-shaped" <<<"$out" && grep -q "no .shall.: The system must be fast" <<<"$out" && grep -q "two shalls" <<<"$out" && ok S6b || fail "S6b: $out"

sed -i '/R-302/d;/R-303/d' docs/spec/05-requirements.md
$DP check 5 && ok S7 || fail S7

# S8: coverage — phase 6 must reference every identifier phase 5 defines
cat > b6.md <<'EOF'
# Validation
## Register
| Entry | Req | Activity | Method | Evidence | Complete | Modification | CR |
|---|---|---|---|---|---|---|---|
| V-001 | R-001 | unit test | Test | tests/t1 | y | n | |
| V-002 | R-101 | k6 run | Test | ci/k6 | n | y | CR-001 |
## Change requests
CR-001: TechSpec N-01 — relax to 5 s.
EOF
body docs/spec/06-validation.md b6.md
out=$($DP check 6 2>&1 || true); grep -q "not covered here: R-301" <<<"$out" && ok S8 || fail "S8: $out"
printf '%s\n' "| V-003 | R-301 | banner test | Test | tests/t3 | n | n | |" >> docs/spec/06-validation.md

for n in 1 2 3 4 5 6; do $DP finalise $n >/dev/null; done
$DP build >/dev/null
# S9: generic traceability — definition phase and downstream references, no scheme knowledge
grep -q '^R-101,5,"6",1' docs/spec/traceability.csv && grep -q '^P-01,3,"4;5",' docs/spec/traceability.csv && grep -q '^G-01,1,"2",' docs/spec/traceability.csv && ok S9 || { cat docs/spec/traceability.csv; fail S9; }

out=$($DP update); grep -q "no status changes" <<<"$out" && ok S10a || fail S10a
# S11: frontmatter-only change upstream must not cascade
sed -i 's/^version: 1.0/version: 1.1/' docs/spec/02-conops.md
out=$($DP update); grep -q "no status changes" <<<"$out" && ok S11 || fail S11
# S12: body edit cascades to every finalised dependant; revise prompt carries body-only diff; no placeholders left
echo "Dose check (F-02) serves G-01." >> docs/spec/01-prd.md
out=$($DP update)
for n in 2 3 4 5; do grep -q "phase $n " <<<"$out" || fail "S12 phase $n"; done
grep -q "phase 6 " <<<"$out" && fail "S12 phase 6 must not be stale" || true
grep -q "| STALE |" docs/spec/PSD.md || fail "S12 register"
out=$($DP update); grep -q "no status changes" <<<"$out" && ok S10b || fail S10b
python3 - <<'EOF' && ok S12 || fail S12
import sys, pathlib; sys.argv=["x"]; sys.path.insert(0,"docpipe"); import docpipe
root=pathlib.Path(".").resolve(); cfg=docpipe.load_config(root)
t=docpipe.assemble(cfg, root, 3, "revise")
blk=t.split("<upstream_changes>")[1].split("</upstream_changes>")[0]
assert '<diff document="01-prd.md">' in blk and "+Dose check (F-02)" in blk, "diff missing"
assert "version:" not in blk, "frontmatter leaked into diff"
assert '"id_pattern"' in t and 'hand-off to coding agents' in t, "conventions block missing"
assert not any(x in t for x in ("{{DOC_PATH}}","{{PHASE_N}}","{{DOCPIPE}}","{{DOCS_DIR}}","{{DOC_TITLE}}","{{INTENDED_PURPOSE}}")), "unresolved placeholder"
EOF
echo "all script-layer tests passed"
