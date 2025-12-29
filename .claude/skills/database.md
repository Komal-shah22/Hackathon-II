---
description: Design database schemas, create SQLModel classes, and configure Neon PostgreSQL connections.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Database Schema Designer

This skill invokes the **database-schema** agent to design and implement database infrastructure for the todo application.

### When to Use

- Designing database schemas and table structures
- Creating SQLModel class definitions
- Setting up Neon PostgreSQL connections
- Adding indexes for query performance
- Implementing timestamp fields (created_at, updated_at)
- Configuring foreign key relationships
- Setting up database session management

### Execution

**Invoke the database-schema agent** with the user's request to:

1. Read database specifications from `specs/database/` if available
2. Design SQLModel classes with proper typing
3. Configure database connection with environment variables
4. Add strategic indexes based on query patterns
5. Implement auto-generated timestamps
6. Set up session dependency injection

### Output Structure

The agent will create/modify:
- `models.py` - SQLModel class definitions
- `db.py` - Database engine, session management, table creation

### SQLModel Standards

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
```

### Indexing Strategy

Create indexes on:
- Foreign keys (e.g., `user_id`) - always for JOIN performance
- Filter columns (e.g., `completed`) - commonly used in WHERE clauses
- Sort columns (e.g., `created_at`) - used in ORDER BY clauses

### Neon PostgreSQL

- Connection format: `postgresql://user:password@host/database?sslmode=require`
- Always use SSL mode for Neon connections
- Handle connection pooling for serverless

### Example Prompts

- "Set up the database schema for tasks"
- "Create the Tasks table with user_id, title, and timestamps"
- "Configure Neon PostgreSQL connection"
- "Add indexes for query performance"
- "Set up database session management"
