import {
  apiFetch,
  clearAccessToken,
  setAccessToken,
} from "./client";

import type {
  LoginInput,
  RegisterInput,
  TokenResponse,
  User,
} from "../types/auth";


export async function registerUser(
  user: RegisterInput,
): Promise<User> {
  const response = await apiFetch(
    "/auth/register",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    },
  );

    if (response.status === 409) {
    throw new Error(
        "An account with this email already exists. Sign in instead.",
    );
    }

    if (!response.ok) {
    throw new Error(
        "Unable to create your account. Please try again.",
    );
    }

  return response.json() as Promise<User>;
}


export async function loginUser(
  credentials: LoginInput,
): Promise<TokenResponse> {
  const response = await apiFetch(
    "/auth/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    },
  );

    if (response.status === 401) {
    throw new Error(
        "Incorrect email or password.",
    );
    }

    if (!response.ok) {
    throw new Error(
        "Unable to sign in. Please try again.",
    );
    }

  const tokenData =
    await response.json() as TokenResponse;

  setAccessToken(tokenData.access_token);

  return tokenData;
}


export async function getCurrentUser(
  signal?: AbortSignal,
): Promise<User> {
  const response = await apiFetch(
    "/auth/me",
    {
      signal,
    },
  );

  if (!response.ok) {
    throw new Error(
      `Unable to load user. Server returned ${response.status}.`,
    );
  }

  return response.json() as Promise<User>;
}


export function logoutUser(): void {
  clearAccessToken();
}