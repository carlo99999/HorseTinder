---
title: "Product Brief: Horse Tinder"
status: complete
created: 2026-09-02
updated: 2026-09-02
---

# Product Brief: Horse Tinder

## Summary

Horse Tinder is a responsive web app that parodies Tinder in a world where horses use phones, type with their fingers, and take romance dramatically seriously. It is a fun personal project rather than a commercial product. Users create real accounts, take on a horse persona, rapidly browse other horse profiles, match, and chat.

The experience should be recognizably Tinder-like but heightened into comedy: horses have almost no patience; lingering on a profile for more than three seconds can earn an “emotionally unavailable” strike; after three strikes, a red-flag badge appears. Matches can turn chat into an escalating contest of grand romantic gestures. The satirical premium tier, Stable Plus, promises message delivery and culminates in a real genie that grants wishes.

## Purpose and Audience

The primary goal is to build a polished, funny full-stack project that is enjoyable to demo and teaches its creator how to ship a modern application with authentication, stateful social interactions, and responsive UI.

The audience is anyone invited to try the joke: they should quickly understand the Tinder parody, laugh at the horse-specific mechanics, and be able to participate through a real account. This is not a real horse-breeding or animal-dating service.

## Core Experience

1. A visitor creates an account and enters the app.
2. They browse fictional, anthropomorphic horse profiles through a fast swipe interface.
3. Mutual positive swipes create a match and open a persistent chat.
4. The app makes impatience a game mechanic: delayed decisions can produce emotional-unavailability strikes and, after three, a visible red flag.
5. Matched horses can send messages and initiate increasingly ridiculous grand gestures.
6. Stable Plus provides intentionally shameless premium-comedy interactions, including its wish-granting genie.

## MVP Scope

**In**

- Responsive Tinder-parody interface for desktop and mobile.
- Real user accounts, sign-in, and authenticated sessions.
- Horse profile browsing, like/pass actions, and mutual-match creation.
- Persistent matches and one-to-one chat.
- Emotional-unavailability strike counter and three-strike red-flag state.
- A gesture escalation interaction in chat.
- Stable Plus/genie as a clearly comedic feature, not real payments.
- Seeded fictional horse profiles so the app is fun to try immediately.

**Out for v1**

- Real payment processing or subscriptions.
- A real-world horse marketplace, breeding workflow, or animal data.
- Native mobile apps.
- Complex recommendation algorithms, location matching, or public social feeds.
- Moderation systems beyond the minimum appropriate for a small invited demo.

## Technical Constraints

- React frontend and Litestar backend.

## Product Principles

- **Fast by design:** the UI must make a decision feel immediate.
- **Absurd, not confusing:** every gag should still support a clear app action.
- **The joke has a heart:** once matched, the chat should make room for playful, unexpectedly earnest romance.
- **Small but real:** real accounts and persisted data make this a credible full-stack project; the feature set stays contained.

## Success Signals

- A new user can sign up, swipe, match, and send a message without explanation.
- The app works comfortably on a phone and desktop browser.
- The main comic mechanics are encountered in one short demo session.
- The project demonstrates a working React + Litestar application with authenticated, persisted social interactions.

## Decisions Still Open

- [ASSUMPTION] Each account represents an adult, fictional anthropomorphic horse character; the profile-creation rules are still to be defined.
- [ASSUMPTION] Authentication provider, database, deployment target, and data-retention approach will be selected during architecture.

## Future Possibilities

If the MVP lands, extend the joke with richer profile customization, better gesture formats, read receipts that fail spectacularly, horse personality traits, or playful matching filters. These are deliberately deferred until the core loop works.
