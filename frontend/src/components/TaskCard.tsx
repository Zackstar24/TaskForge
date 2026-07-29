import { useState } from "react";

import {
  deleteTask,
  updateTask,
} from "../api/tasks";
import type { Task } from "../types/task";


interface TaskCardProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}


function formatCreatedAt(value: string): string {
  const date = new Date(value);

  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}


function TaskCard({
  task,
  onTaskUpdated,
  onTaskDeleted,
}: TaskCardProps) {
  const [pendingAction, setPendingAction] = useState<
    "toggle" | "delete" | null
  >(null);
  const [errorMessage, setErrorMessage] = useState<
    string | null
  >(null);

  const isBusy = pendingAction !== null;

  async function handleToggleCompleted(): Promise<void> {
    try {
      setPendingAction("toggle");
      setErrorMessage(null);

      const updatedTask = await updateTask(
        task.id,
        {
          completed: !task.completed,
        },
      );

      onTaskUpdated(updatedTask);
    } catch (error: unknown) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "An unexpected error occurred.",
      );
    } finally {
      setPendingAction(null);
    }
  }

  async function handleDelete(): Promise<void> {
    const confirmed = window.confirm(
      `Delete "${task.title}"? This action cannot be undone.`,
    );

    if (!confirmed) {
      return;
    }

    try {
      setPendingAction("delete");
      setErrorMessage(null);

      await deleteTask(task.id);

      onTaskDeleted(task.id);
    } catch (error: unknown) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "An unexpected error occurred.",
      );
    } finally {
      setPendingAction(null);
    }
  }

  return (
    <li
      className={
        task.completed
          ? "task-card task-card-completed"
          : "task-card"
      }
      aria-busy={isBusy}
    >
      <div className="task-card-header">
        <h2>{task.title}</h2>

        <span
          className={
            `priority priority-${task.priority}`
          }
        >
          {task.priority}
        </span>
      </div>

      {task.description && (
        <p className="task-description">
          {task.description}
        </p>
      )}

      <div className="task-card-footer">
        <div className="task-meta">
          <span
            className={
              task.completed
                ? "task-status task-status-complete"
                : "task-status"
            }
          >
            {task.completed
              ? "Completed"
              : "Open"}
          </span>

          <time dateTime={task.created_at}>
            Created {formatCreatedAt(task.created_at)}
          </time>
        </div>

        <div className="card-actions">
          <button
            className="card-action-button toggle-task-button"
            type="button"
            disabled={isBusy}
            onClick={() => {
              void handleToggleCompleted();
            }}
          >
            {pendingAction === "toggle"
              ? "Saving..."
              : task.completed
                ? "Reopen"
                : "Mark complete"}
          </button>

          <button
            className="card-action-button delete-task-button"
            type="button"
            disabled={isBusy}
            onClick={() => {
              void handleDelete();
            }}
          >
            {pendingAction === "delete"
              ? "Deleting..."
              : "Delete"}
          </button>
        </div>
      </div>

      {errorMessage && (
        <p
          className="task-action-error"
          role="alert"
        >
          {errorMessage}
        </p>
      )}
    </li>
  );
}

export default TaskCard;