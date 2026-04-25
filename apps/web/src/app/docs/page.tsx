"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ExternalLink } from "lucide-react";

export default function DocsPage() {
  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">Architecture & Docs</h1>
        <p className="text-sm text-muted-foreground">
          How SignalHub APIs works — data flow, modules, decisions, and contracts.
        </p>
      </div>

      {/* Architecture Diagram */}
      <Card className="border-border/60">
        <CardContent className="py-6 space-y-4">
          <h2 className="text-sm font-semibold">Data Flow</h2>
          <div className="rounded-lg bg-muted/50 border border-border/50 p-6 font-mono text-xs leading-relaxed overflow-x-auto">
            <pre className="text-muted-foreground">{`
┌─────────────────────────────────────────────────────────────────┐
│                        External APIs                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Open-Meteo   │  │  Frankfurter  │  │  CoinGecko   │          │
│  │   (Weather)   │  │  (Currency)   │  │   (Crypto)   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Ingestion Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Connector   │  │   Connector   │  │   Connector   │          │
│  │  fetch()      │  │  fetch()      │  │  fetch()      │          │
│  │  validate()   │  │  validate()   │  │  validate()   │          │
│  │  normalize()  │  │  normalize()  │  │  normalize()  │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         └──────────────────┼──────────────────┘                 │
│                            ▼                                    │
│  ┌──────────────────────────────────┐  ┌──────────────────┐    │
│  │  Quality Checks                  │  │  Scheduler        │    │
│  │  null · volume · range · schema  │  │  APScheduler      │    │
│  └──────────────────────────────────┘  └──────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        PostgreSQL                               │
│  sources · runs · raw_payloads · normalized_signals             │
│  freshness_status · quality_checks · event_logs                 │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Read Layer                           │
│  /sources · /runs · /freshness · /quality · /signals · /metrics │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Next.js Status Page                           │
│  Overview · Sources · Runs · Quality · Docs                     │
└─────────────────────────────────────────────────────────────────┘`}</pre>
          </div>
        </CardContent>
      </Card>

      {/* Key Decisions */}
      <Card className="border-border/60">
        <CardContent className="py-6 space-y-4">
          <h2 className="text-sm font-semibold">Key Architecture Decisions</h2>
          <div className="space-y-4">
            {[
              {
                decision: "Single-process architecture",
                rationale: "FastAPI + APScheduler in one process. No distributed overhead for 3 connectors. Simplifies deployment and debugging.",
              },
              {
                decision: "Raw + Normalized persistence",
                rationale: "Store raw API responses as JSONB for debugging and reprocessing. Normalize into typed signals for consumption. Both indexed and traceable.",
              },
              {
                decision: "Idempotency by time window",
                rationale: "Each run has an idempotency key like 'open-meteo:2024-01-15:10'. Prevents duplicate ingestion within the same time window.",
              },
              {
                decision: "Quality checks at ingestion time",
                rationale: "Null checks, volume checks, range validation, and schema drift detection run after each connector. Results are persisted, not transient.",
              },
              {
                decision: "No auth in V1",
                rationale: "Portfolio project. Authentication adds complexity without demonstrating data engineering skills. Scope reduction for terminability.",
              },
              {
                decision: "APScheduler over Celery/Airflow",
                rationale: "Lightweight, in-process, no external dependencies. Overkill tools are explicitly excluded to keep V1 simple and publishable.",
              },
            ].map((item, i) => (
              <div key={i} className="space-y-1">
                <p className="text-sm font-medium">{item.decision}</p>
                <p className="text-xs text-muted-foreground">{item.rationale}</p>
                {i < 5 && <Separator className="bg-border/40 mt-3" />}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Data Model */}
      <Card className="border-border/60">
        <CardContent className="py-6 space-y-4">
          <h2 className="text-sm font-semibold">Data Model (V1)</h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { name: "sources", desc: "Registered data sources (3 in V1)" },
              { name: "runs", desc: "Execution log for each connector invocation" },
              { name: "raw_payloads", desc: "Full API responses stored as JSONB" },
              { name: "normalized_signals", desc: "Typed, uniform signal values" },
              { name: "freshness_status", desc: "Per-source staleness tracking" },
              { name: "quality_checks", desc: "Validation results per run" },
              { name: "event_logs", desc: "System-wide operational events" },
            ].map((table) => (
              <div key={table.name} className="rounded-lg border border-border/50 px-4 py-3 space-y-1">
                <p className="text-sm font-mono font-medium">{table.name}</p>
                <p className="text-xs text-muted-foreground">{table.desc}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Tech Stack */}
      <Card className="border-border/60">
        <CardContent className="py-6 space-y-4">
          <h2 className="text-sm font-semibold">Tech Stack</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {[
              { layer: "Frontend", tech: "Next.js 15 · TypeScript · Tailwind CSS · shadcn/ui" },
              { layer: "Backend", tech: "Python · FastAPI · Pydantic" },
              { layer: "Database", tech: "PostgreSQL 16 · SQLAlchemy 2.0 · Alembic" },
              { layer: "Scheduler", tech: "APScheduler (AsyncIOScheduler)" },
              { layer: "Infra", tech: "Docker Compose" },
              { layer: "CI/CD", tech: "GitHub Actions" },
            ].map((item) => (
              <div key={item.layer} className="flex items-start gap-3">
                <span className="text-xs font-semibold text-primary w-16 shrink-0 pt-0.5">{item.layer}</span>
                <span className="text-xs text-muted-foreground">{item.tech}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Links */}
      <Card className="border-border/60">
        <CardContent className="py-6 space-y-4">
          <h2 className="text-sm font-semibold">API Reference</h2>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-lg border border-border px-4 py-2.5 text-sm font-medium hover:bg-muted transition-colors"
          >
            <ExternalLink className="h-4 w-4" />
            Open Swagger UI
          </a>
          <p className="text-xs text-muted-foreground">
            Interactive API documentation available at <code className="font-mono">localhost:8000/docs</code> when the backend is running.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
