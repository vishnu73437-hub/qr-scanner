# EventHub Upgrade Centre

This folder is the review and deployment checklist for the KSMU EventHub project.

## Start here
1. Read [Technical Audit & Upgrade Status](./EVENTHUB_AUDIT_STATUS.md).
2. Review [Upgrade Roadmap](./EVENTHUB_UPGRADE_ROADMAP.md).
3. Complete the pre-deployment backup and preservation checklist before uploading backend code to Botkeep.
4. Deploy only after confirming the exact Botkeep startup filename and database paths.

## Important
This repository is public. Never commit Telegram bot tokens, admin IDs if treated as private, database files, guest exports, QR secrets, Apps Script secrets, private URLs containing credentials, or production logs containing personal data.

GitHub Pages frontend changes do not automatically update the Botkeep backend. Backend deployment is a separate operation.

## Project endpoints
- Repository: https://github.com/vishnu73437-hub/qr-scanner
- Mini App: https://vishnu73437-hub.github.io/qr-scanner/eventhub-preview.html
- Botkeep API origin: `https://unwjym.bot-keep.xyz`

## Deployment status
- Frontend: previously published through GitHub Pages; recheck the Pages deployment status after any frontend commit.
- Backend: upgrade package is not confirmed deployed to Botkeep.
- Production data: preserve all current records and QR credentials.


## Follow-up — 4 November 2026
- GitHub frontend pages: `index.html` and `eventhub-preview.html` synchronized with the save-flow / Canva-layout preservation fixes.
- Backend: a tested release candidate is prepared separately for Botkeep; it is **not** automatically deployed by GitHub Pages and is not confirmed live.
- See [4 November upgrade and regression-test notes](./EVENTHUB_UPGRADE_20261104.md).
- Preserve the production database and environment variables. Do not send updated passes until the live backend preview has been checked.
