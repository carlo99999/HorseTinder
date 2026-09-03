# Epic 1 Context: Join the Stable

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish the real, secure entry point for the Horse Tinder parody: a visitor can become an authenticated player, create a private-by-default fictional Horse Profile, and use an original responsive app shell. This turns the joke into a credible full-stack demo and supplies the account, profile, accessibility, and runtime foundations required by every later social feature.

## Stories

- Story 1.1: Establish the runnable Horse Tinder foundation
- Story 1.2: Enter Horse Tinder securely
- Story 1.3: Create and manage a Horse Profile
- Story 1.4: Use a polished, original app shell

## Requirements & Constraints

- A fresh checkout must run a React 19.2/Vite 8.2 SPA, Litestar 2.24 API, and PostgreSQL 18 with documented local setup. The SPA communicates only with same-origin `/api/v1` JSON endpoints.
- Validate all required API environment configuration at startup; run migrations before serving traffic; emit structured request and error logs. Never expose secrets to the SPA build.
- Versioned backend fixtures must create deterministic fictional Horse Profiles, a mutual-Match path, and Gesture data for manual testing. Frontend-only copies of fixture data are forbidden.
- Visitors can register, sign in, sign out, and reach only their own authenticated state. Protected data is unavailable without a valid session; sign-out invalidates the active session.
- Each authenticated Account can own exactly one persistent Horse Profile with display name, image, short bio, and playful trait. Only its owner may edit it. Public profile data contains only fictional profile fields, never account contact or session data.
- Profile setup must use visible labels, programmatic required state, linked inline validation errors, a focused error summary after invalid submission, and retained values on any save failure. Expired authentication should preserve safe form input and clearly direct the player to sign in.
- The application is a playful, adult-fictional-anthropomorphic-horse parody—not an animal breeding or real dating service. Use original name, copy, logo, colors, and assets; do not use Tinder marks, flame imagery, or distinctive trade dress. State unaffiliation and avoid payments, location features, public feeds, and unnecessary personal data.
- The shell must work on current desktop and mobile browsers. It must support keyboard operation, accessible names, visible focus, non-color-only meaning, a focusable skip link, reduced motion, semantic active-navigation state, 200% text, and 400% browser zoom without avoidable horizontal scroll.

## Technical Decisions

- Use a modular monolith: separate React SPA and Litestar JSON API runtime boundaries backed by PostgreSQL. The web app must not import server logic and the API must not serve feature UI.
- Organize backend code by feature; routes call that feature's service layer, and services are the exclusive mutation path. Keep persistence access within the owning feature rather than cross-feature direct writes.
- PostgreSQL is authoritative. Derive the actor from the authenticated session and verify ownership server-side; client UI state is never authorization.
- All endpoints live beneath `/api/v1`, use JSON DTOs, and return failures as `{code, message, details?}`. Resource names are plural kebab-case; Python uses snake_case; React components use PascalCase. Use UUID IDs and ISO-8601 UTC timestamps in API payloads.
- Use cookie-backed sessions: cookies are HttpOnly, Secure in production, and SameSite=Lax. Unsafe requests require a server-validated CSRF token. Production SPA and API share one origin; credentialed cross-origin CORS is not a v1 path.
- The planned structure is `apps/web` for the SPA and typed API client, `apps/api` for feature modules and database infrastructure, and `docs` for API/deployment notes. ORM and migration tooling may be selected during the API scaffold, but must preserve service ownership and PostgreSQL authority.

## UX & Interaction Patterns

- Mobile navigation is compact bottom navigation for Discovery, Matches, and Profile; desktop presents the same information structure in a centered top bar, never a sidebar. The experience remains centered and single-column, with a narrow stable reading width on desktop.
- Use the original warm stable palette and restrained system typography. Major imagery and cards use large rounded corners; setup panels and inputs use medium rounded corners; primary action controls use full pills. Routine interactions stay calm and legible; humor belongs in copy and fictional content rather than novelty UI.
- Auth, profile setup, detail, matches, and settings show a labelled inline loading state. Failed authentication, profile, or settings actions keep entered values visible and explain a specific recoverable next step. Unauthorized or unavailable direct links must not reveal another account's data.

## Cross-Story Dependencies

- Story 1.1 supplies the runnable runtime, PostgreSQL schema/migrations, configuration, logging, and deterministic fixtures required by every following story.
- Story 1.2 relies on the foundation and establishes the session/CSRF actor identity that Story 1.3 uses for single-profile ownership and that all later features must enforce.
- Story 1.3 provides the player profile prerequisite for Discovery. Story 1.4 establishes the shared navigation, responsive layout, and accessibility conventions used by Epic 2–4 surfaces.
