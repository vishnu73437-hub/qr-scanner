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

The matching Botkeep Python release candidate and regression tests are packaged separately. It adds additive checkpoint assignment storage, volunteer display-name metadata and Admin checkpoint team/assignment endpoints. The backend restricts checkpoint-only volunteers to stations assigned to them, preserves legacy event-wide checkpoint roles with no station-specific rows, validates checkpoint enablement, and includes checkpoint assignments in event cleanup backups/deletion.

The backend ZIP is based on a saved Library source file, not a live export from the running Botkeep process. Compare it with the exact deployed `bot.py` before installing; do not overwrite a newer running version blindly.

## Validation performed

- Python bytecode compilation: passed.
- Isolated role-resolution and action-permission regression tests: passed.
- Isolated checkpoint-assignment, duplicate constraint, event/station/user isolation, exact-station authorization, volunteer-name SQL, blocked-user filtering and event-chooser tests: passed.
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