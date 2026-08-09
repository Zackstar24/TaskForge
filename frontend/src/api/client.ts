const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000";

const ACCESS_TOKEN_KEY = "taskforge_access_token";


export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}


export function setAccessToken(
  accessToken: string,
): void {
  localStorage.setItem(
    ACCESS_TOKEN_KEY,
    accessToken,
  );
}


export function clearAccessToken(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}


export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const headers = new Headers(options.headers);

  const accessToken = getAccessToken();

  if (accessToken) {
    headers.set(
      "Authorization",
      `Bearer ${accessToken}`,
    );
  }

  return fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers,
    },
  );
}