import { useState } from "react";
import "./index.css";

// Automatically uses local FastAPI on Windows/Mac/Linux, or your Codespace backend when in Codespaces
const API_BASE = window.location.hostname.endsWith(".app.github.dev")
  ? window.location.origin.replace("-5173.", "-8000.")
  : "http://127.0.0.1:8000";
// the above will be updated with real url when deployed

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
    <div className="commit-page">
      <main className="commit-card">
        <span className="commit-badge">Indigo &amp; Cyan Edition</span>
        <h1 className="commit-title">Commit Craft</h1>
        <p className="commit-subtitle">
          Run Conventional Commits and backdated or future commits across any local Git repository.
        </p>

        <div className="commit-row" style={{ marginBottom: "1rem" }}>
          <input
            type="text"
            placeholder="Target repo path (e.g. C:\path\to\project)"
            value={repoPath}
            onChange={(e) => setRepoPath(e.target.value)}
            className="commit-input"
          />
          <button type="button" onClick={handleCheckStatus} className="btn-secondary">
            Check Changes
          </button>
        </div>

        {changes.length > 0 && (
          <ul className="file-list">
            {changes.map((item, idx) => (
              <li key={`${item.file}-${idx}`} className="file-item">
                <span className="file-status">[{item.status}]</span>
                {item.file}
              </li>
            ))}
          </ul>
        )}

        <form onSubmit={handleCommit} className="commit-form">
          <div className="commit-row">
            <select
              value={commitType}
              onChange={(e) => setCommitType(e.target.value)}
              className="commit-select"
            >
              <option value="feat">feat</option>
              <option value="fix">fix</option>
              <option value="docs">docs</option>
              <option value="refactor">refactor</option>
              <option value="chore">chore</option>
            </select>

            <input
              type="text"
              placeholder="Scope (e.g. api, ui)"
              value={scope}
              onChange={(e) => setScope(e.target.value)}
              className="commit-input"
            />

            <input
              type="text"
              placeholder="Date offset (e.g. -1d, +2d, 2026-11-20)"
              value={dateOffset}
              onChange={(e) => setDateOffset(e.target.value)}
              className="commit-input"
            />
          </div>

          <input
            type="text"
            placeholder="Short commit message (required)"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
            className="commit-input"
          />

          <textarea
            rows={3}
            placeholder="Optional detailed body..."
            value={body}
            onChange={(e) => setBody(e.target.value)}
            className="commit-textarea"
          />

          <div className="checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={isBreaking}
                onChange={(e) => setIsBreaking(e.target.checked)}
              />
              Breaking change (!)
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={push}
                onChange={(e) => setPush(e.target.checked)}
              />
              Push to origin
            </label>
          </div>

          <button type="submit" className="btn-primary">
            Create Commit
          </button>
        </form>

        {statusMsg && <div className="banner-success">{statusMsg}</div>}
        {errorMsg && <div className="banner-error">{errorMsg}</div>}
      </main>
    </div>
  );
}