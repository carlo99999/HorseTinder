---
title: 'Use a polished, original app shell'
type: 'feature'
created: '2026-09-03'
status: 'done'
review_loop_iteration: 0
baseline_commit: '5b6e95128bac31b8ad138590ab5c3f25b44caa97'
context:
  - '_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Horse Tinder now has secure entry and private profiles but remains a bare form without coherent navigation, responsive layout, or the accessibility foundation needed by later features.

**Approach:** Wrap authenticated surfaces in an original, responsive three-area shell. Keep Profile fully functional, and make Discovery and Matches honest unavailable placeholders until their stories supply real data.

## Boundaries & Constraints

**Always:** Use original warm-stable branding, copy, shapes, and CSS tokens; never use Tinder marks, flame imagery, or trade dress. Show Discovery, Matches, and Profile in a desktop centered top bar and mobile bottom navigation. Include a keyboard-visible skip link, semantic active navigation (`aria-current`), accessible names, non-color-only selected state, visible focus, 44px primary targets, reduced-motion support, forced-colors resilience, and reflow without avoidable horizontal scrolling at 200% text/400% zoom. Keep existing auth, sign-out, profile-save, and expired-session recovery behavior intact.

**Ask First:** Adding a router, third-party component/icon library, image assets, animations beyond restrained CSS, or implementing any Discovery/Matches product behavior.

**Never:** Add backend endpoints, fake profile/match data, full Discovery/Matches functionality, location/payment/public-feed features, or navigation that conceals profile setup errors.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Authenticated navigation | Keyboard, pointer, mobile, or desktop player selects a primary destination | Current view changes within the shell and active navigation is programmatic and visibly distinct | Discovery/Matches state clearly explains that feature is not yet available |
| Profile operation | Authenticated profile form is opened in the shell | Existing create/edit, save, inline errors, and sign-out behavior remain reachable | Loading, failed save, and expired-session states remain labelled and preserve safe input |
| Reflow/accessibility | Skip-link, keyboard, reduced-motion, forced-colors, or zoom user | Main content can be reached and controls remain operable/legible without horizontal overflow | State never relies only on color or motion |

</frozen-after-approval>

## Code Map

- `apps/web/src/main.tsx` -- current stateful auth/profile flow is the integration point; preserve its API/state recovery while extracting shell/page composition.
- `apps/web/src/api.ts` -- existing same-origin auth/profile client needs no new backend contract.
- `apps/web/src/` -- add local shell/navigation components and global CSS; no router, asset library, or external design system exists.
- `apps/web/src/api.test.ts` -- retain transport tests; add lightweight shell semantics tests if current Vitest environment supports them.
- `apps/web/vite.config.ts` -- current Vite configuration needs no topology change.

## Tasks & Acceptance

**Execution:**
- [x] `apps/web/src/components/` and `apps/web/src/main.tsx` -- add an authenticated AppShell, primary navigation, skip link, and local destination state around existing Profile behavior -- establishes reusable information architecture without inventing later features.
- [x] `apps/web/src/styles.css` and `apps/web/src/main.tsx` -- implement original responsive tokens/layout, desktop top bar, mobile bottom navigation, focus/reduced-motion/forced-colors/reflow rules -- creates the visual and accessibility foundation.
- [x] `apps/web/src/api.test.ts` and/or focused shell tests -- cover active navigation, unavailable destination honesty, and retained Profile surface behavior where supported -- protects the shell contract.
- [x] `README.md` -- document manual accessibility verification expectations if developer workflow changes -- makes non-automated checks reproducible.

**Acceptance Criteria:**
- Given mobile or desktop authenticated players, when they use primary navigation, then Discovery, Matches, and Profile follow the specified responsive pattern and Profile retains its secure working flow.
- Given keyboard, zoomed, forced-colors, or reduced-motion users, when they navigate the shell, then controls have accessible names, visible focus/current state, skip-to-main behavior, and usable reflow without color-only meaning.
- Given unavailable Discovery or Matches destinations, when selected, then the player receives a clear honest placeholder rather than mock data or broken controls.

## Design Notes

Use local React state rather than a router: the shell has three predictable top-level destinations and only Profile has implemented product content. The nav should be a semantic list of buttons; inactive destinations use concise “coming soon” copy, not fake cards.

## Verification

**Commands:**
- `npm --prefix apps/web test -- --run` -- expected: client and shell semantics tests pass.
- `npm --prefix apps/web run build` -- expected: production SPA compiles.

**Manual checks:**
- Keyboard, 200% text, 400% zoom, reduced-motion, and forced-colors inspection -- expected: skip link, focus, navigation, Profile form, and reflow remain usable.

## Suggested Review Order

**Shell structure**

- Establishes skip-to-main, responsive primary navigation, and honest unavailable destinations.
  [`AppShell.tsx:1`](../../apps/web/src/components/AppShell.tsx#L1)

**Responsive accessibility styling**

- Implements original tokens, mobile/desktop layout, focus, motion, forced-colors, and reflow rules.
  [`styles.css:1`](../../apps/web/src/styles.css#L1)

**Shell behavior verification**

- Covers skip link, semantic active navigation, and unavailable destination copy.
  [`AppShell.test.tsx:1`](../../apps/web/src/components/AppShell.test.tsx#L1)
