#!/usr/bin/env python3
"""
Gradio Web Interface for LinkedIn Profile Scraper

This provides a user-friendly web interface to scrape LinkedIn profiles
and download the results as markdown files.
"""

import gradio as gr
from linkedin_scraper import LinkedInScraper, generate_markdown
import os
import tempfile
from datetime import datetime


class GradioLinkedInApp:
    """Gradio application for LinkedIn profile scraping"""

    def __init__(self):
        self.scraper = LinkedInScraper()

    def scrape_profile_interface(self, profile_url: str, progress=gr.Progress()):
        """
        Scrape a LinkedIn profile and return results for Gradio interface

        Args:
            profile_url: LinkedIn profile URL
            progress: Gradio progress tracker

        Returns:
            tuple: (status_message, markdown_preview, download_file_path)
        """
        # Validate URL
        if not profile_url:
            return "❌ Please enter a LinkedIn profile URL", "", None

        if not profile_url.startswith('https://www.linkedin.com/in/'):
            return (
                "❌ Invalid URL format. Please provide a valid LinkedIn profile URL\n"
                "URL should start with: https://www.linkedin.com/in/",
                "",
                None
            )

        # Update progress
        progress(0.2, desc="Fetching profile...")

        # Scrape the profile
        try:
            profile_data = self.scraper.scrape_profile(profile_url)
        except Exception as e:
            return f"❌ Error fetching profile: {str(e)}", "", None

        # Update progress
        progress(0.6, desc="Processing data...")

        # Check if we got valid data
        if not profile_data or not profile_data.get('name'):
            error_msg = """
❌ Could not extract profile data. This could be due to:

• LinkedIn's anti-scraping measures blocking the request
• Private profile (not publicly visible)
• Invalid URL
• Network issues

**Suggestions:**
1. Ensure the profile is set to public
2. Check the URL format
3. Try again after a few minutes
4. Consider using LinkedIn's official API for production use
            """
            return error_msg.strip(), "", None

        # Generate markdown
        progress(0.8, desc="Generating markdown...")
        markdown_content = generate_markdown(profile_data)

        # Create a temporary file for download
        name = profile_data.get('name', 'profile').replace(' ', '_').replace('/', '-')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_linkedin_profile_{timestamp}.md"

        # Save to temp file for download
        temp_file = os.path.join(tempfile.gettempdir(), filename)
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Create success message
        success_msg = f"""
✅ Successfully scraped profile!

**Name:** {profile_data.get('name', 'Unknown')}
**Headline:** {profile_data.get('headline', 'N/A')}
**Location:** {profile_data.get('location', 'N/A')}

**Data extracted:**
• Experience entries: {len(profile_data.get('experience', []))}
• Education entries: {len(profile_data.get('education', []))}
• Skills: {len(profile_data.get('skills', []))}
• Languages: {len(profile_data.get('languages', []))}
• Certifications: {len(profile_data.get('certifications', []))}

**File ready for download:** {filename}
        """

        progress(1.0, desc="Complete!")

        return success_msg.strip(), markdown_content, temp_file

    def create_interface(self):
        """Create and configure the Gradio interface"""

        # Custom CSS for better styling
        custom_css = """
        .gradio-container {
            font-family: 'Arial', sans-serif;
        }
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        """

        # Create the interface
        with gr.Blocks(css=custom_css) as app:
            # Header
            gr.Markdown(
                """
                # 🔍 LinkedIn Profile Scraper

                Extract publicly available LinkedIn profile information and generate a formatted Markdown document.
                """,
                elem_classes="main-header"
            )

            # Warning box
            gr.Markdown(
                """
                ⚠️ **Important:** This tool only works with publicly visible LinkedIn profiles.
                Always respect LinkedIn's Terms of Service and users' privacy.
                """,
                elem_classes="warning-box"
            )

            # Main interface
            with gr.Row():
                with gr.Column(scale=2):
                    # Input section
                    gr.Markdown("### Enter LinkedIn Profile URL")
                    profile_url_input = gr.Textbox(
                        label="LinkedIn Profile URL",
                        placeholder="https://www.linkedin.com/in/username",
                        lines=1,
                        scale=2
                    )

                    # Example URLs
                    gr.Markdown(
                        """
                        **Example format:** `https://www.linkedin.com/in/username`

                        **Note:** The profile must be publicly accessible (not private or requiring login).
                        """
                    )

                    # Buttons
                    with gr.Row():
                        scrape_btn = gr.Button("🚀 Scrape Profile", variant="primary", scale=2)
                        clear_btn = gr.Button("🗑️ Clear", scale=1)

                with gr.Column(scale=1):
                    # Info box
                    gr.Markdown(
                        """
                        ### What gets extracted?

                        ✓ Name & Headline
                        ✓ Location
                        ✓ About/Summary
                        ✓ Work Experience
                        ✓ Education
                        ✓ Skills
                        ✓ Languages
                        ✓ Certifications

                        ### Output Format

                        Clean, formatted Markdown document ready for download.
                        """
                    )

            # Output section
            gr.Markdown("---")
            gr.Markdown("## Results")

            status_output = gr.Markdown(label="Status")

            with gr.Tabs():
                with gr.Tab("📄 Preview"):
                    markdown_preview = gr.Markdown(
                        label="Markdown Preview",
                        value="*Markdown preview will appear here after scraping...*"
                    )

                with gr.Tab("📥 Download"):
                    gr.Markdown("Download the complete profile as a Markdown file:")
                    download_file = gr.File(label="Download Markdown File")

            # Footer
            gr.Markdown(
                """
                ---

                ### Tips for Best Results

                1. **Ensure the profile is public** - Private profiles cannot be scraped
                2. **Use the full profile URL** - Include the complete `https://www.linkedin.com/in/username` URL
                3. **Be patient** - Scraping may take a few seconds
                4. **Respect rate limits** - Avoid scraping too many profiles in quick succession
                5. **Follow LinkedIn TOS** - Only scrape profiles you have permission to access

                ### Troubleshooting

                **❌ "Could not extract profile data"**
                - The profile may be private or require authentication
                - LinkedIn may be blocking the request (anti-scraping measures)
                - Try again after a few minutes
                - Consider using LinkedIn's official API

                **❌ "Invalid URL format"**
                - Ensure the URL starts with `https://www.linkedin.com/in/`
                - Check for typos in the URL

                ---

                **Disclaimer:** This tool is for educational purposes only. Always respect LinkedIn's
                Terms of Service and users' privacy. For production use, consider using the
                [official LinkedIn API](https://developer.linkedin.com/).
                """
            )

            # Event handlers
            scrape_btn.click(
                fn=self.scrape_profile_interface,
                inputs=[profile_url_input],
                outputs=[status_output, markdown_preview, download_file],
                show_progress=True
            )

            clear_btn.click(
                fn=lambda: ("", "", None, "*Markdown preview will appear here after scraping...*"),
                inputs=[],
                outputs=[profile_url_input, status_output, download_file, markdown_preview]
            )

            # Allow Enter key to trigger scraping
            profile_url_input.submit(
                fn=self.scrape_profile_interface,
                inputs=[profile_url_input],
                outputs=[status_output, markdown_preview, download_file],
                show_progress=True
            )

        return app


def launch_app(share=False, server_name="127.0.0.1", server_port=7860):
    """
    Launch the Gradio application

    Args:
        share: Whether to create a public link (default: False)
        server_name: Server host address (default: "127.0.0.1")
        server_port: Server port (default: 7860)
    """
    app_instance = GradioLinkedInApp()
    app = app_instance.create_interface()

    print("🚀 Launching LinkedIn Profile Scraper Web Interface...")
    print(f"📍 Server will run on: http://{server_name}:{server_port}")
    print("\n⚠️  Remember: Only scrape publicly visible profiles and respect LinkedIn's TOS!")
    print("\n🛑 Press CTRL+C to stop the server\n")

    app.launch(
        share=share,
        server_name=server_name,
        server_port=server_port,
        show_error=True,
        inbrowser=True
    )


if __name__ == "__main__":
    # Launch with default settings
    # Set share=True to create a public link (not recommended for production)
    launch_app(share=False)
