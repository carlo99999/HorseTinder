export const API_BASE_PATH = "/api/v1";
export type HealthDto = { data: { service: string; version: string } };
export type ApiFailure = { code: string; message: string; details?: Record<string, unknown> };
export type CsrfDto = { data: { csrfToken: string } };
export type AuthDto = { data: { authenticated: true; csrfToken: string } };
export type SessionDto = { data: { authenticated: true; csrfToken: string } };

export class ApiError extends Error {
  constructor(public readonly failure: ApiFailure, public readonly status: number) {
    super(failure.message);
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_PATH}${path}`, {
    credentials: "same-origin",
    ...init,
    headers: { Accept: "application/json", ...init.headers },
  });
  if (!response.ok) {
    throw new ApiError((await response.json()) as ApiFailure, response.status);
  }
  return (await response.json()) as T;
}

export async function getHealth(): Promise<HealthDto> {
  return request<HealthDto>("/health");
}

export function getAnonymousCsrf(): Promise<CsrfDto> {
  return request<CsrfDto>("/auth/csrf");
}

export function register(email: string, password: string, csrfToken: string): Promise<AuthDto> {
  return request<AuthDto>("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken },
    body: JSON.stringify({ email, password }),
  });
}

export function signIn(email: string, password: string, csrfToken: string): Promise<AuthDto> {
  return request<AuthDto>("/auth/sign-in", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken },
    body: JSON.stringify({ email, password }),
  });
}

export function getSession(): Promise<SessionDto> {
  return request<SessionDto>("/auth/session");
}

export async function signOut(csrfToken: string): Promise<void> {
  const response = await fetch(`${API_BASE_PATH}/auth/sign-out`, {
    method: "POST",
    credentials: "same-origin",
    headers: { Accept: "application/json", "X-CSRF-Token": csrfToken },
  });
  if (!response.ok) throw new ApiError((await response.json()) as ApiFailure, response.status);
}
