"use client";

import { Card, CardContent } from "@/components/ui/card";
import { StatusBadge, FreshnessPill } from "@/components/shared/indicators";
import { api } from "@/lib/api";
import type { SourceWithFreshness } from "@/lib/types";
import { Radio, ArrowRight, Globe, Clock, RefreshCw, AlertCircle } from "lucide-react";
import Link from "next/link";
import { useState, useEffect } from "react";

export default function SourcesPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sources, setSources] = useState<SourceWithFreshness[]>([]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.sources();
      setSources(data);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load sources. Ensure the API is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">Sources</h1>
        <p className="text-sm text-muted-foreground">
          Registered signal sources. Each source has its own connector, schedule, and quality checks.
        </p>
      </div>

      {/* States */}
      {loading ? (
        <div className="flex h-64 flex-col items-center justify-center space-y-4 text-muted-foreground border border-border/60 rounded-xl bg-card">
          <RefreshCw className="h-6 w-6 animate-spin text-primary/50" />
          <p className="text-sm font-medium">Loading sources...</p>
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
      ) : sources.length === 0 ? (
        <div className="flex h-64 flex-col items-center justify-center space-y-4 text-muted-foreground border border-dashed border-border/60 rounded-xl bg-card/50">
          <Radio className="h-8 w-8 opacity-20" />
          <p className="text-sm font-medium">No sources registered</p>
        </div>
      ) : (
        <div className="space-y-4">
          {sources.map((source) => (
            <Link key={source.slug} href={`/sources/${source.slug}`}>
              <Card className="border-border/60 hover:border-primary/30 hover:shadow-sm transition-all duration-200 cursor-pointer group mb-4">
                <CardContent className="py-5">
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    {/* Left */}
                    <div className="space-y-3 flex-1 min-w-0">
                      <div className="flex items-center gap-3">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-muted shrink-0">
                          <Radio className="h-4 w-4 text-muted-foreground" />
                        </div>
                        <div className="min-w-0">
                          <h3 className="text-sm font-semibold group-hover:text-primary transition-colors">
                            {source.name}
                          </h3>
                          <p className="text-xs text-muted-foreground truncate">
                            {source.description}
                          </p>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted-foreground pl-12">
                        <span className="flex items-center gap-1.5">
                          <Globe className="h-3 w-3" />
                          {source.api_base_url || "No Base URL"}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Clock className="h-3 w-3" />
                          Every {source.schedule_interval_minutes}m
                        </span>
                      </div>
                    </div>

                    {/* Right */}
                    <div className="flex items-center gap-4 sm:flex-col sm:items-end sm:gap-3">
                      <div className="flex items-center gap-3">
                        {source.last_run_status && (
                          <StatusBadge status={source.last_run_status} />
                        )}
                        {source.freshness ? (
                          <FreshnessPill
                            isStale={source.freshness.is_stale}
                            minutes={source.freshness.staleness_minutes}
                          />
                        ) : (
                          <span className="text-xs text-muted-foreground px-2 py-1 bg-muted rounded-full">No runs yet</span>
                        )}
                      </div>
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <span className="tabular-nums">{source.total_signals.toLocaleString()} signals</span>
                        <span className="tabular-nums">{source.total_runs.toLocaleString()} runs</span>
                        <ArrowRight className="h-3.5 w-3.5 text-muted-foreground/50 group-hover:text-primary transition-colors" />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
