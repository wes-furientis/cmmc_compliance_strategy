#!/usr/bin/env python3
"""
Render Mermaid diagrams to PNG using mermaid.ink API.
This avoids the need for puppeteer/Chrome browser.
"""

import base64
import requests
import os
import zlib

def render_mermaid_to_png(mmd_content, output_path, theme='default'):
    """
    Render mermaid diagram content to PNG using mermaid.ink API.

    Args:
        mmd_content: The mermaid diagram source code
        mmd_path: Path to save the output PNG
        theme: Mermaid theme (default, dark, forest, neutral)
    """
    # Encode the diagram for the URL
    # mermaid.ink uses base64 encoding
    encoded = base64.urlsafe_b64encode(mmd_content.encode('utf-8')).decode('utf-8')

    # Build the URL for PNG output
    url = f"https://mermaid.ink/img/{encoded}?type=png&bgColor=white&theme={theme}"

    print(f"Fetching diagram from mermaid.ink...")

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"  Created: {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        return False

def render_mermaid_file(mmd_path, output_path=None, theme='default'):
    """
    Render a .mmd file to PNG.

    Args:
        mmd_path: Path to the .mmd file
        output_path: Path for output PNG (defaults to same name with .png extension)
        theme: Mermaid theme
    """
    if output_path is None:
        output_path = os.path.splitext(mmd_path)[0] + '.png'

    with open(mmd_path, 'r') as f:
        content = f.read()

    print(f"\nRendering: {os.path.basename(mmd_path)}")
    return render_mermaid_to_png(content, output_path, theme)

def main():
    """Render all mermaid diagrams in the current directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    diagrams = [
        ('dual_echelon_architecture.mmd', 'dual_echelon_architecture.png'),
        ('cui_data_flow.mmd', 'cui_data_flow.png'),
        ('implementation_roadmap.mmd', 'implementation_roadmap.png'),
    ]

    print("Rendering Mermaid diagrams using mermaid.ink API...")
    print("=" * 50)

    success_count = 0
    for mmd_file, png_file in diagrams:
        mmd_path = os.path.join(script_dir, mmd_file)
        png_path = os.path.join(script_dir, png_file)

        if os.path.exists(mmd_path):
            if render_mermaid_file(mmd_path, png_path, theme='default'):
                success_count += 1
        else:
            print(f"\nSkipping: {mmd_file} (file not found)")

    print("\n" + "=" * 50)
    print(f"Rendered {success_count}/{len(diagrams)} diagrams successfully.")

if __name__ == '__main__':
    main()
