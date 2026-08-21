#!/usr/bin/env python3
"""Inject previous/next post navigation into every rendered blog post.

Quarto has no built-in previous/next for listing-based blogs, so this runs as a
post-render step. It reads the date and title straight out of each post's .qmd
frontmatter, orders the posts, and writes a small nav block into the rendered
HTML just before the Giscus comments (or at the end of the article).

Ordering is by frontmatter date, then filename, so posts sharing a date stay
stable. "Previous" means older, "next" means newer, matching the listing order.

Idempotent: an existing .post-nav block is replaced, so re-rendering is safe.
Stdlib only. Quarto runs it from the project directory (docs/).
"""

import os
import re
import sys
import html

# This script lives in docs/script/, so the Quarto project directory is its
# parent. Quarto sets QUARTO_PROJECT_OUTPUT_DIR when it invokes a post-render
# step; the fallback keeps the script runnable by hand.
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(_HERE)
_env_out = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR")
OUTPUT_DIR = (os.path.abspath(_env_out) if _env_out
              else os.path.abspath(os.path.join(PROJECT, "..", "_site")))

BLOG_SRC = os.path.join(PROJECT, "blog")
SITE = os.path.join(OUTPUT_DIR, "blog")

FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
NAV = re.compile(r'\n?<nav class="post-nav".*?</nav>\n?', re.S)
SERIES = re.compile(r'\n?<aside class="post-series".*?</aside>\n?', re.S)


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        m = FM.match(fh.read().replace("\r\n", "\n"))
    if not m:
        return {}
    out = {}
    for key in ("title", "date", "series"):
        km = re.search(r'^%s:\s*"?(.*?)"?\s*$' % key, m.group(1), re.M)
        if km:
            out[key] = km.group(1).strip()
    return out


def collect():
    posts = []
    if not os.path.isdir(BLOG_SRC):
        return posts
    for fn in sorted(os.listdir(BLOG_SRC)):
        if not fn.endswith(".qmd") or fn.startswith("_"):
            continue
        fm = frontmatter(os.path.join(BLOG_SRC, fn))
        if not fm.get("title"):
            continue
        posts.append({
            "slug": fn[:-4],
            "title": fm["title"],
            # fall back to the filename date if frontmatter has none
            "date": fm.get("date") or "%s-%s-%s" % (fn[:4], fn[4:6], fn[6:8]),
            "series": fm.get("series"),
        })
    posts.sort(key=lambda p: (p["date"], p["slug"]))
    return posts


# A series is declared with a `series:` key in a post's frontmatter, and is
# deliberately not a category (the site keeps a closed set of seven). Where a
# post belongs to one, previous/next follow the series instead of the calendar,
# so a reader working through it is not dropped into an unrelated post
# published in between.
SERIES_PAGES = {
    "Bias Correction": "blog-series-bias-correction",
}


def build_series_header(series, index, total, page_slug):
    """A one-line banner naming the series and this post's place in it."""
    target = SERIES_PAGES.get(series)
    if not target:
        return ""
    return (
        '\n<aside class="post-series">'
        '<a class="no-external" href="../{page}">{series}</a>'
        '<span class="post-series-pos">Part {i} of {n}</span>'
        "</aside>\n"
    ).format(page=target, series=html.escape(series, quote=False),
             i=index, n=total)


def link(post, kind, label):
    # The "no-external" class is Quarto's opt-out. The site sets
    # link-external-newwindow, and Quarto's script decides internal vs external
    # by matching the resolved URL against site-url. That is correct in
    # production but flags these links when the page is opened straight off
    # disk, giving them target="_blank" and an external icon. Opting out keeps
    # prev/next navigating in place wherever the page is served from.
    return (
        '<a class="post-nav-{k} no-external" href="./{slug}" rel="{k}">'
        '<span class="post-nav-label">{label}</span>'
        '<span class="post-nav-title">{title}</span></a>'
    ).format(k=kind, slug=post["slug"], label=label,
             title=html.escape(post["title"], quote=False))


def build_nav(prev_post, next_post):
    parts = []
    if prev_post:
        parts.append(link(prev_post, "prev", "Previous"))
    if next_post:
        parts.append(link(next_post, "next", "Next"))
    if not parts:
        return ""
    return ('\n<nav class="post-nav" aria-label="Post navigation">\n  '
            + "\n  ".join(parts) + "\n</nav>\n")


def main():
    posts = collect()
    if not posts:
        print("blog-prev-next: no posts found", file=sys.stderr)
        return

    # Per-series orderings, alongside the global chronological one.
    series_posts = {}
    for p in posts:
        if p.get("series"):
            series_posts.setdefault(p["series"], []).append(p)

    written = skipped = in_series = 0
    for i, post in enumerate(posts):
        target = os.path.join(SITE, post["slug"] + ".html")
        if not os.path.exists(target):
            skipped += 1
            continue

        # Inside a series, neighbours come from the series, not the calendar.
        header = ""
        s = post.get("series")
        if s and s in series_posts:
            group = series_posts[s]
            j = group.index(post)
            prev_post = group[j - 1] if j > 0 else None
            next_post = group[j + 1] if j + 1 < len(group) else None
            header = build_series_header(s, j + 1, len(group), post["slug"])
            in_series += 1
        else:
            prev_post = posts[i - 1] if i > 0 else None
            next_post = posts[i + 1] if i + 1 < len(posts) else None

        nav = build_nav(prev_post, next_post)

        with open(target, encoding="utf-8") as fh:
            page = fh.read()

        page = NAV.sub("\n", page)          # drop any nav from a previous run
        page = SERIES.sub("", page)         # and any series banner

        # The banner sits directly under the post's title block.
        if header:
            tb = page.find('id="title-block-header"')
            if tb != -1:
                close = page.find("</header>", tb)
                if close != -1:
                    cut = close + len("</header>")
                    page = page[:cut] + header + page[cut:]

        if not nav:
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(page)
            continue

        # Prefer to sit above the comments; otherwise close out the article.
        anchor = None
        for candidate in ('<div id="giscus-comments"',
                          '<div class="giscus"',
                          "</main>"):
            idx = page.find(candidate)
            if idx != -1:
                anchor = idx
                break
        if anchor is None:
            skipped += 1
            continue

        page = page[:anchor] + nav + page[anchor:]
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(page)
        written += 1

    print("blog-prev-next: %d posts linked, %d in a series, %d skipped"
          % (written, in_series, skipped))


if __name__ == "__main__":
    main()
