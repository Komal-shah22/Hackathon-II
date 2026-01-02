# Phase 3 Research: AI-Powered Chatbot Integration

This document outlines the research findings for integrating OpenAI Agents SDK, MCP, and Chat UI patterns into the existing Phase 2 codebase.

## 1. OpenAI Agents SDK with Stateless FastAPI
Integrating the OpenAI Agents SDK into a stateless FastAPI backend requires externalizing session management.

- **Session Protocol**: The SDK uses a `Session` protocol for history. For statelessness, implement a custom session class that interfaces with PostgreSQL via SQLModel.
- **Pattern**:
    - Initialize your agent `Runner` on each request.
    - Retrieve message history from the database using the `conversation_id`.
    - Pass history to the runner (or use a DB-backed `Session` implementation).
    - Save new messages back to the database immediately after the LLM response.
- **Scalability**: For distributed environments, using a shared database (PostgreSQL/Neon) ensures that any FastAPI instance can handle any request for a given `conversation_id`.

## 2. Official MCP SDK (Python) for Database Tools
The Model Context Protocol (MCP) provides a standardized way to expose tools.

- **FastMCP**: Use the `FastMCP` class from the `mcp[server]` package for high-level tool definition.
- **Tool Definition**:
    ```python
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("AppServer")

    @mcp.tool()
    async def add_task(title: str, user_id: str) -> str:
        """Add a new task to the database."""
        # SQLModel database logic here
        return "Task created successfully."
    ```
- **Lifecycle**: Use `@mcp.lifespan` to manage database connection pools (Engine/Session) ensuring they are cleaned up correctly.

## 3. OpenAI ChatKit & Next.js 16 UI Patterns
Research indicates that **"@openai/chatkit"** is likely a placeholder name or a private/internal preview package. It is not currently available as a public package on npm.

- **Recommended Pattern**: Use **Vercel AI SDK** (`ai`) which is the industry standard for Next.js 16 (App Router) chat interfaces.
- **Key Hook**: `useChat` from `ai/react` handles streaming, message state, and API communication out-of-the-box.
- **Alternative**: For a purely OpenAI-native experience, use the `@openai/openai-sdk` to handle streaming and build a custom UI around a standard message list component.

## 4. Stateless Conversation Persistence (SQLModel/PostgreSQL)
To maintain statelessness while persisting conversations, a normalized schema is required.

### Recommended Schema
- **`Conversation` Table**:
    - `id`: UUID (Primary Key)
    - `user_id`: UUID (Foreign Key to User)
    - `created_at`: DateTime
- **`Message` Table**:
    - `id`: UUID (Primary Key)
    - `conversation_id`: UUID (Foreign Key to Conversation)
    - `role`: String (system, user, assistant, tool)
    - `content`: Text
    - `tool_call_id`: Optional[String] (for tool response mapping)
    - `created_at`: DateTime

### Performance Best Practices
- **Indexing**: Index `conversation_id` on the `Message` table for fast retrieval of history.
- **Pruning**: Implement a "windowed" history retrieval (e.g., last 20 messages) to keep token usage within limits while still providing sufficient context.
- **JSON Serialization**: Use SQLModel's `JSON` column type for complex tool outputs if necessary.

---
**Sources:**
- [OpenAI Agents SDK Python Repository](https://github.com/openai/openai-agents-python)
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Vercel AI SDK Documentation](https://ai-sdk.dev/docs/introduction)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
