# Benny Istanto's Personal Website

This is the source code for [benny.istan.to](https://benny.istan.to), built with [Quarto](https://quarto.org) and hosted on GitHub Pages.

## Overview

A personal website showcasing work in GIS, climate data science, and earth observation. The site features a minimal, elegant design with support for both light and dark themes.

## Tech Stack

- **Framework**: Quarto
- **Themes**: Custom light (Cosmo-based) and dark (Darkly-based) themes
- **Hosting**: GitHub Pages
- **Repository**: [github.com/bennyistanto/site](https://github.com/bennyistanto/site)

## Local Development

### Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) installed on your machine

### Setup

1. Clone the repository:
```bash
git clone https://github.com/bennyistanto/site.git
cd site/docs
```

2. Preview the site locally:
```bash
quarto preview
```

3. Build the site:
```bash
quarto render
```

## Structure

```
docs/
├── _quarto.yml          # Main configuration file
├── index.qmd            # Homepage with spotlight showcase
├── about.qmd            # About page
├── blog.qmd             # Blog listing
├── works.qmd            # Portfolio/works overview
│   └── works/           # Works sub-pages
│       ├── experiences.qmd
│       ├── projects.qmd
│       ├── consulting.qmd
│       └── maps-and-infographics.qmd
├── cv.qmd               # Curriculum Vitae
├── csr.qmd              # CSR page
├── changelog.qmd        # Site changelog
├── 404.qmd              # Custom 404 page
├── styles.css           # Main stylesheet
├── custom-light.scss    # Light theme customization
├── custom-dark.scss     # Dark theme customization
└── assets/              # Images, logos, etc.
    ├── logo.png
    ├── favicon.ico
    └── spotlight/       # Inspired by MIT's homepage
```

## Customization

### Changing the Spotlight Image

Inspired by MIT's homepage approach, edit `index.qmd` and update the image path:
```markdown
![](assets/spotlight/your-image.jpg)
```

### Updating the Spotlight Text

Edit the content within the `.spotlight-box` div in `index.qmd`.

### Theme Colors

Modify colors in:
- `custom-light.scss` for light theme
- `custom-dark.scss` for dark theme

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the main branch.

### Manual Deployment

```bash
quarto publish gh-pages
```

## Contributing

This is a personal website, but feel free to use it as a template for your own site.

## License

© 2026 Benny Istanto. All rights reserved.

## Contact

- GitHub: [@bennyistanto](https://github.com/bennyistanto)
- LinkedIn: [bennyistanto](https://linkedin.com/in/bennyistanto)
- Website: [benny.istan.to](https://benny.istan.to)
