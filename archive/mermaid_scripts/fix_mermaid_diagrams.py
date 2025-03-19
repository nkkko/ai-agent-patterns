#!/usr/bin/env python3

import os
import glob
import re
import sys

def fix_class_diagram(content):
    """Fix common issues in class diagrams."""
    
    # Fix note syntax
    fixed = re.sub(r'note for (\w+) "(.*?)"', r'note for \1: "\2"', content, flags=re.DOTALL)
    
    # Handle classDef by removing them completely (simplest fix)
    fixed = re.sub(r'classDef.*?\n', '', fixed)
    
    # Remove class style assignments
    fixed = re.sub(r'class\s+(\w+)\s+(\w+)(\s|$)', '', fixed)
    
    return fixed

def fix_sequence_diagram(content):
    """Fix common issues in sequence diagrams."""
    # Nothing specific yet, but we can add more fixes as needed
    return content

def fix_flowchart_diagram(content):
    """Fix common issues in flowchart diagrams."""
    # Nothing specific yet, but we can add more fixes as needed
    return content

def fix_diagram(file_path):
    """Fix common syntax issues in a mermaid diagram file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    diagram_type = None
    
    # Determine diagram type
    if content.strip().startswith('classDiagram'):
        diagram_type = 'class'
        content = fix_class_diagram(content)
    elif content.strip().startswith('sequenceDiagram'):
        diagram_type = 'sequence'
        content = fix_sequence_diagram(content)
    elif content.strip().startswith('flowchart') or content.strip().startswith('graph'):
        diagram_type = 'flowchart'
        content = fix_flowchart_diagram(content)
    else:
        print(f"Unknown diagram type in {file_path}")
        return False
    
    # Only write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {diagram_type} diagram in {file_path}")
        return True
    else:
        print(f"No changes needed for {file_path}")
        return False

def main():
    # Find all mermaid files
    mermaid_files = glob.glob("chapters/*/mermaid/*.mmd")
    
    if not mermaid_files:
        print("No mermaid diagram files found.")
        return
    
    fixed_count = 0
    
    for file_path in mermaid_files:
        if fix_diagram(file_path):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(mermaid_files)} diagram files")

if __name__ == "__main__":
    main()