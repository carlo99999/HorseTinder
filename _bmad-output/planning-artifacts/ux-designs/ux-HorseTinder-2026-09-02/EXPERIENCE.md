---
title: "Horse Tinder Experience Specification"
status: final
sources:
  - ../../briefs/brief-HorseTinder-2026-09-02/brief.md
  - ../../prds/prd-HorseTinder-2026-09-02/prd.md
  - ../../prds/prd-HorseTinder-2026-09-02/addendum.md
updated: 2026-09-02
---

# Horse Tinder Experience Specification

## Foundation

Responsive web for mobile and desktop. `DESIGN.md` is the visual identity reference; this document owns behavior. The product is a polished, original swipe-app parody: fast in discovery, private in Chat, and funny without making core actions ambiguous. [ASSUMPTION: light mode is the v1 default; dark mode is deferred.]

## Information Architecture

| Surface | Reached from | Purpose |
|---|---|---|
| Welcome / auth | cold open | Sign up, sign in, explain the fictional premise briefly |
| Profile setup | first authenticated session, profile control | Create or edit the owner’s Horse Profile |
| Profile detail | Swipe card / Match / profile control | Read the full fictional Horse Profile and access profile-level safety controls |
| Discovery | successful setup, primary nav | Rapid Swipe deck of eligible Horse Profiles |
| Matches | primary nav / Match reveal | List existing Matches and enter a Chat |
| Chat | Match row / Match reveal | Private messages and Gestures for one Match |
| Stable Plus | profile or settings affordance | Fake premium-comedy genie experience |
| Settings | profile control | Account actions, original-parody disclaimer, sign out |
| Report / block confirmation | Horse Profile or Chat overflow | Safely leave or report an interaction |

Mobile uses a compact bottom navigation for Discovery, Matches, and Profile. Desktop uses the same information structure in a centered top bar; it does not introduce a sidebar. Dialogs/sheets never stack more than one level deep.

## Voice and Tone

Brand posture is in `DESIGN.md`. Microcopy is short, clear, and deadpan; the app treats impossible horse romance as entirely normal.

| Do | Don't |
|---|---|
| “A match. Try not to overthink it.” | “Congratulations!!!” |
| “Too slow. That’s one emotional-unavailability strike.” | “Error: timer expired.” |
| “This is a joke. No payment will be collected.” | Payment-like urgency or deceptive upsell copy |
| “Block this horse?” | Shame the user for blocking or reporting |

## Component Patterns

| Component | Behavior |
|---|---|
| Profile setup | Required fields are display name, image, short bio, and playful trait. Visible labels, programmatic required state, linked inline errors, and a focused error summary follow invalid submit; values persist on failure. |
| primary-button | Used for one committed action per view, including submit, send, and continue. It is keyboard-operable and never relies on color alone. |
| Profile detail | Shows the public Horse Profile, never contact details. `block-report` is reachable without exposing Account data. |
| profile-card / like-action / pass-action | One eligible Horse Profile at a time with persistent, labeled actions. Gesture Swipe is optional, never the only method. Primary controls are at least 44×44 CSS px. |
| timer-state | Discovery defaults to an untimed mode; Fast Mode is opt-in and has a persistent pause/untimed control. Pausing never adds a Strike. |
| match-reveal | Announces the Match and offers **Message** or **Keep swiping**; dismissal never loses the Match. |
| match-row | Shows Horse Profile summary, last message/gesture, and unread state without exposing content to others. |
| chat-composer | Has a visible label and send control. The message log exposes sender, timestamp, delivery state, and text in chronological reading order. |
| gesture-picker | Finite seeded Gestures; escalation is offered only in response to an existing Gesture. |
| red-flag-badge | Shows plain text "Emotional-unavailability strikes: 3" and a labelled explanation; it is not a usability penalty. |
| block-report | From profile and Chat overflow; block confirmation is reversible, report asks for a reason and confirms submission without implying a block. |
| stable-plus-sheet | Clearly fake, no payment fields, explicit genie result and return action. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Loading deck | Discovery | Skeleton profile card and disabled actions; never show an empty white card. |
| Authenticated-surface loading | Profile setup/detail, Matches, Settings | Use a labelled inline loading state; Profile detail uses a skeleton only for its image/card shape. |
| Unavailable surface | Direct Profile or Match link | Show a concise unavailable/unauthorized state and route back to Discovery or Matches; never reveal another Account’s data. |
| No eligible profiles | Discovery | “The stable is quiet.” Explain there are no new Horse Profiles and route to Matches. |
| Decision expiry | Discovery | Brief timer completion, Strike explanation, automatic advance; no blocking error dialog. |
| Three strikes | Profile / Discovery | Red-Flag Badge appears with explanatory copy; all normal functions remain available. |
| New Match | Discovery | Match reveal overlay; user chooses Message or Keep swiping. |
| Empty Matches | Matches | “No matches yet. The next dramatic entrance is in Discovery.” |
| Empty Chat | Chat | One clear prompt to send a message or Gesture. |
| Send failure | Chat | Keep unsent text visible, show retry affordance, and do not claim delivery. |
| Blocked interaction | Chat / Matches | Remove it from ordinary lists; show a short confirmation to the blocker only. |
| Stable Plus | Sheet | Declare the joke before genie outcome; no payment capture or purchase-looking button. |
| Auth / profile / settings failure | Relevant surface | Keep entered values; show a specific recoverable error. Expired sessions route to sign-in with a short explanation. |
| Report failure | Block/report | Preserve reason, offer retry, and distinguish failed submission from successful report or block. |
| Offline action | Any write surface | State that v1 cannot complete the action offline; preserve form/message input and offer retry on reconnection. |

## Interaction Primitives

- Tap/click paired actions to Like or Pass; keyboard users can reach and activate the same controls.
- On touch, optional horizontal Swipe gesture maps to the labeled action only after a threshold; provide undo only if later product scope allows it.
- After Like/Pass or expiry, focus moves to the next card heading; after Match reveal, focus moves to the selected destination; after block/report completion, focus moves to the Matches heading or confirmation landmark. Failed sends retain focus and value in `chat-composer`.
- Match reveal, report, and Stable Plus use one-level overlays and `Esc` closes the topmost dismissible overlay.
- Chat uses ordinary scroll behavior; receiving a message does not force-scroll a reader away from older messages.
- **Banned:** infinite profile auto-advance, hover-only actions, deceptive payment interactions, inaccessible drag-only gestures, and motion that delays a next decision.

## Accessibility Floor

- Every button has an accessible name that includes the Horse Profile name where relevant, e.g. “Like Juniper.”
- One polite status region announces successful sends, Matches, and Strikes; assertive alerts are reserved for blocking errors. It never announces countdown ticks or full incoming message bodies.
- Dialogs/sheets have labelled headings, visible close controls, contained focus, and a discard warning for entered report text.
- Focus order follows visible reading order; focus moves into overlays and returns to their trigger on close.
- Controls retain visible focus and meet target-size expectations; `{colors.accent-like}` and `{colors.accent-pass}` never carry meaning alone.
- Reduced-motion preference replaces card-flight and Match celebration animations with immediate state updates.
- Active navigation has a semantic current-page state; a skip link appears on focus. Core flows work at 200% text and 400% browser zoom without avoidable horizontal scrolling.

## Responsive & Platform

| Breakpoint | Behavior |
|---|---|
| `< 768px` | Full-width card within `{spacing.gutter-mobile}`; bottom navigation; Chat composer remains above the mobile keyboard. |
| `≥ 768px` | Centered reading column; profile card has a stable maximum width; top navigation; Chat does not become a multi-pane inbox. |

## Inspiration & Anti-patterns

- **Reference behavior:** familiar, rapid Swipe and clear Match feedback from mainstream swipe dating apps.
- **Keep original:** name, logo, colors, copy, imagery, and all branded visual details.
- **Reject:** real-world dating pressure, dark patterns, faux billing, location tracking, and public feeds.

## Key Flows

### Flow 1 — UJ-1. Milo enters the parody (Milo, on a phone between errands)

1. Milo signs in and completes his Horse Profile.
2. Discovery opens on one Horse Profile with labeled Like and Pass actions.
3. He selects Like; a mutual match is detected.
4. A Match reveal offers Message or Keep swiping.
5. He chooses Message and lands in the private Chat.
6. **Climax:** Milo sends the first line; the message appears in the Chat with an honest send state.

### Flow 2 — UJ-2. Milo escalates a Match (Milo, on desktop at home)

1. Milo opens a Match from Matches.
2. He reads the existing Chat and selects a seeded Gesture.
3. The other Account replies with an escalation.
4. The Chat makes the relationship between the two Gestures clear.
5. **Climax:** Milo sees the escalation in context without losing the ordinary message thread.

### Flow 3 — UJ-4. Milo leaves an uncomfortable interaction (Milo, receiving an unwanted message)

1. Milo opens Chat overflow.
2. He chooses Block or Report.
3. Block asks for confirmation; Report captures a reason.
4. **Climax:** the interaction disappears from Milo’s normal experience and a confirmation explains what changed.

### Flow 4 — The genie payoff (Milo, showing the app to a friend)

1. Milo opens Stable Plus from Profile or Settings.
2. The sheet plainly says it is a fake upgrade and collects no payment information.
3. He chooses a pre-authored wish.
4. The genie presents its comic result and a clear return to Discovery or Matches.
5. **Climax:** the joke lands as a finished product moment, not a dead-end upsell.

### Flow 5 — UJ-3. Milo hits the impatience gag (Milo, trying Fast Mode)

1. Milo opts into Fast Mode and sees the timer plus a persistent pause/untimed control.
2. He lets a card expire; the app explains the Strike and moves focus to the next card.
3. He repeats the choice until the third Strike appears.
4. **Climax:** his Horse Profile shows the Red-Flag Badge with a plain explanation, while Discovery remains usable.

Continuation: switching back to untimed Discovery keeps the current card available and adds no Strike.

## Open UX Questions

1. Should the timer always be three seconds, and do Emotional-Unavailability Strikes ever reset?
2. Which exact seeded Gestures ship in v1, and is their escalation a simple rank or authored pairing?
3. What is the minimal profile image policy for an invited demo?
4. Is dark mode desired after the core responsive experience is complete?
