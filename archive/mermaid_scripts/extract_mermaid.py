#!/usr/bin/env python3

import os
import re
import sys

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
        if first_line and first_line.startswith('graph') or first_line.startswith('flowchart'):
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
    
    for chapter_file in sorted(chapter_files):
        chapter_path = os.path.join(chapters_dir, chapter_file)
        print(f"\nProcessing {chapter_path}...")
        
        diagrams = extract_mermaid_diagrams(chapter_path)
        if diagrams:
            save_diagrams(chapter_path, diagrams)
            print(f"Extracted {len(diagrams)} diagram(s) from {chapter_path}")
        else:
            print(f"No diagrams found in {chapter_path}")

if __name__ == "__main__":
    process_all_chapters()