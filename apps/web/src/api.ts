export const API_BASE_PATH = "/api/v1";
export type HealthDto = { data: { service: string; version: string } };

export async function getHealth(): Promise<HealthDto> {
  const response = await fetch(`${API_BASE_PATH}/health`, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error("The API health check failed.");
  return (await response.json()) as HealthDto;
}
