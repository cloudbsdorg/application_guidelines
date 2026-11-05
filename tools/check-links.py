#!/usr/bin/env python3
"""Report Markdown links in this repository that do not resolve to a file.

A broken link is worse than an awkward filename: it sends an agent looking for
guidance that is not there, and it fails silently. Run this after moving or
renaming anything.

    tools/check-links.py            check the whole repository
    tools/check-links.py <dir>      check a subtree

Links inside fenced code blocks are ignored, as are external URLs, anchors, and
obvious template placeholders such as `300-Impl.md#<task-id>`.
"""
import os, re, sys, urllib.parse

LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
FENCE = re.compile(r'```.*?```', re.S)
PLACEHOLDER = re.compile(r'[<{]')          # e.g. 300-Impl.md#<task-id>


def main(root):
    root = os.path.abspath(root)
    broken = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            path = os.path.join(dirpath, filename)
            text = FENCE.sub("", open(path, encoding="utf-8").read())
            for match in LINK.finditer(text):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if PLACEHOLDER.search(target):
                    continue
                target = urllib.parse.unquote(target.split("#")[0])
                if not target:
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(dirpath, target))):
                    print(f"{os.path.relpath(path, root)}: {match.group(1)}")
                    broken += 1
    if broken:
        print(f"FAIL: {broken} broken link(s)", file=sys.stderr)
        return 1
    print("PASS: every relative Markdown link resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
