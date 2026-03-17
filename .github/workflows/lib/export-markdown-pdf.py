#!/usr/bin/env python3
"""
Converts a Markdown file to PDF using markdown + weasyprint.

This handles embedded HTML (tables, images, etc.) that commonly appears
in Markdown files, producing a faithful PDF representation.

Usage:
    python export-markdown-pdf.py <input.md> <output.pdf>

Arguments:
    input   - Absolute path to the Markdown file
    output  - Absolute path to the output PDF file
"""

import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import markdown
from weasyprint import HTML


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.pdf>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Converting: {input_path}")
    print(f"Output: {output_path}")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Read the markdown content
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Build the timestamp in Eastern Time
    et_tz = ZoneInfo("America/New_York")
    now_et = datetime.now(et_tz)
    timestamp_str = now_et.strftime("%B %d, %Y %I:%M %p ET")

    # Convert markdown to HTML, enabling useful extensions
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc'],
    )

    # Wrap in a minimal HTML document
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @page {{
      margin: 2cm;
    }}
    body {{
      font-family: sans-serif;
    }}
    img {{
      max-width: 100%;
      height: auto;
      display: block;
    }}
    .no-pdf {{
      display: none;
    }}
    .logo {{
      max-width: 300px;
      text-align: center;
    }}
    .gridLogo {{
      max-width: 60px;
    }}
    .timestamp {{
      font-size: 0.75em;
      color: #666;
      border-bottom: 1px solid #ccc;
      padding-bottom: 0.4em;
      margin-bottom: 1.5em;
    }}
  </style>
</head>
<body>
<div class="timestamp">Generated: {timestamp_str}</div>
{html_body}
</body>
</html>"""

    # Use the input file's directory as the base URL so relative image
    # paths (e.g. ../Assets/Logo/Logo.png) resolve correctly
    base_url = os.path.dirname(input_path)

    HTML(string=html_doc, base_url=base_url).write_pdf(output_path)

    if os.path.exists(output_path):
        print(f"Successfully generated: {output_path}")
    else:
        print("Failed to generate PDF")
        sys.exit(1)


if __name__ == '__main__':
    main()
