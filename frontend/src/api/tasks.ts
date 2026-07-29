import type {
  CreateTaskInput,
  Task,
  UpdateTaskInput,
} from "../types/task";


const API_BASE_URL = "http://127.0.0.1:8000";


export async function getTasks(
  signal?: AbortSignal,
): Promise<Task[]> {
  const response = await fetch(
    `${API_BASE_URL}/tasks`,
    {
      signal,
    },
  );

  if (!response.ok) {
    throw new Error(
      `Unable to load tasks. Server returned ${response.status}.`,
    );
  }

  return response.json() as Promise<Task[]>;
}


export async function createTask(
  task: CreateTaskInput,
): Promise<Task> {
  const response = await fetch(
    `${API_BASE_URL}/tasks`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(task),
    },
  );

  if (!response.ok) {
    throw new Error(
      `Unable to create task. Server returned ${response.status}.`,
    );
  }

  return response.json() as Promise<Task>;
}


export async function updateTask(
  taskId: number,
  updates: UpdateTaskInput,
): Promise<Task> {
  const response = await fetch(
    `${API_BASE_URL}/tasks/${taskId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updates),
    },
  );

  if (!response.ok) {
    throw new Error(
      `Unable to update task. Server returned ${response.status}.`,
    );
  }

  return response.json() as Promise<Task>;
}


export async function deleteTask(
  taskId: number,
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/tasks/${taskId}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Unable to delete task. Server returned ${response.status}.`,
    );
  }
}