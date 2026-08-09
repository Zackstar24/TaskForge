import {
  useEffect,
  useState,
} from "react";

import {
  getCurrentUser,
  logoutUser,
} from "./api/auth";
import { getAccessToken } from "./api/client";
import { getTasks } from "./api/tasks";
import AuthForm from "./components/AuthForm";
import TaskCard from "./components/TaskCard";
import TaskForm from "./components/TaskForm";
import type { User } from "./types/auth";
import type { Task } from "./types/task";

import "./App.css";


function App() {
  const [currentUser, setCurrentUser] =
    useState<User | null>(null);

  const [tasks, setTasks] =
    useState<Task[]>([]);

  const [
    isCheckingSession,
    setIsCheckingSession,
  ] = useState(true);

  const [isLoading, setIsLoading] =
    useState(false);

  const [
    errorMessage,
    setErrorMessage,
  ] = useState<string | null>(null);


  function handleTaskCreated(
    task: Task,
  ): void {
    setTasks((currentTasks) => [
      ...currentTasks,
      task,
    ]);
  }


  function handleTaskUpdated(
    updatedTask: Task,
  ): void {
    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === updatedTask.id
          ? updatedTask
          : task,
      ),
    );
  }


  function handleTaskDeleted(
    taskId: number,
  ): void {
    setTasks((currentTasks) =>
      currentTasks.filter(
        (task) => task.id !== taskId,
      ),
    );
  }


  function handleAuthenticated(
    user: User,
  ): void {
    setCurrentUser(user);
    setErrorMessage(null);
  }


  function handleLogout(): void {
    logoutUser();

    setCurrentUser(null);
    setTasks([]);
    setErrorMessage(null);
  }


  useEffect(() => {
    const controller =
      new AbortController();

    async function restoreSession():
      Promise<void> {
      const accessToken =
        getAccessToken();

      if (!accessToken) {
        setIsCheckingSession(false);
        return;
      }

      try {
        const user =
          await getCurrentUser(
            controller.signal,
          );

        setCurrentUser(user);
      } catch (error: unknown) {
        if (
          error instanceof DOMException
          && error.name === "AbortError"
        ) {
          return;
        }

        logoutUser();
        setCurrentUser(null);
      } finally {
        if (!controller.signal.aborted) {
          setIsCheckingSession(false);
        }
      }
    }

    void restoreSession();

    return () => {
      controller.abort();
    };
  }, []);


  useEffect(() => {
    if (!currentUser) {
      return;
    }

    const controller =
      new AbortController();

    async function loadTasks():
      Promise<void> {
      try {
        setIsLoading(true);
        setErrorMessage(null);

        const taskData =
          await getTasks(
            controller.signal,
          );

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
  }, [currentUser]);


  if (isCheckingSession) {
    return (
      <main className="app-shell">
        <section className="task-panel">
          <p className="status-message">
            Restoring your session...
          </p>
        </section>
      </main>
    );
  }


  if (!currentUser) {
    return (
      <AuthForm
        onAuthenticated={
          handleAuthenticated
        }
      />
    );
  }


  return (
    <main className="app-shell">
      <section className="task-panel">
        <header className="app-header">
          <div>
            <p className="eyebrow">
              TASKFORGE
            </p>

            <h1>My Tasks</h1>

            <p className="subtitle">
              Plan the work. Complete the work.
            </p>
          </div>

          <div className="header-actions">
            {!isLoading
              && !errorMessage && (
                <span className="task-count">
                  {tasks.length}{" "}
                  {tasks.length === 1
                    ? "task"
                    : "tasks"}
                </span>
              )}

            <div className="user-menu">
              <span className="user-email">
                {currentUser.email}
              </span>

              <button
                className="logout-button"
                type="button"
                onClick={handleLogout}
              >
                Log out
              </button>
            </div>
          </div>
        </header>

        <TaskForm
          onTaskCreated={
            handleTaskCreated
          }
        />

        <div aria-live="polite">
          {isLoading && (
            <p className="status-message">
              Loading tasks...
            </p>
          )}

          {!isLoading
            && errorMessage && (
              <div
                className={
                  "status-message "
                  + "error-message"
                }
                role="alert"
              >
                <strong>
                  Tasks could not be loaded.
                </strong>

                <p>{errorMessage}</p>

                <p>
                  Make sure the FastAPI
                  server is running on
                  port 8000.
                </p>
              </div>
            )}

          {!isLoading
            && !errorMessage
            && tasks.length === 0 && (
              <p className="status-message">
                No tasks yet. Your first
                task will appear here.
              </p>
            )}

          {!isLoading
            && !errorMessage
            && tasks.length > 0 && (
              <ul className="task-list">
                {tasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onTaskUpdated={
                      handleTaskUpdated
                    }
                    onTaskDeleted={
                      handleTaskDeleted
                    }
                  />
                ))}
              </ul>
            )}
        </div>
      </section>
    </main>
  );
}


export default App;