---
name: openai-agents-sdk
description: OpenAI Agents SDK usage patterns and best practices. Use when implementing AI agents, conversation management, or agent orchestration.
---

# OpenAI Agents SDK Patterns

## Agent Configuration
```python
from openai import OpenAI
from agents_sdk import Agent, Runner

agent = Agent(
    name="task-assistant",
    instructions="""
    You are a helpful task management assistant.
    Be concise, friendly, and action-oriented.
    Confirm actions and provide clear feedback.
    """,
    tools=[tool1, tool2, tool3],
    model="gpt-4"
)
```

## Running Agent
```python
runner = Runner(agent=agent)

result = runner.run(
    messages=[
        {"role": "user", "content": "Add a task to buy groceries"}
    ],
    context={"user_id": "user123"}
)

response = result.messages[-1].content
tool_calls = result.tool_calls
```

## Conversation Management
```python
# Build message history
messages = []

# Add system context
messages.append({
    "role": "system",
    "content": f"User ID: {user_id}"
})

# Add conversation history
for msg in db_messages:
    messages.append({
        "role": msg.role,
        "content": msg.content
    })

# Add new user message
messages.append({
    "role": "user",
    "content": new_message
})

# Run agent
result = runner.run(messages=messages)
```

## Error Handling
```python
try:
    result = runner.run(messages=messages)
    response = result.messages[-1].content
except OpenAIError as e:
    response = "I'm having trouble right now. Please try again."
    log_error(e)
except Exception as e:
    response = "Something went wrong. Please contact support."
    log_error(e)
```

## Best Practices

1. **Clear Instructions**: Agent needs good system prompt
2. **Context Management**: Include relevant context
3. **Tool Selection**: Let agent choose appropriate tools
4. **Error Recovery**: Graceful error handling
5. **Logging**: Log all interactions for debugging
```
