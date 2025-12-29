---
id: 001
title: Create Next.js App Router Custom Skill
stage: general
date: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create skill
labels: ["skill", "nextjs", "frontend", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/nextjs-app-router.md
tests:
  - none
---

## Prompt

Create a custom skill for my hackathon project Phase 2.

Skill Name: nextjs-app-router

Purpose: This skill teaches Claude the Next.js 16 App Router patterns, server/client component best practices, and modern React patterns for building the todo application frontend.

When to use this skill:
- Building Next.js frontend
- Creating pages and layouts
- Implementing React components
- Setting up routing
- Making API calls from frontend
- User mentions "Next.js", "frontend", "React", "components", or "App Router"

Description for Claude to auto-detect:
"Next.js 16 App Router patterns, server/client components, and best practices. Use when building Next.js frontend, creating pages, or when user mentions Next.js, frontend, or React components."

Key Topics to Cover:

1. PROJECT STRUCTURE

## Response snapshot

Created comprehensive Next.js 16 App Router skill file at `.claude/skills/nextjs-app-router.md` covering:

1. **Project Structure** - Standard App Router folder conventions, route groups, dynamic routes
2. **Server vs Client Components** - Decision framework flowchart, when to use each
3. **Data Fetching Patterns** - Server-side fetching, authentication, SWR for client-side
4. **Layouts and Templates** - Root layout, nested layouts, template for animations
5. **Loading and Error States** - loading.tsx, Suspense streaming, error.tsx boundaries
6. **Forms and Server Actions** - Server actions, useFormStatus, useActionState validation
7. **Authentication Integration** - Auth context, protected routes, login page example
8. **API Client Pattern** - Typed API client class with full CRUD operations
9. **Best Practices Checklist** - Component, data fetching, forms, performance, security guidelines
10. **Common Patterns** - Optimistic updates, modal with parallel routes

## Outcome

- ✅ Impact: Created comprehensive skill file for Next.js 16 App Router development guidance
- 🧪 Tests: None (documentation skill file)
- 📁 Files: 1 file created (.claude/skills/nextjs-app-router.md)
- 🔁 Next prompts: Use skill for frontend development, test with frontend-generator agent
- 🧠 Reflection: Skill provides complete reference for modern Next.js patterns specific to todo app

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - documentation artifact
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate skill integration with frontend-generator agent
