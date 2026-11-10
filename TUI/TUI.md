

# Text-based User Interface (TUI) Guidelines for CloudBSD Applications

This document provides guidelines for designing and implementing high-quality text-based user interfaces for CloudBSD.

## 1. Design Principles

### Simplicity and Clarity
- **Uncluttered Layout**: Avoid overly complex screen layouts. Group related information logically.
- **Minimalist Aesthetic**: Use lines and boxes only when necessary to separate logical sections.

### Responsiveness
- **Window Resizing**: TUIs must handle window resizing gracefully (SIGWINCH).
- **Non-blocking Operations**: Avoid UI freezes during long-running tasks. Use progress indicators or status lines.

## 2. Navigation and Interaction

### Keyboard-First
- **Standard Keybindings**: Use common navigation keys:
  - `j`/`k` or Arrow Keys: Movement
  - `Enter`: Select/Confirm
  - `Esc` or `q`: Go back/Exit
  - `?`: Show help
- **Hotkeys**: Provide consistent and discoverable hotkeys for frequently used actions.

### Focus Management
- **Visual Feedback**: Clearly indicate which element currently has focus (e.g., through color or highlighting).
- **Tab Order**: Ensure a logical tabbing order through input fields and buttons.

## 3. Visual Styling

### Color Usage
- **ANSI Colors**: Stick to the standard 8 or 16 ANSI colors for maximum compatibility.
- **Contrast**: Ensure high contrast for readability. Do not rely solely on color to convey information (for accessibility).
- **Theming**: If possible, support user-definable themes or respect the terminal's default color palette.

### Typography
- **Alignment**: Use consistent alignment for labels and values.
- **Emphasis**: Use bold or underline sparingly for emphasis, but test across multiple terminal emulators.

## 4. Technical Implementation

### Library Selection
- **ncurses**: The classic standard for complex TUI development in C/C++.
- **Bubble Tea (Go)**: Recommended for modern, Elm-architecture-based TUIs in Go.
- **ratatui (Rust)**: Recommended for high-performance, cross-platform TUIs in Rust.

### Terminal Support
- **TERM Variable**: Respect the `TERM` environment variable.
- **Unicode**: Support Unicode characters for a richer UI when the terminal supports it (check `LANG`).
- **Graceful Degradation**: If advanced terminal features (e.g., mouse support, 256 colors) are missing, the application should still be fully functional.
- **Terminal Emulator Compatibility**: Ensure compatibility with popular terminal emulators like xterm, gnome-terminal, and Windows Terminal.
- **Mouse Support**: Ensure mouse support works across different terminal emulators and operating systems.
- **Accessibility**: Test with screen readers and ensure keyboard-only navigation is possible.


## 5. Operator recovery console (LAW)

If a long-running service has operator state to repair, it MUST ship a recovery console.
Recovery is **operator-only** (this TUI or a CLI). It is not a public UI and must not be
an unauthenticated web page.

- Keyboard-first, as in Section 2. `?` for help. Destructive actions require confirmation.
- Pair with `doctor`: the console should surface doctor findings (human form) and not hide JSON evidence.
- See `Configuration-Files/CONFIGURATION.md` (`doctor`, recovery, resource headroom).

## 6. Extra UI refinement through a gateway model (LAW)

**Never use agy (Antigravity CLI) for anything: not as a review voice, not as a fallback, not as a coding agent (owner order, repeated many times; restated 2026-11-10 2:51 AM CT).** The ordered chain is: a gateway model at `https://llm.cloudbsd.org/v1` (for example `dgx/minimax` or `dgx/default`); if that model or the gateway is unavailable, another live gateway model; then Ollama Cloud; then free models through the `opencode-free-model-shim`. Never agy.

Consult that independent interface review for extra polish on **any user interface** — including this TUI (Bubble Tea, ratatui, ncurses, operator recovery console) and every other surface. Examples include web, TUI, desktop, mobile web, operator console, and a future GUI; those examples are not a closed list. Screenshot, iterate, keep evidence.

- **How:** run the review through the ordered chain above. A panel that counted agy as a member must be rebuilt without it, not reported as degraded because agy failed.
- **Scope:** the reviewer must not touch backend, APIs, or business logic. View layer only (widgets, layout, chrome). TUI view code is in scope; Go/Rust/C services, APIs, and domain logic are not.
- **Not a substitute:** Keyboard-first behavior, help (`?`), SIGWINCH, and evidence remain required. The model review is extra refinement, not a replacement for tests or evidence.
- **Theme family:** CloudBSD/REVYTECH. Do not invent a competing palette.

This is the same single law as in `AGENTS.md` rule 28, `Web-User-Interfaces/WEBUI.md`, and `Desktop/DESKTOP.md`.
