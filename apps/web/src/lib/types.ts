// ─── SignalHub API Types ──────────────────────────────────

export type RunStatus = "running" | "success" | "failed" | "partial";
export type CheckStatus = "pass" | "warn" | "fail";
export type Severity = "info" | "warning" | "error";

export interface Source {
  id: string;
  slug: string;
  name: string;
  description: string;
  api_base_url: string;
  schedule_interval_minutes: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SourceWithFreshness extends Source {
  freshness: FreshnessStatus | null;
  last_run_status: RunStatus | null;
  total_signals: number;
  total_runs: number;
}

export interface Run {
  id: string;
  source_id: string;
  source_slug: string;
  source_name: string;
  status: RunStatus;
  started_at: string;
  finished_at: string | null;
  duration_ms: number | null;
  records_fetched: number;
  records_stored: number;
  error_message: string | null;
  created_at: string;
}

export interface FreshnessStatus {
  source_slug: string;
  source_name: string;
  last_success_at: string | null;
  last_attempt_at: string | null;
  is_stale: boolean;
  staleness_minutes: number;
}

export interface QualityCheck {
  id: string;
  run_id: string;
  source_slug: string;
  source_name: string;
  check_name: string;
  check_status: CheckStatus;
  expected_value: string;
  actual_value: string;
  message: string;
  checked_at: string;
}

export interface NormalizedSignal {
  id: string;
  source_slug: string;
  signal_type: string;
  signal_key: string;
  signal_value: number;
  signal_unit: string;
  observed_at: string;
  metadata: Record<string, unknown>;
}

export interface MetricsSummary {
  total_sources: number;
  active_sources: number;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  total_signals: number;
  total_quality_checks: number;
  quality_pass_rate: number;
  sources_stale: number;
  last_activity_at: string | null;
}

export interface QualitySummary {
  total: number;
  passed: number;
  warnings: number;
  failures: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface SourceDetail {
  source: SourceWithFreshness;
  recent_runs: Run[];
  recent_signals: NormalizedSignal[];
  recent_checks: QualityCheck[];
  quality_summary: QualitySummary;
}
