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
3. Propose updates to the vault brief — update current features list and open backlog
4. Wait for approval before writing anything

**Sync rule:** 每次会话结束更新 vault brief 时，同步更新 `_in_case_you_are_bored.md` 里 [[project_slug]] 行的 Current Focus + Updated 字段。

**Session-start reconcile rule:** 每次 CC session 加载 project-context 时，如果 `project-context` skill 在顶部显示 `## ⚠️ Pending App Changes`，必须先 review delta（backlog 完成情况 + coaching sessions 的 decisions），和用户确认是否写入 Obsidian project doc，完成 reconcile 后再进入正式讨论。

---

## Output Rules

1. **Always reply in Chinese** (中文).
2. Never output large code diffs or repeated file contents in chat unless explicitly asked. For code changes, make edits directly in the file — in chat only describe the core change and result.
3. Do not rewrite existing content — only propose additions.

## Deployment Rules

- **Default push target is `develop` branch**, not `main`.
- Only push to `main` when explicitly instructed: "推到 production" / "push to prod" / "deploy to production".
- Never push to production first and develop second.
