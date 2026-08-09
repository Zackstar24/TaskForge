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

  if (!response.ok) {
    throw new Error(
      `Unable to register. Server returned ${response.status}.`,
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

  if (!response.ok) {
    throw new Error(
      `Unable to log in. Server returned ${response.status}.`,
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