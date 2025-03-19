#!/usr/bin/env python3

import os
import glob
import tempfile
import subprocess
import platform
import time
from pathlib import Path

def create_mermaid_html(mmd_file, output_html):
    """Create an HTML file that uses Mermaid.js to render the diagram with auto-sizing."""
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
            padding: 30px;
            background-color: white;
        }}
        .mermaid {{
            font-size: 18px;
            text-align: center;
            width: 100%;
        }}
        svg {{
            max-width: none !important;
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{ useMaxWidth: false }},
            securityLevel: 'loose'
        }});
        
        // After rendering is complete, adjust the SVG viewBox
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(function() {{
                const svgElement = document.querySelector('svg');
                if (svgElement) {{
                    // Make sure entire diagram is visible
                    const bbox = svgElement.getBBox();
                    const padding = 20;
                    svgElement.setAttribute('viewBox', 
                        `${{bbox.x - padding}} ${{bbox.y - padding}} ${{bbox.width + padding*2}} ${{bbox.height + padding*2}}`);
                    
                    // Signal to take screenshot
                    document.title = 'RENDER_COMPLETE';
                }}
            }}, 1000);
        }});
    </script>
</body>
</html>'''
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_html

def wait_for_render_complete(url, timeout=10):
    """Wait for the page to signal that rendering is complete."""
    try:
        if platform.system() == 'Darwin':  # macOS
            command = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--remote-debugging-port=9222',
                url
            ]
        elif platform.system() == 'Linux':
            command = [
                'google-chrome',
                '--headless',
                '--disable-gpu',
                '--remote-debugging-port=9222',
                url
            ]
        elif platform.system() == 'Windows':
            command = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                '--headless',
                '--disable-gpu',
                '--remote-debugging-port=9222',
                url
            ]
        else:
            raise Exception(f"Unsupported platform: {platform.system()}")
        
        # Start Chrome in headless mode
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the title to change
        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(0.5)
            
            # Check if title has changed
            title_check = subprocess.run(
                ['curl', '-s', 'http://localhost:9222/json'],
                capture_output=True, text=True
            )
            
            if 'RENDER_COMPLETE' in title_check.stdout:
                break
        
        # Give it a little more time to ensure everything is ready
        time.sleep(1)
    finally:
        # Make sure to terminate Chrome
        if 'process' in locals():
            process.terminate()

def capture_screenshot(html_path, output_image_path):
    """Use headless Chrome to capture screenshot of a Mermaid diagram."""
    try:
        # URL for the HTML file
        url = f'file://{html_path}'
        
        # Wait for rendering to complete
        wait_for_render_complete(url)
        
        # Now take the screenshot with the properly rendered diagram
        if platform.system() == 'Darwin':  # macOS
            chrome_cmd = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--hide-scrollbars',
                '--screenshot=' + output_image_path,
                '--window-size=1600,1600',
                '--default-background-color=0',
                url
            ]
        elif platform.system() == 'Linux':
            chrome_cmd = [
                'google-chrome',
                '--headless',
                '--disable-gpu',
                '--hide-scrollbars',
                '--screenshot=' + output_image_path,
                '--window-size=1600,1600',
                '--default-background-color=0',
                url
            ]
        elif platform.system() == 'Windows':
            chrome_cmd = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                '--headless',
                '--disable-gpu',
                '--hide-scrollbars',
                '--screenshot=' + output_image_path,
                '--window-size=1600,1600',
                '--default-background-color=0',
                url
            ]
        else:
            raise Exception(f"Unsupported platform: {platform.system()}")
        
        print(f"Running: {' '.join(chrome_cmd)}")
        subprocess.run(chrome_cmd, check=True, capture_output=True, text=True)
        
        if os.path.exists(output_image_path):
            print(f"Successfully generated {output_image_path}")
            return True
        else:
            print(f"Failed to generate image for {html_path}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def generate_mermaid_image(mmd_file, output_dir):
    """Generate a PNG image from a mermaid diagram file."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.basename(mmd_file).rsplit('.', 1)[0]
    output_file = os.path.join(output_dir, f"{base_name}.png")
    
    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        temp_html_path = temp_html.name
    
    try:
        # Create HTML with Mermaid diagram
        create_mermaid_html(mmd_file, temp_html_path)
        
        # Capture screenshot
        if capture_screenshot(temp_html_path, output_file):
            # Post-process the image with ImageMagick
            try:
                # Trim excess white space
                trim_cmd = ["convert", output_file, "-trim", "+repage", output_file]
                subprocess.run(trim_cmd, check=True, capture_output=True)
                
                # Add a small padding around the image
                pad_cmd = ["convert", output_file, "-bordercolor", "white", "-border", "20x20", output_file]
                subprocess.run(pad_cmd, check=True, capture_output=True)
                
                # Ensure good quality
                quality_cmd = ["convert", output_file, "-density", "300", "-quality", "100", output_file]
                subprocess.run(quality_cmd, check=True, capture_output=True)
                
                print(f"Post-processed image: {output_file}")
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"ImageMagick issue: {e}")
            
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
        if generate_mermaid_image(mmd_file, images_dir):
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
        return 1
    
    # Find all chapter directories with mermaid diagrams
    mermaid_dirs = glob.glob("chapters/*/mermaid")
    chapter_nums = [os.path.basename(os.path.dirname(d)) for d in mermaid_dirs]
    
    if not chapter_nums:
        print("No mermaid diagram directories found.")
        return 0
    
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
        return 1
    else:
        print("\nAll images generated successfully!")
        return 0

if __name__ == "__main__":
    main()