# API Contract: Chat Endpoint

## POST /api/{user_id}/chat

Conversational interface endpoint for managing tasks through natural language.

### Security
- **Type**: JWT (Bearer)
- **Constraint**: `user_id` in path MUST match `user_id` in JWT payload.

### Request Body
```json
{
  "message": "string (The user's input message)",
  "conversation_id": "optional integer (Existing conversation ID to continue history)"
}
```

### Response Body
```json
{
  "conversation_id": "integer (ID of the conversation processed)",
  "response": "string (Natural language response from the assistant)",
  "tool_calls": "optional array (Details of any MCP tools invoked during this turn)"
}
```

### Errors
- **401 Unauthorized**: Missing or invalid JWT token.
- **403 Forbidden**: JWT user_id mismatch with path parameter.
- **404 Not Found**: Conversation ID provided does not exist or belong to the user.
- **500 Internal Server Error**: Downstream AI provider error or database failure.
