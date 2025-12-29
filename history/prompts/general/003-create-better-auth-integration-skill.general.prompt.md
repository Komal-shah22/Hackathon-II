---
id: 003
title: Create Better Auth Integration Skill
stage: general
date: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create skill
labels: ["skill", "authentication", "better-auth", "jwt", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/better-auth-integration.md
tests:
  - none
---

## Prompt

Create a custom skill for my hackathon project Phase 2.

Skill Name: better-auth-integration

Purpose: This skill teaches Claude how to implement Better Auth for Next.js frontend authentication and FastAPI backend JWT verification, ensuring secure end-to-end authentication flow.

When to use this skill:
- Implementing authentication
- Creating signup/signin pages
- Setting up JWT verification
- Securing API endpoints
- Managing user sessions
- User mentions "auth", "authentication", "Better Auth", "JWT", "login", "signup", or "signin"

Description for Claude to auto-detect:
"Better Auth setup for Next.js frontend and FastAPI JWT verification. Use when implementing authentication, signup/signin, or when user mentions auth, Better Auth, JWT, or login."

Key Topics to Cover:

1. ARCHITECTURE OVERVIEW

## Response snapshot

Created comprehensive Better Auth integration skill file at `.claude/skills/better-auth-integration.md` covering:

1. **Architecture Overview** - Full authentication flow diagram, component responsibilities, security boundaries
2. **Better Auth Setup** - Installation, client config, server config, API route handler, environment variables
3. **Authentication Pages** - Complete signup page with validation, signin page, auth layout
4. **Protected Routes** - Dashboard layout with server-side auth check, useSession hook, client-side protection
5. **FastAPI JWT Verification** - verify_jwt dependency, authorize_user_access, TokenPayload class
6. **API Client with Auth** - Authenticated fetch wrapper, token handling, 401 redirect
7. **Security Best Practices** - Critical checklist, secret synchronization, common mistakes table
8. **Error Handling** - Frontend error states hook, backend standardized errors
9. **Testing Authentication** - Frontend auth tests, backend JWT validation tests
10. **Complete Integration Example** - Full todo page with auth flow

## Outcome

- ✅ Impact: Created comprehensive skill file for end-to-end authentication implementation
- 🧪 Tests: None (documentation skill file)
- 📁 Files: 1 file created (.claude/skills/better-auth-integration.md)
- 🔁 Next prompts: Use skill for auth implementation, test with auth-implementor agent
- 🧠 Reflection: Skill emphasizes critical secret synchronization and security patterns

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - documentation artifact
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate skill integration with auth-implementor agent
