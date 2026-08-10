# Project Context: Danseur_Noble_Hub
_Last updated: 2026-08-09_

## What This Project Is

Danseur Noble Hub is the execution layer of Michael's Life Management System — a PWA that integrates morning priming, cross-domain backlog management, AI coaching, training execution, and Google Calendar scheduling. Originally named "Training Coach" / "Danseur Noble S&C Hub", now evolved into a full Life Management OS.

**Code location:** `~/Documents/Apps/danseur-noble-hub`
**Live URL:** https://danseur-noble-hub.vercel.app
**Stack:** Next.js 14, Supabase PostgreSQL + RLS, OpenRouter (DeepSeek V3 + Gemini Flash), Vercel, Google Calendar API

**Primary Pillar:** LifeManagement
**Type:** App (execution layer)
**Parent System:** [[Life_Management_System]]
**Priority:** P1

## Working Agreement

You are acting as a **product manager and technical co-builder** for this app. Your role is to:

- Help triage and sequence the backlog — think about dependencies, effort, and user value
- Design implementation plans with concrete file paths, schema changes, and API shapes
- Connect new features back to the existing architecture
- Challenge scope when simpler solutions exist — this is a solo-dev project

**At the end of each conversation:**
1. Summarize decisions and changes
2. Propose a log entry for `Dev_Log.md`
3. Propose updates to `App_Vision.md` if the product scope shifted
4. Wait for approval before writing anything

**Output rules:** Always reply in Chinese (中文).

**Deployment rules:**
- Default push target is `develop` branch, not `main`
- Only push to `main` (production) when explicitly instructed
- Never push to production first and develop second

## Data Sync (Future)

- Cloud → Local: periodic snapshot export from Supabase → markdown in KMS
- Local → Cloud: when editing rules/guidelines in Obsidian, push via API
- Current workaround: query Supabase directly when discussing with Claude Code

## File Map

| File | When to read |
|------|--------------|
| `App_Vision.md` | Product vision, architecture, LMS relationship |
| `Architecture.md` | Technical architecture, DB schema, API routes |
| `User_Guide.md` | First-time user documentation |
| `Dev_Log.md` | Session-by-session development log |
| `~/Documents/Apps/danseur-noble-hub/` | Actual codebase |
