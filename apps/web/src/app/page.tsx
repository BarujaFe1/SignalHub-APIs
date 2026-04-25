"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  StatusBadge,
  FreshnessPill,
  SystemPulse,
  TimeAgo,
  MetricValue,
} from "@/components/shared/indicators";
import { api } from "@/lib/api";
import type { SourceWithFreshness, Run, MetricsSummary, QualitySummary } from "@/lib/types";
import { Radio, Activity, ShieldCheck, TrendingUp, Database, Clock, RefreshCw, AlertCircle } from "lucide-react";
import Link from "next/link";

export default function OverviewPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [sources, setSources] = useState<SourceWithFreshness[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [qualitySummary, setQualitySummary] = useState<QualitySummary | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [sourcesRes, runsRes, metricsRes, qualityRes] = await Promise.all([
        api.sources(),
        api.runs({ limit: 6 }),
        api.metrics(),
        api.quality({ limit: 1 }), // Just need the summary
      ]);
      
      setSources(sourcesRes);
      setRuns(runsRes.items);
      setMetrics(metricsRes);
      setQualitySummary(qualityRes.summary);
    } catch (err: any) {
      console.error(err);
      setError("Unable to connect to the backend API. Please ensure the server is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-[60vh] flex-col items-center justify-center space-y-4 text-muted-foreground animate-fade-in">
        <RefreshCw className="h-6 w-6 animate-spin text-primary/50" />
        <p className="text-sm font-medium">Connecting to SignalHub...</p>
      </div>
    );
  }

  if (error || !metrics || !qualitySummary) {
    return (
      <div className="flex h-[60vh] flex-col items-center justify-center space-y-4 animate-fade-in">
        <div className="p-4 bg-destructive/10 rounded-full">
          <AlertCircle className="h-6 w-6 text-destructive" />
        </div>
        <p className="text-sm font-medium text-foreground">API Connection Failed</p>
        <p className="text-xs text-muted-foreground max-w-[300px] text-center">{error}</p>
        <button 
          onClick={fetchData}
          className="mt-2 px-5 py-2 text-xs font-medium bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  const staleCount = sources.filter((s) => s.freshness?.is_stale).length;
  const recentFails = runs.filter((r) => r.status === "failed").length;
  const qualityRate = qualitySummary.total > 0 
    ? ((qualitySummary.passed / qualitySummary.total) * 100) 
    : 100;

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Page Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">Overview</h1>
        <p className="text-sm text-muted-foreground">
          System status and ingestion health across all signal sources.
        </p>
      </div>

      {/* System Pulse */}
      <Card className="border-border/60">
        <CardContent className="flex items-center justify-between py-4">
          <SystemPulse staleCount={staleCount} failedRecent={recentFails} />
          <p className="text-xs text-muted-foreground">
            {metrics.last_activity_at ? (
              <>Last activity <TimeAgo date={metrics.last_activity_at} /></>
            ) : (
              "No recent activity"
            )}
          </p>
        </CardContent>
      </Card>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
        {[
          { value: metrics.active_sources, label: "Sources", icon: Radio },
          { value: metrics.total_runs.toLocaleString(), label: "Total Runs", icon: Activity },
          { value: metrics.total_signals.toLocaleString(), label: "Signals", icon: Database },
          { value: `${qualityRate.toFixed(1)}%`, label: "Quality Rate", icon: ShieldCheck },
          { value: metrics.failed_runs, label: "Failed Runs", icon: TrendingUp },
          { value: metrics.sources_stale, label: "Stale Sources", icon: Clock },
        ].map((metric) => (
          <Card key={metric.label} className="border-border/60">
            <CardContent className="py-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-2">
                <metric.icon className="h-3.5 w-3.5" />
                <span className="text-xs font-medium">{metric.label}</span>
              </div>
              <p className="text-xl font-semibold tracking-tight tabular-nums">{metric.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Sources Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-foreground">Signal Sources</h2>
          <Link href="/sources" className="text-xs text-primary hover:underline">
            View all →
          </Link>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sources.map((source) => (
            <Link key={source.slug} href={`/sources/${source.slug}`}>
              <Card className="border-border/60 hover:border-primary/30 hover:shadow-sm transition-all duration-200 cursor-pointer group">
                <CardContent className="py-5 space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <h3 className="text-sm font-semibold group-hover:text-primary transition-colors">
                        {source.name}
                      </h3>
                      <p className="text-xs text-muted-foreground line-clamp-1">
                        {source.description}
                      </p>
                    </div>
                    {source.last_run_status && (
                      <StatusBadge status={source.last_run_status} />
                    )}
                  </div>

                  <Separator className="bg-border/50" />

                  <div className="flex items-center justify-between text-xs">
                    <div className="space-y-1">
                      <p className="text-muted-foreground">Freshness</p>
                      {source.freshness ? (
                        <FreshnessPill
                          isStale={source.freshness.is_stale}
                          minutes={source.freshness.staleness_minutes}
                        />
                      ) : (
                        <span className="text-muted-foreground">No data</span>
                      )}
                    </div>
                    <div className="text-right space-y-1">
                      <p className="text-muted-foreground">Signals</p>
                      <p className="font-semibold tabular-nums">{source.total_signals.toLocaleString()}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
          {sources.length === 0 && (
             <div className="col-span-full py-8 text-center text-sm text-muted-foreground border border-dashed rounded-lg">
               No sources configured yet.
             </div>
          )}
        </div>
      </div>

      {/* Recent Activity + Quality Summary */}
      <div className="grid gap-6 lg:grid-cols-5">
        {/* Recent Runs */}
        <div className="lg:col-span-3 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-foreground">Recent Runs</h2>
            <Link href="/runs" className="text-xs text-primary hover:underline">
              View all →
            </Link>
          </div>
          <Card className="border-border/60">
            <CardContent className="p-0">
              <div className="divide-y divide-border/50">
                {runs.map((run) => (
                  <div key={run.id} className="flex items-center justify-between px-4 py-3">
                    <div className="flex items-center gap-3 min-w-0">
                      <StatusBadge status={run.status} />
                      <div className="min-w-0">
                        <p className="text-sm font-medium truncate">{run.source_name}</p>
                        <p className="text-xs text-muted-foreground">
                          {run.records_stored} signals · {run.duration_ms ? `${(run.duration_ms / 1000).toFixed(1)}s` : "—"}
                        </p>
                      </div>
                    </div>
                    <TimeAgo date={run.started_at} />
                  </div>
                ))}
                {runs.length === 0 && (
                  <div className="px-4 py-8 text-center text-sm text-muted-foreground">
                    No recent runs found.
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quality Summary */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-foreground">Quality Summary</h2>
            <Link href="/quality" className="text-xs text-primary hover:underline">
              View all →
            </Link>
          </div>
          <Card className="border-border/60">
            <CardContent className="py-5 space-y-5">
              {/* Pass Rate */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Pass Rate</span>
                  <span className="font-semibold tabular-nums">
                    {qualityRate.toFixed(0)}%
                  </span>
                </div>
                <div className="h-2 rounded-full bg-muted overflow-hidden">
                  <div
                    className="h-full rounded-full bg-signal-success transition-all"
                    style={{ width: `${qualityRate}%` }}
                  />
                </div>
              </div>

              <Separator className="bg-border/50" />

              {/* Breakdown */}
              <div className="grid grid-cols-3 gap-4">
                <MetricValue value={qualitySummary.passed} label="Passed" />
                <MetricValue value={qualitySummary.warnings} label="Warnings" />
                <MetricValue value={qualitySummary.failures} label="Failures" />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

