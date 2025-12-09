# Data Model: Task

**Source**: `specs/001-advanced-task-management/spec.md`

## Task Entity

A single to-do item.

### Attributes

| Name | Type | Description | Constraints |
|---|---|---|---|
| `id` | string (UUID) | A unique identifier for the task. | Mandatory, generated automatically. |
| `title` | string | The name of the task. | Mandatory, non-empty. |
| `description`| string | A more detailed description of the task. | Optional. |
| `status` | string | The current status of the task. | 'pending' or 'complete'. Default is 'pending'. |
| `priority` | string | The priority level of the task. | 'High', 'Medium', 'Low', 'None'. Default is 'None'. |
| `tags` | list of strings | A list of categories associated with the task. | Optional, free-form text. |
| `due_date`| string | The date the task is due. | Optional, ISO 8601 format (YYYY-MM-DD). |

### State Transitions

- A task is created with a `status` of 'pending'.
- A task can be marked as 'complete', changing its `status` to 'complete'.
- A completed task can be marked as 'pending' again.
