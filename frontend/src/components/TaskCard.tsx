import {
  useState,
  type FormEvent,
} from "react";

import {
  deleteTask,
  updateTask,
} from "../api/tasks";
import type {
  Task,
  TaskPriority,
} from "../types/task";


interface TaskCardProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}


type PendingAction =
  | "toggle"
  | "delete"
  | "edit"
  | null;


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
  const [pendingAction, setPendingAction] =
    useState<PendingAction>(null);
  const [errorMessage, setErrorMessage] =
    useState<string | null>(null);

  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(
    task.description ?? "",
  );
  const [editPriority, setEditPriority] =
    useState<TaskPriority>(task.priority);

  const isBusy = pendingAction !== null;

  function handleStartEdit(): void {
    setEditTitle(task.title);
    setEditDescription(task.description ?? "");
    setEditPriority(task.priority);
    setErrorMessage(null);
    setIsEditing(true);
  }

  function handleCancelEdit(): void {
    setErrorMessage(null);
    setIsEditing(false);
  }

  async function handleSaveEdit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const trimmedTitle = editTitle.trim();
    const trimmedDescription = editDescription.trim();

    if (!trimmedTitle) {
      setErrorMessage("Enter a task title.");
      return;
    }

    try {
      setPendingAction("edit");
      setErrorMessage(null);

      const updatedTask = await updateTask(
        task.id,
        {
          title: trimmedTitle,
          description: trimmedDescription || null,
          priority: editPriority,
        },
      );

      onTaskUpdated(updatedTask);
      setIsEditing(false);
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
      {isEditing ? (
        <form
          className="task-edit-form"
          onSubmit={(event) => {
            void handleSaveEdit(event);
          }}
        >
          <div className="form-field task-edit-wide">
            <label htmlFor={`edit-title-${task.id}`}>
              Title
            </label>

            <input
              id={`edit-title-${task.id}`}
              type="text"
              value={editTitle}
              maxLength={200}
              disabled={isBusy}
              onChange={(event) => {
                setEditTitle(event.target.value);
              }}
            />
          </div>

          <div className="form-field task-edit-wide">
            <label htmlFor={`edit-description-${task.id}`}>
              Description
            </label>

            <textarea
              id={`edit-description-${task.id}`}
              value={editDescription}
              rows={3}
              disabled={isBusy}
              onChange={(event) => {
                setEditDescription(event.target.value);
              }}
            />
          </div>

          <div className="form-field">
            <label htmlFor={`edit-priority-${task.id}`}>
              Priority
            </label>

            <select
              id={`edit-priority-${task.id}`}
              value={editPriority}
              disabled={isBusy}
              onChange={(event) => {
                setEditPriority(
                  event.target.value as TaskPriority,
                );
              }}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div className="card-actions task-edit-actions">
            <button
              className="card-action-button save-task-button"
              type="submit"
              disabled={isBusy}
            >
              {pendingAction === "edit"
                ? "Saving..."
                : "Save changes"}
            </button>

            <button
              className="card-action-button"
              type="button"
              disabled={isBusy}
              onClick={handleCancelEdit}
            >
              Cancel
            </button>
          </div>

          {errorMessage && (
            <p
              className="task-action-error task-edit-wide"
              role="alert"
            >
              {errorMessage}
            </p>
          )}
        </form>
      ) : (
        <>
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
                className="card-action-button edit-task-button"
                type="button"
                disabled={isBusy}
                onClick={handleStartEdit}
              >
                Edit
              </button>

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
        </>
      )}
    </li>
  );
}

export default TaskCard;
