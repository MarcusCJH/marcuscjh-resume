# Marcus's LaTeX Resume

This repository contains my professional resume written in LaTeX, organized in a modular structure for easy maintenance.

## Prerequisites

To compile this resume, you need:
- A LaTeX distribution (e.g., TeX Live, MiKTeX)
- A LaTeX editor (optional, but recommended)

## Project Structure

```
.
├── resume.tex          # Main LaTeX file
├── sections/          # Individual resume sections
│   ├── header.tex     # Contact information
│   ├── education.tex  # Education section
│   ├── experience.tex # Work experience
│   ├── skills.tex     # Skills and technologies
│   └── projects.tex   # Project showcase
├── styles/           # Styling and formatting
│   └── formatting.sty # Custom formatting and packages
├── .gitignore        # Git ignore file
└── README.md         # This file
```

## Required LaTeX Packages

The following LaTeX packages are used (all managed in `styles/formatting.sty`):
- inputenc
- fontenc
- geometry
- hyperref
- fontawesome
- titlesec
- enumitem

## Compiling the Resume

To compile the resume, run:
```bash
pdflatex resume.tex
```

This will generate `resume.pdf` in the same directory.

## Customization

To customize the resume:
1. Edit individual section files in the `sections/` directory
2. Modify styling in `styles/formatting.sty`
3. Compile to see the changes

## License

MIT License 