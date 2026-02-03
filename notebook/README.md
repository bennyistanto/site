# Squarespace to Quarto Migration Process

This folder contains Python scripts (Jupyter notebooks) that automate the heavy lifting of migrating a Squarespace website to Quarto. These scripts handle the dirty work that would otherwise take months of manual conversion.

**What these scripts do:** Convert XML exports, download assets, and organize files into a Quarto-ready structure.

**What you still need to do:** After the scripts prepare your files, you'll need to customize the Quarto site to make it beautiful (styling, layouts, navigation, etc.). This part is relatively easy but still takes time.

## Overview

The migration process consists of three main steps, each automated by a dedicated notebook:

1. **Export and convert XML to Quarto markdown** (`1_squarespace_xmlexport_to_quarto.ipynb`)
2. **Download assets from Squarespace** (`2_squarespace_download_assets.ipynb`)
3. **Rename assets to match QMD files** (`3_squarespace_rename_assets.ipynb`)

---

## Prerequisites

- Python 3.x with Jupyter Notebook
- Active Squarespace site with export access
- Required Python packages (listed in each notebook)

---

## Step 1: Export from Squarespace

### Exporting Your Content

Squarespace provides a feature to export site content into an XML file. This is primarily designed for WordPress imports, but we'll use it for Quarto conversion.

**Important:** Not everything will export, as many Squarespace features rely on platform-specific JavaScript and CSS.

### What Content Will Export

✅ **Exports successfully:**
- Blog posts (title, content, tags, categories)
- Pages (title, content)
- Text content and basic formatting
- Image URLs and references
- Publication dates and metadata

❌ **Won't export:**
- Custom CSS and JavaScript
- Form submissions and data
- Commerce data (products, orders)
- Gallery blocks (structure only, not layout)
- Custom blocks and integrations
- Comments
- Audio and video blocks (embedded content may export)
- Site structure and navigation

### Export Instructions

1. **Go to Squarespace Export Page:**
   - Visit: [Squarespace Export Settings](https://account.squarespace.com/project-picker?client_id=helpcenter&redirect_url=%2Fsettings%2Fadvanced%2Fimport-export)
   - Log in to your Squarespace account

2. **Select Your Site:**
   - Choose the website you want to export

3. **Export Your Content:**
   - Click on "Export" or "Download XML"
   - Wait for the export to complete

4. **Download the XML File:**
   - Save the `.xml` file to your local machine
   - Note the file location for use in the notebooks

**Reference:** [Squarespace Export Documentation](https://support.squarespace.com/hc/en-us/articles/206566687-Exporting-your-site?platform=v6&websiteId=5eb8f97b29c7c928b1fbaf3d)

---

## Step 2: Run the Migration Notebooks

### Notebook 1: Convert XML to Quarto Markdown

**File:** `1_squarespace_xmlexport_to_quarto.ipynb`

**Purpose:** Converts the Squarespace XML export into Quarto-compatible markdown documents (.qmd files).

**What it does:**
- Parses the XML export file
- Extracts posts and pages
- Converts HTML content to markdown
- Creates QMD files with proper frontmatter (title, date, categories, tags)
- Preserves image references and links
- Organizes output into appropriate folders

**Input:** Squarespace XML export file

**Output:** QMD files for blog posts and pages

---

### Notebook 2: Download Assets from Squarespace

**File:** `2_squarespace_download_assets.ipynb`

**Purpose:** Downloads images and other assets referenced in the QMD files from Squarespace.

**What it does:**
- Scans QMD files for asset URLs (images, PDFs, etc.)
- Downloads assets from Squarespace servers
- Saves assets to local folders
- Maintains original filenames when possible
- Handles download errors and retries

**Input:** QMD files with Squarespace asset URLs

**Output:** Downloaded assets in the assets folder

**⚠️ Important Note:** Not all assets will successfully download. Some reasons include:
- Private or restricted content
- Expired or moved URLs
- Assets that require authentication
- Rate limiting from Squarespace servers

---

### Notebook 3: Rename Assets to Match QMD Files

**File:** `3_squarespace_rename_assets.ipynb`

**Purpose:** Renames downloaded assets to match their associated QMD files for better organization.

**What it does:**
- Scans QMD files for image references
- Identifies which assets are used in which QMD files
- Renames assets based on the QMD filename (e.g., `2020-01-15-blog-post-01.png`)
- Updates image paths in QMD files to reflect new names
- Preserves unused assets with original names

**Input:**
- QMD files
- Downloaded assets

**Output:**
- Renamed assets
- Updated QMD files with corrected image paths

**Note:** Assets that aren't referenced in any QMD file will not be renamed. This helps identify unused or orphaned assets.

---

## Workflow Summary

```
┌─────────────────────────────┐
│  1. Export from Squarespace │
│     (Manual - via website)  │
└──────────────┬──────────────┘
               │
               │ squarespace-export.xml
               │
               ▼
┌─────────────────────────────┐
│  2. Convert XML to QMD      │
│  (Notebook 1)               │
└──────────────┬──────────────┘
               │
               │ *.qmd files
               │
               ▼
┌─────────────────────────────┐
│  3. Download Assets         │
│  (Notebook 2)               │
└──────────────┬──────────────┘
               │
               │ Images, PDFs, etc.
               │
               ▼
┌─────────────────────────────┐
│  4. Rename Assets           │
│  (Notebook 3)               │
└──────────────┬──────────────┘
               │
               │ Organized assets
               │
               ▼
┌─────────────────────────────┐
│  5. Build Quarto Site       │
│     quarto render           │
└─────────────────────────────┘
```

---

## Post-Migration Tasks

After running all three notebooks, the automated conversion is complete. Your content is now in Quarto format, but the real work begins - making it beautiful and functional.

**The scripts save you months** by automating:
- XML parsing and markdown conversion
- Bulk asset downloading
- File organization and renaming

**You still need to spend time on:**

1. **Review QMD Files:**
   - Check for formatting issues
   - Verify that images are displaying correctly
   - Update any broken links
   - Clean up markdown formatting

2. **Manual Adjustments:**
   - Recreate custom layouts (Squarespace blocks won't transfer)
   - Rebuild navigation structure
   - Add custom CSS/styling
   - Configure Quarto settings in `_quarto.yml`

3. **Asset Management:**
   - Verify all critical images downloaded successfully
   - Manually download any missing assets
   - Optimize images for web (compress, resize)
   - Organize assets into logical folders

4. **Test the Site:**
   - Run `quarto preview` to test locally
   - Check all pages and posts
   - Test internal links
   - Verify responsive design

5. **Deploy:**
   - Configure GitHub Pages or other hosting
   - Set up custom domain (if applicable)
   - Configure redirects from old Squarespace URLs

---

## Disclaimer

⚠️ **Use at Your Own Risk**

This migration process is provided as-is without warranty. Please note:

- **Not all content will migrate perfectly** - Manual review and cleanup are required
- **Not all assets will download** - Some Squarespace content may not be publicly accessible
- **Data loss is possible** - Always keep backups of your original Squarespace export
- **Platform differences** - Squarespace and Quarto work differently; some features won't translate
- **Testing required** - Thoroughly test your migrated site before going live

**Recommendation:** Keep your Squarespace site active during migration and testing. Only deactivate after confirming the new Quarto site is working correctly.

---

## Troubleshooting

### Common Issues

**Problem:** XML export is empty or incomplete
- **Solution:** Check Squarespace export settings, ensure you're exporting the correct site

**Problem:** Assets won't download (403/404 errors)
- **Solution:** Assets may be private or moved. Download manually from Squarespace admin panel

**Problem:** QMD files have broken formatting
- **Solution:** Review and manually fix markdown. Some Squarespace HTML may not convert cleanly

**Problem:** Images don't display in Quarto site
- **Solution:** Check file paths in QMD files, ensure assets are in correct folders

---

## Additional Resources

- [Quarto Documentation](https://quarto.org/docs/guide/)
- [Squarespace Export Guide](https://support.squarespace.com/hc/en-us/articles/206566687-Exporting-your-site)
- [Markdown Guide](https://www.markdownguide.org/)
- [Quarto Publishing](https://quarto.org/docs/publishing/)

---

## License

© 2026 Benny Istanto. All rights reserved.

These notebooks are provided for personal use in migrating your own Squarespace site. Feel free to adapt them for your needs.
