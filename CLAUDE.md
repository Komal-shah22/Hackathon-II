# Claude Code Instructions

This project uses Spec-Driven Development (SDD) with Spec-Kit Plus.

## Quick Start

See [AGENTS.md](AGENTS.md) for detailed agent configurations and workflows.

## Key Commands

- `/sp.specify` - Create feature specifications
- `/sp.plan` - Create implementation plans
- `/sp.tasks` - Generate task breakdowns
- `/sp.implement` - Execute implementation
- `/sp.git.commit_pr` - Commit and create PR

## Project Structure

- `frontend/` - Next.js 16 application
- `backend/` - FastAPI application
- `specs/` - Feature specifications
- `history/` - Development history (PHRs, ADRs)

## Active Technologies
- TypeScript 5.x (frontend), Python 3.11+ (backend) + Next.js 16, FastAPI, SQLModel, Better Auth, Tailwind CSS, Shadcn UI (001-todo-app)
- Neon PostgreSQL (serverless, SSL required) with SQLModel ORM (001-todo-app)

## Recent Changes
- 001-todo-app: Added TypeScript 5.x (frontend), Python 3.11+ (backend) + Next.js 16, FastAPI, SQLModel, Better Auth, Tailwind CSS, Shadcn UI
