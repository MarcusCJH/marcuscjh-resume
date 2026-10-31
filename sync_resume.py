#!/usr/bin/env python3
"""
Resume Sync Script
Fetches data.json from portfolio and updates LaTeX sections accordingly.
"""

import argparse
import json
import os
from pathlib import Path

def infer_cv_density(entry: dict) -> str:
    cv = entry.get("cv") or {}
    if cv.get("density") in {"featured", "compact", "oneliner", "omit"}:
        return cv["density"]
    company = (entry.get("company") or "").lower()
    if "accenture" in company:
        return "featured"
    if "whale" in company:
        return "compact"
    return "oneliner"

CV_SKILL_LABELS = {
    "aws": "AWS",
    "alicloud": "Alibaba Cloud",
    "devops": "DevOps",
    "ai": "AI",
}

def cv_skill_label(category: str) -> str:
    key = category.strip().lower()
    if key in CV_SKILL_LABELS:
        return CV_SKILL_LABELS[key]
    return category.replace("_", " & ").title()

def select_cv_certs(timeline: list, mode: str = "all", limit: int | None = None) -> list:
    """Return certifications for the CV.

    mode=\"all\" keeps every cert (compact one-pager). mode=\"featured\" keeps
    only entries with cv.featured, falling back to all if none are flagged.
    """
    certs = [e for e in timeline if e.get("category") == "certification"]
    if mode == "featured":
        featured = [e for e in certs if (e.get("cv") or {}).get("featured")]
        pool = featured if featured else certs
    else:
        pool = certs
    ordered = sorted(pool, key=lambda x: x.get("order", 0), reverse=True)
    if limit is None:
        return ordered
    return ordered[:limit]


def select_featured_certs(timeline: list, limit: int = 6) -> list:
    return select_cv_certs(timeline, mode="featured", limit=limit)

def extract_cv_bullets(entry: dict, max_bullets: int) -> list:
    cv = entry.get("cv") or {}
    if cv.get("bullets"):
        return list(cv["bullets"])[:max_bullets]
    details = (entry.get("modalContent") or {}).get("details") or []
    bullets = []
    for d in details:
        d = (d or "").rstrip()
        if d.startswith("  •"):
            bullets.append(d[3:].strip())
        elif d.startswith("•"):
            bullets.append(d[1:].strip())
    return bullets[:max_bullets]

def format_oneliner(entry: dict) -> str:
    cv = entry.get("cv") or {}
    if cv.get("line"):
        return cv["line"]
    company = entry.get("company", "")
    title = entry.get("title", "")
    start = (entry.get("startDate") or "").split()[-1] if entry.get("startDate") else ""
    end = (entry.get("endDate") or "").split()[-1] if entry.get("endDate") else ""
    years = f"{start}–{end}" if start or end else ""
    return f"{company} · {title} · {years}".strip(" ·")


PDF_BASE_URL = "marcuscjh.com"
PDF_CREATOR = "marcuscjh-resume (https://marcuscjh.com)"
PDF_KEYWORDS_CAP = 12


def build_pdf_metadata(data: dict) -> dict:
    """Build identical PDF Info fields for resume.pdf and cv.pdf."""
    config = data.get("config") or {}
    cv_config = config.get("cv") or {}
    name = config.get("real_name") or config.get("name") or ""
    subject = cv_config.get("summary") or config.get("summary") or ""

    keywords = []
    work_entries = [
        entry for entry in (data.get("timeline") or [])
        if entry.get("category") == "work"
    ]
    for entry in sorted(work_entries, key=lambda item: item.get("order", 0), reverse=True):
        title = (entry.get("title") or "").strip()
        if title and title not in keywords:
            keywords.append(title)
    for category in data.get("skills") or {}:
        label = cv_skill_label(category)
        if label and label not in keywords:
            keywords.append(label)
    keywords = keywords[:PDF_KEYWORDS_CAP]
    if PDF_BASE_URL not in keywords:
        keywords.append(PDF_BASE_URL)

    return {
        "title": f"{name} — Professional CV/Resume",
        "author": name,
        "subject": subject,
        "keywords": ", ".join(keywords),
        "creator": PDF_CREATOR,
    }


class ResumeSyncer:
    def __init__(self):
        self.data = None
        # CV = full dossier; Resume = curated one-pager
        self.cv_sections_dir = Path("src/sections/cv")
        self.resume_sections_dir = Path("src/sections/resume")
        # Back-compat alias used by dense writers
        self.sections_dir = self.cv_sections_dir
        self.pdf_metadata_path = Path("src/sections/pdf-metadata.tex")
        
    def fetch_data(self, url="https://www.marcuscjh.com/data.json"):
        """Fetch data.json from the live portfolio (source of truth)."""
        import urllib.request
        try:
            print(f"Fetching data from {url}...")
            with urllib.request.urlopen(url) as response:
                self.data = json.loads(response.read().decode())
            print("Data fetched successfully")
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def load_local_data(self, filepath=None):
        """Load data.json from local file"""
        candidates = [Path(filepath)] if filepath else [Path("data.json"), Path("data2.json")]
        data_path = next((path for path in candidates if path.exists()), candidates[0])
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"Local data loaded successfully from {data_path}")
            return True
        except Exception as e:
            print(f"Error loading local data: {e}")
            return False
    
    def update_header(self):
        """Update header.tex with name and contact info"""
        config = self.data.get('config', {})
        social = self.data.get('social', [])
        
        # Get required fields from data
        name = config.get('real_name', config.get('name', ''))
        email = config.get('email', '')
        
        if not name or not email:
            print("Missing required fields in config: name or email")
            return
        
        # Build contact links - email, portfolio website, and LinkedIn
        # No \underline: ATS-friendly + matches cvaccent hyperref styling
        contact_links = [f"\\href{{mailto:{email}}}{{{email}}}"]
        
        # Add portfolio website if available
        portfolio_url = config.get('website', '')
        if portfolio_url:
            display_name = portfolio_url.replace('https://', '').replace('http://', '')
            contact_links.append(f"\\href{{{portfolio_url}}}{{{display_name}}}")
        
        # Add LinkedIn if available
        linkedin_entry = next((s for s in social if s.get('platform', '').lower() == 'linkedin'), None)
        if linkedin_entry:
            linkedin_url = linkedin_entry.get('url', '')
            if linkedin_url:
                # Extract display name from LinkedIn URL (e.g., "linkedin.com/in/marcuschanjh")
                display_name = linkedin_url.replace('https://', '').replace('http://', '').replace('www.', '')
                contact_links.append(f"\\href{{{linkedin_url}}}{{{display_name}}}")
        
        content = f"""%----------HEADING----------
\\begin{{center}}
    \\textbf{{\\Huge {name}}} \\\\ \\vspace{{1pt}}
    \\small {' $|$ '.join(contact_links)}
\\end{{center}}"""
        
        self._write_section('header.tex', content)
    
    def update_summary(self):
        """Update summary.tex with professional summary"""
        config = self.data.get('config', {})
        summary = config.get('summary', '')
        
        if not summary:
            print("No summary found in config")
            return
        
        escaped_summary = self._escape_latex(summary)
        content = f"""% Professional Summary Section
% Customize your professional summary as needed

\\begin{{center}}
    \\colorbox{{backgroundgray}}{{
        \\begin{{minipage}}{{0.95\\textwidth}}
            \\centering
            \\vspace{{6pt}}
            \\textcolor{{textgray}}{{\\textit{{{escaped_summary}}}}}
            \\vspace{{6pt}}
        \\end{{minipage}}
    }}
\\end{{center}}
\\vspace{{6pt}}"""
        
        self._write_section('summary.tex', content)
    
    def update_education(self):
        """Update education.tex with education timeline"""
        timeline = self.data.get('timeline', [])
        education_entries = [e for e in timeline if e.get('category') == 'education']
        
        content = "%-----------EDUCATION-----------\n\\section{Education}\n\\resumeSubHeadingListStart\n"
        
        for entry in sorted(education_entries, key=lambda x: x.get('order', 0), reverse=True):
            company = entry.get('company', '')
            title = entry.get('title', '')
            start_date = entry.get('startDate', '')
            end_date = entry.get('endDate', '')
            
            # Format dates
            if start_date and end_date:
                date_str = f"{start_date} -- {end_date}"
            elif start_date:
                date_str = start_date
            else:
                date_str = ""
            
            # Get location from modalContent
            location = entry.get('modalContent', {}).get('location', '')
            escaped_location = self._escape_table_content(location)
            
            content += f"\\resumeSubheading\n{{{company}}}{{{escaped_location}}}\n{{{title}}}{{{date_str}}}\n"
        
        content += "\\resumeSubHeadingListEnd"
        self._write_section('education.tex', content)
    
    def update_certifications(self):
        """Update certifications.tex with certifications timeline"""
        timeline = self.data.get('timeline', [])
        cert_entries = [e for e in timeline if e.get('category') == 'certification']
        
        content = "%-----------CERTIFICATIONS-----------\n\\section{Certifications}\n\\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n"
        
        for entry in sorted(cert_entries, key=lambda x: x.get('order', 0), reverse=True):
            title = entry.get('title', '')
            company = entry.get('company', '')
            start_date = entry.get('startDate', '')
            
            # Extract just the year from the date (e.g., "Jul 2024" -> "2024")
            year = start_date.split()[-1] if start_date else ''
            
            # Escape LaTeX characters
            escaped_title = self._escape_latex(title)
            escaped_company = self._escape_latex(company)
            
            content += f"        \\textbf{{{escaped_title}}} - {escaped_company} \\hfill {year} \\\\\n"
        
        content += "    }}\n\\end{itemize}"
        self._write_section('certifications.tex', content)
    
    def update_projects(self):
        """Update projects.tex with showcase projects"""
        showcase = self.data.get('showcase', [])
        
        content = "%-----------PROJECTS-----------\n\\section{Projects}\n    \\resumeSubHeadingListStart\n"
        
        for project in showcase:
            title = project.get('title', '')
            technologies = project.get('technologies', [])
            modal_content = project.get('modalContent', {})
            description = modal_content.get('description', '')
            
            # Format technologies
            tech_str = ', '.join(technologies) if technologies else ''
            
            # Extract key points from description
            lines = description.split('. ')
            key_points = [line.strip() for line in lines if line.strip()][:3]  # Take first 3 points
            
            content += f"      \\resumeProjectHeading\n"
            content += f"          {{\\textbf{{{title}}} $|$ \\emph{{{tech_str}}}}}{{}}\n"
            content += f"          \\resumeItemListStart\n"
            
            for point in key_points:
                if point:
                    escaped_point = self._escape_latex(point)
                    content += f"            \\resumeItem{{{escaped_point}}}\n"
            
            content += f"          \\resumeItemListEnd\n"
        
        content += "    \\resumeSubHeadingListEnd"
        self._write_section('projects.tex', content)
    
    def update_experience(self):
        """Update experience.tex with work timeline"""
        timeline = self.data.get('timeline', [])
        work_entries = [e for e in timeline if e.get('category') == 'work']
        
        content = "%-----------EXPERIENCE-----------\n\\section{Experience}\n\\resumeSubHeadingListStart\n"
        
        for i, entry in enumerate(sorted(work_entries, key=lambda x: x.get('order', 0), reverse=True)):
            title = entry.get('title', '')
            company = entry.get('company', '')
            start_date = entry.get('startDate', '')
            end_date = entry.get('endDate', '')
            location = entry.get('modalContent', {}).get('location', '')
            details = entry.get('modalContent', {}).get('details', [])
            
            # Format dates - convert to YYYY format for consistency
            if start_date and end_date:
                start_year = start_date.split()[-1] if start_date else ''
                end_year = end_date.split()[-1] if end_date else ''
                if end_year == 'Present':
                    date_str = f"{start_year} -- Present"
                else:
                    date_str = f"{start_year} -- {end_year}"
            elif start_date:
                year = start_date.split()[-1] if start_date else ''
                date_str = year
            else:
                date_str = ""
            
            # Add needspace before each job (except first)
            if i > 0:
                if company == "Accenture":
                    content += "\n\\needspace{4cm}\n"
                else:
                    content += "\n\\needspace{3cm}\n"
            
            escaped_location = self._escape_table_content(location)
            content += f"\\resumeSubheading\n{{{title}}}{{{date_str}}}\n{{{company}}}{{{escaped_location}}}\n"
            
            if details:
                content += "\\resumeItemListStart\n"
                
                # Process details to match the exact format from experience copy
                in_itemize = False
                
                for detail in details:
                    detail = detail.strip()
                    if not detail:
                        continue
                    
                    # Check if this is a role header (contains dates in parentheses)
                    if "(" in detail and ")" in detail and ("Present" in detail or "20" in detail):
                        if in_itemize:
                            content += "\\end{itemize}\n"
                            in_itemize = False
                        
                        # Format role with " - " separator like in the reference
                        if " - " in detail:
                            # Split only on the first " - " to preserve the rest
                            parts = detail.split(" - ", 1)
                            role_title = self._escape_latex(parts[0].strip())
                            role_dept = self._escape_latex(parts[1].strip())
                            formatted_role = f"\\textbf{{{role_title}}} - {role_dept}"
                        else:
                            escaped_detail = self._escape_latex(detail)
                            formatted_role = f"\\textbf{{{escaped_detail}}}"
                        
                        content += f"\\resumeItem{{{formatted_role}}}\n"
                        content += "\\begin{itemize}\n"
                        in_itemize = True
                    elif detail.startswith("  •"):
                        # This is a nested bullet point (indented)
                        bullet_text = self._escape_latex(detail[3:].strip())
                        content += f"    \\resumeItem{{{bullet_text}}}\n"
                    elif detail.startswith("•"):
                        # This is a bullet point
                        bullet_text = self._escape_latex(detail[1:].strip())
                        content += f"    \\resumeItem{{{bullet_text}}}\n"
                    else:
                        # Regular item - check if it's a sub-section header
                        if detail.endswith(" - Singapore") or detail.endswith(" - Yokohama, Japan"):
                            if in_itemize:
                                content += "\\end{itemize}\n"
                                in_itemize = False
                            escaped_detail = self._escape_latex(detail)
                            content += f"\\resumeItem{{\\textbf{{{escaped_detail}}}}}\n"
                            content += "\\begin{itemize}\n"
                            in_itemize = True
                        else:
                            escaped_detail = self._escape_latex(detail)
                            content += f"\\resumeItem{{{escaped_detail}}}\n"
                
                if in_itemize:
                    content += "\\end{itemize}\n"
                
                content += "\\resumeItemListEnd\n"
        
        content += "\n\\resumeSubHeadingListEnd"
        self._write_section('experience.tex', content)
    
    def update_skills(self):
        """Update skills.tex with skills from data.json"""
        skills = self.data.get('skills', {})
        
        if not skills:
            print("No skills section found in data.json")
            return
        
        # Build skills content dynamically
        content = "%-----------PROGRAMMING SKILLS-----------\n\\section{Technical Skills}\n \\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n"
        
        # Add each skill category
        for category, technologies in skills.items():
            if technologies:  # Only add if technologies exist
                # Replace underscores with &, then title case, then escape LaTeX special characters
                category_name = category.replace('_', ' & ').title()
                category_name = self._escape_latex(category_name)
                # Escape each technology for LaTeX before joining
                escaped_techs = [self._escape_latex(tech) for tech in sorted(technologies)]
                tech_list = ', '.join(escaped_techs)
                content += f"     \\textbf{{{category_name}}}{{: {tech_list}}} \\\\\n"
        
        content += "    }}\n \\end{itemize}"
        
        self._write_section('skills.tex', content)

    def update_cv_header(self):
        """Write the compact CV header."""
        config = self.data.get("config", {})
        cv_config = config.get("cv") or {}
        social = self.data.get("social", [])
        name = self._escape_latex(config.get("real_name") or config.get("name", ""))
        title = self._escape_latex(cv_config.get("title") or config.get("title", ""))
        email = config.get("email", "")
        website = config.get("website", "")
        linkedin = next(
            (
                item.get("url", "")
                for item in social
                if item.get("platform", "").lower() == "linkedin"
            ),
            "",
        )

        lines = [
            "% Generated by sync_resume.py",
            f"\\cvHeader{{{name}}}{{{title}}}",
            "\\cvPhoto{assets/photo.jpg}",
        ]
        if email:
            escaped_email = self._escape_latex(email)
            lines.append(
                f"\\cvContact{{\\cvIconEmail}}{{\\href{{mailto:{email}}}{{{escaped_email}}}}}"
            )
        if website:
            display = website.replace("https://", "").replace("http://", "").rstrip("/")
            lines.append(
                f"\\cvContact{{\\cvIconWebsite}}{{\\href{{{website}}}{{{self._escape_latex(display)}}}}}"
            )
        if linkedin:
            display = linkedin.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
            lines.append(
                f"\\cvContact{{\\cvIconLinkedIn}}{{\\href{{{linkedin}}}{{{self._escape_latex(display)}}}}}"
            )
        self._write_cv_section("header.tex", "\n".join(lines))

    def update_cv_summary(self):
        """Write the CV-specific summary, falling back to a shortened resume summary."""
        config = self.data.get("config", {})
        cv_summary = (config.get("cv") or {}).get("summary")
        summary = cv_summary or config.get("summary", "")
        if not cv_summary and len(summary) > 320:
            summary = summary[:317].rsplit(" ", 1)[0] + "..."
        content = (
            "% Generated by sync_resume.py\n"
            "\\cvSection{Summary}\n"
            f"\\cvSummary{{{self._escape_latex(summary)}}}"
        )
        self._write_cv_section("summary.tex", content)

    def update_cv_experience(self):
        """Write featured, compact, and earlier experience entries."""
        entries = sorted(
            (item for item in self.data.get("timeline", []) if item.get("category") == "work"),
            key=lambda item: item.get("order", 0),
            reverse=True,
        )
        lines = ["% Generated by sync_resume.py", "\\cvSection{Experience}"]
        earlier = []

        for entry in entries:
            density = infer_cv_density(entry)
            if density == "omit":
                continue
            if density == "oneliner":
                earlier.append(format_oneliner(entry))
                continue

            company = self._escape_latex(entry.get("company", ""))
            title = self._escape_latex(entry.get("title", ""))
            dates = self._format_years(entry)
            location = self._escape_latex((entry.get("modalContent") or {}).get("location", ""))
            lines.append(f"\\cvExperience{{{company}}}{{{title}}}{{{dates}}}{{{location}}}")

            if density == "featured":
                roles = (entry.get("cv") or {}).get("roles") or []
                if roles:
                    for role in roles:
                        if role.get("line"):
                            lines.append(f"\\cvRoleLine{{{self._escape_latex(role['line'])}}}")
                            continue
                        role_title = self._escape_latex(role.get("title", ""))
                        years = self._escape_latex(role.get("years", ""))
                        lines.append(f"\\cvRole{{{role_title}}}{{{years}}}")
                        for bullet in role.get("bullets") or []:
                            lines.append(f"\\cvBullet{{{self._escape_latex(bullet)}}}")
                else:
                    for bullet in extract_cv_bullets(entry, max_bullets=5):
                        lines.append(f"\\cvBullet{{{self._escape_latex(bullet)}}}")
            else:
                for bullet in extract_cv_bullets(entry, max_bullets=2):
                    lines.append(f"\\cvBullet{{{self._escape_latex(bullet)}}}")

        if earlier:
            earlier_text = " \\\\ ".join(self._escape_latex(item) for item in earlier)
            lines.append(f"\\cvEarlier{{{earlier_text}}}")
        self._write_cv_section("experience.tex", "\n".join(lines))

    def update_cv_skills(self):
        """Write skill groups as CV pills."""
        skills = self.data.get("skills", {})
        cv_config = (self.data.get("config", {}).get("cv") or {})
        requested_order = cv_config.get("skillOrder") or list(skills)
        categories = list(requested_order) + [
            category for category in skills if category not in requested_order
        ]
        lines = ["% Generated by sync_resume.py", "\\cvSection{Skills}"]
        for category in categories:
            technologies = skills.get(category) or []
            if not technologies:
                continue
            label = self._escape_latex(cv_skill_label(category))
            pills = " ".join(
                f"\\cvPill{{{self._escape_latex(technology)}}}"
                for technology in technologies
            )
            lines.append(f"\\cvSkillGroup{{{label}}}{{{pills}}}")
        self._write_cv_section("skills.tex", "\n".join(lines))

    def update_cv_certifications(self):
        """Write every certification as a description | year table."""
        lines = [
            "% Generated by sync_resume.py",
            "\\cvSection{Certifications}",
            "\\begin{cvCertTable}",
        ]
        for entry in select_cv_certs(self.data.get("timeline", []), mode="all"):
            title = self._escape_latex(entry.get("title", ""))
            issuer = self._escape_latex(entry.get("company", ""))
            year = self._escape_latex(
                (entry.get("startDate") or "").split()[-1]
                if entry.get("startDate")
                else ""
            )
            lines.append(f"\\cvCertification{{{title}}}{{{issuer}}}{{{year}}}")
        lines.append("\\end{cvCertTable}")
        self._write_cv_section("certifications.tex", "\n".join(lines))

    def update_cv_education(self):
        """Write compact education entries."""
        entries = sorted(
            (
                item
                for item in self.data.get("timeline", [])
                if item.get("category") == "education"
            ),
            key=lambda item: item.get("order", 0),
            reverse=True,
        )
        lines = ["% Generated by sync_resume.py", "\\cvSection{Education}"]
        for entry in entries:
            school = self._escape_latex(entry.get("company", ""))
            title = self._escape_latex(entry.get("title", ""))
            years = self._format_years(entry)
            location = self._escape_latex((entry.get("modalContent") or {}).get("location", ""))
            lines.append(f"\\cvEducation{{{school}}}{{{title}}}{{{years}}}{{{location}}}")
        self._write_cv_section("education.tex", "\n".join(lines))

    def sync_cv(self):
        """Generate curated Resume sections (one-pager)."""
        self.resume_sections_dir.mkdir(parents=True, exist_ok=True)
        self.update_cv_header()
        self.update_cv_summary()
        self.update_cv_experience()
        self.update_cv_skills()
        self.update_cv_certifications()
        self.update_cv_education()

    def update_pdf_metadata(self):
        """Write shared PDF Info properties for resume.pdf and cv.pdf."""
        meta = build_pdf_metadata(self.data or {})
        e = self._escape_latex
        content = "\n".join([
            "% Generated by sync_resume.py — identical Info for resume.pdf and cv.pdf",
            r"\hypersetup{%",
            f"  pdftitle={{{e(meta['title'])}}},",
            f"  pdfauthor={{{e(meta['author'])}}},",
            f"  pdfsubject={{{e(meta['subject'])}}},",
            f"  pdfkeywords={{{e(meta['keywords'])}}},",
            f"  pdfcreator={{{e(meta['creator'])}}}",
            "}",
            "",
        ])
        self.pdf_metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self.pdf_metadata_path.write_text(content, encoding="utf-8")
        print(f"Updated {self.pdf_metadata_path}")

    def _format_years(self, entry):
        """Return a compact year range for a timeline entry."""
        start = (entry.get("startDate") or "").split()[-1] if entry.get("startDate") else ""
        end = (entry.get("endDate") or "").split()[-1] if entry.get("endDate") else ""
        if start and end:
            if start == end:
                return self._escape_latex(start)
            return self._escape_latex(f"{start}–{end}")
        return self._escape_latex(start or end)
    
    def _validate_data(self):
        """Validate that required data structure exists"""
        if not self.data:
            print("No data loaded")
            return False
        
        required_sections = ['config', 'timeline', 'showcase', 'skills']
        missing = [section for section in required_sections if section not in self.data]
        
        if missing:
            print(f"Missing required sections: {missing}")
            return False
        
        return True
    
    def _escape_latex(self, text):
        """Escape special LaTeX characters"""
        # Replace % with \% for LaTeX
        text = text.replace('%', '\\%')
        # Replace & with \& for LaTeX (but be careful with table contexts)
        text = text.replace('&', '\\&')
        # Replace $ with \$ for LaTeX
        text = text.replace('$', '\\$')
        # Replace # with \# for LaTeX
        text = text.replace('#', '\\#')
        # Replace ^ with \^{} for LaTeX
        text = text.replace('^', '\\^{}')
        # Replace _ with \_ for LaTeX
        text = text.replace('_', '\\_')
        # Replace { with \{ for LaTeX
        text = text.replace('{', '\\{')
        # Replace } with \} for LaTeX
        text = text.replace('}', '\\}')
        return text
    
    def _escape_table_content(self, text):
        """Escape LaTeX characters for table content (like resumeSubheading)"""
        # For table content, we need to be more careful with &
        # Replace & with \& for LaTeX table contexts
        text = text.replace('&', '\\&')
        # Replace % with \% for LaTeX
        text = text.replace('%', '\\%')
        # Replace $ with \$ for LaTeX
        text = text.replace('$', '\\$')
        # Replace # with \# for LaTeX
        text = text.replace('#', '\\#')
        # Replace ^ with \^{} for LaTeX
        text = text.replace('^', '\\^{}')
        # Replace _ with \_ for LaTeX
        text = text.replace('_', '\\_')
        # Replace { with \{ for LaTeX
        text = text.replace('{', '\\{')
        # Replace } with \} for LaTeX
        text = text.replace('}', '\\}')
        return text
    
    def _write_section(self, filename, content):
        """Write a full CV section."""
        self.cv_sections_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.cv_sections_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated cv/{filename}")
        except Exception as e:
            print(f"Error writing {filename}: {e}")

    def _write_cv_section(self, filename, content):
        """Write a curated Resume section (historically named update_cv_*)."""
        self.resume_sections_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.resume_sections_dir / filename
        filepath.write_text(content, encoding="utf-8")
        print(f"Updated resume/{filename}")
    
    def sync_all(self, use_local=False, target="all"):
        """Sync CV (full) and/or Resume (curated) sections."""
        print(f"Starting {target} sync...")
        
        # Load data
        if use_local:
            if not self.load_local_data():
                return False
        else:
            if not self.fetch_data():
                return False
        
        # Validate data structure
        if not self._validate_data():
            print("Data validation failed")
            return False

        # Shared PDF Info for both documents (any target)
        self.update_pdf_metadata()
        
        # CV = full dossier
        if target in {"cv", "all"}:
            self.update_header()
            self.update_summary()
            self.update_experience()
            self.update_education()
            self.update_certifications()
            self.update_projects()
            self.update_skills()

        # Resume = curated one-pager
        if target in {"resume", "all"}:
            self.sync_cv()
        
        print(f"{target.title()} sync completed!")
        return True

def resolve_use_local(source="auto", local_exists=None):
    """Decide whether to load a local data.json.

    auto (default): use local data.json/data2.json if present (testing), else remote
    remote: always fetch https://www.marcuscjh.com/data.json
    local: always local (fails if missing)
    """
    if source == "local":
        return True
    if source == "remote":
        return False
    if local_exists is None:
        local_exists = os.path.exists("data.json") or os.path.exists("data2.json")
    return bool(local_exists)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate LaTeX sections: CV (full dossier) and/or Resume (curated one-pager)"
    )
    parser.add_argument(
        "--target",
        choices=("resume", "cv", "all"),
        default="all",
        help="cv=full dossier, resume=curated one-pager, all=both (default: all)",
    )
    parser.add_argument(
        "--source",
        choices=("local", "remote", "auto"),
        default="auto",
        help="auto (default): local data.json if present for testing, else "
             "https://www.marcuscjh.com/data.json; remote/local force one source",
    )
    args = parser.parse_args(argv)
    syncer = ResumeSyncer()

    use_local = resolve_use_local(args.source)
    print(f"Data source: {'local' if use_local else 'remote'} (--source {args.source})")
    ok = syncer.sync_all(use_local=use_local, target=args.target)
    if not ok:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
