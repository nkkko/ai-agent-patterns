#!/usr/bin/env python3

import os
import glob
import tempfile
import subprocess
import base64
import json
from pathlib import Path

def create_mermaid_html(mmd_file, output_html):
    """Create an HTML file that uses Mermaid.js to render the diagram."""
    with open(mmd_file, 'r', encoding='utf-8') as f:
        mermaid_code = f.read()
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mermaid Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: white;
        }}
        #container {{
            display: inline-block;
            background-color: white;
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default'
        }});
    </script>
</body>
</html>'''
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_html

def create_puppeteer_script(html_path, output_path):
    """Create a Puppeteer script to capture the diagram element only."""
    script = f'''
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {{
  const browser = await puppeteer.launch({{
    headless: "new"
  }});
  const page = await browser.newPage();
  
  // Navigate to the HTML file
  await page.goto('file://{html_path}', {{
    waitUntil: 'networkidle0',
  }});
  
  // Wait for Mermaid to render
  await page.waitForFunction(() => {{
    return document.querySelector('.mermaid svg') !== null;
  }}, {{ timeout: 5000 }});
  
  // Get the SVG element
  const svgElement = await page.$('.mermaid svg');
  if (!svgElement) {{
    console.error('SVG element not found');
    await browser.close();
    process.exit(1);
  }}
  
  // Get the bounding box
  const boundingBox = await svgElement.boundingBox();
  
  // Take a screenshot of just the SVG element
  await svgElement.screenshot({{
    path: '{output_path}',
    omitBackground: true
  }});
  
  await browser.close();
}})();
'''
    script_path = os.path.join(os.path.dirname(html_path), 'puppeteer_script.js')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    return script_path

def generate_mermaid_image(mmd_file, output_dir):
    """Generate a precisely sized PNG image from a mermaid file."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.basename(mmd_file).rsplit('.', 1)[0]
    output_file = os.path.join(output_dir, f"{base_name}.png")
    
    # Create temporary directory for working files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the HTML file
        html_path = os.path.join(temp_dir, 'diagram.html')
        create_mermaid_html(mmd_file, html_path)
        
        # Create the Puppeteer script
        script_path = create_puppeteer_script(html_path, output_file)
        
        # Run Puppeteer to capture the screenshot
        try:
            # Check if puppeteer is installed
            check_cmd = ["npm", "list", "puppeteer"]
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            if "puppeteer" not in result.stdout:
                print("Installing puppeteer...")
                install_cmd = ["npm", "install", "puppeteer"]
                subprocess.run(install_cmd, check=True)
            
            # Run the Puppeteer script
            cmd = ["node", script_path]
            subprocess.run(cmd, check=True)
            
            if os.path.exists(output_file):
                print(f"Successfully generated {output_file}")
                return True
            else:
                print(f"Failed to generate image for {mmd_file}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"Error running Puppeteer: {e}")
            return False

def process_chapter_diagrams(chapter_num):
    """Process all mermaid diagrams for a specific chapter."""
    mermaid_dir = f"chapters/{chapter_num}/mermaid"
    images_dir = f"chapters/{chapter_num}/images"
    
    if not os.path.exists(mermaid_dir):
        print(f"No mermaid directory found for chapter {chapter_num}")
        return 0
    
    mmd_files = glob.glob(f"{mermaid_dir}/*.mmd")
    success_count = 0
    
    for mmd_file in mmd_files:
        if generate_mermaid_image(mmd_file, images_dir):
            success_count += 1
    
    print(f"Generated {success_count} out of {len(mmd_files)} images for chapter {chapter_num}")
    return success_count

def main():
    """Main function to process all chapters with mermaid diagrams."""
    # Find all chapter directories with mermaid diagrams
    mermaid_dirs = glob.glob("chapters/*/mermaid")
    chapter_nums = [os.path.basename(os.path.dirname(d)) for d in mermaid_dirs]
    
    if not chapter_nums:
        print("No mermaid diagram directories found.")
        return
    
    total_success = 0
    total_diagrams = 0
    
    for chapter_num in sorted(chapter_nums):
        print(f"\nProcessing chapter {chapter_num}...")
        mmd_files = glob.glob(f"chapters/{chapter_num}/mermaid/*.mmd")
        total_diagrams += len(mmd_files)
        total_success += process_chapter_diagrams(chapter_num)
    
    print(f"\nSummary: Generated {total_success} out of {total_diagrams} images")
    
    if total_success < total_diagrams:
        print("\nSome images failed to generate. Make sure you have Node.js installed.")
        return 1
    else:
        print("\nAll images generated successfully!")
        return 0

if __name__ == "__main__":
    main()