"""
Chatbot API Routes

Routes for the AI-powered todo chatbot functionality.
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
import httpx
from models import User, Conversation, Message, MessageRole
from schemas import ChatRequest, ChatResponse, ToolCall
from routes.auth import get_current_user_id
from db import get_session
import asyncio
import os
from openai import OpenAI


router = APIRouter(prefix="/api", tags=["chatbot"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_with_bot(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Chat endpoint for AI-powered todo management.

    Receives natural language input and processes it using AI agent with MCP tools.
    """
    # Verify user access
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Verify user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get or create conversation
    conversation_id = request.conversation_id
    if conversation_id:
        # Verify conversation belongs to user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id

    # Add user message to conversation
    user_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=MessageRole.USER,
        content=request.message
    )
    session.add(user_message)
    session.commit()

    # Process the natural language request using AI and MCP tools
    response_data = await process_natural_language_request_with_openai(
        user_id=user_id,
        message=request.message,
        session=session
    )

    ai_response = response_data.get("response", "")
    tool_calls = response_data.get("tool_calls", [])

    # Add AI response to conversation
    ai_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=MessageRole.ASSISTANT,
        content=ai_response
    )
    session.add(ai_message)
    session.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        response=ai_response,
        tool_calls=tool_calls
    )


async def process_natural_language_request_with_openai(user_id: str, message: str, session: Session):
    """
    Process natural language request using OpenAI Functions API.

    This implementation uses OpenAI's Functions API to call our backend methods directly.
    """
    # This would require the OPENAI_API_KEY to be set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # For development without API key, return a mock response
        # This is a fallback that simulates AI behavior for development
        mock_responses = {
            "hello": "Hello! I'm your AI assistant. How can I help you with your tasks today?",
            "hi": "Hi there! I'm ready to help you manage your tasks.",
            "help": "I can help you add, list, update, complete, or delete tasks. Try saying 'add a task to buy groceries' or 'show me my tasks'.",
            "default": f"I received your message: '{message}'. For actual AI responses, please configure your OPENAI_API_KEY environment variable."
        }

        lower_msg = message.lower()
        if "hello" in lower_msg:
            response_text = mock_responses["hello"]
        elif "hi " in lower_msg or lower_msg.startswith("hi"):
            response_text = mock_responses["hi"]
        elif "help" in lower_msg or "what can you" in lower_msg:
            response_text = mock_responses["help"]
        else:
            response_text = mock_responses["default"]

        return {
            "response": response_text,
            "tool_calls": []
        }

    client = OpenAI(api_key=api_key)

    # Define available functions (these represent our MCP tools)
    functions = [
        {
            "name": "add_task",
            "description": "Add a new task to the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user's ID"},
                    "title": {"type": "string", "description": "The title of the task"},
                    "description": {"type": "string", "description": "The description of the task"}
                },
                "required": ["user_id", "title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "List tasks for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user's ID"},
                    "status": {"type": "string", "description": "Filter by status: all, pending, completed"}
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user's ID"},
                    "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user's ID"},
                    "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Update a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user's ID"},
                    "task_id": {"type": "integer", "description": "The ID of the task to update"},
                    "title": {"type": "string", "description": "The new title for the task"},
                    "description": {"type": "string", "description": "The new description for the task"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    ]

    try:
        # First, get the initial response from OpenAI to determine if tools should be called
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful todo list assistant. Help the user manage their tasks.
                    Use the available tools to add, list, update, complete, or delete tasks.
                    When the user asks to add a task, use the add_task tool.
                    When the user asks to see tasks, use the list_tasks tool.
                    When the user asks to complete a task, use the complete_task tool.
                    When the user asks to delete a task, use the delete_task tool.
                    When the user asks to update a task, use the update_task tool.
                    Be concise and friendly in your responses.
                    Always confirm actions you take and provide specific details."""
                },
                {"role": "user", "content": message}
            ],
            tools=[{"type": "function", "function": func} for func in functions],
            tool_choice="auto"
        )

        # Process the response
        response_message = response.choices[0].message
        final_response = ""

        # Check if the model wants to call any tools
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            # Prepare messages for the second call, including the tool responses
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful todo list assistant. Help the user manage their tasks.
                    Use the available tools to add, list, update, complete, or delete tasks.
                    When the user asks to add a task, use the add_task tool.
                    When the user asks to see tasks, use the list_tasks tool.
                    When the user asks to complete a task, use the complete_task tool.
                    When the user asks to delete a task, use the delete_task tool.
                    When the user asks to update a task, use the update_task tool.
                    Be concise and friendly in your responses.
                    Always confirm actions you take and provide specific details."""
                },
                {"role": "user", "content": message},
                response_message  # The initial response with tool calls
            ]

            # Make HTTP requests to MCP server and collect results
            tool_results = []
            async with httpx.AsyncClient(timeout=30.0) as client_http:
                for tool_call in response_message.tool_calls:
                    import json
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    try:
                        # Map function names to MCP endpoints
                        mcp_endpoint_map = {
                            "add_task": "/mcp/tools/add_task",
                            "list_tasks": "/mcp/tools/list_tasks",
                            "complete_task": "/mcp/tools/complete_task",
                            "delete_task": "/mcp/tools/delete_task",
                            "update_task": "/mcp/tools/update_task"
                        }

                        if function_name in mcp_endpoint_map:
                            # Add user_id to the parameters
                            mcp_params = {**function_args, "user_id": user_id}

                            # Make HTTP request to MCP server
                            mcp_response = await client_http.post(
                                f"http://localhost:8002{mcp_endpoint_map[function_name]}",
                                json=mcp_params
                            )

                            if mcp_response.status_code == 200:
                                result = mcp_response.json()["result"]

                                # Add the tool result to messages for the AI to process
                                messages.append({
                                    "role": "tool",
                                    "content": json.dumps(result),
                                    "tool_call_id": tool_call.id
                                })

                                # Record the successful tool call
                                tool_results.append({"name": function_name, "arguments": function_args})
                            else:
                                error_result = {"error": f"MCP server error: {mcp_response.text}", "status_code": mcp_response.status_code}
                                messages.append({
                                    "role": "tool",
                                    "content": json.dumps(error_result),
                                    "tool_call_id": tool_call.id
                                })
                                print(f"MCP server error for {function_name}: {mcp_response.text}")
                        else:
                            error_result = {"error": f"Unknown function: {function_name}"}
                            messages.append({
                                "role": "tool",
                                "content": json.dumps(error_result),
                                "tool_call_id": tool_call.id
                            })

                    except httpx.RequestError as e:
                        error_result = {"error": f"HTTP request failed: {str(e)}"}
                        messages.append({
                            "role": "tool",
                            "content": json.dumps(error_result),
                            "tool_call_id": tool_call.id
                        })
                        print(f"Error calling MCP server {function_name}: {str(e)}")
                    except Exception as e:
                        error_result = {"error": str(e)}
                        messages.append({
                            "role": "tool",
                            "content": json.dumps(error_result),
                            "tool_call_id": tool_call.id
                        })
                        print(f"Error executing tool {function_name}: {str(e)}")

            # Call the API again with the tool results to get the final response
            if len(messages) > 2:  # We have tool results to process
                final_response_obj = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                final_response = final_response_obj.choices[0].message.content

        elif hasattr(response_message, 'function_call') and response_message.function_call:
            # Handle legacy function call format
            function_call = response_message.function_call
            import json
            function_name = function_call.name
            function_args = json.loads(function_call.arguments)

            # Map function names to MCP endpoints
            mcp_endpoint_map = {
                "add_task": "/mcp/tools/add_task",
                "list_tasks": "/mcp/tools/list_tasks",
                "complete_task": "/mcp/tools/complete_task",
                "delete_task": "/mcp/tools/delete_task",
                "update_task": "/mcp/tools/update_task"
            }

            # Prepare messages for the second call
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful todo list assistant. Help the user manage their tasks.
                    Use the available tools to add, list, update, complete, or delete tasks.
                    When the user asks to add a task, use the add_task tool.
                    When the user asks to see tasks, use the list_tasks tool.
                    When the user asks to complete a task, use the complete_task tool.
                    When the user asks to delete a task, use the delete_task tool.
                    When the user asks to update a task, use the update_task tool.
                    Be concise and friendly in your responses.
                    Always confirm actions you take and provide specific details."""
                },
                {"role": "user", "content": message},
                response_message  # The initial response with function call
            ]

            try:
                if function_name in mcp_endpoint_map:
                    # Add user_id to the parameters
                    mcp_params = {**function_args, "user_id": user_id}

                    # Make HTTP request to MCP server
                    async with httpx.AsyncClient(timeout=30.0) as client_http:
                        mcp_response = await client_http.post(
                            f"http://localhost:8002{mcp_endpoint_map[function_name]}",
                            json=mcp_params
                        )

                        if mcp_response.status_code == 200:
                            result = mcp_response.json()["result"]

                            # Add the tool result to messages for the AI to process
                            messages.append({
                                "role": "function",
                                "name": function_name,
                                "content": json.dumps(result)
                            })
                        else:
                            error_result = {"error": f"MCP server error: {mcp_response.text}", "status_code": mcp_response.status_code}
                            messages.append({
                                "role": "function",
                                "name": function_name,
                                "content": json.dumps(error_result)
                            })
                            print(f"MCP server error for {function_name}: {mcp_response.text}")
                else:
                    error_result = {"error": f"Unknown function: {function_name}"}
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(error_result)
                    })

            except httpx.RequestError as e:
                error_result = {"error": f"HTTP request failed: {str(e)}"}
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(error_result)
                })
                print(f"Error calling MCP server {function_name}: {str(e)}")
            except Exception as e:
                error_result = {"error": str(e)}
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(error_result)
                })
                print(f"Error executing tool {function_name}: {str(e)}")

            # Call the API again with the tool results to get the final response
            if len(messages) > 2:  # We have tool results to process
                final_response_obj = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                final_response = final_response_obj.choices[0].message.content

        else:
            # No function calls were made, just return the AI's response
            final_response = response_message.content or "I processed your request."

        # Return the final response with empty tool_calls for now (since they've been processed)
        return {
            "response": final_response or "I've processed your request.",
            "tool_calls": []  # Tool calls have already been processed
        }

    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error processing your request: {str(e)}",
            "tool_calls": []
        }