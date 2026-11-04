# EventHub — Upgrade Roadmap

This roadmap is a review checklist, not a claim that every item is implemented or live.

## Priority 0 — Protect production data
- [ ] Verify database backup and restore procedure.
- [ ] Verify exact Botkeep entry point, working directory, and database locations.
- [ ] Preserve all registrations, pending registrations, QR tokens, event settings, volunteers, admins, audit logs, and Sheets outbox.
- [ ] Confirm no secrets or guest personal data are committed to this public repository.

## Priority 1 — Core reliability
- [ ] Confirm single bot process / polling ownership.
- [ ] Verify health endpoint and database connectivity after deployment.
- [ ] Verify registration, approval, QR issuance, QR revocation/reissue, and pass retrieval using test accounts.
- [ ] Verify scanner start/stop/retry and duplicate-scan handling on a physical phone.
- [ ] Verify entry and food checkpoint updates are idempotent and auditable.
- [ ] Verify admin and volunteer authorization on every protected API route.

## Priority 2 — Google Sheets
- [ ] Verify Apps Script deployment URL and access mode.
- [ ] Verify secret equality without exposing either value.
- [ ] Test one controlled guest upsert and confirm the resulting row.
- [ ] Test retry behavior for temporary failures and Unauthorized responses.
- [ ] Confirm timezone handling uses the intended Kazan / Europe-Moscow setting.
- [ ] Confirm duplicate retries do not create duplicate guest rows.

## Priority 3 — Performance and usability
- [ ] Measure Mini App first-load time on mobile data and Wi-Fi.
- [ ] Check scrolling and long-list rendering on Android and desktop.
- [ ] Measure slow admin endpoints with timing logs.
- [ ] Test camera permission denial, camera switch, stop, retry, and navigation away.
- [ ] Run a controlled concurrent-use test without using real guest passes.

## Priority 4 — Operations and maintainability
- [ ] Verify event isolation: Halloween, Diwali, and future events must not leak registrations or announcements into one another.
- [ ] Verify event-specific registration schema and food settings.
- [ ] Verify backup, audit log, announcement, checkpoint, and cleanup functions.
- [ ] Verify volunteer role assignment and removal.
- [ ] Document a rollback procedure and who is authorized to perform it.

## Release gate
Do not call the upgrade complete until all critical checks have been performed on the live Botkeep service and the Mini App has been tested from Telegram on a physical phone. Record test date, test account, result, and any failure without recording secrets or guest personal data.


## 4 November 2026 code follow-up (isolated, not a production release)
- [x] Frontend source: prevent `pass_layout: null` from being sent when the visual editor is closed.
- [x] Frontend source: keep request timeout active through JSON parsing and distinguish uncertain save outcomes.
- [x] Frontend source: guard duplicate settings submissions and separate save success from page-refresh failure.
- [x] Backend candidate: bound `update_event` SQLite waits and preserve a registry audit fallback.
- [x] Offline regression: verify layout retention, QR geometry, locked secondary DB behavior and existing guest-data preservation.
- [ ] Install backend candidate on the existing Botkeep service after backing up source and databases.
- [ ] Verify live health, admin save, guest pass preview, Telegram /mypass, QR scan, and Google Sheets from production test accounts.
