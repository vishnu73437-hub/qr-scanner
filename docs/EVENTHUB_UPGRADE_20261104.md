# EventHub — 4 November 2026 Upgrade Notes

## Frontend changes (GitHub Pages)
The two EventHub entry pages are synchronized. The save request timeout now remains active through response-body parsing, a timeout warns that the save may have completed, and settings submissions are protected against double-clicks. The frontend omits `pass_layout` when the visual editor is not displayed, preventing a settings-only save from overwriting a saved Canva layout with null. It also distinguishes a successful save from a later refresh failure and displays backend mirror/audit warnings.

## Backend release candidate
The Botkeep candidate is separate from GitHub Pages. It includes the Canva layout validator and renderer, wrapped venue text, a bounded primary registry write, a short best-effort secondary DB mirror using the current request connection, and a registry audit fallback if the event DB is locked.

## Regression evidence
Offline tests used temporary SQLite files and a preview-only QR; production DB files were not opened. Tests covered layout retention, QR geometry, pass rendering, a deliberately locked secondary DB, audit fallback, mirror recovery after lock release, guest-data preservation and a bounded primary DB lock response.

## Not deployed
The backend candidate has not been installed or restarted on Botkeep. The live Telegram bot, Apps Script/Sheets, physical camera scanner and production load have not been tested. Follow the existing audit-status checklist before deployment.
