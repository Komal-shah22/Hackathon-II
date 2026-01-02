import os
import json
import asyncio
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
import openai

from auth import get_current_user_id
from mcp_server import mcp_server
from mcp_server.handlers import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)
from mcp_server.schemas import (
    AddTaskInput, ListTasksInput, CompleteTaskInput,
    DeleteTaskInput, UpdateTaskInput, AddTaskOutput, ListTasksOutput,
    CompleteTaskOutput, DeleteTaskOutput, UpdateTaskOutput
)
from db import get_session
from models import Conversation, Message

router = APIRouter(
    prefix="/api/{user_id}/chat",
    tags=["Chat"],
    dependencies=[Depends(get_current_user_id)]
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List[dict]] = None

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: str

class ConversationCreateResponse(BaseModel):
    id: int
    messages: List[MessageResponse] = []

# TaskBot Assistant Instructions
ASSISTANT_INSTRUCTIONS = """
You are TaskBot, an expert at managing a user's tasks through natural language conversation.
You can help users create, list, complete, update, and delete tasks from their todo list.

Your capabilities:
1. Add tasks: When a user wants to add a task, use the add_task tool with a clear title and optional description.
2. List tasks: Use list_tasks to show the user's current tasks. Present them in a clear, organized manner.
3. Complete tasks: Mark tasks as done using complete_task. Users may refer to tasks by position ("first task"), title, or description.
4. Update tasks: Modify task details (title, description, priority, category, due date) using update_task.
5. Delete tasks: Remove tasks using delete_task.

Important guidelines:
- Be concise and helpful in your responses
- When listing tasks, include their status (completed/pending), priority, and category if available
- If a user mentions "it" or refers to a previously discussed task, use context to identify which task they mean
- Confirm actions with the user (e.g., "I've added 'Buy milk' to your tasks.")
- If you need clarification, ask polite questions

Current date context is available if needed for due date recommendations.
"""

# Maximum number of messages to include in context window
MAX_HISTORY_MESSAGES = 20


TOOL_HANDLERS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}

INPUT_SCHEMAS = {
    "add_task": AddTaskInput,
    "list_tasks": ListTasksInput,
    "complete_task": CompleteTaskInput,
    "delete_task": DeleteTaskInput,
    "update_task": UpdateTaskInput,
}


def get_openai_client() -> openai.Client:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.Client(api_key=api_key)


# Dependency for OpenAI client
OpenAIClientDep = Annotated[openai.Client, Depends(get_openai_client)]


async def get_openai_tool_definitions(mcp_server_instance):
    """Convert MCP tools to OpenAI tool format."""
    # Define tools directly in OpenAI format
    openai_tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's ID"
                        },
                        "title": {
                            "type": "string",
                            "description": "Task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional task description"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Task priority level"
                        },
                        "category": {
                            "type": "string",
                            "description": "Task category (e.g., work, personal, shopping)"
                        }
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List user's tasks with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's ID"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter by task status"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Filter by priority"
                        },
                        "category": {
                            "type": "string",
                            "description": "Filter by category"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's ID"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The task ID to complete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's ID"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The task ID to delete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's ID"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The task ID to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "New priority level"
                        },
                        "category": {
                            "type": "string",
                            "description": "New category"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]
    
    return openai_tools


def save_message(
    session: Session,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_call_id: Optional[str] = None
) -> Message:
    """Persist a message to the database."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_call_id=tool_call_id
    )
    session.add(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = message.created_at

    session.commit()
    session.refresh(message)
    return message


def get_conversation_messages(
    session: Session,
    conversation_id: int,
    limit: int = MAX_HISTORY_MESSAGES
) -> List[Message]:
    """Retrieve messages for a conversation with sliding window limit."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = session.exec(statement).all()

    # Apply sliding window - only return the most recent messages
    if len(messages) > limit:
        return messages[-limit:]
    return messages


def get_or_create_conversation(
    session: Session,
    user_id: str,
    conversation_id: Optional[int] = None
) -> Conversation:
    """Get an existing conversation or create a new one."""
    if conversation_id:
        # Verify the conversation belongs to the user
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or access denied"
            )
        return conversation

    # Create a new conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


@router.post("/", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    openai_client: OpenAIClientDep,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    T016: Core chat endpoint logic for natural language task management.

    - Creates or retrieves conversation
    - Saves user message to database
    - Gets message history (sliding window)
    - Invokes TaskBot agent with tools
    - Saves assistant response to database
    - Returns response with conversation_id
    """
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Get or create conversation with proper session management
    conversation = get_or_create_conversation(session, user_id, request.conversation_id)
    conversation_id = conversation.id

    # Save user message
    save_message(session, conversation_id, user_id, "user", request.message)

    # Get message history for context (sliding window)
    history_messages = get_conversation_messages(session, conversation_id)

    # 1. Get tools from MCP server in OpenAI format
    tools = await get_openai_tool_definitions(mcp_server)

    # 2. Build messages array with history for the agent
    messages_for_agent = []

    # Add recent history (excluding the just-saved user message since we'll add it fresh)
    for msg in history_messages[:-1] if len(history_messages) > 0 else []:
        messages_for_agent.append({
            "role": msg.role,
            "content": msg.content
        })

    # Add the current user message
    messages_for_agent.append({
        "role": "user",
        "content": request.message
    })

    # 3. Create a thread with message history
    thread = openai_client.beta.threads.create(
        messages=messages_for_agent
    )

    # 4. Create assistant with tools and run
    assistant = openai_client.beta.assistants.create(
        name="TaskBot",
        instructions=ASSISTANT_INSTRUCTIONS,
        tools=tools,
        model="gpt-4-turbo-preview",
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # 5. Wait for the run to complete and handle tool calls
    tool_calls_made = []
    while run.status in ["queued", "in_progress", "requires_action"]:
        if run.status == "requires_action" and run.required_action:
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Track tool calls for response
                tool_calls_made.append({
                    "name": tool_name,
                    "arguments": tool_args
                })

                # Add user_id to arguments if not present
                if "user_id" not in tool_args:
                    tool_args["user_id"] = user_id

                # Get the handler function
                handler = TOOL_HANDLERS.get(tool_name)
                if not handler:
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({"error": f"Unknown tool: {tool_name}"}),
                    })
                    continue

                # Call the handler
                try:
                    input_schema = INPUT_SCHEMAS[tool_name]
                    typed_input = input_schema(**tool_args)
                    
                    # Call handler with typed input, user_id, and session
                    result = handler(input=typed_input, user_id=user_id, session=session)
                    
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result.model_dump()),
                    })
                except Exception as e:
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({"error": str(e)}),
                    })

            # Submit tool outputs
            run = openai_client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs,
            )

        # Wait for a short period before checking the status again
        await asyncio.sleep(1)
        run = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # 6. Get the final response
    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = "No response from assistant."
    for msg in messages.data:
        if msg.role == "assistant":
            assistant_response = msg.content[0].text.value
            break

    # 7. Save assistant response to database
    save_message(session, conversation_id, user_id, "assistant", assistant_response)

    return ChatResponse(
        conversation_id=conversation_id,
        response=assistant_response,
        tool_calls=tool_calls_made if tool_calls_made else None
    )


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    user_id: str,
    conversation_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """T028: Retrieve conversation messages for frontend history display."""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Verify conversation exists and belongs to user
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = session.exec(statement).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get messages
    messages = get_conversation_messages(session, conversation_id, limit=100)

    return [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at.isoformat()
        )
        for msg in messages
    ]


@router.get("/conversations", response_model=List[ConversationCreateResponse])
async def list_conversations(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """List all conversations for a user."""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = session.exec(statement).all()

    result = []
    for conv in conversations:
        # Get message count for each conversation
        msg_statement = select(Message).where(
            Message.conversation_id == conv.id
        )
        messages = session.exec(msg_statement).all()
        result.append(ConversationCreateResponse(
            id=conv.id,
            messages=[
                MessageResponse(
                    id=msg.id,
                    conversation_id=msg.conversation_id,
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at.isoformat()
                )
                for msg in messages[:3]  # Only first 3 messages for preview
            ]
        ))

    return result
