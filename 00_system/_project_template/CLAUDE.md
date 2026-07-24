# [Project Name]

[One-line description of what this project is.]

## Key Facts

- **Stack:** [tech stack]
- **Live URL / Entry point:** [url or local path]
- **Vault brief:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/[project_slug]/[project_slug].md`

## What NOT to change

- [Stable interfaces, API contracts, storage keys, etc.]

---

## At the end of each conversation

1. Summarize decisions made and what changed
2. Propose a log entry for the dev log — date + decisions + open questions
3. Propose updates to the vault brief — update project status and `## Strategic Direction`
4. **Commit KMS vault to git** — if any KMS files were modified during the session (project docs, coaching files, wiki pages, POS signals, etc.):
   ```bash
   cd "/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS"
   git add -A && git status --short
   git commit -m "feat: [brief description of changes]"
   ```
   Show the commit message for approval, then push: `git push origin main`
5. Wait for approval before writing anything

---

## Session-End Backlog Sync

**每次 CC session 结束时，执行 Backlog Sync：**

1. 收集本次 session 产生的 action items（可执行的具体任务）
2. 调用 `POST /api/backlog/review/cc` (action: "preview") 预览 diff：
   - `new_actions`：新增项（会去重，已存在的自动跳过）
   - `stale`：可能过期的旧 backlog items
3. 显示预览结果，逐条或批量确认
4. 用户确认后，调用 `POST /api/backlog/review/cc` (action: "apply") 写入 DB
5. 报告结果：`新增 X 条，标记完成 Y 条，跳过 Z 条（重复）`

```bash
KEY=$(grep SUPABASE_SERVICE_ROLE_KEY .env.local.prod | cut -d= -f2)
BASE="https://danseur-noble-hub.vercel.app"  # or http://localhost:3000 for dev

# Preview
curl -s -X POST "$BASE/api/backlog/review/cc" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"action":"preview","proposed_items":[...],"project_ids":[...]}'

# Apply after confirmation
curl -s -X POST "$BASE/api/backlog/review/cc" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"action":"apply","accept_tasks":[...],"resolve_stale_ids":[...]}'
```

**Project-specific Rules:**
- Only CC sessions that `project-context` loaded a specific project trigger this
- Global CC sessions (no project loaded) skip Backlog Sync
- The `## Strategic Direction` section in the project doc is updated by coaching decisions, not individual tasks — Backlog Sync handles the tasks

---

## Output Rules

1. **Always reply in Chinese** (中文).
2. Never output large code diffs or repeated file contents in chat unless explicitly asked. For code changes, make edits directly in the file — in chat only describe the core change and result.
3. Do not rewrite existing content — only propose additions.

## Deployment Rules

- **Default push target is `develop` branch**, not `main`.
- Only push to `main` when explicitly instructed: "推到 production" / "push to prod" / "deploy to production".
- Never push to production first and develop second.
