import { FormEvent, StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { ApiError, getAnonymousCsrf, getSession, register, signIn, signOut } from "./api";

function App() {
  const [mode, setMode] = useState<"register" | "sign-in">("register");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [csrfToken, setCsrfToken] = useState("");
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void Promise.all([getAnonymousCsrf(), getSession().then((value) => ({ value, error: null }), (error: unknown) => ({ value: null, error }))]).then(
      ([anonymousCsrf, current]) => {
        setCsrfToken(current.value?.data.csrfToken ?? anonymousCsrf.data.csrfToken);
        setAuthenticated(Boolean(current.value));
        if (current.error instanceof ApiError && current.error.failure.message.includes("expired")) setError(current.error.message);
        setLoading(false);
      },
      () => {
        setError("The stable gate is unavailable. Please refresh and try again.");
        setLoading(false);
      },
    );
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const result = mode === "register" ? await register(email, password, csrfToken) : await signIn(email, password, csrfToken);
      setCsrfToken(result.data.csrfToken);
      setAuthenticated(true);
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : "We could not open your stable. Try again.");
      const csrf = await getAnonymousCsrf().catch(() => null);
      if (csrf) setCsrfToken(csrf.data.csrfToken);
    } finally {
      setSubmitting(false);
    }
  }

  async function leave() {
    setSubmitting(true);
    setError("");
    try {
      await signOut(csrfToken);
      const csrf = await getAnonymousCsrf();
      setCsrfToken(csrf.data.csrfToken);
      setAuthenticated(false);
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : "We could not sign you out. Try again.");
      if (cause instanceof ApiError && cause.failure.code === "unauthorized") {
        const csrf = await getAnonymousCsrf().catch(() => null);
        if (csrf) setCsrfToken(csrf.data.csrfToken);
        setAuthenticated(false);
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main>
      <h1>Horse Tinder</h1>
      <p>An original fictional stable for future connections.</p>
      {loading && <p role="status">Preparing the stable gate…</p>}
      {error && <p role="alert">{error}</p>}
      {!loading && authenticated && <section aria-labelledby="profile-setup"><h2 id="profile-setup">Profile setup</h2><p>You’re securely signed in. Your private Horse Profile setup is next.</p><button type="button" onClick={() => void leave()} disabled={submitting}>{submitting ? "Signing out…" : "Sign out"}</button></section>}
      {!loading && !authenticated && <section aria-labelledby="entry-heading"><h2 id="entry-heading">Enter the stable</h2><div><button type="button" aria-pressed={mode === "register"} onClick={() => setMode("register")}>Register</button><button type="button" aria-pressed={mode === "sign-in"} onClick={() => setMode("sign-in")}>Sign in</button></div><form onSubmit={(event) => void submit(event)}><p><label htmlFor="email">Email address</label><input id="email" name="email" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} /></p><p><label htmlFor="password">Password</label><input id="password" name="password" type="password" autoComplete={mode === "register" ? "new-password" : "current-password"} minLength={12} required value={password} onChange={(event) => setPassword(event.target.value)} /></p><button type="submit" disabled={submitting || !csrfToken}>{submitting ? "Opening the stable…" : mode === "register" ? "Create account" : "Sign in"}</button></form></section>}
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
