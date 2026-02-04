# Phase III: AI-Powered Todo Chatbot

## Overview
This phase implements an AI-powered chatbot for managing todo lists through natural language. The system integrates OpenAI's API with our existing todo application to provide a conversational interface for task management.

## Features Implemented

### Core Chatbot Functionality
- Natural language processing for task management
- Integration with existing task database
- Conversation persistence in database
- User authentication and isolation

### MCP (Model Context Protocol) Server
- Standalone server exposing task operations as tools
- Secure user authentication and isolation
- Implements all required MCP tools:
  - `add_task`: Create new tasks
  - `list_tasks`: Retrieve tasks with filtering
  - `complete_task`: Mark tasks as complete
  - `delete_task`: Remove tasks
  - `update_task`: Modify task details

### Frontend Integration
- Dedicated chat interface
- Real-time conversation display
- User authentication integration
- Responsive design

## Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │    Neon DB      │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │  (PostgreSQL)   │
│  (Frontend)     │     │  │  POST /api/{user_id}/chat             │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │  - tasks        │
│                 │     │                  │                           │     │  - conversations│
│                 │     │                  ▼                           │     │  - messages     │
│                 │◀────│  ┌────────────────────────────────────────┐  │     │                 │
│                 │     │  │      OpenAI Integration                │  │     │                 │
│                 │     │  │      (Functions API)                   │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                     │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## API Endpoints

### Chat Endpoint
- `POST /api/{user_id}/chat` - Chat with AI assistant
  - Request: `{ "message": "string", "conversation_id": "number (optional)" }`
  - Response: `{ "conversation_id": "number", "response": "string", "tool_calls": "array" }`

### Existing Task Endpoints (Inherited from Phase II)
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Database Schema

### New Tables for Chatbot
- **conversations** table
  - id: integer (primary key)
  - user_id: string (foreign key -> users.id)
  - created_at: timestamp
  - updated_at: timestamp

- **messages** table
  - id: integer (primary key)
  - conversation_id: integer (foreign key -> conversations.id)
  - user_id: string (foreign key -> users.id)
  - role: string (enum: 'user', 'assistant')
  - content: text (not null)
  - created_at: timestamp

## Environment Variables

### Backend
- `OPENAI_API_KEY` - Required for AI functionality
- `DATABASE_URL` - Database connection string
- `BETTER_AUTH_SECRET` - Authentication secret

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_OPENAI_API_KEY` - Frontend API key (if needed)

## Installation and Setup

### Backend
1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY='your-openai-api-key'
export DATABASE_URL='your-database-url'
export BETTER_AUTH_SECRET='your-auth-secret'
```

3. Start the services:
```bash
# Option 1: Run both servers separately
python -m uvicorn main:app --port 8000  # Main API
python -m uvicorn mcp_server.server:app --port 8001  # MCP Server

# Option 2: Use the start script
python start_services.py
```

### Frontend
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set environment variables in `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

## Usage Examples

The AI chatbot understands natural language commands such as:

- "Add a task to buy groceries"
- "Show me my pending tasks"
- "Mark task 3 as complete"
- "Delete the meeting task"
- "Change task 1 to 'Call mom tonight'"
- "What have I completed?"

## Error Handling

- Invalid requests return appropriate HTTP status codes
- Authentication failures are properly handled
- Database errors are caught and logged
- AI service errors are gracefully handled with fallback messages

## Security Considerations

- All endpoints require JWT authentication
- Users can only access their own data
- MCP tools verify user permissions before operations
- Rate limiting is implemented on API endpoints

## Testing

To test the chatbot functionality:
1. Sign in to the application
2. Navigate to the "AI Chatbot" page
3. Type natural language commands to manage tasks
4. Verify that tasks are created, updated, and modified as expected

## Future Enhancements

- Voice command integration
- Support for multiple languages
- Advanced natural language understanding
- Integration with calendar services
- Enhanced conversation memory