# Phase III: AI-Powered Todo Chatbot Implementation Plan

## Objective
Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture and using Claude Code and Spec-Kit Plus.

## Architecture Overview
```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │    Neon DB      │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │  (PostgreSQL)   │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │  - tasks        │
│                 │     │                  │                           │     │  - conversations│
│                 │     │                  ▼                           │     │  - messages     │
│                 │◀────│  ┌────────────────────────────────────────┐  │     │                 │
│                 │     │  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                     │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## Components to Implement

### 1. MCP Server (Model Context Protocol)
- Create MCP server with Official MCP SDK
- Expose task operations as MCP tools
- Tools must match specifications in chatbot.md

### 2. FastAPI Backend Extensions
- Add chat endpoint POST /api/{user_id}/chat
- Integrate OpenAI Agents SDK
- Add conversation and message database models
- Implement stateless conversation flow

### 3. Database Extensions
- Add conversations table
- Add messages table
- Update existing models to support chatbot functionality

### 4. Frontend Integration
- Integrate OpenAI ChatKit
- Connect to chat endpoint
- Handle conversation state on frontend

## Implementation Steps

### Step 1: Database Layer
1. Extend SQLModel models to include conversations and messages
2. Create database migrations for new tables
3. Implement CRUD operations for conversation and message models

### Step 2: MCP Server
1. Set up MCP server infrastructure
2. Implement MCP tools for all task operations
3. Ensure tools authenticate and scope operations to user

### Step 3: Backend Integration
1. Add OpenAI Agents SDK integration
2. Create chat endpoint that connects agents to MCP tools
3. Implement conversation state management
4. Ensure JWT authentication works with chat endpoints

### Step 4: Frontend Integration
1. Set up OpenAI ChatKit
2. Connect to chat API endpoint
3. Handle JWT tokens in chat requests

## Technology Stack
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth

## Success Criteria
- Natural language commands work for all basic todo operations
- MCP tools are properly implemented and secured
- Conversations persist in database
- State is maintained correctly
- Error handling is graceful
- Authentication works properly