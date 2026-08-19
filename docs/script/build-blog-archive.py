#!/usr/bin/env python3
"""
Quarto pre-render: regenerate blog-archive.qmd from what is in docs/blog/.

The archive needs one Quarto listing per year, plus a matching section in the
body. Maintaining that by hand does not survive contact with a new post: a
post in a new year has no section to land in, and every post makes the "N
posts" line under some heading wrong. Both had already happened.

So the page is generated. Years come from the YYYYMMDD prefix on each post
filename, which is the naming convention the blog already uses. Add a post in
any year, including one that has never appeared before, and the section, the
listing and the count all appear on the next render.

Runs before Quarto reads the project, so the file it writes is the file Quarto
renders. Idempotent: same posts in, same bytes out.
"""

import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(_HERE)                 # docs/
BLOG = os.path.join(PROJECT, "blog")
TARGET = os.path.join(PROJECT, "blog-archive.qmd")

# posts are named YYYYMMDD-slug.qmd; anything else in blog/ is not a post
POST = re.compile(r"^(\d{4})\d{4}-.+\.qmd$")

INTRO = (
    "A chronological index of every post. Looking for something by topic "
    "instead?\nThe [main blog page](blog.qmd) has category filters and search."
)


def years():
    """{year: count} for every dated post file, newest year first."""
    counts = {}
    if not os.path.isdir(BLOG):
        return counts
    for name in os.listdir(BLOG):
        m = POST.match(name)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return counts


def listing(year):
    return "\n".join([
        "  - id: y%s" % year,
        "    contents: blog/%s*.qmd" % year,
        '    sort: "date desc"',
        "    type: table",
        "    fields: [date, title, categories]",
        "    field-display-names:",
        '      date: "Date"',
        '      title: "Post"',
        '      categories: "Categories"',
        "    date-format: 'D MMM YYYY'",
        "    filter-ui: false",
        "    sort-ui: false",
        "    categories: false",
    ])


def build(counts):
    order = sorted(counts, reverse=True)

    out = [
        "---",
        'title: "Blog Archive"',
        'subtitle: "Every post, oldest to newest, grouped by year"',
        "page-layout: full",
        "toc: true",
        "toc-title: Years",
        "css: styles/blog.css",
        "listing:",
    ]
    out.extend(listing(y) for y in order)
    out.append("---")
    out.append("")
    out.append(INTRO)
    out.append("")

    for y in order:
        n = counts[y]
        # Explicit heading id. Without one, Quarto cannot make an id from a
        # digits-only heading and falls back to section, section-1, section-2
        # ... which are positional: #section-3 is 2023 today and 2024 as soon
        # as a 2027 post appears, silently breaking any saved link. #year-2023
        # keeps meaning 2023.
        out.append("## %s {#year-%s}" % (y, y))
        out.append("")
        out.append("%d post%s" % (n, "" if n == 1 else "s"))
        out.append("")
        out.append(":::{#y%s}" % y)
        out.append(":::")
        out.append("")

    return "\n".join(out)


def main():
    counts = years()
    if not counts:
        print("[blog-archive] no dated posts found in %s, leaving the page "
              "alone" % BLOG, file=sys.stderr)
        return 1

    new = build(counts)
    old = ""
    if os.path.exists(TARGET):
        with open(TARGET, encoding="utf-8") as fh:
            old = fh.read()

    total = sum(counts.values())
    if new == old.replace("\r\n", "\n"):
        print("[blog-archive] %d posts across %d years, already current"
              % (total, len(counts)))
        return 0

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(new)
    print("[blog-archive] rebuilt: %d posts across %d years (%s to %s)"
          % (total, len(counts), min(counts), max(counts)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
