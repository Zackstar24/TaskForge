import { useState } from "react";

import {
  getCurrentUser,
  loginUser,
  registerUser,
} from "../api/auth";
import type { User } from "../types/auth";


type AuthMode = "login" | "register";

interface AuthFormProps {
  onAuthenticated: (user: User) => void;
}


function AuthForm({
  onAuthenticated,
}: AuthFormProps) {
  const [mode, setMode] =
    useState<AuthMode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] =
    useState(false);
  const [errorMessage, setErrorMessage] =
    useState<string | null>(null);

  const isRegistering = mode === "register";

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    try {
      setIsSubmitting(true);
      setErrorMessage(null);

      if (isRegistering) {
        await registerUser({
          email,
          password,
        });
      }

      await loginUser({
        email,
        password,
      });

      const user = await getCurrentUser();

      onAuthenticated(user);
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

  function switchMode(): void {
    setMode((currentMode) =>
      currentMode === "login"
        ? "register"
        : "login",
    );

    setPassword("");
    setErrorMessage(null);
  }

  return (
    <main className="app-shell">
      <section className="task-panel auth-panel">
        <header className="auth-header">
          <p className="eyebrow">
            TASKFORGE
          </p>

          <h1>
            {isRegistering
              ? "Create your account"
              : "Welcome back"}
          </h1>

          <p className="subtitle">
            {isRegistering
              ? "Create an account to start organizing your work."
              : "Sign in to access your tasks."}
          </p>
        </header>

        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >
          <div className="form-field">
            <label htmlFor="auth-email">
              Email
            </label>

            <input
              id="auth-email"
              type="email"
              value={email}
              autoComplete="email"
              required
              disabled={isSubmitting}
              onChange={(event) =>
                setEmail(event.target.value)
              }
            />
          </div>

          <div className="form-field">
            <label htmlFor="auth-password">
              Password
            </label>

            <input
              id="auth-password"
              type="password"
              value={password}
              autoComplete={
                isRegistering
                  ? "new-password"
                  : "current-password"
              }
              minLength={
                isRegistering ? 8 : 1
              }
              required
              disabled={isSubmitting}
              onChange={(event) =>
                setPassword(event.target.value)
              }
            />

            {isRegistering && (
              <span className="field-help">
                Use at least 8 characters.
              </span>
            )}
          </div>

          {errorMessage && (
            <p
              className="form-error"
              role="alert"
            >
              {errorMessage}
            </p>
          )}

          <button
            className="auth-submit-button"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Please wait..."
              : isRegistering
                ? "Create account"
                : "Sign in"}
          </button>
        </form>

        <div className="auth-switch">
          <span>
            {isRegistering
              ? "Already have an account?"
              : "New to TaskForge?"}
          </span>

          <button
            type="button"
            onClick={switchMode}
            disabled={isSubmitting}
          >
            {isRegistering
              ? "Sign in"
              : "Create an account"}
          </button>
        </div>
      </section>
    </main>
  );
}


export default AuthForm;