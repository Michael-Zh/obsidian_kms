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
EXCLUDED_FILES = {"CLAUDE.md"}

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


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract simple YAML frontmatter between --- markers. Returns key→value dict."""
    result: dict[str, str] = {}
    # Find frontmatter block (first --- to second ---)
    blocks = re.findall(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not blocks:
        return result
    fm = blocks[0]
    for line in fm.split('\n'):
        # Match "key: value" (value may be quoted or unquoted, may have inline comments)
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+)$', line)
        if m:
            key = m.group(1).strip().lower()
            val = m.group(2).strip().strip('"').strip("'")
            # Strip inline comments (but not date fields like 2026-08-09)
            if not re.match(r'^\d{4}-\d{2}-\d{2}', val):
                val = re.sub(r'\s+#.*$', '', val)
            result[key] = val
    return result


def parse_project_file(path: Path) -> Optional[dict]:
    """
    Parse a project markdown file and return a projects_state row dict.

    Canonical project files MUST have `project_id: pjXXXX` in frontmatter.
    Files without this are skipped (they are support docs, not project definitions).

    Fields extracted:
      - project_id: from frontmatter (REQUIRED)
      - title: first H1 heading
      - status: from frontmatter (default: "active")
      - pillar: from frontmatter
      - priority: from frontmatter (P1/P2/P3)
      - next_actions: bulleted list from ## Strategic Direction section
      - notes: first paragraph after frontmatter (capped at 500 chars)
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    # ── Require project_id frontmatter ──
    fm = parse_frontmatter(text)
    project_id = fm.get("project_id", "")
    if not project_id.startswith("pj"):
        return None  # Not a tracked project file — skip

    # ── Title: first H1 ──
    title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.stem

    # ── Status: from frontmatter, map "completed" → "done" ──
    status = fm.get("status", "active").lower()
    if status == "completed":
        status = "done"
    if status not in ("active", "paused", "done"):
        status = "active"

    # ── Pillar: from frontmatter ──
    pillar = fm.get("pillar")

    # ── Priority: from frontmatter (P1/P2/P3) — kept for Step-1 compatibility ──
    priority = fm.get("priority")
    if priority and not re.match(r'^P[123]$', priority):
        # Try to extract from frontmatter value (e.g. "P2 — something")
        m = re.search(r'\b(P[123])\b', priority)
        priority = m.group(1) if m else None

    # ── Execution state: from frontmatter (main|on_deck|ongoing|autopilot|parked) ──
    execution_state = fm.get("execution_state")
    if execution_state and execution_state.lower() not in ("main", "on_deck", "ongoing", "autopilot", "parked"):
        execution_state = None

    # ── Next actions: from ## Strategic Direction bullets ──
    next_actions = []
    for heading in ("Strategic Direction", "Next Steps", "Pending Next Steps"):
        section = extract_section(text, heading)
        if section:
            # Match both bullet (-, *) and numbered list (1., 2), ...) formats
            bullets = re.findall(r"^(?:[-*]\s+|(?:\d+[.)])\s+)(.+)$", section, re.MULTILINE)
            next_actions = [b.strip() for b in bullets if b.strip()]
            break

    # ── Notes: first paragraph after frontmatter (skip H1 lines) ──
    notes = ""
    # Get body text (after frontmatter block)
    fm_end = text.find("---", text.find("---") + 3) + 3
    body = text[fm_end:] if fm_end > 2 else text
    paras = [p.strip() for p in re.split(r"\n{2,}", body) if p.strip() and not p.startswith("#")]
    if paras:
        notes = paras[0][:500]

    source_path = str(path.relative_to(VAULT_PATH))

    return {
        "project_id": project_id,
        "title": title,
        "status": status,
        "pillar": pillar,
        "priority": priority,
        "execution_state": execution_state,
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

    # 2. Sync projects_state
    #    Canonical detection: file has `project_id: pjXXXX` in frontmatter.
    #    This naturally handles nested sub-directories (e.g. Training/Meal_prep_routine/).
    #    Support docs without project_id (Architecture.md, Dev_Log.md, etc.) are skipped.
    print("\n[2] Syncing projects_state…")
    project_files = sorted(VAULT_PATH.glob(PROJECTS_GLOB))

    # Filter: skip CLAUDE.md, _-prefixed files, _archive directories
    valid = []
    for p in project_files:
        if p.name in EXCLUDED_FILES:
            continue
        if p.stem.startswith("_"):
            continue
        if any(part.startswith("_") for part in p.parts):
            continue
        valid.append(p)

    parsed = [parse_project_file(p) for p in valid]
    # Deduplicate by project_id — last file wins (handles same project_id in multiple docs)
    seen: dict[str, dict] = {}
    for r in parsed:
        if r is not None:
            pid = r["project_id"]
            if pid in seen:
                print(f"  DEDUP: {pid} — overriding {seen[pid]['source_path']} with {r['source_path']}")
            seen[pid] = r

    project_rows = list(seen.values())
    print(f"  parsed {len(project_rows)} project files (filtered from {len(project_files)} total)")

    if project_rows:
        for r in project_rows:
            print(f"  {r['project_id']} → {r['title']} ({r['status']}, {r['priority']}, {r['execution_state']}) — {len(r['next_actions'])} actions")
        supabase_upsert("projects_state", project_rows, ["project_id"])
    else:
        print("  WARNING: no projects with project_id found — nothing to sync")

    print("\n=== done ===")


if __name__ == "__main__":
    main()
