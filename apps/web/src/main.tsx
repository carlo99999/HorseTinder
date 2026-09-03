import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { getHealth } from "./api";

function App() {
  const [status, setStatus] = useState<"loading" | "ready" | "failed">("loading");

  useEffect(() => {
    void getHealth().then(
      () => setStatus("ready"),
      () => setStatus("failed"),
    );
  }, []);

  return (
    <main>
      <h1>Horse Tinder</h1>
      <p>An original fictional stable for future connections.</p>
      {status === "loading" && <p role="status">Checking the stable gate…</p>}
      {status === "ready" && <p role="status">Stable gate is open.</p>}
      {status === "failed" && (
        <p role="alert">The stable gate is unavailable. Please refresh and try again.</p>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
