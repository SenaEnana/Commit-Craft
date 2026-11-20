import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [repoPath, setRepoPath] = useState("");
  const [commitType, setCommitType] = useState("feat");
  const [scope, setScope] = useState("");
  const [isBreaking, setIsBreaking] = useState(false);
  const [message, setMessage] = useState("");
  const [body, setBody] = useState("");
  const [dateOffset, setDateOffset] = useState("");
  const [push, setPush] = useState(false);
  const [changes, setChanges] = useState([]);
  const [statusMsg, setStatusMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  async function handleCheckStatus() {
    setErrorMsg("");
    setStatusMsg("");
    try {
      const res = await fetch(
        `${API_BASE}/api/status?repo_path=${encodeURIComponent(repoPath)}`
      );
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to read repo status");
      setChanges(data.changes || []);
      setStatusMsg(`Found ${data.changes.length} changed file(s).`);
    } catch (err) {
      setErrorMsg(err.message);
    }
  }

  async function handleCommit(e) {
    e.preventDefault();
    setErrorMsg("");
    setStatusMsg("");
    try {
      const res = await fetch(`${API_BASE}/api/commit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_path: repoPath,
          commit_type: commitType,
          scope,
          is_breaking: isBreaking,
          message,
          body,
          date_offset: dateOffset,
          files: ["all"],
          push,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Commit failed");
      setStatusMsg(`Committed: ${data.commit_message}`);
      setMessage("");
      setBody("");
      await handleCheckStatus();
    } catch (err) {
      setErrorMsg(err.message);
    }
  }

  return (
    <main style={{ maxWidth: 680, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Commit Craft</h1>
      <p>Run Conventional Commits and backdated/future commits on any local repo.</p>

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          type="text"
          placeholder="Target repo path (e.g. C:\path\to\project)"
          value={repoPath}
          onChange={(e) => setRepoPath(e.target.value)}
          style={{ flex: 1, padding: 8 }}
        />
        <button type="button" onClick={handleCheckStatus}>
          Check Changes
        </button>
      </div>

      {changes.length > 0 && (
        <ul style={{ background: "#f5f5f5", padding: "10px 24px", borderRadius: 6 }}>
          {changes.map((item, idx) => (
            <li key={`${item.file}-${idx}`}>
              <strong>[{item.status}]</strong> {item.file}
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={handleCommit} style={{ display: "grid", gap: 12 }}>
        <div style={{ display: "flex", gap: 8 }}>
          <select value={commitType} onChange={(e) => setCommitType(e.target.value)} style={{ padding: 8 }}>
            <option value="feat">feat</option>
            <option value="fix">fix</option>
            <option value="docs">docs</option>
            <option value="refactor">refactor</option>
            <option value="chore">chore</option>
          </select>
          <input
            type="text"
            placeholder="Scope (optional, e.g. api, ui)"
            value={scope}
            onChange={(e) => setScope(e.target.value)}
            style={{ flex: 1, padding: 8 }}
          />
          <input
            type="text"
            placeholder="Date offset (e.g. -1d, +2d, 2026-11-19)"
            value={dateOffset}
            onChange={(e) => setDateOffset(e.target.value)}
            style={{ flex: 1, padding: 8 }}
          />
        </div>

        <input
          type="text"
          placeholder="Short commit message (required)"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
          style={{ padding: 8 }}
        />

        <textarea
          rows={3}
          placeholder="Optional detailed body..."
          value={body}
          onChange={(e) => setBody(e.target.value)}
          style={{ padding: 8 }}
        />

        <div style={{ display: "flex", gap: 16 }}>
          <label>
            <input
              type="checkbox"
              checked={isBreaking}
              onChange={(e) => setIsBreaking(e.target.checked)}
            />{" "}
            Breaking change (!)
          </label>
          <label>
            <input
              type="checkbox"
              checked={push}
              onChange={(e) => setPush(e.target.checked)}
            />{" "}
            Push to origin
          </label>
        </div>

        <button type="submit" style={{ padding: 10, cursor: "pointer" }}>
          Create Commit
        </button>
      </form>

      {statusMsg && <p style={{ color: "green", marginTop: 12 }}>{statusMsg}</p>}
      {errorMsg && <p style={{ color: "crimson", marginTop: 12 }}>{errorMsg}</p>}
    </main>
  );
}