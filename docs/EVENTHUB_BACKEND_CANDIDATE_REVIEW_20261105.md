# EventHub backend candidate review — final candidate, 5 November 2026

## Candidate identity

- Base source: saved Library file bot(20261104-204816).py; this is not a fresh export from the running Botkeep process.
- Final bot.py size: 364,251 bytes.
- Final candidate bot.py SHA-256: 970d88a75bb0b860afe90895d197f5625fab5ace5f6657c61acb34211eef808c.
- Final release ZIP: 88,423 bytes.
- Final release ZIP SHA-256: a80986282984ebb911f08308bf26f538bf2ed2726cadc35f1992a37b86d43cec.

## Issues found and fixed during the audit

1. **Checkpoint-role fail-open fallback:** checkpoint-only volunteers with no explicit assignment previously retained legacy event-wide checkpoint access. The final backend requires at least one assigned enabled station for guest lookup, checkpoint list, volunteer dashboard and checkpoint scan. A scan is accepted only at an explicitly assigned station.
2. **Blocked global users in assignment picker:** the global-volunteer arm of checkpoint_team now filters blocked profiles. The backend additionally rejects blocked Telegram profiles at event-role, checkpoint and core/global assignment endpoints, even if a stale/manual request bypasses the picker.
3. **Volunteer scanner preflight:** the staging frontend disables both camera and manual verification when a checkpoint-only volunteer has no enabled station and directs them to the workspace/admin.
4. **Orphaned checkpoint assignment after removing core access:** cleanup now preserves an assignment only when that same event still has an event-specific checkpoint role. It removes stale assignments belonging to event-scoped entry/food/proof/scanner roles and assignments with no event role, while preserving legitimate checkpoint-role assignments.

## Backend functionality retained

- Additive bot_users.display_name / username migration and unique checkpoint assignment storage.
- Named Admin candidate picker, checkpoint team, assignment and removal actions.
- Event-specific and core/global volunteer access remain separate.
- Multiple station assignments per volunteer; removing one station preserves the others.
- Blocked profile state is not cleared by opening the Mini App; blocked users are rejected by assignment endpoints.
- Checkpoint deletion, event cleanup and volunteer cleanup handle assignment rows.
- Exact station authorization is enforced by the backend, not merely hidden in the UI.

## Isolated checks rerun against the final packaged source

- Python bytecode compilation for bot.py and both tests: PASS.
- test_staff_roles.py: PASS, including role resolution, role-to-action matrix, dashboard route and cross-event isolation.
- test_checkpoint_assignments.py: PASS, including no-assignment fail-closed checks, exact-station authorization, blocked candidate filtering, blocked endpoint rejection guards, name selection, isolated SQLite query execution, and core-access cleanup that preserves only an event-specific checkpoint role.
- Package SHA-256 values recorded in SHA256SUMS.txt and independently recomputed after packaging.

Tests use disposable SQLite databases and AST/source checks. They do not connect to Botkeep, Telegram, Google Sheets or physical Android devices.

## Remaining release blockers

1. Exact running Botkeep bot.py has not been retrieved. The candidate is based on a saved Library source from 4 November 2026; compare and reconcile the current deployment before replacement.
2. Verified backup and restore of the live primary registry database and complete event-database directory has not been performed.
3. No live Botkeep API restart/health check, Telegram authentication, Google Sheets delivery, or physical camera/queue test has been performed.
4. Frontend and backend must be deployed as a coordinated release after backend reconciliation; do not publish this frontend alone while production Botkeep lacks matching checkpoint assignment APIs.

## Safety

No Botkeep source was uploaded or restarted. No live database, event, guest, QR record, credential, Telegram token or Sheets secret was changed. Preserve the existing .env, process configuration, persistent SQLite files and old backend for rollback.
