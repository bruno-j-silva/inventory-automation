export class ApiError extends Error {
  constructor(
    public status: number,
    public requestId?: string,
  ) {
    super("Não foi possível consultar o serviço.");
  }
}

export async function getReadiness(signal?: AbortSignal): Promise<boolean> {
  const response = await fetch("/api/health/ready", {
    credentials: "same-origin",
    signal,
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new ApiError(
      response.status,
      response.headers.get("X-Request-ID") ?? undefined,
    );
  }
  const body: unknown = await response.json();
  return (
    typeof body === "object" &&
    body !== null &&
    "status" in body &&
    body.status === "ready"
  );
}
