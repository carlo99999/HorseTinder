---
title: 'Create and manage a Horse Profile'
type: 'feature'
created: '2026-09-03'
status: 'done'
review_loop_iteration: 0
baseline_commit: '9c72d7e8bf4d02ab517663f511cb07726668f143'
context:
  - '_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Authenticated players can enter the stable but cannot yet create the fictional identity required for Discovery, while existing fixture profiles have no secure account ownership boundary.

**Approach:** Add an owner-scoped Horse Profile API and replace the authenticated placeholder with an accessible setup/edit form that persists only public fictional fields.

## Boundaries & Constraints

**Always:** Derive the owning Account only from the validated cookie session and require its session CSRF capability for profile mutations. Each Account owns at most one persistent profile; new player profiles must have an owner, while existing deterministic fixture profiles remain unowned and usable for later discovery. Store and return only display name, image URL, short bio, trait, UUID, and UTC timestamps as profile data; never include account email, password hash, session data, or arbitrary client-selected ownership IDs. Validate all four fields server-side with field-specific standard error details.

**Ask First:** Accepting image uploads or external media hosting, changing the fixture identities/data, adding profile visibility controls, or collecting any additional account/personal information.

**Never:** Let a player read or edit another Account’s private `/me` profile, create a second profile through repeated requests, trust browser ownership state, or add Discovery, navigation-shell, or public-profile screens.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| First setup | Authenticated Account without a profile and valid four-field form | One owner-linked Profile persists and the same public DTO is returned | Invalid fields retain browser values and return linked field errors |
| Edit | Authenticated owner with valid replacement fields | Only that owner’s existing Profile updates and survives a new session | A failed save leaves the current values visible with a recoverable message |
| Ownership / repeat create | Missing session, invalid CSRF, client-supplied ownership, or second create | No profile data or mutation beyond the actor’s one profile | Standard unauthorized/CSRF/conflict error; no cross-account data exposure |
| Expired session | Safe setup values entered when session is no longer valid | Form values remain visible and UI directs the player to sign in | Do not discard safe input or report a false save success |

</frozen-after-approval>

## Code Map

- `apps/api/app/db/models.py:32-40` -- existing public profile fields need nullable fixture-safe `account_id` ownership plus a unique Account constraint; retain fixture-compatible public fields.
- `apps/api/app/db/migration_versions/` and `apps/api/app/db/migrations.py:13-18` -- add an ordered forward-only ownership revision without rewriting foundation/auth migrations.
- `apps/api/app/db/fixtures.py:33-91` -- deterministic profiles are intentionally unowned; preserve their identities and repeatable load behavior.
- `apps/api/app/auth/services.py:125-161` -- reuse the session-derived actor and session-CSRF validator; profiles must not parse ownership from request data.
- `apps/api/app/main.py:103-142` -- register new versioned profile handlers within existing JSON error/logging composition.
- `apps/api/app/profiles/` -- new feature-owned routes/services should contain validation, DTO projection, and all profile mutation logic.
- `apps/api/tests/test_auth.py` and new `apps/api/tests/test_profiles.py` -- reuse authenticated test-client helpers and add owner/CSRF/persistence/privacy coverage.
- `apps/web/src/api.ts:13-61` -- extend typed same-origin client with public profile DTO and CSRF-bearing `/profiles/me` calls.
- `apps/web/src/main.tsx:15-75` -- replace the authenticated Profile setup placeholder with labelled create/edit form states without prebuilding Story 1.4 shell.
- `apps/web/src/api.test.ts` -- preserve client boundary tests and cover profile request construction/failures.

## Tasks & Acceptance

**Execution:**
- [x] `apps/api/app/db/models.py`, `apps/api/app/db/migration_versions/`, and `apps/api/app/db/migrations.py` -- add fixture-safe account ownership and one-profile persistence constraint -- makes PostgreSQL the authority for ownership.
- [x] `apps/api/app/profiles/` and `apps/api/app/main.py` -- implement authenticated get/create/update `/api/v1/profiles/me` handlers through a profile service -- enforces actor-derived owner access and public DTOs.
- [x] `apps/api/tests/test_profiles.py` and applicable fixture/migration tests -- cover the matrix, persistence, one-profile rule, CSRF, and absence of private Account/session fields -- protects authorization and recovery boundaries.
- [x] `apps/web/src/api.ts`, `apps/web/src/main.tsx`, and `apps/web/src/api.test.ts` -- add typed profile calls and accessible labelled setup/edit UI with inline errors, focused error summary, loading state, and retained values -- turns entry into an actionable private profile flow.
- [x] `README.md` -- document profile API/manual verification where it changes the local developer workflow -- keeps the runnable stack discoverable.

**Acceptance Criteria:**
- Given an authenticated player without a profile, when valid display name, image URL, short bio, and trait are saved, then exactly one owner-linked profile persists and the player receives only its public fictional fields.
- Given an owner with an existing profile, when they edit valid fields, then the update persists across a new session and no other Account can access or modify it through owner-scoped endpoints.
- Given invalid setup input, a failed save, or expired authentication, when the player submits, then entered safe values remain visible with linked recoverable feedback and a sign-in path where required.
- Given a profile response, when it is returned or rendered, then it never contains account contact, credentials, session details, or a client-chosen owner identity.

## Design Notes

Keep seeded Discovery fixtures outside account ownership: nullable ownership preserves the canonical fixture path while a unique non-null `account_id` enforces one profile per real player. Use the existing `image_url` contract as a labelled URL field; uploads are deliberately out of scope.

## Verification

**Commands:**
- `uv run pytest` -- expected: foundation, auth, profile ownership, privacy, validation, CSRF, and migration tests pass.
- `uv run ruff check .` -- expected: backend profile feature meets lint policy.
- `npm --prefix apps/web test -- --run` -- expected: same-origin profile client behavior tests pass.
- `npm --prefix apps/web run build` -- expected: accessible profile UI compiles without server secrets.

## Suggested Review Order

**Ownership and persistence**

- Enforces one real-player profile while preserving unowned deterministic fixtures.
  [`models.py:32`](../../apps/api/app/db/models.py#L32)

- Adds the portable forward-only ownership migration.
  [`profiles_0003.py:1`](../../apps/api/app/db/migration_versions/profiles_0003.py#L1)

**Private API boundary**

- Derives owner access and validates public profile fields server-side.
  [`services.py:1`](../../apps/api/app/profiles/services.py#L1)

- Applies authenticated, CSRF-protected owner-scoped routes without cacheable private responses.
  [`routes.py:1`](../../apps/api/app/profiles/routes.py#L1)

**Profile experience and verification**

- Hydrates setup/edit state and preserves safe values on failures.
  [`main.tsx:15`](../../apps/web/src/main.tsx#L15)

- Covers ownership, privacy, validation, CSRF, and re-auth persistence.
  [`test_profiles.py:1`](../../apps/api/tests/test_profiles.py#L1)
