# EventHub All-Plus Upgrade & Operations Guide

This branch contains the review checklist and implementation requirements for the DEEPOTSAV 2026 EventHub upgrade. It is documentation only: it does **not** deploy code, change Botkeep, or modify the production database.

## Safety rules before any upgrade
- [ ] Back up the current Botkeep application files and the complete EventHub database directory.
- [ ] Confirm the exact Botkeep startup command, working directory, and Python entry-point filename.
- [ ] Preserve every existing guest, pending registration, QR token, event, volunteer, permission, checkpoint, announcement, audit record, and Sheets outbox item.
- [ ] Preserve all environment variables and secrets. Never commit tokens, API keys, database files, environment files, or Sheets secrets to GitHub.
- [ ] Do not run database reset, destructive migrations, bulk QR regeneration, or bulk pass sending.
- [ ] Deploy to the existing Botkeep service; do not run a second Telegram polling process with the same bot token.
- [ ] Keep the frontend URL and backend public URL aligned with the current deployment settings.

## All-Plus review checklist

### 1. Guest registration and event isolation
- [ ] Each event has its own registration state and configuration.
- [ ] A guest who has registered for an event cannot register again for that same event.
- [ ] Required fields and event-specific form settings are validated server-side.
- [ ] Phone number remains required; food options remain Vegetarian and Non-vegetarian.
- [ ] Hostel guests provide hostel and room details; apartment guests provide apartment details without a room-number requirement.
- [ ] Admin approval, rejection, revocation, and reissue actions are audited.

### 2. QR passes and entry control
- [ ] Existing QR tokens remain valid after a non-destructive upgrade.
- [ ] QR preview, download, reissue, revoke, and reset are tested with a dedicated test guest only.
- [ ] Entry and food/checkpoint scans reject duplicate use and show a clear status.
- [ ] Scanner handles camera permission denial, repeated decode callbacks, navigation away during startup, and camera stop/clear safely.
- [ ] Test on a real Android phone and desktop browser before event-day use.

### 3. Admin and volunteer tools
- [ ] Admin-only controls are protected by backend authorization, not merely hidden in the UI.
- [ ] Volunteer permissions are scoped to their assigned event/checkpoints.
- [ ] Guest search, approval queue, QR actions, announcements, event settings, reports, backup, and audit log are checked.
- [ ] Mobile scrolling and dashboard loading are tested on a normal mobile connection.

### 4. Google Sheets synchronization
- [ ] Verify the configured Apps Script URL and shared secret on the server without exposing either value.
- [ ] Confirm failed outbox items retry and successful items are marked delivered.
- [ ] Confirm updates are idempotent (retries do not create duplicate guest rows).
- [ ] Confirm timestamps use the intended event timezone (Kazan: Europe/Moscow).
- [ ] Test with one controlled test registration and verify the matching row in Sheets.

### 5. Hosting and reliability
- [ ] Check the health endpoint after deployment; expected service and database status should be healthy.
- [ ] Monitor Botkeep memory, CPU, storage, response latency, and application logs.
- [ ] Test registration, admin dashboard, QR generation, scanning, and Sheets retry under a small controlled load.
- [ ] Keep a known-good rollback copy of the previous application source.
- [ ] Do not increase the hosting plan unless measured resource use or sustained latency justifies it.

## Food count and cooking report — required upgrade

The food report must calculate the **full approved guest list**, not just the latest page or latest 50 records.

### Required count rules
- [ ] Count only guests with approved/active registration for the selected event.
- [ ] Exclude pending, rejected, and revoked registrations.
- [ ] Count Vegetarian and Non-vegetarian separately using the stored food preference.
- [ ] Include a total approved guest count and a reconciliation check: Vegetarian + Non-vegetarian = guests with a valid food preference.
- [ ] Show guests with missing/invalid food preference separately; never silently classify them.
- [ ] Avoid duplicate counting when the same guest is updated or when Sheets sync retries.
- [ ] Allow an admin to select an event and refresh the report.
- [ ] Show the report's last-updated time and clearly label whether counts are live or cached.
- [ ] Provide CSV export and a printer-friendly cooking summary.
- [ ] Keep food preference editing subject to the existing admin permissions and audit log.

### Suggested report layout

| Event | Approved total | Vegetarian | Non-vegetarian | Missing preference |
|---|---:|---:|---:|---:|
| Selected event | Live count | Live count | Live count | Live count |

The backend should calculate these aggregates from the authoritative event database. The frontend should not estimate totals from a paginated guest list or a limited API response.

### Historical count note — not a live cooking total

A prior screenshot review on 27 October 2026 showed **19 Vegetarian and 31 Non-vegetarian among the latest 50 records only**. At that time, the reported approved total was 183. The 19/31 split must **not** be treated as the split for all 183 approved guests. Obtain a fresh full database-backed report before purchasing ingredients or finalizing quantities.

## Safe deployment sequence
1. Review this checklist and confirm the current production configuration.
2. Back up source and the entire database directory.
3. Review backend and frontend changes in a separate branch/pull request.
4. Run syntax checks and isolated tests against a temporary database copy.
5. Verify migrations are additive and preserve existing rows and QR tokens.
6. Deploy during a controlled window to the existing Botkeep service.
7. Check health endpoint, admin access, volunteer access, one test QR, and one test Sheets sync.
8. Verify the full-event food counts against the database.
9. Keep the previous source and database backup available for rollback.

## Deployment configuration checklist (do not paste secrets here)

Record only whether each setting is present and correct; do not store its value in this repository.
- [ ] Telegram bot token configured in Botkeep environment
- [ ] Admin IDs configured
- [ ] Database path and event database directory confirmed
- [ ] Public HTTPS API origin configured
- [ ] Telegram Mini App URL configured
- [ ] Google Sheets sync URL configured
- [ ] Google Sheets shared secret configured
- [ ] Port and startup command confirmed

## Current verification status

This document is a review plan, not a declaration that production is upgraded. Live Botkeep deployment, live Google Sheets delivery, Telegram polling, and physical-device camera scanning must be tested in the actual environment. Do not mark a checklist item complete until it has been verified.
