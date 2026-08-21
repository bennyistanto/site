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

`render` writes to `../_site/`, which is generated and gitignored.

## Two files you should not edit

`blog-archive.qmd` and `blog-series-bias-correction.qmd` are rebuilt from scratch
by pre-render hooks on every build. Editing them does nothing that survives.

Change `script/build-blog-archive.py` or `script/build-blog-series.py` instead.
To add a post to the series, put one line in the post's own front matter:

```yaml
series: "Bias Correction"
```

## Where things are

| | |
|---|---|
| `_quarto.yml` | Site configuration, navigation, theme, and the four build hooks |
| `styles/custom-light.scss` | Light theme, layered on Cosmo |
| `styles/custom-dark.scss` | Dark theme, layered on Darkly |
| `styles/styles.css` | Site-wide CSS |
| `styles/*.css` | Per-page CSS, named after the page it serves |
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
