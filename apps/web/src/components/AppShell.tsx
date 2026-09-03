import { ReactNode } from "react";

export type Destination = "discovery" | "matches" | "profile";

const destinations: ReadonlyArray<{ id: Destination; label: string }> = [
  { id: "discovery", label: "Discovery" },
  { id: "matches", label: "Matches" },
  { id: "profile", label: "Profile" },
];

type AppShellProps = {
  activeDestination: Destination;
  onNavigate: (destination: Destination) => void;
  children: ReactNode;
};

export function AppShell({ activeDestination, onNavigate, children }: AppShellProps) {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <header className="app-header">
        <a className="brand" href="#main-content" aria-label="Horse Tinder home">
          <span aria-hidden="true" className="brand-mark">HT</span>
          <span>Horse Tinder</span>
        </a>
        <PrimaryNavigation activeDestination={activeDestination} onNavigate={onNavigate} className="desktop-navigation" />
      </header>
      <main id="main-content" className="app-main" tabIndex={-1}>{children}</main>
      <PrimaryNavigation activeDestination={activeDestination} onNavigate={onNavigate} className="mobile-navigation" />
    </div>
  );
}

type PrimaryNavigationProps = Pick<AppShellProps, "activeDestination" | "onNavigate"> & { className: string };

export function PrimaryNavigation({ activeDestination, onNavigate, className }: PrimaryNavigationProps) {
  return (
    <nav className={className} aria-label="Primary navigation">
      <ul>
        {destinations.map(({ id, label }) => {
          const isCurrent = id === activeDestination;
          return <li key={id}>
            <button
              type="button"
              aria-current={isCurrent ? "page" : undefined}
              className={isCurrent ? "is-current" : undefined}
              onClick={() => onNavigate(id)}
            >
              <span aria-hidden="true" className="nav-marker">{isCurrent ? "●" : "○"}</span>
              <span>{label}</span>
            </button>
          </li>;
        })}
      </ul>
    </nav>
  );
}

export function UnavailableDestination({ destination }: { destination: "Discovery" | "Matches" }) {
  return (
    <section className="unavailable-panel" aria-labelledby={`${destination.toLowerCase()}-heading`}>
      <p className="eyebrow">The stable is growing</p>
      <h1 id={`${destination.toLowerCase()}-heading`}>{destination}</h1>
      <p>{destination} is not available yet. We&apos;re preparing this part of the stable for a future visit.</p>
      <p className="quiet-note">There are no profiles or matches to browse here yet.</p>
    </section>
  );
}
