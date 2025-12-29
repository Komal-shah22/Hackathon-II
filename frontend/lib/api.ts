const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface FetchOptions {
  method?: string;
  body?: object;
  headers?: Record<string, string>;
  retries?: number;
  retryDelay?: number;
}

interface ApiError extends Error {
  status?: number;
  code?: string;
}

class ApiClient {
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private async fetch<T>(
    endpoint: string,
    options: FetchOptions = {}
  ): Promise<T> {
    const {
      retries = 2,
      retryDelay = 1000,
    } = options;

    const token = this.getToken();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const response = await fetch(`${API_URL}${endpoint}`, {
          method: options.method || 'GET',
          headers,
          body: options.body ? JSON.stringify(options.body) : undefined,
        });

        if (!response.ok) {
          // Handle 401 Unauthorized - clear token and redirect to login
          if (response.status === 401) {
            if (typeof window !== 'undefined') {
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              window.location.href = '/signin';
            }
            throw new Error('Session expired. Please sign in again.');
          }

          // Handle rate limiting
          if (response.status === 429) {
            const retryAfter = response.headers.get('Retry-After');
            const waitTime = retryAfter ? parseInt(retryAfter) * 1000 : retryDelay;
            if (attempt < retries) {
              await this.sleep(waitTime);
              continue;
            }
          }

          const error = await response.json().catch(() => ({ detail: 'Request failed' }));
          const apiError: ApiError = new Error(error.detail || 'Request failed');
          apiError.status = response.status;
          throw apiError;
        }

        return response.json();
      } catch (err) {
        lastError = err instanceof Error ? err : new Error('Unknown error');

        // Don't retry on client errors (4xx)
        if (lastError instanceof Error) {
          const apiError = lastError as ApiError;
          if (typeof apiError.status === 'number' && apiError.status >= 400 && apiError.status < 500) {
            throw lastError;
          }
        }

        // Retry on server errors or network issues
        if (attempt < retries) {
          await this.sleep(retryDelay * (attempt + 1)); // Exponential backoff
          continue;
        }

        throw lastError;
      }
    }

    throw lastError;
  }

  // ============ Auth API ============

  async signup(email: string, password: string, name?: string) {
    return this.fetch<{ user: import('./types').UserResponse; token: string }>(
      '/auth/signup',
      {
        method: 'POST',
        body: { email, password, name },
        retries: 0, // Don't retry auth requests
      }
    );
  }

  async signin(email: string, password: string) {
    return this.fetch<{ user: import('./types').UserResponse; token: string }>(
      '/auth/signin',
      {
        method: 'POST',
        body: { email, password },
        retries: 0, // Don't retry auth requests
      }
    );
  }

  async getMe() {
    return this.fetch<import('./types').UserResponse>('/auth/me', {
      retries: 1,
    });
  }

  async logout() {
    return this.fetch<import('./types').MessageResponse>('/auth/logout', {
      method: 'POST',
      retries: 0,
    });
  }

  // ============ Tasks API ============

  async getTasks(
    userId: string,
    params?: {
      status?: string;
      priority?: string;
      category?: string;
      search?: string;
      sort_by?: string;
      sort_order?: string;
    }
  ) {
    const searchParams = new URLSearchParams();
    if (params?.status && params.status !== 'all') {
      searchParams.set('status', params.status);
    }
    if (params?.priority && params.priority !== 'all') {
      searchParams.set('priority', params.priority);
    }
    if (params?.category && params.category !== 'all') {
      searchParams.set('category', params.category);
    }
    if (params?.search) {
      searchParams.set('search', params.search);
    }
    if (params?.sort_by) {
      searchParams.set('sort_by', params.sort_by);
    }
    if (params?.sort_order) {
      searchParams.set('sort_order', params.sort_order);
    }

    const query = searchParams.toString() ? `?${searchParams.toString()}` : '';
    return this.fetch<import('./types').TaskListResponse>(
      `/api/${userId}/tasks${query}`,
      { retries: 2 }
    );
  }

  async getTask(userId: string, taskId: number) {
    return this.fetch<import('./types').Task>(
      `/api/${userId}/tasks/${taskId}`,
      { retries: 2 }
    );
  }

  async createTask(userId: string, data: import('./types').TaskCreate) {
    return this.fetch<import('./types').Task>(
      `/api/${userId}/tasks`,
      { method: 'POST', body: data, retries: 1 }
    );
  }

  async updateTask(
    userId: string,
    taskId: number,
    data: import('./types').TaskUpdate
  ) {
    return this.fetch<import('./types').Task>(
      `/api/${userId}/tasks/${taskId}`,
      { method: 'PUT', body: data, retries: 1 }
    );
  }

  async deleteTask(userId: string, taskId: number) {
    return this.fetch<import('./types').MessageResponse>(
      `/api/${userId}/tasks/${taskId}`,
      { method: 'DELETE', retries: 0 }
    );
  }

  async toggleComplete(userId: string, taskId: number, completed: boolean = true) {
    return this.fetch<import('./types').Task>(
      `/api/${userId}/tasks/${taskId}/complete?completed=${completed}`,
      { method: 'PATCH', retries: 1 }
    );
  }

  // ============ Stats API ============

  async getUserStats(userId: string) {
    return this.fetch<import('./types').UserStats>(
      `/api/${userId}/stats`,
      { retries: 2 }
    );
  }
}

export const api = new ApiClient();
