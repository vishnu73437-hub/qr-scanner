# EventHub 2.0 — Implementation Plan and Safety Gates

Prepared: 4 November 2026  
Repository: https://github.com/vishnu73437-hub/qr-scanner  
Working branch: `eventhub-2.0-staging-2026-11-04`  
Production branch: `main` (must remain untouched until staging checks and operator approval)

## Product direction

A professional, clean, responsive event operations dashboard. Keep event branding configurable; avoid unnecessary animation, crowded controls, and technical settings in the primary workflow.

## Non-negotiable data-safety rules

1. Do not reset, replace, migrate destructively, or reinitialize the production SQLite database.
2. Preserve all guest and pending-registration rows, primary IDs, pass codes, QR tokens, approval/revocation states, entry/food flags and timestamps.
3. Preserve events, event-specific databases, registration schemas, volunteers, admins, checkpoints, announcements, audit history, backups and Sheets outbox/queue.
4. Do not regenerate QR credentials during UI or renderer changes.
5. Do not bulk-refresh or send passes without an approved preview and explicit operator action.
6. Do not change Botkeep secrets, environment variables, startup command, database paths or polling process count.
7. Any schema change must be additive, versioned, backed up, tested against a copy and have a rollback path.
8. Never include tokens, secrets, guest PII, database files or production logs in Git.

## Implementation status — 4 November 2026

- **Staging frontend:** admin dashboard refresh and read-only Botkeep / database status card completed; scanner camera is released when the app is backgrounded; `index.html` and `eventhub-preview.html` are synchronized.
- **Frontend static checks:** inline application script parses successfully; 216 literal element lookups were matched to existing static HTML IDs; no missing literal IDs were found.
- **Backend candidate:** `EventHub_Canva_Backend_Upgrade_20261104.zip` includes the pass-layout renderer and bounded SQLite lock-handling changes. Its standard `python -m unittest discover -s tests -v` suite passes four test groups, including seven isolated regression assertions.
- **Not yet verified:** no live Botkeep install/restart, production DB backup verification, Telegram polling test, Google Sheets live test, or real Android / iPhone / tablet / desktop browser acceptance test has been performed in this work session.
- **Production protection:** GitHub `main` and the live Botkeep process have not been changed. Do not treat the staging branch or backend ZIP as deployed.

## Rollout strategy

### Stage 0 — Baseline and protection
- Record current production entrypoint, working directory, database locations, environment variable names and startup command.
- Download and validate source and database backups; test that a backup can be opened.
- Capture baseline counts for events, guests, pending registrations, volunteers, admins and outbox rows without exposing PII.
- Confirm the current main-branch SHA and keep production unchanged.

**Gate:** no backend deployment until the backup is verified and the operator confirms Botkeep configuration.

### Stage 1 — Professional admin experience (frontend-only)
- Improve dashboard hierarchy, spacing, typography, responsive statistic cards, event-day action area and navigation focus states.
- Keep the existing admin API actions and event-scoped page routing.
- Keep guest and volunteer views outside admin-only styling.
- Do not alter registration, QR validation, entry, food or checkpoint behavior.

**Current staging work:** admin-only visual polish and a read-only Botkeep service-health card have been added to `eventhub-preview.html`. The health card checks `GET /health`, reports API / primary registry state and response time, and has a manual retry; it does not access guest data or mutate records. The root `index.html` is byte-for-byte synchronized with it. Inline application JavaScript syntax and static ID references have been checked. This is not deployed to GitHub Pages production.

### Stage 2 — Event command centre
- Display event-scoped approved, checked-in, food-served and volunteer totals.
- Add clear API freshness/error states and last-refresh time.
- Use existing read-only statistics first; do not add new write endpoints for dashboard cards.
- Add operational warnings for pending approvals, missing food preference and Sheets sync backlog only when the API supplies reliable data.

**Gate:** compare displayed counts with direct read-only backend counts on a database copy and a controlled test event.

### Stage 3 — Guest operations
- Improve search, status filters, guest detail view and action confirmations.
- Preserve existing guest primary keys and QR tokens when editing non-credential fields.
- Make revoke, reissue and reset actions explicit, permission checked and auditable.
- Keep destructive or credential-changing actions out of bulk operations.

**Gate:** tests prove the same guest ID, pass code and QR token remain unchanged for ordinary edits.

### Stage 4 — Scanner and volunteer workflow
- Improve camera start/stop lifecycle, permission-denied recovery, scan feedback and duplicate-scan messaging.
- Keep server-side QR validation authoritative; client-side UI must not decide entry validity.
- Enforce volunteer permissions server-side for each event and checkpoint.
- Test Android Chrome and iOS Safari with a dedicated test guest.

**Gate:** test valid, invalid, revoked, already-used, wrong-event and network-timeout cases without touching real guest records.

### Stage 5 — Food, checkpoints and volunteer operations
- Make food collection availability event-configurable.
- Keep vegetarian/non-vegetarian totals derived from all approved guests, not a paginated UI list.
- Improve checkpoint and volunteer assignment summaries.
- Preserve scan records and audit timestamps; no automatic reset at event boundaries.

**Gate:** compare all totals and checkpoint history with source DB copies.

### Stage 6 — Announcements, reports and maintenance
- Add safe preview-before-send for announcements, with audience and event confirmation.
- Add CSV exports with explicit event and date scope.
- Add backup status, health checks, queue visibility and redacted error details.
- Never expose secrets or guest phone numbers in public dashboards or diagnostic logs.

**Gate:** preview, permissions, export scope and redaction tests pass.

### Stage 7 — Reusable multi-event EventHub
- Add event templates and event-specific registration schemas/branding.
- Keep Halloween, DEEPOTSAV and future events isolated by event ID and database boundaries.
- Add archive/read-only behavior and configurable lifecycle states.
- Make any schema evolution additive and reversible.

**Gate:** cross-event isolation tests prove that guest lists, passes, settings and scanner events never leak between events.

## Test matrix

- Existing guest records and pending registrations are preserved.
- Existing pass codes and QR tokens are unchanged.
- Existing entry/food usage flags and timestamps are unchanged.
- Registration still requires full name and phone; food options remain Vegetarian / Non-vegetarian.
- Hostel guests retain hostel and room fields; apartment guests do not require a room number.
- Admin and volunteer authorization is enforced server-side.
- QR scans remain event-scoped and idempotent.
- Sheets sync retains its current URL/secret configuration and retry queue.
- Mobile and desktop layouts are usable.
- API timeout and lock failures produce actionable messages and do not cause duplicate writes.
- Frontend JavaScript parses and both HTML entry files are identical.
- GitHub Pages build succeeds before production frontend promotion.
- Backend smoke tests pass on a copied database before Botkeep replacement.

## Promotion and rollback

- Work only on the staging branch until tests and review are complete.
- Promote frontend changes to `main` only after preview review and a successful build.
- Promote backend only after source + DB backups are verified, Botkeep paths/configuration are confirmed, and a maintenance window is agreed.
- Replace only the configured source entrypoint; never overwrite production DBs or `.env`.
- Restart the existing Botkeep process only; never launch a second polling process with the same Telegram token.
- If health checks fail, restore the previous source and investigate before retrying.
- No live deployment is implied by a staging commit or a GitHub Pages build.

## Current status

- [x] Separate staging branch created from the recorded main commit.
- [x] Admin-only professional visual styling added to staging preview.
- [ ] Synchronize staging `index.html` with `eventhub-preview.html`.
- [ ] Review all existing admin, guest and volunteer flows on staging.
- [ ] Add focused UI tests and run the frontend build.
- [ ] Verify production source/database backup and Botkeep configuration.
- [ ] Backend deployment and live smoke tests — pending.
- [ ] Production promotion — pending explicit review.

## Device-friendly requirement — applies to every phase

The interface must work comfortably on:
- Android phones (including smaller screens and Telegram's in-app browser).
- iPhone / iOS Safari and Telegram's in-app browser.
- iPad and Android tablets, in portrait and landscape.
- Windows, macOS and Linux desktop browsers.

### Responsive behavior and accessibility
- Mobile-first layout with no page-level horizontal scrolling at 320 CSS pixels and above.
- Use fluid widths and responsive grids; collapse multi-column dashboards and forms into one column on phones.
- Convert wide data tables into readable stacked cards or provide a clearly labelled, contained horizontal scroll region.
- Keep primary actions visible and easy to reach; use touch targets of at least 44 × 44 CSS pixels where practical.
- Inputs must remain usable when the mobile keyboard opens; labels must not rely on placeholders alone.
- Keep scanner controls large, avoid tiny icons, and handle camera permission denial, orientation changes, screen sleep and returning from another app.
- Respect safe-area insets, browser zoom, text scaling and reduced-motion preferences.
- Maintain readable contrast, visible keyboard focus, accessible labels and status messages that do not rely on colour alone.
- Avoid hover-only interactions; every action must work by touch, mouse and keyboard.
- Keep images compressed and correctly sized; lazy-load non-critical images and avoid unnecessary animation or heavy libraries.
- Preserve loading, empty, offline, timeout and retry states so a slow mobile connection does not appear frozen.
- Never put secrets, QR tokens or sensitive guest details into client logs or analytics.

### Device acceptance checklist
- [ ] Android phone, narrow viewport: event selection, registration, My Pass, admin pages and scanner fit without clipped controls.
- [ ] iPhone: same flows work in Safari and Telegram's in-app browser.
- [ ] Tablet portrait and landscape: dashboard adapts without awkward empty columns.
- [ ] Desktop: navigation and data views remain efficient with keyboard and mouse.
- [ ] 320 px viewport: no unintended page-level horizontal overflow.
- [ ] Touch targets, text scaling, browser zoom and mobile keyboard are usable.
- [ ] Camera scanner survives permission denial, rotate, background/foreground and retry.
- [ ] Slow network and API timeout show a clear status and safe retry behavior.
