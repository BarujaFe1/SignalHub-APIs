import type {
  SourceWithFreshness,
  SourceDetail,
  Run,
  FreshnessStatus,
  QualityCheck,
  NormalizedSignal,
  MetricsSummary,
  PaginatedResponse,
  QualitySummary,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const TRIGGER_API_KEY = process.env.NEXT_PUBLIC_TRIGGER_API_KEY || "";

async function fetchAPI<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  health: () => fetchAPI<{ status: string; database: string; scheduler: string }>("/health"),
  sources: () => fetchAPI<SourceWithFreshness[]>("/api/v1/sources"),
  sourceDetail: (slug: string) => fetchAPI<SourceDetail>(`/api/v1/sources/${slug}`),
  runs: (params?: { source?: string; status?: string; limit?: number; offset?: number }) => {
    const search = new URLSearchParams();
    if (params?.source) search.set("source", params.source);
    if (params?.status) search.set("status", params.status);
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset) search.set("offset", String(params.offset));
    const qs = search.toString();
    return fetchAPI<PaginatedResponse<Run>>(`/api/v1/runs${qs ? `?${qs}` : ""}`);
  },
  freshness: () => fetchAPI<FreshnessStatus[]>("/api/v1/freshness"),
  quality: (params?: { source?: string; status?: string; limit?: number }) => {
    const search = new URLSearchParams();
    if (params?.source) search.set("source", params.source);
    if (params?.status) search.set("status", params.status);
    if (params?.limit) search.set("limit", String(params.limit));
    const qs = search.toString();
    return fetchAPI<{ items: QualityCheck[]; summary: QualitySummary }>(`/api/v1/quality${qs ? `?${qs}` : ""}`);
  },
  signals: (params?: { source?: string; limit?: number }) => {
    const search = new URLSearchParams();
    if (params?.source) search.set("source", params.source);
    if (params?.limit) search.set("limit", String(params.limit));
    const qs = search.toString();
    return fetchAPI<PaginatedResponse<NormalizedSignal>>(`/api/v1/signals${qs ? `?${qs}` : ""}`);
  },
  metrics: () => fetchAPI<MetricsSummary>("/api/v1/metrics/summary"),
  triggerRun: async (slug: string) => {
    const headers: HeadersInit = { "Content-Type": "application/json" };
    if (TRIGGER_API_KEY) {
      headers["X-API-Key"] = TRIGGER_API_KEY;
    }
    const res = await fetch(`${API_BASE}/api/v1/runs/trigger/${slug}`, {
      method: "POST",
      headers,
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(body.detail || `Trigger failed: ${res.status}`);
    }
    return body as { run_id: string; source_slug: string; status: string; message: string };
  },
};
