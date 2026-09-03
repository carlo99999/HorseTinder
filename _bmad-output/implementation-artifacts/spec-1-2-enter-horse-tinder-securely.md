---
title: 'Enter Horse Tinder securely'
type: 'feature'
created: '2026-09-03'
status: 'done'
review_loop_iteration: 0
baseline_commit: 'f5fe0a7d654015889b77e00ed8df776743abc446'
context:
  - '_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The runnable foundation has no player identity, so visitors cannot securely access their own Horse Tinder experience and later profile ownership cannot be enforced.

**Approach:** Add a cookie-session authentication boundary and a small, accessible browser entry flow for registration, sign-in, sign-out, and the authenticated Profile-setup destination.

## Boundaries & Constraints

**Always:** Keep API endpoints beneath `/api/v1`, return failures as `{code, message, details?}`, hash passwords server-side, derive the actor exclusively from the validated session, and use UUIDs plus UTC timestamps. Session cookies must be `HttpOnly`, `SameSite=Lax`, and `Secure` in production. Every unsafe request, including registration and sign-in, requires a server-validated CSRF token. The browser must first obtain an anonymous CSRF capability; authenticated sessions use their own CSRF capability. Sign-in failures must not disclose whether an account exists. Duplicate registration returns a neutral generic failure rather than naming an existing account. Browser requests stay same-origin with credentials.

**Ask First:** Adding identity providers, email delivery or verification, password-reset flows, external auth services, or collecting personal information beyond the minimum account credentials.

**Never:** Put session IDs, CSRF secrets, password hashes, or account contact fields in public profile DTOs, local storage, SPA build variables, logs, fixtures, or client-selected actor IDs. Do not implement Horse Profile persistence or editing in this story.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Anonymous CSRF bootstrap | Visitor requests entry capability | Server returns a signed or persisted anonymous CSRF token suitable for the current browser | No unsafe authentication request is accepted without the matching token |
| Registration | Valid unused account credentials and anonymous CSRF token | Persisted Account, authenticated cookie session, CSRF token available to the browser, and route to Profile setup | Return validation failures or a neutral duplicate-registration failure in the standard shape without creating a session |
| Sign-in failure | Unknown account or wrong password | No session or account disclosure | Return one recoverable, generic authentication failure and retain entered safe values |
| Protected access / expiry | Missing, invalid, expired, or revoked session | Protected API response is denied and UI directs visitor to sign in | Preserve safe unfinished form state and explain why sign-in is required |
| Sign-out / unsafe request | Valid session with sign-out, or unsafe request without valid CSRF token | Sign-out revokes the active session; unsafe request executes only with matching server validation | Return standard unauthorized/CSRF failure and do not mutate data |

</frozen-after-approval>

## Code Map

- `apps/api/app/main.py:42-116` -- reuse the versioned route, standard `error_response()`, exception handler, and application factory; register authentication routes/middleware without weakening structured logging.
- `apps/api/app/config.py:10-25` -- reuse the server-only app secret to validate anonymous CSRF capabilities and extend settings only for secure session configuration; never surface values to web code.
- `apps/api/app/db/models.py:12-55` -- add Account and session persistence alongside existing durable feature models; future profile ownership will reference Account.
- `apps/api/app/db/migration_versions/` -- add a forward-only revision for account/session schema rather than rewriting the applied foundation migration.
- `apps/api/app/db/migrations.py:31-67` -- existing migration runner is the schema preparation path and must discover the new revision.
- `apps/api/tests/test_foundation.py:16-112` and `apps/api/tests/conftest.py` -- follow the existing in-process Litestar/SQLite test conventions; add isolated auth, authorization, expiry/revocation, and CSRF coverage.
- `apps/web/src/api.ts:1-9` -- extend the typed same-origin client with credentialed anonymous/authenticated CSRF bootstrap, auth/session calls, and CSRF request handling while retaining `/api/v1` as the only base path.
- `apps/web/src/main.tsx:5-32` -- replace the health-only surface with labelled registration/sign-in, authenticated Profile-setup placeholder, loading/error state, and sign-out action; do not prebuild Story 1.4 navigation.
- `apps/web/src/api.test.ts` and `apps/web/package.json` -- preserve existing browser-client test/build conventions and add client behavior tests for credentials/CSRF and auth failures.

## Tasks & Acceptance

**Execution:**
- [x] `apps/api/app/auth/` -- add feature-owned account, password, anonymous and session CSRF, and request-actor services/routes -- centralizes all authentication mutations and server-side authorization.
- [x] `apps/api/app/db/models.py` and `apps/api/app/db/migration_versions/` -- persist minimally scoped Accounts and revocable, expiring sessions in a new migration -- establishes durable identity without changing deterministic horse fixtures.
- [x] `apps/api/app/main.py` and `apps/api/app/config.py` -- compose secure cookie/session behavior, protected-route handling, and safe configuration into the API -- keeps the existing versioned error/logging contract intact.
- [x] `apps/api/tests/` -- test anonymous-CSRF bootstrap, registration, generic sign-in failure, cookie/session actor isolation, protected denial, expiry/sign-out revocation, and CSRF rejection -- proves the matrix and prevents authorization regression.
- [x] `apps/web/src/api.ts`, `apps/web/src/main.tsx`, and `apps/web/src/api.test.ts` -- implement typed credentialed auth requests and accessible entry states that retain safe values on failure/expiry -- gives visitors a recoverable route to their private experience.
- [x] `README.md` and `.env.example` -- document any newly required server-only auth settings and local verification without real credentials -- keeps secure setup reproducible.

**Acceptance Criteria:**
- Given valid new visitor credentials, when registration succeeds, then the account is authenticated with a cookie-backed session and the UI reaches Profile setup without rendering private account data.
- Given an authenticated request, when the API determines the acting account, then it uses only the server-validated session and never a client-provided account identifier.
- Given a valid anonymous CSRF capability for registration/sign-in, or a valid session CSRF capability for an authenticated unsafe request, when the browser performs that request, then it succeeds; when either is missing or invalid, then no mutation occurs and the standard error shape is returned.
- Given an expired session while safe form data is entered, when the protected operation is denied, then the values remain visible and the UI gives a clear sign-in recovery path.

## Design Notes

Treat CSRF values as request capabilities, not substitutes for the HttpOnly session. Issue a server-validated anonymous capability before entry-form submissions, then issue a distinct session capability after authentication; require the matching explicit header for every unsafe request. Use one generic response for unknown-account and incorrect-password sign-in attempts, while duplicate registration receives a neutral failure and field-level validation stays accessible.

## Verification

**Commands:**
- `uv run pytest` -- expected: foundation and authentication persistence, session, authorization, and CSRF tests pass.
- `uv run ruff check .` -- expected: API implementation satisfies project lint rules.
- `npm --prefix apps/web test -- --run` -- expected: typed client and auth-state behavior tests pass.
- `npm --prefix apps/web run build` -- expected: SPA build succeeds with no server secret embedded.

## Suggested Review Order

**Authentication boundary**

- Defines the versioned, cookie-backed entry and exit contract.
  [`routes.py:71`](../../apps/api/app/auth/routes.py#L71)

- Keeps password, session, and CSRF authority entirely server-side.
  [`services.py:46`](../../apps/api/app/auth/services.py#L46)

**Durable identity**

- Adds forward-only Account and session persistence.
  [`auth_0002.py:12`](../../apps/api/app/db/migration_versions/auth_0002.py#L12)

- Wires the migration into the existing schema preparation sequence.
  [`migrations.py:13`](../../apps/api/app/db/migrations.py#L13)

**Browser recovery path**

- Bootstraps CSRF, retains safe form values, and handles expired sessions.
  [`main.tsx:15`](../../apps/web/src/main.tsx#L15)

- Restricts browser traffic to credentialed same-origin API calls.
  [`api.ts:13`](../../apps/web/src/api.ts#L13)

**Verification and setup**

- Exercises CSRF, authentication, expiry, and revocation behavior.
  [`test_auth.py:1`](../../apps/api/tests/test_auth.py#L1)

- Documents server-only session configuration for local setup.
  [`README.md:16`](../../README.md#L16)
