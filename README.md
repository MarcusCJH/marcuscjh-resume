# Marcus's LaTeX Resume 📄

A professionally crafted, modular LaTeX resume with automated builds and live preview.

[![View Resume](https://img.shields.io/badge/View%20Resume-PDF-blue)](https://marcuscjh.github.io/marcuscjh-resume/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


## ✨ Key Features

- **Modular Architecture**: Organized sections and styles for easy updates
- **Automated Builds**: GitHub Actions CI/CD pipeline that:
  - Builds PDF on relevant file changes
  - Auto-commits to `docs/` directory
  - Optimizes workflow with smart change detection
- **Live Preview**: Custom landing page with instant preview and download options
- **Clean Design**: Minimal and accessible web layout via GitHub Pages

## 🚀 Getting Started

### Prerequisites

- LaTeX distribution (TeX Live or MiKTeX)
- LaTeX editor (recommended)

### Quick Start

1. Clone the repository
```bash
git clone https://github.com/yourusername/your-resume-repo.git
```

2. Compile the resume
```bash
pdflatex resume.tex
```

## 📁 Project Structure

```
.
├── src/
│   ├── resume.tex          # Main LaTeX entry point
│   └── sections/           # Modular content sections
│       ├── header.tex          # Contact information
│       ├── education.tex       # Academic background
│       ├── experience.tex      # Professional experience
│       ├── skills.tex          # Technical skills
│       └── projects.tex        # Project highlights
│   └── styles/             # Design and formatting
│       └── formatting.sty  # LaTeX style definitions
├── docs/                   # Public assets
│   ├── index.html          # Landing page
│   └── resume.pdf          # Latest build
└── .github/workflows       # CI/CD configuration
```

## 📦 Dependencies

Required LaTeX packages (managed in `styles/formatting.sty`):
- `inputenc` - Input encoding
- `fontenc` - Font encoding
- `geometry` - Page layout
- `hyperref` - PDF metadata and links
- `fontawesome` - Icons
- `titlesec` - Section formatting
- `enumitem` - List customization

## 🔄 CI/CD Pipeline

The automated workflow:
1. Monitors changes in LaTeX source files
2. Triggers builds for relevant updates
3. Deploys to GitHub Pages

## 🎨 Customization Guide

1. **Content Updates**:
   - Modify section files in `sections/`
   - Update personal information in `header.tex`

2. **Style Changes**:
   - Adjust formatting in `styles/formatting.sty`
   - Customize page layout in `resume.tex`

3. **Preview Changes**:
   - Compile locally for immediate feedback
   - Wait for CI/CD pipeline for production build


<div align="center">
Made with ❤️ by Marcus
</div> 