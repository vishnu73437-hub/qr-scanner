# EventHub backend candidate review — 5 November 2026

## Candidate identity

- Candidate source: `EventHub_EventDay_Smart_Upgrade_2026-11-05/bot.py`
- Candidate SHA-256: `c412b7fef9f22de0c3213c88c5852116ac58f345fecd109d5c5b96e9ec974323`
- Candidate size: 361,211 bytes
- This candidate is a separate release package, not the Python file currently in the GitHub frontend branch and not a fresh download from the running Botkeep service.

## Review findings

The candidate contains the backend actions used by the upgraded frontend, including:
- `event_volunteer_candidates`
- `checkpoint_team`
- `assign_checkpoint_volunteer`
- `remove_checkpoint_volunteer`
- `assign_event_volunteer`
- `remove_event_volunteer`
- `volunteer_dashboard`

It also includes additive checkpoint assignment storage and exact-station authorization for checkpoint-only volunteers.

## Isolated checks rerun

- Python source and test AST/syntax compilation: PASS.
- `test_staff_roles.py`: PASS.
- `test_checkpoint_assignments.py`: PASS.
- Cross-event role isolation and role/action matrix: PASS.
- Duplicate checkpoint assignment constraint: PASS.
- Exact-station authorization: PASS.
- Checkpoint-team SQL and volunteer name-picker SQL: PASS.
- Blocked-user filtering and assigned-active-event chooser: PASS.

A portability defect was found in the original `test_staff_roles.py`: it read `/mnt/data/eventhub_upgrade/bot.py`, which could test a different saved source rather than the candidate beside the test. The release-candidate copy was corrected to load `bot.py` relative to `__file__`, and both test scripts were rerun successfully against the 361,211-byte candidate.

## Remaining release blockers

1. The candidate source and test files are not yet part of this GitHub branch; they remain a separate package.
2. The exact currently running Botkeep source has not been retrieved, so source reconciliation is still required.
3. No verified backup/restore of the live primary SQLite database and full `event_databases` directory has been performed.
4. Live Telegram authentication, Google Sheets sync, Botkeep API workflows, and physical Android camera behavior remain untested.

## Safety

Do not replace the live Botkeep entry point or merge the frontend PR solely on the basis of these isolated tests. Preserve the existing database files, `.env`, bot token, Sheets credentials, startup command and Botkeep process configuration. Deploy frontend and backend separately after exact-source reconciliation and a verified backup/restore rehearsal.

## Frontend/backend action-name compatibility

A static cross-check was also run between the current staging `index.html` and the 361,211-byte backend candidate. All 40 distinct `adminCall(...)` action names used by the frontend were found in the backend candidate's admin action dispatch. No frontend admin action name was missing. This is a source-level contract check only; it does not replace authenticated HTTP requests against a running Botkeep instance.
