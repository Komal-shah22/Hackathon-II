# REST API Endpoints for AI Chatbot

## Base URL
- Development: http://localhost:8000
- Production: https://api.example.com

## Authentication
All endpoints require JWT token in header:
Authorization: Bearer <token>

## Chat Endpoint

### POST /api/{user_id}/chat
Send message to AI chatbot and get response.

#### Request
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conversation_id | integer | No | Existing conversation ID (creates new if not provided) |
| message | string | Yes | User's natural language message |

#### Response
| Field | Type | Description |
|-------|------|-------------|
| conversation_id | integer | The conversation ID |
| response | string | AI assistant's response |
| tool_calls | array | List of MCP tools invoked |

## Existing Task Endpoints (Inherited from Phase II)
All existing task endpoints remain the same with JWT authentication:
- GET /api/{user_id}/tasks - List all tasks
- POST /api/{user_id}/tasks - Create a new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update a task
- DELETE /api/{user_id}/tasks/{id} - Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

## Database Models for Chatbot

### Conversation Table
- id: integer (primary key)
- user_id: string (foreign key -> users.id)
- created_at: timestamp
- updated_at: timestamp

### Message Table
- id: integer (primary key)
- conversation_id: integer (foreign key -> conversations.id)
- user_id: string (foreign key -> users.id)
- role: string (user/assistant)
- content: text
- created_at: timestamp