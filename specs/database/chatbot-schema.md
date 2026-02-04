# Database Schema for AI Chatbot

## Updated Tables (Extending Phase II Schema)

### users (managed by Better Auth)
- id: string (primary key)
- email: string (unique)
- name: string
- created_at: timestamp

### tasks (from Phase II)
- id: integer (primary key)
- user_id: string (foreign key -> users.id)
- title: string (not null)
- description: text (nullable)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

## New Tables for Chatbot

### conversations
- id: integer (primary key)
- user_id: string (foreign key -> users.id)
- created_at: timestamp
- updated_at: timestamp

### messages
- id: integer (primary key)
- conversation_id: integer (foreign key -> conversations.id)
- user_id: string (foreign key -> users.id)
- role: string (enum: 'user', 'assistant')
- content: text (not null)
- created_at: timestamp

## Indexes
- tasks.user_id (for filtering by user)
- tasks.completed (for status filtering)
- conversations.user_id (for filtering by user)
- messages.conversation_id (for retrieving conversation history)
- messages.created_at (for chronological ordering)