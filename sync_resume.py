#!/usr/bin/env python3
"""
Resume Sync Script
Fetches data.json from portfolio and updates LaTeX sections accordingly.
"""

import json
import os
from pathlib import Path

class ResumeSyncer:
    def __init__(self):
        self.data = None
        self.sections_dir = Path("src/sections")
        
    def fetch_data(self, url="https://marcuscjh.github.io/data.json"):
        """Fetch data.json from portfolio"""
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
    
    def load_local_data(self, filepath="data2.json"):
        """Load data.json from local file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print("Local data loaded successfully")
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
        
        # Build contact links - only email and portfolio website
        contact_links = [f"\\href{{mailto:{email}}}{{\\underline{{{email}}}}}"]
        
        # Add portfolio website if available
        portfolio_url = config.get('website', '')
        if portfolio_url:
            display_name = portfolio_url.replace('https://', '').replace('http://', '')
            contact_links.append(f"\\href{{{portfolio_url}}}{{\\underline{{{display_name}}}}}")
        
        content = f"""%----------HEADING----------
\\begin{{center}}
    \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}
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
        
        content = f"""% Professional Summary Section
% Customize your professional summary as needed

\\begin{{center}}
    \\colorbox{{backgroundgray}}{{
        \\begin{{minipage}}{{0.95\\textwidth}}
            \\centering
            \\vspace{{6pt}}
            \\textcolor{{textgray}}{{\\textit{{{summary}}}}}
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
            
            content += f"\\resumeSubheading\n{{{company}}}{{{location}}}\n{{{title}}}{{{date_str}}}\n"
        
        content += "\\resumeSubHeadingListEnd"
        self._write_section('education.tex', content)
    
    def update_certifications(self):
        """Update certifications.tex with certifications timeline"""
        timeline = self.data.get('timeline', [])
        cert_entries = [e for e in timeline if e.get('category') == 'certification']
        
        content = "%-----------CERTIFICATIONS-----------\n\\section{Certifications}\n  \\resumeSubHeadingListStart\n"
        
        for entry in sorted(cert_entries, key=lambda x: x.get('order', 0), reverse=True):
            title = entry.get('title', '')
            company = entry.get('company', '')
            start_date = entry.get('startDate', '')
            
            # Extract just the year from the date (e.g., "Jul 2024" -> "2024")
            year = start_date.split()[-1] if start_date else ''
            
            content += f"    \\resumeSubheading\n      {{{title}}}{{{year}}}\n      {{{company}}}{{}}\n"
        
        content += "  \\resumeSubHeadingListEnd"
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
                    content += f"            \\resumeItem{{{point}}}\n"
            
            content += f"          \\resumeItemListEnd\n"
        
        content += "    \\resumeSubHeadingListEnd"
        self._write_section('projects.tex', content)
    
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
                category_name = category.replace('_', ' \\& ').title()
                tech_list = ', '.join(sorted(technologies))
                content += f"     \\textbf{{{category_name}}}{{: {tech_list}}} \\\\\n"
        
        content += "    }}}\n \\end{itemize}"
        
        self._write_section('skills.tex', content)
    
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
    
    def _write_section(self, filename, content):
        """Write content to a section file"""
        filepath = self.sections_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
        except Exception as e:
            print(f"Error writing {filename}: {e}")
    
    def sync_all(self, use_local=False):
        """Sync all sections"""
        print("Starting resume sync...")
        
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
        
        # Update all sections
        self.update_header()
        self.update_summary()
        self.update_education()
        self.update_certifications()
        self.update_projects()
        self.update_skills()
        
        print("Resume sync completed!")
        return True

def main():
    syncer = ResumeSyncer()
    
    # Check if data2.json exists locally
    if os.path.exists('data2.json'):
        print("Found local data2.json, using local data...")
        syncer.sync_all(use_local=True)
    else:
        print("No local data2.json found, fetching from portfolio...")
        syncer.sync_all(use_local=False)

if __name__ == "__main__":
    main()
