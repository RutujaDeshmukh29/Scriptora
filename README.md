# Scriptora

> Write. Collaborate. Create.

Scriptora is a collaborative script-writing and project-management workspace for filmmakers, content creators, production teams, theatre groups, YouTubers, agencies, and creative studios — built to replace the Word/Google Docs shuffle with one purpose-built platform.

**Suggested repository name:** `scriptora` (private, monorepo layout).

## Status

🚧 Active build — 3-day initial sprint, followed by a phased rollout. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for exactly what's live now versus what's coming.

## Documentation

| Doc | Purpose |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | Product Requirements — what we're building and why |
| [`docs/SRS.md`](docs/SRS.md) | Software Requirements Specification — detailed functional & non-functional requirements |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System design, database schema, API conventions, deployment topology |
| [`docs/DIRECTORY_STRUCTURE.md`](docs/DIRECTORY_STRUCTURE.md) | Complete, file-level scaffold for every app in the monorepo |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | 3-day sprint plan + full phased roadmap beyond it |

## Features

**Shipping in the 3-day sprint**
- Auth (register/login, JWT + refresh tokens)
- Projects with Owner / Editor / Viewer roles
- Script creation, organization, duplication
- Tiptap rich text editor with autosave (debounced, no manual save button)
- Basic "who's viewing" presence
- Comments (highlight, reply, resolve)
- Basic in-app notifications and activity log
- PDF export
- Deployed, working end-to-end demo

**Phase 2 and beyond** (see [`docs/ROADMAP.md`](docs/ROADMAP.md) for full detail)
- True real-time collaborative editing (live cursors, conflict-free concurrent edits via Yjs)
- Version history (compare/restore)
- Global search, full notification system, DOCX/TXT export
- Screenplay-specific formatting and Fountain/.fdx import
- Billing, multi-tenant workspaces
- AI-assisted writing features (V2)

## Tech Stack

**Frontend** — Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui, Framer Motion, React Hook Form, Zustand, Tiptap

**Backend** — FastAPI, SQLAlchemy, Alembic, Pydantic, JWT auth, WebSockets, Redis

**Real-time collaboration** (Phase 2) — Yjs + Hocuspocus as a dedicated Node.js service, kept separate from the main API — see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for why

**Database** — PostgreSQL (Neon)

**Storage** — Supabase Storage or Cloudinary

**Deployment** — Vercel (frontend) · Railway or Fly.io (backend + collaboration service)

## Project Structure

```
scriptora/
├── apps/
│   ├── web/              # Next.js frontend
│   ├── api/                # FastAPI backend
│   └── collaboration/      # Yjs + Hocuspocus real-time service (Phase 2)
├── docs/
├── .github/workflows/
└── README.md
```

Full file-by-file breakdown: [`docs/DIRECTORY_STRUCTURE.md`](docs/DIRECTORY_STRUCTURE.md).

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL connection (Neon recommended)
- Redis (local via Docker, or a hosted instance)

### Environment variables

**`apps/web/.env.example`**
```
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_WS_URL=
```

**`apps/api/.env.example`**
```
DATABASE_URL=
JWT_SECRET=
JWT_ACCESS_EXPIRE_MINUTES=15
JWT_REFRESH_EXPIRE_DAYS=30
REDIS_URL=
STORAGE_PROVIDER=
STORAGE_API_KEY=
CORS_ORIGINS=
```

**`apps/collaboration/.env.example`** *(Phase 2)*
```
DATABASE_URL=
API_AUTH_VERIFY_URL=
REDIS_URL=
```

### Running locally

```bash
# Frontend
cd apps/web
npm install
npm run dev

# Backend
cd apps/api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Collaboration service (Phase 2)
cd apps/collaboration
npm install
npm run dev
```

### Available scripts

| Location | Command | Purpose |
|---|---|---|
| `apps/web` | `npm run dev` | Local dev server |
| `apps/web` | `npm run build` | Production build |
| `apps/api` | `uvicorn app.main:app --reload` | Local dev server |
| `apps/api` | `alembic revision --autogenerate -m "..."` | Create a migration |
| `apps/api` | `alembic upgrade head` | Apply migrations |
| `apps/api` | `pytest` | Run backend tests |

## Testing

Backend: `pytest` under `apps/api/tests/`, covering auth, project permissions, and script CRUD as a baseline. Frontend: add Vitest/Playwright coverage as features stabilize post-sprint — not a day-1–3 priority.

## Deployment

1. **Database** — provision a Neon Postgres project, run `alembic upgrade head` against it.
2. **Backend** — deploy `apps/api` to Railway or Fly.io; set env vars from `.env.example`.
3. **Frontend** — deploy `apps/web` to Vercel; set `NEXT_PUBLIC_API_URL` to the backend's public URL.
4. **Collaboration service** (Phase 2) — deploy `apps/collaboration` as a second Railway/Fly.io service once built.

## Development Workflow

- `main` — always deployable.
- Feature branches off `main`, merged via PR.
- CI (`.github/workflows/`) runs lint/test on every PR; deploy triggers on merge to `main`.

## License

Proprietary — all rights reserved. This is a commissioned project; confirm IP ownership and usage terms with the project owner before treating any part of this repository as open source.
