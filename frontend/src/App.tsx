import { useEffect, useState } from "react";

import { getTasks } from "./api/tasks";
import type { Task } from "./types/task";

import "./App.css";


function formatCreatedAt(value: string): string {
  const date = new Date(value);

  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}


function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(
    null,
  );

  useEffect(() => {
    const controller = new AbortController();

    async function loadTasks(): Promise<void> {
      try {
        setIsLoading(true);
        setErrorMessage(null);

        const taskData = await getTasks(controller.signal);

        setTasks(taskData);
      } catch (error: unknown) {
        if (
          error instanceof DOMException
          && error.name === "AbortError"
        ) {
          return;
        }

        setErrorMessage(
          error instanceof Error
            ? error.message
            : "An unexpected error occurred.",
        );
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    }

    void loadTasks();

    return () => {
      controller.abort();
    };
  }, []);

  return (
    <main className="app-shell">
      <section className="task-panel">
        <header className="app-header">
          <div>
            <p className="eyebrow">TASKFORGE</p>
            <h1>My Tasks</h1>
            <p className="subtitle">
              Your first React and FastAPI connection.
            </p>
          </div>

          {!isLoading && !errorMessage && (
            <span className="task-count">
              {tasks.length} {tasks.length === 1 ? "task" : "tasks"}
            </span>
          )}
        </header>

        <div aria-live="polite">
          {isLoading && (
            <p className="status-message">
              Loading tasks...
            </p>
          )}

          {!isLoading && errorMessage && (
            <div
              className="status-message error-message"
              role="alert"
            >
              <strong>Tasks could not be loaded.</strong>
              <p>{errorMessage}</p>
              <p>
                Make sure the FastAPI server is running on port
                8000.
              </p>
            </div>
          )}

          {!isLoading
            && !errorMessage
            && tasks.length === 0 && (
              <p className="status-message">
                No tasks yet. Your first task will appear here.
              </p>
            )}

          {!isLoading
            && !errorMessage
            && tasks.length > 0 && (
              <ul className="task-list">
                {tasks.map((task) => (
                  <li
                    className="task-card"
                    key={task.id}
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
                  </li>
                ))}
              </ul>
            )}
        </div>
      </section>
    </main>
  );
}

export default App;