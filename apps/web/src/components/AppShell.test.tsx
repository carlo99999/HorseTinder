import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { AppShell, UnavailableDestination } from "./AppShell";

describe("AppShell", () => {
  it("provides a skip link and semantic current primary navigation", () => {
    const html = renderToStaticMarkup(
      <AppShell activeDestination="profile" onNavigate={vi.fn()}><p>Profile content</p></AppShell>,
    );

    expect(html).toContain('href="#main-content"');
    expect(html).toContain('id="main-content"');
    expect(html).toContain('aria-label="Primary navigation"');
    expect(html).toContain('aria-current="page"');
    expect(html).toContain("Discovery");
    expect(html).toContain("Matches");
    expect(html).toContain("Profile content");
  });

  it.each(["Discovery", "Matches"] as const)("is honest when %s is unavailable", (destination) => {
    const html = renderToStaticMarkup(<UnavailableDestination destination={destination} />);

    expect(html).toContain(`${destination} is not available yet.`);
    expect(html).toContain("There are no profiles or matches to browse here yet.");
  });
});
