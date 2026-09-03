# Architecture Spine Rubric Review

**Artifact:** `ARCHITECTURE-SPINE.md`  
**Lens:** Good-spine checklist  
**Verdict:** Needs revision before build handoff.

## Checklist Result

| Check | Result | Notes |
| --- | --- | --- |
| Fixes the meaningful one-level-down divergences | Partial | Module, API, state authority, and chat transport are well bound; safety and data-integrity seams remain unbound. |
| AD rules are enforceable and prevent their stated divergence | Partial | AD-1–AD-5 are usable; AD-6 does not address request forgery for cookie-authenticated mutations. |
| Deferred items cannot create incompatible units | Partial | Deployment/provider can safely wait, but blocking behavior and unique social-state constraints cannot. |
| Named technology is current and precisely bound | Partial | Vite is expressed as an `8.1 line`, not a concrete verified version. |
| PRD capabilities are covered | Partial | Core loop is mapped, but report inspection and block enforcement lack an ownership/enforcement rule. |
| Every altitude-owned dimension is decided/deferred/open | Partial | Operational provider is deferred, but baseline environments, migrations, logging, and deployment verification are silent. |

## Findings

### High — Cookie-backed session mutations lack a CSRF contract

AD-6 specifies `HttpOnly` cookie sessions and cookie attributes, but no CSRF token, Origin/Referer validation, or equivalent rule is required for unsafe requests. `SameSite=Lax` alone is not a sufficient mutation-defense contract. Independently built routes can therefore differ in their handling of forged cross-site POST/PATCH/DELETE requests.

**Autofix:** Extend AD-6 (or add an AD) to bind one server-enforced CSRF approach for every unsafe cookie-authenticated request, including the API-client behavior needed to send the proof.

### High — Blocking and matching have no database-level consistency contract

AD-3 establishes server authority, but it does not bind the rules that make social state consistent: a Match must be unique for an unordered pair of accounts; a duplicate Swipe must not create duplicate state; and an active Block must prevent discovery, new interaction, and access to the normal Chat path from either affected participant as required by FR-11. Different feature services/repositories could make incompatible choices here.

**Autofix:** Add an invariant for database constraints/idempotent commands and a single safety-policy check used by discovery, match, and chat reads/mutations. State the behavior for existing Match/Chat records after a block.

### Medium — Demo reachability is left to accidental seed behavior

The PRD success metric requires a new participant to reach a Match, while the architecture only says fixtures contain seeded profiles and gestures. It does not bind whether fixtures include backing Accounts and reciprocal likes, nor how the first-match demo path is deterministic. Discovery, fixtures, and test implementations can otherwise diverge and make the core demo loop unreliable.

**Autofix:** Bind a development/demo fixture contract (including the reciprocal-like/match path) or explicitly defer it with a revisit condition if manual fixture setup is intended.

### Medium — The operational envelope is too silent for a build substrate

The provider is reasonably deferred, but the spine does not decide, defer, or question minimum environments, schema migration execution, structured error logging, health checks, or deployment verification. Those are cross-module seams once an authenticated API and PostgreSQL database exist.

**Autofix:** Add a short operational invariant or explicit Deferred entries with a concrete revisit condition (before first hosted demo).

### Low — Vite version is not an exact verified dependency target

`Vite 8.1 line` is a release line rather than a version. This is weaker than the spine’s own pinned-version convention and gives scaffolders different valid selections.

**Autofix:** Pin the version actually verified, or state that the scaffold’s lockfile is authoritative and record the exact starter command/version there.

## Strengths

- The named modular-monolith paradigm is appropriate and clearly drawn.
- AD-1 through AD-5 prevent the most likely frontend/backend and polling-transport drift.
- The source map, structural seed, error envelope, and server-authoritative social-state rule are concise and useful.
