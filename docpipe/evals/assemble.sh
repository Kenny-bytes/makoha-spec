#!/usr/bin/env bash
# promptfoo prompt function: assemble the docpipe prompt for a fixture + phase, then append the user turn.
# promptfoo passes vars as JSON on stdin.
set -euo pipefail
vars=$(cat)
fixture=$(echo "$vars" | python3 -c 'import sys,json;print(json.load(sys.stdin)["vars"]["fixture"])')
phase=$(echo "$vars" | python3 -c 'import sys,json;print(json.load(sys.stdin)["vars"]["phase"])')
mode=$(echo "$vars" | python3 -c 'import sys,json;print(json.load(sys.stdin)["vars"].get("mode","interview"))')
turn=$(echo "$vars" | python3 -c 'import sys,json;print(json.load(sys.stdin)["vars"]["turn"])')
here=$(cd "$(dirname "$0")/.." && pwd)
python3 - "$here" "$fixture" "$phase" "$mode" <<'EOF'
import sys, pathlib
here, fixture, phase, mode = sys.argv[1:]
sys.path.insert(0, here)
import docpipe
root = pathlib.Path(fixture).resolve()
cfg = docpipe.load_config(root)
cfg["prompts_dir"] = str(pathlib.Path(here) / "prompts")
print(docpipe.assemble(cfg, root, int(phase), mode))
EOF
printf '\n<user_turn>\n%s\n</user_turn>\n' "$turn"
