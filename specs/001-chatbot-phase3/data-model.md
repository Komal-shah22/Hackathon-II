# Data Model: Phase 3 AI Chatbot

## Entities

### Conversation
Represents a unique chat session between a user and the AI assistant.

- **id**: `int` (Primary Key)
- **user_id**: `str` (Foreign Key to User)
- **created_at**: `datetime` (Default: now)
- **updated_at**: `datetime` (Default: now)

**Relationships**:
- Has many **Messages**.

### Message
Represents a single message within a conversation.

- **id**: `int` (Primary Key)
- **conversation_id**: `int` (Foreign Key to Conversation)
- **user_id**: `str` (Foreign Key to User)
- **role**: `str` (Enum: `user`, `assistant`, `system`, `tool`)
- **content**: `text`
- **tool_call_id**: `str` (Optional: for linking tool results)
- **created_at**: `datetime` (Default: now)

**Relationships**:
- Belongs to one **Conversation**.

## State Transitions

### Conversation Flow
1. **Initiated**: Triggered by user's first message to `/api/{user_id}/chat` without a `conversation_id`.
2. **Active**: Characterized by ongoing turns of `user` and `assistant` messages.
3. **Archived**: (Future scope) Conversation is closed or deleted.

## Validation Rules
- `conversation_id` MUST be valid and exist in the `conversations` table.
- `role` MUST be one of the specified enum values.
- `content` MUST NOT be empty for user messages.
- Total messages per conversation SHOULD be capped (or sliding window applied) for LLM context limits.
