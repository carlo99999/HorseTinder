---
title: 'Establish the runnable Horse Tinder foundation'
type: 'feature'
created: '2026-09-03'
status: 'done'
review_loop_iteration: 0
baseline_commit: '4ef225a62baa92fa234cc65c599958d936bdcae6'
context:
  - '_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repository contains only a minimal Python package, so Horse Tinder cannot yet run as the planned full-stack parody or persist real product data. Later authentication, profiles, discovery, and chat need a reliable shared runtime rather than frontend-only mock data.

**Approach:** Create the documented React/Vite SPA, Litestar API, and PostgreSQL development foundation. Establish the versioned database, startup safeguards, API contract, deterministic backend fixtures, and a small verifiable health path that future feature stories can extend.

## Boundaries & Constraints

**Always:** Use React 19.2/Vite 8.2, Litestar 2.24, and PostgreSQL 18; serve versioned JSON only below `/api/v1`; keep the SPA/API same-origin boundary and keep secrets server-side. Validate required API configuration at startup, run migrations before serving, log requests and errors structurally, and make PostgreSQL the sole authoritative fixture source. Use feature-owned service mutations, UUID IDs, UTC ISO-8601 payload timestamps, and `{code, message, details?}` API errors.

**Ask First:** Introducing external hosted services, payment/location features, real-person data collection, or a materially different deployment topology.

**Never:** Build product screens, authentication flows, profile editing, discovery, matching UI, or frontend-only copies of fixture data in this story. Do not use Tinder marks, flame imagery, or distinctive trade dress.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Healthy local runtime | Valid API environment, migrated PostgreSQL, and running SPA/API | SPA builds and communicates only with same-origin `/api/v1` JSON; API health/version path responds with a versioned JSON DTO | N/A |
| Missing required API configuration | API starts without a required server setting | Service refuses to start before serving traffic | Structured startup error identifies the missing setting without exposing a secret |
| Fresh or reset database | Migrations and fixture command execute | Schema is current and deterministic fictional profiles, a mutual-match path, and gestures are available from the database | Migration/fixture failure exits non-zero with structured error logging |
| Unknown API route | Request below `/api/v1` does not resolve | JSON response retains the standard error contract | Return a stable machine-readable error code and no HTML fallback |

</frozen-after-approval>

## Code Map

- `pyproject.toml:1-34` -- current Python-only package/tooling baseline; add or replace API-runtime dependency and test configuration without weakening Ruff/Pyrefly policy.
- `uv.lock:1-115` -- regenerated after Python dependency changes; presently has no web/API/database closure.
- `src/horsetinder/__init__.py:1-2` and `tests/test_placeholder.py:1-2` -- disposable skeleton, with no feature behavior to preserve.
- `README.md:1-2` -- replace placeholder documentation with a clean-checkout local run, migration, fixture, and verification guide.
- `apps/web/` -- new React/Vite 8.2 SPA boundary; contains only a minimal shell plus typed API client constrained to `/api/v1`, never seed data or server secrets.
- `apps/api/app/` -- new Litestar application; add configuration, structured logging, versioned route/error handling, database migration entry point, and feature-oriented fixture ownership.
- `apps/api/app/db/` -- new PostgreSQL connection, migration, and deterministic fixture modules; data needed by later profile/match/gesture stories lives here.
- `docs/` -- new concise API/deployment conventions if they cannot live clearly in the README.
- `_bmad-output/implementation-artifacts/epic-1-context.md` -- generated Epic 1 constraints; retain as planning context and do not discard.

## Tasks & Acceptance

**Execution:**
- [x] `apps/web/` -- scaffold the React 19.2/Vite 8.2 SPA with package scripts, an original minimal shell, and a typed same-origin `/api/v1` client -- establishes the browser runtime without product features or embedded fixture data.
- [x] `apps/api/app/` -- scaffold Litestar 2.24 as a feature-oriented API with validated environment settings, structured request/error logging, JSON exception handling, and a `/api/v1` health/version DTO -- creates a testable contract boundary.
- [x] `apps/api/app/db/` and migration configuration -- establish PostgreSQL 18 persistence, a repeatable migration-before-serve path, and versioned deterministic fixture loading for fictional horse profiles, a mutual-match path, and gestures -- makes backend data authoritative from day one.
- [x] `apps/api/tests/` and `apps/web/` test/build configuration -- cover missing configuration, health DTO/error contract, migration/fixture repeatability, and client base-path behavior -- protect the foundation's failure cases and boundary.
- [x] `README.md`, `.env.example`, and local orchestration/config files -- document a fresh-checkout setup, isolated server environment variables, database startup, migration, fixture load, and verification commands -- makes the stack reproducible without leaking secrets.
- [x] `pyproject.toml`, `uv.lock`, and obsolete skeleton files -- align Python runtime/tool versions and remove or replace placeholders that conflict with the new API layout -- leave one coherent developer workflow.

**Acceptance Criteria:**
- Given a fresh checkout and documented prerequisites, when the documented setup is followed, then the React SPA, Litestar API, and PostgreSQL start successfully and the web production build succeeds.
- Given the running SPA, when it calls its API client, then every request uses the configured same-origin `/api/v1` JSON boundary and no server secret is bundled into the client.
- Given valid server configuration, when the API starts, then pending migrations complete before traffic is accepted and request/error events are structured.
- Given a new or reset database, when the fixture command is run repeatedly, then it creates the same fictional profile, mutual-match, and gesture test data without frontend duplicates.
- Given a required API setting is absent or an `/api/v1` route is unknown, when a request/startup occurs, then the failure is machine-readable, non-secret-bearing, and conforms to the error contract.

## Design Notes

Keep the first browser surface deliberately minimal: its job is to prove the real boundary, not pre-build Story 1.4. The API health response is a foundation contract, for example:

```json
{"data":{"service":"horse-tinder-api","version":"v1"}}
```

Use a migration and fixture command that can be run independently in development and automatically in the API startup path where appropriate. Fixture identities must be stable enough for future API and manual test assertions.

## Verification

**Commands:**
- `uv run pytest` -- expected: API configuration, contract, migration, and fixture tests pass.
- `uv run ruff check .` -- expected: project Python files satisfy configured lint rules.
- `npm --prefix apps/web run build` -- expected: SPA production build completes without server environment leakage.
- `docker compose up --build` (or documented equivalent) -- expected: PostgreSQL, API, and SPA become reachable using the documented local workflow.

## Suggested Review Order

**API boundary and startup**

- Centralizes versioned routing, structured logging, safe startup failures, and JSON errors.
  [`main.py:70`](../../apps/api/app/main.py#L70)

- Keeps browser requests same-origin and constrained to the versioned API base.
  [`api.ts:1`](../../apps/web/src/api.ts#L1)

**Database authority**

- Applies the recorded schema revision before the API accepts traffic.
  [`migrations.py:12`](../../apps/api/app/db/migrations.py#L12)

- Loads stable fictional profiles, reciprocal gestures, and the mutual-match fixture path.
  [`fixtures.py:22`](../../apps/api/app/db/fixtures.py#L22)

**Local runtime and verification**

- Wires PostgreSQL 18, API, and SPA into the documented local stack.
  [`compose.yaml:1`](../../compose.yaml#L1)

- Exercises configuration, error-contract, startup-log, migration, and fixture guarantees.
  [`test_foundation.py:12`](../../apps/api/tests/test_foundation.py#L12)
