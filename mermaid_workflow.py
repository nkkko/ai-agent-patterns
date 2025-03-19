#!/usr/bin/env python3

import os
import re
import glob
import subprocess
import tempfile
import json
import sys
import argparse
from pathlib import Path

#########################
# EXTRACTION FUNCTIONS
#########################

def extract_mermaid_diagrams(file_path):
    """Extract all mermaid diagrams from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match mermaid diagrams
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        print(f"No mermaid diagrams found in {file_path}")
        return []

    return matches

def save_diagrams(chapter_path, diagrams):
    """Save diagrams to individual files in the mermaid directory."""
    # Extract chapter number from file name (e.g., 01_building_blocks_of_software_agents.md -> 01)
    chapter_name = os.path.basename(chapter_path)
    chapter_num = chapter_name.split('_')[0]

    # Create directory if it doesn't exist
    mermaid_dir = f"chapters/{chapter_num}/mermaid"
    os.makedirs(mermaid_dir, exist_ok=True)

    # Save each diagram to a separate file
    saved_files = []
    for i, diagram in enumerate(diagrams, 1):
        # Create a name based on the first line of the diagram
        first_line = diagram.strip().split('\n')[0].strip()
        # Use the first line to create a file name, or default to diagram_N
        if first_line and (first_line.startswith('graph') or first_line.startswith('flowchart')):
            name = first_line.split()[1] if len(first_line.split()) > 1 else f"diagram_{i}"
        else:
            name = f"diagram_{i}"

        # Clean name to be a valid filename
        name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

        file_path = f"{mermaid_dir}/{name}.mmd"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(diagram)

        saved_files.append(file_path)
        print(f"Saved diagram to {file_path}")

    return saved_files

def process_all_chapters():
    """Process all markdown files in the chapters directory."""
    chapters_dir = "chapters"
    chapter_files = [f for f in os.listdir(chapters_dir) if f.endswith('.md') and f[0].isdigit()]

    total_diagrams = 0
    for chapter_file in sorted(chapter_files):
        chapter_path = os.path.join(chapters_dir, chapter_file)
        print(f"\nProcessing {chapter_path}...")

        diagrams = extract_mermaid_diagrams(chapter_path)
        if diagrams:
            saved_files = save_diagrams(chapter_path, diagrams)
            print(f"Extracted {len(diagrams)} diagram(s) from {chapter_path}")
            total_diagrams += len(diagrams)
        else:
            print(f"No diagrams found in {chapter_path}")

    return total_diagrams

#########################
# IMAGE GENERATION FUNCTIONS
#########################

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

def generate_all_images():
    """Generate images for all mermaid diagrams."""
    # Check if Node.js is installed
    try:
        node_version = subprocess.run(['node', '--version'],
                                    capture_output=True, text=True).stdout.strip()
        print(f"Node.js version: {node_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Node.js is required but not found.")
        print("Please install Node.js from https://nodejs.org/")
        return 0

    # Install or verify Mermaid CLI
    if not install_mermaid_cli_if_needed():
        return 0

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

            images_dir = f"chapters/{chapter_num}/images"
            success_count = 0

            for mmd_file in mmd_files:
                if generate_mermaid_image(mmd_file, images_dir, config_path):
                    success_count += 1

            print(f"Generated {success_count} out of {len(mmd_files)} images for chapter {chapter_num}")
            total_success += success_count

        print(f"\nSummary: Generated {total_success} out of {total_diagrams} images")

        return total_success

#########################
# MAIN FUNCTION
#########################

def main():
    parser = argparse.ArgumentParser(description='Mermaid Diagram Workflow for AI Agent Patterns Book')
    parser.add_argument('--extract-only', action='store_true', help='Only extract diagrams from markdown files')
    parser.add_argument('--generate-only', action='store_true', help='Only generate images from existing mermaid diagrams')

    args = parser.parse_args()

    # If no specific action is selected, perform all steps
    all_steps = not (args.extract_only or args.generate_only)

    if all_steps or args.extract_only:
        print("\n=== STEP 1: EXTRACTING MERMAID DIAGRAMS ===")
        num_extracted = process_all_chapters()
        print(f"Total diagrams extracted: {num_extracted}")

    if all_steps or args.generate_only:
        print("\n=== STEP 2: GENERATING DIAGRAM IMAGES ===")
        num_generated = generate_all_images()
        print(f"Total images generated: {num_generated}")

    print("\n=== WORKFLOW COMPLETED ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())