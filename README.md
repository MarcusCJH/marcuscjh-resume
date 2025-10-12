# Marcus's LaTeX Resume 📄

A professionally crafted, modular LaTeX resume with automated builds and live preview.

[![View Resume](https://img.shields.io/badge/View%20Resume-PDF-blue)](https://marcuscjh.github.io/marcuscjh-resume/)
[![Build Status](https://github.com/marcuscjh/marcuscjh-resume/workflows/Build%20and%20Deploy%20LaTeX%20Resume/badge.svg)](https://github.com/marcuscjh/marcuscjh-resume/actions)
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
- XeLaTeX engine (recommended for best font support)

### Quick Start

1. Clone the repository
```bash
git clone https://github.com/marcuscjh/marcuscjh-resume.git
```

2. Compile the resume
```bash
# Using XeLaTeX (recommended)
xelatex -output-directory=out -aux-directory=auxil src/resume.tex

# Or using the GitHub Actions workflow (automatic)
# Just push changes to master branch
```

## 📁 Project Structure

```
.
├── src/
│   ├── resume.tex          # Main LaTeX entry point
│   └── sections/           # Modular content sections
│       ├── header.tex          # Contact information
│       ├── summary.tex         # Professional summary
│       ├── education.tex       # Academic background
│       ├── experience.tex      # Professional experience
│       ├── skills.tex          # Technical skills
│       ├── projects.tex        # Project highlights
│       └── certifications.tex  # Certifications & awards
│   └── styles/             # Design and formatting
│       └── formatting.sty  # LaTeX style definitions
├── docs/                   # Public assets
│   ├── index.html          # Landing page
│   └── resume.pdf          # Latest build
└── .github/workflows       # CI/CD configuration
```

## 🎨 Template Features

### Page Break Controls
- **`\newpagesection{Title}`** - Start section on new page
- **`\pagebreakhere`** - Force page break
- **`\smartpagebreak`** - Fill current page then break
- **`\moderndivider`** - Visual section separator

### Professional Elements
- **Color-coded sections** with professional blue theme
- **Achievement-focused bullets** with arrow indicators
- **Professional summary box** for key highlights
- **Clean contact layout** with social links
- **Skill categorization** for easy scanning

## 📝 Customization Guide

### Content Updates
1. **Personal Information**: Update `sections/header.tex`
2. **Professional Summary**: Modify the summary in `resume.tex`
3. **Experience**: Add your roles in `sections/experience.tex`
4. **Projects**: Showcase your work in `sections/projects.tex`
5. **Skills**: List your technologies in `sections/skills.tex`
6. **Education**: Update academic info in `sections/education.tex`

### Layout Control
```latex
% Example: Move Technical Skills to new page
\newpagesection{Technical Skills}

% Example: Add page break before Education
\pagebreakhere
\input{sections/education}
```

### Advanced LaTeX Commands
The template includes powerful custom commands:

**Content Commands:**
- `\resumeSubheading{Title}{Date}{Company}{Location}` - Professional experience entries
- `\resumeProjectHeading{Project}{Date}` - Project entries
- `\achievementItem{Achievement}` - Achievement with arrow indicator
- `\achievementWithMetric{Achievement}{Metric}` - Achievement with metrics
- `\certificationItem{Certification}{Date}{Issuer}` - Certification entries
- `\educationEntry{Institution}{Date}{Degree}{Location}{Details}` - Education entries

**Formatting Commands:**
- `\skillCategory{Category}{Skills}` - Categorized skill listings
- `\professionalsummary{Text}` - Professional summary box
- `\moderndivider` - Visual section separator
- `\contactinfo{Email}{Phone}{GitHub}{LinkedIn}{Website}` - Contact information


## 🔧 Compilation Tips

- Use **XeLaTeX** for best results with FontAwesome icons
- Output directory structure keeps files organized
- Compile twice if references seem off

## 📦 Dependencies

Core LaTeX packages (auto-managed):
- `geometry` - Page layout
- `xcolor` - Professional color scheme
- `fontawesome` - Contact icons
- `hyperref` - Clickable links
- `enumitem` - List formatting

---

<div align="center">
Made with ❤️ by Marcus
</div> 