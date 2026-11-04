# EventHub — Technical Audit & Upgrade Status

Last prepared: 3 November 2026  
Repository: https://github.com/vishnu73437-hub/qr-scanner

## Purpose
This document records the isolated checks completed for the KSMU EventHub project and separates them from checks that still require the live Botkeep server, Telegram, Google Apps Script, or a physical phone.

## Safety / production status
- No production database was opened or modified during the isolated audit.
- No registrations, guest records, QR tokens, event settings, admin permissions, or secrets were reset.
- No Botkeep production deployment or restart was performed.
- No bulk pass refresh or bulk Telegram message was sent.
- Treat all deployment steps as pending until verified on the live service.

## Components
- Telegram Mini App frontend: `eventhub-preview.html` (the root `index.html` was previously synchronized with this file).
- Hosting: GitHub Pages for the frontend.
- Telegram bot/API: Botkeep, currently referenced as `https://unwjym.bot-keep.xyz`.
- Mini App URL: `https://vishnu73437-hub.github.io/qr-scanner/eventhub-preview.html`.

## Isolated checks reported as passed
- Python source compilation.
- API handler checks.
- QR stale-credential helper checks.
- Secret-redaction checks.
- Registration normalization checks.
- Temporary database initialization twice while preserving sample guest, pass, QR, pending-registration, and outbox records.
- Local `/health` endpoint test.
- CORS preflight / OPTIONS test.
- API public-origin validation.

These checks are not proof of a successful live deployment.

## Not verified against production
- Full Telegram polling and bot command flow (the Telegram library/runtime was unavailable in the isolated test environment).
- Live Botkeep deployment, process startup, DNS, reverse proxy, and external network behavior.
- Live Google Apps Script delivery and spreadsheet writes.
- Physical camera scanning on Android/iOS.
- Real guest registration, approval, QR entry, food checkpoint, and volunteer workflows.
- Production load and concurrent use.

## Outstanding verification checklist

### Before deployment
- [ ] Confirm Botkeep startup command and exact working directory.
- [ ] Confirm the exact Python entry-point filename expected by Botkeep; do not assume it is `bot.py`.
- [ ] Download a backup of the currently running backend source.
- [ ] Take a database backup and verify that it can be read.
- [ ] Confirm the existing database path and event database directory.
- [ ] Confirm all existing environment variables are retained without copying secrets into GitHub.
- [ ] Confirm only one bot polling process will run for this Telegram token.

### Botkeep configuration — preserve existing values
Do not paste secret values into this repository, screenshots, issues, or chat.
- `TELEGRAM_BOT_TOKEN`
- `ADMIN_IDS`
- `DATABASE_FILE`
- `EVENT_DATABASE_DIR`
- `API_PUBLIC_URL` or `BOTKEEP_PUBLIC_URL`
- `MINI_APP_URL`
- `SHEETS_SYNC_URL`
- `SHEETS_SYNC_SECRET`
- `PORT` / `SERVER_PORT`

Expected public API origin format:
`https://unwjym.bot-keep.xyz`

Use the HTTPS origin only — do not append `/health` or `/api`.

### Deployment procedure
1. Record the current Botkeep startup command, working directory, environment variable names, and database paths.
2. Back up the current backend source and database files.
3. Upload the reviewed backend file to the exact filename/path required by the existing Botkeep startup command.
4. Preserve the existing database and event database directory in place. Do not initialize a fresh production database over them.
5. Preserve all environment variables and secret values unchanged.
6. Restart the existing Botkeep service only. Do not start a second bot process using the same token.
7. Check `GET /health`. Expected healthy response:
   ```json
   {"ok":true,"service":"KSMU EventHub API","database":"ok"}
   ```
8. If health fails, restore the backed-up backend source and investigate logs before attempting another change.

### Post-deployment smoke tests
- [ ] Telegram bot starts and responds to an admin account.
- [ ] Volunteer account permissions are correct.
- [ ] Mini App opens from Telegram.
- [ ] Guest registration form loads and validates required fields.
- [ ] Existing guest records and passes remain visible.
- [ ] A controlled test registration can be approved.
- [ ] A test QR can be previewed and scanned.
- [ ] Entry and food checkpoint state updates correctly for the test guest.
- [ ] `/mypass` or the equivalent pass retrieval works.
- [ ] Sheets sync queue processes a controlled test record.
- [ ] Admin and volunteer screens work on desktop and mobile.
- [ ] Camera permission denial and retry do not leave the scanner stuck.

Do not test by revoking or reissuing a real guest's pass. Use a dedicated test guest.

## Known project risks / items to review
- Google Sheets previously returned `Unauthorized`; verify the configured URL and secret match the Apps Script deployment. Never expose the secret in GitHub.
- Admin API calls previously showed occasional 1.5–1.74 second responses; measure again after deployment before changing hosting.
- Botkeep had intermittent slow responses / timeouts in earlier troubleshooting.
- Scanner behavior must be tested on a real phone and browser.
- Confirm Kazan timestamps use the intended `Europe/Moscow` timezone in both the backend and spreadsheet receiver.
- Do not remove the existing food preference field or event-specific registration configuration without checking the current event schema and data.

## Hosting recommendation
Earlier resource screenshot showed approximately 116 MB of 512 MB memory, 0.63% of 50% CPU allocation, and 54.8 MB of 1 GB storage. Based on that snapshot alone, there was no evidence that a paid hosting upgrade was necessary. Recheck live resource usage and response times after a controlled load test.

## Change log
- 2026-11-03: Isolated audit results and safe deployment checklist documented.
- Live deployment: NOT performed by this audit.


## Follow-up audit — 4 November 2026

### GitHub Pages frontend changes committed
Both `index.html` and `eventhub-preview.html` are synchronized (current blob SHA: `e47c9b34f33d192fbd486654186a85de7df3b842`).

- The API request timeout now remains active through JSON response parsing.
- `update_event` and other long admin actions have a 120-second client timeout.
- An aborted `update_event` request tells the admin that the outcome may be uncertain and advises checking saved values before retrying.
- Saving settings while the visual editor is not shown omits `pass_layout` instead of sending `null`, so an existing layout is not erased.
- Duplicate settings-form submissions are blocked while a save is in progress.
- A confirmed save is distinguished from a later page-refresh failure.
- The admin sees a warning if the backend reports an unsynchronized event mirror or audit write.
- Frontend inline JavaScript syntax checks passed in the isolated audit.

### Backend release candidate prepared and tested offline
The updated Botkeep source candidate adds:
- validation and retention of the per-event Canva `pass_layout`;
- portrait-renderer support for layer positions, sizes, visibility, colour, alignment and rotation, while keeping QR square and upright;
- wrapped venue text and the corrected right-side venue panel;
- a bounded registry lock wait for `update_event`;
- best-effort local event-database mirroring using the request's existing connection;
- an audit fallback to the shared registry when the event-local database is locked.

Isolated regression tests passed for:
- saved Canva layout surviving an incoming `pass_layout: null`;
- QR geometry and out-of-bounds rejection;
- a 1024 × 1536 PNG pass preview;
- `update_event` returning in about one second with a deliberately locked secondary event database instead of waiting 30 seconds;
- registry audit fallback and subsequent local mirror synchronization after lock release;
- preservation of an existing guest row, pass code, QR token, approval status, and entry/food flags;
- a bounded 503 response for a locked primary database.

### Production deployment remains unverified
- The Botkeep source candidate has **not** been installed or restarted on the live Botkeep service.
- No production SQLite database was opened or modified by the isolated tests.
- No real guest registration, QR issuance/reissue, bulk pass send, Telegram polling, Google Sheets delivery, or physical camera scan was performed.
- Do not mark the backend deployed until the existing Botkeep entry point and working directory are confirmed, backups are taken, and the live `/health` endpoint plus controlled smoke tests pass.
