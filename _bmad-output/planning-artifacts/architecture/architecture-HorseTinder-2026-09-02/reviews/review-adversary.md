# Adversarial Architecture Review

## Verdict: needs revision before independent implementation

The spine has a clear runtime split and a sound server-authoritative principle, but several independently compliant feature modules can still disagree on the same social-state transition. The gaps below can cause privacy failures, duplicate matches/messages, or a demo whose seeded profiles can never produce the advertised first match.

## High findings

### 1. Block state is not a mandatory authorization gate

**Compatible conflicting implementations:** `safety` records a `BLOCK(blocker_id, blocked_id)` and removes the account from its own discovery query. `chat`, correctly following AD-3, permits a message/read whenever the actor is a `MATCH_MEMBER`; `matches` lists every match membership. Both obey their own feature ownership and server-side membership checks, but the blocked account can still read, send to, or appear in the existing Chat/Match.

**Missing invariant:** Define one server-side visibility/interaction policy (owned by safety or a shared policy service) that discovery, match listing, chat reads, chat writes, and match creation must invoke. Define whether a one-way block hides a match for both participants, whether it permanently closes message writes, and whether it prevents any future match.

### 2. Swipe-to-match has no single owner, transaction, or pair uniqueness rule

**Compatible conflicting implementations:** `discovery` persists the actor's Like then calls `matches` to create a Match; meanwhile the other account likes in another request/tab. Both transactions observe reciprocal likes and each inserts a match. Alternatively, `discovery` concludes it owns all swipe side effects and inserts the match itself, violating AD-2, while `matches` expects a command it never receives.

**Missing invariant:** Assign ownership of the cross-feature orchestration (for example, `matches` owns `record_like_and_create_match`), require an atomic transaction, and enforce a canonical unordered-pair unique constraint. Specify its idempotent result so retries and concurrent Likes produce exactly one Match/reveal.

### 3. The seed/demo actor model cannot reliably satisfy mutual matching

**Compatible conflicting implementations:** Fixtures create profile-only seeded horses, while discovery correctly excludes the signed-in profile and exposes fixture profiles. No backing Account can submit the reciprocal Like, so FR-4's match never occurs. A separate implementation creates fixture Accounts but exposes them as ordinary credentialed users, or adds a frontend-only auto-match rule, each conflicting with the server-authoritative state rule.

**Missing invariant:** State whether every visible Horse Profile is backed by an Account and define ownership of deterministic demo reciprocity (fixture reciprocal swipes, a server-side scripted persona policy, or two demo accounts). It must be server-side and distinguish seeded/demo personas from interactive accounts without leaking authentication data.

### 4. Cookie sessions lack a cross-site mutation defense contract

**Compatible conflicting implementations:** A route accepts any cookie-authenticated `POST`, which obeys AD-6. An attacker page causes a logged-in browser to Like, block, report, or send a message. `SameSite=Lax` reduces some cases but is not a complete API mutation policy and is not an explicit substitute for CSRF verification.

**Missing invariant:** Bind cookie-authenticated unsafe methods to an origin check plus CSRF mechanism (or an explicitly documented same-origin custom-header strategy), and define CORS/allowed-origin behavior. Apply it uniformly through the API boundary.

## Medium findings

### 5. Chat delivery has no ordering, cursor, or idempotency contract

**Compatible conflicting implementations:** The polling endpoint returns timestamps sorted differently at equal precision; the client merges pages by arrival order. A retry after an ambiguous network failure posts the same text twice. Both comply with REST polling and server ownership, but users see duplicated or re-ordered messages.

**Missing invariant:** Define a server-assigned monotonically ordered message cursor per Match, cursor-based polling semantics, and a client-supplied idempotency key for message creation. The server response is the delivery source of truth.

### 6. Fast Mode expiry and Strike mutation are ambiguous across client timers/tabs

**Compatible conflicting implementations:** The web client calls `POST /strike` when its three-second timer ends; two tabs or a retry create multiple strikes for one profile. Another client calls `POST /pass` on expiry and the server records no strike. Both preserve PostgreSQL authority after the request, but do not agree on what event deserves a Strike.

**Missing invariant:** Bind the active deck item (or issued decision token) to a server-visible expiry and consume it once atomically; make expiry/pass/like mutually exclusive outcomes. State who decides expiry and how untimed/pause transitions affect an outstanding token.

### 7. Gesture escalation lacks a shared relation and validation rule

**Compatible conflicting implementations:** `chat` stores any chosen Gesture as a Message attachment. A `stable_plus` or fixture module supplies a larger-looking gesture, while the client decides whether it is an escalation based on display order. The system can record an alleged escalation that is not larger or that answers the wrong sender's Gesture.

**Missing invariant:** Put the finite Gesture catalog and rank/pairing policy under one owner; require an escalation command to reference an eligible prior Gesture message in the same Match, with the opposite member as actor, and persist the parent-message relationship.

## Lower finding

### 8. Profile image boundary is deferred but the v1 profile contract requires it

FR-2 requires an image, while image storage/moderation is deferred. Independently built profile/setup and API modules may choose URL strings, local uploads, or data URIs incompatibly. For an invited demo, bind a minimal v1 representation (for example selected fixture avatar ID or validated HTTPS URL) and defer uploads, rather than deferring the whole boundary.

## Recommended AD additions

1. A **Safety interaction policy** binding every social read/write to block status.
2. A **Match transition** AD assigning atomic reciprocal-like orchestration and canonical-pair uniqueness.
3. A **Demo persona** AD defining server-owned seeded profiles and reciprocal match behavior.
4. A **Mutation integrity** AD covering CSRF/origin protection, idempotency, and transaction semantics.
5. A **Chat/gesture event contract** binding ordered cursors, message idempotency, and valid escalation links.
6. A **Discovery decision lifecycle** AD binding issued cards, Fast Mode expiry, and exactly-once strikes.
