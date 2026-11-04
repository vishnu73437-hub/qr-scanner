# EventHub Event-Day Smart Upgrade — revised candidate

## Scope

This staging branch improves EventHub event-day volunteer and admin workflows. It is **not a production deployment**.

## Frontend

- Captures one QR at a time; detection pauses immediately while the camera session remains open.
- Camera and manual pass-code lookup share the same scan lock.
- Keeps a guest selected through the required action and verifies expected state with a fresh backend guest lookup before showing success.
- On timeout, checks backend state before retrying to avoid duplicate entry, food, proof, exit or checkpoint records.
- High-contrast full-screen progress, success and failure dialogs keep errors visible. An uncertain save keeps scanning locked and offers Retry / Check Status.
- Full-scanner/admin/event-lead/entry/proof workflows retain the guest after Entry until proof is stored or No Proof Provided is confirmed. The Entry desk can perform Entry plus proof deposit/no-proof confirmation; the Proof/Exit desk handles proof return and exit.
- Large primary actions, sticky action controls, compact status grid, collapsed help and manual code fallback keep the volunteer workflow on one screen.
- Adds role-specific volunteer home/desk information, assigned stations and recent action summaries.
- Admin-only checkpoint manager creates/edits/enables stations and assigns eligible volunteers by display name.
- An unassigned checkpoint-only volunteer is blocked from both camera and manual scanning by the frontend; failed station-list verification also blocks scanning until Retry access check succeeds. The backend also fails closed.
- index.html and eventhub-preview.html remain byte-for-byte identical.

## Backend candidate (separate Botkeep release ZIP)

The revised backend candidate and isolated tests are packaged separately. It contains additive checkpoint assignment storage, Telegram display-name metadata, name-based volunteer candidate and checkpoint team/assignment actions, and assignment-aware checkpoint permissions. The checkpoint candidate picker includes authorized core/event volunteers but excludes blocked accounts, administrators and ordinary attendees. Core/global volunteers retain their event-wide access; event-scoped checkpoint volunteers are limited to the stations assigned to their account.

**Important strict-access change:** a checkpoint-only role with no assigned enabled station is denied guest lookup, checkpoint listing, volunteer dashboard access and checkpoint scan submission. The previous legacy fallback that silently granted all stations when no assignments existed is removed. Existing checkpoint-role volunteers must be explicitly assigned an enabled station before event-day use.

The revised Botkeep package is 88,305 bytes as a ZIP. Its bot.py is 362,347 bytes (SHA-256 a01244a1f27e3eb3efb795503845ea0aafe64b717777bed9b47c07a118d09ceb); the ZIP SHA-256 is 9361f4880965855578668e134514fe7e2bf8a1e753e084a88fb439f0588a18da. It is based on saved Library source bot(20261104-204816).py, **not a live export from the running Botkeep process**. Do not overwrite the live backend until the exact deployed source is obtained and reconciled.

## Validation

- python -m py_compile bot.py test_staff_roles.py test_checkpoint_assignments.py: passed.
- python test_staff_roles.py: passed all isolated role, action-matrix, dashboard-route and cross-event checks.
- python test_checkpoint_assignments.py: passed helper isolation, duplicate assignment constraint, no-assignment fail-closed checks, exact-station authorization, blocked global candidate exclusion, SQLite query execution, name-picker and active-event chooser checks.
- The frontend GitHub Actions check parses inline JavaScript and verifies index.html / eventhub-preview.html parity. A fresh run is required after the latest frontend commit.

These are source-level, static and isolated SQLite checks. They are not live Botkeep HTTP integration, Telegram authentication, Google Sheets delivery, or physical Android camera/queue tests.

## Safe rollout boundary

- This branch remains separate from production main.
- No Botkeep upload/restart, live database write, token/secret update, guest/pass mutation or Google Sheets action was performed.
- Obtain and compare the exact running Botkeep source; back up the live backend, primary registry DB and complete event-database directory before any backend replacement.
- Deploy the matching frontend and backend as a coordinated release only after live-source reconciliation and a reviewed backup/restore path.
- Test with a dedicated volunteer and test guest: Entry → proof stored / No Proof Provided → Food → proof return → Exit; assigned and unassigned checkpoint access; wrong-station rejection; repeated scans; simulated timeout; Sheets delivery; restore.

## Backend review

See EVENTHUB_BACKEND_CANDIDATE_REVIEW_20261105.md for details. The backend candidate also preserves blocked-delivery state when the Mini App opens and propagates Telegram delivery failures into the shared registry and event DB. It still requires comparison with the exact running Botkeep source and a verified live-database backup before deployment.
