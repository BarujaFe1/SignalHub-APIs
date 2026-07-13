# Screenshots

Real dashboard captures (no PII — public APIs / demo data only).

| File | Contents |
|------|----------|
| `01-overview-dashboard.png` | Overview KPIs and system pulse |
| `02-runs-timeline.png` | Runs history |
| `03-source-detail.png` | Source detail / freshness |
| `04-quality-checks.png` | Quality gates |
| `05-swagger-ui.png` | OpenAPI Swagger UI |

## How to re-capture

1. Seed + start API on `:8000` and web on `:3000` (see root README).
2. Trigger at least one successful run (`Run now` or HTTP collection).
3. Use browser width ≥ 1280px; prefer light or dark consistently.
4. Avoid personal emails, private keys, or local absolute paths in the frame.
5. Overwrite the PNGs above with the same filenames.

Port note: dashboard is **`:3000`** (not 3001).
