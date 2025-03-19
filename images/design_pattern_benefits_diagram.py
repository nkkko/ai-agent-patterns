#!/usr/bin/env python3
"""
Generate Design Pattern Benefits Diagram for AI Agent Design Patterns book.

This image illustrates the key benefits of using established design patterns
for AI agent development for Chapter 0: Introduction.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import os
import math
from matplotlib.patheffects import withStroke

# Create output directory if it doesn't exist - use absolute path
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = script_dir.parent  # Go up one level from the script directory
output_dir = project_root / "images" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

# Set up the figure with transparent background
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'
fig, ax = plt.subplots(figsize=(12, 9))  # Slightly taller figure for better spacing
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# Define vibrant colors optimized for dark backgrounds
colors = {
    'primary': '#38B0DE',      # Bright Blue
    'secondary': '#50C878',    # Emerald Green
    'accent': '#FF5349',       # Vivid Red
    'highlight': '#FFD700',    # Gold
    'purple': '#BF5FFF',       # Bright Purple
    'neutral': '#F5F5F5',      # Bright White
    'text': '#FFFFFF',         # Pure White
    'text_shadow': '#000000'   # Pure Black
}

# Stronger text effects for better visibility
text_effects = [
    withStroke(linewidth=4, foreground=colors['text_shadow'])
]

# Create a central "Design Patterns" node
center_x, center_y = 6, 4.5  # Centered more in the figure
center_radius = 1.7

# Main center circle with white outline
center_outline = plt.Circle((center_x, center_y), center_radius + 0.08,
                          fc='white', ec='white', alpha=1.0, zorder=4)
ax.add_patch(center_outline)

center = plt.Circle((center_x, center_y), center_radius,
                   fc=colors['primary'], ec='white',
                   linewidth=3, alpha=1.0, zorder=5)
ax.add_patch(center)

# Central text
central_text = ax.text(center_x, center_y, "AI Agent\nDesign\nPatterns",
                      ha='center', va='center', color='white',
                      fontsize=18, fontweight='bold')  # Larger text
central_text.set_path_effects(text_effects)

# Define benefits with better positions for readability
benefits = [
    {
        'label': "Reusability",
        'description': "Proven solutions that can be\nreused across projects",
        'color': colors['secondary'],
        'angle': 45,
        'distance': 3.6  # Increased distance
    },
    {
        'label': "Maintainability",
        'description': "Structured approach leads to\neasier code maintenance",
        'color': colors['accent'],
        'angle': 90,
        'distance': 3.6
    },
    {
        'label': "Reliability",
        'description': "Tested patterns lead to\nmore reliable systems",
        'color': colors['purple'],
        'angle': 135,
        'distance': 3.6
    },
    {
        'label': "Scalability",
        'description': "Patterns that support\ngrowth and complexity",
        'color': colors['highlight'],
        'angle': 225,
        'distance': 3.6
    },
    {
        'label': "Collaboration",
        'description': "Common vocabulary for\nteam communication",
        'color': colors['purple'],
        'angle': 270,
        'distance': 3.6
    },
    {
        'label': "Flexibility",
        'description': "Adaptable solutions for\nvarying requirements",
        'color': colors['secondary'],
        'angle': 315,
        'distance': 3.6
    }
]

# Helper function to calculate position
def calc_position(angle_deg, distance):
    angle_rad = math.radians(angle_deg)
    x = center_x + distance * math.cos(angle_rad)
    y = center_y + distance * math.sin(angle_rad)
    return x, y

# Draw connecting lines first (behind everything else)
for benefit in benefits:
    x, y = calc_position(benefit['angle'], benefit['distance'])

    # Connect with thicker white line with black outline
    line = plt.Line2D([center_x, x], [center_y, y],
                     color='white', linewidth=2.5, alpha=0.9, zorder=1,
                     path_effects=[withStroke(linewidth=4, foreground='black')])
    ax.add_line(line)

# Now draw nodes and text
for benefit in benefits:
    x, y = calc_position(benefit['angle'], benefit['distance'])
    node_radius = 1.0  # Slightly smaller nodes

    # White outline for better visibility
    outline = plt.Circle((x, y), node_radius + 0.08,
                        fc='white', ec='white', alpha=1.0, zorder=4)
    ax.add_patch(outline)

    # Add benefit node
    node = plt.Circle((x, y), node_radius,
                     fc=benefit['color'], ec='white',
                     linewidth=2.5, alpha=1.0, zorder=5)
    ax.add_patch(node)

    # Small connection points that are less visually dominant
    # Only add one connection point at each end for simplicity
    conn1 = plt.Circle((center_x + (x-center_x)*0.2, center_y + (y-center_y)*0.2),
                      0.12, fc=benefit['color'], ec='white',
                      linewidth=1.5, alpha=0.9, zorder=6)
    ax.add_patch(conn1)

    conn2 = plt.Circle((center_x + (x-center_x)*0.8, center_y + (y-center_y)*0.8),
                      0.12, fc=benefit['color'], ec='white',
                      linewidth=1.5, alpha=0.9, zorder=6)
    ax.add_patch(conn2)

    # Label background with rounded corners
    label_bg = patches.FancyBboxPatch(
        (x - node_radius*0.9, y - 0.2), node_radius*1.8, 0.4,
        boxstyle="round,pad=0.2,rounding_size=0.2",
        fc='black', ec=benefit['color'], alpha=0.7, linewidth=2, zorder=6
    )
    ax.add_patch(label_bg)

    # Add benefit label centered in node
    label_text = ax.text(x, y, benefit['label'],
                        ha='center', va='center',
                        color='white', fontsize=14, fontweight='bold',
                        zorder=7)
    label_text.set_path_effects(text_effects)

    # Calculate optimized description position to avoid line overlaps
    # We'll place descriptions farther out and offset based on angle
    desc_radius = node_radius + 2.0

    # Fine-tuned positions for each description to avoid overlaps
    desc_offset_angles = {
        45: -10,    # Reusability (slightly counterclockwise)
        90: 0,      # Maintainability (directly outward)
        135: 10,    # Reliability (slightly clockwise)
        225: -10,   # Scalability (slightly counterclockwise)
        270: 0,     # Collaboration (directly outward)
        315: 10     # Flexibility (slightly clockwise)
    }

    offset_angle = benefit['angle'] + desc_offset_angles.get(benefit['angle'], 0)
    desc_x = x + desc_radius * math.cos(math.radians(offset_angle))
    desc_y = y + desc_radius * math.sin(math.radians(offset_angle))

    # Custom size each description box based on content
    desc_lines = benefit['description'].count('\n') + 1
    desc_width = 3.2
    desc_height = 0.3 + (desc_lines * 0.25)

    # Add connecting line from node to description box for clarity
    desc_conn = plt.Line2D([x + node_radius*math.cos(math.radians(offset_angle)),
                           desc_x - 0.5*math.cos(math.radians(offset_angle))],
                          [y + node_radius*math.sin(math.radians(offset_angle)),
                           desc_y - 0.5*math.sin(math.radians(offset_angle))],
                          color='white', linewidth=1.5, alpha=0.6, zorder=5,
                          linestyle='--')
    ax.add_line(desc_conn)

    # Description background with matching color
    desc_bg = patches.FancyBboxPatch(
        (desc_x - desc_width/2, desc_y - desc_height/2), desc_width, desc_height,
        boxstyle="round,pad=0.3,rounding_size=0.2",
        fc=benefit['color'], ec='white', alpha=0.8, linewidth=1.5, zorder=6
    )
    ax.add_patch(desc_bg)

    # Add description text
    desc_text = ax.text(desc_x, desc_y, benefit['description'],
                       ha='center', va='center', color='white',
                       fontsize=11, style='italic', zorder=7)
    desc_text.set_path_effects(text_effects)

# Add title
title_text = ax.text(6, 8.2, "Benefits of AI Agent Design Patterns",
                    ha='center', va='center', color=colors['text'],
                    fontsize=22, fontweight='bold')
title_text.set_path_effects(text_effects)

# Add subtitle with better proportions
subtitle_width = 10  # Wider background
subtitle_bg = patches.FancyBboxPatch(
    (center_x - subtitle_width/2, 7.5), subtitle_width, 0.6,
    boxstyle="round,pad=0.3,rounding_size=0.2",
    fc='black', ec='white', alpha=0.7, linewidth=1.5, zorder=6
)
ax.add_patch(subtitle_bg)

subtitle_text = ax.text(center_x, 7.8,
                       "Established patterns provide numerous advantages for agent development",
                       ha='center', va='center', color=colors['text'],
                       fontsize=14, zorder=7)
subtitle_text.set_path_effects(text_effects)

# Set the axis limits with more margin
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)

# Remove the axes
ax.axis('off')

# Save the image
output_path = output_dir / 'design_pattern_benefits_diagram.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
print(f"Image saved to {output_path}")