# Product Requirements Document (PRD)

**Product:** Scriptora
**Tagline:** Write. Collaborate. Create.
**Version:** 1.0 (Draft)
**Status:** Architecture Phase
**Date:** July 2026
**Owner:** Rutuja Deshmukh

---

## 1. Executive Summary

Scriptora is a collaborative script-writing and project-management workspace built for filmmakers, content creators, production teams, theatre groups, YouTubers, agencies, and creative studios. It replaces the ad-hoc workflow of sharing Word/Google Docs for scripts with a single, purpose-built platform where teams write, review, comment on, and manage scripts together in real time.

## 2. Problem Statement

Creative teams currently write and manage scripts in general-purpose word processors. This produces predictable friction:

- Scripts for multiple projects become scattered across files and folders with no shared structure.
- Permissions are all-or-nothing; there's no concept of "editor vs. reviewer" per project.
- Feedback lives in scattered comment threads, chat messages, or marked-up PDFs.
- There is no activity history, no per-script version control, and no dedicated production workflow (scenes, revisions, shooting drafts).
- General-purpose editors have no concept of screenplay-specific structure (scene headings, character blocks, dialogue formatting).

## 3. Goals & Objectives

**Business goals**
- Deliver a production-ready V1 that a real creative team can adopt for daily script work.
- Establish an architecture that supports paid multi-tenant usage (workspaces/organizations, billing-ready) from day one, even if billing itself ships later.
- Build a foundation that can absorb AI-assisted writing features in V2 without a rewrite.

**Product goals**
- Make creating and organizing scripts across multiple projects effortless.
- Make real-time collaborative editing feel as reliable as Google Docs.
- Give teams role-based access (Owner / Editor / Viewer) instead of blunt sharing links.
- Centralize feedback via inline comments, mentions, and resolution tracking.
- Preserve full script history with the ability to compare and restore versions.

## 4. Target Users & Personas

| Persona | Who they are | Primary need |
|---|---|---|
| **Producer / Director** | Owns the project, manages the team | Oversight: project status, team activity, control over access |
| **Writer** | Writes and revises scripts | A distraction-free, screenplay-aware editor with autosave |
| **Assistant Director / Coordinator** | Coordinates logistics, reviews drafts | Comment, track revisions, no accidental edit risk |
| **Content Creator / YouTuber** | Solo or small team, faster iteration cycles | Lightweight project structure, quick script turnaround |
| **Agency / Studio Admin** | Manages multiple clients and teams | Workspace-level organization, member management across projects |

## 5. Scope

### 5.1 In Scope — V1 (MVP)
- Authentication (register, login, logout, forgot/reset password, email verification, JWT + refresh tokens)
- Dashboard (projects, recent activity, recently opened scripts, team, notifications)
- Project management (create/edit/delete/archive, invite/remove members, role management)
- Roles: Owner, Editor, Viewer
- Script management (create, delete, rename, duplicate, move, organize)
- Rich text / screenplay-aware editor (Tiptap-based) with autosave, no manual save button
- Real-time collaborative editing (live cursors, presence, typing indicators, conflict-free sync)
- Comments (highlight, reply, resolve, @mentions)
- Global search (projects, scripts, titles, content)
- Notifications (invite, mention, comment, permission change)
- Activity timeline per project
- Version history (view, restore, compare)
- Export (PDF, DOCX, TXT)
- User profile (name, avatar, password, theme, preferences)

### 5.2 Out of Scope — V1
- AI-assisted writing features (see Section 10, planned for V2)
- Native mobile apps (V1 is responsive web only)
- Offline editing mode
- Billing/subscription UI (architecture should anticipate it; not built in V1)
- Public script sharing / publishing

## 6. User Stories (representative sample)

**Authentication**
- As a new user, I can register with email/password and verify my email before accessing the workspace.
- As a user, I can reset my password via a time-limited email link.

**Projects**
- As an Owner, I can create a project and invite teammates with a specific role.
- As an Owner, I can archive a project without deleting its scripts.

**Scripts & Editor**
- As a Writer, I can create a new script inside a project and start typing immediately, with changes saved automatically.
- As a Writer, I can see my collaborators' cursors and edits appear live as they type.

**Comments**
- As a Reviewer, I can select a line of dialogue and leave a comment that notifies the author.
- As a Writer, I can resolve a comment once I've addressed it.

**Version History**
- As an Owner, I can compare two versions of a script and restore an earlier one if needed.

**Search**
- As any user, I can search across all my projects and scripts by title or content and jump directly to a result.

## 7. Success Metrics (KPIs)

- **Activation:** % of invited users who complete onboarding and open a script within 24 hours.
- **Collaboration engagement:** average number of concurrent editors per active script session.
- **Retention:** % of projects with script activity in the last 7 / 30 days.
- **Comment resolution rate:** % of comments resolved within a project's active lifecycle.
- **Export usage:** exports per active project (signal of scripts reaching production-ready state).

## 8. Assumptions & Dependencies

- Teams are small-to-mid-sized (a handful to a few dozen members per project) for V1 scale targets.
- Users have modern browsers; no legacy browser support required.
- Third-party dependencies: transactional email provider (verification/reset emails), file storage provider (avatars, exports), Postgres-compatible hosting (Neon).

## 9. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Real-time collaboration is harder than it looks (conflict resolution) | Use a CRDT-based sync engine (Yjs) via a dedicated service rather than building custom conflict resolution — see Architecture doc |
| Scope creep before V1 ships | Freeze V1 scope to Section 5.1; track everything else as V1.1/V2 |
| Client/friend relationship blurring scope boundaries | Document scope and change requests in writing, even informally |
| Screenplay-specific formatting adds unplanned editor complexity | Ship V1 with generic rich text first; treat screenplay-element formatting as a fast-follow enhancement to the editor, not a blocker |

## 10. Future Scope — V2 (AI Features)

Architecture must remain modular enough to add these without major refactoring:

AI Script Writer · Dialogue Improvement · Grammar Correction · Scene Summarizer · Character Generator · Story Outline Generator · Plot Hole Detection · Character Consistency Checker · Story Expansion · Script Review · AI Director Suggestions · Shooting Schedule Generator

## 11. Release Phasing (no fixed dates — sequence only)

1. **Phase 1 — Foundation:** Auth, Projects, Roles, basic Script CRUD, editor without real-time collab.
2. **Phase 2 — Collaboration:** Real-time sync (Yjs/Hocuspocus), presence, comments, mentions.
3. **Phase 3 — Workspace intelligence:** Search, notifications, activity timeline.
4. **Phase 4 — History & handoff:** Version history, PDF/DOCX/TXT export.
5. **Phase 5 (V2) — AI:** AI-assisted writing modules.

## 12. Glossary

- **Script** — a single writable document within a Project.
- **Project** — a container for one or more Scripts and its team.
- **Workspace/Organization** — recommended top-level container for teams running multiple Projects (see Architecture doc).
- **Presence** — real-time indication of who is currently viewing/editing a Script.
