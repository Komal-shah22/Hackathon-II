# Agents Configuration

This document defines the specialized agents available for this project.

## Available Agents

### backend-generator
Purpose: FastAPI backend infrastructure
- Database models with SQLModel
- REST API endpoints
- JWT authentication
- Database connections

### frontend-generator
Purpose: Next.js frontend components
- App Router pages and layouts
- React components
- API client integration
- Authentication UI

### auth-implementor
Purpose: Authentication setup
- Better Auth configuration
- JWT verification
- Protected routes

### database-schema
Purpose: Database design
- SQLModel definitions
- Schema migrations
- Performance optimization

### api-router
Purpose: REST API implementation
- Endpoint handlers
- Request validation
- Response formatting

## Usage

Claude automatically invokes the appropriate agent based on your request.

---

## Phase 3: AI-Powered Chatbot (NEW)

### Objective
Transform the existing Phase 2 todo app by adding an AI-powered chatbot interface using OpenAI ChatKit, Agents SDK, and MCP Server.

### Technology Stack Addition
- Frontend: OpenAI ChatKit (AI chat UI)
- Backend: OpenAI Agents SDK (AI logic)
- Backend: MCP Server (Model Context Protocol - Official SDK)
- Tools: 5 MCP tools for task operations

### Architecture Principles
1. **Stateless Backend**: All conversation state stored in database
2. **MCP Tools**: Standardized interface for AI to interact with app
3. **Natural Language**: Users interact via chat, not forms/buttons
4. **Conversation Persistence**: Chat history survives server restarts
5. **Security**: Same JWT authentication, user isolation

### Key Components to Build
1. MCP Server with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
2. Chat API endpoint (POST /api/{user_id}/chat)
3. OpenAI Agents SDK integration
4. ChatKit frontend UI
5. Conversation and Messages database tables

### Integration with Phase 2
- Phase 2 dashboard continues to work
- Phase 3 adds new /chatbot route
- Both interfaces share same backend database
- Users can switch between UI and chat

### Non-Negotiable Requirements
- Stateless architecture (database-backed conversations)
- MCP protocol compliance
- All 5 MCP tools implemented
- JWT security on chat endpoint
- User isolation (can only access own tasks)
- Conversation history persistence
