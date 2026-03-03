

# Web User Interface (Web UI) Guidelines for CloudBSD Applications

This document provides guidelines for developing modern, secure, and accessible Web UIs for CloudBSD applications.

## 1. Frontend Standards

### Modern Languages and Frameworks
- **React**: will be used for the frontend.
- **Tailwind CSS**: will be used for the frontend as well to make the UI more consistent, and mobile friendly.
- **TypeScript**: will be the language used for the frontend.


### Progressive Enhancement
- **Responsive Design**: Interfaces must be fully responsive and work on mobile, tablet, and desktop.

## 2. Accessibility (A11y)

### WCAG Compliance
- **Standard**: Aim for WCAG 2.1 Level AA compliance.
- **Semantic HTML**: Use correct HTML tags (e.g., `<button>` for buttons, `<a>` for links).
- **ARIA**: Use ARIA labels and roles only when semantic HTML is insufficient.

### Keyboard Accessibility
- **Full Navigation**: All features must be accessible via keyboard.
- **Focus Indicators**: Ensure clear, visible focus states for all interactive elements.

## 3. Security

### Input Validation
- **Sanitize Everything**: Never trust user input. Sanitize all data displayed in the browser.
- **CSRF and XSS**: Implement robust protections against common web vulnerabilities.

### Data Transmission
- **HTTPS Only**: All traffic must be encrypted using TLS/SSL.
  - Make a dev mode available for testing, or a way to switch between HTTP and HTTPS.
- **Content Security Policy (CSP)**: Implement a strict CSP to mitigate XSS attacks.
  - Give some exceptions for third-party scripts and styles, and development mode.

## 4. Performance

### Optimization
- **Asset Minification**: Use build tools to minify CSS, JS, and images.
- **Lazy Loading**: Use lazy loading for images and non-critical resources.
- **Bundle Size**: Monitor and minimize JavaScript bundle sizes.

### Core Web Vitals
- **Metrics**: Pay close attention to LCP (Largest Contentful Paint), FID (First Input Delay), and CLS (Cumulative Layout Shift).
