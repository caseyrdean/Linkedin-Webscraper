# LinkedIn Profile Web Scraper

A Python-based web scraper that extracts publicly available LinkedIn profile information and generates a well-formatted Markdown document.

## Features

- Scrapes public LinkedIn profiles
- Extracts comprehensive profile data:
  - Name, headline, and location
  - About/summary section
  - Work experience
  - Education
  - Skills
  - Languages
  - Certifications
- Generates clean, formatted Markdown output
- Built with Python and managed with `uv`

## Prerequisites

- Python 3.11 or higher
- `uv` package manager (recommended) or `pip`

## Installation

### Using uv (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd Linkedin-Webscraper
```

2. Install dependencies:
```bash
uv sync
```

### Using pip

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Using uv
uv run python linkedin_scraper.py https://www.linkedin.com/in/username

# Or using the main entry point
uv run python main.py https://www.linkedin.com/in/username

# Without uv (if using pip)
python linkedin_scraper.py https://www.linkedin.com/in/username
```

### Example

```bash
uv run python linkedin_scraper.py https://www.linkedin.com/in/johndoe
```

This will:
1. Scrape the profile at the provided URL
2. Extract all available public information
3. Generate a Markdown file named `John_Doe_linkedin_profile.md`
4. Display a preview of the scraped content

## Output Format

The scraper generates a Markdown file with the following structure:

```markdown
# [Name]

**[Headline/Title]**

📍 [Location]

🔗 [LinkedIn Profile](url)

---

## About
[About section content]

## Experience
### [Job Title]
**[Company Name]**
*[Date Range]*

[Description]

## Education
### [School Name]
**[Degree]**
*[Date Range]*

## Skills
- [Skill 1]
- [Skill 2]

## Languages
- [Language 1]

## Certifications
### [Certification Name]
*Issued by: [Issuer]*

---
*Profile scraped on: [Timestamp]*
```

## Important Notes

### LinkedIn's Terms of Service

This scraper is designed for educational purposes and works with **publicly available** LinkedIn profile data only. Please be aware:

- Always respect LinkedIn's [Terms of Service](https://www.linkedin.com/legal/user-agreement)
- LinkedIn has anti-scraping measures in place
- For production use, consider using the [official LinkedIn API](https://developer.linkedin.com/)
- Rate limiting may apply - avoid excessive requests
- Some profiles may be private or have limited public visibility

### Limitations

- Only scrapes publicly visible information
- LinkedIn's HTML structure changes frequently, which may affect scraping accuracy
- JavaScript-rendered content may not be fully captured
- Private profiles or profiles requiring authentication will not work
- Anti-bot measures may block requests

### Best Practices

1. Use sparingly and respect rate limits
2. Add delays between multiple requests
3. Consider using the official LinkedIn API for production applications
4. Only scrape profiles you have permission to access
5. Be respectful of users' privacy

## Project Structure

```
Linkedin-Webscraper/
├── linkedin_scraper.py   # Main scraper module
├── main.py              # Entry point wrapper
├── pyproject.toml       # Project configuration and dependencies
├── README.md            # This file
└── .python-version      # Python version specification
```

## Dependencies

- `requests` - HTTP library for making requests
- `beautifulsoup4` - HTML parsing library
- `lxml` - XML/HTML parser

## Troubleshooting

### "Could not extract profile data"

This error can occur due to:
- LinkedIn's anti-scraping measures blocking the request
- Private profile (not publicly visible)
- Invalid URL format
- Network issues

**Solutions:**
- Ensure the profile is public
- Check the URL format (should be `https://www.linkedin.com/in/username`)
- Try again after some time
- Consider using LinkedIn's official API

### Rate Limiting

If you're scraping multiple profiles, add delays between requests:

```python
import time
time.sleep(2)  # Wait 2 seconds between requests
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is for educational purposes. Always respect LinkedIn's Terms of Service and users' privacy.

## Disclaimer

This tool is provided for educational purposes only. The authors are not responsible for any misuse or violations of LinkedIn's Terms of Service. Always ensure you have permission to scrape data and respect website policies and user privacy.
