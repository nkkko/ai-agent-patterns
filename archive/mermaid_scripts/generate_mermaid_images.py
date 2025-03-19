#!/usr/bin/env python3

import os
import subprocess
import glob
import sys
import platform
import tempfile
import base64
import re

def create_mermaid_html(mmd_file, output_html):
    """Create an HTML file that uses Mermaid.js to render the diagram."""
    with open(mmd_file, 'r', encoding='utf-8') as f:
        mermaid_code = f.read()
    
    # Clean any SVG-invalid characters from the diagram code
    mermaid_code = mermaid_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mermaid Diagram</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.7.0/mermaid.min.js"></script>
    <style>
        body {{ background-color: white; margin: 0; padding: 20px; }}
        #diagram {{ width: 100%; }}
    </style>
</head>
<body>
    <div id="diagram" class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            fontFamily: 'Trebuchet MS, Verdana, Arial, sans-serif',
            logLevel: 5
        }});
        window.onload = function() {{
            // Add small delay to ensure diagram renders correctly
            setTimeout(function() {{
                // Send message to parent window when rendering is complete
                window.status = 'done';
            }}, 500);
        }};
    </script>
</body>
</html>
'''
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_html

def capture_screenshot(html_path, output_image_path, width=1200, height=800):
    """Use headless Chrome to capture screenshot of the rendered Mermaid diagram."""
    try:
        # Construct the command to capture the web page
        if platform.system() == 'Darwin':  # macOS
            chrome_cmd = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                f'--window-size={width},{height}',
                f'--screenshot={output_image_path}',
                f'file://{html_path}'
            ]
        elif platform.system() == 'Linux':
            chrome_cmd = [
                'google-chrome',
                '--headless',
                '--disable-gpu',
                f'--window-size={width},{height}',
                f'--screenshot={output_image_path}',
                f'file://{html_path}'
            ]
        elif platform.system() == 'Windows':
            chrome_cmd = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                '--headless',
                '--disable-gpu',
                f'--window-size={width},{height}',
                f'--screenshot={output_image_path}',
                f'file://{html_path}'
            ]
        else:
            raise Exception(f"Unsupported platform: {platform.system()}")
        
        print(f"Running: {' '.join(chrome_cmd)}")
        subprocess.run(chrome_cmd, check=True, capture_output=True, text=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def generate_diagram_image(mmd_file, output_dir):
    """Generate an image from a mermaid diagram file."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.basename(mmd_file).rsplit('.', 1)[0]
    output_file = os.path.join(output_dir, f"{base_name}.png")
    
    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        temp_html_path = temp_html.name
    
    try:
        # Create the HTML with embedded mermaid
        create_mermaid_html(mmd_file, temp_html_path)
        
        # Capture screenshot of rendered diagram
        if capture_screenshot(temp_html_path, output_file):
            print(f"Successfully generated {output_file}")
            return True
        else:
            return False
    finally:
        # Clean up temporary file
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)

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
        if generate_diagram_image(mmd_file, images_dir):
            success_count += 1
    
    print(f"Generated {success_count} out of {len(mmd_files)} images for chapter {chapter_num}")
    return success_count

def check_chrome_installed():
    """Check if Chrome is installed on the system."""
    try:
        if platform.system() == 'Darwin':  # macOS
            return os.path.exists('/Applications/Google Chrome.app')
        elif platform.system() == 'Linux':
            return subprocess.run(['which', 'google-chrome'], 
                                 capture_output=True).returncode == 0
        elif platform.system() == 'Windows':
            return os.path.exists(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        return False
    except Exception:
        return False

def main():
    # Check if Chrome is installed
    if not check_chrome_installed():
        print("Google Chrome is required but not found.")
        print("Please install Chrome and try again.")
        sys.exit(1)
    
    # Find all chapter directories with mermaid diagrams
    mermaid_dirs = glob.glob("chapters/*/mermaid")
    chapter_nums = [os.path.basename(os.path.dirname(d)) for d in mermaid_dirs]
    
    if not chapter_nums:
        print("No mermaid diagrams found in any chapter.")
        sys.exit(0)
    
    total_success = 0
    total_diagrams = 0
    
    for chapter_num in sorted(chapter_nums):
        print(f"\nProcessing chapter {chapter_num}...")
        mmd_files = glob.glob(f"chapters/{chapter_num}/mermaid/*.mmd")
        total_diagrams += len(mmd_files)
        total_success += process_chapter_diagrams(chapter_num)
    
    print(f"\nSummary: Generated {total_success} out of {total_diagrams} images")
    
    if total_success < total_diagrams:
        print("\nSome images failed to generate.")
        sys.exit(1)
    else:
        print("\nAll images generated successfully!")

if __name__ == "__main__":
    main()