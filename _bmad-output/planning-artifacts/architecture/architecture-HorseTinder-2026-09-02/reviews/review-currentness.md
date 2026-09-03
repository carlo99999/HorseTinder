# Currentness & Stack-Fit Review

**Verdict:** Changes required before finalization: the runtime-boundary/cookie rule needs a same-origin (or explicit cross-origin) deployment invariant. The version table is otherwise current enough, with Vite’s selected minor line now behind the newest stable minor.

## Sources checked (2026-09-02)

- [React versions](https://react.dev/versions): latest documented release line is React 19.2; the release list includes 19.2.7 (June 2026).
- [Vite 8 announcement](https://vite.dev/blog/announcing-vite8): Vite 8 was released 12 March 2026.
- [Vite 8.1 announcement](https://main.vite.dev/blog/announcing-vite8-1): Vite 8.1 was released 23 June 2026.
- [Vite releases](https://github.com/vitejs/vite/releases): reports Vite 8.2.0 after the 8.1 patch series.
- [Litestar changelog](https://docs.litestar.dev/2/release-notes/changelog.html): 2.24.0 released 11 June 2026.
- [Litestar PyPI](https://pypi.org/project/litestar/): latest release is 2.24.0.
- [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/): PostgreSQL 18 is supported; current minor is 18.6 and PostgreSQL recommends the current minor of a chosen major.

## Findings

### High — Cookie rule lacks a deployment-origin invariant

**Evidence:** AD-1 specifies a React SPA and Litestar API as separate runtime boundaries, while AD-6 mandates a `SameSite=Lax` session cookie. The SPA calls a relative `/api/v1` path, but the architecture neither binds the SPA and API to the same site/origin nor defines credentialed CORS and `SameSite=None; Secure` for a cross-site deployment.

**Impact:** A conventional deployment of the SPA and API on unrelated hosts would omit the `Lax` cookie from `fetch`/XHR API requests, so authenticated profile, swipe, match, and chat calls fail even though sign-in appears to succeed.

**Required correction:** Add an invariant such as: "Production exposes the SPA and `/api/v1` behind one HTTPS origin (or at minimum the same site) via a reverse proxy; cookie-authenticated CORS is not supported in v1." If separate cross-site origins are desired instead, explicitly bind an allowlisted credentialed-CORS policy, `fetch(..., { credentials: 'include' })`, CSRF protection, and `SameSite=None; Secure` cookies.

### Medium — Vite 8.1 line is not the current stable minor line

**Evidence:** Vite 8.1 is valid and stable, but the official release list now contains Vite 8.2.0. The project has no stated compatibility reason to pin an older minor.

**Impact:** The technical plan’s claim that the stack is "current" is slightly stale; a fresh scaffold may resolve to a newer 8.x version than the spine names.

**Recommended correction:** Change the table to `Vite | 8.2 (latest stable 8.x at review)` or state a bounded package policy such as `^8.2.0`, with the lockfile pinning the exact patch. If retaining 8.1, state why.

### Low — PostgreSQL version is valid but should express patch-upgrade policy

**Evidence:** `PostgreSQL | 18` correctly identifies a supported current major. The vendor’s current minor is 18.6 and recommends running the current minor within the selected major.

**Impact:** No immediate incompatibility; this is an operations clarity gap.

**Recommended correction:** Keep `18` as the major compatibility target and add that deployments track the current PostgreSQL 18 minor (18.6 at this review) through normal maintenance updates.

## Verified and compatible calls

| Item | Result |
| --- | --- |
| React 19.2 | Current documented major/minor line; suitable for the React SPA. |
| Litestar 2.24 | Latest release line; suitable for the JSON API and server-owned authorization rules. |
| PostgreSQL 18 | Supported current major; a good fit for transactional match creation and persistent chat state. |
| REST + active-chat polling | Consistent with the PRD’s deferred real-time transport and the UX’s honest delivery/failure states. |
| Modular-monolith feature ownership | Consistent with the hobby-project scope and with the requirements for server-authoritative social state. |

## Internal consistency notes

- The PRD leaves the database, authentication/session mechanism, and real-time transport to architecture; the chosen PostgreSQL, cookie sessions, and polling do not conflict with it.
- The UX makes Fast Mode opt-in and provides an untimed/pause control. The architecture does not bind timing behavior, so it remains compatible with that UX choice.
- The entity diagram is intentionally skeletal. Its one-to-one `ACCOUNT`–`HORSE_PROFILE` ownership agrees with the one-profile v1 requirement; implementation must still model the profile target of a `SWIPE` and the two members of a `MATCH`.
