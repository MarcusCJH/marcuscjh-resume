# Marcus's LaTeX Resume and CV 📄

A data-driven LaTeX project that generates two documents from the same portfolio data:

- **Resume:** curated one-pager — selected highlights ([PDF](https://marcuscjh.github.io/marcuscjh-resume/resume.pdf))
- **CV:** full dossier — everything you have ([PDF](https://marcuscjh.github.io/marcuscjh-resume/cv.pdf))

[![View Documents](https://img.shields.io/badge/View-Resume%20%2B%20CV-blue)](https://marcuscjh.github.io/marcuscjh-resume/)
[![Build Status](https://github.com/marcuscjh/marcuscjh-resume/workflows/Build%20and%20Deploy%20LaTeX%20Resume/badge.svg)](https://github.com/marcuscjh/marcuscjh-resume/actions)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## ✨ Key Features

- **Data-Driven**: Single source of truth at [www.marcuscjh.com/data.json](https://www.marcuscjh.com/data.json)
- **Dual Documents**: curated Resume + full CV from one data source
- **Auto-Sync**: Python script updates both sets of LaTeX sections automatically
- **Modular Design**: Clean separation of content and formatting
- **Automated Workflow**: GitHub Actions syncs data, builds both PDFs, and creates PRs automatically
- **Scheduled Updates**: Checks the live portfolio data every 6 hours
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
Portfolio JSON is **not** committed here. Source of truth:

**https://www.marcuscjh.com/data.json**

`sync_resume.py --source auto|remote|local` (default `auto`):

- **auto** (default): use untracked local `data.json` / `data2.json` if present (handy for testing), otherwise fetch the live portfolio JSON
- **remote**: always fetch https://www.marcuscjh.com/data.json
- **local**: always use local file (for forced offline runs)

CI always uses `--source remote`. Local `data.json` stays gitignored so test copies never get committed.

### CI checks
After building the Resume, CI asserts that `resume.pdf` is exactly one page.
The Resume uses OFL **Archivo** + **Space Grotesk** from `src/fonts/` (Swiss
Portfolio 2026 tokens in `resume-formatting.sty`), with TeX Gyre Heros /
Latin Modern Sans as fallbacks if those files are missing. CI rebuilds when
`src/fonts/` changes.

## 📁 Project Structure

```
.
├── sync_resume.py
├── src/
│   ├── resume.tex                 # Curated one-pager (XeLaTeX)
│   ├── cv.tex                     # Full dossier (pdfLaTeX)
│   ├── assets/photo.jpg           # Resume headshot
│   ├── fonts/                     # Archivo + Space Grotesk (OFL)
│   ├── styles/
│   │   ├── resume-formatting.sty  # Swiss Portfolio resume design system
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
1. **Syncs** from www.marcuscjh.com/data.json (every 6 hours or on push/manual trigger)
2. **Detects** changes in .tex files (from sync or manual edits)
3. **Builds** the resume and CV PDFs if changes are detected
4. **Creates PR** with updated .tex files and both PDFs
5. **Exits early** if no changes detected (saves resources)

### Manual Workflow
1. **Source**: Live portfolio JSON (optional local override)
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
- **Every 6 hours**: Checks for updates on www.marcuscjh.com/data.json
- **On push to master**: Syncs and builds if .tex files changed
- **Manual trigger**: Use "Run workflow" in GitHub Actions tab

When changes are detected, a PR is automatically created with:
- Updated .tex section files
- Rebuilt resume and CV PDFs

### Manual Update
```bash
# Sync latest portfolio data and rebuild locally
make build
```

### Customize Data
- Edit the portfolio data at www.marcuscjh.com (portfolio repo)
- Workflow syncs and opens a PR within 6 hours
- Or push .tex changes directly — workflow builds PDFs and creates a PR
- For local testing, drop an untracked `data.json` in the repo root — `make sync` / `--source auto` will pick it up

---

<div align="center">
Made with ❤️ by Marcus
</div> 