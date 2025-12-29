// Enums matching backend
export type TaskPriority = 'high' | 'medium' | 'low' | null;
export type TaskCategory = 'work' | 'personal' | 'shopping' | 'health' | 'finance' | 'other' | null;
export type RecurrencePattern = 'daily' | 'weekly' | 'monthly' | null;

// User types
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
  updated_at?: string | null;
}

export interface UserResponse {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface AuthResponse {
  user: UserResponse;
  token: string;
}

export interface UserCreate {
  email: string;
  password: string;
  name?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

// Task types
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  // Intermediate fields
  priority: TaskPriority;
  category: TaskCategory;
  // Advanced fields
  due_date: string | null;
  reminder_time: string | null;
  reminder_sent: boolean;
  is_recurring: boolean;
  recurrence_pattern: RecurrencePattern;
  recurrence_interval: number | null;
  recurrence_days: string | null;
  recurrence_end_date: string | null;
  parent_task_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: TaskPriority;
  category?: TaskCategory;
  due_date?: string;
  reminder_time?: string;
  is_recurring?: boolean;
  recurrence_pattern?: RecurrencePattern;
  recurrence_interval?: number;
  recurrence_days?: string;
  recurrence_end_date?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  category?: TaskCategory;
  due_date?: string;
  reminder_time?: string;
  is_recurring?: boolean;
  recurrence_pattern?: RecurrencePattern;
  recurrence_interval?: number;
  recurrence_days?: string;
  recurrence_end_date?: string;
  completed?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface MessageResponse {
  message: string;
}

// Stats types
export interface UserStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  completion_rate: number;
  overdue_count: number;
  due_today_count: number;
  by_category: Record<string, number>;
  by_priority: Record<string, number>;
}

// Filter/Sort types
export interface TaskFilters {
  status: 'all' | 'pending' | 'completed';
  priority: 'all' | 'high' | 'medium' | 'low' | 'none';
  category: string;
  search: string;
  sort_by: 'created_at' | 'due_date' | 'priority' | 'title';
  sort_order: 'asc' | 'desc';
}
