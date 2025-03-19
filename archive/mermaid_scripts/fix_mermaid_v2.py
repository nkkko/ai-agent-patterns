#!/usr/bin/env python3

import os
import glob
import re
import sys

def fix_diagram(file_path):
    """Fix common syntax issues in a mermaid diagram file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove multi-line classDef blocks
    content = re.sub(r'class\s+\w+\s+{[\s\S]*?style\s+fill:.*?}.*?$', '', content, flags=re.MULTILINE)
    
    # Remove classDef lines
    content = re.sub(r'classDef\s+.*?$', '', content, flags=re.MULTILINE)
    
    # Remove class style assignments
    content = re.sub(r'class\s+\w+\s+\w+.*?$', '', content, flags=re.MULTILINE)
    
    # Fix note syntax with quotes (keep it simple)
    if 'note for' in content and not 'note for' in content.replace('note for', ''):
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.strip().startswith('note for') and '"' in line:
                parts = line.split('"')
                if len(parts) >= 3:
                    note_text = parts[1].replace('\n', ' ')
                    target = line.split('note for')[1].split('"')[0].strip()
                    new_line = f'    note for {target} "{note_text}"'
                    new_lines.append(new_line)
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)
    
    # Clean up any leftover "color:white" fragments
    content = re.sub(r'color:.*?$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines at the end
    content = content.rstrip() + '\n'
    
    # Only write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed diagram in {file_path}")
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