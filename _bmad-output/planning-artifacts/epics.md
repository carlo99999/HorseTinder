---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-01-requirements-confirmed
  - step-02-epics-approved
  - step-03-stories-created
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-HorseTinder-2026-09-02/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-HorseTinder-2026-09-02/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-HorseTinder-2026-09-02/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-HorseTinder-2026-09-02/EXPERIENCE.md
---

# HorseTinder - Epic Breakdown

## Overview

This document will decompose the approved PRD, architecture spine, and UX contract into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1: Visitors can create an Account, sign in/out, and access only authenticated state.

FR-2: An Account can create and edit one persisted Horse Profile with display name, image, bio, and trait.

FR-3: An authenticated Account can view eligible Horse Profiles and record like/pass Swipes without seeing itself or repeated choices.

FR-4: Mutual likes create one persisted Match visible to both Accounts; passes never create a Match.

FR-5: Discovery exposes a decision window; expiry may record a persisted, explained Emotional-Unavailability Strike.

FR-6: Only Match members can read or write their private Chat.

FR-7: Match members can send persisted messages with sender and time metadata.

FR-8: Match members can send seeded Gestures and answer one with a larger Gesture.

FR-9: Three Emotional-Unavailability Strikes display a non-blocking, explained Red-Flag Badge.

FR-10: Stable Plus presents a fake, payment-free genie outcome.

FR-11: An Account can block or report from a Horse Profile or Chat; blocks hide normal interactions and reports persist audit data.

FR-12: The product minimizes collected data, hides contact details, and uses original unaffiliated branding.

### NonFunctional Requirements

NFR-1: Primary Swipe, Match, and Chat flows work on current desktop and mobile browsers.

NFR-2: Core controls are keyboard-operable, accessible by name, and never encode state by color alone.

NFR-3: Server-side authorization protects authenticated data, Chat membership, and profile ownership.

NFR-4: Demo data and primary interactions remain responsive enough for a fast-swipe experience.

### Additional Requirements

- Use a modular monolith: React SPA communicates only with a Litestar JSON API under `/api/v1`.
- Use React 19.2, Vite 8.2, Litestar 2.24, and PostgreSQL 18.
- Backend feature services are the only mutation path; PostgreSQL is authoritative.
- Use UUIDs, ISO-8601 UTC API timestamps, versioned backend fixtures, and `{code,message,details?}` API errors.
- Use REST with active-chat polling in v1; no WebSockets, typing, read receipts, or push notifications.
- Use cookie-backed sessions, server-side ownership checks, same-origin SPA/API deployment, and CSRF protection for unsafe requests.
- Make swipe-to-match transactional; enforce blocks on discovery, Match, and Chat reads/writes; use idempotency keys for Chat messages.
- Validate environment config at API startup; run migrations before deployment; use structured request/error logs.

### UX Design Requirements

UX-DR-1: Implement the original DESIGN.md token system, component styling, WCAG-AA contrast targets, and original branding boundary.

UX-DR-2: Implement responsive single-column mobile/desktop IA with mobile bottom navigation and desktop top navigation.

UX-DR-3: Implement labelled, keyboard-operable Profile setup/detail forms with validation, save/error states, and private Account data separation.

UX-DR-4: Implement accessible Discovery card, like/pass actions, optional gesture Swipe, loading/empty/unavailable states, and visible focus transitions.

UX-DR-5: Implement opt-in Fast Mode with pause/untimed control; no Strike on pause; explain expiry and Red-Flag Badge state.

UX-DR-6: Implement Match reveal with Message/Keep swiping choices and deterministic focus behavior.

UX-DR-7: Implement Matches, accessible chronological Chat, send/retry state, seeded Gesture picker/escalation, and no forced scroll on incoming messages.

UX-DR-8: Implement block/report confirmation, reason capture, retry, privacy-safe feedback, and removal of blocked interactions.

UX-DR-9: Implement Stable Plus as a clearly fake, payment-free sheet with genie result and return action.

UX-DR-10: Implement accessibility floor: labelled dialogs, focus containment/return, skip link, current navigation semantics, live-region rules, reduced motion, zoom/reflow, and 44px primary targets.

UX-DR-11: Implement skeleton/loading, offline/retry, expired-session, and unauthorized state patterns without losing entered content.

### FR Coverage Map

FR-1: Epic 1 — account access.
FR-2: Epic 1 — Horse Profile creation and editing.
FR-3: Epic 2 — eligible-profile discovery and Swipes.
FR-4: Epic 2 — transactional mutual Matches.
FR-5: Epic 2 — Fast Mode and Emotional-Unavailability Strikes.
FR-6: Epic 3 — Match-gated Chat.
FR-7: Epic 3 — persisted messages.
FR-8: Epic 3 — Gesture escalation.
FR-9: Epic 2 — Red-Flag Badge after three Strikes.
FR-10: Epic 3 — Stable Plus genie payoff.
FR-11: Epic 4 — block and report.
FR-12: Epic 1 — private profile data and original branding boundary.

## Epic List

### Epic 1: Join the Stable

Players can sign in, create and manage a private-by-default fictional Horse Profile, and enter a polished, original app shell.

**FRs covered:** FR-1, FR-2, FR-12

### Epic 2: Find a Dramatic Match

Players can rapidly discover eligible Horse Profiles, Like or Pass them, create a mutual Match, and experience optional Fast Mode, Strikes, and the Red-Flag Badge.

**FRs covered:** FR-3, FR-4, FR-5, FR-9

### Epic 3: Turn a Match into Romance

Matched players can use private Chat, exchange persisted messages and escalating Gestures, and reach the payment-free Stable Plus genie payoff.

**FRs covered:** FR-6, FR-7, FR-8, FR-10

### Epic 4: Keep the Joke Safe

Players can block or report uncomfortable interactions while the app maintains privacy, accessible feedback, and a trustworthy invited-demo experience.

**FRs covered:** FR-11

## Epic 1: Join the Stable

Players can sign in, create and manage a private-by-default fictional Horse Profile, and enter a polished, original app shell.

### Story 1.1: Establish the runnable Horse Tinder foundation

As the builder,
I want a runnable React and Litestar application with its required data foundation,
So that players can use real, persisted features from the first user-facing story.

**Acceptance Criteria:**

**Given** a fresh checkout,
**When** the documented local setup is run,
**Then** the React 19.2/Vite 8.2 SPA and Litestar 2.24 API start with PostgreSQL 18,
**And** the SPA reaches only `/api/v1` JSON endpoints through the configured same-origin boundary.

**Given** API configuration or schema setup,
**When** the service starts or deploys,
**Then** required environment values are validated, migrations run before the API serves traffic, and structured request/error logs are emitted,
**And** secrets are never included in the SPA build.

**Given** demo data is loaded,
**When** the app is prepared for manual testing,
**Then** versioned backend fixtures create deterministic fictional Horse Profiles, a mutual-Match path, and Gesture data,
**And** fixture data is not duplicated as frontend-only constants.

### Story 1.2: Enter Horse Tinder securely

As a visitor,
I want to create an account, sign in, and sign out,
So that I can access my own Horse Tinder experience securely.

**Acceptance Criteria:**

**Given** a new visitor,
**When** they submit valid registration details,
**Then** the API creates an authenticated Account and cookie-backed session,
**And** the app routes them to Profile setup without exposing private data.

**Given** an unauthenticated visitor,
**When** they request a protected resource,
**Then** access is denied with the standard error shape or sign-in route,
**And** expired sessions preserve safe form input and explain that sign-in is required.

**Given** an authenticated player,
**When** they sign out or send an unsafe request,
**Then** the session is invalidated or the request requires a server-validated CSRF token,
**And** the acting Account is derived from the session rather than client input.

### Story 1.3: Create and manage a Horse Profile

As an authenticated player,
I want to create and edit my Horse Profile,
So that other players can meet my fictional horse persona without seeing my private account data.

**Acceptance Criteria:**

**Given** an authenticated player without a Horse Profile,
**When** they open Profile setup,
**Then** they can enter a display name, image, short bio, and playful trait,
**And** visible labels, required-state semantics, and linked validation errors are available.

**Given** valid profile input,
**When** the player saves,
**Then** the backend persists exactly one Horse Profile owned by their Account,
**And** the app shows a saved state and retains the profile after a new session.

**Given** invalid input or a save failure,
**When** the player submits the form,
**Then** entered values remain visible with a specific recoverable error,
**And** only the owning Account can edit that Horse Profile.

**Given** another player views the Horse Profile,
**When** it is returned by the API or rendered in the app,
**Then** it contains only public fictional profile fields,
**And** it never exposes account-only contact or session data.

### Story 1.4: Use a polished, original app shell

As an authenticated player,
I want a responsive Horse Tinder shell with clear navigation and accessible feedback,
So that the app feels complete on phone or desktop.

**Acceptance Criteria:**

**Given** a mobile or desktop player,
**When** they navigate the shell,
**Then** Discovery, Matches, and Profile use the specified navigation pattern,
**And** original tokens, visible focus, skip link, reduced motion, and non-color-only state are implemented.

**Given** a keyboard, zoomed, or forced-colors user,
**When** they navigate the shell,
**Then** every shell control has a visible accessible name and current-page state,
**And** the shell works at 200% text and 400% browser zoom without avoidable horizontal scrolling.

## Epic 2: Find a Dramatic Match

### Story 2.1: Browse and decide on Horse Profiles

As an authenticated player,
I want to Like or Pass eligible Horse Profiles,
So that I can quickly discover possible matches.

**Acceptance Criteria:**

**Given** a player with a Horse Profile,
**When** they open Discovery,
**Then** one eligible seeded Horse Profile appears with labelled Like and Pass controls,
**And** their own and previously decided profiles are excluded.

**Given** loading, empty, or unavailable Discovery data,
**When** the state occurs,
**Then** the UI shows the specified skeleton, empty, or recoverable state,
**And** keyboard focus moves to the next card heading after a decision.

**Given** a profile image or primary decision action,
**When** it renders in Discovery,
**Then** meaningful images have concise text alternatives and a labelled fallback on image failure,
**And** Like and Pass controls are labelled and at least 44×44 CSS pixels.

### Story 2.2: Create and view a mutual Match

As a player,
I want mutual Likes to create a Match,
So that I know when another horse likes me too.

**Acceptance Criteria:**

**Given** two Accounts have liked each other,
**When** the second Like is recorded,
**Then** one transactional, persisted Match is created and visible to both,
**And** duplicate requests cannot create duplicate Matches.

**Given** a new Match,
**When** the player is in Discovery,
**Then** a Match reveal offers Message or Keep swiping,
**And** it follows the specified focus and reduced-motion behavior.

**Given** the Match reveal opens or closes,
**When** the player uses a keyboard,
**Then** focus lands on its heading or Message action,
**And** dismissal returns focus to the invoking Like control while choosing an action moves focus to its destination heading.

### Story 2.3: Experience Fast Mode and the Red-Flag Badge

As a player,
I want to opt into Fast Mode and understand its consequences,
So that the impatience joke is funny rather than confusing.

**Acceptance Criteria:**

**Given** Discovery in default mode,
**When** a player opts into Fast Mode,
**Then** a visible timer and pause/untimed control appear,
**And** pausing never creates a Strike.

**Given** Fast Mode is enabled, paused, or returned to untimed mode,
**When** its state changes,
**Then** the control exposes its selected state programmatically,
**And** remaining time is available without relying only on the visual timer.

**Given** a Fast Mode expiry,
**When** the server records a Strike,
**Then** the player sees an explanation and continues to the next card,
**And** after three persisted Strikes their profile shows a non-blocking, explained Red-Flag Badge.

## Epic 3: Turn a Match into Romance

### Story 3.1: Open a private Match Chat

As a matched player,
I want to open my Match Chat,
So that I can talk only with the horse I matched.

**Acceptance Criteria:**

**Given** Match members,
**When** either opens the Match,
**Then** they can read its private persisted Chat,
**And** non-members receive no Chat content.

### Story 3.2: Send and receive Chat messages

As a matched player,
I want to send messages with honest delivery state,
So that the conversation feels real and reliable.

**Acceptance Criteria:**

**Given** an open Chat,
**When** a member sends text,
**Then** it persists with sender and UTC timestamp through an idempotent API request,
**And** active polling displays messages chronologically without forcing scroll.

**Given** send failure or offline state,
**When** it occurs,
**Then** draft text remains available with retry feedback,
**And** the UI never falsely claims delivery.

### Story 3.3: Escalate romance and meet the genie

As a matched player,
I want to send Gestures and visit Stable Plus,
So that the app delivers its ridiculous romantic payoff.

**Acceptance Criteria:**

**Given** a Match Chat,
**When** a member selects a seeded Gesture,
**Then** it is persisted and a member can answer with a larger Gesture,
**And** arbitrary user-authored Gesture media is unavailable in v1.

**Given** a player chooses a Gesture or escalation,
**When** selection changes,
**Then** the chosen Gesture state is exposed semantically,
**And** every Gesture control is keyboard-operable with an accessible name.

**Given** Stable Plus,
**When** a player opens it and chooses a wish,
**Then** they see a pre-authored genie result and return action,
**And** no payment data, subscription, or deceptive purchase interaction exists.

## Epic 4: Keep the Joke Safe

### Story 4.1: Block or report an interaction

As a player,
I want to block or report another horse from a profile or Chat,
So that I can leave an uncomfortable interaction safely.

**Acceptance Criteria:**

**Given** a Horse Profile or Chat,
**When** a player chooses Block,
**Then** confirmation clearly identifies the action and blocked Accounts disappear from Discovery, Matches, and Chat,
**And** the server enforces the block on every relevant read/write.

**Given** a player chooses Report,
**When** they supply a reason and submit,
**Then** reporter, reported Account, reason, and time persist for owner review,
**And** success, retry, and report-only feedback are clearly distinguished from Block.
