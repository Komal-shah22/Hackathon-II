from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routes.health import router as health_router
from routes.tasks import router as tasks_router
from routes.auth import router as auth_router
from routes.chatbot import router as chatbot_router
from db import init_db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Todo App API",
    description="Full-stack todo application API with authentication and task management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Additional common dev port
        "http://127.0.0.1:3001",
        "http://0.0.0.0:3000",   # Docker container access
        "http://localhost:3002",  # Additional common dev port
        "http://127.0.0.1:3002",
        "https://frontend-todo-smoky.vercel.app/",  # For Vercel deployments
        "http://localhost:19006",  # For Expo apps
        "exp://*",  # For Expo apps
        "*"  # Allow all origins in development - remove for production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    init_db()


# Include routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(chatbot_router)


@app.get("/")
def root():
    return {
        "message": "Todo App API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api-docs", response_class=HTMLResponse)
async def api_docs():
    """Returns HTML page with API documentation links"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo App API Documentation</title>
        <style>
            body { font-family: system-ui, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #fff; padding: 3px 8px; border-radius: 3px; }
            .get { background: #61affe; }
            .post { background: #49cc90; }
            .put { background: #fca130; }
            .patch { background: #50e3c2; }
            .delete { background: #f93e3e; }
            a { color: #0066cc; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Todo App API Documentation</h1>
        <p>Version: 1.0.0</p>
        <p>
            <a href="/docs">OpenAPI Docs (Swagger UI)</a> |
            <a href="/redoc">ReDoc</a> |
            <a href="/openapi.json">OpenAPI JSON</a>
        </p>
        <h2>Authentication Endpoints</h2>
        <div class="endpoint">
            <span class="method post">POST</span> <code>/auth/signup</code> - Create new account
        </div>
        <div class="endpoint">
            <span class="method post">POST</span> <code>/auth/signin</code> - Sign in to account
        </div>
        <div class="endpoint">
            <span class="method post">POST</span> <code>/auth/logout</code> - Sign out
        </div>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/auth/me</code> - Get current user
        </div>
        <h2>Task Endpoints</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/{user_id}/tasks</code> - List tasks (with filters, pagination)
        </div>
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/{user_id}/tasks</code> - Create task
        </div>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/{user_id}/tasks/{task_id}</code> - Get task
        </div>
        <div class="endpoint">
            <span class="method put">PUT</span> <code>/api/{user_id}/tasks/{task_id}</code> - Update task
        </div>
        <div class="endpoint">
            <span class="method delete">DELETE</span> <code>/api/{user_id}/tasks/{task_id}</code> - Delete task
        </div>
        <div class="endpoint">
            <span class="method patch">PATCH</span> <code>/api/{user_id}/tasks/{task_id}/complete</code> - Toggle completion
        </div>
        <h2>Statistics Endpoints</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/{user_id}/stats</code> - Get user statistics
        </div>
        <h2>Health Endpoints</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/health</code> - Health check
        </div>
        <h2>Chatbot Endpoints</h2>
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/{user_id}/chat</code> - Chat with AI assistant
        </div>
    </body>
    </html>
    """


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
