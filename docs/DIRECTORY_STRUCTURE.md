# Scriptora — Complete Directory Structure

This is the full, file-level scaffold for all three apps. It supersedes the high-level view in `ARCHITECTURE.md` §2 with actual filenames so the repo can be scaffolded directly from this document. Files marked `(P2)` belong to the Phase 2+ feature set (see `ROADMAP.md`) — create the folder now, fill in during that phase.

```
scriptora/
├── apps/
│   ├── web/
│   ├── api/
│   └── collaboration/          # (P2)
├── docs/
│   ├── PRD.md
│   ├── SRS.md
│   ├── ARCHITECTURE.md
│   ├── DIRECTORY_STRUCTURE.md
│   └── ROADMAP.md
├── .github/workflows/
│   ├── ci-web.yml
│   └── ci-api.yml
├── README.md
└── .gitignore
```

---

## `apps/web/` — Next.js Frontend

```
apps/web/
├── app/
│   ├── (auth)/
│   │   ├── layout.tsx
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   ├── reset-password/page.tsx
│   │   └── verify-email/page.tsx              # (P2 — email verification)
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── dashboard/page.tsx
│   │   ├── projects/
│   │   │   ├── page.tsx                        # project list
│   │   │   ├── new/page.tsx
│   │   │   └── [projectId]/
│   │   │       ├── page.tsx                     # project overview
│   │   │       ├── settings/page.tsx
│   │   │       ├── members/page.tsx
│   │   │       ├── activity/page.tsx            # (P2 full timeline; day-3 shows basic log)
│   │   │       └── scripts/
│   │   │           ├── page.tsx                 # script list
│   │   │           └── [scriptId]/page.tsx      # script editor
│   │   ├── search/page.tsx                       # (P2)
│   │   ├── notifications/page.tsx
│   │   └── profile/page.tsx
│   ├── layout.tsx
│   ├── globals.css
│   └── providers.tsx                             # theme, auth, query client providers
│
├── components/
│   ├── ui/                                        # shadcn/ui primitives (button, dialog, dropdown-menu, input, avatar, badge, toast, tabs, etc.)
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Topbar.tsx
│   │   └── AppShell.tsx
│   └── common/
│       ├── Avatar.tsx
│       ├── EmptyState.tsx
│       ├── LoadingSpinner.tsx
│       └── ConfirmDialog.tsx
│
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   ├── ForgotPasswordForm.tsx
│   │   │   └── ResetPasswordForm.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useLogin.ts
│   │   │   └── useRegister.ts
│   │   └── api.ts
│   │
│   ├── projects/
│   │   ├── components/
│   │   │   ├── ProjectCard.tsx
│   │   │   ├── ProjectForm.tsx
│   │   │   ├── MemberList.tsx
│   │   │   ├── InviteMemberDialog.tsx
│   │   │   └── RoleBadge.tsx
│   │   ├── hooks/
│   │   │   ├── useProjects.ts
│   │   │   └── useProjectMembers.ts
│   │   └── api.ts
│   │
│   ├── scripts/
│   │   ├── components/
│   │   │   ├── ScriptCard.tsx
│   │   │   ├── ScriptList.tsx
│   │   │   ├── NewScriptDialog.tsx
│   │   │   └── ScriptSidebarTree.tsx
│   │   ├── hooks/
│   │   │   ├── useScripts.ts
│   │   │   └── useScriptActions.ts
│   │   └── api.ts
│   │
│   ├── editor/
│   │   ├── components/
│   │   │   ├── Editor.tsx
│   │   │   ├── EditorToolbar.tsx
│   │   │   ├── PresenceAvatars.tsx              # day-3: simple "viewing now" list
│   │   │   └── CollaborationCursor.tsx           # (P2 — true live cursors via Yjs)
│   │   ├── extensions/                             # (P2 — screenplay-aware Tiptap nodes)
│   │   │   ├── sceneHeading.ts
│   │   │   └── characterBlock.ts
│   │   ├── hooks/
│   │   │   ├── useAutosave.ts                      # day-3: debounced REST PUT
│   │   │   └── useCollaboration.ts                  # (P2 — swaps in Yjs/Hocuspocus)
│   │   └── utils/
│   │       ├── exportToPdf.ts
│   │       ├── exportToDocx.ts                       # (P2)
│   │       └── exportToTxt.ts                         # (P2)
│   │
│   ├── comments/
│   │   ├── components/
│   │   │   ├── CommentThread.tsx
│   │   │   ├── CommentComposer.tsx
│   │   │   └── CommentMarker.tsx
│   │   ├── hooks/useComments.ts
│   │   └── api.ts
│   │
│   ├── notifications/
│   │   ├── components/
│   │   │   ├── NotificationList.tsx
│   │   │   └── NotificationItem.tsx
│   │   ├── hooks/useNotifications.ts
│   │   └── api.ts
│   │
│   ├── search/                                        # (P2)
│   │   ├── components/
│   │   │   ├── SearchBar.tsx
│   │   │   └── SearchResults.tsx
│   │   └── api.ts
│   │
│   ├── activity/
│   │   ├── components/
│   │   │   ├── ActivityFeed.tsx
│   │   │   └── ActivityItem.tsx
│   │   └── api.ts
│   │
│   ├── versions/                                       # (P2)
│   │   ├── components/
│   │   │   ├── VersionHistoryPanel.tsx
│   │   │   └── VersionDiffView.tsx
│   │   └── api.ts
│   │
│   └── profile/
│       ├── components/
│       │   ├── ProfileForm.tsx
│       │   └── ThemeToggle.tsx
│       └── api.ts
│
├── hooks/
│   ├── useDebounce.ts
│   ├── useMediaQuery.ts
│   └── useOnlineStatus.ts
├── services/
│   ├── http.ts                                          # fetch/axios instance, interceptors
│   └── websocket.ts                                       # (P2)
├── store/
│   ├── authStore.ts
│   ├── uiStore.ts
│   └── presenceStore.ts
├── lib/
│   ├── utils.ts
│   ├── formatDate.ts
│   └── permissions.ts                                       # client-side role gating (UI only — never trusted alone)
├── constants/
│   ├── roles.ts
│   └── routes.ts
├── types/
│   ├── user.ts
│   ├── project.ts
│   ├── script.ts
│   ├── comment.ts
│   └── notification.ts
├── middleware.ts
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── .env.example
```

---

## `apps/api/` — FastAPI Backend

```
apps/api/
├── app/
│   ├── main.py                          # app instance, router registration, CORS, startup events
│   ├── core/
│   │   ├── config.py                      # Pydantic Settings (env vars)
│   │   ├── security.py                     # password hashing, JWT encode/decode
│   │   └── logging.py
│   ├── middleware/
│   │   ├── auth_middleware.py
│   │   ├── error_handler.py
│   │   └── rate_limiter.py
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── users_router.py
│   │   ├── projects_router.py
│   │   ├── scripts_router.py
│   │   ├── comments_router.py
│   │   ├── notifications_router.py
│   │   ├── activity_router.py
│   │   ├── search_router.py                 # (P2)
│   │   └── export_router.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── script_service.py
│   │   ├── comment_service.py
│   │   ├── notification_service.py
│   │   ├── activity_service.py
│   │   ├── search_service.py                 # (P2)
│   │   └── export_service.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── script_repository.py
│   │   ├── comment_repository.py
│   │   └── notification_repository.py
│   ├── models/
│   │   ├── user.py
│   │   ├── organization.py                     # table created day-1; UI deferred
│   │   ├── project.py
│   │   ├── script.py
│   │   ├── script_version.py                     # (P2 UI; table exists day-1)
│   │   ├── comment.py
│   │   ├── notification.py
│   │   ├── activity_log.py
│   │   └── refresh_token.py
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── project_schema.py
│   │   ├── script_schema.py
│   │   ├── comment_schema.py
│   │   └── notification_schema.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   └── utils/
│       ├── email.py                              # (P2 — transactional email)
│       ├── pdf_export.py
│       ├── docx_export.py                          # (P2)
│       └── permissions.py                           # server-side role enforcement — the real gate
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── test_auth.py
│   ├── test_projects.py
│   └── test_scripts.py
├── requirements.txt
├── alembic.ini
└── .env.example
```

---

## `apps/collaboration/` — Real-Time Service (P2)

Scaffold the folder now so the day-3 build can drop it in without restructuring later; implementation happens in Phase 2.

```
apps/collaboration/
├── src/
│   ├── server.ts                # Hocuspocus bootstrap
│   ├── auth.ts                   # onAuthenticate — validates JWT against FastAPI
│   ├── persistence.ts              # onStoreDocument / onLoadDocument — Postgres read/write
│   ├── awareness.ts                 # presence/cursor broadcast
│   └── config.ts
├── package.json
├── tsconfig.json
└── .env.example
```

---

## Notes on `(P2)` markers

Creating these folders/files as empty placeholders on day 1 costs almost nothing and keeps the 3-day build from having to restructure the repo later — but don't spend day-1/2/3 hours implementing their contents. See `ROADMAP.md` for exactly what's in scope per day.
