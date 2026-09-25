#!/usr/bin/env python3
"""
docpipe — phase-gated, interview-driven design documentation for a repo.

IDEA -> 1 PRD -> 2 ConOps -> 3 OpsCon -> 4 TechSpec -> 5 Requirements
     -> 6 Validation -> 7 Approvals -> PSD.md (compiled Product Specification Document)

Greenfield by design: the script imposes no document structure and no identifier
scheme. Each phase's interview builds the document's structure for the set's
intended purpose. Phase 1 establishes the conventions (identifier pattern,
requirement syntax) and records them in docpipe.json; every check below reads
them from there and does nothing when they are unset.

Commands
  init                      scaffold docs/spec (idempotent)
  status                    phase table: draft / final / stale, open items
  prompt N [--stdout]       assemble the phase-N interview prompt (upstream injected)
  run N                     open an interactive Claude session on phase N
  check N                   lint: open markers, unresolved references, coverage
  finalise N [--force]      lock phase N, snapshot upstream, unlock N+1
  update [--apply]          re-hash upstream; mark stale; --apply runs headless revision
  build                     compile PSD.md, traceability.csv, register
  set KEY VALUE             write a convention into docpipe.json (used by the phase-1 interview)

Stdlib only. Python 3.9+.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_NAME = "docpipe.json"

# n, slug, title, upstream phase numbers (0 = the idea)
PHASES = [
    (1, "prd", "Product Requirements Document", [0]),
    (2, "conops", "Concept of Operations", [0, 1]),
    (3, "opscon", "Operations Concept", [1, 2]),
    (4, "techspec", "Technical Specifications", [1, 3]),
    (5, "requirements", "Specific Requirements", [1, 3, 4]),
    (6, "validation", "Validation Activities", [5]),
    (7, "approvals", "Completion and Approvals", [1, 2, 3, 4, 5, 6]),
]
PHASE_BY_N = {p[0]: p for p in PHASES}
IDEA_FILE = "00-idea.md"

DEFAULT_CONFIG = {
    "docs_dir": "docs/spec",
    "prompts_dir": str(HERE / "prompts"),
    "templates_dir": str(HERE / "templates"),
    "state_dir": ".docpipe",
    "project_name": "",
    "system_name": "",
    # What the finished set is for. Every structural decision in every phase is judged against it.
    "intended_purpose": "",
    # Conventions the phase-1 interview establishes. Empty = not yet decided; checks are skipped.
    "id_pattern": "",                 # regex for identifiers, e.g. "\\b[A-Z]{2,4}-\\d{2,4}\\b"
    "requirements_syntax": "",        # "ears" enables the EARS shape check on phase 5; "" disables
    # coverage: {"6": 5} means every identifier first defined in phase 5 must be referenced in phase 6
    "coverage": {"6": 5},
    # Runner templates. {prompt} = assembled prompt file, {message} = first user turn.
    "runner_interactive": "claude --append-system-prompt-file {prompt}",
    "runner_headless": (
        "claude -p --bare --append-system-prompt-file {prompt} "
        "--permission-mode acceptEdits --allowedTools Read,Edit,Write,Glob,Grep "
        "--output-format json {message}"
    ),
    "open_marker": "{{TBD",
}

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
EARS_RE = re.compile(r"^\s*(The|When|While|If|Where)\b.*\bshall\b", re.I)


def load_config(root: Path) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    p = root / CONFIG_NAME
    if p.exists():
        cfg.update(json.loads(p.read_text()))
    return cfg


def save_config(root: Path, cfg: dict) -> None:
    keys = [k for k in DEFAULT_CONFIG] + [k for k in cfg if k not in DEFAULT_CONFIG]
    (root / CONFIG_NAME).write_text(json.dumps({k: cfg[k] for k in keys}, indent=2) + "\n")


def find_root() -> Path:
    cur = Path.cwd()
    for c in [cur, *cur.parents]:
        if (c / CONFIG_NAME).exists() or (c / ".git").exists():
            return c
    return cur


# --------------------------------------------------------------------------- doc io

def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v[:1] in "[{":
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                pass
        meta[k.strip()] = v
    return meta, text[m.end():]


def dump_frontmatter(meta: dict) -> str:
    out = ["---"]
    for k, v in meta.items():
        if isinstance(v, (list, dict)):
            v = json.dumps(v)
        out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out) + "\n"


def sha(path: Path) -> str:
    """Hash of the document body only — frontmatter status changes must not cascade."""
    _, body = parse_frontmatter(path.read_text())
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def doc_path(cfg: dict, root: Path, n: int) -> Path:
    if n == 0:
        return root / cfg["docs_dir"] / IDEA_FILE
    _, slug, *_ = PHASE_BY_N[n]
    return root / cfg["docs_dir"] / f"{n:02d}-{slug}.md"


def read_doc(cfg, root, n):
    p = doc_path(cfg, root, n)
    if not p.exists():
        return None, {}, ""
    meta, body = parse_frontmatter(p.read_text())
    return p, meta, body


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def open_markers(cfg, text: str) -> list[str]:
    m = cfg["open_marker"]
    out, i = [], 0
    while True:
        i = text.find(m, i)
        if i < 0:
            return out
        j = text.find("}}", i)
        out.append(text[i:(j + 2) if j > 0 else i + 40])
        i = i + len(m)


def id_regex(cfg):
    return re.compile(cfg["id_pattern"]) if cfg.get("id_pattern") else None


def ids_in(cfg, text: str) -> list[str]:
    rx = id_regex(cfg)
    return rx.findall(text) if rx else []


def family(i: str) -> str:
    """An identifier's family is its shape with digits removed (R-001 -> R-)."""
    return re.sub(r"\d+", "", i)


def definitions_by_phase(cfg, root) -> dict[int, list[str]]:
    """An identifier is 'defined' in the earliest phase where its family appears; an identifier of
    a family homed upstream that first shows up downstream is a dangling reference, not a definition."""
    seen, home, out = set(), {}, {}
    for n in range(0, 8):
        p, _, body = read_doc(cfg, root, n)
        out[n] = []
        if p is None:
            continue
        for i in ids_in(cfg, body):
            if i in seen:
                continue
            seen.add(i)
            fam = family(i)
            home.setdefault(fam, n)
            if home[fam] == n:
                out[n].append(i)
    return out


# --------------------------------------------------------------------------- init / set

def cmd_init(cfg, root, args):
    docs = root / cfg["docs_dir"]
    docs.mkdir(parents=True, exist_ok=True)
    (root / cfg["state_dir"] / "snapshots").mkdir(parents=True, exist_ok=True)
    tdir = Path(cfg["templates_dir"])
    made = []
    if not (root / CONFIG_NAME).exists():
        save_config(root, cfg)
        made.append(CONFIG_NAME)
    idea = doc_path(cfg, root, 0)
    if not idea.exists():
        shutil.copy(tdir / "00-idea.md", idea)
        made.append(idea.name)
    for n, slug, title, ups in PHASES:
        p = doc_path(cfg, root, n)
        if p.exists():
            continue
        meta = {
            "docpipe": 1, "phase": n, "title": title,
            "status": "draft", "version": "0.1",
            "upstream": [doc_path(cfg, root, u).name for u in ups],
            "upstream_hash": {}, "finalised": "",
        }
        p.write_text(dump_frontmatter(meta) + (tdir / f"{n:02d}-{slug}.md").read_text())
        made.append(p.name)
    gi = root / ".gitignore"
    line = f"{cfg['state_dir']}/prompts/\n"
    if not gi.exists() or line not in gi.read_text():
        with gi.open("a") as f:
            f.write(line)
    print("initialised:", ", ".join(made) if made else "nothing to do (already initialised)")
    print(f"next: write {idea.relative_to(root)} then `docpipe run 1`")


def cmd_set(cfg, root, args):
    key, value = args.key, args.value
    if key not in DEFAULT_CONFIG:
        sys.exit(f"unknown key {key}; known: {', '.join(DEFAULT_CONFIG)}")
    if isinstance(DEFAULT_CONFIG[key], dict):
        value = json.loads(value)
    if key == "id_pattern" and value:
        try:
            re.compile(value)
        except re.error as e:
            sys.exit(f"id_pattern is not a valid regex: {e}")
    cfg[key] = value
    save_config(root, cfg)
    print(f"{key} = {value!r}")


# --------------------------------------------------------------------------- status

def upstream_state(cfg, root, n) -> tuple[dict, bool]:
    _, meta, _ = read_doc(cfg, root, n)
    cur = {}
    for u in PHASE_BY_N[n][3]:
        p = doc_path(cfg, root, u)
        cur[p.name] = sha(p) if p.exists() else "missing"
    recorded = meta.get("upstream_hash") or {}
    stale = meta.get("status") in ("final", "stale", "revised") and recorded and recorded != cur
    return cur, bool(stale)


def cmd_status(cfg, root, args):
    print(f"purpose: {cfg['intended_purpose'] or '(unset — phase 1 asks for it)'}")
    print(f"conventions: id_pattern={cfg['id_pattern'] or '(unset)'}  requirements_syntax={cfg['requirements_syntax'] or '(unset)'}\n")
    print(f"{'ph':>2}  {'document':<22} {'status':<8} {'ver':<5} {'open':>4}  {'stale':<5} upstream")
    idea = doc_path(cfg, root, 0)
    itxt = idea.read_text() if idea.exists() else ""
    print(f"{0:>2}  {IDEA_FILE:<22} {'seed':<8} {'-':<5} {len(open_markers(cfg, itxt)):>4}  {'-':<5} -")
    prev_final = idea.exists() and len(itxt.strip()) > 0
    for n, slug, title, ups in PHASES:
        p, meta, body = read_doc(cfg, root, n)
        if p is None:
            print(f"{n:>2}  (missing — run init)")
            continue
        cur, stale = upstream_state(cfg, root, n)
        status = "STALE" if stale else meta.get("status", "?")
        gate = "" if prev_final else "  [blocked: upstream not final]"
        print(f"{n:>2}  {p.name:<22} {status:<8} {meta.get('version','?'):<5} "
              f"{len(open_markers(cfg, body)):>4}  {'yes' if stale else 'no':<5} {', '.join(cur)}{gate}")
        prev_final = meta.get("status") == "final" and not stale


# --------------------------------------------------------------------------- prompt assembly

def wrap_doc(tag: str, path: Path, text: str, **attrs) -> str:
    a = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag} path=\"{path.name}\" {a}>\n{text.rstrip()}\n</{tag}>\n"


def assemble(cfg, root, n, mode="interview") -> str:
    pdir = Path(cfg["prompts_dir"])
    _, slug, title, ups = PHASE_BY_N[n]
    parts = ["<upstream_documents>"]
    for u in ups:
        p, meta, body = read_doc(cfg, root, u)
        if p is None:
            continue
        parts.append(wrap_doc("document", p, body, phase=u, title=meta.get("title", "Idea"),
                              status=meta.get("status", "seed"), version=meta.get("version", "-")))
    parts.append("</upstream_documents>\n")
    p, meta, body = read_doc(cfg, root, n)
    parts.append(wrap_doc("current_document", p, body, phase=n, title=title, status=meta.get("status", "draft")))
    if mode == "revise":
        parts.append("<upstream_changes>")
        snapdir = root / cfg["state_dir"] / "snapshots" / f"{n:02d}"
        for u in ups:
            up = doc_path(cfg, root, u)
            old = snapdir / up.name
            if old.exists() and up.exists():
                _, old_body = parse_frontmatter(old.read_text())
                _, new_body = parse_frontmatter(up.read_text())
                d = "\n".join(difflib.unified_diff(
                    old_body.splitlines(), new_body.splitlines(),
                    fromfile=f"{up.name}@finalised", tofile=f"{up.name}@now", lineterm=""))
                if d:
                    parts.append(f"<diff document=\"{up.name}\">\n{d}\n</diff>")
        parts.append("</upstream_changes>\n")
    conv = {k: cfg[k] for k in ("project_name", "system_name", "intended_purpose", "id_pattern", "requirements_syntax")}
    parts.append("<conventions>\n" + json.dumps(conv, indent=2) + "\n</conventions>\n")
    parts.append((pdir / "00-orchestrator.md").read_text())
    parts.append((pdir / f"{n:02d}-{slug}.md").read_text())
    if mode == "revise":
        parts.append((pdir / "revise.md").read_text())
    text = "\n".join(parts)
    script = Path(__file__).resolve()
    try:
        script = script.relative_to(root)
    except ValueError:
        pass
    for k, v in {
        "{{DOC_PATH}}": str(p.relative_to(root)), "{{PHASE_N}}": str(n), "{{DOCPIPE}}": str(script),
        "{{DOCS_DIR}}": cfg["docs_dir"], "{{DOC_TITLE}}": title,
        "{{PROJECT_NAME}}": cfg["project_name"] or "(unnamed project)",
        "{{SYSTEM_NAME}}": cfg["system_name"] or "the system",
        "{{INTENDED_PURPOSE}}": cfg["intended_purpose"] or "(not yet stated — establish it first)",
    }.items():
        text = text.replace(k, v)
    return text


def write_prompt(cfg, root, n, mode="interview") -> Path:
    out = root / cfg["state_dir"] / "prompts" / f"{mode}-{n:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(assemble(cfg, root, n, mode))
    return out


def gate_ok(cfg, root, n) -> tuple[bool, str]:
    for u in PHASE_BY_N[n][3]:
        if u == 0:
            idea = doc_path(cfg, root, 0)
            if not idea.exists() or not idea.read_text().strip():
                return False, "00-idea.md is missing or empty"
            continue
        _, meta, _ = read_doc(cfg, root, u)
        _, stale = upstream_state(cfg, root, u)
        if meta.get("status") != "final" or stale:
            return False, f"phase {u} is not final (status={meta.get('status')}, stale={stale})"
    return True, ""


def cmd_prompt(cfg, root, args):
    ok, why = gate_ok(cfg, root, args.n)
    if not ok and not args.force:
        sys.exit(f"gate: {why}. Use --force to assemble anyway.")
    if args.stdout:
        print(assemble(cfg, root, args.n))
    else:
        print(write_prompt(cfg, root, args.n))


def cmd_run(cfg, root, args):
    ok, why = gate_ok(cfg, root, args.n)
    if not ok and not args.force:
        sys.exit(f"gate: {why}. Use --force to run anyway.")
    prompt = write_prompt(cfg, root, args.n)
    cmd = cfg["runner_interactive"].format(prompt=str(prompt))
    print(f"$ {cmd}\n(first message to send: 'Begin phase {args.n}.')")
    if shutil.which(cmd.split()[0]) is None:
        sys.exit(f"runner '{cmd.split()[0]}' not on PATH — paste {prompt} into your Claude session instead.")
    subprocess.call(cmd, shell=True, cwd=root)


# --------------------------------------------------------------------------- check

def check(cfg, root, n) -> list[str]:
    problems = []
    p, meta, body = read_doc(cfg, root, n)
    if p is None:
        return ["document missing"]
    if not body.strip() or len(re.findall(r"^#{1,6} ", body, re.M)) < 2:
        problems.append("document has no structure yet (fewer than two headings)")
    marks = open_markers(cfg, body)
    if marks:
        problems.append(f"{len(marks)} open marker(s): " + "; ".join(m[:60] for m in marks[:5]))
    rx = id_regex(cfg)
    defs = definitions_by_phase(cfg, root) if rx else {}
    if rx:
        known_upstream = {i for u in range(0, n) for i in defs[u]}
        here = set(ids_in(cfg, body))
        own = set(defs[n])
        unresolved = sorted(i for i in here if i not in known_upstream and i not in own)
        if unresolved:
            problems.append("unresolved references: " + ", ".join(unresolved[:10]))
        cov = cfg.get("coverage") or {}
        src = cov.get(str(n))
        if src is not None:
            missing = sorted(i for i in defs[int(src)] if i not in here)
            if missing:
                problems.append(f"{len(missing)} identifier(s) from phase {src} not covered here: " + ", ".join(missing[:10]))
    if n == 5 and cfg.get("requirements_syntax", "").lower() == "ears":
        own = set(defs.get(n, [])) if rx else set()
        bad, heading = [], ""
        for line in body.splitlines():
            if line.startswith("#"):
                heading = line.lower()
                continue
            if "withdrawn" in heading:
                continue
            is_req_row = bool(own and line.lstrip().startswith("|") and any(i in line for i in ids_in(cfg, line)))
            has_shall = bool(re.search(r"\bshall\b", line, re.I))
            if not (is_req_row or has_shall):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.lstrip().startswith("|") else [line.strip()]
            sentence = next((c for c in cells if re.search(r"\bshall\b", c, re.I)), None)
            if sentence is None:
                sentence = max(cells, key=len)
                bad.append("no 'shall': " + sentence[:50])
                continue
            if not EARS_RE.match(sentence):
                bad.append(sentence[:60])
            if len(re.findall(r"\bshall\b", sentence, re.I)) > 1:
                bad.append("two shalls: " + sentence[:50])
        if bad:
            problems.append(f"{len(bad)} requirement(s) not EARS-shaped: " + " | ".join(bad[:5]))
    return problems


def cmd_check(cfg, root, args):
    probs = check(cfg, root, args.n)
    if not probs:
        print(f"phase {args.n}: clean")
        return
    print(f"phase {args.n}: {len(probs)} finding(s)")
    for x in probs:
        print("  -", x)
    sys.exit(1)


# --------------------------------------------------------------------------- finalise

def bump(v: str) -> str:
    try:
        major, _ = v.split(".")
        return f"{int(major) + 1}.0"
    except ValueError:
        return "1.0"


def cmd_finalise(cfg, root, args):
    n = args.n
    p, meta, body = read_doc(cfg, root, n)
    ok, why = gate_ok(cfg, root, n)
    if not ok and not args.force:
        sys.exit(f"gate: {why}")
    probs = check(cfg, root, n)
    if probs and not args.force:
        print("not finalised — fix or --force:")
        for x in probs:
            print("  -", x)
        sys.exit(1)
    cur, _ = upstream_state(cfg, root, n)
    meta.update({"status": "final", "version": bump(meta.get("version", "0.1")),
                 "upstream_hash": cur, "finalised": date.today().isoformat()})
    p.write_text(dump_frontmatter(meta) + body)
    snapdir = root / cfg["state_dir"] / "snapshots" / f"{n:02d}"
    snapdir.mkdir(parents=True, exist_ok=True)
    for u in PHASE_BY_N[n][3]:
        up = doc_path(cfg, root, u)
        if up.exists():
            shutil.copy(up, snapdir / up.name)
    print(f"finalised {p.name} v{meta['version']}" + (f" — next: docpipe run {n + 1}" if n < 7 else " — run docpipe build"))


# --------------------------------------------------------------------------- update

def cmd_update(cfg, root, args):
    changed = False
    for n, slug, title, ups in PHASES:
        p, meta, body = read_doc(cfg, root, n)
        if p is None:
            continue
        cur, stale = upstream_state(cfg, root, n)
        if not stale:
            continue
        print(f"phase {n} ({p.name}): upstream changed since finalise")
        if args.apply:
            prompt = write_prompt(cfg, root, n, mode="revise")
            msg = json.dumps(f"Revise {p.relative_to(root)} against the upstream changes. Edit the file in place.")
            cmd = cfg["runner_headless"].format(prompt=str(prompt), message=msg)
            if shutil.which(cmd.split()[0]) is None:
                print(f"  runner not on PATH; revision prompt written to {prompt}")
                continue
            print(f"  $ {cmd}")
            r = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True)
            print("  exit", r.returncode)
            if r.returncode != 0:
                print(r.stderr[-2000:])
                continue
            p2, meta2, body2 = read_doc(cfg, root, n)
            meta2["status"] = "revised"
            meta2["upstream_hash"] = cur
            p2.write_text(dump_frontmatter(meta2) + body2)
            changed = True
            print(f"  {p.name} revised -> status=revised (review, then docpipe finalise {n})")
        elif meta.get("status") != "stale":
            meta["status"] = "stale"
            p.write_text(dump_frontmatter(meta) + body)
            changed = True
        else:
            print(f"  already marked stale — revise and `docpipe finalise {n}`, or `update --apply`")
    if not changed:
        print("no status changes")
    cmd_build(cfg, root, args)


# --------------------------------------------------------------------------- build

def cmd_build(cfg, root, args):
    docs = root / cfg["docs_dir"]
    register = ["| # | Document | Status | Version | Finalised | Hash |", "|---|---|---|---|---|---|"]
    sections = []
    idea = doc_path(cfg, root, 0)
    if idea.exists():
        sections.append(f"\n\n# 0. Idea\n\n{idea.read_text().strip()}\n")
    for n, slug, title, ups in PHASES:
        p, meta, body = read_doc(cfg, root, n)
        if p is None:
            continue
        _, stale = upstream_state(cfg, root, n)
        st = "STALE" if stale else meta.get("status", "?")
        register.append(f"| {n} | {title} | {st} | {meta.get('version','')} | {meta.get('finalised','')} | {sha(p)} |")
        sections.append(f"\n\n# {n}. {title}\n\n_status: {st} · version {meta.get('version','')}_\n\n{body.strip()}\n")
    # traceability: where each identifier is defined and which later documents reference it
    trace = ["identifier,defined_in_phase,referenced_in_phases,reference_count"]
    if id_regex(cfg):
        defs = definitions_by_phase(cfg, root)
        bodies = {n: (read_doc(cfg, root, n)[2] or "") for n in range(0, 8)}
        for dn in range(0, 8):
            for i in defs[dn]:
                refs = [str(m) for m in range(dn + 1, 8) if i in ids_in(cfg, bodies[m])]
                count = sum(bodies[m].count(i) for m in range(dn + 1, 8))
                trace.append(f"{i},{dn},\"{';'.join(refs)}\",{count}")
    head = (f"# {cfg['project_name'] or 'Project'} — Product Specification Document\n\n"
            f"Intended purpose: {cfg['intended_purpose'] or '(unset)'}\n\n"
            f"Compiled by docpipe from `{cfg['docs_dir']}`. Edit the phase documents, not this file.\n\n"
            "## Document register\n\n" + "\n".join(register) + "\n")
    w1 = write_if_changed(docs / "PSD.md", head + "".join(sections))
    w2 = write_if_changed(docs / "traceability.csv", "\n".join(trace) + "\n")
    print(f"build: PSD.md {'updated' if w1 else 'unchanged'}, traceability.csv {'updated' if w2 else 'unchanged'}")


# --------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(prog="docpipe", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="repo root (default: nearest docpipe.json or .git)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    for name in ("prompt", "run", "check", "finalise"):
        s = sub.add_parser(name)
        s.add_argument("n", type=int, choices=range(1, 8))
        s.add_argument("--force", action="store_true")
        if name == "prompt":
            s.add_argument("--stdout", action="store_true")
    u = sub.add_parser("update")
    u.add_argument("--apply", action="store_true", help="run headless revision on stale phases")
    sub.add_parser("build")
    st = sub.add_parser("set")
    st.add_argument("key")
    st.add_argument("value")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else find_root()
    cfg = load_config(root)
    {
        "init": cmd_init, "status": cmd_status, "prompt": cmd_prompt, "run": cmd_run,
        "check": cmd_check, "finalise": cmd_finalise, "update": cmd_update, "build": cmd_build,
        "set": cmd_set,
    }[args.cmd](cfg, root, args)


if __name__ == "__main__":
    main()
