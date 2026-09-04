#!/usr/bin/env python3
"""Generate and verify SKILLS/TOC.md from the skill tree itself.

SKILLS/TOC.md is the only list of skills in this repository. It is generated
from the frontmatter of every SKILLS/**/SKILL.md so that it cannot drift away
from the tree it indexes.

    tools/skills-index.py --write    regenerate SKILLS/TOC.md
    tools/skills-index.py --check    fail if TOC.md is stale or a skill is malformed

The layout rule this enforces:

    SKILLS/<category>[/<sub-category>]/<skill-name>/SKILL.md

A directory holding SKILL.md is a skill and its directory name is the skill's
name. Every SKILL.md carries `name`, `description`, and `keywords` frontmatter.
"""
import argparse, io, os, re, sys

SKILLS = "SKILLS"
TOC = os.path.join(SKILLS, "TOC.md")
RAW = ("https://raw.githubusercontent.com/cloudbsdorg/"
       "application_guidelines/main")

CATEGORY_BLURB = {
    "analysis": "Understand code you did not write, before changing or porting it.",
    "analysis/os-analysis": "Operating-system dependencies, for cross-platform porting.",
    "diagramming": "Producing diagrams in the formats CloudBSD law allows.",
    "freebsd-admin": "Running FreeBSD itself: VMs, jails, storage, services, safe deploys.",
    "migration": "Moving a legacy application to a modern platform.",
    "planning": "The .plan/ standard: creating, validating, and indexing plan documents.",
    "platform/cloudflare": "Building and publishing on Cloudflare.",
    "platform/opencode": "Workflows driven through the opencode tooling.",
    "quality": "Standing review disciplines, for code and for interfaces.",
    "release": "Turning a verified change into a published artifact.",
    "security": "Risk, audit, and the security document series.",
    "testing": "Planning tests and recording the evidence they produce.",
    "workflow": "Day-to-day development: tasks, debugging, review, shipping.",
}


class SkillError(Exception):
    pass


def parse_frontmatter(path):
    text = io.open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        raise SkillError(f"{path}: no YAML frontmatter")
    try:
        end = text.index("\n---\n", 3)
    except ValueError:
        raise SkillError(f"{path}: unterminated frontmatter")
    block = text[4:end + 1]

    fields, key, buf, kws = {}, None, [], []
    for line in block.split("\n"):
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", line):
            if key == "description":
                fields["description"] = " ".join(buf).strip()
            key = line.split(":", 1)[0]
            rest = line.split(":", 1)[1].strip()
            buf = []
            if key == "keywords":
                continue
            if rest in (">-", ">", "|", "|-", ""):
                continue
            fields[key] = rest.strip('"').strip("'")
            key = None
        elif key == "description":
            buf.append(line.strip())
        elif line.startswith("  - "):
            kws.append(line[4:].strip().strip('"').strip("'"))
    if key == "description":
        fields["description"] = " ".join(buf).strip()
    fields["keywords"] = kws
    return fields


def discover():
    skills = []
    for dirpath, dirnames, filenames in os.walk(SKILLS):
        if "SKILL.md" not in filenames:
            continue
        dirnames[:] = []                      # a skill never nests a skill
        rel = os.path.relpath(dirpath, SKILLS).replace(os.sep, "/")
        fm = parse_frontmatter(os.path.join(dirpath, "SKILL.md"))
        name, category = rel.rsplit("/", 1)[-1], rel.rsplit("/", 1)[0]
        if "/" not in rel:
            raise SkillError(f"{rel}: a skill must live inside a category directory")
        if fm.get("name") != name:
            raise SkillError(
                f"{rel}/SKILL.md: frontmatter name {fm.get('name')!r} "
                f"does not match directory name {name!r}")
        if not fm.get("description"):
            raise SkillError(f"{rel}/SKILL.md: no description")
        if not re.search(r"(?:^|[.!?]\s+)Use\b", fm["description"]):
            raise SkillError(
                f"{rel}/SKILL.md: the description does not say when to use the "
                "skill. It needs a sentence beginning 'Use ...' - that sentence "
                "is what an agent scans to decide whether to load it.")
        if not fm["keywords"]:
            raise SkillError(f"{rel}/SKILL.md: no keywords")
        refs = sorted(f for f in filenames if f.endswith(".md") and f != "SKILL.md")
        skills.append({"path": rel, "name": name, "category": category,
                       "description": fm["description"], "keywords": fm["keywords"],
                       "refs": refs})
    dupes = {s["name"] for s in skills
             if sum(1 for t in skills if t["name"] == s["name"]) > 1}
    if dupes:
        raise SkillError(f"duplicate skill names: {sorted(dupes)}")
    return sorted(skills, key=lambda s: s["path"])


def summary(description):
    """First sentence of the description, without the 'Use when' half."""
    first = re.split(r"(?<=[.!?]) ", description)[0].strip()
    return first.rstrip(".")


def render(skills):
    out = []
    w = out.append
    w("# Skills — Table of Contents")
    w("")
    w("> **Generated file.** Produced from the frontmatter of every")
    w("> `SKILLS/**/SKILL.md` by `tools/skills-index.py`. Do not hand-edit it:")
    w("> change the skill's frontmatter and regenerate. This is the *only* list")
    w("> of skills in the repository, so that no second list can contradict it.")
    w("")
    w("**For agents:** scan the trigger table, find the row that matches your task,")
    w("and load **that one skill**. Do not load the tree. Loading everything is not")
    w("thoroughness — it spends the context you needed for the work.")
    w("")
    w("Each skill is a directory containing `SKILL.md`. Other `.md` files beside it")
    w("are that skill's reference material; load them only when `SKILL.md` says to.")
    w("")
    w("If you cannot browse a filesystem, every path below resolves as:")
    w("")
    w("```")
    w(f"{RAW}/SKILLS/<path>/SKILL.md")
    w("```")
    w("")
    w(f"There are **{len(skills)} skills**.")
    w("")
    w("---")
    w("")
    w("## Trigger index")
    w("")
    w("| If the task mentions… | Load | What it is |")
    w("|---|---|---|")
    rows = []
    for s in skills:
        trig = ", ".join(f"`{k}`" for k in s["keywords"])
        rows.append((s["keywords"][0].lower(), trig, s["path"], summary(s["description"])))
    for _, trig, path, summ in sorted(rows):
        w(f"| {trig} | `{path}/SKILL.md` | {summ} |")
    w("")
    w("---")
    w("")
    w("## By category")
    w("")
    cats = {}
    for s in skills:
        cats.setdefault(s["category"], []).append(s)
    for cat in sorted(cats):
        w(f"### `{cat}/`")
        if cat in CATEGORY_BLURB:
            w("")
            w(CATEGORY_BLURB[cat])
        w("")
        w("| Skill | Path | Use it when |")
        w("|---|---|---|")
        for s in sorted(cats[cat], key=lambda x: x["name"]):
            use = s["description"]
            m = re.search(r"(Use when.*)", use, re.S)
            use = (m.group(1) if m else use).replace("\n", " ").strip()
            use = re.sub(r"\s+", " ", use)
            w(f"| **{s['name']}** | `{s['path']}/SKILL.md` | {use} |")
        w("")
        extra = [s for s in cats[cat] if s["refs"]]
        if extra:
            w("<details><summary>Reference files inside these skills</summary>")
            w("")
            for s in extra:
                w(f"- `{s['path']}/` — " + ", ".join(f"`{r}`" for r in s["refs"]))
            w("")
            w("</details>")
            w("")
    w("---")
    w("")
    w("## How to use this index")
    w("")
    w("```")
    w("1. Match the task against the trigger index above.")
    w("2. Read that one SKILL.md.")
    w("3. Follow its links to reference files only if it tells you to.")
    w("```")
    w("")
    w("The law itself is in [`AGENTS.md`](../AGENTS.md); a skill explains *how* to")
    w("carry out a rule and links to it rather than restating it. If a skill and")
    w("`AGENTS.md` ever disagree, `AGENTS.md` wins and the skill is the defect.")
    w("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="regenerate SKILLS/TOC.md")
    g.add_argument("--check", action="store_true", help="verify TOC.md is current")
    args = ap.parse_args()

    try:
        skills = discover()
    except SkillError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    text = render(skills)

    if args.write:
        io.open(TOC, "w", encoding="utf-8").write(text)
        print(f"wrote {TOC} ({len(skills)} skills)")
        return 0

    current = io.open(TOC, encoding="utf-8").read() if os.path.exists(TOC) else ""
    if current != text:
        print(f"FAIL: {TOC} is out of date; run tools/skills-index.py --write",
              file=sys.stderr)
        return 1
    print(f"PASS: {TOC} matches the tree ({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
