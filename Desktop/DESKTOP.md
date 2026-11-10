# Desktop and other native UI (CloudBSD)

CloudBSD has no separate desktop-stack standard beyond this note. GTK, Qt, and other native FreeBSD GUIs still follow CloudBSD law.

## Extra UI refinement through a gateway model (LAW)

**Never use agy (Antigravity CLI) for anything: not as a review voice, not as a fallback, not as a coding agent (owner order, repeated many times; restated 2026-11-10 2:51 AM CT).** The ordered chain is: a gateway model at `https://llm.cloudbsd.org/v1` (for example `dgx/minimax` or `dgx/default`); if that model or the gateway is unavailable, another live gateway model; then Ollama Cloud; then free models through the `opencode-free-model-shim`. Never agy.

Consult that independent interface review for extra polish on **any user interface**. Desktop (GTK/Qt/native) is one surface, not a special case. Examples include web, TUI, desktop, mobile web, operator console, and a future GUI; those examples are not a closed list. Screenshot, iterate, keep evidence. Purpose: prettier UI, closer to https://cloudbsd.org / https://revytechinc.com.

- **How:** run the review through the ordered chain above. A panel that counted agy as a member must be rebuilt without it, not reported as degraded because agy failed.
- **Scope:** the reviewer must not touch backend, APIs, or business logic. View layer only (widgets, layout, chrome).
- **Not a substitute:** Tests, visible text, keyboard access, and evidence remain required. The model review is extra refinement, not a replacement for tests or evidence.
- **Theme family:** CloudBSD/REVYTECH tokens (navy, `#0066cc`, `#00d4ff`, Outfit/Inter, CloudBSD `#00529B`). Do not invent a competing palette.

This is the same single law as in `AGENTS.md` rule 28, `Web-User-Interfaces/WEBUI.md`, and `TUI/TUI.md`.
