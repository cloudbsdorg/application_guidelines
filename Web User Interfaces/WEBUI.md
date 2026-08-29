# Web User Interface (Web UI) Guidelines for CloudBSD Applications

This document provides guidelines for developing modern, secure, and accessible Web UIs for CloudBSD applications.

## 0. Role of the Web UI

The web UI is the **view**. It presents state and passes messages to a backend controller. It does not contain domain logic, secrets, or direct access to databases, queues, or LLM providers. See [MVC and Isolation](../Architecture/MVC.md). Backends are not publicly reachable unless you are deliberately exposing an API.

## 1. Frontend Standards

### Framework
- **Angular**: The primary frontend framework for CloudBSD web user interfaces (the view). React is not the standard. The backend stays Go or another allowed systems language; see `Languages/LANGUAGES.md`.
- **TypeScript**: The programming language for that frontend. Do not ship a new CloudBSD web UI in plain JavaScript when Angular/TypeScript can be used.
- **Styling**: **Tailwind CSS** is required for layout, spacing, and breakpoints so every UI is desktop and mobile friendly. Do not ship a desktop-only layout with no small-screen treatment. Component styles may add what Tailwind cannot, but breakpoints and page chrome go through Tailwind.
- **Design and prototyping artifacts**: UI wireframes, mockups, and screens are **SVG**, kept in-repo as `.svg` files. The live product is the Angular + Tailwind application. Do not use ASCII art for UI mockups. Architecture diagrams remain Mermaid; do not replace those with SVG.

Small static admin pages (a login form and a few screens with no build step) are allowed when a full Angular app would be disproportionate. They must still use responsive Tailwind (or equivalent utility breakpoints), accessibility, security, and HTTPS. Prefer Angular once the UI has real application state (multiple views, forms, live data).

### Progressive Enhancement
- **Responsive Design**: Every UI must work on phone, tablet, and desktop. Use Tailwind breakpoints (`sm`/`md`/`lg`). Stack navigation and tables on small screens; do not rely on horizontal scroll as the only mobile story.
- **Progressive Enhancement**: Ensure core functionality is available to all users, regardless of browser capabilities.

## 2. Accessibility (A11y)

### WCAG Compliance
- **Standard**: All web interfaces must aim for WCAG 2.1 Level AA compliance.
- **Semantic HTML**: Use native HTML elements where possible (e.g., `<button>` for actions, `<a>` for navigation).
- **ARIA**: Use WAI-ARIA labels and roles only when semantic HTML is insufficient to describe complex components.

### Keyboard Accessibility
- **Full Navigation**: All features and interactive elements must be accessible via keyboard alone.
- **Focus Indicators**: Provide clear, high-contrast focus states for all interactive elements.

## 3. Security

### Authentication and Session Management
- **Root Path (`/`)**: The root path of the application server MUST present the **login page**, or **redirect to login**. A public landing page is not a substitute. Login at `/` is law.
- **Session Redirects**: Automatically redirect users to the login page when a session is invalid or has expired.
- **Login UX**: Identifier, eye-icon show/hide password (inside the field; not a Show/Hide text button), remember username, factory bootstrap wizard, and password-manager rules are law. See [Login UX (LAW)](#8-login-ux-law).

### Input Validation
- **Sanitization**: Never trust user input. Sanitize all data before displaying it in the browser to prevent XSS.
- **Protection**: Implement robust protections against common web vulnerabilities, including CSRF and XSS.

### Data Transmission
- **HTTPS Only**: All production traffic must be encrypted using TLS/SSL.
- **Test Mode**: Provide a configuration to toggle between HTTP and HTTPS for local development and testing environments.
- **Content Security Policy (CSP)**: Implement a strict CSP to mitigate XSS attacks.
  - Defined exceptions are permitted for trusted third-party scripts and styles in specific development modes.

## 4. Performance

### Optimization
- **Asset Minification**: Use build tools to minify CSS, JavaScript, and images.
- **Lazy Loading**: Use lazy loading for images and non-critical resources to speed up initial page loads.
- **Bundle Size**: Actively monitor and minimize JavaScript bundle sizes to reduce time-to-interactive.

### Core Web Vitals
- **Metrics**: Optimize for the following key metrics:
  - **LCP (Largest Contentful Paint)**: Measure loading performance.
  - **INP (Interaction to Next Paint)**: Measure interactivity.
  - **CLS (Cumulative Layout Shift)**: Measure visual stability.

## 5. UI evidence (LAW)

A Web UI task is not complete until there is evidence the UI works. Compile-only and "I ran it" are not evidence.

- **Tool:** Playwright or equivalent. If the tool is not installed, find one or make one; skipping because a required tool is missing is a defect.
- **Assertions:** Elements are where they belong (visible, labeled, at the expected route). Do not only screenshot; assert.
- **Viewports:** Desktop and mobile. Tailwind breakpoints (`sm`/`md`/`lg`) must be covered.
- **Artifacts:** Save screenshots, traces, and the HTML report. Commit representative screenshots for UI proof, or store the report as a CI artifact or clearly named path (`artifacts/playwright/`).
- Login at `/` must be in the suite.
- Login UX must be in the suite: identifier accepts a regular username **and** an email address; eye-icon show/hide on password fields (open eye = visible, slashed = hidden; not a Show/Hide text button); remember-username checkbox plus `autocomplete=username`; factory path does not prompt the browser to save `admin:admin`; first-login wizard fields (login id, display name, new password + confirm, optional tenant/org name) and `autocomplete=new-password` / `autocomplete=name`; wizard can rename the factory `admin` login id; wizard reappears when setup is incomplete, the factory password is still in use, or required config is still placeholder. Wizard MUST NOT collect street address, phone, country, or birthday.

## 6. Visual identity (LAW)

CloudBSD apps look like https://cloudbsd.org. REVYTECH products look like https://revytechinc.com (same family).
Angular + Tailwind UIs MUST use these tokens, taken from live CSS. Do not invent palettes.

### CloudBSD
- Brand blue: `#00529B`
- Slate: `#0f172a`
- Error: `#D32F2F`

### REVYTECH
- Navy: `#001a33` / `#002a55` / `#013a73`
- Blue: `#0066cc` / `#004a99`
- Cyan accent: `#00d4ff`
- Light: `#f8fafc`

### Type
- Headings: Outfit
- Body: Inter (as on revytechinc.com)

Put tokens in Tailwind theme config (`colors`, `fontFamily`), not ad-hoc hex in templates.
Screenshots stored as evidence MUST look like those sites, not a generic admin theme.

## 7. Extra UI refinement with agy (LAW)

When Mark has granted access to Google Antigravity (`agy` CLI, Gemini), typically via **agy-ui-mcp** (`ui_implement` / `ui_review`), consult it for extra polish on **any user interface** — not only this Angular + Tailwind view. Examples include web, TUI, desktop, mobile web, operator recovery console, and a future GUI; those examples are not a closed list. Screenshot, iterate, keep evidence. Purpose: prettier UI, closer to https://cloudbsd.org / https://revytechinc.com.

- **When access exists:** consult agy for UI polish. Screenshot, iterate, store evidence with the change.
- **When agy is not connected yet:** do not block shipping a working UI. Playwright, visible text, and theme tokens still apply.
- **Scope:** agy must not touch backend, APIs, or business logic. View layer only (CSS, components, widgets, layout, chrome).
- **Not a substitute:** Playwright + visible text + theme tokens remain required. agy is extra refinement, not a replacement for tests or evidence.
- **Theme stays CloudBSD/REVYTECH:** navy `#001a33` / `#002a55` / `#013a73`, blue `#0066cc` / `#004a99`, cyan accent `#00d4ff`, light `#f8fafc`, Outfit headings, Inter body, CloudBSD brand blue `#00529B`. Do not invent a new palette.

This is the same single law as in `AGENTS.md`, `TUI/TUI.md`, and `Desktop/DESKTOP.md`.

## 8. Login UX (LAW)

The product brand on the login screen is **top-level REVYTECH** (looks like https://revytechinc.com). CloudBSD is the platform; do not put CloudBSD as the product kicker. Use REVYTECH tokens (navy `#001a33` / `#002a55` / `#013a73`, blue `#0066cc` / `#004a99`, cyan accent `#00d4ff`, light `#f8fafc`, Outfit headings, Inter body). See [Visual identity](#6-visual-identity-law).

This is the same login law as `AGENTS.md`.

### Identifier

- The login identifier MAY be a **regular username OR an email address**, like most sites.
- Do not require email-only. Do not reject a valid username because it is not an email. Do not reject a valid email because it is not a "username" token.

### Password fields

- Every password field MUST have a **show/hide** control (toggle visibility).
- That control is an **eye icon inside the password field**, not a Show/Hide text button. Open eye = password visible; slashed eye = password hidden.
- The control is keyboard-accessible and labeled (WCAG 2.1 AA).

### Remember username

- The login screen MUST offer remember/save username: a **checkbox** plus `autocomplete="username"` on the identifier field.
- Do **not** remember the factory password. Never persist `admin`/`admin` as a saved password (password manager, local storage, or any credential-save API).

### Factory bootstrap and first-login wizard

- Factory bootstrap credentials MAY be `admin` / `admin` for a one-box install. That pair boots the box; it is not the lasting operator identity.
- After that factory sign-in, the app MUST force a **first-login wizard** that changes the password, lets the operator rename the login id away from `admin`, and completes required setup **BEFORE** the browser password manager is invited to save credentials.

Wizard fields (this product; usual SaaS collect — email or username, password, optional display name):

| Field | Required | Rules |
|-------|----------|-------|
| Login id | Yes | Username **OR** email, like most sites. Not locked to `admin`. Operator MAY rename the factory admin to anything (`mark`, `mark@revytechinc.com`, etc.). `autocomplete="username"`. |
| Display / real name | Yes | One field. `autocomplete="name"`. |
| New password | Yes | Eye icon inside the field (open = visible, slashed = hidden); not a Show/Hide text button. `autocomplete="new-password"`. |
| Confirm password | Yes | Same eye-icon show/hide. `autocomplete="new-password"`. |
| Tenant / org display name | Optional | Org label only. |

- **Do not collect** street address, phone, country, or birthday. Address is later/never for this product.
- Wizard password fields use `autocomplete="new-password"`. Never put `autocomplete="current-password"` on the factory password field.
- Detect and **re-show the wizard** when any of these is true:
  - setup is incomplete
  - the factory password is still in use
  - required config is still a placeholder
- Browsers MUST NOT be prompted to save `admin:admin`. That pair is a well-known leaked password and triggers browser leaked-password warnings. Do not use `autocomplete="current-password"` on factory login; do not call a credential-save API; complete the wizard first. Invite the password manager only after the wizard has set the new login id and new password.
