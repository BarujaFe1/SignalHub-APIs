# Problem statement — SignalHub APIs

## Who feels the pain?

Analytics engineers, data engineers, and full-stack builders who integrate **multiple public or partner APIs** into a product or analytics layer — and then lose visibility when those integrations silently fail, drift, or go stale.

## What breaks today?

| Invisible work | Consequence |
|----------------|-------------|
| Scheduled fetches with no run history | “Did it run?” becomes a log archaeology exercise |
| Heterogeneous JSON shapes | Downstream code assumes fields that disappeared |
| No freshness signal | Dashboards show yesterday’s data without warning |
| No quality gates | Bad values reach consumers before anyone notices |
| Manual triggers without audit | Hard to reproduce incidents |

## Decision / flow this project enables

SignalHub answers, in one place:

1. Which sources are registered and active?
2. Did the last run succeed, how long did it take, how many records?
3. Are data still fresh relative to the schedule?
4. Did quality checks pass (null, volume, range, required schema keys)?
5. What normalized signals were stored?

That turns an opaque integration into an **explainable ops loop**: ingest → validate → normalize → persist → observe → decide whether to trust the data.

## Consumers (V1)

| Consumer | How they use SignalHub |
|----------|------------------------|
| Engineer (local demo / lab) | Swagger + dashboard to prove the pipeline |
| Recruiter / interviewer | Readable evidence of data-product thinking |
| Future product surface | REST `/api/v1` as a stable contract for UIs |

Not a multi-tenant SaaS. Not a replacement for Airflow/Kafka. A **focused lab** that makes backend analytics work visible.

## Success criteria (honest)

- Clone → seed SQLite → run API + web without Docker.
- Trigger a source and see run, signals, QC, and freshness update.
- OpenAPI documents the same shapes the UI consumes.
- Claims in the README match what the code actually does.
