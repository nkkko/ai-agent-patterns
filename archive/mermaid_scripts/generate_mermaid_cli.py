#!/usr/bin/env python3

import os
import glob
import subprocess
import tempfile
import json
import sys
import platform
from pathlib import Path

def install_mermaid_cli_if_needed():
    """Install Mermaid CLI globally if not already installed."""
    try:
        # First check if mmdc is already available
        result = subprocess.run(['mmdc', '--version'], 
                               capture_output=True, text=True)
        print(f"Mermaid CLI is already installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            print("Installing @mermaid-js/mermaid-cli globally...")
            cmd = ['npm', 'install', '-g', '@mermaid-js/mermaid-cli']
            subprocess.run(cmd, check=True)
            print("Mermaid CLI installed successfully.")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to install Mermaid CLI: {e}")
            print("Please install Node.js and run: npm install -g @mermaid-js/mermaid-cli")
            return False

def create_mermaid_config(output_dir):
    """Create a Mermaid CLI configuration file."""
    config_path = os.path.join(output_dir, 'mermaid.config.json')
    
    config = {
        "theme": "default",
        "themeVariables": {
            "fontSize": "16px"
        },
        "flowchart": {
            "useMaxWidth": False,
            "htmlLabels": True
        },
        "sequence": {
            "useMaxWidth": False,
            "showSequenceNumbers": False,
            "boxMargin": 10
        },
        "gantt": {
            "useMaxWidth": False
        },
        "themeCSS": ".node rect { fill: #fff; stroke: #333; stroke-width: 1.5px; } .edgePath path { stroke: #333; stroke-width: 1.5px; }"
    }
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_path

def generate_mermaid_image(mmd_file, output_dir, config_path):
    """Generate a PNG image from a mermaid diagram file using mmdc CLI."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.basename(mmd_file).rsplit('.', 1)[0]
    output_file = os.path.join(output_dir, f"{base_name}.png")
    
    try:
        # Use mmdc to generate the image with the config
        cmd = [
            'mmdc', 
            '-i', mmd_file, 
            '-o', output_file,
            '-c', config_path,
            '-w', '1080',  # Set width
            '-H', '768',   # Set height
            '-b', 'white'  # Background color
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Optionally post-process with ImageMagick for better quality
        try:
            # Trim excess white space
            trim_cmd = ["convert", output_file, "-trim", "+repage", output_file]
            subprocess.run(trim_cmd, check=True, capture_output=True)
            
            # Add padding
            pad_cmd = ["convert", output_file, "-bordercolor", "white", "-border", "20x20", output_file]
            subprocess.run(pad_cmd, check=True, capture_output=True)
            
            # Enhance quality
            quality_cmd = ["convert", output_file, "-density", "300", "-quality", "100", output_file]
            subprocess.run(quality_cmd, check=True, capture_output=True)
            
            print(f"Enhanced image quality: {output_file}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Note: ImageMagick processing skipped: {e}")
        
        print(f"Successfully generated {output_file}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error generating image for {mmd_file}: {e}")
        if hasattr(e, 'stdout'):
            print(f"STDOUT: {e.stdout}")
        if hasattr(e, 'stderr'):
            print(f"STDERR: {e.stderr}")
        return False

def process_chapter_diagrams(chapter_num, config_path):
    """Process all mermaid diagrams for a specific chapter."""
    mermaid_dir = f"chapters/{chapter_num}/mermaid"
    images_dir = f"chapters/{chapter_num}/images"
    
    if not os.path.exists(mermaid_dir):
        print(f"No mermaid directory found for chapter {chapter_num}")
        return 0
    
    mmd_files = glob.glob(f"{mermaid_dir}/*.mmd")
    success_count = 0
    
    for mmd_file in mmd_files:
        if generate_mermaid_image(mmd_file, images_dir, config_path):
            success_count += 1
    
    print(f"Generated {success_count} out of {len(mmd_files)} images for chapter {chapter_num}")
    return success_count

def main():
    # Check if Node.js is installed
    try:
        node_version = subprocess.run(['node', '--version'], 
                                     capture_output=True, text=True).stdout.strip()
        print(f"Node.js version: {node_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Node.js is required but not found.")
        print("Please install Node.js from https://nodejs.org/")
        return 1
    
    # Install or verify Mermaid CLI
    if not install_mermaid_cli_if_needed():
        return 1
    
    # Create temp directory for configuration
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create Mermaid configuration
        config_path = create_mermaid_config(temp_dir)
        
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
            total_success += process_chapter_diagrams(chapter_num, config_path)
        
        print(f"\nSummary: Generated {total_success} out of {total_diagrams} images")
        
        if total_success < total_diagrams:
            print("\nSome images failed to generate.")
            return 1
        else:
            print("\nAll images generated successfully!")
            return 0

if __name__ == "__main__":
    sys.exit(main())