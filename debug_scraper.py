#!/usr/bin/env python3
"""
Debug version of the LinkedIn scraper to help troubleshoot issues
"""

import requests
from bs4 import BeautifulSoup
import sys


def debug_scrape(url):
    """Debug function to see what's being returned"""

    print("="*60)
    print("LINKEDIN SCRAPER DEBUG MODE")
    print("="*60)
    print(f"\n📍 Target URL: {url}\n")

    # Check URL format
    if not url.startswith('https://www.linkedin.com/in/'):
        print("❌ ERROR: Invalid URL format")
        print("   URL must start with: https://www.linkedin.com/in/")
        return

    print("✅ URL format is valid\n")

    # Set up headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    print("📡 Making request to LinkedIn...\n")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"✅ Response received!")
        print(f"   Status code: {response.status_code}")
        print(f"   Content length: {len(response.content)} bytes")
        print(f"   Content type: {response.headers.get('content-type', 'Unknown')}\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch URL")
        print(f"   Error: {e}")
        return

    # Check if we got a valid response
    if response.status_code != 200:
        print(f"❌ ERROR: HTTP {response.status_code}")
        print("   LinkedIn may be blocking the request or the profile doesn't exist")
        return

    # Parse HTML
    print("📄 Parsing HTML...\n")
    soup = BeautifulSoup(response.content, 'lxml')

    # Check if LinkedIn is showing a login wall
    if 'authwall' in response.url or 'login' in response.url:
        print("❌ ERROR: LinkedIn redirected to login page")
        print("   This means the profile is NOT actually public")
        print("   Or LinkedIn is requiring login despite public setting")
        return

    # Look for common LinkedIn elements
    print("🔍 Searching for profile elements...\n")

    # Check title
    title = soup.find('title')
    if title:
        print(f"   Page title: {title.get_text()[:100]}")

    # Check for meta tags
    meta_title = soup.find('meta', property='og:title')
    if meta_title:
        print(f"   Meta title: {meta_title.get('content', 'N/A')}")

    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        print(f"   Meta description: {meta_desc.get('content', 'N/A')[:100]}")

    # Look for name
    print("\n🔍 Looking for name...")
    name_h1 = soup.find('h1')
    if name_h1:
        print(f"   Found h1: {name_h1.get_text(strip=True)}")
    else:
        print("   ❌ No h1 tag found")

    # Look for headline
    print("\n🔍 Looking for headline...")
    h2_tags = soup.find_all('h2')[:3]
    if h2_tags:
        for i, h2 in enumerate(h2_tags):
            print(f"   h2 #{i+1}: {h2.get_text(strip=True)[:100]}")
    else:
        print("   ❌ No h2 tags found")

    # Check for sections
    print("\n🔍 Looking for sections...")
    sections = soup.find_all('section')
    print(f"   Found {len(sections)} section tags")

    # Save HTML for inspection
    output_file = "debug_output.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"\n💾 Full HTML saved to: {output_file}")
    print("   You can open this file to see what LinkedIn returned")

    # Check for common blocking indicators
    print("\n🚨 Checking for blocking indicators...")
    html_text = response.text.lower()

    blocking_signs = {
        'authwall': 'Authentication wall detected',
        'login': 'Login page detected',
        'sign in': 'Sign in prompt detected',
        'join now': 'Join prompt detected',
        'captcha': 'CAPTCHA detected',
        'robot': 'Bot detection triggered'
    }

    found_blocks = []
    for indicator, message in blocking_signs.items():
        if indicator in html_text:
            found_blocks.append(message)

    if found_blocks:
        print("   ❌ Potential blocking detected:")
        for block in found_blocks:
            print(f"      - {block}")
    else:
        print("   ✅ No obvious blocking indicators")

    print("\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_scraper.py <linkedin_profile_url>")
        print("\nExample:")
        print("  python debug_scraper.py https://www.linkedin.com/in/username")
        sys.exit(1)

    debug_scrape(sys.argv[1])
