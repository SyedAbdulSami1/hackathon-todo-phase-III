---
id: 011
title: Fixing Frontend 404 Redirect Error
stage: general
date_iso: 2026-02-27
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: pc
command: fix redirect
labels: ["frontend", "nextjs", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/lib/api-client.ts
---

# Prompt Text
fronted console ... GET http://localhost:3000/login 404 (Not Found) ... (Logs showing 401 on /api/tasks)

# Response Text
I diagnosed that the 404 error was caused by a hardcoded redirect to `/login` in `ApiClient.handleError` when a 401 Unauthorized response is received. Since the application handles login directly on the root `/` page via conditional rendering, the `/login` page doesn't exist. I removed the redirect and corrected the localStorage key for the user object to match the rest of the application.

# Outcome / Evaluation
The frontend should no longer 404 when unauthenticated; instead, it will stay on the root page and correctly prompt for login or registration.
