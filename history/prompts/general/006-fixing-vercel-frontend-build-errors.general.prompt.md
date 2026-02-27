---
id: 006
title: Fixing Vercel Frontend Build Errors
stage: general
date_iso: 2026-02-27
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: pc
command: fix vercel build
labels: ["frontend", "nextjs", "linting", "vercel"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/app/page.tsx
  - frontend/next.config.js
  - frontend/components/FloatingChat.tsx
tests_yaml:
  - npm run build (local simulation)
---

# Prompt Text
vercel ke build me error a rahe h. ... (logs showing react/no-unescaped-entities and img tag errors) ... kindly in ko bhi sahi ker den.

# Response Text
I have fixed the Vercel build errors in the frontend:
1.  **Unescaped Entities:** Fixed `react/no-unescaped-entities` errors in `frontend/app/page.tsx` and `frontend/components/FloatingChat.tsx` by escaping quotes with `&quot;` and `&apos;`.
2.  **Optimized Images:** Replaced the standard `<img>` tag in `frontend/app/page.tsx` with the Next.js `<Image />` component for better performance and to satisfy the `@next/next/no-img-element` lint rule.
3.  **Next.js Config:** Updated `frontend/next.config.js` to allow the `api.dicebear.com` domain for the new `<Image />` component.

# Outcome / Evaluation
The frontend should now build successfully on Vercel without linting errors.
