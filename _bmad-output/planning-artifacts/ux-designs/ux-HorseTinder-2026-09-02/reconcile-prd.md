# PRD Reconciliation — Horse Tinder UX

**Input:** `../../prds/prd-HorseTinder-2026-09-02/prd.md`  
**Compared with:** `DESIGN.md`, `EXPERIENCE.md`  
**Verdict:** The UX contracts cover the core swipe, match, private chat, strike, gesture, Stable Plus, and safety loop. The following details are absent or underspecified in the UX spines.

1. **Profile setup and editing behavior is not specified.** FR-2 requires one persistent Horse Profile with a display name, image, short bio, and playful trait, editable only by its owner. The IA names Profile setup and profile control, but neither spine specifies the form fields, validation/error states, save feedback, or how editing is reached after onboarding.

2. **Horse Profile detail/visibility needs closure.** The PRD says only the fictional Horse Profile is presented to others, prohibits exposing contact details by default, and permits block/report from a Horse Profile. The current Swipe card is the only described profile presentation; no profile-detail surface or privacy treatment explains where a user reads the full profile, accesses profile-level safety controls, or sees that personal account data stays private.

3. **Chat message metadata is incomplete.** FR-7 requires every message to identify sender and sending time, while the Chat patterns cover composing, delivery failure, and match-row previews. The spines should state message ordering, sender attribution, timestamp presentation, and how persisted/reopened threads preserve those cues.

4. **Report completion feedback is underspecified.** The UX captures a report reason, but FR-11 also requires a stored report for the project owner to inspect. The reporter-facing flow should explicitly confirm report submission (separately from block confirmation) and clarify whether reporting alone changes the interaction; this prevents a user from assuming a report automatically blocked the account.

