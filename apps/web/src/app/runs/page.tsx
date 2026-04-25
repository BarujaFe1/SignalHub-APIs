"use client";

import { Card, CardContent } from "@/components/ui/card";
import { StatusBadge, TimeAgo, Duration, EmptyState } from "@/components/shared/indicators";
import { api } from "@/lib/api";
import type { Run, SourceWithFreshness } from "@/lib/types";
import { Activity, Filter, RefreshCw, AlertCircle } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

const statusFilters = ["all", "success", "failed", "running"] as const;

export default function RunsPage() {
  const [sourceFilter, setSourceFilter] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [runs, setRuns] = useState<Run[]>([]);
  const [sources, setSources] = useState<SourceWithFreshness[]>([]);
  const [total, setTotal] = useState(0);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const runsParams: any = { limit: 50 };
      if (sourceFilter !== "all") runsParams.source = sourceFilter;
      if (statusFilter !== "all") runsParams.status = statusFilter;
      
      const [runsRes, sourcesRes] = await Promise.all([
        api.runs(runsParams),
        api.sources()
      ]);
      
      setRuns(runsRes.items);
      setTotal(runsRes.total);
      setSources(sourcesRes);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load runs. Ensure the API is running.");
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
        <h1 className="text-2xl font-semibold tracking-tight">Runs</h1>
        <p className="text-sm text-muted-foreground">
          Execution history across all connectors. Each run represents a complete fetch → normalize → persist cycle.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        {/* Status tabs */}
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

        {/* Source filter */}
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
          <p className="text-sm font-medium">Loading runs...</p>
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
      ) : runs.length === 0 ? (
        <EmptyState
          title="No runs found"
          description="Try adjusting your filters to see more results."
          icon={<Activity className="h-8 w-8" />}
        />
      ) : (
        <Card className="border-border/60 overflow-hidden animate-fade-in">
          <CardContent className="p-0">
            {/* Table Header */}
            <div className="hidden sm:grid sm:grid-cols-12 gap-4 px-4 py-2.5 text-xs font-medium text-muted-foreground border-b border-border/50 bg-muted/30">
              <div className="col-span-1">Status</div>
              <div className="col-span-3">Source</div>
              <div className="col-span-2">Started</div>
              <div className="col-span-1 text-right">Duration</div>
              <div className="col-span-2 text-right">Records</div>
              <div className="col-span-3">Error</div>
            </div>

            {/* Table Body */}
            <div className="divide-y divide-border/40">
              {runs.map((run) => (
                <div
                  key={run.id}
                  className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 px-4 py-3 hover:bg-muted/20 transition-colors text-sm items-center"
                >
                  <div className="sm:col-span-1">
                    <StatusBadge status={run.status} />
                  </div>
                  <div className="sm:col-span-3 font-medium truncate">
                    {run.source_name}
                  </div>
                  <div className="sm:col-span-2">
                    <TimeAgo date={run.started_at} />
                  </div>
                  <div className="sm:col-span-1 text-right">
                    <Duration ms={run.duration_ms} />
                  </div>
                  <div className="sm:col-span-2 text-right tabular-nums text-muted-foreground">
                    {run.records_fetched > 0 ? (
                      <span>{run.records_fetched} fetched · {run.records_stored} stored</span>
                    ) : (
                      <span>—</span>
                    )}
                  </div>
                  <div className="sm:col-span-3 truncate">
                    {run.error_message ? (
                      <span className="text-xs text-signal-error font-mono">{run.error_message}</span>
                    ) : (
                      <span className="text-muted-foreground/50 text-xs">—</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Footer */}
      {!loading && !error && runs.length > 0 && (
        <p className="text-xs text-muted-foreground text-center">
          Showing {runs.length} of {total} runs
        </p>
      )}
    </div>
  );
}
