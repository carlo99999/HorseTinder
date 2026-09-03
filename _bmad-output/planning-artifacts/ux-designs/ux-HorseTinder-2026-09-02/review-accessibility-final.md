# Accessibility & Usability Review — Final

**Scope:** `DESIGN.md` and `EXPERIENCE.md`, dated 2026-09-02  
**Verdict:** Pass with revisions before implementation. The contracts establish a strong, unusually complete accessibility floor for a hobby consumer app. No critical or high-severity blocker is present, but the implementation handoff should close the medium items below so the stated accessibility intent remains testable.

## Strengths

- Discovery is not drag-only: persistent labelled Like/Pass controls, keyboard operation, and an optional rather than mandatory swipe gesture make the core loop reachable.
- The timer gag is opt-in, can be paused/switched to untimed, does not penalize a pause, and avoids announcing every tick. This appropriately protects people who need more decision time.
- Dialog behavior is specified well: labelled heading, visible close affordance, focus containment, Escape behavior, focus return, and a warning before discarding report text.
- The documents cover common failure states, preserve entered content on error/offline, avoid false delivery claims, and give chat entries sender, timestamp, and delivery state in chronological order.
- Reduced motion, a focus-visible treatment, skip link, semantic current navigation, labelled controls, live-region discipline, zoom expectations, and non-colour-only Like/Pass distinctions are all explicitly addressed.
- The product rejects deceptive purchase interactions and does not make the comedy depend on inaccessible animation or colour cues.

## Findings

### Medium

1. **Define image text alternatives and fallback behavior.**
   Profile imagery is central to the card, but neither spine states whether it is decorative when a nearby textual profile name/traits already identify the horse, nor how user-supplied images receive an accessible name. Specify that a card image is `alt=""` only when its adjacent text fully supplies the identity and meaningful content; otherwise provide concise author-supplied alt text. Also specify a labelled, non-image fallback when an image fails to load. This closes WCAG 1.1.1 and makes the demo resilient.

2. **Resolve Match-reveal focus wording into a deterministic contract.**
   `Interaction Primitives` says focus moves “to the selected destination” after Match reveal, although the user has not yet selected a destination. The accessibility floor correctly says focus moves into overlays, but an implementer could follow either reading. State that opening Match reveal moves focus to its labelled heading (or the primary **Message** button); closing it without navigation returns focus to the invoking Like control, while choosing an action moves focus to the destination page heading.

3. **Give toggle/selection controls explicit state semantics.**
   Fast Mode/untimed, pause, and Gesture selection are important controls but only their visual/interaction behavior is described. Require native checkbox/switch/button patterns as appropriate, plus an exposed state (`aria-pressed`, `aria-expanded`, selected option semantics, or native control state). Ensure the current Fast Mode status and remaining time are programmatically available without relying on the visual timer.

4. **Set a measurable target-size rule for every interactive control.**
   The 44×44 CSS-pixel requirement currently applies to Like/Pass only; the generic “meet target-size expectations” statement is too loose for chat overflow, close buttons, report choices, navigation, and gesture chips. Require a minimum 44×44 CSS px pointer target or at least 24×24 px with sufficient spacing under WCAG 2.2’s target-size exception, and verify it at both breakpoints.

### Low

1. **Make colour-token contrast implementable.**
   The documents promise AA for load-bearing combinations, but `accent-like`, `accent-magic`, and surface tokens do not name foreground pairings. Add approved foreground/background pairings (and hover, disabled, and focus-indicator pairings) with tested ratios. In particular, do not assume white text will meet 4.5:1 over every accent.

2. **Specify readable timestamp and delivery-state text.**
   Require machine-readable `<time datetime>` values, human-readable local display, and text such as “Sent”, “Sending”, or “Failed” alongside any icon. This supports assistive technology and removes ambiguity when a message retry is offered.

3. **Add password and authentication input guidance.**
   The auth surface should use native labelled fields, appropriate `autocomplete` tokens (`username`, `new-password`, `current-password`), no clipboard restrictions, and an accessible show/hide-password control. This is small but prevents predictable account-flow friction.

4. **Set announcement priority for async Match vs. chat events.**
   “One polite status region” is a good baseline; clarify that a Match is announced once, while incoming chat activity announces only sender plus a short neutral notice when the chat is not active, never the message body. Do not interrupt a user composing or reviewing an older thread.

5. **Add a visible timeout warning only if Fast Mode’s countdown is later lengthened or made mandatory.**
   The current opt-in pause/untimed design is acceptable. Keep the explicit invariant that any future mandatory time limit needs an accessible extension/disable route before expiry rather than relying on the strike explanation afterward.

## Implementation Verification Checklist

- Keyboard-only test: sign in, setup, Like/Pass, Match reveal, Chat, Gesture, Block/Report, Stable Plus, and sign out; verify every focus transition above.
- Screen-reader test: confirm control names include the horse name where stated, dialogs announce heading and close control, status messages are concise, and chat does not disclose incoming message text unexpectedly.
- Zoom/reflow test at 200% text and 400% browser zoom on narrow and desktop viewports; verify navigation, chat composer, timers, and overlay actions remain operable without horizontal page scrolling.
- Reduced-motion test: card advance and Match/genie outcomes complete without animation and communicate their result through text/status.
- Contrast and target-size audit using final rendered styles, including disabled, hover, focus, destructive, and violet genie states.

## Severity Summary

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 4 |
| Low | 5 |

