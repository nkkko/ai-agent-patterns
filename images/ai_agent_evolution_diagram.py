#!/usr/bin/env python3
"""
Generate AI Agent Evolution Diagram for AI Agent Design Patterns book.

This image illustrates the evolution of AI agents and how design patterns
in the book address each stage of development for Chapter 0: Introduction.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from pathlib import Path as FilePath
import os
from matplotlib.patheffects import withStroke, Stroke

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

# Define colors with good contrast that work well on dark backgrounds
colors = {
    'primary': '#3498db',     # Blue - brighter
    'secondary': '#2ecc71',   # Green - brighter
    'accent': '#e74c3c',      # Red - brighter
    'neutral': '#ecf0f1',     # Light Gray - almost white
    'text': '#ffffff',        # Pure white
    'highlight': '#f39c12',   # Orange
    'outline': 'black',       # Black for outlines
    'background': 'none'
}

# Path effects for text to make it visible on any background
text_effects = [
    withStroke(linewidth=3, foreground='black')
]

# Draw a timeline arrow
arrow_length = 9
arrow_y = 4
head_width = 0.2
head_length = 0.3

# Draw the main arrow - make it brighter and with outline
timeline_arrow = ax.arrow(1, arrow_y, arrow_length, 0,
                          head_width=head_width, head_length=head_length,
                          fc=colors['primary'], ec='white',
                          linewidth=3, length_includes_head=True,
                          zorder=2)

# Evolution stages - with brighter colors
stages = [
    {'x': 1.5, 'label': 'Simple\nAutomation', 'color': colors['primary']},
    {'x': 3.5, 'label': 'Basic LLM-based\nAgents',
     'color': colors['secondary']},
    {'x': 5.5, 'label': 'Tool-integrated\nAgents',
     'color': colors['secondary']},
    {'x': 7.5, 'label': 'Multi-agent\nSystems', 'color': colors['accent']},
    {'x': 9.5, 'label': 'Future\nEvolution', 'color': colors['highlight']}
]

# Add circles and labels for each stage
circle_radius = 0.3
for stage in stages:
    # Add white outline to circles
    outline = plt.Circle((stage['x'], arrow_y), circle_radius + 0.02,
                         fc='white', ec='white', alpha=1.0, zorder=4)
    ax.add_patch(outline)

    # Add the circle
    circle = plt.Circle((stage['x'], arrow_y), circle_radius,
                        fc=stage['color'], ec='white', alpha=1.0,
                        zorder=5, linewidth=1.5)
    ax.add_patch(circle)

    # Add stage label below with enhanced visibility
    stage_text = ax.text(stage['x'], arrow_y - circle_radius - 0.4,
                         stage['label'],
                         ha='center', va='top', fontsize=11,
                         fontweight='bold',
                         color=stage['color'], wrap=True)
    stage_text.set_path_effects(text_effects)

# Add timeline label with enhanced visibility
timeline_text = ax.text(5.5, arrow_y + 0.7, 'Evolution of AI Agents',
                        ha='center', va='center', fontsize=14,
                        fontweight='bold',
                        color=colors['text'])
timeline_text.set_path_effects(text_effects)

# Add year markers with enhanced visibility
years = ['2020', '2021', '2022', '2023', 'Beyond']
for i, year in enumerate(years):
    x_pos = 1.5 + 2 * i
    year_text = ax.text(x_pos, arrow_y + 0.3, year,
                        ha='center', va='bottom', fontsize=10,
                        color=colors['neutral'])
    year_text.set_path_effects(text_effects)

# Draw book coverage area
coverage_start = 1.2
coverage_end = 8.0
coverage_height = 2.5
coverage_y = arrow_y - 1.3

# Create a semi-transparent colored area with more visible outline
rect = patches.Rectangle(
    (coverage_start, coverage_y),
    coverage_end - coverage_start, coverage_height,
    linewidth=3, edgecolor=colors['text'],
    facecolor=colors['primary'], alpha=0.15,
    linestyle='--', zorder=1
)
ax.add_patch(rect)

# Add book coverage label with enhanced visibility
coverage_text = ax.text(
    (coverage_start + coverage_end) / 2,
    coverage_y + coverage_height / 2,
    "Book's Design Pattern Coverage",
    ha='center', va='center', fontsize=14, fontweight='bold',
    color=colors['text']
)
coverage_text.set_path_effects(text_effects)

# Add pattern bubbles within the coverage area - with better contrast
patterns = [
    {'x': 2.0, 'y': coverage_y + 0.6, 'label': 'Building\nBlocks',
     'color': colors['primary']},
    {'x': 3.5, 'y': coverage_y + 1.5, 'label': 'Core\nArchitecture',
     'color': colors['primary']},
    {'x': 5.0, 'y': coverage_y + 0.8, 'label': 'Tool\nIntegration',
     'color': colors['secondary']},
    {'x': 6.5, 'y': coverage_y + 1.7, 'label': 'Memory\nPatterns',
     'color': colors['secondary']},
    {'x': 7.5, 'y': coverage_y + 0.7, 'label': 'Multi-agent\nPatterns',
     'color': colors['accent']}
]

# Add pattern bubbles with outlines
bubble_radius = 0.5
for pattern in patterns:
    # Add white outline
    outline = plt.Circle((pattern['x'], pattern['y']), bubble_radius + 0.02,
                         fc='white', ec='white', alpha=1.0, zorder=3)
    ax.add_patch(outline)

    # Add the bubble
    bubble = plt.Circle((pattern['x'], pattern['y']), bubble_radius,
                        fc=pattern['color'], ec='white', alpha=0.9,
                        zorder=4, linewidth=1.5)
    ax.add_patch(bubble)

    # Add pattern label with enhanced visibility
    pattern_text = ax.text(pattern['x'], pattern['y'], pattern['label'],
                           ha='center', va='center', fontsize=9,
                           fontweight='bold',
                           color='white')
    pattern_text.set_path_effects([withStroke(linewidth=2,
                                             foreground='black')])

# Add practical focus callout with better visibility
callout_x = 10
callout_y = coverage_y + coverage_height / 2
callout_width = 1.5
callout_height = 1.5

# Create callout box with white background and border
callout = patches.FancyBboxPatch(
    (callout_x - callout_width/2, callout_y - callout_height/2),
    callout_width, callout_height,
    boxstyle="round,pad=0.3,rounding_size=0.2",
    fc='white', ec=colors['highlight'], alpha=0.9,
    linewidth=3, zorder=6
)
ax.add_patch(callout)

# Add callout text
callout_text = ax.text(callout_x, callout_y,
                       "Practical\nImplementation\nFocus",
                       ha='center', va='center', fontsize=10,
                       fontweight='bold',
                       color='black')

# Add arrow from callout to coverage area - make it more visible
arrow = patches.FancyArrowPatch(
    (callout_x - callout_width/2, callout_y),
    (coverage_end + 0.1, callout_y),
    connectionstyle="arc3,rad=-0.2",
    arrowstyle="simple,head_width=10,head_length=10",
    fc=colors['highlight'], ec='white',
    linewidth=3, zorder=3
)
ax.add_patch(arrow)

# Set the axis limits
ax.set_xlim(0, 12)
ax.set_ylim(1, 7)

# Remove the axes
ax.axis('off')

# Add title with enhanced visibility
title_text = ax.text(6, 6.5, "AI Agent Design Patterns - Evolution Coverage",
                     ha='center', va='center', color=colors['text'],
                     fontsize=16, fontweight='bold')
title_text.set_path_effects(text_effects)

# Save the image
output_path = output_dir / 'ai_agent_evolution_diagram.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
print(f"Image saved to {output_path}")