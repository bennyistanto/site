#!/usr/bin/env python3
"""
Quarto pre-render: build an index page for each post series.

A series is declared with a `series:` key in a post's frontmatter. That is
deliberately not a category: the site keeps a closed set of seven, and a
series is a different kind of thing anyway, being an ordered reading path
rather than a subject label. Quarto ignores the key, and blog.qmd names its
listing fields explicitly, so it never leaks into the UI.

Two consumers read it: this script, which writes the index, and
blog-prev-next.py, which makes previous/next follow the series rather than the
calendar.

Idempotent: same posts in, same bytes out.
"""

import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(_HERE)
BLOG = os.path.join(PROJECT, "blog")

FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

# One entry per series: the frontmatter value, the output page, and the prose.
SERIES = {
    "Bias Correction": {
        "file": "blog-series-bias-correction.qmd",
        "title": "Bias Correction",
        "subtitle": "Two years of correcting satellite rainfall, in order",
        "lede": (
            "Everything below is one piece of work: a framework for correcting "
            "daily satellite precipitation over Indonesia, from the first "
            "attempt to understand the problem through to a published paper and "
            "a submitted thesis.\n\n"
            "The posts are interleaved with unrelated ones on the "
            "[main blog](blog.qmd), so this page is the reading order. Each post "
            "also links to the next one in the series rather than to whatever "
            "was published next."
        ),
        # year -> (heading, one-line framing)
        "acts": {
            "2024": ("Working out the pieces",
                     "Before any correction could be judged, the scaffolding "
                     "had to exist: what the rain is like, what to measure it "
                     "against, and how to score anything at all."),
            "2025": ("Building, and two findings",
                     "The model, the gate that keeps it quiet, the trade-offs, "
                     "and then the wall and the way through it."),
            "2026": ("Writing and publishing",
                     "Documentation, a paper, an examination that reframed the "
                     "whole argument, and a graduation letter."),
        },
    },
    "El Nino 2026": {
        "file": "blog-series-el-nino.qmd",
        "title": "El Niño 2026",
        "subtitle": "Drought is what arrives minus what leaves. "
                    "Most maps measure only the arriving half",
        "lede": (
            "An El Niño developed through 2026. The question that follows is "
            "always the same: where will it be dry, and how dry.\n\n"
            "Drought is a balance. Water arrives as rain and leaves as "
            "evaporation, and the atmosphere's capacity to pull it out varies "
            "on its own, driven by temperature, humidity, wind and sunlight. "
            "Both halves have standard, well-documented indices behind them. In "
            "practice almost everything published measures the first half and "
            "stops.\n\n"
            "This series measures both, globally, across seventy-six years of "
            "record, and asks what El Niño does to each. Nothing here is a new "
            "method. The indices are the ones climate services already run, and "
            "the framework for turning them into events dates to 1967. What is "
            "unusual is the combination, and the insistence on reporting how "
            "much the record can actually carry.\n\n"
            "The posts are interleaved with unrelated ones on the "
            "[main blog](blog.qmd), so this page is the reading order. Each "
            "post also links to the next one in the series rather than to "
            "whatever was published next.\n\n"
            "### The whole series, in six findings\n\n"
            "**Globally, El Nino barely touches dry spells.** It raises the "
            "share of dry months by one to fourteen per cent of itself, which "
            "is real and close to useless. Rainfall moves around the tropics "
            "rather than leaving the planet.\n\n"
            "**Regionally it changes a great deal.** Nineteen more months in "
            "every hundred come in short of rain over the Maritime Continent, "
            "with the sign reversed over southwestern North America.\n\n"
            "**It starts dry spells rather than stretching them**, by up to "
            "1.9 times in onsets against at most 1.16 in duration. A monitor "
            "already watching a spell would not see it coming.\n\n"
            "**Both halves of the balance move together, not apart.** The "
            "case this project was built to find, normal rain with abnormal "
            "thirst, is 0.3 per cent of the land where both responses are "
            "solid. The other 99.7 per cent sits on the diagonal.\n\n"
            "**Record-breaking evaporative demand runs four to five times "
            "likelier than chance** across the coming seven seasons, and "
            "about half of that is the warming trend rather than the "
            "Pacific.\n\n"
            "**On 56 to 74 per cent of land the relationship predicts nothing.** "
            "Hide a season, refit, predict it, and the fit does worse than "
            "guessing that season's own average. The series is really about "
            "the 18 per cent where it holds, and the maps do not look like "
            "they are."
        ),
        "acts": {
            "2026": ("Two halves of a balance",
                     "What arrives, what leaves, how long each lasts, and how "
                     "far forty-four events will stretch."),
        },
    },
}


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        m = FM.match(fh.read().replace("\r\n", "\n"))
    if not m:
        return {}
    out = {}
    for key in ("title", "date", "series", "description"):
        km = re.search(r'^%s:\s*"?(.*?)"?\s*$' % key, m.group(1), re.M)
        if km:
            out[key] = km.group(1).strip()
    return out


def collect(series_name):
    posts = []
    if not os.path.isdir(BLOG):
        return posts
    for fn in sorted(os.listdir(BLOG)):
        if not fn.endswith(".qmd") or fn.startswith("_"):
            continue
        fm = frontmatter(os.path.join(BLOG, fn))
        if fm.get("series") != series_name or not fm.get("title"):
            continue
        posts.append({
            "slug": fn[:-4],
            "title": fm["title"],
            "date": fm.get("date") or "%s-%s-%s" % (fn[:4], fn[4:6], fn[6:8]),
            "description": fm.get("description", ""),
        })
    posts.sort(key=lambda p: (p["date"], p["slug"]))
    return posts


MONTHS = ("January February March April May June July August September "
          "October November December").split()


def pretty(date):
    try:
        y, m, d = date.split("-")
        return "%d %s %s" % (int(d), MONTHS[int(m) - 1], y)
    except (ValueError, IndexError):
        return date


def build(name, spec, posts):
    out = [
        "---",
        'title: "%s"' % spec["title"],
        'subtitle: "%s"' % spec["subtitle"],
        "page-layout: full",
        "toc: true",
        "toc-title: Years",
        "css: styles/blog.css",
        "---",
        "",
        spec["lede"],
        "",
    ]
    n = len(posts)
    seen = 0
    for year in sorted({p["date"][:4] for p in posts}):
        heading, framing = spec["acts"].get(year, (year, ""))
        out.append("## %s {#year-%s}" % (year, year))
        out.append("")
        out.append("**%s.** %s" % (heading, framing))
        out.append("")
        for p in [q for q in posts if q["date"][:4] == year]:
            seen += 1
            out.append("**%d. [%s](blog/%s.qmd)**  "
                       % (seen, p["title"], p["slug"]))
            out.append("*%s*  " % pretty(p["date"]))
            if p["description"]:
                out.append("%s" % p["description"])
            out.append("")
    out.append("---")
    out.append("")
    out.append("%d posts, %s to %s."
               % (n, pretty(posts[0]["date"]), pretty(posts[-1]["date"])))
    out.append("")
    return "\n".join(out)


def main():
    total = 0
    for name, spec in SERIES.items():
        posts = collect(name)
        if not posts:
            print("[blog-series] no posts tagged %r, skipping" % name,
                  file=sys.stderr)
            continue
        target = os.path.join(PROJECT, spec["file"])
        new = build(name, spec, posts)
        old = ""
        if os.path.exists(target):
            with open(target, encoding="utf-8") as fh:
                old = fh.read().replace("\r\n", "\n")
        if new == old:
            print("[blog-series] %s: %d posts, already current"
                  % (name, len(posts)))
            continue
        with open(target, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        print("[blog-series] %s: rebuilt with %d posts (%s to %s)"
              % (name, len(posts), posts[0]["date"], posts[-1]["date"]))
        total += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
