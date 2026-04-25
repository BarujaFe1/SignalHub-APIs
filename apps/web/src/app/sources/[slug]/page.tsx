"use client";

import { use, useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  StatusBadge,
  CheckBadge,
  FreshnessPill,
  TimeAgo,
  Duration,
  MetricValue,
  EmptyState,
} from "@/components/shared/indicators";
import { api } from "@/lib/api";
import type { SourceDetail } from "@/lib/types";
import { ArrowLeft, Globe, Clock, Radio, Zap, RefreshCw, AlertCircle } from "lucide-react";
import Link from "next/link";

export default function SourceDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<SourceDetail | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.sourceDetail(slug);
      setData(res);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load source details. It might not exist or the API is down.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex h-[60vh] flex-col items-center justify-center space-y-4 text-muted-foreground animate-fade-in">
        <RefreshCw className="h-6 w-6 animate-spin text-primary/50" />
        <p className="text-sm font-medium">Loading source details...</p>
      </div>
    );
  }

  if (error || !data) {
     return (
      <div className="flex h-[60vh] flex-col items-center justify-center space-y-4 animate-fade-in">
        <div className="p-4 bg-destructive/10 rounded-full">
          <AlertCircle className="h-6 w-6 text-destructive" />
        </div>
        <p className="text-sm font-medium text-foreground">Source Not Found</p>
        <p className="text-xs text-muted-foreground max-w-[300px] text-center">{error}</p>
        <div className="flex gap-3 mt-2">
          <Link href="/sources" className="px-5 py-2 text-xs font-medium bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80 transition-colors">
            Back to Sources
          </Link>
          <button 
            onClick={fetchData}
            className="px-5 py-2 text-xs font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { source, recent_runs: sourceRuns, recent_signals: sourceSignals, recent_checks: sourceChecks } = data;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Back link */}
      <Link
        href="/sources"
        className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-3 w-3" />
        Back to Sources
      </Link>

      {/* Source Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
              <Radio className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">{source.name}</h1>
              <p className="text-sm text-muted-foreground">{source.description}</p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <Globe className="h-3 w-3" />
              {source.api_base_url || "No base URL"}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="h-3 w-3" />
              Every {source.schedule_interval_minutes} minutes
            </span>
            <span className="flex items-center gap-1.5">
              <Zap className="h-3 w-3" />
              {source.is_active ? "Active" : "Paused"}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {source.last_run_status && <StatusBadge status={source.last_run_status} />}
          {source.freshness && (
            <FreshnessPill isStale={source.freshness.is_stale} minutes={source.freshness.staleness_minutes} />
          )}
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Card className="border-border/60">
          <CardContent className="py-4">
            <MetricValue value={source.total_signals.toLocaleString()} label="Total Signals" />
          </CardContent>
        </Card>
        <Card className="border-border/60">
          <CardContent className="py-4">
            <MetricValue value={source.total_runs.toLocaleString()} label="Total Runs" />
          </CardContent>
        </Card>
        <Card className="border-border/60">
          <CardContent className="py-4">
            <MetricValue
              value={source.freshness ? source.freshness.staleness_minutes + "m" : "—"}
              label="Staleness"
            />
          </CardContent>
        </Card>
        <Card className="border-border/60">
          <CardContent className="py-4">
            <MetricValue
              value={sourceChecks.filter((c) => c.check_status === "pass").length + "/" + (sourceChecks.length || 0)}
              label="Checks Passing"
            />
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="runs" className="space-y-4">
        <TabsList className="bg-muted/50 border border-border/50">
          <TabsTrigger value="runs">Recent Runs</TabsTrigger>
          <TabsTrigger value="signals">Signals</TabsTrigger>
          <TabsTrigger value="quality">Quality</TabsTrigger>
        </TabsList>

        {/* Runs Tab */}
        <TabsContent value="runs" className="space-y-3">
          {sourceRuns.length === 0 ? (
            <EmptyState title="No runs yet" description="This source has not been executed yet." />
          ) : (
            <Card className="border-border/60">
              <CardContent className="p-0 divide-y divide-border/40">
                {sourceRuns.map((run) => (
                  <div key={run.id} className="flex items-center justify-between px-4 py-3 hover:bg-muted/20 transition-colors">
                    <div className="flex items-center gap-3 min-w-0">
                      <StatusBadge status={run.status} />
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 text-sm">
                          <Duration ms={run.duration_ms} />
                          <span className="text-muted-foreground">·</span>
                          <span className="text-muted-foreground tabular-nums text-xs">
                            {run.records_stored} signals
                          </span>
                        </div>
                        {run.error_message && (
                          <p className="text-xs text-signal-error font-mono truncate mt-0.5">
                            {run.error_message}
                          </p>
                        )}
                      </div>
                    </div>
                    <TimeAgo date={run.started_at} />
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Signals Tab */}
        <TabsContent value="signals" className="space-y-3">
          {sourceSignals.length === 0 ? (
            <EmptyState title="No signals" description="No normalized signals have been stored for this source." />
          ) : (
            <Card className="border-border/60 overflow-hidden">
              <CardContent className="p-0">
                <div className="hidden sm:grid sm:grid-cols-12 gap-4 px-4 py-2.5 text-xs font-medium text-muted-foreground border-b border-border/50 bg-muted/30">
                  <div className="col-span-3">Signal Key</div>
                  <div className="col-span-2">Type</div>
                  <div className="col-span-2 text-right">Value</div>
                  <div className="col-span-1">Unit</div>
                  <div className="col-span-4">Observed</div>
                </div>
                <div className="divide-y divide-border/40">
                  {sourceSignals.map((signal) => (
                    <div key={signal.id} className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 px-4 py-3 text-sm items-center hover:bg-muted/20 transition-colors">
                      <div className="sm:col-span-3 font-mono text-xs font-medium">{signal.signal_key}</div>
                      <div className="sm:col-span-2 text-muted-foreground text-xs">{signal.signal_type}</div>
                      <div className="sm:col-span-2 text-right font-mono font-semibold tabular-nums">
                        {signal.signal_value.toLocaleString(undefined, { maximumFractionDigits: 4 })}
                      </div>
                      <div className="sm:col-span-1 text-muted-foreground text-xs">{signal.signal_unit}</div>
                      <div className="sm:col-span-4 text-xs text-muted-foreground">
                        <TimeAgo date={signal.observed_at} />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Quality Tab */}
        <TabsContent value="quality" className="space-y-3">
          {sourceChecks.length === 0 ? (
            <EmptyState title="No checks" description="No quality checks have been recorded for this source." />
          ) : (
            <Card className="border-border/60">
              <CardContent className="p-0 divide-y divide-border/40">
                {sourceChecks.map((check) => (
                  <div key={check.id} className="flex items-start justify-between gap-4 px-4 py-3 hover:bg-muted/20 transition-colors">
                    <div className="flex items-start gap-3 min-w-0">
                      <CheckBadge status={check.check_status} />
                      <div className="min-w-0">
                        <p className="text-sm font-medium font-mono">{check.check_name}</p>
                        <p className="text-xs text-muted-foreground mt-0.5">{check.message}</p>
                        <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                          <span>Expected: <span className="font-mono">{check.expected_value || "—"}</span></span>
                          <span>Actual: <span className="font-mono">{check.actual_value || "—"}</span></span>
                        </div>
                      </div>
                    </div>
                    <TimeAgo date={check.checked_at} />
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
