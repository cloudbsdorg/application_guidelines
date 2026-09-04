# Markdown Viewer and Editor for CloudBSD Applications

CloudBSD applications that show or edit prose (bot prompts, chat, docs, READMEs in-app) ship a **markdown viewer and a markdown editor**, not a plain unstyled `<textarea>` as the only experience.

## Viewer

- Render GitHub-flavored markdown: headings, lists, links, tables, fenced code with language.
- Sanitize HTML. Never assign unsanitized markdown HTML to the DOM. Strip `javascript:` URLs and inline event handlers.
- The backend stores and returns **markdown strings**. The view renders them. Do not store provider-native HTML. This is the MVC re-wrap rule applied to documents.
- Mermaid fences may render as diagrams when that can be done without evaluating untrusted JavaScript; otherwise show them as code.

## Editor

- Source and preview (split on desktop, toggle on mobile). Keyboard accessible. Undo that matches user expectation.
- Use this for system prompts, documents, and any long markdown field. A one-line chat composer may stay simple; **rendered assistant output is still viewed as markdown**.

## Responsive

Viewer and editor must work on phone and desktop. Use Tailwind breakpoints. Do not require a wide split-pane on a small screen.

## Tests

Cover sanitization (script tags, `javascript:` links) and that stored values remain markdown, not HTML.
