import { apiFetch } from "./client";

import type {
  CreateTaskInput,
  Task,
  UpdateTaskInput,
} from "../types/task";


export async function getTasks(
  signal?: AbortSignal,
): Promise<Task[]> {
  const response = await apiFetch(
    "/tasks",
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
  const response = await apiFetch(
    "/tasks",
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
  const response = await apiFetch(
    `/tasks/${taskId}`,
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
  const response = await apiFetch(
    `/tasks/${taskId}`,
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