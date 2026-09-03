import { FormEvent, StrictMode, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { ApiError, createMyProfile, getAnonymousCsrf, getMyProfile, getSession, ProfileInput, register, signIn, signOut, updateMyProfile } from "./api";
import { AppShell, Destination, UnavailableDestination } from "./components/AppShell";
import "./styles.css";

const emptyProfile: ProfileInput = { displayName: "", imageUrl: "", bio: "", trait: "" };

function App() {
  const [mode, setMode] = useState<"register" | "sign-in">("register");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [csrfToken, setCsrfToken] = useState("");
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [profile, setProfile] = useState<ProfileInput>(emptyProfile);
  const [hasProfile, setHasProfile] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [profileExpired, setProfileExpired] = useState(false);
  const [destination, setDestination] = useState<Destination>("profile");
  const summaryRef = useRef<HTMLDivElement>(null);

  async function hydrateProfile() {
    try {
      const response = await getMyProfile();
      const { id: _, createdAt: __, updatedAt: ___, ...saved } = response.data;
      setProfile(saved);
      setHasProfile(true);
    } catch (cause) {
      if (cause instanceof ApiError && cause.failure.code === "profile_not_found") setHasProfile(false);
      else if (cause instanceof ApiError && cause.failure.code === "unauthorized") {
        setAuthenticated(false); setProfileExpired(true); setError("Your session has expired. Sign in to save your profile.");
      } else setError("We could not load your profile. Please refresh and try again.");
    }
  }

  useEffect(() => {
    void Promise.all([getAnonymousCsrf(), getSession().then((value) => ({ value, error: null }), (error: unknown) => ({ value: null, error }))]).then(
      async ([anonymousCsrf, current]) => {
        setCsrfToken(current.value?.data.csrfToken ?? anonymousCsrf.data.csrfToken);
        setAuthenticated(Boolean(current.value));
        if (current.value) await hydrateProfile();
        else if (current.error instanceof ApiError && current.error.failure.message.includes("expired")) setError(current.error.message);
        setLoading(false);
      },
      () => { setError("The stable gate is unavailable. Please refresh and try again."); setLoading(false); },
    );
  }, []);

  useEffect(() => { if (Object.keys(fieldErrors).length) summaryRef.current?.focus(); }, [fieldErrors]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setSubmitting(true); setError("");
    try {
      const result = mode === "register" ? await register(email, password, csrfToken) : await signIn(email, password, csrfToken);
      setCsrfToken(result.data.csrfToken); setAuthenticated(true); setProfileExpired(false); setDestination("profile");
      await hydrateProfile();
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : "We could not open your stable. Try again.");
      const csrf = await getAnonymousCsrf().catch(() => null);
      if (csrf) setCsrfToken(csrf.data.csrfToken);
    } finally { setSubmitting(false); }
  }

  async function saveProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setSubmitting(true); setError(""); setFieldErrors({});
    try { await (hasProfile ? updateMyProfile(profile, csrfToken) : createMyProfile(profile, csrfToken)); setHasProfile(true); }
    catch (cause) {
      if (cause instanceof ApiError) {
        setError(cause.message);
        if (cause.failure.code === "validation_failed") setFieldErrors((cause.failure.details ?? {}) as Record<string, string>);
        if (cause.failure.code === "unauthorized") { setAuthenticated(false); setProfileExpired(true); }
      } else setError("We could not save your profile. Try again.");
    } finally { setSubmitting(false); }
  }

  async function leave() {
    setSubmitting(true); setError("");
    try {
      await signOut(csrfToken); const csrf = await getAnonymousCsrf();
      setCsrfToken(csrf.data.csrfToken); setAuthenticated(false); setHasProfile(false); setProfile(emptyProfile); setFieldErrors({}); setProfileExpired(false);
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : "We could not sign you out. Try again.");
      if (cause instanceof ApiError && cause.failure.code === "unauthorized") {
        const csrf = await getAnonymousCsrf().catch(() => null); if (csrf) setCsrfToken(csrf.data.csrfToken); setAuthenticated(false);
      }
    } finally { setSubmitting(false); }
  }

  const updateField = (field: keyof ProfileInput, value: string) => {
    setProfile((current) => ({ ...current, [field]: value }));
    setFieldErrors((current) => { const { [field]: _, ...rest } = current; return rest; });
  };

  const profileForm = (authenticated || profileExpired) && <section className="content-panel" aria-labelledby="profile-heading">
    <p className="eyebrow">Your private stable</p>
    <h1 id="profile-heading">{hasProfile ? "Edit your Horse Profile" : "Set up your Horse Profile"}</h1>
    {profileExpired && <p className="session-notice" role="alert">Your session has expired. Your profile values are still here—sign in to save them.</p>}
    {Object.keys(fieldErrors).length > 0 && <div className="error-summary" ref={summaryRef} tabIndex={-1} role="alert"><p>Check the profile fields below.</p><ul>{Object.entries(fieldErrors).map(([field, message]) => <li key={field}><a href={`#${field}`}>{message}</a></li>)}</ul></div>}
    <form onSubmit={(event) => void saveProfile(event)} noValidate>
      <div className="form-field"><label htmlFor="displayName">Display name</label><input id="displayName" required aria-required="true" aria-invalid={Boolean(fieldErrors.displayName)} aria-describedby={fieldErrors.displayName ? "displayName-error" : undefined} value={profile.displayName} onChange={(event) => updateField("displayName", event.target.value)} />{fieldErrors.displayName && <span className="field-error" id="displayName-error">{fieldErrors.displayName}</span>}</div>
      <div className="form-field"><label htmlFor="imageUrl">Image URL</label><input id="imageUrl" type="url" required aria-required="true" aria-invalid={Boolean(fieldErrors.imageUrl)} aria-describedby={fieldErrors.imageUrl ? "imageUrl-error" : undefined} value={profile.imageUrl} onChange={(event) => updateField("imageUrl", event.target.value)} />{fieldErrors.imageUrl && <span className="field-error" id="imageUrl-error">{fieldErrors.imageUrl}</span>}</div>
      <div className="form-field"><label htmlFor="bio">Short bio</label><textarea id="bio" required aria-required="true" maxLength={500} aria-invalid={Boolean(fieldErrors.bio)} aria-describedby={fieldErrors.bio ? "bio-error" : undefined} value={profile.bio} onChange={(event) => updateField("bio", event.target.value)} />{fieldErrors.bio && <span className="field-error" id="bio-error">{fieldErrors.bio}</span>}</div>
      <div className="form-field"><label htmlFor="trait">Playful trait</label><input id="trait" required aria-required="true" aria-invalid={Boolean(fieldErrors.trait)} aria-describedby={fieldErrors.trait ? "trait-error" : undefined} value={profile.trait} onChange={(event) => updateField("trait", event.target.value)} />{fieldErrors.trait && <span className="field-error" id="trait-error">{fieldErrors.trait}</span>}</div>
      <div className="button-row"><button type="submit" disabled={submitting || !csrfToken || profileExpired}>{submitting ? "Saving profile…" : hasProfile ? "Save profile" : "Create profile"}</button></div>
    </form>
    {authenticated && <div className="button-row"><button className="secondary-button" type="button" onClick={() => void leave()} disabled={submitting}>{submitting ? "Signing out…" : "Sign out"}</button></div>}
  </section>;

  const entry = <section className="content-panel" aria-labelledby="entry-heading">
    <p className="eyebrow">An original fictional stable</p><h1 id="entry-heading">Enter the stable</h1>
    <p>Meet fictional, adult anthropomorphic horses. Horse Tinder is unaffiliated with Tinder.</p>
    <div className="mode-switch" aria-label="Entry mode"><button type="button" aria-pressed={mode === "register"} onClick={() => setMode("register")}>Register</button><button type="button" aria-pressed={mode === "sign-in"} onClick={() => setMode("sign-in")}>Sign in</button></div>
    <form onSubmit={(event) => void submit(event)}><div className="form-field"><label htmlFor="email">Email address</label><input id="email" name="email" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} /></div><div className="form-field"><label htmlFor="password">Password</label><input id="password" name="password" type="password" autoComplete={mode === "register" ? "new-password" : "current-password"} minLength={12} required value={password} onChange={(event) => setPassword(event.target.value)} /></div><div className="button-row"><button type="submit" disabled={submitting || !csrfToken}>{submitting ? "Opening the stable…" : mode === "register" ? "Create account" : "Sign in"}</button></div></form>
  </section>;

  const content = loading ? <p role="status">Preparing the stable gate…</p> : authenticated
    ? destination === "profile" ? profileForm : <UnavailableDestination destination={destination === "discovery" ? "Discovery" : "Matches"} />
    : profileExpired ? profileForm : entry;

  return authenticated ? <AppShell activeDestination={destination} onNavigate={setDestination}>{error && <p className="page-alert" role="alert">{error}</p>}{content}</AppShell>
    : <main id="main-content" className="app-main">{error && <p className="page-alert" role="alert">{error}</p>}{content}</main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
