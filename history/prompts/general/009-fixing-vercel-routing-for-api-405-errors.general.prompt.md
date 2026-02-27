---
id: 009
title: Fixing Vercel Routing for API 405 Errors
stage: general
date_iso: 2026-02-27
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: pc
command: fix api routing
labels: ["vercel", "routing", "deployment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - vercel.json
tests_yaml:
  - manual verification on vercel
---

# Prompt Text
me ne https://hackathon-todo-phase-iii.vercel.app/ per account login kerne ke koshis ki to error agaya. ... (showing 405 error on /api/auth/login)

# Response Text
The 405 Method Not Allowed error on Vercel was caused by incorrect routing configuration. In a monorepo-style setup on Vercel where both frontend (Next.js) and backend (FastAPI/Python) coexist, we need explicit `rewrites` to ensure requests starting with `/api` are directed to the Python backend instead of being handled by the Next.js static router. I updated `vercel.json` with a modern `rewrites` configuration and ensured the `builds` section correctly points to `frontend/package.json` and `backend/main.py`.

# Outcome / Evaluation
API requests should now be correctly routed to the FastAPI backend on Vercel, resolving the 405 errors during login and registration.
