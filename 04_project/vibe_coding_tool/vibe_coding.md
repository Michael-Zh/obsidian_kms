---
name: Vibe Coding Tool
project_id: pj0009
status: parked
pillar: CreativityCuriosity
priority: P3
---

# Vibe Coding Tool

**GitHub:** https://github.com/Michael-Zh/vibe_coding  
**Route:** `/dev`（与 Travel App 同 repo）  
**本地代码：** `~/Documents/Apps/vibe-coding`  
**Stack:** Next.js, OpenRouter → DeepSeek R1（planning）+ V4 Flash（coding）, GitHub Git Trees API, Vercel

---

## Vision

Mobile-first AI coding assistant。描述代码改动 → planning agent 分析 → coding agent 提出文件替换 → 直接 commit 到 GitHub + Vercel 自动部署。每次 Apply 原子提交：修改文件 + `dev-log.md` 更新。

---

## 已上线功能

- **三种 UI 模式：** Plan（DeepSeek R1 讨论 → Spec Card）、Code（执行改动 → Code Proposal）、Debug（粘贴 error log → 修复提案）
- **GitHub 提交：** Git Trees API 原子多文件提交，AI 生成 commit message（subject + Why + Approach）
- **Dev Log 自动更新：** 每次 Apply 同步写入 `dev-log.md`

---

## Open Backlog

- Multi-repo switching — UI 里切换目标 repo/file，不用改 env vars
- Streaming responses — SSE for plan + code routes
- Multi-file support — `proposals: { target_file, new_code }[]`
- Auth layer — `TOOL_PASSWORD` env var 或 Supabase Auth
- Vercel deploy status polling — Apply 后轮询 deploy 状态
- Cloud Executor（云端执行端） — GitHub Codespaces 或廉价 VPS（Hetzner $5/月）运行 Claude Code，实现纯移动端闭环

---
## Strategic Direction

- Multi-repo switching — 同一界面切换目标 repo
- Streaming responses — SSE 实时流式输出
- Cloud Executor — 云端 Claude Code 执行端，实现手机端闭环

---
## Decisions

- **2026-07:** MVP 上线 — 三种 UI 模式（Plan/Code/Debug）+ GitHub Trees API 原子提交
- **长期:** 切换到 Claude Code subagent 架构，当前 DeepSeek 方案作为 fallback

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_
