# Horse Tinder

An original, fictional horse-themed social parody. It is unaffiliated with Tinder and contains no Tinder marks, flame imagery, real-person data, payments, or location features.

## Local development

Prerequisites: Python 3.13.11, Node.js 20.19+, npm, Docker Compose.

1. Copy `.env.example` to `.env` and replace `APP_SECRET` with a local random value. `SESSION_TTL_SECONDS` controls cookie-session expiry and stays server-only.
2. Start the complete local stack: `docker compose up --build`. The API migrates and loads fixtures before accepting traffic; open `http://localhost:5173`.
3. The Vite dev server proxies same-origin `/api/v1` requests to the API container. For a host-run SPA, use `npm --prefix apps/web ci` then `npm --prefix apps/web run dev` while the API is available at `http://localhost:8000` (set the proxy target accordingly).
4. To prepare a reset database manually, export the server-only values from `.env` and run `PYTHONPATH=apps/api uv run python -m app.cli`. The command applies ordered migrations, then repeatably loads the fictional profiles, mutual match, and gestures.

The SPA calls only same-origin `/api/v1` JSON. An executable production topology is `docker compose -f compose.yaml -f compose.production.yaml up --build`; nginx serves the SPA at `http://localhost:8080` and proxies `/api/v1` to the API service. Browser builds never receive `DATABASE_URL` or `APP_SECRET`.

## Verification

Run `uv run pytest`, `uv run ruff check .`, `npm --prefix apps/web test -- --run`, and `npm --prefix apps/web run build`. Health is available at `GET /api/v1/health` and returns `{"data":{"service":"horse-tinder-api","version":"v1"}}`. API failures use `{ "code", "message", "details"? }`.

## Secure entry

The browser first requests `GET /api/v1/auth/csrf`, then sends its returned token as `X-CSRF-Token` for registration or sign-in. Successful authentication sets an HttpOnly, SameSite=Lax cookie and returns a separate session CSRF capability for later unsafe requests such as sign-out. In production the cookie is also Secure. Never put either token, account email, or password data in browser storage.

## Horse Profiles

After signing in, create a private owner-scoped profile with `POST /api/v1/profiles/me` or edit it with `PUT /api/v1/profiles/me`. Send the session CSRF capability as `X-CSRF-Token`; `GET /api/v1/profiles/me` returns only the public fictional profile fields. Each account can create one profile, while deterministic discovery fixtures remain unowned.

## Shell accessibility checks

After signing in, verify that the centered desktop top navigation and mobile bottom navigation both expose Discovery, Matches, and Profile. Use the keyboard to reach the visible “Skip to main content” link and verify that it moves focus to the main content. Confirm each selected destination has a visible current state as well as the programmatic current-page state; Discovery and Matches should plainly say they are unavailable, without sample profiles or matches.

Also check the Profile form at 200% text size and 400% browser zoom, then enable reduced motion and a forced-colors mode. Navigation, focus indicators, form labels, validation, saving, sign-out, and expired-session recovery must remain usable with no avoidable horizontal scrolling.
