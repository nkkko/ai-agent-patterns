#!/usr/bin/env python3
"""
Generate Book Chapter Overview Diagram for AI Agent Design Patterns book.

This image illustrates the structure and flow of chapters in the book
for Chapter 0: Introduction.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.patheffects import withStroke
from pathlib import Path as FilePath
import os

# Create output directory if it doesn't exist - use absolute path
script_dir = FilePath(os.path.dirname(os.path.abspath(__file__)))
project_root = script_dir.parent  # Go up one level from the script directory
output_dir = project_root / "images" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

# Set up the figure with transparent background
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# Define vibrant colors that work extremely well on dark backgrounds
colors = {
    'intro': '#38B0DE',            # Bright Blue
    'building_blocks': '#3CB371',  # Medium Sea Green (brighter)
    'architecture': '#1E90FF',     # Dodger Blue (brighter)
    'tools': '#9370DB',            # Medium Purple (brighter)
    'memory': '#FF7F50',           # Coral (brighter orange)
    'multi_agent': '#FF5349',      # Red-Orange (brighter red)
    'case_study': '#20B2AA',       # Light Sea Green (brighter teal)
    'text': '#FFFFFF',             # Pure White
    'outline': '#000000',          # Pure Black
    'arrow': '#FFFFFF',            # White for arrows
    'bg': 'none',                  # Transparent background
    'text_shadow': '#000000'       # Shadow for text
}

# Stronger text effects for better visibility on dark backgrounds
text_effects = [
    withStroke(linewidth=4, foreground=colors['text_shadow'])
]

# Function to create chapter box with enhanced styling for visibility
def create_chapter_box(x, y, width, height, title, number, details, color):
    # Add thicker white outline for better visibility
    outline = patches.FancyBboxPatch(
        (x-0.08, y-0.08), width+0.16, height+0.16,
        boxstyle="round,pad=0.4,rounding_size=0.2",
        fc='white', ec='white', alpha=1.0, zorder=3
    )
    ax.add_patch(outline)

    # Add the main box with thicker outline
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.4,rounding_size=0.2",
        fc=color, ec='white', alpha=1.0, linewidth=3, zorder=4
    )
    ax.add_patch(box)

    # Add chapter number - larger and more visible
    number_text = ax.text(
        x + 0.5, y + 0.5, f"Ch {number}",
        ha='center', va='center', color='white',
        fontsize=16, fontweight='bold'
    )
    number_text.set_path_effects(text_effects)

    # Add title - larger and more visible
    title_text = ax.text(
        x + width/2, y + height/2, title,
        ha='center', va='center', color='white',
        fontsize=14, fontweight='bold'
    )
    title_text.set_path_effects(text_effects)

    # Add details - more visible
    details_text = ax.text(
        x + width/2, y + height - 0.8, details,
        ha='center', va='center', color='white',
        fontsize=11, style='italic'
    )
    details_text.set_path_effects(text_effects)

    return box

# Define the chapters with improved positioning
chapters = [
    {
        'x': 1, 'y': 6, 'width': 3.2, 'height': 1.6,  # Slightly larger
        'title': "Introduction",
        'number': 0,
        'details': "Purpose and approach",
        'color': colors['intro']
    },
    {
        'x': 2, 'y': 4, 'width': 3.2, 'height': 1.6,
        'title': "Building Blocks",
        'number': 1,
        'details': "Foundational agent components",
        'color': colors['building_blocks']
    },
    {
        'x': 5.5, 'y': 4, 'width': 3.2, 'height': 1.6,
        'title': "Core Architecture",
        'number': 2,
        'details': "Structural patterns",
        'color': colors['architecture']
    },
    {
        'x': 9, 'y': 4, 'width': 3.2, 'height': 1.6,
        'title': "Tool Integration",
        'number': 3,
        'details': "Connecting agents to tools",
        'color': colors['tools']
    },
    {
        'x': 3.5, 'y': 2, 'width': 3.2, 'height': 1.6,
        'title': "Memory Patterns",
        'number': 4,
        'details': "State and persistence",
        'color': colors['memory']
    },
    {
        'x': 7.5, 'y': 2, 'width': 3.2, 'height': 1.6,
        'title': "Multi-Agent Systems",
        'number': 5,
        'details': "Agent collaboration patterns",
        'color': colors['multi_agent']
    },
    {
        'x': 5.5, 'y': 0, 'width': 3.2, 'height': 1.6,
        'title': "Case Studies",
        'number': 6,
        'details': "Real-world implementations",
        'color': colors['case_study']
    }
]

# Draw all chapter boxes
for chapter in chapters:
    create_chapter_box(
        chapter['x'], chapter['y'], chapter['width'], chapter['height'],
        chapter['title'], chapter['number'], chapter['details'], chapter['color']
    )

# Define connection arrows with enhanced visibility
connections = [
    # From Introduction to Building Blocks
    {'start': (2.5, 6), 'end': (3.5, 5.5), 'start_chapter': 0, 'end_chapter': 1},
    # From Building Blocks to Core Architecture
    {'start': (5, 4.75), 'end': (5.5, 4.75), 'start_chapter': 1, 'end_chapter': 2},
    # From Core Architecture to Tool Integration
    {'start': (8.5, 4.75), 'end': (9, 4.75), 'start_chapter': 2, 'end_chapter': 3},
    # From Building Blocks to Memory Patterns
    {'start': (3.5, 4), 'end': (4, 3.5), 'start_chapter': 1, 'end_chapter': 4},
    # From Core Architecture to Memory Patterns
    {'start': (5.5, 4), 'end': (5, 3.5), 'start_chapter': 2, 'end_chapter': 4},
    # From Tool Integration to Multi-Agent Systems
    {'start': (9, 4), 'end': (8.5, 3.5), 'start_chapter': 3, 'end_chapter': 5},
    # From Memory Patterns to Multi-Agent Systems
    {'start': (6.5, 2.75), 'end': (7.5, 2.75), 'start_chapter': 4, 'end_chapter': 5},
    # From Memory Patterns to Case Studies
    {'start': (5, 2), 'end': (5.5, 1.5), 'start_chapter': 4, 'end_chapter': 6},
    # From Multi-Agent Systems to Case Studies
    {'start': (8, 2), 'end': (8.5, 1.5), 'start_chapter': 5, 'end_chapter': 6}
]

# Draw connections with improved visibility
for connection in connections:
    start_color = chapters[connection['start_chapter']]['color']
    end_color = chapters[connection['end_chapter']]['color']

    # Draw arrow with white outline for better visibility on dark backgrounds
    # First draw a thicker black outline
    outline_arrow = patches.FancyArrowPatch(
        connection['start'], connection['end'],
        connectionstyle="arc3,rad=0.1",
        arrowstyle="simple,head_width=12,head_length=12",
        fc='black', ec='black',
        linewidth=5, alpha=1.0, zorder=1
    )
    ax.add_patch(outline_arrow)

    # Then draw the colored arrow on top
    arrow = patches.FancyArrowPatch(
        connection['start'], connection['end'],
        connectionstyle="arc3,rad=0.1",
        arrowstyle="simple,head_width=10,head_length=10",
        fc=end_color, ec='white',
        linewidth=3, alpha=1.0, zorder=2
    )
    ax.add_patch(arrow)

# Add title with enhanced visibility
title_text = ax.text(
    6, 7.5, "AI Agent Design Patterns - Chapter Overview",
    ha='center', va='center', color=colors['text'],
    fontsize=20, fontweight='bold'
)
title_text.set_path_effects(text_effects)

# Add clearer legend for chapter progression
legend_x = 0.5
legend_y = 0.5

# Add a background box for the legend
legend_box = patches.FancyBboxPatch(
    (legend_x - 0.3, legend_y - 0.6), 3.2, 1.2,
    boxstyle="round,pad=0.3,rounding_size=0.2",
    fc='black', ec='white', alpha=0.7, linewidth=2, zorder=3
)
ax.add_patch(legend_box)

# Add legend text with enhanced visibility
legend_title = ax.text(
    legend_x, legend_y + 0.3, "Chapter Flow:",
    ha='left', va='center', color=colors['text'],
    fontsize=12, fontweight='bold'
)
legend_title.set_path_effects(text_effects)

legend_text = ax.text(
    legend_x, legend_y - 0.1,
    "→ Read in sequence\n→ Reference as needed",
    ha='left', va='center', color=colors['text'],
    fontsize=11
)
legend_text.set_path_effects(text_effects)

# Set the axis limits
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)

# Remove the axes
ax.axis('off')

# Save the image
output_path = output_dir / 'book_chapter_overview.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
print(f"Image saved to {output_path}")