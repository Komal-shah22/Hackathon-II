<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.1.0 (MINOR: Added Phase 3 AI Chatbot principles and agents)

Modified principles:
- I. AI-First Architecture (Added Phase 3 agent triggers and skill integration)
- II. Security by Design (Added MCP tool user ownership validation)
- III. Scalability and Modularity (Added OpenAI SDK and MCP Server to technology standards)
- V. Reliability and Correctness (Added stateless conversation persistence requirement)

Added sections:
- VI. Stateless AI Interactions (New principle for Phase 3 architecture)

Templates requiring updates:
- .specify/templates/plan-template.md ✅ Compatible
- .specify/templates/spec-template.md ✅ Compatible
- .specify/templates/tasks-template.md ✅ Compatible

Follow-up TODOs: None
==================
-->

# AI-Native Full-Stack Hackathon Platform Constitution

## Core Principles

### I. AI-First Architecture

Agents and skills drive the development workflow. The system MUST be designed around AI-assisted
code generation, with clear separation between specialized agents and orchestration through skills.

- All significant implementation work MUST be routed through appropriate specialized agents:
  - **MCP Tools Generator**: For MCP server tools, Pydantic schemas, and tool validation.
  - **Chatbot Agent Integrator**: For OpenAI Agents SDK, chat endpoints, and conversation flow.
  - **ChatKit UI Builder**: For ChatKit components and chat frontend integration.
  - **Existing Agents**: Backend (FastAPI), Frontend (Next.js), Auth (Better Auth), Database (SQLModel).
- Skills MUST provide clear interfaces for common development tasks:
  - **MCP Protocol Standards**: Provides tool structure and security best practices.
  - **OpenAI Agents SDK Patterns**: Provides agent configuration and conversation management.
- Agent context MUST be maintained and updated as the codebase evolves.
- Human oversight remains required for architectural decisions and security-critical changes.

### II. Security by Design

Security MUST be built into every layer from the start. Authentication, authorization, and data
protection are non-negotiable.

- All API endpoints MUST require authentication unless explicitly public.
- User data MUST be isolated; queries MUST filter by authenticated user_id.
- **MCP Tools Ownership**: MCP tools MUST explicitly validate that the user has permission to
  access/modify the requested resource.
- Secrets and credentials MUST NEVER be hardcoded; environment variables are required.
- JWT tokens MUST be verified on every protected request.
- Input validation MUST occur at system boundaries (API endpoints, form submissions, MCP tools).
- CORS MUST be explicitly configured with specific allowed origins.

### III. Scalability and Modularity

The architecture MUST maintain clean separation between frontend, backend, auth, database, and AI layers.

- Frontend: Next.js 16 (App Router) + OpenAI ChatKit for conversation interfaces.
- Backend: FastAPI (routers/dependency injection) + OpenAI Agents SDK.
- Protocol: Official Model Context Protocol (MCP) for agent-to-app interaction.
- Auth: Better Auth (frontend) with JWT verification (backend).
- Database: SQLModel ORM with Neon PostgreSQL.
- Each layer MUST be developable independently through clear contracts/interfaces.

### IV. Developer Experience

The codebase MUST prioritize clarity, readability, and strong typing.

- TypeScript MUST be used for all frontend code with strict mode enabled.
- Python type hints MUST be used for all backend code.
- Naming conventions MUST be consistent and self-documenting.
- ESLint and formatting tools MUST be configured and enforced.
- Each module MUST include clear usage instructions.

### V. Reliability and Correctness

Data flows MUST be validated at every boundary. Error handling MUST be comprehensive and predictable.

- All API responses MUST use proper HTTP status codes.
- Pydantic models MUST validate all request/response data and MCP tool inputs.
- Database operations MUST handle errors and rollback on failure.
- Loading states MUST be shown during async operations (including AI message streaming).
- Error boundaries MUST catch and display errors gracefully in the frontend.

### VI. Stateless AI Interactions

Phase 3 architecture requires a strictly stateless backend to ensure scalability and persistence.

- **Stateless Backend**: The server MUST NOT store conversation state in memory.
- **Database Persistence**: All conversation history MUST be stored in the database.
- **Message Integrity**: Messages MUST be saved to the database after each agent run.
- **User Isolation**: Chat history and MCP tool access MUST be strictly limited to the owner.

## Technology Standards

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend Framework | Next.js | 16 with App Router |
| Chat UI | OpenAI ChatKit | Conversation components |
| AI Integration | OpenAI Agents SDK | Stateless orchestration |
| Protocol | MCP | Model Context Protocol |
| Backend Framework | FastAPI | Async endpoints |
| ORM | SQLModel | Hybrid SQLAlchemy/Pydantic |
| Database | Neon PostgreSQL | Serverless, SSL required |
| Authentication | Better Auth + JWT | Shared secret, HS256 |

**Folder Structure:**

```
frontend/           # Next.js 16 application
├── app/           # App Router pages (/dashboard, /chatbot)
├── components/    # Reusable UI components
└── lib/           # Utilities and API client

backend/            # FastAPI application
├── routes/        # API endpoint handlers (/chat, /todos)
├── mcp/           # MCP tool definitions and server
├── models.py      # SQLModel database models (Tasks, Conversations, Messages)
├── db.py          # Database connection
└── auth.py        # JWT verification

.claude/            # AI agent configuration
├── agents/        # Specialized agent definitions (Phase 2 + Phase 3)
├── skills/        # Development workflow skills (Protocol, SDK)
└── commands/      # Slash command definitions
```

## Development Workflow

### Workflow Integration (Phase 3)

1. **/sp.specify**:
   - MCP Tools Generator analyzes tool requirements.
   - Chatbot Agent Integrator designs conversation flow.
   - ChatKit UI Builder plans frontend interface.
   - Database Agent plans new tables (Conversations, Messages).

2. **/sp.plan**:
   - MCP Tools Generator creates MCP server architecture.
   - Chatbot Agent Integrator designs chat endpoint.
   - ChatKit UI Builder plans ChatKit integration.
   - All agents collaborate on stateless design.

3. **/sp.tasks**:
   - Tasks broken down by agent expertise (Tools, Endpoints, UI, Schema).

4. **/sp.implement**:
   - Route each task to the appropriate agent.
   - Agents use their respective specialized skills.
   - Maintain full compatibility with Phase 2 features.

### Quality Gates

1. **MCP Compliance**: Tools MUST follow MCP protocol standards and validation patterns.
2. **Stateless Check**: No in-memory conversation state is permitted.
3. **Security**: JWT validation for chat endpoints and user_id isolation in all tools.
4. **Phase 2 Preservation**: Dashboard and existing routes MUST remain functional.

## Governance

**Version**: 1.1.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-31
