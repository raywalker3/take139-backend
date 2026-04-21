# Take 139 Backend

FastAPI backend for the Take 139 premarital diagnostic.

## Phase 1 features
- Stores completed assessments
- Generates unique pair codes (ANCHOR-4829 format)
- Creates a professional PDF report (cover page, profile, behavioral markers, gospel truth, reflections, prayer)
- Emails results to admin + (optionally) test-taker via Resend
- Basic health + recent submissions endpoint

## Required environment variables
- `RESEND_API_KEY` — from resend.com
- `ADMIN_EMAIL` — where every submission goes (default: christopher.hilken@gmail.com)
- `FROM_EMAIL` — e.g. `Take 139 <results@take139.com>` (must be a verified domain in Resend)
- `DATABASE_PATH` — path to SQLite file (Railway: `/data/take139.db`)

## Endpoints
- `GET  /` — service info
- `GET  /health` — health check
- `POST /submit` — submit completed assessment
- `GET  /submissions/recent` — admin placeholder (add auth in Phase 2)

## Local dev
```
pip install -r requirements.txt
export RESEND_API_KEY=...
uvicorn main:app --reload
```
