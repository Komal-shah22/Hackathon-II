# Phase 3 Research: AI-Powered Chatbot Integration

This document outlines the research findings for integrating OpenAI Agents SDK, MCP, and Chat UI patterns into the existing Phase 2 codebase.

## Decision: Stateless Backend with Database Persistence
**Decision**: Use a strictly stateless FastAPI backend where every request retrieves conversation history from PostgreSQL and persists new messages before responding.
**Rationale**: Aligns with Phase 3 objective for horizontal scalability and reliability (survives restarts).
**Alternatives considered**: In-memory session stores (rejected due to lack of persistence across restarts) or sticky sessions (rejected due to scalability constraints).

## Decision: Vercel AI SDK for Frontend
**Decision**: Use **Vercel AI SDK** (`ai` and `ai/react`) instead of `@openai/chatkit`.
**Rationale**: `@openai/chatkit` is identified as a placeholder; Vercel AI SDK is the modern standard for Next.js 16 (App Router) and provides `useChat` for streaming and message state management.
**Alternatives considered**: Building plain React state management (rejected as too complex for streaming) or using unofficial libraries.

## Decision: FastMCP for Python MCP Server
**Decision**: Use the official `mcp` Python SDK with the `FastMCP` class.
**Rationale**: Provides a high-level, declarative way to expose tools via the MCP protocol.
**Alternatives considered**: Building a raw JSON-RPC interface (rejected as reinventing the wheel and protocol non-compliant).

## Decision: Normalized Message Schema
**Decision**: Implement a `Conversation` table (meta) and a `Message` table (individual turns) in SQLModel.
**Rationale**: Essential for complex multi-turn context and avoids large JSON blobs in a single field.
**Alternatives considered**: Single JSON column for all messages in a `Conversation` table (rejected due to query limitations and message indexing needs).
