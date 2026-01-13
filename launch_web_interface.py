#!/usr/bin/env python3
"""
Simple launcher script for the LinkedIn Profile Scraper Web Interface

This script provides an easy way to launch the Gradio web interface
with customizable options.
"""

import argparse
from gradio_app import launch_app


def main():
    parser = argparse.ArgumentParser(
        description="Launch the LinkedIn Profile Scraper Web Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_web_interface.py
  python launch_web_interface.py --port 8080
  python launch_web_interface.py --share
  python launch_web_interface.py --host 0.0.0.0 --port 7860
        """
    )

    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Server host address (default: 127.0.0.1)'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=7860,
        help='Server port (default: 7860)'
    )

    parser.add_argument(
        '--share',
        action='store_true',
        help='Create a public shareable link (temporary, not recommended for production)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LinkedIn Profile Scraper - Web Interface Launcher")
    print("=" * 60)
    print()

    if args.share:
        print("⚠️  WARNING: You are creating a public shareable link!")
        print("   Anyone with the link can access your scraper.")
        print("   This is not recommended for production use.")
        print()

    launch_app(
        share=args.share,
        server_name=args.host,
        server_port=args.port
    )


if __name__ == "__main__":
    main()
