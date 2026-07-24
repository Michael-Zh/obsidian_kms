---
name: "vibe_coding_tool"
status: "active"
pillar: "Career"
current_focus: "Mobile-first AI coding assistant — Plan/Code/Debug three-mode interface"
created: "2026-05-15"
updated: "2026-07-24"
target_completion: "ongoing"
priority: "P3"
tags: [Career, LifeManagement]
---

# Vibe Coding Tool

## Overview

Mobile-first AI coding assistant. Describe code changes → planning agent analyzes → coding agent proposes file replacements → commit to GitHub + Vercel auto-deploy. Each Apply is an atomic commit: modified files + `dev-log.md` update.

**Stack:** Next.js, OpenRouter → DeepSeek R1 (planning) + V4 Flash (coding), GitHub Git Trees API, Vercel  
**Repo:** https://github.com/Michael-Zh/vibe_coding  
**Route:** `/dev` (same repo as Travel App)  
**Local:** `~/Documents/Apps/vibe-coding`

---

## Context & Background

- **Trigger:** Need to code on mobile — ideas that can't wait until at a computer
- **Key Assumptions:** AI-generated code with human review is good enough for personal projects
- **Constraints:** Mobile-only interface; limited to GitHub-hosted repos
- **Prior Work:** Three UI modes built (Plan/Code/Debug)

---

## Objectives & Goals

- **Goal 1:** Enable meaningful code changes from mobile
- **Goal 2:** Maintain safety via planning agent review before code generation
- **Goal 3:** Keep dev log automatically updated for project continuity

---

## Strategic Direction

- Stabilize Plan → Code pipeline — reduce hallucinated file modifications
- Debug mode refinement — better error log parsing and fix suggestions
- Multi-repo support beyond current GitHub workflow

---

## Decisions

<!-- Populate after coaching sessions -->

---

## Connections

**Parent Pillar:** [[Career]]

**Related Projects:**
- [[Training_Coach]] — Primary app built with this tool
- [[AI_learning]] — Output > input learning philosophy
