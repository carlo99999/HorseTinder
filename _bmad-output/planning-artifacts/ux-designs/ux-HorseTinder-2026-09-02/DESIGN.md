---
name: Horse Tinder
description: "A polished, original swipe-app parody for fictional anthropomorphic horses."
status: final
sources:
  - ../../briefs/brief-HorseTinder-2026-09-02/brief.md
  - ../../prds/prd-HorseTinder-2026-09-02/prd.md
  - ../../prds/prd-HorseTinder-2026-09-02/addendum.md
updated: 2026-09-02
colors:
  surface: '#FFF9F0'
  surface-raised: '#FFFFFF'
  ink: '#211A16'
  ink-muted: '#6D625B'
  primary: '#5B3A29'
  primary-foreground: '#FFFFFF'
  accent-like: '#D85C4A'
  accent-pass: '#556E76'
  accent-magic: '#7656A8'
  border: '#E9DDD1'
  danger: '#A52A2A'
typography:
  display:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 32px
    fontWeight: '800'
    lineHeight: '1.1'
  title:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 22px
    fontWeight: '750'
    lineHeight: '1.2'
  body:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.45'
  label:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.2'
rounded:
  sm: 10px
  md: 16px
  lg: 24px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
  gutter-mobile: 16px
  gutter-desktop: 24px
components:
  primary-button:
    background: '{colors.primary}'
    foreground: '{colors.primary-foreground}'
    radius: '{rounded.full}'
  profile-card:
    background: '{colors.surface-raised}'
    radius: '{rounded.lg}'
    border: '{colors.border}'
  like-action:
    color: '{colors.accent-like}'
    radius: '{rounded.full}'
  pass-action:
    color: '{colors.accent-pass}'
    radius: '{rounded.full}'
  profile-setup:
    background: '{colors.surface-raised}'
    radius: '{rounded.md}'
    border: '{colors.border}'
  profile-detail:
    background: '{colors.surface-raised}'
    radius: '{rounded.lg}'
  timer-state:
    foreground: '{colors.ink-muted}'
  match-row:
    background: '{colors.surface-raised}'
    radius: '{rounded.md}'
  chat-composer:
    background: '{colors.surface-raised}'
    border: '{colors.border}'
  gesture-picker:
    background: '{colors.surface-raised}'
    radius: '{rounded.md}'
  red-flag-badge:
    background: '{colors.danger}'
    foreground: '{colors.primary-foreground}'
    radius: '{rounded.full}'
  block-report:
    background: '{colors.surface-raised}'
    radius: '{rounded.md}'
  match-reveal:
    background: '{colors.surface-raised}'
    radius: '{rounded.lg}'
  stable-plus-sheet:
    background: '{colors.accent-magic}'
    radius: '{rounded.lg}'
---

# Horse Tinder Design System

## Brand & Style

Horse Tinder should look like a finished consumer app, not a meme pasted onto a prototype. The presentation is warm, clean, direct, and confidently theatrical. The joke arrives in names, images, and moments of escalation; routine actions remain calm and legible.

[ASSUMPTION: the palette uses warm stable-like neutrals, deep brown for commitment, coral for positive action, muted blue for passing, and violet only for the genie.] This is an original visual system, not a reproduction of Tinder’s name, flame mark, colors, or trade dress.

## Colors

- `{colors.surface}` and `{colors.surface-raised}` create a bright, finished consumer-app canvas.
- `{colors.ink}` and `{colors.ink-muted}` carry ordinary reading and metadata; humor never depends on low contrast.
- `{colors.primary}` is reserved for committed actions such as continuing, saving, and sending.
- `{colors.accent-like}` and `{colors.accent-pass}` distinguish the two Swipe actions; labels/icons must accompany both.
- `{colors.accent-magic}` appears only on Stable Plus and genie moments.
- `{colors.danger}` is reserved for destructive confirmation and report/block states.

## Typography

Use `{typography.display}` for a Match reveal, genie outcome, and one screen-level headline. Use `{typography.title}` for Horse Profile names and Chat titles. Everything else uses `{typography.body}` or `{typography.label}`. Do not use novelty or horse-themed display fonts; polish comes from restraint.

## Layout & Spacing

The app is a centered, single-column experience. On mobile, the Swipe card occupies most of the viewport above a fixed action row; on desktop, it remains intentionally narrow rather than expanding into a dashboard. Use `{spacing.gutter-mobile}` on small screens and `{spacing.gutter-desktop}` on larger screens. The Match list and Chat keep readable line lengths.

## Elevation & Depth

Use one restrained shadow on an active `{components.profile-card}` and sheets/dialogs. Do not stack floating cards or use shadows as decoration. Motion and layering should make the current Swipe card feel tactile without obscuring the next action.

## Shapes

Use `{rounded.lg}` for Horse Profile imagery and major cards, `{rounded.md}` for panels and inputs, and `{rounded.full}` only for primary action controls, badges, and compact status chips. Avoid flame-shaped, hoof-shaped, or novelty containers.

## Components

- **Profile card:** image first; Horse Profile name, age/trait metadata, and bio remain readable over or beneath the image. Red-Flag Badge is visually secondary to the person.
- **Swipe actions:** paired, persistent, large touch controls; use `{components.like-action}` and `{components.pass-action}` plus explicit labels.
- **Match reveal:** a brief, celebratory overlay with a direct route to Chat and a less-prominent route back to discovery.
- **Chat composer:** anchored to the bottom of the Chat, with text entry, send action, and separate Gesture entry point.
- **Gesture card:** clearly identifies its sender and escalation level; it is amusing but cannot displace normal messages.
- **Stable Plus sheet:** visually distinct through `{colors.accent-magic}`, plainly states it is a joke, and contains no payment-style form fields.
- **Profile setup / detail:** use `profile-setup` and `profile-detail`; forms are calm raised surfaces and public profile content never resembles account settings.
- **`timer-state` / Red-Flag Badge:** use `timer-state` and `red-flag-badge`; the badge always pairs with plain explanatory text.
- **Match row / Chat composer / Gesture picker:** use their identically named component tokens; each is a quiet raised surface, with Gestures visually distinct from ordinary text.
- **Block/report / Match reveal:** use `block-report` and `match-reveal`; destructive decisions use clear labels rather than dramatic decoration.

All load-bearing text/control combinations meet WCAG AA: normal text is at least 4.5:1, large text at least 3:1, and focus/non-text action indicators at least 3:1 against adjacent surfaces.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Make the primary action obvious within one glance | Recreate Tinder branding or its flame iconography |
| Keep jokes in copy and product moments | Turn every component into a horse pun |
| Use explicit labels alongside color and icons | Encode like/pass, errors, or strikes only by color |
| Keep desktop focused around the card and Chat | Fill empty desktop space with unrelated panels |
| Use motion to clarify a completed Swipe or Match | Use prolonged, blocking animations |
