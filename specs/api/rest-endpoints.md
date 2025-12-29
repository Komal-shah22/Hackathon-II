# REST API Endpoints Specification

## Base URL
- Development: http://localhost:8000
- Production: https://your-backend.railway.app

## Authentication
All endpoints require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### 1. GET /api/{user_id}/tasks
**Description:** List all tasks for a user
**Query Parameters:**
- `status` (optional): "all" | "pending" | "completed" (default: "all")

**Request:**
```http
GET /api/user123/tasks?status=pending
Authorization: Bearer eyJhbGc...
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T10:00:00Z"
  }
]
```

**Errors:**
- 401: Invalid/missing token
- 403: user_id doesn't match token

---

### 2. POST /api/{user_id}/tasks
**Description:** Create a new task

**Request:**
```http
POST /api/user123/tasks
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": "2024-12-01T10:00:00Z"
}
```

**Errors:**
- 400: Invalid input (missing title, too long)
- 401: Invalid/missing token
- 403: user_id doesn't match token

---

### 3. GET /api/{user_id}/tasks/{task_id}
**Description:** Get a specific task

**Request:**
```http
GET /api/user123/tasks/1
Authorization: Bearer eyJhbGc...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": "2024-12-01T10:00:00Z"
}
```

**Errors:**
- 401: Invalid/missing token
- 403: user_id doesn't match token or task owner
- 404: Task not found

---

### 4. PUT /api/{user_id}/tasks/{task_id}
**Description:** Update a task

**Request:**
```http
PUT /api/user123/tasks/1
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": false,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": "2024-12-01T11:00:00Z"
}
```

**Errors:**
- 400: Invalid input
- 401: Invalid/missing token
- 403: user_id doesn't match token or task owner
- 404: Task not found

---

### 5. DELETE /api/{user_id}/tasks/{task_id}
**Description:** Delete a task

**Request:**
```http
DELETE /api/user123/tasks/1
Authorization: Bearer eyJhbGc...
```

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Errors:**
- 401: Invalid/missing token
- 403: user_id doesn't match token or task owner
- 404: Task not found

---

### 6. PATCH /api/{user_id}/tasks/{task_id}/complete
**Description:** Toggle task completion status

**Request:**
```http
PATCH /api/user123/tasks/1/complete
Authorization: Bearer eyJhbGc...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": "2024-12-01T12:00:00Z"
}
```

**Errors:**
- 401: Invalid/missing token
- 403: user_id doesn't match token or task owner
- 404: Task not found

## Error Response Format
All errors follow this format:
```json
{
  "detail": "Error message here"
}
```

## Security Requirements
- JWT verification on EVERY endpoint
- User ID from token MUST match user_id in URL
- All database queries filtered by user_id
- Input validation on all requests
- SQL injection prevention (SQLModel handles this)
