# Web User Interface (Web UI) Guidelines for CloudBSD Applications

This document provides guidelines for developing modern, secure, and accessible Web UIs for CloudBSD applications.

## 1. Frontend Standards

### Modern Languages and Frameworks
- **React**: The primary frontend framework for building interactive user interfaces.
- **Tailwind CSS**: The utility-first CSS framework for consistent styling and responsive design.
- **TypeScript**: The mandatory programming language for frontend development to ensure type safety and maintainability.

### Progressive Enhancement
- **Responsive Design**: Interfaces must be fully responsive across mobile, tablet, and desktop devices.
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
- **Root Path**: The root path of the application server must present a sensible entry point, such as a login page or public landing page.
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
  - **FID (First Input Delay)**: Measure interactivity.
  - **CLS (Cumulative Layout Shift)**: Measure visual stability.
