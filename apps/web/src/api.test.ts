import { describe, expect, it, vi } from "vitest";
import { API_BASE_PATH, getAnonymousCsrf, getHealth, register } from "./api";
import config from "../vite.config";

describe("API client", () => {
  it("uses only the same-origin versioned base path", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ data: { service: "horse-tinder-api", version: "v1" } }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await getHealth();

    expect(API_BASE_PATH).toBe("/api/v1");
    expect(fetchMock).toHaveBeenCalledWith("/api/v1/health", {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
  });

  it("uses credentialed, CSRF-protected auth requests", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ data: { csrfToken: "anonymous-token" } }),
    });
    vi.stubGlobal("fetch", fetchMock);
    await getAnonymousCsrf();
    expect(fetchMock).toHaveBeenCalledWith("/api/v1/auth/csrf", {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });

    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: { authenticated: true, csrfToken: "session-token" } }),
    });
    await register("rider@example.test", "a safe horse password", "anonymous-token");
    expect(fetchMock).toHaveBeenLastCalledWith("/api/v1/auth/register", {
      method: "POST",
      credentials: "same-origin",
      headers: { Accept: "application/json", "Content-Type": "application/json", "X-CSRF-Token": "anonymous-token" },
      body: JSON.stringify({ email: "rider@example.test", password: "a safe horse password" }),
    });
  });

  it("proxies the versioned API path during local development", () => {
    expect(config.server?.proxy?.[API_BASE_PATH]).toMatchObject({ target: "http://api:8000" });
  });
});
