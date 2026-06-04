import { useState } from "react";

const MODES = [
  {
    value: "kurvenreich",
    label: "Kurvenreich",
    hint: "Bevorzugt kurvenreiche Neben- und Landstraßen",
  },
  {
    value: "sehr_kurvenreich",
    label: "Sehr kurvenreich",
    hint: "Maximale Kurven — Autobahnen und Schnellstraßen komplett gemieden",
  },
];

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function parseCoord(s) {
  const parts = s.split(",").map((v) => parseFloat(v.trim()));
  if (parts.length !== 2 || parts.some(isNaN)) return null;
  return parts;
}

export default function App() {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [mode, setMode] = useState("kurvenreich");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);

    const startPoint = parseCoord(start);
    const endPoint = parseCoord(end);

    if (!startPoint) {
      setError("Startpunkt ungültig — Format: lon,lat (z. B. 9.53, 47.14)");
      return;
    }
    if (!endPoint) {
      setError("Zielpunkt ungültig — Format: lon,lat (z. B. 9.67, 47.25)");
      return;
    }

    setLoading(true);
    try {
      const resp = await fetch(`${API_URL}/route`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ points: [startPoint, endPoint], mode }),
      });
      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`${resp.status}: ${text}`);
      }
      setResult(await resp.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const path = result?.paths?.[0];

  return (
    <main style={{ maxWidth: 500, margin: "2rem auto", fontFamily: "sans-serif", padding: "0 1rem" }}>
      <h1>fun-nav</h1>

      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <label>
          Start (lon, lat)
          <input
            type="text"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            placeholder="9.53, 47.14"
            required
            style={{ display: "block", width: "100%", marginTop: 4, padding: "0.4rem", boxSizing: "border-box" }}
          />
        </label>

        <label>
          Ziel (lon, lat)
          <input
            type="text"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            placeholder="9.67, 47.25"
            required
            style={{ display: "block", width: "100%", marginTop: 4, padding: "0.4rem", boxSizing: "border-box" }}
          />
        </label>

        <fieldset style={{ border: "1px solid #ccc", borderRadius: 4, padding: "0.5rem 1rem" }}>
          <legend>Kurvigkeits-Modus</legend>
          {MODES.map((m) => (
            <label
              key={m.value}
              style={{ display: "block", marginBottom: 6, cursor: "pointer" }}
            >
              <input
                type="radio"
                name="mode"
                value={m.value}
                checked={mode === m.value}
                onChange={() => setMode(m.value)}
              />{" "}
              <strong>{m.label}</strong>
              <span style={{ color: "#666", fontSize: "0.85em", marginLeft: 6 }}>
                — {m.hint}
              </span>
            </label>
          ))}
        </fieldset>

        <button
          type="submit"
          disabled={loading}
          style={{ padding: "0.5rem 1rem", cursor: loading ? "wait" : "pointer" }}
        >
          {loading ? "Berechne…" : "Route berechnen"}
        </button>
      </form>

      {error && (
        <p style={{ color: "crimson", marginTop: "1rem" }}>
          <strong>Fehler:</strong> {error}
        </p>
      )}

      {path && (
        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            background: "#f5f5f5",
            borderRadius: 4,
          }}
        >
          <h2 style={{ margin: "0 0 0.5rem" }}>Route berechnet</h2>
          <p style={{ margin: "0.25rem 0" }}>
            Distanz: <strong>{(path.distance / 1000).toFixed(1)} km</strong>
          </p>
          <p style={{ margin: "0.25rem 0" }}>
            Fahrzeit: <strong>{Math.round(path.time / 60000)} min</strong>
          </p>
          <p style={{ margin: "0.25rem 0", fontSize: "0.85em", color: "#666" }}>
            Modus: {MODES.find((m) => m.value === mode)?.label}
          </p>
        </div>
      )}
    </main>
  );
}
