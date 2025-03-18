#!/usr/bin/env python3
"""
Generate book cover image for AI Agent Design Patterns book.

This script creates a professional book cover in O'Reilly style with title,
authors, and a Python-related illustration.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib import patheffects
from pathlib import Path as FilePath
import random

# Create output directory if it doesn't exist
output_dir = FilePath("images/generated")
output_dir.mkdir(parents=True, exist_ok=True)

# Configuration
WIDTH, HEIGHT = 2400, 3200  # Standard book cover ratio (3:4)
DPI = 300
TITLE = "AI Agent\nDesign Patterns"
AUTHORS = "Nikola Balić & Ivan Burazin"
OREILLY_RED = "#a42239"  # Classic O'Reilly red
WHITE = "#ffffff"
BLACK = "#000000"
PYTHON_BLUE = "#4584b6"
PYTHON_YELLOW = "#ffde57"
AI_BLUE = "#58A6FF"
SHADOW_COLOR = (0, 0, 0, 0.3)  # Shadow as RGBA tuple
SUBTITLE = "A Guide to Building Effective AI Systems"

# Set up the figure with a specific size for book cover
fig = plt.figure(figsize=(WIDTH/DPI, HEIGHT/DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])  # Fill the entire figure

# Create a white background
ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=WHITE,
             edgecolor='none', zorder=-1, transform=ax.transAxes))

# Draw the O'Reilly style red band across the top portion
ax.add_patch(Rectangle((0, 0.65), 1, 0.35, facecolor=OREILLY_RED,
             edgecolor='none', zorder=0, transform=ax.transAxes))

# Function to draw a Python snake intertwined with AI network
def draw_python_ai_illustration():
    # Center of the illustration
    center_x = 0.5
    center_y = 0.35

    # Draw a coiled Python snake
    segments = 20
    snake_points = []
    radius = 0.12
    inner_radius = 0.03

    # Create a spiral for the snake body
    for i in range(segments):
        angle = i * 2 * np.pi / (segments - 1)
        r = radius - (radius - inner_radius) * i / segments
        x = center_x + r * np.cos(angle)
        y = center_y + r * np.sin(angle)
        snake_points.append((x, y))

    # Draw segments of the snake
    for i in range(len(snake_points) - 1):
        start = snake_points[i]
        end = snake_points[i + 1]

        # Calculate thickness vectors
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = np.sqrt(dx*dx + dy*dy)

        if length > 0:
            # Perpendicular vector for thickness
            perpx = -dy / length * 0.02
            perpy = dx / length * 0.02
        else:
            perpx, perpy = 0, 0.02

        # Create polygon points for the segment
        poly_points = [
            (start[0] + perpx, start[1] + perpy),
            (start[0] - perpx, start[1] - perpy),
            (end[0] - perpx, end[1] - perpy),
            (end[0] + perpx, end[1] + perpy)
        ]

        # Alternate colors
        color = PYTHON_BLUE if i % 2 == 0 else PYTHON_YELLOW

        # Draw the segment
        segment = Polygon(poly_points, closed=True, facecolor=color,
                          edgecolor=BLACK, linewidth=0.5, zorder=5)
        ax.add_patch(segment)

    # Add snake head
    head_x, head_y = snake_points[0]
    head_radius = 0.025
    head = Circle((head_x, head_y), head_radius, facecolor=PYTHON_BLUE,
                  edgecolor=BLACK, linewidth=0.5, zorder=6)
    ax.add_patch(head)

    # Add eyes to the snake
    eye_size = head_radius * 0.3
    eye1 = Circle((head_x + head_radius * 0.5, head_y + head_radius * 0.3),
                  eye_size, facecolor=BLACK, zorder=7)
    eye2 = Circle((head_x + head_radius * 0.5, head_y - head_radius * 0.3),
                  eye_size, facecolor=BLACK, zorder=7)
    ax.add_patch(eye1)
    ax.add_patch(eye2)

    # Add AI network nodes around the snake
    num_nodes = 12
    nodes = []

    # Create nodes
    for _ in range(num_nodes):
        angle = random.uniform(0, 2 * np.pi)
        r = random.uniform(0.17, 0.25)
        x = center_x + r * np.cos(angle)
        y = center_y + r * np.sin(angle)
        size = random.uniform(0.01, 0.015)
        nodes.append((x, y, size))

    # Draw nodes
    for x, y, size in nodes:
        # Add glow effect
        for i in range(3):
            alpha = 0.3 - i * 0.1
            s = size + i * 0.004
            glow = Circle((x, y), s, facecolor=AI_BLUE, alpha=alpha, zorder=3)
            ax.add_patch(glow)

        # Draw main node
        node = Circle((x, y), size, facecolor=AI_BLUE,
                      edgecolor=WHITE, linewidth=0.5, zorder=4)
        ax.add_patch(node)

    # Connect nodes
    for i in range(len(nodes)):
        # Connect to 2-3 other nodes
        connections = random.randint(2, 3)
        connected = []

        for _ in range(connections):
            j = random.randint(0, len(nodes) - 1)
            if j != i and j not in connected:
                connected.append(j)

                x1, y1, _ = nodes[i]
                x2, y2, _ = nodes[j]

                # Create glowing connection line
                for k in range(2):
                    alpha = 0.4 - k * 0.2
                    lw = 0.5 - k * 0.2
                    line = plt.Line2D([x1, x2], [y1, y2], lw=lw, alpha=alpha,
                                     color=AI_BLUE, zorder=2)
                    ax.add_line(line)

# Draw the Python and AI illustration
draw_python_ai_illustration()

# Add title with O'Reilly style
title_props = {'fontsize': 60, 'fontweight': 'bold', 'color': WHITE,
               'ha': 'left', 'va': 'center', 'family': 'sans-serif'}
title_text = ax.text(0.08, 0.82, TITLE, **title_props, transform=ax.transAxes)

# Add shadow effect to title
title_text.set_path_effects([
    patheffects.withStroke(linewidth=2, foreground=SHADOW_COLOR)
])

# Add subtitle in the white area
subtitle_props = {'fontsize': 28, 'color': BLACK, 'fontweight': 'normal',
                  'ha': 'left', 'va': 'center', 'family': 'sans-serif'}
ax.text(0.08, 0.58, SUBTITLE, **subtitle_props, transform=ax.transAxes)

# Add authors
author_props = {'fontsize': 20, 'color': BLACK, 'fontweight': 'normal',
                'ha': 'left', 'va': 'center', 'family': 'sans-serif'}
ax.text(0.08, 0.52, AUTHORS, **author_props, transform=ax.transAxes)

# Add O'Reilly logo text
logo_props = {'fontsize': 18, 'color': BLACK, 'fontweight': 'bold',
              'ha': 'right', 'va': 'top', 'family': 'serif'}

# Add a thin line below the red section
ax.axhline(y=0.65, xmin=0, xmax=1, color=BLACK, linewidth=1, zorder=10)

# Add text at the bottom
bottom_text_props = {'fontsize': 14, 'color': BLACK, 'alpha': 0.7,
                     'ha': 'center', 'va': 'center', 'family': 'sans-serif'}
ax.text(0.5, 0.06, "Design scalable and reliable AI agent systems",
        **bottom_text_props, transform=ax.transAxes)

# Remove all axes
ax.axis('off')

# Save the image
output_path = output_dir / "book_cover.png"
plt.savefig(output_path, dpi=DPI, bbox_inches='tight', pad_inches=0)
print(f"Cover image saved to {output_path}")

# Close the figure to free memory
plt.close(fig)