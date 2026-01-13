#!/usr/bin/env python3
"""
Example script demonstrating how to use the LinkedIn scraper programmatically
"""

from linkedin_scraper import LinkedInScraper, generate_markdown


def scrape_profile_example():
    """
    Example of using the LinkedInScraper class programmatically
    """
    # Initialize the scraper
    scraper = LinkedInScraper()

    # Example profile URL (replace with actual URL)
    profile_url = "https://www.linkedin.com/in/example-username"

    print(f"Scraping profile: {profile_url}\n")

    # Scrape the profile
    profile_data = scraper.scrape_profile(profile_url)

    # Check if we got data
    if profile_data and profile_data.get('name'):
        print(f"Successfully scraped profile for: {profile_data['name']}")

        # Generate markdown
        markdown_content = generate_markdown(profile_data)

        # Save to file
        output_file = "example_profile.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"Markdown saved to: {output_file}")

        # You can also access individual fields
        print(f"\nProfile Details:")
        print(f"  Name: {profile_data.get('name')}")
        print(f"  Headline: {profile_data.get('headline')}")
        print(f"  Location: {profile_data.get('location')}")
        print(f"  Number of experiences: {len(profile_data.get('experience', []))}")
        print(f"  Number of skills: {len(profile_data.get('skills', []))}")
    else:
        print("Failed to scrape profile. See troubleshooting in README.md")


def batch_scrape_example():
    """
    Example of scraping multiple profiles with rate limiting
    """
    import time

    scraper = LinkedInScraper()

    # List of profile URLs to scrape
    profile_urls = [
        "https://www.linkedin.com/in/profile1",
        "https://www.linkedin.com/in/profile2",
        "https://www.linkedin.com/in/profile3",
    ]

    profiles = []

    for url in profile_urls:
        print(f"Scraping: {url}")

        # Scrape the profile
        profile_data = scraper.scrape_profile(url)

        if profile_data and profile_data.get('name'):
            profiles.append(profile_data)
            print(f"  ✓ Scraped: {profile_data['name']}")
        else:
            print(f"  ✗ Failed to scrape")

        # Rate limiting - wait 3 seconds between requests
        # This is important to avoid being blocked
        time.sleep(3)

    print(f"\nSuccessfully scraped {len(profiles)} profiles")

    # Generate markdown for each profile
    for profile in profiles:
        markdown = generate_markdown(profile)
        filename = f"{profile['name'].replace(' ', '_')}_profile.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Saved: {filename}")


if __name__ == "__main__":
    print("LinkedIn Scraper Examples")
    print("=" * 50)
    print("\n1. Single Profile Scraping")
    print("2. Batch Profile Scraping (with rate limiting)")
    print("\nNote: Replace example URLs with real LinkedIn profile URLs")
    print("=" * 50)

    # Uncomment to run examples:
    # scrape_profile_example()
    # batch_scrape_example()

    print("\nTo use these examples, edit example.py and uncomment the desired function call.")
