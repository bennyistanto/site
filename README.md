# benny.istan.to

Source for my personal website: [benny.istan.to](https://benny.istan.to).

Built with [Quarto](https://quarto.org), hosted on GitHub Pages. Around 175 blog
posts going back to 2003, a works portfolio, and a small catalogue of free
climate datasets.

## What is here

| Path | What it holds |
|---|---|
| `docs/` | The Quarto project. Everything that becomes the site. |
| `docs/blog/` | Posts, one `.qmd` per post, named `YYYYMMDD-slug`. |
| `docs/works/` | Projects, experiences, consulting, maps and infographics. |
| `docs/csr/` | Climate Social Responsibility: the free dataset pages. |
| `docs/assets/` | Images, grouped by the section that uses them. |
| `docs/styles/` | Themes (`custom-light.scss`, `custom-dark.scss`) and per-page CSS. |
| `docs/script/` | Pre- and post-render hooks, run by Quarto on every build. |
| `notebook/` | The Squarespace migration tooling. See below. |
| `downloads/` | The original Squarespace XML export, kept for reference. |

Two directories exist locally but are gitignored and never reach the deployed
site: `docs/blog-draft/`, for posts that are not finished, and `temp/`, for
scratch work. Drafts render if you build locally, so they show up in your own
`_site/` and its search index, but CI only ever sees tracked files.

## Requirements

[Quarto](https://quarto.org/docs/get-started/) and Python 3.

Quarto does the rendering. Python runs the four build hooks below, and they use
only the standard library, so there is nothing to install beyond a working
`python3` on your `PATH`.

## Running it locally

```bash
git clone https://github.com/bennyistanto/site.git
```

```bash
cd site/docs && quarto preview
```

`quarto render` builds the whole site into `_site/` at the repository root. That
folder is generated and gitignored.

## Build hooks

Four scripts run on every build, wired up under `project:` in `docs/_quarto.yml`.

| Stage | Script | What it does |
|---|---|---|
| pre | `build-blog-archive.py` | Rebuilds `blog-archive.qmd`, grouped by year, from the post filenames |
| pre | `build-blog-series.py` | Rebuilds `blog-series-bias-correction.qmd` from posts carrying a `series:` key |
| post | `blog-prev-next.py` | Adds previous and next links to each post, following the series where a post is in one |
| post | `strip-html-ext.py` | Drops the visible `.html` from internal links, and normalises `\` to `/` in paths |

**`blog-archive.qmd` and `blog-series-bias-correction.qmd` are generated files.**
Edit the scripts, not the pages. Anything typed into those two is overwritten on
the next render.

Adding a post needs nothing beyond the file itself. The archive picks up anything
in `docs/blog/` whose filename starts with `YYYYMMDD-`. To put a post in the
series as well, add one line to its front matter:

```yaml
series: "Bias Correction"
```

## Deployment

Pushing to `main` runs `.github/workflows/publish.yml`, which clears the Quarto
cache, renders with `--no-cache`, and publishes `_site/` to the `gh-pages` branch
with the `benny.istan.to` CNAME.

The workflow checks out only tracked files, so anything the site references has
to be committed. An image that renders locally but was never added to git will
simply be missing once deployed, and nothing in the build will complain.

## Want a site like this?

This one started on Squarespace. Moving it off took a set of Python notebooks
that convert the Squarespace XML export into Quarto markdown, pull down the
assets, and rename them to match the posts they belong to.

Those notebooks are in [`notebook/`](notebook/), and the process is written up
here:

**[Migrating a Squarespace site to Quarto](https://benny.istan.to/blog/20260208-migrating-from-squarespace-to-quarto)**

You are welcome to take any of it. Fork the repository, point the notebooks at
your own export, and strip out my content. The theme, the layouts and the build
hooks are all plain files you can read and change.

If you are not coming from Squarespace, skip the notebooks entirely: `docs/`
on its own is a working example of a Quarto site with a blog, a portfolio and
light/dark theming.

## Contact

- Website: [benny.istan.to](https://benny.istan.to)
- GitHub: [@bennyistanto](https://github.com/bennyistanto)
- LinkedIn: [bennyistanto](https://linkedin.com/in/bennyistanto)

## License

Site content, meaning the writing and images, is © 2026 Benny Istanto.

The migration notebooks and the site machinery are free to reuse and adapt.
