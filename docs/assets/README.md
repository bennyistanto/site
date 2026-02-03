# Assets Directory

This directory contains all static assets for the website.

## Structure

```
assets/
├── logo.png              # Site logo (navbar)
├── favicon.ico           # Browser favicon
└── spotlight/            # Homepage spotlight images
    └── landsat-name.jpg  # Current showcase image
```

## Image Guidelines

### Logo
- Format: PNG with transparent background
- Recommended size: 200x200px or similar square dimensions
- Used in: Navbar

### Favicon
- Format: ICO or PNG
- Size: 32x32px or 16x16px
- Used in: Browser tab

### Spotlight Images
- Format: JPG or PNG
- Recommended size: 1920x1080px or higher
- Aspect ratio: 16:9 or similar
- File size: Optimized for web (< 500KB recommended)
- Used in: Homepage showcase

## Adding New Spotlight Images

1. Add your image to `assets/spotlight/`
2. Update `index.qmd` with the new image path
3. Update the spotlight text description

Inspired by MIT's homepage approach, spotlight images showcase featured visuals with accompanying narratives.

## Optimization

Consider optimizing images before adding:
- Use tools like ImageOptim, TinyPNG, or similar
- Balance quality and file size for faster loading
