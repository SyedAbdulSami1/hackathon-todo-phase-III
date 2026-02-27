---
id: 010
title: Switching to Localhost for Debugging 405 Errors
stage: general
date_iso: 2026-02-27
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: pc
command: local run
labels: ["debugging", "localhost", "vercel"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - RUN_LOCAL.bat
  - vercel.json
---

# Prompt Text
kia me localhost per run kron. (User still facing 405 on Vercel)

# Response Text
I recommended running the project on localhost to bypass Vercel's routing complexities and verify the core functionality. I provided instructions for starting both backend and frontend locally and created a `RUN_LOCAL.bat` script to automate the process. I also reverted `vercel.json` to a more traditional `routes` configuration as a final attempt for deployment.

# Outcome / Evaluation
Running locally will allow the user to confirm if the backend and database integration are working correctly without being blocked by deployment-specific issues.
