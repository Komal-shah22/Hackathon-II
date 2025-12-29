---
description: Monorepo organization for full-stack projects with Spec-Kit Plus. Use when setting up project structure, organizing files, or when user mentions monorepo, project structure, or folder organization.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Monorepo Structure with Spec-Kit Plus

This skill teaches Claude how to organize a full-stack monorepo with frontend, backend, and specifications using Spec-Kit Plus methodology for the hackathon project.

---

## 1. COMPLETE MONOREPO STRUCTURE

### Full Project Layout

```
project-root/
│
├── .claude/                    # AI Agent Configuration
│   ├── agents/                 # Specialized agent definitions
│   │   ├── frontend.md         # Frontend generation agent
│   │   ├── backend.md          # Backend generation agent
│   │   ├── auth.md             # Authentication agent
│   │   ├── database.md         # Database schema agent
│   │   └── api.md              # API routing agent
│   │
│   ├── skills/                 # Development workflow skills
│   │   ├── frontend.md         # Invokes frontend-generator
│   │   ├── backend.md          # Invokes backend-generator
│   │   ├── auth.md             # Invokes auth-implementor
│   │   ├── database.md         # Invokes database-schema
│   │   ├── api.md              # Invokes api-router
│   │   ├── nextjs-app-router.md    # Next.js patterns reference
│   │   ├── fastapi-sqlmodel.md     # FastAPI patterns reference
│   │   ├── better-auth-integration.md  # Auth patterns reference
│   │   └── monorepo-structure.md   # Project organization reference
│   │
│   └── commands/               # Slash command definitions
│       └── sp.*.md             # Spec-Kit Plus commands
│
├── .specify/                   # Spec-Kit Plus System
│   ├── memory/                 # Project memory and constitution
│   │   └── constitution.md     # Core principles and standards
│   │
│   ├── templates/              # Document templates
│   │   ├── spec-template.md    # Feature specification template
│   │   ├── plan-template.md    # Implementation plan template
│   │   ├── tasks-template.md   # Task breakdown template
│   │   ├── adr-template.md     # Architecture decision template
│   │   ├── phr-template.prompt.md  # Prompt history template
│   │   ├── checklist-template.md   # Custom checklist template
│   │   └── agent-file-template.md  # Agent definition template
│   │
│   └── scripts/                # Automation scripts
│       └── bash/               # Bash helper scripts
│           ├── create-new-feature.sh
│           ├── create-adr.sh
│           ├── create-phr.sh
│           ├── setup-plan.sh
│           ├── update-agent-context.sh
│           ├── check-prerequisites.sh
│           └── common.sh
│
├── specs/                      # Feature Specifications
│   ├── <feature-name>/         # Per-feature directory
│   │   ├── spec.md             # Feature requirements
│   │   ├── plan.md             # Architecture decisions
│   │   └── tasks.md            # Implementation tasks
│   │
│   ├── api/                    # API specifications
│   │   └── rest-endpoints.md   # REST API contract
│   │
│   ├── database/               # Database specifications
│   │   └── schema.md           # Database schema design
│   │
│   └── ui/                     # UI specifications
│       └── components.md       # Component requirements
│
├── history/                    # Development History
│   ├── prompts/                # Prompt History Records (PHRs)
│   │   ├── constitution/       # Constitution-related prompts
│   │   ├── general/            # General prompts
│   │   └── <feature-name>/     # Feature-specific prompts
│   │
│   └── adr/                    # Architecture Decision Records
│       └── 001-*.md            # Numbered ADRs
│
├── frontend/                   # Next.js 16 Application
│   ├── app/                    # App Router (pages, layouts)
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Global styles
│   │   │
│   │   ├── (auth)/             # Auth route group
│   │   │   ├── layout.tsx      # Auth layout (redirects logged-in)
│   │   │   ├── signin/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (dashboard)/        # Protected route group
│   │   │   ├── layout.tsx      # Dashboard layout (requires auth)
│   │   │   ├── todos/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── loading.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   │
│   │   └── api/                # API routes (BFF pattern)
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # Reusable UI primitives
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── modal.tsx
│   │   │
│   │   ├── forms/              # Form components
│   │   │   └── todo-form.tsx
│   │   │
│   │   ├── todos/              # Feature-specific components
│   │   │   ├── todo-card.tsx
│   │   │   ├── todo-list.tsx
│   │   │   └── todo-filter.tsx
│   │   │
│   │   ├── layout/             # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── nav.tsx
│   │   │
│   │   └── auth/               # Auth-related components
│   │       └── require-auth.tsx
│   │
│   ├── lib/                    # Utilities and configuration
│   │   ├── auth.ts             # Better Auth server config
│   │   ├── auth-client.ts      # Better Auth client hooks
│   │   ├── api-client.ts       # Backend API client
│   │   └── utils.ts            # Helper functions
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── use-todos.ts
│   │   └── use-auth.ts
│   │
│   ├── types/                  # TypeScript type definitions
│   │   ├── todo.ts
│   │   └── api.ts
│   │
│   ├── public/                 # Static assets
│   │   └── ...
│   │
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── .env.local              # Frontend environment (git-ignored)
│
├── backend/                    # FastAPI Application
│   ├── main.py                 # Application entry point
│   ├── config.py               # Settings from environment
│   ├── db.py                   # Database engine and sessions
│   ├── models.py               # SQLModel table definitions
│   ├── schemas.py              # Pydantic request/response
│   ├── auth.py                 # JWT verification
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── routes/                 # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── tasks.py            # Task CRUD endpoints
│   │   ├── users.py            # User endpoints (if needed)
│   │   └── health.py           # Health check endpoint
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── task_service.py
│   │
│   ├── middleware/             # Custom middleware
│   │   ├── __init__.py
│   │   └── logging.py
│   │
│   ├── tests/                  # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py         # Pytest fixtures
│   │   ├── test_tasks.py
│   │   └── test_auth.py
│   │
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Backend environment (git-ignored)
│   └── .env.example            # Template for env vars
│
├── shared/                     # Shared Types/Contracts (optional)
│   └── types/
│       └── todo.ts             # Shared type definitions
│
├── scripts/                    # Project-level scripts
│   ├── setup.sh                # Initial project setup
│   ├── dev.sh                  # Start development servers
│   └── test.sh                 # Run all tests
│
├── .gitignore                  # Git ignore patterns
├── CLAUDE.md                   # AI agent instructions
├── README.md                   # Project documentation
└── package.json                # Root package (if using npm workspaces)
```

---

## 2. DIRECTORY PURPOSES

### AI Configuration (`.claude/`)

| Directory | Purpose |
|-----------|---------|
| `agents/` | Specialized agent definitions with system prompts and capabilities |
| `skills/` | Workflow skills that invoke agents or provide reference documentation |
| `commands/` | Slash command definitions for common operations |

### Spec-Kit Plus (`.specify/`)

| Directory | Purpose |
|-----------|---------|
| `memory/constitution.md` | Core principles, technology standards, governance rules |
| `templates/` | Document templates for specs, plans, tasks, ADRs, PHRs |
| `scripts/bash/` | Automation helpers for creating features, ADRs, PHRs |

### Specifications (`specs/`)

| Directory | Purpose |
|-----------|---------|
| `<feature>/spec.md` | Requirements: who, what, why, acceptance criteria |
| `<feature>/plan.md` | Architecture: how, decisions, tradeoffs |
| `<feature>/tasks.md` | Implementation: ordered tasks with test cases |
| `api/` | REST endpoint contracts |
| `database/` | Schema designs and migrations |
| `ui/` | Component specifications |

### Development History (`history/`)

| Directory | Purpose |
|-----------|---------|
| `prompts/constitution/` | PHRs for constitution changes |
| `prompts/general/` | PHRs not tied to a feature |
| `prompts/<feature>/` | PHRs for specific feature development |
| `adr/` | Architecture Decision Records |

### Frontend (`frontend/`)

| Directory | Purpose |
|-----------|---------|
| `app/` | Next.js App Router pages and layouts |
| `components/` | Reusable React components by category |
| `lib/` | Configuration, utilities, API client |
| `hooks/` | Custom React hooks |
| `types/` | TypeScript type definitions |

### Backend (`backend/`)

| Directory | Purpose |
|-----------|---------|
| `routes/` | HTTP endpoint handlers (thin layer) |
| `services/` | Business logic (reusable) |
| `middleware/` | Request/response middleware |
| `tests/` | Pytest test files |
| Root files | Core config: main.py, db.py, models.py, auth.py |

---

## 3. SPEC-KIT PLUS WORKFLOW

### Development Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     SPEC-KIT PLUS WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. SPECIFY (/sp.specify)                                               │
│     └── Create feature specification                                    │
│         → specs/<feature>/spec.md                                       │
│                                                                          │
│  2. CLARIFY (/sp.clarify)                                               │
│     └── Ask targeted clarification questions                            │
│         → Update spec.md with answers                                   │
│                                                                          │
│  3. PLAN (/sp.plan)                                                     │
│     └── Design implementation approach                                  │
│         → specs/<feature>/plan.md                                       │
│         → Suggest ADRs for significant decisions                        │
│                                                                          │
│  4. TASKS (/sp.tasks)                                                   │
│     └── Break down into ordered implementation tasks                    │
│         → specs/<feature>/tasks.md                                      │
│                                                                          │
│  5. IMPLEMENT (/sp.implement)                                           │
│     └── Execute tasks via specialized agents                            │
│         → Code changes in frontend/ and backend/                        │
│         → PHRs in history/prompts/<feature>/                            │
│                                                                          │
│  6. COMMIT (/sp.git.commit_pr)                                          │
│     └── Commit changes and create PR                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Command Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `/sp.constitution` | Create/update project principles | `.specify/memory/constitution.md` |
| `/sp.specify` | Create feature specification | `specs/<feature>/spec.md` |
| `/sp.clarify` | Clarify underspecified areas | Updates to `spec.md` |
| `/sp.plan` | Design implementation | `specs/<feature>/plan.md` |
| `/sp.tasks` | Generate task breakdown | `specs/<feature>/tasks.md` |
| `/sp.taskstoissues` | Convert tasks to GitHub issues | GitHub issues |
| `/sp.implement` | Execute implementation | Code changes |
| `/sp.analyze` | Cross-artifact consistency check | Analysis report |
| `/sp.checklist` | Generate custom checklist | Checklist document |
| `/sp.adr` | Document architectural decision | `history/adr/*.md` |
| `/sp.phr` | Record prompt history | `history/prompts/*.md` |
| `/sp.git.commit_pr` | Commit and create PR | Git commit + PR |
| `/sp.reverse-engineer` | Reverse engineer existing code | SDD-RI artifacts |

---

## 4. FILE NAMING CONVENTIONS

### Specifications

```
specs/
├── todo-feature/           # kebab-case feature name
│   ├── spec.md             # Always spec.md
│   ├── plan.md             # Always plan.md
│   └── tasks.md            # Always tasks.md
```

### Prompt History Records

```
history/prompts/
├── constitution/
│   └── 001-initial-constitution-setup.constitution.prompt.md
├── general/
│   └── 001-create-skill.general.prompt.md
└── todo-feature/
    ├── 001-implement-task-model.tasks.prompt.md
    └── 002-add-crud-endpoints.green.prompt.md

Format: <ID>-<slug>.<stage>.prompt.md
Stages: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general
```

### Architecture Decision Records

```
history/adr/
├── 001-use-better-auth-for-authentication.md
├── 002-choose-neon-postgresql.md
└── 003-app-router-over-pages.md

Format: <ID>-<kebab-case-title>.md
```

### Skills and Agents

```
.claude/
├── skills/
│   ├── frontend.md         # Invokes agent
│   ├── nextjs-app-router.md  # Reference documentation
│   └── ...
└── agents/
    ├── frontend.md         # Agent definition
    └── ...
```

---

## 5. ENVIRONMENT CONFIGURATION

### Frontend Environment (`.env.local`)

```bash
# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database (for Better Auth)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Auth secret (MUST match backend JWT_SECRET)
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
```

### Backend Environment (`.env`)

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# JWT (MUST match frontend BETTER_AUTH_SECRET)
JWT_SECRET=your-super-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Debug
DEBUG=false
```

### Git Ignore Patterns

```gitignore
# Environment files
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
.venv/

# Build outputs
.next/
dist/
build/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
```

---

## 6. CREATING NEW FEATURES

### Manual Process

```bash
# 1. Create feature directory
mkdir -p specs/my-feature

# 2. Copy templates
cp .specify/templates/spec-template.md specs/my-feature/spec.md
cp .specify/templates/plan-template.md specs/my-feature/plan.md
cp .specify/templates/tasks-template.md specs/my-feature/tasks.md

# 3. Create PHR directory
mkdir -p history/prompts/my-feature
```

### Using Spec-Kit Commands

```bash
# Create specification interactively
/sp.specify my-feature

# Clarify requirements
/sp.clarify

# Create implementation plan
/sp.plan

# Generate task breakdown
/sp.tasks

# Execute implementation
/sp.implement
```

---

## 7. AGENT-SKILL RELATIONSHIP

### How Agents and Skills Work Together

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENT-SKILL ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User Request                                                           │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────┐                                                    │
│  │  Main Claude    │  Reads CLAUDE.md + Skills                          │
│  │  (Orchestrator) │                                                    │
│  └────────┬────────┘                                                    │
│           │                                                             │
│           ▼ Matches skill description                                   │
│  ┌─────────────────┐                                                    │
│  │   Skill File    │  Provides context and invocation pattern           │
│  │ (.claude/skills)│                                                    │
│  └────────┬────────┘                                                    │
│           │                                                             │
│           ▼ Invokes Task tool with subagent_type                        │
│  ┌─────────────────┐                                                    │
│  │ Specialized     │  Has specific tools and capabilities               │
│  │ Agent           │                                                    │
│  └────────┬────────┘                                                    │
│           │                                                             │
│           ▼ Executes task                                               │
│  ┌─────────────────┐                                                    │
│  │   Code Output   │  Creates/modifies files                            │
│  └─────────────────┘                                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Types and Their Skills

| Agent Type | Skill | Purpose |
|------------|-------|---------|
| `frontend-generator` | `frontend.md` | Build Next.js components and pages |
| `backend-generator` | `backend.md` | Build FastAPI infrastructure |
| `auth-implementor` | `auth.md` | Set up authentication |
| `database-schema` | `database.md` | Design database models |
| `api-router` | `api.md` | Implement REST endpoints |

### Reference Skills (No Agent Invocation)

These skills provide reference documentation, not agent invocation:

| Skill | Purpose |
|-------|---------|
| `nextjs-app-router.md` | Next.js 16 patterns reference |
| `fastapi-sqlmodel.md` | FastAPI/SQLModel patterns reference |
| `better-auth-integration.md` | Authentication patterns reference |
| `monorepo-structure.md` | Project organization reference |

---

## 8. CONSTITUTION COMPLIANCE

### Every Code Change Must

1. **Follow Technology Standards**
   - Frontend: Next.js 16, TypeScript strict, Tailwind CSS
   - Backend: FastAPI, Python 3.11+, SQLModel
   - Auth: Better Auth + JWT
   - Database: Neon PostgreSQL

2. **Maintain Security Requirements**
   - Auth on all protected endpoints
   - User data isolation
   - No hardcoded secrets
   - Explicit CORS origins

3. **Support Modularity**
   - Clean layer separation
   - Independent deployability
   - Explicit cross-layer contracts

4. **Ensure Developer Experience**
   - Strong typing everywhere
   - Consistent naming
   - Clear error messages

5. **Guarantee Reliability**
   - Proper HTTP status codes
   - Comprehensive validation
   - Graceful error handling

---

## 9. INITIALIZATION CHECKLIST

### Setting Up a New Project

```markdown
## Project Initialization Checklist

### 1. Create Directory Structure
- [ ] Create root project directory
- [ ] Initialize git repository
- [ ] Create `.claude/`, `.specify/`, `specs/`, `history/` directories
- [ ] Create `frontend/` and `backend/` directories

### 2. Configure Spec-Kit Plus
- [ ] Copy templates to `.specify/templates/`
- [ ] Create constitution at `.specify/memory/constitution.md`
- [ ] Set up scripts in `.specify/scripts/bash/`

### 3. Configure AI Agents
- [ ] Create agent definitions in `.claude/agents/`
- [ ] Create skills in `.claude/skills/`
- [ ] Create CLAUDE.md with project instructions

### 4. Initialize Frontend
- [ ] Create Next.js 16 app with App Router
- [ ] Configure TypeScript strict mode
- [ ] Set up Tailwind CSS
- [ ] Configure Better Auth
- [ ] Create `.env.local` template

### 5. Initialize Backend
- [ ] Create FastAPI application structure
- [ ] Set up SQLModel and database connection
- [ ] Configure JWT verification
- [ ] Create `.env` template
- [ ] Set up pytest

### 6. Configure Development Environment
- [ ] Create root `package.json` (if using workspaces)
- [ ] Set up `.gitignore`
- [ ] Create development scripts
- [ ] Document setup in README.md

### 7. Verify Constitution Compliance
- [ ] Review constitution principles
- [ ] Ensure technology standards match
- [ ] Verify security requirements
- [ ] Confirm folder structure alignment
```

---

## 10. QUICK REFERENCE

### Key File Locations

| What | Where |
|------|-------|
| Project principles | `.specify/memory/constitution.md` |
| Feature specs | `specs/<feature>/spec.md` |
| Implementation plans | `specs/<feature>/plan.md` |
| Task breakdowns | `specs/<feature>/tasks.md` |
| Prompt history | `history/prompts/` |
| Architecture decisions | `history/adr/` |
| AI agent configs | `.claude/agents/` |
| Workflow skills | `.claude/skills/` |
| Frontend app | `frontend/app/` |
| Backend API | `backend/routes/` |
| Database models | `backend/models.py` |

### Development Commands

```bash
# Frontend
cd frontend && npm run dev     # Start dev server (port 3000)
cd frontend && npm run build   # Build for production
cd frontend && npm run lint    # Run ESLint

# Backend
cd backend && uvicorn main:app --reload  # Start dev server (port 8000)
cd backend && pytest                      # Run tests
cd backend && pip install -r requirements.txt  # Install dependencies

# Spec-Kit Plus
/sp.specify <feature>   # Create new spec
/sp.plan                # Create implementation plan
/sp.tasks               # Generate tasks
/sp.implement           # Execute implementation
```

---

## Execution

When this skill is invoked, Claude should:

1. **Analyze the request** to determine which structural pattern applies
2. **Check existing structure** for consistency
3. **Follow constitution** technology standards and folder conventions
4. **Create directories** following the established patterns
5. **Include appropriate files** with correct naming conventions
6. **Maintain Spec-Kit Plus** workflow compatibility
7. **Document structural decisions** if significant

### Example Prompts

- "Set up the project structure for my todo app"
- "Create a new feature specification directory"
- "Where should I put the new API endpoint?"
- "How should I organize my React components?"
- "Set up the Spec-Kit Plus workflow"
- "Initialize the monorepo structure"
