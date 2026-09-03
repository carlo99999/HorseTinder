# Accessibility & Usability Review — Horse Tinder UX

**Verdict: revise before finalization.** The contracts establish a good accessibility baseline (labeled alternatives to swipe gestures, focus return, reduced motion, and live announcements), but the timed, automatic strike mechanism and several state-management details leave material keyboard and assistive-technology gaps for a consumer web app.

## High

### A11y-H1 — Timed decisions need a non-timed equivalent or a user control

The three-second timer automatically advances a card and assigns a strike. This can disadvantage people who need more time to read, use a screen reader, operate a switch/keyboard, process cognitive information, or recover from interruption. The contract calls the timer “non-alarming,” but does not provide pause, extension, disable, or an equivalent untimed route. This conflicts with the intent of WCAG 2.2.1 (Timing Adjustable) unless the time limit is genuinely essential, which is not established for a parody product.

**Fix:** Make Fast Mode an opt-in setting and default Discovery to no automatic expiry, or provide a persistent “Pause timer / use untimed discovery” control before and during the deck. Pausing or extending must not create a strike. Announce remaining time sparingly (not every second), preserve the current card while paused, and describe this behavior in Timer state, Interaction Primitives, Accessibility Floor, and Flow 1.

### A11y-H2 — Define focus outcomes when cards, overlays, and blocked items disappear

The spec says focus enters and returns from overlays, but not where it lands after Like/Pass, timer expiry, Match reveal dismissal, block confirmation, or a failed/send-retried message. Automatic card replacement can leave keyboard focus on a removed node; returning focus to a removed overflow trigger after blocking is also impossible.

**Fix:** Add deterministic focus rules: after a non-match decision, focus the next card’s heading (or its Like control); after closing a Match reveal, focus the destination heading/action selected; after block/report completion, move focus to the Matches heading or a confirmation landmark; after chat send failure, retain focus in the composer and preserve its value. Use programmatic focus only for these meaningful context changes, never for incoming chat messages.

### A11y-H3 — Live-region behavior needs roles, priority, and content rules

“Use concise live announcements” is a useful start but is too underspecified. Timer expiry/strike, match reveal, send progress, failed sending, report confirmation, and incoming messages can easily generate overlapping or overly verbose announcements. Announcing complete incoming messages can expose private content to people nearby using screen readers.

**Fix:** Specify a single polite status region for successful sends, matches, strikes, and non-urgent updates; use assertive alert behavior only for errors that block the immediate action. Do not announce countdown ticks or full message bodies. For new chat messages, announce sender and a short neutral cue such as “New message from Juniper”; expose full text through normal reading/navigation. Ensure visual status text remains in the DOM long enough to be announced.

## Medium

### A11y-M1 — Modal/dialog semantics and destructive confirmations are incomplete

One-level overlays and Escape are specified, but there is no requirement for `role=dialog`/`aria-modal`, an accessible dialog name/description, contained focus while open, a visible Close button, or what happens for an overlay with unsaved report text. Escape must not silently discard a report reason without a warning.

**Fix:** Require each dialog/sheet to have a labelled heading, a visible labelled close control, modal focus containment, and Escape behavior that either closes safely or asks before discarding entered report text. The final block/report confirmation should name the horse and clearly distinguish **Block**, **Report**, **Cancel**, and any reversible unblock route.

### A11y-M2 — Forms need explicit labels, semantic errors, and error recovery rules

Profile setup says “inline validation,” and Report asks for a reason, but neither specifies persistent programmatic labels, required indicators, error association, error summary/focus behavior, character limits, or submit-disabled logic. Placeholder-only controls and color-only inline errors would be easy implementation failures.

**Fix:** Require visible `<label>`-equivalent names for every form control, required status conveyed in text and programmatically, errors associated using `aria-describedby`, and an error summary that receives focus after an invalid submit. Keep user-entered values after validation/network errors. For report reasons, include a clearly labeled optional/required state, character count where limited, and a non-judgmental confirmation.

### A11y-M3 — Touch target and contrast requirements are qualitative, not testable

The documents say targets meet expectations and meaning is not color-only, but do not give a measurable minimum or require WCAG contrast ratios for normal text, labels on colored controls, focus indicators, borders/state indicators, and disabled controls. `accent-like`/`accent-pass` appear as action colors without defined icon/label foregrounds, making a low-contrast implementation plausible.

**Fix:** State a minimum 24×24 CSS px target (prefer 44×44 for primary Swipe, navigation, overflow, and destructive controls), at least 4.5:1 text contrast (3:1 for large text), 3:1 for actionable non-text indicators and focus outlines, and a focus indicator that remains visible against every surface. Define foreground/background pairs for Like, Pass, Magic, and Danger states; do not rely on a colored icon alone.

### A11y-M4 — Chat needs an accessible message-log and composer contract

Chronological display and non-forced scrolling are good, but the spec does not say how a screen-reader user identifies the conversation, sender boundaries, read/unread status, message grouping, gesture escalation, or send state. Enter/Return behavior is ambiguous across desktop and mobile keyboards.

**Fix:** Specify a labelled message-log region/list with each message exposing sender, timestamp, delivery state, and text in reading order; do not use visual alignment as the sole sender distinction. Give the composer a visible label and document that Enter sends only when the multiline control does not need it (e.g. explicit send button always works; Shift+Enter inserts a line break if supported). Keep new-message affordances keyboard reachable without moving a reader’s scroll position.

### A11y-M5 — Swipe-card imagery and dynamic content require alternatives and loading behavior

Profiles are image-first, but no alt-text policy is defined. Skeletons may be announced as content unless hidden; the automatic next-card swap needs a clear accessible card title/state without duplicate reading.

**Fix:** Require meaningful profile image alt text only when the image conveys profile information; otherwise use an empty alternative and make name/bio available as text. Mark decorative skeletons hidden from assistive technology. Give each active card a stable heading and avoid duplicating image, name, and action text in accessible names.

## Low

### A11y-L1 — Navigation and current location need an accessible convention

Bottom/top navigation is named, but current-page indication and an early skip-to-main-content mechanism are absent.

**Fix:** Add a visible-on-focus skip link and require the active navigation item to be indicated visually and with `aria-current="page"` (or equivalent semantic state).

### A11y-L2 — Honor additional user preferences beyond reduced motion

Reduced motion is covered, but forced colors/high contrast, zoom/reflow, and text scaling are not explicitly guarded. A single narrow column should hold up well, but this should be an acceptance criterion.

**Fix:** Require core flows to work at 200% text zoom and 400% browser zoom/reflow without horizontal scrolling (except inherently two-dimensional media), avoid fixed-height text containers, and preserve visible focus/state information in forced-colors modes.

### A11y-L3 — The red-flag badge needs neutral semantics and an accessible explanation on demand

It is described as secondary and non-penalizing, which is good, but status must not be exposed only through a badge/icon or surprise users as a stigmatizing announcement.

**Fix:** Render plain text such as “Emotional-unavailability strikes: 3” next to any icon, offer a labelled “Why am I seeing this?” disclosure, and announce the strike only when it changes as a result of the user’s action or timer choice.

## Positive coverage to retain

- Buttons have explicit action labels and gestures are optional.
- Focus return, reduced motion, and no forced chat auto-scroll are explicitly recognized.
- Block/report is reachable from both relevant contexts and report is not conflated with blocking.
- The fake premium flow avoids payment capture and deceptive purchase mechanics.
