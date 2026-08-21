# benny.istan.to

Source for my personal website: [benny.istan.to](https://benny.istan.to).

Built with [Quarto](https://quarto.org), hosted on GitHub Pages. Blog posts,
a works portfolio, and a small catalogue of free climate datasets.

## What is here

| Path | What it holds |
|---|---|
| `docs/` | The Quarto project. Everything that becomes the site. |
| `docs/blog/` | Posts, one `.qmd` per post, named `YYYYMMDD-slug`. |
| `docs/blog-draft/` | Unfinished posts. Currently still rendered, see the note below. |
| `docs/works/` | Projects, experiences, consulting, maps and infographics. |
| `docs/csr/` | Climate Social Responsibility: the free dataset pages. |
| `docs/assets/` | Images, grouped by the section that uses them. |
| `docs/styles/` | Themes (`custom-light.scss`, `custom-dark.scss`) and per-page CSS. |
| `docs/script/` | Pre- and post-render hooks, run by Quarto on every build. |
| `notebook/` | The Squarespace migration tooling. See below. |

## Build hooks

Four scripts run on every build, wired up under `project:` in `docs/_quarto.yml`.

| Stage | Script | What it does |
|---|---|---|
| pre | `build-blog-archive.py` | Rebuilds `blog-archive.qmd` by year from the post filenames |
| pre | `build-blog-series.py` | Rebuilds `blog-series-bias-correction.qmd` from posts carrying a `series:` key |
| post | `blog-prev-next.py` | Adds previous/next links to each post, following the series where a post is in one |
| post | `strip-html-ext.py` | Drops the visible `.html` from internal links and normalises `\` to `/` in paths |

**`blog-archive.qmd` and `blog-series-bias-correction.qmd` are generated files.**
Edit the scripts, not the pages. Anything typed into those two is overwritten on
the next render.

A post joins the series by adding one line to its front matter:

```yaml
series: "Bias Correction"
```

Nothing else is needed. The archive picks up any post whose filename starts with
`YYYYMMDD-`.

Everything under `docs/blog-draft/` still renders and reaches the sitemap and the
site search, even though no listing page links to it. Add a `render:` list to
`docs/_quarto.yml` if you would rather it stayed private.

## Running it locally

You need [Quarto](https://quarto.org/docs/get-started/). Nothing else.

```bash
git clone https://github.com/bennyistanto/site.git
cd site/docs
quarto preview
```

`quarto render` builds the whole site into `_site/`. That folder is generated
and gitignored, so there is no need to commit it.

## Deployment

Pushing to `main` triggers a GitHub Actions workflow that renders the site and
publishes it to GitHub Pages. Because the workflow checks out only tracked
files, anything referenced by the site has to be committed, not merely present
on your machine.

## Want a site like this?

This one started on Squarespace. Moving it off took a set of Python notebooks
that convert the Squarespace XML export into Quarto markdown, pull down the
assets, and rename them to match the posts they belong to.

Those notebooks are in [`notebook/`](notebook/), and the process is written up
here:

**[Migrating a Squarespace site to Quarto](https://benny.istan.to/blog/20260208-migrating-from-squarespace-to-quarto)**

You are welcome to take any of it. Fork the repository, point the notebooks at
your own export, and strip out my content. The theme, the layouts and the
post-render hooks are all plain files you can read and change.

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
