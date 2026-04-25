import type {
  SourceWithFreshness,
  Run,
  FreshnessStatus,
  QualityCheck,
  NormalizedSignal,
  MetricsSummary,
  QualitySummary,
} from "./types";

// ─── Mock Sources ─────────────────────────────────────────

export const mockSources: SourceWithFreshness[] = [
  {
    id: "s1-open-meteo",
    slug: "open-meteo",
    name: "Open-Meteo Weather",
    description: "Current weather conditions for Berlin — temperature, humidity, and wind speed.",
    api_base_url: "https://api.open-meteo.com",
    schedule_interval_minutes: 30,
    is_active: true,
    created_at: "2024-01-10T08:00:00Z",
    updated_at: "2024-01-15T10:30:00Z",
    freshness: {
      source_slug: "open-meteo",
      source_name: "Open-Meteo Weather",
      last_success_at: new Date(Date.now() - 12 * 60000).toISOString(),
      last_attempt_at: new Date(Date.now() - 12 * 60000).toISOString(),
      is_stale: false,
      staleness_minutes: 12,
    },
    last_run_status: "success",
    total_signals: 1284,
    total_runs: 428,
  },
  {
    id: "s2-frankfurter",
    slug: "frankfurter",
    name: "Frankfurter Exchange",
    description: "EUR exchange rates — USD, GBP, BRL, JPY from the European Central Bank.",
    api_base_url: "https://api.frankfurter.dev",
    schedule_interval_minutes: 60,
    is_active: true,
    created_at: "2024-01-10T08:00:00Z",
    updated_at: "2024-01-15T09:00:00Z",
    freshness: {
      source_slug: "frankfurter",
      source_name: "Frankfurter Exchange",
      last_success_at: new Date(Date.now() - 35 * 60000).toISOString(),
      last_attempt_at: new Date(Date.now() - 35 * 60000).toISOString(),
      is_stale: false,
      staleness_minutes: 35,
    },
    last_run_status: "success",
    total_signals: 856,
    total_runs: 214,
  },
  {
    id: "s3-coingecko",
    slug: "coingecko",
    name: "CoinGecko Crypto",
    description: "Cryptocurrency prices — Bitcoin, Ethereum, Solana in USD with 24h changes.",
    api_base_url: "https://api.coingecko.com",
    schedule_interval_minutes: 15,
    is_active: true,
    created_at: "2024-01-10T08:00:00Z",
    updated_at: "2024-01-15T10:45:00Z",
    freshness: {
      source_slug: "coingecko",
      source_name: "CoinGecko Crypto",
      last_success_at: new Date(Date.now() - 72 * 60000).toISOString(),
      last_attempt_at: new Date(Date.now() - 3 * 60000).toISOString(),
      is_stale: true,
      staleness_minutes: 72,
    },
    last_run_status: "failed",
    total_signals: 2142,
    total_runs: 714,
  },
];

// ─── Mock Runs ────────────────────────────────────────────

function makeRun(
  id: string,
  source: SourceWithFreshness,
  status: "success" | "failed" | "running",
  minutesAgo: number,
  durationMs: number,
  fetched: number,
  stored: number,
  error?: string
): Run {
  const started = new Date(Date.now() - minutesAgo * 60000);
  return {
    id,
    source_id: source.id,
    source_slug: source.slug,
    source_name: source.name,
    status,
    started_at: started.toISOString(),
    finished_at: status === "running" ? null : new Date(started.getTime() + durationMs).toISOString(),
    duration_ms: status === "running" ? null : durationMs,
    records_fetched: fetched,
    records_stored: stored,
    error_message: error || null,
    created_at: started.toISOString(),
  };
}

export const mockRuns: Run[] = [
  makeRun("r01", mockSources[0], "success", 12, 1240, 3, 3),
  makeRun("r02", mockSources[2], "failed", 3, 4520, 0, 0, "HTTP 429 Too Many Requests"),
  makeRun("r03", mockSources[1], "success", 35, 890, 4, 4),
  makeRun("r04", mockSources[0], "success", 42, 1100, 3, 3),
  makeRun("r05", mockSources[2], "success", 18, 2300, 3, 3),
  makeRun("r06", mockSources[0], "success", 72, 980, 3, 3),
  makeRun("r07", mockSources[1], "success", 95, 920, 4, 4),
  makeRun("r08", mockSources[2], "success", 33, 1950, 3, 3),
  makeRun("r09", mockSources[0], "success", 102, 1300, 3, 3),
  makeRun("r10", mockSources[1], "failed", 155, 5100, 0, 0, "Connection timeout"),
  makeRun("r11", mockSources[2], "success", 48, 2100, 3, 3),
  makeRun("r12", mockSources[0], "success", 132, 1150, 3, 3),
];

// ─── Mock Freshness ───────────────────────────────────────

export const mockFreshness: FreshnessStatus[] = mockSources.map((s) => s.freshness!);

// ─── Mock Quality Checks ─────────────────────────────────

export const mockQualityChecks: QualityCheck[] = [
  {
    id: "qc01", run_id: "r01", source_slug: "open-meteo", source_name: "Open-Meteo Weather",
    check_name: "null_check", check_status: "pass",
    expected_value: "non-null", actual_value: "all fields present",
    message: "All critical fields are present and non-null.",
    checked_at: new Date(Date.now() - 12 * 60000).toISOString(),
  },
  {
    id: "qc02", run_id: "r01", source_slug: "open-meteo", source_name: "Open-Meteo Weather",
    check_name: "volume_check", check_status: "pass",
    expected_value: "3", actual_value: "3",
    message: "Expected 3 signals, received 3.",
    checked_at: new Date(Date.now() - 12 * 60000).toISOString(),
  },
  {
    id: "qc03", run_id: "r01", source_slug: "open-meteo", source_name: "Open-Meteo Weather",
    check_name: "range_check", check_status: "pass",
    expected_value: "-60..60", actual_value: "8.2",
    message: "Temperature 8.2°C is within expected range.",
    checked_at: new Date(Date.now() - 12 * 60000).toISOString(),
  },
  {
    id: "qc04", run_id: "r03", source_slug: "frankfurter", source_name: "Frankfurter Exchange",
    check_name: "null_check", check_status: "pass",
    expected_value: "non-null", actual_value: "all fields present",
    message: "All critical fields are present and non-null.",
    checked_at: new Date(Date.now() - 35 * 60000).toISOString(),
  },
  {
    id: "qc05", run_id: "r03", source_slug: "frankfurter", source_name: "Frankfurter Exchange",
    check_name: "volume_check", check_status: "pass",
    expected_value: "4", actual_value: "4",
    message: "Expected 4 signals, received 4.",
    checked_at: new Date(Date.now() - 35 * 60000).toISOString(),
  },
  {
    id: "qc06", run_id: "r02", source_slug: "coingecko", source_name: "CoinGecko Crypto",
    check_name: "null_check", check_status: "fail",
    expected_value: "non-null", actual_value: "no data",
    message: "Fetch failed — no data to validate.",
    checked_at: new Date(Date.now() - 3 * 60000).toISOString(),
  },
  {
    id: "qc07", run_id: "r05", source_slug: "coingecko", source_name: "CoinGecko Crypto",
    check_name: "volume_check", check_status: "pass",
    expected_value: "3", actual_value: "3",
    message: "Expected 3 signals, received 3.",
    checked_at: new Date(Date.now() - 18 * 60000).toISOString(),
  },
  {
    id: "qc08", run_id: "r05", source_slug: "coingecko", source_name: "CoinGecko Crypto",
    check_name: "schema_drift", check_status: "warn",
    expected_value: "stable schema", actual_value: "new field: total_supply",
    message: "Unexpected field 'total_supply' found in response.",
    checked_at: new Date(Date.now() - 18 * 60000).toISOString(),
  },
];

export const mockQualitySummary: QualitySummary = {
  total: mockQualityChecks.length,
  passed: mockQualityChecks.filter((c) => c.check_status === "pass").length,
  warnings: mockQualityChecks.filter((c) => c.check_status === "warn").length,
  failures: mockQualityChecks.filter((c) => c.check_status === "fail").length,
};

// ─── Mock Signals ─────────────────────────────────────────

export const mockSignals: NormalizedSignal[] = [
  { id: "sig01", source_slug: "open-meteo", signal_type: "weather", signal_key: "temperature_celsius", signal_value: 8.2, signal_unit: "°C", observed_at: new Date(Date.now() - 12 * 60000).toISOString(), metadata: { location: "Berlin" } },
  { id: "sig02", source_slug: "open-meteo", signal_type: "weather", signal_key: "humidity_percent", signal_value: 73, signal_unit: "%", observed_at: new Date(Date.now() - 12 * 60000).toISOString(), metadata: { location: "Berlin" } },
  { id: "sig03", source_slug: "open-meteo", signal_type: "weather", signal_key: "wind_speed_kmh", signal_value: 14.5, signal_unit: "km/h", observed_at: new Date(Date.now() - 12 * 60000).toISOString(), metadata: { location: "Berlin" } },
  { id: "sig04", source_slug: "frankfurter", signal_type: "exchange_rate", signal_key: "EUR_USD", signal_value: 1.0842, signal_unit: "USD", observed_at: new Date(Date.now() - 35 * 60000).toISOString(), metadata: { base: "EUR" } },
  { id: "sig05", source_slug: "frankfurter", signal_type: "exchange_rate", signal_key: "EUR_GBP", signal_value: 0.8573, signal_unit: "GBP", observed_at: new Date(Date.now() - 35 * 60000).toISOString(), metadata: { base: "EUR" } },
  { id: "sig06", source_slug: "frankfurter", signal_type: "exchange_rate", signal_key: "EUR_BRL", signal_value: 5.4821, signal_unit: "BRL", observed_at: new Date(Date.now() - 35 * 60000).toISOString(), metadata: { base: "EUR" } },
  { id: "sig07", source_slug: "frankfurter", signal_type: "exchange_rate", signal_key: "EUR_JPY", signal_value: 163.45, signal_unit: "JPY", observed_at: new Date(Date.now() - 35 * 60000).toISOString(), metadata: { base: "EUR" } },
  { id: "sig08", source_slug: "coingecko", signal_type: "crypto_price", signal_key: "bitcoin_usd", signal_value: 97245.0, signal_unit: "USD", observed_at: new Date(Date.now() - 18 * 60000).toISOString(), metadata: { change_24h: 2.34 } },
  { id: "sig09", source_slug: "coingecko", signal_type: "crypto_price", signal_key: "ethereum_usd", signal_value: 3412.5, signal_unit: "USD", observed_at: new Date(Date.now() - 18 * 60000).toISOString(), metadata: { change_24h: -0.87 } },
  { id: "sig10", source_slug: "coingecko", signal_type: "crypto_price", signal_key: "solana_usd", signal_value: 189.3, signal_unit: "USD", observed_at: new Date(Date.now() - 18 * 60000).toISOString(), metadata: { change_24h: 5.12 } },
];

// ─── Mock Metrics ─────────────────────────────────────────

export const mockMetrics: MetricsSummary = {
  total_sources: 3,
  active_sources: 3,
  total_runs: 1356,
  successful_runs: 1298,
  failed_runs: 58,
  total_signals: 4282,
  total_quality_checks: 4068,
  quality_pass_rate: 0.946,
  sources_stale: 1,
  last_activity_at: new Date(Date.now() - 3 * 60000).toISOString(),
};
