"use client";

import { cn } from "@/lib/utils";
import type { RunStatus, CheckStatus } from "@/lib/types";

// ─── Status Badge ─────────────────────────────────────────

const statusConfig: Record<RunStatus, { label: string; className: string }> = {
  success: { label: "Success", className: "bg-signal-teal-subtle text-signal-success" },
  failed: { label: "Failed", className: "bg-red-50 text-signal-error dark:bg-red-950/30 dark:text-signal-error" },
  running: { label: "Running", className: "bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400 animate-pulse-subtle" },
  partial: { label: "Partial", className: "bg-amber-50 text-signal-warning dark:bg-amber-950/30 dark:text-signal-warning" },
};

export function StatusBadge({ status, className }: { status: RunStatus; className?: string }) {
  const config = statusConfig[status];
  return (
    <span className={cn(
      "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium tracking-tight",
      config.className,
      className,
    )}>
      <span className={cn("h-1.5 w-1.5 rounded-full", {
        "bg-signal-success": status === "success",
        "bg-signal-error": status === "failed",
        "bg-blue-500": status === "running",
        "bg-signal-warning": status === "partial",
      })} />
      {config.label}
    </span>
  );
}

// ─── Check Status Badge ──────────────────────────────────

const checkConfig: Record<CheckStatus, { label: string; className: string }> = {
  pass: { label: "Pass", className: "bg-signal-teal-subtle text-signal-success" },
  warn: { label: "Warning", className: "bg-amber-50 text-signal-warning dark:bg-amber-950/30 dark:text-signal-warning" },
  fail: { label: "Fail", className: "bg-red-50 text-signal-error dark:bg-red-950/30 dark:text-signal-error" },
};

export function CheckBadge({ status, className }: { status: CheckStatus; className?: string }) {
  const config = checkConfig[status];
  return (
    <span className={cn(
      "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
      config.className,
      className,
    )}>
      {config.label}
    </span>
  );
}

// ─── Freshness Pill ───────────────────────────────────────

export function FreshnessPill({ isStale, minutes }: { isStale: boolean; minutes: number }) {
  return (
    <span className={cn(
      "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
      isStale
        ? "bg-amber-50 text-signal-warning dark:bg-amber-950/30"
        : "bg-signal-teal-subtle text-signal-success"
    )}>
      <span className={cn("h-1.5 w-1.5 rounded-full", isStale ? "bg-signal-warning" : "bg-signal-success")} />
      {isStale ? `Stale (${minutes}m)` : `Fresh (${minutes}m ago)`}
    </span>
  );
}

// ─── System Pulse ─────────────────────────────────────────

export function SystemPulse({ staleCount, failedRecent }: { staleCount: number; failedRecent: number }) {
  const status = staleCount === 0 && failedRecent === 0
    ? "healthy"
    : failedRecent > 0
    ? "degraded"
    : "warning";

  const config = {
    healthy: { label: "All Systems Operational", color: "bg-signal-success", textColor: "text-signal-success" },
    warning: { label: "Partial Staleness", color: "bg-signal-warning", textColor: "text-signal-warning" },
    degraded: { label: "Issues Detected", color: "bg-signal-error", textColor: "text-signal-error" },
  };

  const c = config[status];

  return (
    <div className="flex items-center gap-2.5">
      <span className="relative flex h-2.5 w-2.5">
        <span className={cn("absolute inline-flex h-full w-full rounded-full opacity-75 animate-ping", c.color)} />
        <span className={cn("relative inline-flex h-2.5 w-2.5 rounded-full", c.color)} />
      </span>
      <span className={cn("text-sm font-medium", c.textColor)}>{c.label}</span>
    </div>
  );
}

// ─── Time Ago ─────────────────────────────────────────────

export function TimeAgo({ date }: { date: string | null }) {
  if (!date) return <span className="text-muted-foreground">Never</span>;

  const diff = Date.now() - new Date(date).getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  let label: string;
  if (minutes < 1) label = "Just now";
  else if (minutes < 60) label = `${minutes}m ago`;
  else if (hours < 24) label = `${hours}h ago`;
  else label = `${days}d ago`;

  return <span className="text-muted-foreground text-sm tabular-nums">{label}</span>;
}

// ─── Metric Card ──────────────────────────────────────────

export function MetricValue({ value, label, sublabel }: { value: string | number; label: string; sublabel?: string }) {
  return (
    <div className="space-y-1">
      <p className="text-2xl font-semibold tracking-tight tabular-nums">{value}</p>
      <p className="text-sm text-muted-foreground">{label}</p>
      {sublabel && <p className="text-xs text-muted-foreground/70">{sublabel}</p>}
    </div>
  );
}

// ─── Empty State ──────────────────────────────────────────

export function EmptyState({ title, description, icon }: { title: string; description: string; icon?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      {icon && <div className="mb-4 text-muted-foreground/50">{icon}</div>}
      <h3 className="text-sm font-medium text-foreground">{title}</h3>
      <p className="mt-1 text-sm text-muted-foreground max-w-sm">{description}</p>
    </div>
  );
}

// ─── Duration ─────────────────────────────────────────────

export function Duration({ ms }: { ms: number | null }) {
  if (ms === null) return <span className="text-muted-foreground">—</span>;
  if (ms < 1000) return <span className="tabular-nums">{ms}ms</span>;
  return <span className="tabular-nums">{(ms / 1000).toFixed(1)}s</span>;
}
