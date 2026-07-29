export type TaskPriority = "low" | "medium" | "high";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  priority: TaskPriority;
  completed: boolean;
  created_at: string;
}

export interface CreateTaskInput {
  title: string;
  description: string | null;
  priority: TaskPriority;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string | null;
  priority?: TaskPriority;
  completed?: boolean;
}