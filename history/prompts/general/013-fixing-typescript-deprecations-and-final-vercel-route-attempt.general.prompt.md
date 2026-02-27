---
id: 013
title: Fixing TypeScript Deprecations and Final Vercel Route Attempt
stage: general
date_iso: 2026-02-27
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: pc
command: fix ts and routes
labels: ["typescript", "vercel", "routing", "deployment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/tsconfig.json
  - vercel.json
---

# Prompt Text
git per push ker dia new build bhi ho gai koi error nahi h. lekin phir bhi online nahi chal raha ... (Errors showing deprecated TS options and 405 on Vercel)

# Response Text
I resolved the TypeScript deprecation warnings in `frontend/tsconfig.json` by updating the `target` and adding `ignoreDeprecations`. I also refined `vercel.json` to use the `routes` array and explicitly set `NEXT_PUBLIC_API_URL` to an empty string in the environment, which forces the frontend to use relative paths—essential for Vercel's proxying to work correctly.

# Outcome / Evaluation
The project should now build without deprecation warnings, and API routing should be more reliable on Vercel.
