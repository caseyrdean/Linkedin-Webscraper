"""
LinkedIn Profile Scraper

This script scrapes publicly available LinkedIn profile information and generates
a markdown document with the profile data.

Note: This scraper works with publicly visible LinkedIn profiles. LinkedIn has
anti-scraping measures, so consider:
- Using proper authentication for better access
- Respecting rate limits
- Following LinkedIn's Terms of Service
- Using official LinkedIn API for production use
"""

import requests
from bs4 import BeautifulSoup
import re
import sys
from typing import Dict, List, Optional
from datetime import datetime


class LinkedInScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_profile(self, url: str) -> Dict:
        """
        Scrape a LinkedIn profile and return structured data.

        Args:
            url: LinkedIn profile URL

        Returns:
            Dictionary containing profile information
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile: {e}", file=sys.stderr)
            return {}

        soup = BeautifulSoup(response.content, 'lxml')

        profile_data = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'name': self._extract_name(soup),
            'headline': self._extract_headline(soup),
            'location': self._extract_location(soup),
            'about': self._extract_about(soup),
            'experience': self._extract_experience(soup),
            'education': self._extract_education(soup),
            'skills': self._extract_skills(soup),
            'languages': self._extract_languages(soup),
            'certifications': self._extract_certifications(soup),
        }

        return profile_data

    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile name"""
        # Try different selectors for name
        selectors = [
            ('h1', {'class': re.compile(r'.*name.*', re.I)}),
            ('h1', {'class': re.compile(r'.*top-card.*', re.I)}),
            ('h1', {}),
        ]

        for tag, attrs in selectors:
            element = soup.find(tag, attrs)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 0:
                    return text

        # Try meta tags
        meta_name = soup.find('meta', property='og:title')
        if meta_name:
            return meta_name.get('content', '').split('|')[0].strip()

        return None

    def _extract_headline(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile headline/title"""
        selectors = [
            ('div', {'class': re.compile(r'.*headline.*', re.I)}),
            ('h2', {'class': re.compile(r'.*top-card.*', re.I)}),
        ]

        for tag, attrs in selectors:
            element = soup.find(tag, attrs)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 0:
                    return text

        # Try meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            content = meta_desc.get('content', '')
            if ' - ' in content:
                return content.split(' - ')[0].strip()

        return None

    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract location"""
        selectors = [
            ('span', {'class': re.compile(r'.*location.*', re.I)}),
            ('div', {'class': re.compile(r'.*location.*', re.I)}),
        ]

        for tag, attrs in selectors:
            element = soup.find(tag, attrs)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 0:
                    return text

        return None

    def _extract_about(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract about/summary section"""
        selectors = [
            ('section', {'class': re.compile(r'.*about.*', re.I)}),
            ('div', {'class': re.compile(r'.*summary.*', re.I)}),
        ]

        for tag, attrs in selectors:
            element = soup.find(tag, attrs)
            if element:
                # Remove the section header
                header = element.find(['h2', 'h3'])
                if header:
                    header.decompose()

                text = element.get_text(strip=True, separator=' ')
                if text and len(text) > 0:
                    return text

        return None

    def _extract_experience(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract work experience"""
        experiences = []

        # Look for experience section
        exp_section = soup.find('section', {'id': re.compile(r'.*experience.*', re.I)})
        if not exp_section:
            exp_section = soup.find('section', {'class': re.compile(r'.*experience.*', re.I)})

        if exp_section:
            # Find all experience items
            items = exp_section.find_all(['li', 'div'], recursive=True)

            for item in items:
                exp = {}

                # Try to extract title
                title = item.find(['h3', 'h4'], {'class': re.compile(r'.*title.*', re.I)})
                if title:
                    exp['title'] = title.get_text(strip=True)

                # Try to extract company
                company = item.find(['span', 'p'], {'class': re.compile(r'.*company.*', re.I)})
                if company:
                    exp['company'] = company.get_text(strip=True)

                # Try to extract date range
                date_range = item.find(['span', 'p'], {'class': re.compile(r'.*date.*', re.I)})
                if date_range:
                    exp['date_range'] = date_range.get_text(strip=True)

                # Try to extract description
                description = item.find(['div', 'p'], {'class': re.compile(r'.*description.*', re.I)})
                if description:
                    exp['description'] = description.get_text(strip=True)

                if exp:
                    experiences.append(exp)

        return experiences

    def _extract_education(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract education"""
        education = []

        # Look for education section
        edu_section = soup.find('section', {'id': re.compile(r'.*education.*', re.I)})
        if not edu_section:
            edu_section = soup.find('section', {'class': re.compile(r'.*education.*', re.I)})

        if edu_section:
            items = edu_section.find_all(['li', 'div'], recursive=True)

            for item in items:
                edu = {}

                # School name
                school = item.find(['h3', 'h4'], {'class': re.compile(r'.*school.*', re.I)})
                if school:
                    edu['school'] = school.get_text(strip=True)

                # Degree
                degree = item.find(['span', 'p'], {'class': re.compile(r'.*degree.*', re.I)})
                if degree:
                    edu['degree'] = degree.get_text(strip=True)

                # Date range
                date_range = item.find(['span', 'p'], {'class': re.compile(r'.*date.*', re.I)})
                if date_range:
                    edu['date_range'] = date_range.get_text(strip=True)

                if edu:
                    education.append(edu)

        return education

    def _extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills"""
        skills = []

        skills_section = soup.find('section', {'class': re.compile(r'.*skills.*', re.I)})
        if skills_section:
            skill_items = skills_section.find_all(['span', 'p'], {'class': re.compile(r'.*skill.*', re.I)})
            skills = [item.get_text(strip=True) for item in skill_items if item.get_text(strip=True)]

        return skills

    def _extract_languages(self, soup: BeautifulSoup) -> List[str]:
        """Extract languages"""
        languages = []

        lang_section = soup.find('section', {'class': re.compile(r'.*language.*', re.I)})
        if lang_section:
            lang_items = lang_section.find_all(['span', 'p'])
            languages = [item.get_text(strip=True) for item in lang_items if item.get_text(strip=True)]

        return languages

    def _extract_certifications(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract certifications"""
        certifications = []

        cert_section = soup.find('section', {'class': re.compile(r'.*certification.*', re.I)})
        if cert_section:
            items = cert_section.find_all(['li', 'div'])

            for item in items:
                cert = {}

                # Certification name
                name = item.find(['h3', 'h4'])
                if name:
                    cert['name'] = name.get_text(strip=True)

                # Issuing organization
                org = item.find(['span', 'p'], {'class': re.compile(r'.*issuer.*', re.I)})
                if org:
                    cert['issuer'] = org.get_text(strip=True)

                if cert:
                    certifications.append(cert)

        return certifications


def generate_markdown(profile_data: Dict) -> str:
    """
    Generate a markdown document from profile data.

    Args:
        profile_data: Dictionary containing profile information

    Returns:
        Markdown formatted string
    """
    md = []

    # Header
    if profile_data.get('name'):
        md.append(f"# {profile_data['name']}")
        md.append("")

    # Headline
    if profile_data.get('headline'):
        md.append(f"**{profile_data['headline']}**")
        md.append("")

    # Location
    if profile_data.get('location'):
        md.append(f"📍 {profile_data['location']}")
        md.append("")

    # Profile URL
    if profile_data.get('url'):
        md.append(f"🔗 [LinkedIn Profile]({profile_data['url']})")
        md.append("")

    md.append("---")
    md.append("")

    # About Section
    if profile_data.get('about'):
        md.append("## About")
        md.append("")
        md.append(profile_data['about'])
        md.append("")

    # Experience Section
    if profile_data.get('experience'):
        md.append("## Experience")
        md.append("")
        for exp in profile_data['experience']:
            if exp.get('title'):
                md.append(f"### {exp['title']}")
            if exp.get('company'):
                md.append(f"**{exp['company']}**")
            if exp.get('date_range'):
                md.append(f"*{exp['date_range']}*")
            if exp.get('description'):
                md.append("")
                md.append(exp['description'])
            md.append("")

    # Education Section
    if profile_data.get('education'):
        md.append("## Education")
        md.append("")
        for edu in profile_data['education']:
            if edu.get('school'):
                md.append(f"### {edu['school']}")
            if edu.get('degree'):
                md.append(f"**{edu['degree']}**")
            if edu.get('date_range'):
                md.append(f"*{edu['date_range']}*")
            md.append("")

    # Skills Section
    if profile_data.get('skills'):
        md.append("## Skills")
        md.append("")
        for skill in profile_data['skills']:
            md.append(f"- {skill}")
        md.append("")

    # Languages Section
    if profile_data.get('languages'):
        md.append("## Languages")
        md.append("")
        for lang in profile_data['languages']:
            md.append(f"- {lang}")
        md.append("")

    # Certifications Section
    if profile_data.get('certifications'):
        md.append("## Certifications")
        md.append("")
        for cert in profile_data['certifications']:
            if cert.get('name'):
                md.append(f"### {cert['name']}")
            if cert.get('issuer'):
                md.append(f"*Issued by: {cert['issuer']}*")
            md.append("")

    # Footer
    md.append("---")
    md.append("")
    md.append(f"*Profile scraped on: {profile_data.get('scraped_at', 'Unknown')}*")

    return "\n".join(md)


def main():
    """Main function to run the scraper"""
    if len(sys.argv) < 2:
        print("Usage: python linkedin_scraper.py <linkedin_profile_url>")
        print("\nExample:")
        print("  python linkedin_scraper.py https://www.linkedin.com/in/username")
        sys.exit(1)

    profile_url = sys.argv[1]

    # Validate URL
    if not profile_url.startswith('https://www.linkedin.com/in/'):
        print("Error: Please provide a valid LinkedIn profile URL")
        print("URL should start with: https://www.linkedin.com/in/")
        sys.exit(1)

    print(f"Scraping LinkedIn profile: {profile_url}")
    print("Please wait...\n")

    # Create scraper and scrape profile
    scraper = LinkedInScraper()
    profile_data = scraper.scrape_profile(profile_url)

    if not profile_data or not profile_data.get('name'):
        print("\nWarning: Could not extract profile data. This could be due to:")
        print("- LinkedIn's anti-scraping measures")
        print("- Private profile (not publicly visible)")
        print("- Invalid URL")
        print("- Network issues")
        print("\nNote: For best results, consider using LinkedIn's official API")
        sys.exit(1)

    # Generate markdown
    markdown_content = generate_markdown(profile_data)

    # Create output filename
    name = profile_data.get('name', 'profile').replace(' ', '_')
    output_file = f"{name}_linkedin_profile.md"

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✓ Profile scraped successfully!")
    print(f"✓ Markdown file created: {output_file}")
    print("\n" + "="*50)
    print("PREVIEW:")
    print("="*50 + "\n")
    print(markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content)


if __name__ == "__main__":
    main()
