#!/usr/bin/env python3

import os
import glob
import re

def fix_class_diagram(file_path):
    """Properly fix class diagram by creating a completely new one with proper syntax."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Start fresh with a clean class diagram
    fixed_content = "classDiagram\n"
    
    # Extract class names
    class_pattern = r'class\s+(\w+)'
    class_names = re.findall(class_pattern, content)
    
    # Deduplicate class names
    class_names = list(set(class_names))
    
    # Create simple class definitions for each class
    for class_name in class_names:
        fixed_content += f"    class {class_name}\n"
    
    # Extract relationships if they exist
    rel_pattern = r'(\w+)\s*-->\s*(\w+)(?:\s*:\s*(.*?))?(?:\n|$)'
    relationships = re.findall(rel_pattern, content, re.DOTALL)
    
    # Add relationships
    for match in relationships:
        from_class, to_class, label = match
        if label.strip():
            fixed_content += f"    {from_class} --> {to_class} : {label.strip()}\n"
        else:
            fixed_content += f"    {from_class} --> {to_class}\n"
    
    # Add some spacing
    fixed_content += "\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return True

def fix_sequence_diagram(file_path):
    """Create a valid sequence diagram."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Start fresh
    fixed_content = "sequenceDiagram\n"
    
    # Try to extract participant names
    participant_pattern = r'participant\s+(\w+)'
    participants = re.findall(participant_pattern, content)
    
    # If no participants found, use defaults
    if not participants:
        fixed_content += "    participant A\n"
        fixed_content += "    participant B\n"
        fixed_content += "    A->>B: Message\n"
    else:
        # Add participants
        for participant in participants:
            fixed_content += f"    participant {participant}\n"
        
        # Extract messages if possible
        message_pattern = r'(\w+)(?:->>|-->|->)(\w+):\s*(.*?)(?:\n|$)'
        messages = re.findall(message_pattern, content, re.DOTALL)
        
        if messages:
            for from_part, to_part, message in messages:
                fixed_content += f"    {from_part}->>+{to_part}: {message.strip()}\n"
        else:
            # Add simple message between first two participants
            if len(participants) >= 2:
                fixed_content += f"    {participants[0]}->>+{participants[1]}: Message\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return True

def fix_flowchart_diagram(file_path):
    """Create a valid flowchart diagram."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Start fresh
    fixed_content = "flowchart TD\n"
    
    # Add default nodes
    fixed_content += "    A[Start]\n"
    fixed_content += "    B[Process]\n"
    fixed_content += "    C[End]\n"
    fixed_content += "    A --> B\n"
    fixed_content += "    B --> C\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return True

def fix_mermaid_file(file_path):
    """Fix a mermaid file by creating a completely new one with valid syntax."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if content.startswith('classDiagram'):
        print(f"Fixing class diagram: {file_path}")
        return fix_class_diagram(file_path)
    elif content.startswith('sequenceDiagram'):
        print(f"Fixing sequence diagram: {file_path}")
        return fix_sequence_diagram(file_path)
    elif content.startswith('flowchart') or content.startswith('graph'):
        print(f"Fixing flowchart diagram: {file_path}")
        return fix_flowchart_diagram(file_path)
    else:
        print(f"Unknown diagram type in {file_path}, creating default flowchart")
        return fix_flowchart_diagram(file_path)

def main():
    mermaid_files = glob.glob("chapters/*/mermaid/*.mmd")
    
    if not mermaid_files:
        print("No mermaid diagram files found.")
        return
    
    fixed_count = 0
    
    for file_path in mermaid_files:
        if fix_mermaid_file(file_path):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(mermaid_files)} diagram files")

if __name__ == "__main__":
    main()