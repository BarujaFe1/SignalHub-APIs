"use client";

import { Card, CardContent } from "@/components/ui/card";
import { CheckBadge, TimeAgo, MetricValue, EmptyState } from "@/components/shared/indicators";
import { api } from "@/lib/api";
import type { QualityCheck, QualitySummary, SourceWithFreshness } from "@/lib/types";
import { ShieldCheck, Filter, RefreshCw, AlertCircle } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

const statusFilters = ["all", "pass", "warn", "fail"] as const;

export default function QualityPage() {
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [sourceFilter, setSourceFilter] = useState<string>("all");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [checks, setChecks] = useState<QualityCheck[]>([]);
  const [summary, setSummary] = useState<QualitySummary | null>(null);
  const [sources, setSources] = useState<SourceWithFreshness[]>([]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params: any = { limit: 50 };
      if (sourceFilter !== "all") params.source = sourceFilter;
      if (statusFilter !== "all") params.status = statusFilter;

      const [qualityRes, sourcesRes] = await Promise.all([
        api.quality(params),
        api.sources()
      ]);
      
      setChecks(qualityRes.items);
      setSummary(qualityRes.summary);
      setSources(sourcesRes);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load quality metrics. Ensure the API is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [sourceFilter, statusFilter]);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">Quality</h1>
        <p className="text-sm text-muted-foreground">
          Data quality checks executed after each connector run. Validates null fields, expected volumes, value ranges, and schema consistency.
        </p>
      </div>

      {/* Global Health */}
      <Card className="border-border/60">
        <CardContent className="py-5">
          {summary ? (
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="space-y-2 flex-1">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Global Pass Rate</span>
                  <span className="font-semibold tabular-nums">
                    {summary.total > 0 
                      ? ((summary.passed / summary.total) * 100).toFixed(1) 
                      : 100}%
                  </span>
                </div>
                <div className="h-2.5 rounded-full bg-muted overflow-hidden">
                  <div className="h-full rounded-full bg-signal-success transition-all" style={{
                    width: summary.total > 0 
                      ? `${(summary.passed / summary.total) * 100}%` 
                      : "100%"
                  }} />
                </div>
              </div>
              <div className="flex items-center gap-6">
                <MetricValue value={summary.passed} label="Passed" />
                <MetricValue value={summary.warnings} label="Warnings" />
                <MetricValue value={summary.failures} label="Failures" />
              </div>
            </div>
          ) : (
             <div className="flex justify-center text-sm text-muted-foreground">Loading summary...</div>
          )}
        </CardContent>
      </Card>

      {/* Filters */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-1 rounded-lg bg-muted p-1">
          {statusFilters.map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={cn(
                "rounded-md px-3 py-1.5 text-xs font-medium transition-all",
                statusFilter === status
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-3.5 w-3.5 text-muted-foreground" />
          <select
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            className="rounded-lg border border-border bg-background px-3 py-1.5 text-xs font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Sources</option>
            {sources.map((s) => (
              <option key={s.slug} value={s.slug}>{s.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* States */}
      {loading ? (
        <div className="flex h-64 flex-col items-center justify-center space-y-4 text-muted-foreground border border-border/60 rounded-xl bg-card">
          <RefreshCw className="h-6 w-6 animate-spin text-primary/50" />
          <p className="text-sm font-medium">Loading quality data...</p>
        </div>
      ) : error ? (
         <div className="flex h-64 flex-col items-center justify-center space-y-4 border border-border/60 rounded-xl bg-card">
          <div className="p-3 bg-destructive/10 rounded-full">
            <AlertCircle className="h-6 w-6 text-destructive" />
          </div>
          <p className="text-sm font-medium">Failed to load data</p>
          <p className="text-xs text-muted-foreground">{error}</p>
          <button 
            onClick={fetchData}
            className="mt-2 px-4 py-2 text-xs font-medium bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80"
          >
            Retry
          </button>
        </div>
      ) : checks.length === 0 ? (
        <EmptyState
          title="No checks found"
          description="Adjust your filters to see quality check results."
          icon={<ShieldCheck className="h-8 w-8" />}
        />
      ) : (
        <Card className="border-border/60 overflow-hidden animate-fade-in">
          <CardContent className="p-0">
            <div className="hidden sm:grid sm:grid-cols-12 gap-4 px-4 py-2.5 text-xs font-medium text-muted-foreground border-b border-border/50 bg-muted/30">
              <div className="col-span-1">Status</div>
              <div className="col-span-2">Source</div>
              <div className="col-span-2">Check</div>
              <div className="col-span-4">Message</div>
              <div className="col-span-1 text-right">Expected</div>
              <div className="col-span-2 text-right">Time</div>
            </div>
            <div className="divide-y divide-border/40">
              {checks.map((check) => (
                <div key={check.id} className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 px-4 py-3 hover:bg-muted/20 transition-colors text-sm items-center">
                  <div className="sm:col-span-1">
                    <CheckBadge status={check.check_status} />
                  </div>
                  <div className="sm:col-span-2 text-xs text-muted-foreground truncate">{check.source_name}</div>
                  <div className="sm:col-span-2 font-mono text-xs font-medium">{check.check_name}</div>
                  <div className="sm:col-span-4 text-xs text-muted-foreground truncate">{check.message}</div>
                  <div className="sm:col-span-1 text-right font-mono text-xs tabular-nums">{check.expected_value || "—"}</div>
                  <div className="sm:col-span-2 text-right">
                    <TimeAgo date={check.checked_at} />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
