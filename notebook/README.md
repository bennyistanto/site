# Squarespace to Quarto migration

Python notebooks that convert a Squarespace XML export into a Quarto site.
They handle the bulk work: parsing the export, downloading the assets, and
renaming those assets to match the posts that use them.

**The full write-up lives in a blog post**, and that is the canonical version:

**[Migrating a Squarespace site to Quarto](https://benny.istan.to/blog/20260208-migrating-from-squarespace-to-quarto)**

It covers what the Squarespace export includes and what it silently drops, the
reasoning behind each step, the equation problem, and what is still left to do
by hand once the scripts finish. Read that first.

## Run order

| | Notebook | |
|---|---|---|
| 1 | `1_squarespace_xmlexport_to_quarto.ipynb` | Required. XML export to `.qmd` files. |
| 2 | `2_squarespace_download_assets.ipynb` | Required. Pulls the assets down off Squarespace. |
| 3 | `3_squarespace_rename_assets.ipynb` | Optional. Only if your filenames are a mess. |

Each notebook has a configuration cell at the top. Set the paths there, then
run the cells in order. Notebook 3 has a `DRY_RUN` flag; leave it on for the
first pass.

`convert_equations.py`, `convert_radiation_equations.py` and
`convert_remaining_equations.py` are a separate one-off pass. Squarespace
exports equations as images, and these rewrite them as LaTeX. Run them only if
your posts contain equations.

## Requirements

Python 3.x with Jupyter. Each notebook imports what it needs at the top.

## Before you start

- Keep the Squarespace site live until the new one is working. The export is a
  one-way door once the subscription lapses.
- Keep the raw XML. You will want to re-run the conversion after improving the
  script, and you cannot re-export from a site you no longer pay for.
- Not everything migrates, and not every asset downloads. Both are expected;
  the notebooks log what failed rather than stopping.

Provided as-is. Back up your export before running anything.
