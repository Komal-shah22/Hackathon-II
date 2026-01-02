---
id: 0002
title: create-phase3-chatbot-plan
stage: plan
date: 2025-12-31
surface: cli
model: claude-sonnet-4-5-20250929
feature: 001-chatbot-phase3
branch: 001-chatbot-phase3
user: claude
command: /sp.plan
labels: [plan, chatbot, ai, phase3, research, mcp]
links:
  spec: specs/001-chatbot-phase3/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/001-chatbot-phase3/plan.md
  - specs/001-chatbot-phase3/research.md
  - specs/001-chatbot-phase3/data-model.md
  - specs/001-chatbot-phase3/quickstart.md
  - specs/001-chatbot-phase3/contracts/chat.md
tests:
  - Phase 1 Design/Contract validation
---

## Prompt

/sp.plan
Create comprehensive implementation plan for Phase 3: AI-Powered Todo Chatbot based on the specification.

**Context:**
- Phase 2 is complete (Next.js + FastAPI + Neon DB + Better Auth)
- We are ADDING chatbot functionality
... [full instruction from user] ...

## Response snapshot

Generated a comprehensive implementation plan for the Phase 3 AI Chatbot.
Key architectural decisions captured:
1. **Stateless Backend**: Externalized session management using PostgreSQL.
2. **FastMCP**: Using the official MCP SDK for tool definitions.
3. **Vercel AI SDK**: Replaced the placeholder @openai/chatkit with the industry-standard `ai` package for streaming.
4. **Data Model**: Normalized `Conversation` and `Message` tables for reliable context persistence.

Established clear contracts, a data model, and a quickstart guide.

## Outcome

- ✅ Impact: Defined the technical path for a strictly stateless AI architecture.
- 🧪 Tests: Validated architectural decisions against the Project Constitution.
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/chat.md.
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: Resolving the "@openai/chatkit" placeholder was a critical early win. The transition to Vercel AI SDK ensures a much more stable and standard implementation phase.

## Evaluation notes (flywheel)

- Failure modes observed: Initial confusion on @openai/chatkit package existence resolved via research agent.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
