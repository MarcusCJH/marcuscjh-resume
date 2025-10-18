# Marcus's LaTeX Resume 📄

A data-driven, modular LaTeX resume that syncs with portfolio data and builds automatically.

[![View Resume](https://img.shields.io/badge/View%20Resume-PDF-blue)](https://marcuscjh.github.io/marcuscjh-resume/)
[![Build Status](https://github.com/marcuscjh/marcuscjh-resume/workflows/Build%20and%20Deploy%20LaTeX%20Resume/badge.svg)](https://github.com/marcuscjh/marcuscjh-resume/actions)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## ✨ Key Features

- **Data-Driven**: Single source of truth from portfolio data.json
- **Auto-Sync**: Python script updates all LaTeX sections automatically
- **Modular Design**: Clean separation of content and formatting
- **Automated Builds**: GitHub Actions CI/CD pipeline
- **Live Preview**: GitHub Pages with instant download

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- LaTeX distribution (TeX Live or MiKTeX)

### Build Resume
```bash
# 1. Sync data and update sections
python sync_resume.py

# 2. Compile PDF
xelatex -output-directory=out -aux-directory=auxil src/resume.tex
```

### Data Source
- **Local**: Uses `data.json` if available
- **Remote**: Fetches from `https://marcuscjh.github.io/data.json`

## 📁 Project Structure

```
.
├── sync_resume.py          # Data sync script
├── data.json              # Data source (optional)
├── src/
│   ├── resume.tex         # Main LaTeX entry point
│   └── sections/          # Auto-generated content
│       ├── header.tex         # Contact info
│       ├── summary.tex        # Professional summary
│       ├── education.tex      # Academic background
│       ├── experience.tex     # Work experience
│       ├── skills.tex         # Technical skills
│       ├── projects.tex       # Project highlights
│       └── certifications.tex # Certifications
└── out/                   # Generated PDF output
```

## 📝 How It Works

### Data Flow
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
    "summary": "Professional summary..."
  },
  "timeline": [
    {"category": "work", "title": "Job Title", "company": "Company", ...},
    {"category": "education", "title": "Degree", "company": "University", ...},
    {"category": "certification", "title": "Cert Name", "company": "Issuer", ...}
  ],
  "showcase": [...],
  "skills": {...}
}
```

## 🔧 Usage

### Update Resume
```bash
# Sync latest data and rebuild
python sync_resume.py
xelatex -output-directory=out -aux-directory=auxil src/resume.tex
```

### Customize Data
- Edit `data.json` locally for testing
- Push changes to portfolio repo for live updates
- Script automatically uses local data when available

---

<div align="center">
Made with ❤️ by Marcus
</div> 