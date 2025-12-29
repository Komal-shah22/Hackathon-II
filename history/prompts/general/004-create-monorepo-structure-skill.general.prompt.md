---
id: 004
title: Create Monorepo Structure Skill
stage: general
date: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create skill
labels: ["skill", "monorepo", "project-structure", "spec-kit", "organization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/monorepo-structure.md
tests:
  - none
---

## Prompt

Create a custom skill for my hackathon project Phase 2.

Skill Name: monorepo-structure

Purpose: This skill teaches Claude how to organize a full-stack monorepo with frontend, backend, and specifications using Spec-Kit Plus methodology for the hackathon project.

When to use this skill:
- Setting up project structure
- Organizing files and folders
- Creating monorepo layout
- Managing multiple packages
- Setting up Spec-Kit
- User mentions "monorepo", "project structure", "folder structure", "organization", or "Spec-Kit"

Description for Claude to auto-detect:
"Monorepo organization for full-stack projects with Spec-Kit Plus. Use when setting up project structure, organizing files, or when user mentions monorepo, project structure, or folder organization."

Key Topics to Cover:

1. COMPLETE MONOREPO STRUCTURE

## Response snapshot

Created comprehensive monorepo structure skill file at `.claude/skills/monorepo-structure.md` covering:

1. **Complete Monorepo Structure** - Full project layout tree with all directories explained
2. **Directory Purposes** - Tables explaining purpose of each directory (.claude, .specify, specs, history, frontend, backend)
3. **Spec-Kit Plus Workflow** - Development lifecycle diagram and command reference table
4. **File Naming Conventions** - Patterns for specs, PHRs, ADRs, skills, and agents
5. **Environment Configuration** - Frontend and backend .env templates, .gitignore patterns
6. **Creating New Features** - Manual process and Spec-Kit commands
7. **Agent-Skill Relationship** - Architecture diagram showing how agents and skills work together
8. **Constitution Compliance** - Every code change checklist for constitution adherence
9. **Initialization Checklist** - Step-by-step project setup checklist
10. **Quick Reference** - Key file locations and development commands

## Outcome

- ✅ Impact: Created comprehensive skill file for monorepo organization and Spec-Kit Plus methodology
- 🧪 Tests: None (documentation skill file)
- 📁 Files: 1 file created (.claude/skills/monorepo-structure.md)
- 🔁 Next prompts: Use skill for project setup, reference for file organization questions
- 🧠 Reflection: Skill bridges AI agent workflow with project structure, aligns with constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - documentation artifact
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test skill with project initialization requests
