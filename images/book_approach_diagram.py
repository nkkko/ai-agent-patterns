#!/usr/bin/env python3
"""
Generate Book Approach Diagram for AI Agent Design Patterns book.

This image illustrates the book's approach focusing on practical implementation
patterns for immediate application for Chapter 0: Introduction.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch
from pathlib import Path
import matplotlib.colors as mcolors
import os
from matplotlib.patheffects import withStroke

# Create output directory if it doesn't exist - use absolute path
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = script_dir.parent  # Go up one level from the script directory
output_dir = project_root / "images" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

# Set up the figure with transparent background
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# Define colors with good contrast that work well on dark backgrounds
colors = {
    'primary': '#3498db',     # Blue - more saturated
    'secondary': '#2ecc71',   # Green - more saturated
    'accent': '#e74c3c',      # Red - more saturated
    'neutral': '#bdc3c7',     # Light Gray - brighter for dark backgrounds
    'text': '#ecf0f1',        # Almost White - for better visibility on dark
    'highlight': '#f39c12',   # Orange
    'outline': '#2c3e50',     # Dark blue/gray for outlines
    'text_shadow': 'black'    # Text shadow color
}

# Path effects for text to make it visible on any background
text_effects = [
    withStroke(linewidth=3, foreground=colors['text_shadow'])
]

# Function to create a fancy box with shadow and rounded corners
def create_fancy_box(x, y, width, height, color, label, fontsize=12, alpha=0.95):
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.5,rounding_size=0.2",
        fc=color, ec='white', alpha=alpha, zorder=2,
        linewidth=2
    )
    ax.add_patch(box)
    text = ax.text(x + width/2, y + height/2, label,
            ha='center', va='center', color='white',
            fontsize=fontsize, fontweight='bold', zorder=3)
    text.set_path_effects(text_effects)
    return box

# Draw the main book approach structure
# 1. Core foundation box (bottom)
foundation_width, foundation_height = 8, 1.5
foundation_x, foundation_y = 2, 1
create_fancy_box(
    foundation_x, foundation_y,
    foundation_width, foundation_height,
    colors['primary'],
    "Core Design Patterns Foundation",
    fontsize=14
)

# 2. Middle layer: Practical implementation examples
impl_blocks = [
    ("Agent Building\nBlocks", colors['secondary']),
    ("Architectural\nPatterns", colors['secondary']),
    ("Tool\nIntegration", colors['secondary']),
    ("Memory\nPatterns", colors['secondary'])
]

block_width = foundation_width / len(impl_blocks) - 0.2
block_height = 1.8
block_y = foundation_y + foundation_height + 0.5

for i, (label, color) in enumerate(impl_blocks):
    block_x = foundation_x + i * (block_width + 0.2)
    create_fancy_box(block_x, block_y, block_width, block_height, color, label)

# 3. Top layer: Advanced concepts
advanced_width, advanced_height = 6, 1.3
advanced_x = foundation_x + (foundation_width - advanced_width)/2
advanced_y = block_y + block_height + 0.5

advanced_box = create_fancy_box(
    advanced_x, advanced_y,
    advanced_width, advanced_height,
    colors['accent'],
    "Advanced Multi-Agent Patterns",
    fontsize=13
)

# 4. Future expansion box (dotted outline)
future_width, future_height = 9, 1.2
future_x = foundation_x + (foundation_width - future_width)/2
future_y = advanced_y + advanced_height + 0.5

future_box = FancyBboxPatch(
    (future_x, future_y), future_width, future_height,
    boxstyle="round,pad=0.5,rounding_size=0.2",
    fc='none', ec=colors['highlight'], alpha=1.0,
    linestyle='dashed', linewidth=3, zorder=2
)
ax.add_patch(future_box)
future_text = ax.text(future_x + future_width/2, future_y + future_height/2,
        "Future Expansion (Specialized Patterns)",
        ha='center', va='center', color=colors['highlight'],
        fontsize=13, fontweight='bold', zorder=3)
future_text.set_path_effects(text_effects)

# Add arrows connecting the layers - make them thicker and brighter
def add_arrow(x_start, y_start, x_end, y_end, color):
    arrow = FancyArrowPatch(
        (x_start, y_start), (x_end, y_end),
        connectionstyle="arc3,rad=0.1",
        arrowstyle="simple,head_width=10,head_length=10",
        fc=color, ec='white', alpha=1.0, linewidth=3, zorder=1
    )
    ax.add_patch(arrow)

# Connect foundation to implementation blocks
for i in range(len(impl_blocks)):
    block_x = foundation_x + i * (block_width + 0.2) + block_width/2
    add_arrow(
        block_x, foundation_y + foundation_height,
        block_x, block_y,
        colors['primary']
    )

# Connect implementation blocks to advanced concepts
for i in range(len(impl_blocks)):
    if i > 0 and i < len(impl_blocks) - 1:
        block_x = foundation_x + i * (block_width + 0.2) + block_width/2
        add_arrow(
            block_x, block_y + block_height,
            advanced_x + advanced_width/2, advanced_y,
            colors['secondary']
        )

# Connect advanced concepts to future expansion
add_arrow(
    advanced_x + advanced_width/2, advanced_y + advanced_height,
    future_x + future_width/2, future_y,
    colors['accent']
)

# Add "Practical Implementation Focus" brace and label
brace_y = 0.3
brace_width = foundation_width + 1
brace_height = advanced_y + advanced_height - foundation_y + 0.2
brace_x = foundation_x - 0.5

# Draw the left side of the brace - make it white for visibility
ax.plot([brace_x, brace_x - 0.3, brace_x, brace_x],
        [brace_y, brace_y + brace_height/2, brace_y + brace_height, brace_y + brace_height + 0.2],
        color='white', linewidth=3, zorder=1, path_effects=[withStroke(linewidth=5, foreground='black')])

# Add the label with better visibility
brace_text = ax.text(brace_x - 1.5, brace_y + brace_height/2, "Book's\nPractical\nImplementation\nFocus",
        ha='center', va='center', color=colors['text'],
        fontsize=12, fontweight='bold', rotation=90)
brace_text.set_path_effects(text_effects)

# Set the axis limits
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)

# Remove the axes
ax.axis('off')

# Add title with enhanced visibility
title_text = ax.text(6, 7.5, "AI Agent Design Patterns - Book Approach",
        ha='center', va='center', color=colors['text'],
        fontsize=16, fontweight='bold')
title_text.set_path_effects(text_effects)

# Save the image
output_path = output_dir / 'book_approach_diagram.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
print(f"Image saved to {output_path}")