# EventHub Event-Day Smart Upgrade — 5 November 2026

## Scope

This staging branch improves the EventHub event-day volunteer and admin workflows. It is not yet a production deployment.

## Frontend

- Captures one QR at a time and pauses detection immediately after the first decode. The camera session stays open between guests.
- Manual pass-code verification uses the same one-guest lock as camera scans.
- Keeps the guest locked through verification and event-day writes. Before a write it checks the latest guest state; after a write it re-fetches the guest and only shows success when the expected state is visible.
- If a request times out, it checks the guest state before considering a retry. A previously saved action is recognized instead of being submitted blindly again.
- In full-scanner/admin/event-lead workflows, a guest's Entry action is not the end of the scan: if ID proof remains unresolved, the same guest stays selected until the proof is stored or an explicit No Proof Provided record is confirmed. Dedicated Entry-only volunteers can complete their entry task and hand off to the proof desk.
- Proof, food, exit and checkpoint actions each hold the scanner until their own saved state is confirmed.
- Failure dialogs are full-screen, high-contrast and remain visible. A failed or uncertain write keeps the scanner locked with Retry / Check Status. The app blocks the top Back action and browser-back navigation while a write or required proof step remains unresolved.
- Confirmed success is visibly displayed before the scanner automatically prepares for the next guest. The volunteer can also use the explicit Next Guest button.
- Keeps volunteer actions visible in a compact single-screen layout with large touch targets, sticky actions, collapsed help and manual-code fallback.
- Adds a role-specific volunteer home desk and shift snapshot.
- Restricts checkpoint tools to the assigned role/station. Admin checkpoint management supports creating/editing stations and assigning eligible volunteers by name.
- The name picker includes authorized core/event volunteers, excludes ordinary attendees who merely opened the Mini App, and excludes blocked profiles.
- Selecting a disabled checkpoint no longer offers an unusable assignment button.
- Keeps `index.html` and `eventhub-preview.html` byte-for-byte identical.

## Backend candidate (separate Botkeep release ZIP)

The matching Botkeep Python release candidate and regression tests are packaged separately. It adds additive checkpoint assignment storage, signed Telegram display-name metadata, name-based volunteer promotion and Admin checkpoint team/assignment endpoints. The staff promotion picker can select named, unblocked Telegram users; the checkpoint picker is narrower and includes only authorized core/event volunteers. Event/core team lists now return display names and usernames. The backend restricts checkpoint-only volunteers to explicitly assigned enabled stations and fails closed if a checkpoint-role volunteer has no station assignment. Existing checkpoint-role volunteers must be assigned before use. Core/global volunteers retain their event-wide access. Assignment rows are included in cleanup backups/deletion and are removed with unused station or volunteer cleanup.

The backend ZIP is based on saved Library source `bot(20261104-204816).py`, not a live export from the running Botkeep process. The packaged candidate is 360,201 bytes (SHA-256 `0a2357fadbf792be11a22a6153279c293768d335f63e1a371e702963ae213853`); the ZIP SHA-256 is `54ab372ce9983f5278f5fe40430bd4970635eee3c719bc370a9608808c43fe9e`. Compare it with the exact deployed `bot.py` before installing; do not overwrite a newer running version blindly.

## Validation performed

- Python bytecode compilation: passed.
- Isolated role-resolution and action-permission regression tests: passed.
- Isolated checkpoint-team and event-volunteer candidate APIs, named Admin team lists, blocked-profile preservation, duplicate assignment idempotency, role-conflict rejection, disabled-station rejection, exact-station API authorization, multi-station removal, fail-closed unassigned roles, and checkpoint/volunteer cleanup tests: passed.
- Static frontend/backend action-contract check: all 40 distinct Admin action names used by the staging frontend are present in the Python Admin dispatcher.
- Frontend inline JavaScript compilation: passed.
- Static literal element-ID reference check: 232 fixed ID references checked; no missing fixed IDs found.
- Manual QR lock, backend pre/post verification, proof-gated release, failed-write lock and browser-back protection: source assertions passed.
- Staging `index.html` and `eventhub-preview.html`: same Git blob, byte-for-byte identical.
- Production `main` is unchanged and its two frontend files remain byte-for-byte identical.

These checks do not replace live Botkeep/API integration tests, Telegram WebApp tests, Google Sheets verification or physical Android camera/queue tests.

## Safe rollout

- This branch is not merged to `main` and is not deployed to GitHub Pages production.
- No Botkeep upload/restart, live database write, token/secret change, guest/pass mutation or Google Sheets action was performed.
- Compare the backend candidate with the exact running Botkeep file. Back up the current backend and all persistent SQLite/event database files before replacing anything.
- Deploy backend and frontend as a coordinated change; do not publish this frontend alone while the live backend is missing the matching checkpoint-team APIs.
- Test with a dedicated volunteer and test guest, including entry → proof stored/no proof → food → proof return → exit, one checkpoint assignment, duplicate scan, and a simulated network timeout.

## Backend candidate review (5 November 2026)

A separate candidate review is recorded in [EVENTHUB_BACKEND_CANDIDATE_REVIEW_20261105.md](EVENTHUB_BACKEND_CANDIDATE_REVIEW_20261105.md). The reviewed candidate SHA-256 is `c412b7fef9f22de0c3213c88c5852116ac58f345fecd109d5c5b96e9ec974323`. Its two isolated regression scripts were rerun successfully against that candidate after correcting a test portability issue that previously pointed to a different absolute local path.

The backend candidate is still a separate ZIP release and has not been reconciled against the exact running Botkeep source. It must not be deployed until that source is compared and a verified persistent-database backup is made.
