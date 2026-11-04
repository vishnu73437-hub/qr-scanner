# EventHub Event-Day Smart Upgrade — 5 November 2026

## Scope

This staging branch improves the EventHub event-day volunteer and admin workflows. It is not a production deployment.

## Frontend

- Locks QR capture as soon as one guest is detected and holds the lock across guest verification and Entry, Proof, Food, Exit or checkpoint recording.
- Re-reads the guest record after each mutation and only presents success after the expected saved state is visible in the backend response.
- Before retrying a timed-out action, checks the current guest state to avoid blindly submitting a duplicate.
- Uses large, fixed success/failure dialogs. Failures remain locked and offer retry/status verification; volunteers can leave to their desk without silently clearing the unresolved lock.
- Adds a compact volunteer scanner with role-specific actions, a bottom-sticky primary action, manual pass-code fallback and camera help in collapsed sections.
- Adds a role-specific volunteer home desk and shift snapshot.
- Reloads the selected-event role when an event is opened from the event chooser.
- Uses volunteer names in event volunteer and checkpoint assignment selectors.

## Backend candidate (separate release ZIP)

The matching Botkeep Python release candidate and regression tests are packaged separately. It adds volunteer identity metadata, checkpoint assignment records and exact-station authorization; makes the event chooser limit event-scoped volunteers to their assigned active events; and includes name-based admin candidate queries.

The backend ZIP is a candidate reconstructed from a saved Library source file, not from the running Botkeep process. It must be compared against the currently deployed file before installation.

## Validation performed

- Inline JavaScript compilation: passed.
- Static literal element ID references: no missing IDs found.
- index.html and eventhub-preview.html: byte-for-byte identical (same Git blob).
- Python syntax compilation: passed.
- Isolated role-resolution and event-scope tests: passed.
- Isolated checkpoint-assignment, unique assignment, exact-station authorization, volunteer-name SQL, blocked-user filtering and active-event chooser SQL tests: passed.

These checks do not replace a live Botkeep/API test or physical Android/Telegram camera test.

## Safety / deployment

- This branch is not merged to main.
- No GitHub Pages production promotion, Botkeep upload/restart, live DB write, token/secret change, or real guest/pass mutation was performed.
- Review the branch and backend ZIP; compare the backend with the exact running Botkeep source; back up the database and event files; then deploy frontend and backend separately in an approved window.
- Test with a dedicated test volunteer and test guest before event-day use.
