# Spine Pair Review — Horse Tinder

## Overall verdict

**Adequate, with high-impact contract gaps.** The pair gives downstream implementation a clear original visual posture, responsive IA, and an unusually complete set of core interaction states for a small parody app. It is not yet a dependable build contract because the source journeys are not all represented as flows and the two documents do not share a complete, consistently named component inventory.

## 1. Flow coverage — thin

Checked the four named journeys in `prd.md` §2.3 against `EXPERIENCE.md` §Key Flows. Every documented flow has a named protagonist, numbered steps, and a climax. Failure paths are provided for the safety-related flow through its explicit block/report steps; however, the source journey set is not fully covered and the only explicit send-failure treatment is in State Patterns rather than the first-match flow.

### Findings

- **high** The PRD's **UJ-3. Milo hits the impatience gag** has no corresponding Key Flow. `EXPERIENCE.md` covers expiry and three strikes as isolated State Patterns, but does not show the user completing that journey through the Red-Flag Badge outcome. (PRD §2.3; EXPERIENCE.md §State Patterns, §Key Flows.) *Fix:* Add a named, numbered impatience flow with the expiry/strike sequence, Badge climax, and an applicable failure/continuation state.
- **medium** Source journey names are not carried verbatim into the flow headings, making automated traceability weaker. For example, `UJ-1. Milo enters the parody` is represented as `Flow 1 — First Match`. (PRD §2.3; EXPERIENCE.md §Key Flows.) *Fix:* Prefix or cross-reference each flow heading with its UJ ID and source title.

## 2. Token completeness — adequate

All YAML color values are hex strings. Every `{…}` token reference in DESIGN.md and EXPERIENCE.md resolves to a defined path: colors, typography roles, spacing gutters, radii, or component objects. The system is intentionally light-mode-only for v1, so paired dark tokens are not required.

### Findings

- **medium** The contract does not state contrast targets or verify the load-bearing foreground/background pairs, despite defining primary, action, danger, and text colors used in critical controls. (DESIGN.md frontmatter; DESIGN.md §Colors; EXPERIENCE.md §Accessibility Floor.) *Fix:* State WCAG AA as the target and identify the required pairs, at minimum `{colors.primary}`/`{colors.primary-foreground}`, `{colors.ink}`/`{colors.surface}`, `{colors.ink-muted}`/`{colors.surface}`, and error/report text treatments.

## 3. Component coverage — broken

Checked each component named in DESIGN.md frontmatter/body and EXPERIENCE.md §Component Patterns. The documents describe useful individual components, but they do not form one shared inventory: several behavioral components have no visual specification, and several visual/token components have no named behavioral rule.

### Findings

- **high** The behavioral components `Profile setup`, `Profile detail`, `Timer state`, `Match row`, `Gesture picker`, `Red-Flag Badge`, and `Block/report` lack corresponding visual component specifications in DESIGN.md. (EXPERIENCE.md §Component Patterns; DESIGN.md §Components and frontmatter `components`.) *Fix:* Add visual rows/specifications for these components, or explicitly state that an existing named component owns each visual treatment.
- **high** The visual/token components `primary-button`, `like-action`, and `pass-action` lack identically named behavioral entries; `profile-card` also does not align exactly with the behavioral `Profile detail`. (DESIGN.md frontmatter `components`; EXPERIENCE.md §Component Patterns.) *Fix:* Adopt one canonical component-name vocabulary and give every tokenized component a behavior row, including keyboard/touch states and use constraints.
- **medium** `Match reveal`, `Chat composer`, and `Stable Plus sheet` are described in both spines, but their component names vary in casing and are not represented in DESIGN.md frontmatter tokens. (DESIGN.md §Components; EXPERIENCE.md §Component Patterns.) *Fix:* Normalize names and, where a component needs reusable visual tokens, add a frontmatter component entry.

## 4. State coverage — thin

Walked every IA surface for applicable cold-load, empty, focus, error, offline, and permission/safety states. Discovery, Matches, Chat, and key comedy/safety conditions are well covered. Auth, profile surfaces, Settings, report submission, and several loading/error boundaries are not specified enough for reliable implementation.

### Findings

- **high** Welcome/auth, Profile setup/detail, Matches, Settings, and Report/block confirmation lack defined cold-load and error treatments; auth also lacks invalid-credential/session-expiry behavior. (EXPERIENCE.md §Information Architecture, §State Patterns.) *Fix:* Add concise state rows for these surfaces, covering loading, validation/submission failure, not-found/unauthorized where relevant, and session expiry.
- **medium** Report flow has no submission-failure, validation, or duplicate-report state, and the genie flow has no outcome-loading/failure or return-state specification. (EXPERIENCE.md §Component Patterns, §State Patterns, §Key Flows.) *Fix:* Define non-deceptive failure/retry feedback for report submission and the complete Stable Plus outcome/return states.
- **medium** Offline/reconnection behavior is unspecified for profile saves, swipes, matching, and chat beyond a chat send failure. (EXPERIENCE.md §State Patterns.) *Fix:* State whether v1 disables these actions offline, queues them, or presents a recoverable retry state.

## 5. Visual reference coverage — strong

The workspace contains no `mockups/`, `wireframes/`, or `imports/` files. Therefore there are no visual artifacts requiring inline references and no orphaned files. Both spines appropriately stand as the visual/behavioral contract at this stage.

### Findings

- No findings.

## 6. Bloat & overspecification — strong

Both documents are concise and appropriate to a hobby responsive web app. DESIGN.md uses prose for rationale and tables/lists for rules; EXPERIENCE.md uses compact tables for IA, components, states, and breakpoints. The brief/PRD are referenced rather than duplicated, and the few implementation-adjacent statements (such as mobile keyboard behavior) are necessary behavioral constraints.

### Findings

- No findings.

## 7. Inheritance discipline — adequate

All three `sources` entries resolve from the UX workspace, and product terms such as Horse Profile, Match, Chat, Gesture, Stable Plus, Emotional-Unavailability Strike, and Red-Flag Badge match the PRD. Cross-spine token references resolve. The gaps are traceability and component naming consistency rather than broken source paths.

### Findings

- **medium** Key Flow titles omit the source UJ IDs/names, so the UJ inheritance is semantic rather than explicit. (PRD §2.3; EXPERIENCE.md §Key Flows.) *Fix:* Include the UJ ID and verbatim source name in each mapped flow heading.
- **high** Component names are not identical across Design tokens, Design prose, and Experience behavioral patterns. (DESIGN.md frontmatter and §Components; EXPERIENCE.md §Component Patterns.) *Fix:* Establish a shared component glossary/table and use its canonical names in both spines.

## 8. Shape fit — strong

DESIGN.md has all canonical sections in the required order: Brand & Style, Colors, Typography, Layout & Spacing, Elevation & Depth, Shapes, Components, and Do's and Don'ts. EXPERIENCE.md contains every required default section in the expected order and includes Responsive & Platform plus Inspiration & Anti-patterns, both warranted by a responsive multi-surface app using mainstream swipe-app behavior as a reference. The open-questions section is warranted for unresolved UX decisions.

### Findings

- No findings.

## Mechanical notes

- Frontmatter source paths resolve to the brief, PRD, and addendum.
- All discovered brace-token references resolve; no undefined DESIGN.md token paths found.
- No Mermaid diagrams are present.
- The documents remain `status: draft`, which is appropriate during the review gate; finalization should update both only after findings are triaged.
