<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (MAJOR: Initial constitution ratification)

Modified principles: N/A (initial creation)

Added sections:
- Core Principles (5 principles: AI-First, Security by Design, Scalability & Modularity,
  Developer Experience, Reliability & Correctness)
- Technology Standards
- Development Workflow
- Governance

Removed sections: N/A (initial creation)

Templates requiring updates:
- .specify/templates/plan-template.md ✅ Compatible (Constitution Check section exists)
- .specify/templates/spec-template.md ✅ Compatible (requirements structure aligns)
- .specify/templates/tasks-template.md ✅ Compatible (phase structure supports principles)

Follow-up TODOs: None
==================
-->

# AI-Native Full-Stack Hackathon Platform Constitution

## Core Principles

### I. AI-First Architecture

Agents and skills drive the development workflow. The system MUST be designed around AI-assisted
code generation, with clear separation between specialized agents (frontend, backend, auth,
database, API) and orchestration through skills.

- All significant implementation work MUST be routed through appropriate specialized agents
- Skills MUST provide clear interfaces for common development tasks
- Agent context MUST be maintained and updated as the codebase evolves
- Human oversight remains required for architectural decisions and security-critical changes

### II. Security by Design

Security MUST be built into every layer from the start, not added as an afterthought.
Authentication, authorization, and data protection are non-negotiable requirements.

- All API endpoints MUST require authentication unless explicitly public
- User data MUST be isolated; queries MUST filter by authenticated user_id
- Secrets and credentials MUST NEVER be hardcoded; environment variables are required
- JWT tokens MUST be verified on every protected request
- Input validation MUST occur at system boundaries (API endpoints, form submissions)
- CORS MUST be explicitly configured with specific allowed origins

### III. Scalability and Modularity

The architecture MUST maintain clean separation between frontend, backend, auth, database,
and API layers. Each layer MUST be independently deployable and testable.

- Frontend: Next.js 16 with App Router, Server Components by default
- Backend: FastAPI with structured routers and dependency injection
- Auth: Better Auth (frontend) with JWT verification (backend)
- Database: SQLModel ORM with Neon PostgreSQL
- API: RESTful design with full CRUD operations
- Each layer MUST have its own directory structure and can be developed independently
- Cross-layer dependencies MUST be explicitly defined through contracts/interfaces

### IV. Developer Experience

The codebase MUST prioritize clarity, readability, and strong typing. Developers MUST be able
to understand and modify code with confidence.

- TypeScript MUST be used for all frontend code with strict mode enabled
- Python type hints MUST be used for all backend code
- Naming conventions MUST be consistent and self-documenting
- ESLint and formatting tools MUST be configured and enforced
- Each module MUST include clear usage instructions
- Error messages MUST be actionable and user-friendly

### V. Reliability and Correctness

Data flows MUST be validated at every boundary. Error handling MUST be comprehensive and
predictable. The system MUST fail gracefully and provide clear feedback.

- All API responses MUST use proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Pydantic models MUST validate all request/response data
- Database operations MUST handle errors and rollback on failure
- Loading states MUST be shown during async operations
- Error boundaries MUST catch and display errors gracefully in the frontend
- All external calls MUST have timeout and retry logic where appropriate

## Technology Standards

The following technology stack is mandated for this project:

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend Framework | Next.js | 16 with App Router |
| Frontend Language | TypeScript | Strict mode |
| Frontend Styling | Tailwind CSS | Utility-first, responsive |
| Backend Framework | FastAPI | Async endpoints |
| Backend Language | Python | 3.11+ with type hints |
| ORM | SQLModel | Hybrid SQLAlchemy/Pydantic |
| Database | Neon PostgreSQL | Serverless, SSL required |
| Authentication | Better Auth + JWT | Shared secret, HS256 |
| API Design | REST | JSON request/response |

**Folder Structure:**

```
frontend/           # Next.js 16 application
├── app/           # App Router pages and layouts
├── components/    # Reusable UI components
└── lib/           # Utilities and API client

backend/            # FastAPI application
├── routes/        # API endpoint handlers
├── models.py      # SQLModel database models
├── db.py          # Database connection
└── auth.py        # JWT verification

.claude/            # AI agent configuration
├── agents/        # Specialized agent definitions
├── skills/        # Development workflow skills
└── commands/      # Slash command definitions
```

## Development Workflow

### Code Quality Gates

All code MUST pass these checks before merge:

1. **Type Safety**: No TypeScript errors, no untyped Python functions
2. **Linting**: ESLint passes with zero warnings
3. **Security**: No hardcoded secrets, proper auth on all protected routes
4. **Testing**: Critical paths covered (auth flow, CRUD operations)

### Commit Standards

- Commits MUST be atomic and focused on a single change
- Commit messages MUST follow conventional format: `type: description`
- Types: feat, fix, docs, refactor, test, chore

### Agent Workflow

1. User requests feature or fix
2. Orchestrator routes to appropriate specialized agent
3. Agent reads specifications and existing code
4. Agent generates implementation following constitution
5. Human reviews and approves changes
6. PHR (Prompt History Record) documents the exchange

## Governance

This constitution supersedes all other development practices for this project. Any deviation
MUST be documented with justification in the relevant spec or plan file.

### Amendment Process

1. Propose amendment with rationale
2. Document impact on existing code and templates
3. Update constitution with new version number
4. Propagate changes to affected templates
5. Create PHR documenting the amendment

### Version Policy

- **MAJOR**: Breaking changes to principles or removal of non-negotiable requirements
- **MINOR**: New principles, sections, or significant guidance additions
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance

- All PRs MUST verify compliance with constitution principles
- Complexity beyond minimum viable MUST be justified
- Security violations are blocking; no exceptions without documented approval

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
