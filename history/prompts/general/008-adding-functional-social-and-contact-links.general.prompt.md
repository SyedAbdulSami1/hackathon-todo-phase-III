---
id: 008
title: Adding Functional Social and Contact Links
stage: general
date_iso: 2026-02-27
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: pc
command: add social links
labels: ["frontend", "nextjs", "ui-polish", "contact-info"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/app/page.tsx
tests_yaml:
  - link functionality verification
---

# Prompt Text
page.txs me ... me link blank h. is me email and whatsapp bhi add ker den email= samiwpp@gmail.com and whatsapp number 00923018420180 number me reading ke leye asaan rahe. is hi ther linkedin me https://www.linkedin.com/in/syed-abdul-sami-964a36277/?isSelfProfile=true aur github me https://github.com/SyedAbdulSami1

# Response Text
I have updated the founder section in `frontend/app/page.tsx` with functional links for GitHub, LinkedIn, Email, and WhatsApp.
- **GitHub**: Linked to your profile.
- **LinkedIn**: Linked to your profile.
- **Email**: Added a `mailto:` link for easy emailing.
- **WhatsApp**: Added a `wa.me` link with your phone number.
I also replaced the `<button>` tags with `<a>` tags for proper link behavior and added tooltips for better UX.

# Outcome / Evaluation
Users can now easily connect with you through various professional and personal channels directly from the landing page.
