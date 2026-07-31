# Software Requirements Specification (SRS)

**Product:** Scriptora
**Version:** 1.0 (Draft)
**Date:** July 2026
**Prepared by:** Rutuja Deshmukh

---

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for Scriptora V1, a collaborative script-writing and project-management SaaS platform. It is intended for engineering use during design and implementation.

### 1.2 Scope
Scriptora provides authentication, project/team management, script creation and organization, a real-time collaborative rich-text editor, commenting, search, notifications, activity tracking, version history, and export. See the PRD for product rationale; this document specifies *how* the system must behave.

### 1.3 Definitions & Acronyms
- **FR** — Functional Requirement
- **NFR** — Non-Functional Requirement
- **CRDT** — Conflict-free Replicated Data Type (used for real-time sync)
- **RBAC** — Role-Based Access Control
- **JWT** — JSON Web Token

### 1.4 References
Scriptora PRD v1.0; Scriptora Architecture Document v1.0.

### 1.5 Overview
Section 2 describes the product at a high level; Section 3 lists functional requirements by module; Section 4 covers external interfaces; Section 5 covers non-functional requirements; Sections 6–8 summarize architecture, data, and other requirements (detailed further in the Architecture document).

---

## 2. Overall Description

### 2.1 Product Perspective
Scriptora is a new, standalone web SaaS product. It consists of a Next.js frontend, a FastAPI backend for business logic, a dedicated real-time collaboration service (Yjs/Hocuspocus) for concurrent editing, PostgreSQL for persistence, and Redis for caching/pub-sub.

### 2.2 Product Functions (summary)
Authentication · Project & team management · Role-based access · Script CRUD & organization · Real-time collaborative editing · Commenting & mentions · Global search · Notifications · Activity timeline · Version history · Document export · User profile management.

### 2.3 User Classes and Characteristics
- **Owner** — full control over a project: members, roles, scripts, settings.
- **Editor** — can create/edit scripts and comment; cannot manage members or delete the project.
- **Viewer** — read-only access plus commenting (per PRD; confirm during design whether Viewers can comment or are strictly read-only).
- **Unauthenticated visitor** — can only access public marketing pages, register, or log in.

### 2.4 Operating Environment
Modern evergreen browsers (Chrome, Firefox, Safari, Edge) on desktop and mobile viewports. No native app requirement for V1. Backend runs on Linux containers (Railway/Fly.io).

### 2.5 Design & Implementation Constraints
- Frontend: Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui, Tiptap.
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic.
- Database: PostgreSQL (Neon).
- Real-time sync must use a CRDT-based approach (Yjs) rather than custom operational-transform logic.
- Auth must use JWT access tokens with a refresh-token rotation strategy.

### 2.6 Assumptions & Dependencies
Third-party transactional email service is available for verification/reset emails. File storage provider (Supabase Storage or Cloudinary) is available for avatars and export artifacts.

---

## 3. System Features (Functional Requirements)

### 3.1 Authentication (FR-AUTH)
- **FR-AUTH-01**: The system shall allow a user to register with name, email, and password.
- **FR-AUTH-02**: The system shall send an email verification link on registration; unverified accounts shall have restricted access.
- **FR-AUTH-03**: The system shall allow login via email/password, issuing a short-lived JWT access token and a rotating refresh token.
- **FR-AUTH-04**: The system shall allow logout, invalidating the current refresh token.
- **FR-AUTH-05**: The system shall support "forgot password" via a time-limited, single-use reset link.
- **FR-AUTH-06**: The system shall rate-limit login and password-reset attempts.

### 3.2 Dashboard (FR-DASH)
- **FR-DASH-01**: The system shall display the user's projects, recently opened scripts, recent activity, and unread notifications on login.

### 3.3 Project Management (FR-PROJ)
- **FR-PROJ-01**: An Owner shall be able to create, edit, delete, and archive a project.
- **FR-PROJ-02**: An Owner shall be able to invite members by email with an assigned role.
- **FR-PROJ-03**: An Owner shall be able to remove members and change member roles.
- **FR-PROJ-04**: Archived projects shall remain read-accessible but not editable until restored.

### 3.4 Roles & Permissions (FR-ROLE)
- **FR-ROLE-01**: The system shall enforce three project roles — Owner (full access), Editor (edit scripts, add comments), Viewer (read-only).
- **FR-ROLE-02**: All write operations shall be authorized server-side against the user's role for the relevant project, not only hidden in the UI.

### 3.5 Script Management (FR-SCRIPT)
- **FR-SCRIPT-01**: An Editor or Owner shall be able to create, rename, duplicate, move, and delete scripts within a project.
- **FR-SCRIPT-02**: Deleted scripts shall be recoverable from a trash state for a defined retention window before permanent deletion.

### 3.6 Rich Text Editor (FR-EDIT)
- **FR-EDIT-01**: The editor shall support bold, italic, underline, strike, font size/family, text color, highlight, alignment, headings, ordered/unordered/checklists, block quotes, horizontal rule, tables, links, images, and undo/redo.
- **FR-EDIT-02**: The editor shall support standard keyboard shortcuts for common formatting actions.
- **FR-EDIT-03**: The editor shall render correctly on both desktop and mobile viewports.

### 3.7 Autosave (FR-SAVE)
- **FR-SAVE-01**: All content changes shall be persisted automatically without a manual save action, with visible save-status feedback to the user.

### 3.8 Real-Time Collaboration (FR-COLLAB)
- **FR-COLLAB-01**: Multiple users shall be able to edit the same script concurrently with changes merged without data loss (CRDT-based conflict resolution).
- **FR-COLLAB-02**: The system shall display live cursor positions and presence (who is currently viewing/editing) for a script.
- **FR-COLLAB-03**: The system shall display typing indicators for active collaborators.
- **FR-COLLAB-04**: Editing sessions shall recover gracefully from a dropped connection, resyncing without duplicating or losing content.

### 3.9 Comments (FR-COMM)
- **FR-COMM-01**: A user with comment permission shall be able to highlight text and attach a comment.
- **FR-COMM-02**: Users shall be able to reply to a comment thread and resolve it.
- **FR-COMM-03**: Users shall be able to @mention a project member in a comment, triggering a notification.

### 3.10 Search (FR-SEARCH)
- **FR-SEARCH-01**: The system shall provide a global search across the user's accessible projects, scripts, titles, and content.
- **FR-SEARCH-02**: Search results shall respect the user's project-level permissions.

### 3.11 Notifications (FR-NOTIF)
- **FR-NOTIF-01**: The system shall notify a user when invited to a project, mentioned, commented on, or when their role changes.
- **FR-NOTIF-02**: Notifications shall be viewable in-app with a read/unread state.

### 3.12 Activity Timeline (FR-ACT)
- **FR-ACT-01**: The system shall maintain a per-project activity feed recording project creation, script edits, member joins, comments, and role updates.

### 3.13 Version History (FR-VER)
- **FR-VER-01**: The system shall retain script version snapshots at a defined cadence and on significant edits.
- **FR-VER-02**: Users with appropriate permission shall be able to view, compare, and restore prior versions.

### 3.14 Export (FR-EXP)
- **FR-EXP-01**: The system shall support exporting a script to PDF, DOCX, and plain text.

### 3.15 User Profile (FR-PROF)
- **FR-PROF-01**: A user shall be able to update their name, avatar, password, theme, and preferences.

---

## 4. External Interface Requirements

### 4.1 User Interfaces
Responsive web UI supporting desktop and mobile breakpoints; light and dark themes; accessibility-conscious component design (keyboard navigation, sufficient contrast, ARIA labeling via shadcn/ui primitives).

### 4.2 Hardware Interfaces
None (web-based SaaS).

### 4.3 Software Interfaces
- Transactional email provider (verification, password reset, notification digests).
- File storage provider (Supabase Storage or Cloudinary) for avatars and generated export files.
- PDF/DOCX generation libraries invoked server-side for export.

### 4.4 Communication Interfaces
- REST/HTTPS for standard API operations (`/api/v1/*`).
- WebSocket connections for real-time collaboration, served by a dedicated collaboration service.

---

## 5. Non-Functional Requirements

### 5.1 Performance
Editor input latency should feel instantaneous locally (optimistic local updates) regardless of network round-trip; API responses for standard CRUD operations should complete within normal web-application latency budgets under expected load.

### 5.2 Security
Passwords hashed with a modern algorithm (Argon2/bcrypt); JWT access tokens short-lived; refresh tokens rotated and revocable; all authorization checks enforced server-side; input validated via Pydantic schemas; rate limiting on authentication endpoints; HTTPS enforced everywhere.

### 5.3 Reliability & Availability
Autosave and real-time sync must not lose user input on connection drops. Database backups must be enabled at the hosting provider level.

### 5.4 Scalability
The system shall support horizontal scaling of the API and collaboration services independently; WebSocket/presence state shall not depend on in-process memory alone (Redis-backed) once multiple instances are running.

### 5.5 Usability & Accessibility
Interface shall follow accessibility-first design principles (keyboard operability, screen-reader-friendly markup, adequate color contrast in both themes).

### 5.6 Maintainability
Backend organized into clearly separated routers, services, repositories, models, and schemas; frontend organized into components, features, hooks, services, and types, per the Architecture document.

### 5.7 Portability
Containerized backend services deployable to any compatible host (Railway, Fly.io, or equivalent); no vendor-specific lock-in beyond managed Postgres and storage.

---

## 6. System Architecture Overview
See the accompanying Architecture document for the full system diagram, folder structure, database schema, and real-time collaboration design.

## 7. Data Requirements
Core entities: User, Organization, OrganizationMember, Project, ProjectMember, Invitation, Script, ScriptVersion, Comment, CommentReply, Notification, ActivityLog, RefreshToken. Full entity-relationship diagram in the Architecture document.

## 8. Other Requirements
Terms of Service, Privacy Policy, and data retention/deletion policy should be defined before public launch; not a technical requirement of this document but a launch dependency.
