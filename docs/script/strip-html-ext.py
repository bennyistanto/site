#!/usr/bin/env python3
"""
Quarto post-render: strip the visible .html extension from internal links.

GitHub Pages already serves /about and /about.html identically, so the pages
are reachable without the extension. This script only rewrites the links that
Quarto bakes into the rendered output so visitors never *see* .html:

  - *.html  : internal href="..." values            foo.html      -> foo
                                                     ../foo.html   -> ../foo
                                                     ./index.html  -> ./   (dir root)
                                                     foo.html#frag -> foo#frag
                                                     ..\blog/foo   -> ../blog/foo
  - search.json : "href" and "objectID" values (so search results land clean)
  - *.xml       : sitemap.xml + RSS feed URLs (so Google indexes the clean form)

External links (anything with a scheme or //), #fragments, mailto:/tel:, and
asset paths under site_libs/ are left untouched.

Idempotent: running it twice is a no-op (no .html left to strip).
Runs on Windows (local) and Linux (CI). Stdlib only.
"""

import json
import os
import re
import sys
from pathlib import Path

# --- locate the rendered output directory -----------------------------------
# When invoked by Quarto, CWD = project dir (docs/) and QUARTO_PROJECT_OUTPUT_DIR
# is set (e.g. "../_site"). This script lives in docs/script/, so the fallback
# goes up two levels: docs/script -> docs -> repo root, then into _site.
_env_out = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR")
if _env_out:
    OUTPUT_DIR = Path(_env_out).resolve()
else:
    OUTPUT_DIR = (Path(__file__).resolve().parent.parent / ".." / "_site").resolve()

# A path is "internal" if it has no URI scheme and is not a bare fragment /
# protocol-relative / mailto / tel link.
_EXTERNAL = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.\-]*:|//|#|mailto:|tel:)")


def clean_path(url: str) -> str:
    """Normalise separators and strip .html, preserving #frag / ?query."""
    if not url or _EXTERNAL.match(url):
        return url
    m = re.match(r"^([^#?]*)([#?].*)?$", url)
    path, tail = m.group(1), m.group(2) or ""
    # Quarto resolves root-relative links ("/blog/foo") using the host OS
    # separator, so a Windows render emits "..\blog/foo". Browsers normalise
    # backslashes for http(s), so those links do work, but a literal "\" is
    # not valid in a URL path (it would have to be %5C) and it shows up in
    # the status bar and in copied link text. Fix it at the source.
    path = path.replace("\\", "/")
    if not path.endswith(".html"):
        return path + tail
    base = path[:-5]  # drop ".html"
    if base == "index":
        path = "./"
    elif base.endswith("/index"):
        path = base[:-5]  # "foo/index" -> "foo/"
    else:
        path = base
    return path + tail


# --- HTML: rewrite only href="..." attribute values -------------------------
_HREF = re.compile(r'(href=")([^"]*)(")')


def process_html(text: str) -> str:
    return _HREF.sub(lambda m: m.group(1) + clean_path(m.group(2)) + m.group(3), text)


# --- search.json: rewrite href + objectID -----------------------------------
def process_search_json(text: str) -> str:
    data = json.loads(text)
    for rec in data:
        for key in ("href", "objectID"):
            if isinstance(rec.get(key), str):
                rec[key] = clean_path(rec[key])
    return json.dumps(data, ensure_ascii=False, indent=2)


# --- XML (sitemap + feeds): strip .html at the end of a URL token ------------
# Matches .html immediately before a closing tag (<) or attribute quote (").
def process_xml(text: str) -> str:
    text = re.sub(r'/index\.html(?=["<])', "/", text)
    text = re.sub(r'\.html(?=["<])', "", text)
    return text


def main() -> int:
    if not OUTPUT_DIR.is_dir():
        print(f"[strip-html-ext] output dir not found: {OUTPUT_DIR}", file=sys.stderr)
        return 1

    html_n = json_n = xml_n = 0

    for path in OUTPUT_DIR.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        try:
            if suffix in (".html", ".htm"):
                src = path.read_text(encoding="utf-8")
                out = process_html(src)
                handler_changed = out != src
                html_n += 1 if handler_changed else 0
            elif path.name == "search.json":
                src = path.read_text(encoding="utf-8")
                out = process_search_json(src)
                handler_changed = out != src
                json_n += 1 if handler_changed else 0
            elif suffix == ".xml":
                src = path.read_text(encoding="utf-8")
                out = process_xml(src)
                handler_changed = out != src
                xml_n += 1 if handler_changed else 0
            else:
                continue
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"[strip-html-ext] skipped {path.name}: {e}", file=sys.stderr)
            continue

        if handler_changed:
            path.write_text(out, encoding="utf-8")

    print(
        f"[strip-html-ext] cleaned {html_n} html, {json_n} search.json, "
        f"{xml_n} xml under {OUTPUT_DIR}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
