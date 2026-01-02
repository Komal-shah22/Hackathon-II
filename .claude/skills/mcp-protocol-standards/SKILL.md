---
name: mcp-protocol-standards
description: MCP (Model Context Protocol) standards and best practices. Use when creating MCP servers, tools, or implementing protocol compliance.
---

# MCP Protocol Standards

## Overview
MCP (Model Context Protocol) is a standardized way to expose tools to AI agents.

## Tool Structure

Every MCP tool requires:
1. **Name**: Unique identifier (snake_case)
2. **Description**: What the tool does (for AI understanding)
3. **Input Schema**: Pydantic model for inputs
4. **Output Schema**: Pydantic model for outputs
5. **Handler Function**: Implementation logic

## Tool Definition Pattern
```python
from pydantic import BaseModel, Field
from typing import Optional

class ToolInput(BaseModel):
    """Input schema with validation"""
    required_field: str = Field(description="Required parameter")
    optional_field: Optional[str] = Field(None, description="Optional parameter")

class ToolOutput(BaseModel):
    """Output schema for consistent responses"""
    status: str
    data: dict
    message: Optional[str] = None

async def tool_handler(input: ToolInput) -> ToolOutput:
    """Implementation logic"""
    try:
        # Process input
        result = do_something(input.required_field)

        return ToolOutput(
            status="success",
            data=result,
            message="Operation completed"
        )
    except Exception as e:
        return ToolOutput(
            status="error",
            data={},
            message=str(e)
        )
```

## Best Practices

1. **Clear Descriptions**: AI needs good descriptions to choose tools
2. **Type Safety**: Use Pydantic for validation
3. **Error Handling**: Always return structured errors
4. **Idempotency**: Same input = same output
5. **Documentation**: Document expected behavior

## Security

- Validate all inputs
- Check authentication
- Enforce user isolation
- Log tool usage
- Rate limiting (if needed)
