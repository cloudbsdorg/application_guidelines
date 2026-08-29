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
