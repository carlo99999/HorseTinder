# Horse Tinder — Technical Plan

The app has two parts: a React frontend that renders the swipe and chat experience, and a Litestar backend that owns all real data and rules. They talk through `/api/v1` JSON endpoints.

PostgreSQL stores accounts, horse profiles, swipes, matches, messages, gestures, strikes, blocks, and reports. The browser never decides whether a user matched or can read a chat—the backend checks the signed-in account on every request.

Build feature-by-feature: auth/profile first, then seeded discovery and swipes, then mutual matches and chat, then strikes/gestures/genie, then safety controls. Chat starts with polling while open; no websocket complexity is needed for v1.

The key rule: each backend feature owns its writes. A chat route never edits a Match directly, and React only updates optimistic UI after the server confirms the action.
