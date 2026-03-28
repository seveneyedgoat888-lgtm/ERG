# Emotional Regulation Graph Tracker (MVP)

A local-first Next.js app for tracking emotional baseline, stress events, and emotional intensity over time.
It visualizes escalation patterns and highlights when intensity crosses the **Autopilot Zone** threshold (**7/10**).

## Features

- Dashboard with summary cards:
  - today's baseline
  - latest intensity
  - stress events this week
  - autopilot crossings this week
  - average baseline this week
  - most common trigger this week
- Emotional regulation time-series chart:
  - baseline + stress entries in one timeline
  - autopilot threshold reference line at intensity 7
  - range filters: today, 7 days, 30 days, custom
- Daily baseline logging (1–10, one per day, optional notes)
- Stress event logging (title, optional description, stress increase 1–5, intensity 1–10, trigger, coping, autopilot flag)
- History page:
  - chronological entries
  - filter by entry type
  - edit and delete entries
- Insights page:
  - baseline averages (7/14/30)
  - autopilot crossing counts
  - most common trigger
  - simple text summary of trend and threshold status
- CSV export endpoint (`/api/export`)
- Seed script with demo data
- Unit tests for analytics helpers and trend/threshold logic

## Emotional regulation model

The app models emotional regulation as **intensity over time**:

- **X-axis:** time
- **Y-axis:** emotional intensity (1 to 10)
- **Autopilot Zone:** intensity `>= 7`

This supports quick review of:
- baseline state,
- stress spikes,
- recovery patterns,
- and potential trigger patterns.

## Tech stack

- Next.js (App Router) + TypeScript
- SQLite + Prisma
- Recharts for charting
- Vitest for unit tests

## Project structure

```txt
app/
  api/
    baselines/
    stress-events/
    export/
  history/
  insights/
  log-baseline/
  log-stress-event/
  layout.tsx
  page.tsx
components/
  BaselineForm.tsx
  StressEventForm.tsx
  DashboardView.tsx
  RegulationChart.tsx
  HistoryClient.tsx
lib/
  analytics.ts
  constants.ts
  data.ts
  date.ts
  db.ts
  validation.ts
prisma/
  schema.prisma
  seed.ts
tests/
  analytics.test.ts
```

## Setup

### 1) Install dependencies

```bash
npm install
```

### 2) Set environment variables

Create `.env` in project root:

```env
DATABASE_URL="file:./prisma/dev.db"
```

### 3) Generate Prisma client + run migration

```bash
npm run prisma:generate
npm run prisma:migrate -- --name init
```

### 4) (Optional) Seed demo data

```bash
npm run prisma:seed
```

### 5) Start dev server

```bash
npm run dev
```

Open: `http://localhost:3000`

## Running tests

```bash
npm run test
```

## Key technical decisions

- **Single user MVP with multi-user-ready structure:** all entries include `userId`; app uses a default local user now.
- **Simple API routes + client forms:** straightforward local CRUD without overengineering auth.
- **Prisma enum for trigger categories:** keeps input controlled and analytics consistent.
- **Chart built from merged baseline + stress series:** one timeline view to compare baseline and stress escalation.
- **Trend logic:** compares current week average baseline against previous week with a small meaningful delta threshold.

## Notes

- Intended for local MVP usage and fast iteration.
- Designed to feel minimal and calm, especially for non-technical users.
