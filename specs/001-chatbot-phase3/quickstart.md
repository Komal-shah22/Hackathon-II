# Quickstart: Phase 3 AI-Powered Todo Chatbot

## Setup Instructions

### 1. Environment Variables
Add the following to your `backend/.env` file:
```bash
OPENAI_API_KEY=sk-...
```

### 2. Install Dependencies
```bash
# Backend
cd backend
pip install mcp openai-agents

# Frontend
cd frontend
npm install ai
```

### 3. Database Migration
```bash
cd backend
alembic revision --autogenerate -m "Add conversations and messages tables"
alembic upgrade head
```

### 4. Running the App
1. Start the FastAPI backend: `fastapi dev main.py`
2. Start the Next.js frontend: `npm run dev`
3. Navigate to `http://localhost:3000/chatbot` to start chatting with TaskBot.

## Key Files
- `backend/mcp_server/`: MCP tool definitions.
- `backend/routes/chat.py`: Main chat API logic.
- `frontend/app/chatbot/page.tsx`: Chat UI and streaming logic.
