# EventHub backend candidate review — final candidate, 5 November 2026

## Candidate identity

- Base source: saved Library file bot(20261104-204816).py; not a fresh export from the running Botkeep process.
- Final bot.py size: 365,412 bytes.
- Final candidate bot.py SHA-256: 0510c10f9df31b9f3884c3d168f07f33ed8ecab9ab7a086fbf9033372661a848.
- Final release ZIP: 89,817 bytes.
- Final release ZIP SHA-256: ff2cc90b1db5bf0db3ee4432c1a5af626471051735f269b030cbb904253dcfd3.

## Issues found and fixed during the audit

1. **Checkpoint-role fail-open fallback:** checkpoint-only volunteers with no explicit assignment previously retained legacy event-wide checkpoint access. The final backend requires at least one assigned enabled station for guest lookup, checkpoint list, volunteer dashboard and checkpoint scan. A scan is accepted only at an explicitly assigned station.
2. **Blocked global users in assignment picker:** checkpoint_team filters blocked profiles. The backend additionally rejects blocked Telegram profiles at event-role, checkpoint and core/global assignment endpoints, even if a stale/manual request bypasses the picker.
3. **Volunteer scanner preflight:** the staging frontend disables both camera and manual verification when a checkpoint-only volunteer has no enabled station. If the station-list request fails, the scanner stays blocked until the station-access check succeeds.
4. **Orphaned checkpoint assignment after removing core access:** cleanup preserves an assignment only when that same event still has an event-specific checkpoint role. It removes stale assignments belonging to event-scoped entry/food/proof/scanner roles and assignments with no event role, while preserving legitimate checkpoint-role assignments.
5. **Blocked-status regression:** /api/role previously reset the blocked flag when the Mini App opened. It now refreshes last-seen/name metadata without clearing a blocked flag; an actual /start interaction can reactivate the user.
6. **Shared blocked-status propagation:** Telegram delivery failures indicating blocked/deactivated/chat-not-found now upsert blocked status into both the shared registry and current event database. This makes Admin picker filters consistent with announcement delivery results, including when a user had no registry row yet.
7. **Entry-to-proof hand-off:** Entry-role volunteers can now record Entry and then store proof or explicitly confirm No Proof Provided. The backend still denies food, proof return and exit to the Entry role; the scanner remains locked until proof is resolved, while the Proof/Exit role handles return and exit.

## Isolated checks rerun against the final packaged source

- Python bytecode compilation for bot.py and both tests: PASS.
- test_staff_roles.py: PASS, including role resolution, role-to-action matrix, dashboard route, cross-event isolation and Mini App blocked-state preservation, and Entry-to-proof role gating.
- test_checkpoint_assignments.py: PASS, including no-assignment fail-closed checks, exact-station authorization, blocked candidate filtering, blocked endpoint rejection guards, blocked-status propagation to both databases, name selection, isolated SQLite query execution, and core-access cleanup that preserves only an event-specific checkpoint role.
- Package SHA-256 values recorded in SHA256SUMS.txt and recomputed after packaging.

Tests use disposable SQLite databases and AST/source checks. They do not connect to Botkeep, Telegram, Google Sheets or physical Android devices.

## Remaining release blockers

1. Exact running Botkeep bot.py has not been retrieved. The candidate is based on a saved Library source from 4 November 2026; compare and reconcile the current deployment before replacement.
2. Verified backup and restore of the live primary registry database and complete event-database directory has not been performed.
3. No live Botkeep API restart/health check, Telegram authentication, Google Sheets delivery, or physical camera/queue test has been performed.
4. Frontend and backend must be deployed as a coordinated release after backend reconciliation; do not publish this frontend alone while production Botkeep lacks matching checkpoint assignment APIs.

## Safety

No Botkeep source was uploaded or restarted. No live database, event, guest, QR record, credential, Telegram token or Sheets secret was changed. Preserve the existing .env, process configuration, persistent SQLite files and old backend for rollback.