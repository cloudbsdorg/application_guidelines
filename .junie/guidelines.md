# CloudBSD Application Guidelines Project - Development Guidelines

This project contains the official guidelines for applications developed for CloudBSD. All documentation is written in Markdown and must follow specific standards to maintain consistency across the project.

## 1. Build/Configuration Instructions

As this is a documentation-only project, no traditional build steps are required. However, for a consistent development experience, it is recommended to:

- **Environment**: Use a Markdown-capable editor (like GoLand, VS Code, or Vim with Markdown plugins).
- **Structure**: Maintain the directory-based organization. Each major category should have its own directory containing a relevant `.md` file (e.g., `TUI/TUI.md`).
- **Permissions**: Ensure newly created Markdown files are world-readable.

## 2. Testing Information

To ensure documentation quality, we use a simple sanity check script to verify the structure of the Markdown files.

### Running Tests
You can run the existing sanity check script from the project root:
```bash
bash test_md.sh
```

### Adding New Tests
If new documentation requirements are added (e.g., mandatory sections, link checking), update `test_md.sh` to include these checks. Follow the existing pattern:
1. Define a check (e.g., using `grep`, `find`, or a Markdown linter).
2. Report errors clearly.
3. Set a non-zero exit code if a check fails.

### Example Test (Demonstration)
The current `test_md.sh` script performs the following:
- **Empty File Check**: Ensures no Markdown files are empty.
- **Header Check**: Verifies that `README.md` starts with a Level 1 header.

To see it in action, you can temporarily empty a file and run the script:
```bash
echo "" > "TUI/TUI.md"
bash test_md.sh
# It should report an error for TUI/TUI.md
```

## 3. Additional Development Information

### Code (Documentation) Style
- **Headers**: Use ATX-style headers (`# Header 1`, `## Header 2`).
- **Line Endings**: Use standard Unix LF line endings.
- **Emphasis**: Use `**bold**` for strong emphasis and `*italics*` for light emphasis.
- **Lists**: Use dashes (`-`) for unordered lists and numbers (`1.`) for ordered lists.
- **Language**: All documentation must be written in English.

### Project Consistency
- All documents must be interpreted as "law" for CloudBSD products.
- Major sections of the guidelines should be linked or mentioned in the root `README.md`.
