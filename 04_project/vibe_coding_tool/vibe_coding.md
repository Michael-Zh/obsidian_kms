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

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_
