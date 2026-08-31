# The Quarto project

This directory is the site. Everything in it becomes [benny.istan.to](https://benny.istan.to).

**The project README is one level up**, in [`../README.md`](../README.md), and that
is the canonical one: what the repository holds, how deployment works, and how to
reuse any of this for your own site. This file only covers what you need to know
once you are working inside `docs/`.

## Commands

Run from this directory:

```bash
quarto preview
```

```bash
quarto render
```

`render` writes to `../_site/`, which is generated and gitignored. Both need
Python 3 on your `PATH`, because four build hooks run on every render.

## Two files you should not edit

`blog-archive.qmd` and `blog-series-bias-correction.qmd` are rebuilt from scratch
by pre-render hooks on every build. Editing them does nothing that survives.

Change `script/build-blog-archive.py` or `script/build-blog-series.py` instead.
To add a post to the series, put one line in the post's own front matter:

```yaml
series: "Bias Correction"
```

## Adding a post

One file in `blog/`, named `YYYYMMDD-slug.qmd`. The archive and the listing pick
it up on the next render; nothing has to be registered anywhere.

Front matter looks like this:

```yaml
---
title: "Something specific"
author: "Benny Istanto"
date: "2026-06-26"
description: "One or two sentences. This is the blog card subtitle and the meta description."
image: "../assets/image-blog/20260626-slug-01.png"
categories:
  - "Climate"
  - "Data Science"
---
```

**Categories are a fixed set of seven**, and new ones should not be invented:
Climate, Data Science, General, GIS, Remote Sensing, Research, Travel.

**Images live in `assets/image-blog/`** and are named after the post that uses
them, `YYYYMMDD-slug-NN.png`, numbered from `01`. The `image:` in the front
matter is the card thumbnail on the blog listing, so it wants to read well
cropped to a wide, short box.

Drafts go in `blog-draft/`, which is gitignored. They still render locally and
land in your own search index, but CI never sees them.

## Things the pages can do

- **Collapsible code**, used for long scripts at the foot of a post:

  ````markdown
  ::: {.callout-note collapse="true" title="Python - what it does"}
  ```python
  ...
  ```
  :::
  ````

- **Diagrams**, rendered natively by Quarto from a ` ```{mermaid} ` block. Write
  the arrows as plain characters. HTML entities like `&le;` get escaped and show
  up literally, so use `≤` itself.

- **Side-by-side figures**, via `::: {layout-ncol=2}`. Worth checking at mobile
  width first: wide, short images become unreadable in two columns.

- **Maths**, in `$…$` and `$$…$$`.

## Where things are

| | |
| --- | --- |
| `_quarto.yml` | Site configuration, navigation, theme, and the four build hooks |
| `styles/custom-light.scss` | Light theme, layered on Cosmo |
| `styles/custom-dark.scss` | Dark theme, layered on Darkly |
| `styles/styles.css` | Site-wide CSS |
| `styles/*.css` | Per-page CSS, named after the page it serves |
| `styles/blog-post.css` | Post furniture: series banner, and `.pdf-embed` for an embedded PDF viewer |
| `assets/image-spotlight/` | The homepage hero image |
| `assets/image-logo/favicon.png` | Favicon |

Dark-mode rules key off `body.quarto-dark`, which is what Quarto's own toggle
sets. An `@media (prefers-color-scheme: dark)` block reads the operating system
instead and ignores the toggle, so a visitor switching the site to dark gets the
light styling. The per-page stylesheets carry this note where it matters.

## Changing the homepage

The hero image and the spotlight text both live in `index.qmd`, inside the
`.hero-section` and `.spotlight-box` divs. Layout for both is in
`styles/index.css`.
