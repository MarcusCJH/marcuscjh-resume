# Marcus's LaTeX Resume and CV 📄

A data-driven LaTeX project that generates two documents from the same portfolio data:

- **Resume:** curated one-pager — selected highlights ([PDF](https://marcuscjh.github.io/marcuscjh-resume/resume.pdf))
- **CV:** full dossier — everything you have ([PDF](https://marcuscjh.github.io/marcuscjh-resume/cv.pdf))

[![View Documents](https://img.shields.io/badge/View-Resume%20%2B%20CV-blue)](https://marcuscjh.github.io/marcuscjh-resume/)
[![Build Status](https://github.com/marcuscjh/marcuscjh-resume/workflows/Build%20and%20Deploy%20LaTeX%20Resume/badge.svg)](https://github.com/marcuscjh/marcuscjh-resume/actions)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## ✨ Key Features

- **Data-Driven**: Single source of truth from portfolio data.json
- **Dual Documents**: curated Resume + full CV from one data source
- **Auto-Sync**: Python script updates both sets of LaTeX sections automatically
- **Modular Design**: Clean separation of content and formatting
- **Automated Workflow**: GitHub Actions syncs data, builds both PDFs, and creates PRs automatically
- **Scheduled Updates**: Checks for data.json updates every 6 hours
- **Live Preview**: GitHub Pages with instant download

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- LaTeX distribution (TeX Live or MiKTeX)

### Build Documents
```bash
# Sync CV (full) + Resume (curated) sections
python sync_resume.py --target all

# Build
make cv        # full dossier -> out/cv.pdf
make resume    # curated one-pager -> out/resume.pdf
make build     # sync + both
```

The **CV** uses pdfLaTeX; the **Resume** uses XeLaTeX. Add a headshot at
`src/assets/photo.jpg`; the Resume shows a placeholder when it is absent.

### Data Source
`sync_resume.py --source local|remote|auto` (default `auto`):

- **local**: always use the committed `data.json`
- **remote**: always fetch `https://marcuscjh.github.io/data.json`
- **auto** (default): use `data.json` if present, otherwise fetch remote

The scheduled GitHub Actions sync runs with `--source remote`, so CI always
picks up the live portfolio data.

> **Note:** The portfolio is the long-term source of truth. The committed
> `data.json` also carries Resume curation metadata under `config.cv` /
> timeline `cv` fields (density, compact bullets, etc.). Until the portfolio
> includes those fields, remote syncs (including CI) build the Resume with
> built-in fallbacks. Add the `cv` metadata to the portfolio before relying
> on remote sync for the curated Resume.

### CI checks
After building the Resume, CI asserts that `resume.pdf` is exactly one page.
The Resume font stack falls back through common system and TeX sans fonts.

## 📁 Project Structure

```
.
├── sync_resume.py
├── data.json
├── src/
│   ├── resume.tex                 # Curated one-pager (XeLaTeX)
│   ├── cv.tex                     # Full dossier (pdfLaTeX)
│   ├── assets/photo.jpg           # Resume headshot
│   ├── styles/
│   │   ├── resume-formatting.sty  # Curated resume design system
│   │   └── cv-formatting.sty      # Full CV template
│   └── sections/
│       ├── resume/                # Curated sections
│       └── cv/                    # Full sections
├── docs/
│   ├── resume.pdf
│   └── cv.pdf
└── out/
```

## 📝 How It Works

### Automated Workflow
The GitHub Actions workflow automatically:
1. **Syncs** data.json from portfolio (every 6 hours or on push/manual trigger)
2. **Detects** changes in .tex files (from sync or manual edits)
3. **Builds** the resume and CV PDFs if changes are detected
4. **Creates PR** with updated .tex files and both PDFs
5. **Exits early** if no changes detected (saves resources)

### Manual Workflow
1. **Source**: Portfolio data.json (local or remote)
2. **Sync**: Python script extracts data and generates LaTeX sections
3. **Build**: LaTeX compiles sections into final PDF

### Content Sections
- **Header**: Name, email, portfolio website
- **Summary**: Professional overview from data
- **Experience**: Work history with detailed descriptions
- **Education**: Academic background with locations
- **Skills**: Categorized technical skills
- **Projects**: Showcase projects with descriptions
- **Certifications**: Professional certifications with years

### Data Structure
```json
{
  "config": {
    "real_name": "Marcus Chan",
    "email": "marcuschanjh@gmail.com",
    "website": "https://marcuscjh.github.io",
    "summary": "Professional summary...",
    "cv": {
      "title": "Technical Lead · Cloud & Full-Stack",
      "summary": "Short human-first CV summary...",
      "photo": "optional URL or path"
    }
  },
  "timeline": [
    {
      "category": "work",
      "title": "Job Title",
      "company": "Company",
      "cv": {
        "density": "featured",
        "bullets": ["CV-specific achievement"]
      }
    },
    {"category": "education", "title": "Degree", "company": "University", ...},
    {"category": "certification", "title": "Cert Name", "company": "Issuer", ...}
  ],
  "showcase": [...],
  "skills": {...}
}
```

`config.cv` controls the curated Resume title, summary, and optional photo.
Timeline entries may use a `cv` object with fields such as `density`,
`bullets`, `line`, `roles`, and `featured`.

## 🔧 Usage

### Automated Updates (Recommended)
The workflow runs automatically:
- **Every 6 hours**: Checks for data.json updates from portfolio
- **On push to master**: Syncs and builds if .tex files changed
- **Manual trigger**: Use "Run workflow" in GitHub Actions tab

When changes are detected, a PR is automatically created with:
- Updated .tex section files
- Rebuilt resume and CV PDFs

### Manual Update
```bash
# Sync latest data and rebuild locally
make build
```

### Customize Data
- Edit `data.json` in your portfolio repo
- Workflow automatically syncs and creates PR within 6 hours
- Or push .tex changes directly - workflow will build PDF and create PR
- Script automatically uses local `data2.json` if available

---

<div align="center">
Made with ❤️ by Marcus
</div> 