# EventHub backend candidate review — 5 November 2026

## Candidate identity

- Candidate source: saved Library file `bot(20261104-204816).py`, with the changes described below.
- Packaged candidate size: 360,201 bytes.
- Candidate `bot.py` SHA-256: `0a2357fadbf792be11a22a6153279c293768d335f63e1a371e702963ae213853`.
- Release ZIP SHA-256: `54ab372ce9983f5278f5fe40430bd4970635eee3c719bc370a9608808c43fe9e`.
- This is not a fresh export from the running Botkeep process.

## Backend additions and fixes

- Adds shared checkpoint assignment storage and additive `bot_users.display_name` / `username` migrations.
- Implements the frontend's `event_volunteer_candidates` action for name-based Admin promotion. It returns named, unblocked Telegram users and excludes administrators.
- Adds `checkpoint_team`, `assign_checkpoint_volunteer`, and `remove_checkpoint_volunteer`.
- Checkpoint station assignment candidates are limited to authorized core/event volunteers; ordinary guests cannot appear in that picker.
- Event/core team lists now include display names and usernames rather than rendering only Telegram IDs.
- Checkpoint-only roles are fail-closed: a volunteer with no explicit station assignment cannot list or scan checkpoints. Existing checkpoint-role volunteers must be assigned a station before event-day use.
- Backend checks the volunteer's exact station assignment when the checkpoint scan is submitted.
- Multi-station assignment removal preserves other stations; removing the final station removes the checkpoint-only event role. Core/global access is intentionally retained.
- Blocked profile flags are not cleared by opening the Mini App. Removed core volunteers do not leave orphaned core-only checkpoint assignments.
- Checkpoint deletion removes the linked station assignments and any now-unused checkpoint-only roles. Event cleanup includes assignment rows in the backup and deletes them for the selected event.
- The primary event cleanup/checkpoint deletion paths reuse their current SQLite connection to avoid a nested writer lock against the same database.

## Isolated checks rerun against the exact packaged source

- Python bytecode compilation: PASS.
- `test_staff_roles.py`: PASS.
- `test_checkpoint_assignments.py`: PASS.
- Name-based candidate selection, ordinary-attendee promotion picker vs restricted checkpoint picker, blocked user filtering, profile update without clearing blocked state: PASS.
- Event/core Admin team list name/username fields: PASS.
- Assignment idempotency, disabled checkpoint rejection, desk-role conflict rejection: PASS.
- Exact-station checkpoint listing and wrong-station scan rejection: PASS.
- Multiple station assignments, removing one station, fail-closed after last station removal: PASS.
- Core volunteer access preservation and orphan cleanup: PASS.
- Checkpoint deletion and assignment cleanup: PASS.
- Static cross-check: all 40 distinct `adminCall(...)` action names in the staging frontend appear in the Python Admin action dispatcher: PASS.

Tests use isolated temporary SQLite databases and AST-extracted code. They do not connect to production Botkeep, Telegram, Google Sheets or physical Android devices.

## Remaining release blockers

1. The exact running Botkeep `bot.py` has not been retrieved. Compare it with this candidate and manually reconcile any newer/custom changes before replacement.
2. A verified backup/restore of the live primary SQLite database and the complete event-database directory has not been performed.
3. No live Botkeep API restart/health check, Telegram authentication workflow, Google Sheets delivery test, or physical camera/queue test has been performed.
4. The frontend staging branch and backend ZIP must be deployed as one coordinated release. Do not merge/deploy the frontend by itself while production Botkeep lacks these APIs.

## Safety

This package was created from a saved Library source. No Botkeep file was uploaded or restarted, no live database was changed, and no event/guest/QR records or credentials were modified. Preserve the current `.env`, persistent SQLite files, process configuration and old backend for rollback.

## Frontend/backend action-name compatibility

The staging frontend uses 40 distinct Admin action names. Static inspection confirms those literals are implemented by the packaged backend candidate. This source-level contract check does not substitute for authenticated HTTP requests against a live Botkeep service.
