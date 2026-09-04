# Desktop and other native UI (CloudBSD)

CloudBSD has no separate desktop-stack standard beyond this note. GTK, Qt, and other native FreeBSD GUIs still follow CloudBSD law.

## Extra UI refinement with agy (LAW)

When Mark has granted access to Google Antigravity (`agy` CLI, Gemini), typically via **agy-ui-mcp** (`ui_implement` / `ui_review`), consult it for extra polish on **any user interface**. Desktop (GTK/Qt/native) is one surface, not a special case. Examples include web, TUI, desktop, mobile web, operator console, and a future GUI; those examples are not a closed list. Screenshot, iterate, keep evidence. Purpose: prettier UI, closer to https://cloudbsd.org / https://revytechinc.com.

- **When access exists:** consult agy for UI polish. Screenshot, iterate, store evidence with the change.
- **When agy is not connected yet:** do not block shipping a working UI.
- **Scope:** agy must not touch backend, APIs, or business logic. View layer only (widgets, layout, chrome).
- **Not a substitute:** Tests, visible text, keyboard access, and evidence remain required.
- **Theme family:** CloudBSD/REVYTECH tokens (navy, `#0066cc`, `#00d4ff`, Outfit/Inter, CloudBSD `#00529B`). Do not invent a competing palette.

This is the same single law as in `AGENTS.md`, `Web-User-Interfaces/WEBUI.md`, and `TUI/TUI.md`.
