# Quick Start Guide - LinkedIn Profile Scraper

Get started with the LinkedIn Profile Scraper in just a few steps!

## 🚀 Quick Start with Web Interface (Recommended)

The easiest way to use the scraper is through the Gradio web interface:

### Step 1: Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd Linkedin-Webscraper

# Install dependencies using uv
uv sync
```

### Step 2: Launch the Web Interface

```bash
uv run python gradio_app.py
```

### Step 3: Open Your Browser

The interface will automatically open at: **http://127.0.0.1:7860**

If it doesn't open automatically, copy and paste that URL into your browser.

### Step 4: Scrape a Profile

1. Enter a LinkedIn profile URL (e.g., `https://www.linkedin.com/in/username`)
2. Click **"🚀 Scrape Profile"**
3. Wait for the scraping to complete
4. Preview the results in the browser
5. Download the markdown file

That's it! 🎉

## 📋 What You'll See

The web interface includes:
- **Input field** for LinkedIn profile URL
- **Real-time progress** indicator
- **Preview tab** showing the formatted markdown
- **Download tab** with a button to save the file
- **Tips and troubleshooting** built right in

## 💡 Tips for Success

1. **Make sure the profile is public** - Private profiles won't work
2. **Use the full URL** - Copy the complete URL from LinkedIn
3. **Be patient** - Scraping takes a few seconds
4. **Follow the rules** - Respect LinkedIn's Terms of Service

## 🎯 Alternative: Command Line Usage

If you prefer the command line:

```bash
uv run python linkedin_scraper.py https://www.linkedin.com/in/username
```

This will create a markdown file in your current directory.

## ❓ Common Issues

### "Could not extract profile data"
- The profile might be private
- LinkedIn might be blocking the request
- Try a different profile or wait a few minutes

### Web interface won't open
- Check if port 7860 is already in use
- Try a different port: `uv run python -c "from gradio_app import launch_app; launch_app(server_port=8080)"`

### Missing dependencies
- Run `uv sync` again
- Make sure you're in the project directory

## 🔗 Need More Help?

Check out the full [README.md](README.md) for:
- Detailed documentation
- Advanced usage examples
- Programmatic API usage
- Best practices and limitations

## ⚠️ Important Reminder

This tool is for educational purposes and works only with publicly visible LinkedIn profiles. Always respect:
- LinkedIn's Terms of Service
- Users' privacy
- Rate limits (don't scrape too many profiles at once)

For production use, consider using the [official LinkedIn API](https://developer.linkedin.com/).

---

**Happy Scraping! 🎊**
