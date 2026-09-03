---
title: "PRD: Horse Tinder"
status: draft
created: 2026-09-02
updated: 2026-09-02
---

# PRD: Horse Tinder

## 0. Document Purpose

This PRD defines a small, funny, full-stack hobby project. It turns the approved [product brief](../../briefs/brief-HorseTinder-2026-09-02/brief.md) and brainstorm into testable behavior for later UX, architecture, and implementation. Technical choices live in the [addendum](addendum.md).

## 1. Vision

Horse Tinder is a responsive swipe-based dating-app parody set in a world of adult, fictional, anthropomorphic horses. It should feel familiar—create a profile, make a rapid decision, match, and chat—while treating horse impatience and extravagant romance as product mechanics.

It is a personal demo project, not a real-world breeding, animal-dating, or monetization service. A complete session should be funny without explanation, while demonstrating real accounts, persisted state, private messaging, and responsible defaults.

## 2. Target User

### 2.1 Jobs To Be Done

- As a player, I want to create a Horse Profile and enter the joke quickly.
- As a player, I want quick Swipe decisions and clear Match outcomes.
- As a matched player, I want private Chat and absurd Gestures, so romance becomes a comic loop.
- As the builder, I want a contained product that exercises authentication, persisted social state, and responsive UI.

### 2.2 Non-Users (v1)

- Real horses, breeders, stables, or animal-service customers.
- Anyone seeking payments, location-based dating, or a public social network.

### 2.3 Key User Journeys

- **UJ-1. Milo enters the parody.** [ASSUMPTION: Milo is an adult fictional horse persona.] Milo creates an Account, completes a Horse Profile, makes a fast positive Swipe, sees a Match, and enters a private Chat.
- **UJ-2. Milo escalates a Match.** In a Chat, Milo sends a message and a Gesture; the other participant can answer with a larger Gesture, visible in the same Chat.
- **UJ-3. Milo hits the impatience gag.** Milo lets the decision window expire enough times to receive an Emotional-Unavailability Strike and then a Red-Flag Badge, with an explanation of the comic cause.
- **UJ-4. Milo leaves an uncomfortable interaction.** From a Horse Profile or Chat, Milo blocks or reports another Account; that interaction no longer appears normally.

## 3. Glossary

- **Account** — Authenticated identity representing one adult fictional horse persona in v1.
- **Horse Profile** — Fictional dating profile controlled by an Account.
- **Swipe** — Like or pass decision on a Horse Profile.
- **Match** — Relationship created when two Accounts have liked each other.
- **Chat** — Private thread available only to the two Accounts in a Match.
- **Emotional-Unavailability Strike** — Comic state recorded after a slow Swipe decision.
- **Red-Flag Badge** — Visible profile state earned after three Emotional-Unavailability Strikes.
- **Gesture** — Deliberately absurd romantic action sent in a Chat and eligible for escalation.
- **Stable Plus** — Fake premium-comedy surface with no payment collection.

## 4. Features

### 4.1 Account and Horse Profile

**Description:** A visitor needs an Account and Horse Profile before accessing the Swipe deck. The app presents only the fictional Horse Profile to others. Realizes UJ-1.

#### FR-1: Account access

A visitor can create an Account, sign in, sign out, and access only their authenticated state.

**Consequences (testable):**

- Unauthenticated visitors cannot access Swipe, Match, or Chat data.
- Signing out ends the active session.

#### FR-2: Horse Profile creation

An authenticated Account can create and edit one Horse Profile with a display name, image, short bio, and playful trait.

**Consequences (testable):**

- The Horse Profile persists across sessions.
- Only its owning Account can edit it.

### 4.2 Fast Discovery and Match Creation

**Description:** The Swipe deck presents seeded fictional Horse Profiles without slowing the joke down. Mutual likes create a Match; passes do not. Realizes UJ-1 and UJ-3.

#### FR-3: Swipe deck

An authenticated Account can view eligible Horse Profiles one at a time and record a like or pass Swipe.

**Consequences (testable):**

- The current Account never sees its own Horse Profile.
- A prior Swipe is not shown again in the same deck state.

#### FR-4: Mutual Match

The system creates one Match when both Accounts have recorded a like Swipe for each other.

**Consequences (testable):**

- A Match persists and is visible to both Accounts.
- A pass Swipe cannot create a Match.

#### FR-5: Impatience mechanic

The Swipe experience visibly communicates a short decision window; expiry can record an Emotional-Unavailability Strike. [ASSUMPTION: three seconds is the initial window.]

**Consequences (testable):**

- Expiry lets the Account continue to another Horse Profile.
- The Emotional-Unavailability Strike count persists and is explainable in the UI.

### 4.3 Match Chat and Gesture Escalation

**Description:** Chat is a persistent space for two matched Accounts. It supports normal messages and a comedic Gesture interaction. Realizes UJ-1 and UJ-2.

#### FR-6: Match-gated Chat

Only the two Accounts in a Match can open its Chat, read messages, or send messages.

**Consequences (testable):**

- An Account cannot start a Chat without a Match.
- Chat content persists for both matched Accounts.

#### FR-7: Message delivery

An Account can send a text message in a Chat, and the other matched Account can see it.

**Consequences (testable):**

- Each message identifies its sender and sending time.
- Messages are never displayed outside their Match.

#### FR-8: Gesture and escalation

An Account can send a Gesture in a Chat; the other Account can answer with an explicitly larger Gesture.

**Consequences (testable):**

- The Chat records a Gesture and its escalation relationship.
- v1 provides a seeded, finite set of Gestures; users do not author arbitrary Gesture media.

### 4.4 Comedy States and Stable Plus

#### FR-9: Red-Flag Badge

After three Emotional-Unavailability Strikes, an Account’s Horse Profile displays a Red-Flag Badge.

**Consequences (testable):**

- The badge explains its comic cause in plain language.
- It does not prevent Swiping, matching, or Chat.

#### FR-10: Stable Plus genie gag

The app offers a Stable Plus screen that culminates in a wish-granting genie interaction.

**Consequences (testable):**

- The screen collects no money, payment details, or subscriptions.
- The genie produces a pre-authored comic result, not an external service or purchase.

### 4.5 Safety, Privacy, and Original Presentation

#### FR-11: Block and report

An Account can block or report another Account from a Horse Profile or Chat. Realizes UJ-4.

**Consequences (testable):**

- A blocked Account disappears from the blocker’s Swipe deck and normal Chat experience.
- A report stores reporter, reported Account, reason, and time for the project owner to inspect.

#### FR-12: Data and branding boundaries

The product collects only data needed for v1 and presents original branding, copy, logo, and assets.

**Consequences (testable):**

- The UI does not expose contact details by default or request unnecessary personal data.
- It states that it is unaffiliated with Tinder and uses no Tinder marks or logos.

## 5. Cross-Cutting NFRs

- Primary Swipe, Match, and Chat flows work on current desktop and mobile browsers.
- Core controls are keyboard-operable, have accessible names, and do not rely on color alone for state.
- Authenticated data access is authorized server-side; the client is not trusted to enforce Chat or profile ownership.
- A normal demo dataset and interactions feel responsive enough to preserve the fast-swipe premise.

## 6. Aesthetic and Tone

- Playful, theatrical, and affectionate—not cruel.
- Horses use phones and fingers in a fictional anthropomorphic world.
- Use original art direction; do not copy Tinder’s name, flame mark, or distinctive branded presentation.

## 7. Non-Goals

- Payments, subscriptions, or financial solicitation.
- Real animals, breeding, marketplace listings, or veterinary data.
- Location matching, recommendation algorithms, native apps, public feeds, or user-created Gesture media.
- Production-scale trust-and-safety operations.

## 8. MVP Scope

**In scope:** Account access; Horse Profile creation; seeded Horse Profiles; Swipes; mutual Matches; persistent Chat; Emotional-Unavailability Strikes; Red-Flag Badge; seeded Gestures; Stable Plus/genie; block/report; responsive original UI.

**Out of scope:** the Non-Goals above, plus advanced profile customization and matching filters, deferred until the core loop is enjoyable.

## 9. Success Metrics

- **SM-1:** In a manual demo, a new participant can create an Account, reach a Match, and send a Chat message without instruction. Validates FR-1–FR-7.
- **SM-2:** The same core loop works on one desktop and one mobile browser. Validates FR-3–FR-7 and the NFRs.
- **SM-3:** A participant encounters and understands at least one comic mechanic. Validates FR-5 and FR-8–FR-10.
- **Counter-metric:** Do not optimize retention, payments, or time-on-app at the expense of a small, funny build.

## 10. Open Questions

1. Which authentication provider, database, and deployment target should architecture choose?
2. Does every Account create a Horse Profile, or can some only browse seeded profiles?
3. How are Emotional-Unavailability Strikes reset, if at all?
4. What minimal owner workflow inspects reports during an invited demo?

## 11. Assumptions Index

- §2.3: Each Account represents one adult fictional anthropomorphic-horse persona.
- §4.2 / FR-5: The initial slow-decision window is three seconds.
- §4.3 / FR-8: Gestures are seeded, finite choices rather than user-authored media.
