import type { Task } from "../types/task";


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