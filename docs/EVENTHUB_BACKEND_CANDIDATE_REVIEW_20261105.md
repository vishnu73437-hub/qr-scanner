# EventHub backend candidate review — revised 5 November 2026

## Candidate identity

- Base source: saved Library file bot(20261104-204816).py; this is not a fresh export from the running Botkeep process.
- Revised bot.py size: 362,347 bytes.
- Revised candidate bot.py SHA-256: a01244a1f27e3eb3efb795503845ea0aafe64b717777bed9b47c07a118d09ceb.
- Revised release ZIP: 88,305 bytes.
- Revised release ZIP SHA-256: 9361f4880965855578668e134514fe7e2bf8a1e753e084a88fb439f0588a18da.

## Important issues found and fixed during the full audit

1. **Checkpoint-role fail-open fallback:** checkpoint-only volunteers with no explicit assignment previously retained legacy event-wide checkpoint access. This conflicted with the stated restricted-station policy. The revised backend now requires at least one assigned enabled station for guest lookup, checkpoint list, volunteer dashboard and checkpoint scan. A scan is accepted only at an explicitly assigned station.
2. **Blocked global users in assignment picker:** the global-volunteer arm of the checkpoint_team UNION omitted its blocked-profile filter. The revised SQL adds WHERE COALESCE(bu.blocked,0)=0, and a regression row verifies a blocked core account is excluded.
3. **Volunteer scanner preflight:** the staging frontend now disables both camera and manual verification when a checkpoint-only volunteer has no enabled station, and directs them to the workspace/admin rather than letting them scan into a generic error.

## Backend functionality retained

- Additive bot_users.display_name / username migration and unique checkpoint assignment storage.
- Named Admin candidate picker, checkpoint team, assignment and removal actions.
- Event-specific and core/global volunteer access remain separate.
- Multiple checkpoint assignments per volunteer; removing one station preserves the others.
- Blocked profile state is not cleared by opening the Mini App.
- Checkpoint deletion, event cleanup and volunteer cleanup handle assignment rows.
- Exact station authorization is enforced on the backend, not merely hidden in the UI.

## Isolated checks rerun against the revised source

- Python bytecode compilation for bot.py and both tests: PASS.
- test_staff_roles.py: PASS.
- test_checkpoint_assignments.py: PASS, including no-assignment fail-closed, assigned-enabled station filtering, exact-station rejection, blocked global candidate filtering, name selection and SQLite query execution.

Tests use disposable SQLite databases and AST-extracted helpers/source checks. They do not connect to Botkeep, Telegram, Google Sheets or physical Android devices.

## Remaining release blockers

1. Exact running Botkeep bot.py has not been retrieved. Compare and reconcile the current deployment before replacement.
2. Verified backup and restore of the live primary registry database and complete event-database directory has not been performed.
3. No live Botkeep API restart/health check, Telegram authentication, Google Sheets delivery, or physical camera/queue test has been performed.
4. Frontend and backend must be deployed as a coordinated release after backend reconciliation; do not publish this frontend alone while production Botkeep lacks matching checkpoint assignment APIs.

## Safety

No Botkeep source was uploaded or restarted. No live database, event, guest, QR record, credential, Telegram token or Sheets secret was changed. Preserve the existing .env, process configuration, persistent SQLite files and old backend for rollback.
