#!/usr/bin/env python3
"""
kms_search.py — KMS vault CLI (wraps ripgrep + Python yaml)

Auto-detects vault from its own location: this script lives in $VAULT/00_system/
So call it as: python3 /path/to/KMS/00_system/kms_search.py <command> [options]

Commands:
  search  "keyword" [--pillar NAME] [--type TYPE] [--limit N]
      Find pages containing keyword. Returns file, pillar, type, description.

  list    [--pillar NAME] [--json]
      List all wiki pages with metadata. Optionally filter by pillar.

  meta    PAGE
      Dump YAML frontmatter of a page as JSON.

  section PAGE SECTION
      Extract content of a named section (e.g. "Connections", "Insights").

  links   PAGE
      List all [[wikilinks]] found in a page.

  backlinks PAGE
      Find all wiki pages that link to [[PAGE]].

  projects [--status active|one_day]
      List all projects from /04_project/ with their YAML metadata.
"""

from __future__ import annotations  # keeps `Path | None` valid on python 3.9 (/usr/bin/python3)

import argparse, json, os, re, subprocess, sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # PyYAML missing (e.g. homebrew python3) — use fallback parser
    yaml = None

# Auto-detect vault root: this script is at $VAULT/00_system/kms_search.py
VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "02_wiki"
PROJECTS = VAULT / "04_project"


# ── helpers ──────────────────────────────────────────────────────────────────

def _fallback_frontmatter(block: str) -> dict:
    """Minimal key: value frontmatter parser, used when PyYAML is unavailable.

    Handles the subset of YAML actually used in this vault: flat `key: value`
    pairs plus `- item` list entries. Nested mappings are ignored.
    """
    meta: dict = {}
    current_list_key = None
    for line in block.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        list_item = re.match(r"^\s+-\s+(.*)$", line)
        if list_item and current_list_key:
            meta.setdefault(current_list_key, []).append(
                list_item.group(1).strip().strip('"').strip("'")
            )
            continue
        pair = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if pair:
            key, val = pair.group(1).strip(), pair.group(2).strip()
            if val == "":
                current_list_key = key
                meta.setdefault(key, [])
            else:
                current_list_key = None
                meta[key] = val.strip('"').strip("'")
    return meta


def parse_frontmatter(text: str):
    """Return (meta_dict, body_text) from a markdown file."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end]
    if yaml is not None:
        try:
            meta = yaml.safe_load(block) or {}
        except Exception:
            meta = _fallback_frontmatter(block)
    else:
        meta = _fallback_frontmatter(block)
    if not isinstance(meta, dict):
        meta = {}
    return meta, text[end + 4:].lstrip("\n")


def find_page(name: str) -> Path | None:
    """Locate a page file by name (with or without .md, with or without path)."""
    p = Path(name)
    if p.is_absolute() and p.exists():
        return p
    # Try as-is relative to vault
    candidates = [
        VAULT / name,
        VAULT / (name + ".md"),
    ]
    for c in candidates:
        if c.exists():
            return c
    # Search recursively in wiki + projects
    for base in [WIKI, PROJECTS]:
        for found in base.rglob(p.name if p.suffix else p.name + ".md"):
            return found
    return None


def _python_grep(pattern: str, path: str, ignore_case=False, files_only=False):
    """Pure-python stand-in for ripgrep over *.md, used when `rg` is unavailable."""
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error:
        regex = re.compile(re.escape(pattern), flags)
    out = []
    for f in sorted(Path(path).rglob("*.md")):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if files_only:
            if regex.search(text):
                out.append(str(f))
        else:
            for i, line in enumerate(text.split("\n"), 1):
                if regex.search(line):
                    out.append(f"{f}:{i}:{line}")
    return out


def rg(pattern: str, path: str, extra_flags: list = None, files_only=False):
    """Run ripgrep and return stdout lines, falling back to python if rg is absent.

    `rg` may be shadowed by a shell function rather than a real binary, so a
    subprocess call raises FileNotFoundError. Fall back rather than crash.
    """
    cmd = ["rg", "--glob", "*.md"]
    if files_only:
        cmd.append("-l")
    if extra_flags:
        cmd.extend(extra_flags)
    cmd.extend([pattern, path])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except (FileNotFoundError, OSError):
        return _python_grep(
            pattern, path,
            ignore_case=bool(extra_flags and "-i" in extra_flags),
            files_only=files_only,
        )
    return [l for l in result.stdout.strip().split("\n") if l]


# ── commands ─────────────────────────────────────────────────────────────────

def cmd_search(args):
    search_dir = str(WIKI / args.pillar) if args.pillar else str(WIKI)
    files = rg(args.keyword, search_dir, extra_flags=["-i"], files_only=True)
    # Exclude index files and lint folder
    files = [f for f in files
             if not Path(f).name.startswith("_")
             and "/lint/" not in f]

    rows = []
    for f in files:
        try:
            meta, _ = parse_frontmatter(Path(f).read_text())
        except Exception:
            meta = {}
        if args.type and meta.get("type", "").lower() != args.type.lower():
            continue
        rows.append({
            "file": str(Path(f).relative_to(VAULT)),
            "name": meta.get("name", Path(f).stem),
            "pillar": meta.get("pillar", ""),
            "type": meta.get("type", ""),
            "description": meta.get("description", ""),
        })

    rows = rows[:args.limit]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for r in rows:
            print(f"{r['file']}")
            print(f"  [{r['pillar']} | {r['type']}] {r['description'][:80]}")
            print()


def cmd_list(args):
    search_dir = WIKI / args.pillar if args.pillar else WIKI
    rows = []
    for f in sorted(search_dir.rglob("*.md")):
        if f.name.startswith("_"):
            continue
        # Exclude lint folder
        if "lint" in f.parts:
            continue
        try:
            meta, _ = parse_frontmatter(f.read_text())
        except Exception:
            meta = {}
        rows.append({
            "file": str(f.relative_to(VAULT)),
            "name": meta.get("name", f.stem),
            "pillar": meta.get("pillar", ""),
            "type": meta.get("type", ""),
            "status": meta.get("status", ""),
            "updated": str(meta.get("updated", "")),
            "description": meta.get("description", ""),
        })

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        fmt = "{:<50} {:<12} {:<10} {:<12} {}"
        print(fmt.format("File", "Pillar", "Type", "Updated", "Description"))
        print("─" * 110)
        for r in rows:
            print(fmt.format(
                r["file"][:50],
                r["pillar"][:12],
                r["type"][:10],
                r["updated"][:10],
                r["description"][:40],
            ))


def cmd_meta(args):
    f = find_page(args.page)
    if not f:
        print(f"Page not found: {args.page}", file=sys.stderr)
        sys.exit(1)
    meta, _ = parse_frontmatter(f.read_text())
    print(json.dumps(meta, indent=2, default=str))


def cmd_section(args):
    f = find_page(args.page)
    if not f:
        print(f"Page not found: {args.page}", file=sys.stderr)
        sys.exit(1)
    content = f.read_text()
    target = args.section.lstrip("#").strip()
    in_section = False
    lines = []
    for line in content.split("\n"):
        if re.match(r"^#{1,4}\s+" + re.escape(target) + r"\s*$", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if re.match(r"^#{1,4}\s", line):
                break
            lines.append(line)
    print("\n".join(lines).strip())


def cmd_links(args):
    f = find_page(args.page)
    if not f:
        print(f"Page not found: {args.page}", file=sys.stderr)
        sys.exit(1)
    links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", f.read_text())
    for link in sorted(set(links)):
        print(f"[[{link}]]")


def cmd_backlinks(args):
    page = args.page.replace("[[", "").replace("]]", "")
    files = rg(re.escape(f"[[{page}]]"), str(WIKI), files_only=True)
    for f in files:
        print(str(Path(f).relative_to(VAULT)))


def find_project_files() -> list[Path]:
    """Return every canonical project file under /04_project/.

    Canonical marker is `project_id: pjXXXX` in frontmatter — same rule as
    scripts/sync-context.py. Keying on the marker rather than on
    `<dirname>/<dirname>.md` means this also finds:
      - nested projects (e.g. Training/Meal_prep_routine/)
      - overview files named differently from their folder (LMS.md, App_Vision.md)
    Support docs (Architecture.md, Dev_Log.md, CLAUDE.md) have no project_id
    and are skipped automatically.
    """
    found = []
    for path in sorted(PROJECTS.rglob("*.md")):
        if path.name == "CLAUDE.md" or path.stem.startswith("_"):
            continue
        if any(part.startswith("_") for part in path.relative_to(PROJECTS).parts):
            continue
        try:
            meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(meta.get("project_id", "")).startswith("pj"):
            found.append(path)
    return found


def cmd_projects(args):
    rows = []
    for overview in find_project_files():
        try:
            meta, _ = parse_frontmatter(overview.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        if args.status and meta.get("status", "active") != args.status:
            continue
        rel = overview.relative_to(PROJECTS)
        rows.append({
            "name": meta.get("name") or overview.stem,
            "project_id": str(meta.get("project_id", "")),
            "pillar": meta.get("pillar", ""),
            "priority": meta.get("priority", ""),
            "execution_state": meta.get("execution_state", ""),
            "status": meta.get("status", "active"),
            "current_focus": meta.get("current_focus", ""),
            "updated": str(meta.get("updated", "")),
            "path": str(overview.relative_to(VAULT)),
            "nested": len(rel.parts) > 2,
        })
    rows.sort(key=lambda r: r["project_id"])

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        fmt = "{:<8} {:<28} {:<18} {:<10} {:<8} {:<10} {}"
        print(fmt.format("ID", "Project", "Pillar", "ExecState", "Status", "Updated", "Current Focus"))
        print("─" * 120)
        for r in rows:
            print(fmt.format(
                r["project_id"][:8],
                (r["name"] + (" *" if r["nested"] else ""))[:28],
                str(r["pillar"])[:18],
                str(r["execution_state"])[:10],
                str(r["status"])[:8],
                r["updated"][:10],
                str(r["current_focus"])[:45],
            ))
        if any(r["nested"] for r in rows):
            print("\n* nested under a parent project folder")


# ── CLI wiring ────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(
    description="KMS vault CLI — search, list, and inspect your Obsidian KMS",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
sub = parser.add_subparsers(dest="command", metavar="command")

# search
p = sub.add_parser("search", help="Find pages containing keyword")
p.add_argument("keyword", help="Search term (case-insensitive)")
p.add_argument("--pillar", default=None, help="Limit to a specific pillar folder")
p.add_argument("--type", default=None, help="Filter by page type (concept/practice/topic/synthesis)")
p.add_argument("--limit", type=int, default=10, help="Max results (default 10)")
p.add_argument("--json", action="store_true", help="Output as JSON")
p.set_defaults(func=cmd_search)

# list
p = sub.add_parser("list", help="List all wiki pages with metadata")
p.add_argument("--pillar", default=None, help="Limit to a specific pillar folder")
p.add_argument("--json", action="store_true", help="Output as JSON")
p.set_defaults(func=cmd_list)

# meta
p = sub.add_parser("meta", help="Dump YAML frontmatter of a page")
p.add_argument("page", help="Page name or path (with or without .md)")
p.add_argument("--json", action="store_true", help="Output as JSON (default)")
p.set_defaults(func=cmd_meta)

# section
p = sub.add_parser("section", help="Extract a named section from a page")
p.add_argument("page", help="Page name or path")
p.add_argument("section", help="Section heading (e.g. 'Connections', 'Insights')")
p.set_defaults(func=cmd_section)

# links
p = sub.add_parser("links", help="List all [[wikilinks]] in a page")
p.add_argument("page", help="Page name or path")
p.set_defaults(func=cmd_links)

# backlinks
p = sub.add_parser("backlinks", help="Find pages that link to [[PAGE]]")
p.add_argument("page", help="Page name (without [[]])")
p.set_defaults(func=cmd_backlinks)

# projects
p = sub.add_parser("projects", help="List all projects with metadata")
p.add_argument("--status", default=None, help="Filter by status (active, one_day)")
p.add_argument("--json", action="store_true", help="Output as JSON")
p.set_defaults(func=cmd_projects)

args = parser.parse_args()
if args.command:
    args.func(args)
else:
    parser.print_help()
