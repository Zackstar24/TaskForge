import {
  useState,
  type FormEvent,
} from "react";

import { createTask } from "../api/tasks";
import type {
  Task,
  TaskPriority,
} from "../types/task";


interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
}


function TaskForm({
  onTaskCreated,
}: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] =
    useState<TaskPriority>("medium");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] =
    useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const trimmedTitle = title.trim();
    const trimmedDescription = description.trim();

    if (!trimmedTitle) {
      setErrorMessage("Enter a task title.");
      return;
    }

    try {
      setIsSubmitting(true);
      setErrorMessage(null);

      const createdTask = await createTask({
        title: trimmedTitle,
        description: trimmedDescription || null,
        priority,
      });

      onTaskCreated(createdTask);

      setTitle("");
      setDescription("");
      setPriority("medium");
    } catch (error: unknown) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "An unexpected error occurred.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="task-form-section">
      <div className="section-heading">
        <div>
          <p className="section-label">NEW TASK</p>
          <h2>Add something to your list</h2>
        </div>
      </div>

      <form
        className="task-form"
        onSubmit={(event) => {
          void handleSubmit(event);
        }}
      >
        <div className="form-field form-field-wide">
          <label htmlFor="task-title">
            Title
          </label>

          <input
            id="task-title"
            name="title"
            type="text"
            value={title}
            maxLength={200}
            placeholder="What needs to be done?"
            disabled={isSubmitting}
            onChange={(event) => {
              setTitle(event.target.value);
            }}
          />
        </div>

        <div className="form-field form-field-wide">
          <label htmlFor="task-description">
            Description
            <span className="optional-label">
              Optional
            </span>
          </label>

          <textarea
            id="task-description"
            name="description"
            value={description}
            rows={3}
            placeholder="Add any useful details"
            disabled={isSubmitting}
            onChange={(event) => {
              setDescription(event.target.value);
            }}
          />
        </div>

        <div className="form-field">
          <label htmlFor="task-priority">
            Priority
          </label>

          <select
            id="task-priority"
            name="priority"
            value={priority}
            disabled={isSubmitting}
            onChange={(event) => {
              setPriority(
                event.target.value as TaskPriority,
              );
            }}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Adding task..."
              : "Add task"}
          </button>
        </div>

        {errorMessage && (
          <p
            className="form-error"
            role="alert"
          >
            {errorMessage}
          </p>
        )}
      </form>
    </section>
  );
}

export default TaskForm;