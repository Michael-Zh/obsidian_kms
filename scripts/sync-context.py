#!/usr/bin/env python3
"""
sync-context.py — Parse KMS vault markdown and upsert to Supabase.

Reads from the local KMS vault checkout (or GITHUB_WORKSPACE in CI).
Upserts context_snapshots (POS, priority) and projects_state (active projects).

Usage:
  SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... VAULT_PATH=/path/to/vault python3 scripts/sync-context.py
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

# ─── Config ──────────────────────────────────────────────────────────────────

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
VAULT_PATH = Path(os.environ.get("VAULT_PATH", "."))

# Project files to sync (relative to vault root)
SYSTEM_FILES = {
    "pos": "00_system/_POS.md",
    "priority": "00_system/_priority.md",
}
PROJECTS_GLOB = "04_project/**/*.md"

# ─── Supabase helpers ─────────────────────────────────────────────────────────

def supabase_upsert(table: str, rows: list[dict], conflict_cols: list[str]) -> None:
    url = f"{SUPABASE_URL}/rest/v1/{table}?on_conflict={','.join(conflict_cols)}"
    data = json.dumps(rows).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
        print(f"  upsert {table} ({len(rows)} rows) → {status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  ERROR upsert {table}: {e.code} {body}", file=sys.stderr)
        sys.exit(1)

# ─── Markdown parsers ─────────────────────────────────────────────────────────

def extract_section(md: str, heading: str) -> str:
    """Extract everything under a ## heading until the next ## heading."""
    pattern = rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)"
    m = re.search(pattern, md, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def parse_project_file(path: Path) -> Optional[dict]:
    """
    Parse a project markdown file and return a projects_state row dict.
    Expected frontmatter or top-level fields:
      - Title: from filename or first H1
      - Status: from frontmatter 'Status:' or section
      - Pillar: from frontmatter
      - Priority: from frontmatter (P1/P2/P3)
      - Next Steps: bulleted list → next_actions array
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    # project_id = stem of filename (e.g. Training_Coach)
    project_id = path.stem

    # Skip non-project files (index pages, etc.)
    if project_id.startswith("_") or project_id.lower() in ("readme", "index"):
        return None

    # Extract title — first H1 or filename
    title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else project_id

    # Extract status from frontmatter or inline
    status = "active"
    status_m = re.search(r"(?:Status|状态)[:\s]+([A-Za-z]+)", text, re.IGNORECASE)
    if status_m:
        raw_status = status_m.group(1).lower()
        if raw_status in ("active", "paused", "done", "idea", "completed"):
            status = raw_status if raw_status != "completed" else "done"

    # Extract pillar
    pillar = None
    pillar_m = re.search(r"Pillar[:\s]+([A-Za-z]+)", text, re.IGNORECASE)
    if pillar_m:
        pillar = pillar_m.group(1).strip()

    # Extract priority
    priority = None
    priority_m = re.search(r"\bP([123])\b", text)
    if priority_m:
        priority = f"P{priority_m.group(1)}"

    # Extract next actions from "## Next Steps" or "## Pending Next Steps"
    next_actions = []
    for heading in ("Next Steps", "Pending Next Steps", "下一步", "Next Actions"):
        section = extract_section(text, heading)
        if section:
            bullets = re.findall(r"^[-*]\s+(.+)$", section, re.MULTILINE)
            # Skip already-done items (strikethrough ~~...~~)
            next_actions = [b.strip() for b in bullets if not b.strip().startswith("~~")]
            break

    # Brief notes — first paragraph after title
    notes = ""
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip() and not p.startswith("#")]
    if paras:
        notes = paras[0][:500]  # cap at 500 chars

    source_path = str(path.relative_to(VAULT_PATH))

    return {
        "project_id": project_id,
        "title": title,
        "status": status,
        "pillar": pillar,
        "priority": priority,
        "next_actions": next_actions,
        "notes": notes,
        "source_path": source_path,
    }

# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=== sync-context ===")

    # 1. Sync context_snapshots (POS + priority)
    print("\n[1] Syncing context_snapshots…")
    snapshot_rows = []
    for key, rel_path in SYSTEM_FILES.items():
        full_path = VAULT_PATH / rel_path
        if not full_path.exists():
            print(f"  SKIP {rel_path} (not found)")
            continue
        content = full_path.read_text(encoding="utf-8").strip()
        snapshot_rows.append({
            "key": key,
            "content": content,
            "source_path": rel_path,
        })
        print(f"  read {rel_path} ({len(content)} chars)")

    if snapshot_rows:
        supabase_upsert("context_snapshots", snapshot_rows, ["key"])

    # 2. Sync projects_state (04_project/**/*.md)
    print("\n[2] Syncing projects_state…")
    project_files = sorted(VAULT_PATH.glob(PROJECTS_GLOB))
    parsed = [parse_project_file(p) for p in project_files]
    project_rows = [r for r in parsed if r is not None]
    print(f"  parsed {len(project_rows)} project files")

    if project_rows:
        supabase_upsert("projects_state", project_rows, ["project_id"])

    print("\n=== done ===")


if __name__ == "__main__":
    main()
