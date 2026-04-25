# Screenshots Placeholder

This directory will contain screenshots of the SignalHub APIs dashboard.

## Required Screenshots

1. **01-overview-dashboard.png** - Overview page with KPI cards and metrics
2. **02-runs-timeline.png** - Runs page showing execution history
3. **03-source-detail.png** - Source detail page with freshness and quality
4. **04-quality-checks.png** - Quality checks page with pass/fail breakdown
5. **05-swagger-ui.png** - Swagger UI showing API endpoints

## How to Capture

1. Start the backend: `cd apps/api && uvicorn app.main:app --reload`
2. Start the frontend: `cd apps/web && npm run dev`
3. Navigate to http://localhost:3001
4. Capture screenshots of each page
5. Save them in this directory with the names above

## Note

Screenshots should be captured with the system running and showing real data from the database.
