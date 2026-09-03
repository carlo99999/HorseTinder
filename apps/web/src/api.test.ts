import { describe, expect, it, vi } from "vitest";
import { API_BASE_PATH, getHealth } from "./api";

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
      headers: { Accept: "application/json" },
    });
  });
});
