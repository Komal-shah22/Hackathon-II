---
description: Build Next.js 16 frontend components, pages, layouts, and UI features for the todo application.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Frontend Generator

This skill invokes the **frontend-generator** agent to build Next.js 16 frontend code for the todo application.

### When to Use

- Creating new pages with App Router patterns
- Building reusable UI components
- Implementing layouts and navigation
- Setting up protected routes with authentication guards
- Integrating API calls with the backend
- Adding form handling and validation
- Implementing loading and error states

### Execution

**Invoke the frontend-generator agent** with the user's request to:

1. Read existing UI specifications from `specs/ui/` if available
2. Check existing components for reusability patterns
3. Generate properly typed TypeScript components
4. Use Server Components by default, Client Components only when needed
5. Apply Tailwind CSS styling with responsive design
6. Implement authentication integration where required

### Output Expectations

The agent will:
- Create/modify files in `app/`, `components/`, or `lib/` directories
- Use proper TypeScript typing throughout
- Follow Next.js 16 App Router conventions
- Include loading and error handling states
- Integrate with Better Auth for protected routes
- Provide clear explanations of architectural decisions

### Example Prompts

- "Create a todo list page that displays all tasks"
- "Build a reusable todo card component with edit/delete buttons"
- "Set up the dashboard layout with navigation"
- "Add a form for creating new todos"
- "Implement the protected routes wrapper"
