import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { getHealth } from "./api";

function App() {
  void getHealth();
  return <main><h1>Horse Tinder</h1><p>An original fictional stable for future connections.</p></main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
