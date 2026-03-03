

# Internationalization (i18n) Guidelines for CloudBSD Applications

This document provides guidelines for ensuring CloudBSD applications are ready for a global audience through effective internationalization.

## 1. Core Principles

### Separation of Concerns
- **Text Extraction**: Never hardcode user-facing strings in the source code. All strings should be stored in external files (e.g., `.po`, `.json`, `.yaml`).
- **Standardized Tools**: Use industry-standard tools for string management:
  - **gettext**: The preferred tool for C, C++, Python, and many other languages.
  - **i18next**: Common for web-based (JavaScript/TypeScript) applications.

## 2. Technical Standards

### Encoding
- **UTF-8 Everywhere**: All source code, configuration files, and data files must be encoded in UTF-8. Applications must handle UTF-8 characters correctly in all inputs and outputs.

### Date and Time
- **ISO 8601**: Use ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`) for machine-readable dates and times.
- **Locale-Aware Formatting**: Use libraries that support locale-specific date, time, and currency formatting (e.g., `ICU` libraries).
- **Datestamps**: Provide datestamps in a consistent format for logging and debugging purposes. When storing dates in a database, ensure that datestamps are stored in UTC to avoid timezone-related issues.

### Pluralization and Context
- **Plural Rules**: Support complex pluralization rules through your chosen i18n framework (e.g., gettext plural forms).
- **Contextual Hints**: Provide comments or context for translators when a string's meaning is ambiguous (e.g., is "Open" a verb or an adjective?).

## 3. User Experience

### Locale Detection
- **Environment Variables**: Applications should respect standard environment variables:
  - `LANG`, `LC_ALL`, `LC_MESSAGES`.
- **Configuration Overrides**: Allow users to explicitly set their preferred language in the application configuration.

### Right-to-Left (RTL) Support
- **Layout Consideration**: For graphical and web interfaces, ensure the layout can be mirrored to support RTL languages (e.g., Arabic, Hebrew).

### Web Accessibility
- **Accessible Names**: Provide clear and descriptive names for UI elements to improve screen reader compatibility.
- **Keyboard Navigation**: Ensure all interactive elements are keyboard accessible and follow a logical tab order.
- **Color Contrast**: Maintain sufficient color contrast between text and background to ensure readability for users with visual impairments.
- **Localization**: Ensure that all UI elements and content are localized for different languages and cultures. And URL and navigation patterns should be localized as well.

## 4. Documentation

### Language Requirements
- **Primary Language**: All technical documentation, code comments, and the primary version of any software must be in **English**.
- **Translation Contributions**: Encourage community contributions for translations by providing clear instructions and a simple workflow (e.g., using platforms like Transifex or Weblate).

## 5. Languages that MUST be Supported

When presenting the language name, use the native language name. And the list should be ordered by the language's native name, 
with the exception of English, where it should be first when alphabetically ordered.
The primary language for all technical documentation is English, the default language for all software, and must be present in all translations. And first on any list, dropdown, or menu.

### List of Languages
- English
- Spanish
- French
- Esperanto
- Italian
- Norwegian
- Swedish
- Punjabi
- Klingon
- Elvish
- German
- Chinese
- Japanese
- Arabic
- Kiswahili
- Yorùbá
- Hindi
- 한국어
- Finnish
- Russian
- Polish
- Dothraki
- Valyrian
- Na'vi
- Atlantean
- Turkish
- Catalan
- Czech
- Greek
- Hebrew
- Ukrainian
- Russian
- Serbian
- Slovak
- Slovenian
- Urdu
- Bulgarian
- Croatian
- Hungarian
- Lithuanian
- Latvian
- Indonesian
- Portuguese (Brazil)
- Portuguese (Portugal)
- Romanian
- Serbian
- Slovak
- Slovenian
- Urdu
- Korean
- Elvish
- Dothraki
- High Valyrian
- Atlantean