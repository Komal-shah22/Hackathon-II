---
id: 005
title: Create Global Claude Skills in ~/.claude/skills
stage: general
date: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create skills
labels: ["skill", "global", "claude-code", "nextjs", "fastapi", "auth", "monorepo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ~/.claude/skills/nextjs-app-router/SKILL.md
  - ~/.claude/skills/fastapi-sqlmodel/SKILL.md
  - ~/.claude/skills/better-auth-integration/SKILL.md
  - ~/.claude/skills/monorepo-structure/SKILL.md
tests:
  - none
---

## Prompt

I need you to create 4 custom Skills for my hackathon Phase 2 project. Each skill should be in its own directory with a SKILL.md file.

Create the following structure:

~/.claude/skills/
├── nextjs-app-router/
│   └── SKILL.md
├── fastapi-sqlmodel/
│   └── SKILL.md
├── better-auth-integration/
│   └── SKILL.md
└── monorepo-structure/
    └── SKILL.md

[Detailed specifications provided for each skill]

## Response snapshot

Created 4 global Claude Code skills in `~/.claude/skills/` directory:

1. **nextjs-app-router/SKILL.md** - Next.js 16 App Router patterns including:
   - Project structure for App Router
   - Server vs Client component decision tree
   - Layouts and route groups
   - Data fetching patterns
   - Loading and error states
   - Server Actions
   - TypeScript types

2. **fastapi-sqlmodel/SKILL.md** - FastAPI with SQLModel patterns including:
   - Backend project structure
   - Main application setup with lifespan
   - Configuration management
   - Database connection for Neon PostgreSQL
   - SQLModel database models
   - Pydantic schemas
   - JWT authentication
   - Complete CRUD endpoints
   - Testing setup

3. **better-auth-integration/SKILL.md** - Authentication patterns including:
   - Architecture flow diagram
   - Critical secret synchronization requirement
   - Better Auth server/client setup
   - Signup and signin pages
   - Protected route layouts
   - Backend JWT verification
   - API client with auth
   - Security checklist

4. **monorepo-structure/SKILL.md** - Project organization including:
   - Complete project layout tree
   - Directory purposes
   - Spec-Kit Plus workflow
   - Command reference
   - File naming conventions
   - Environment configuration
   - Constitution compliance

## Outcome

- ✅ Impact: Created 4 global skills available across all Claude Code sessions
- 🧪 Tests: Verified directory structure with `ls -la ~/.claude/skills/`
- 📁 Files: 4 SKILL.md files in 4 directories
- 🔁 Next prompts: Skills will auto-trigger based on description keywords
- 🧠 Reflection: Global skills provide consistent patterns across projects

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - documentation artifact
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test skill auto-detection in new conversation
