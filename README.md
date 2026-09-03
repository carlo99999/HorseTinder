# Horse Tinder

An original, fictional horse-themed social parody. It is unaffiliated with Tinder and contains no Tinder marks, flame imagery, real-person data, payments, or location features.

## Local development

Prerequisites: Python 3.11+, Node.js 20+, npm, Docker Compose.

1. Copy `.env.example` to `.env` and replace `APP_SECRET` with a local random value.
2. Start PostgreSQL and the API: `docker compose up --build`.
3. In another terminal, install and start the SPA: `npm --prefix apps/web install` then `npm --prefix apps/web run dev`.
4. To prepare a reset database manually, export the server-only values from `.env` and run `PYTHONPATH=apps/api uv run python -m app.cli`. The command migrates first, then repeatably loads the fictional profiles, mutual match, and gestures.

The SPA calls only same-origin `/api/v1` JSON. In production, place the SPA and API behind the same origin; browser builds never receive `DATABASE_URL` or `APP_SECRET`.

## Verification

Run `uv run pytest`, `uv run ruff check .`, and `npm --prefix apps/web run build`. Health is available at `GET /api/v1/health` and returns `{"data":{"service":"horse-tinder-api","version":"v1"}}`. API failures use `{ "code", "message", "details"? }`.
