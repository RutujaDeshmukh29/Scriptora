# Scriptora — Roadmap

Two things live in this document: a concrete **3-day sprint plan** that ships a real, usable product, and the **full phased roadmap** for everything that comes after it. Read the note at the top before starting the sprint.

---

## Before you start: what the 3-day sprint deliberately cuts

To hit 3 days, the sprint below trades the *hardest, slowest* feature — true conflict-free simultaneous editing (Yjs/Hocuspocus) — for a simpler "autosave + who's currently viewing" version. It also defers global search, DOCX/TXT export, the full notification system, and version compare/restore. Everything cut has a named Phase below and a placeholder folder already scaffolded in `DIRECTORY_STRUCTURE.md`, so nothing needs to be re-architected to add it back — it just gets built.

What you *do* have at the end of day 3: working auth, projects with roles, script creation and organization, a real rich-text editor with autosave, basic comments, basic PDF export, and a deployed URL your friend can actually use.

---

## 3-Day Sprint Plan

### Day 1 — Foundation: Auth, Data Layer, Projects

**Morning**
- Scaffold the monorepo (`apps/web`, `apps/api`) per `DIRECTORY_STRUCTURE.md`.
- Provision Neon Postgres; set up SQLAlchemy + Alembic; create core models: `User`, `Organization`, `Project`, `ProjectMember`, `Script`.
- Run first migration.

**Midday**
- Build auth: register, login, JWT access + refresh token issuance, logout.
- Skip email verification and "forgot password" email flow for now (defer to Phase 2 — they need a transactional email provider wired up, which is its own setup cost). Use direct signup for the sprint.

**Afternoon**
- Project CRUD (create/edit/archive) with Owner/Editor/Viewer roles enforced server-side.
- Add members by email directly (skip the invitation-token email flow for now — same reasoning as above).

**Evening**
- Wire the Next.js dashboard shell to real endpoints: login, project list, create project.

### Day 2 — Script Editor Core

**Morning**
- Script CRUD within a project: create, rename, duplicate, delete, list.

**Midday**
- Integrate Tiptap with core formatting (bold, italic, headings, lists, checklists, tables, links, images, undo/redo).
- Build autosave: debounced PUT to the API on change, with a visible "Saved / Saving…" indicator. This is *not* real-time multi-user merging — two people editing the same paragraph at the same instant can overwrite each other. Acceptable for a small team's first week of use; flagged clearly as the first Phase 2 priority.

**Afternoon**
- Basic presence: a lightweight heartbeat (poll or simple WebSocket broadcast) showing who else currently has the script open — not live cursors, just "Priya is also viewing this script."

**Evening**
- Comments: highlight text, add comment, reply, resolve. Mentions can wait for Phase 2 (needs the notification system to be meaningful).

### Day 3 — Polish, Export, Deploy

**Morning**
- Minimal notifications: invited-to-project and new-comment only (in-app, not email).
- Basic activity log (project created, script created/edited, member joined) — simple feed, not the full timeline UI yet.

**Midday**
- PDF export (the format most likely to matter first for a script that needs to be shared/printed). DOCX and TXT deferred.

**Afternoon**
- Deploy: frontend to Vercel, backend to Railway (or Fly.io), confirm Neon connection, set all env vars, smoke-test the full flow end-to-end (register → create project → invite → write a script → comment → export PDF).

**Evening**
- Bug bash with your friend actually using it live. Capture the punch list — this becomes the start of Phase 2.

---

## Full Phased Roadmap (post-sprint)

### Phase 2 — Real Collaboration & History (next up)
- Replace the day-2 autosave/presence hack with true CRDT-based collaboration: stand up `apps/collaboration` (Yjs + Hocuspocus), wire JWT auth into the WebSocket handshake, implement persistence back to Postgres.
- Live cursors, typing indicators, proper conflict-free concurrent editing.
- Version history: periodic snapshots, compare, restore.
- Email verification and password reset (transactional email provider).
- Comment @mentions tied into the notification system.

### Phase 3 — Workspace Intelligence
- Global search across projects/scripts/titles/content.
- Full notification system (all event types from the SRS, in-app + optional email digest).
- Full activity timeline UI (filterable, per-project).
- DOCX and TXT export.

### Phase 4 — Screenplay-Native Editing
- Screenplay-specific Tiptap nodes (Scene Heading, Action, Character, Dialogue, Parenthetical, Transition) with industry-standard auto-formatting.
- Import from Fountain / Final Draft (`.fdx`).
- Script trash/recovery window.

### Phase 5 — Monetization & Multi-Tenant Readiness
- Stripe billing (plans, seats, trial).
- Organization-level settings and billing surfaced in the UI (data model already supports this from day 1).

### Phase 6 (V2) — AI Features
AI Script Writer · Dialogue Improvement · Grammar Correction · Scene Summarizer · Character Generator · Story Outline Generator · Plot Hole Detection · Character Consistency Checker · Story Expansion · Script Review · AI Director Suggestions · Shooting Schedule Generator

---

## Suggested working order after the sprint

Tackle Phase 2's collaboration engine before anything else in Phase 3+ — it's the feature that most defines whether Scriptora feels like "a real product" versus "a form with a text box," and every day it's delayed is a day your friend's team is editing with the collision risk from the day-2 shortcut.
