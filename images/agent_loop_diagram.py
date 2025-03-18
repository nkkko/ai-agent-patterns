#!/usr/bin/env python3
"""
Generate Agent Loop Diagram for AI Agent Design Patterns book.

This image illustrates the fundamental agent loop concept for Chapter 1: Building Blocks of Software Agents.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import matplotlib.patches as patches
import os

# Determine the correct output directory based on the script's location
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
if script_dir.name == 'images':
    # Script is already in the images directory, so generated should be a sibling directory
    output_dir = script_dir / "generated"
else:
    # Script is in the root directory
    output_dir = script_dir / "images" / "generated"

# Create output directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Set consistent style for book images
# Using updated style name for compatibility with newer matplotlib versions
try:
    plt.style.use('seaborn-v0_8-whitegrid')  # For newer matplotlib versions
except OSError:
    try:
        plt.style.use('seaborn-whitegrid')  # For older matplotlib versions
    except OSError:
        print("Using default style as seaborn styles aren't available")

fig, ax = plt.subplots(figsize=(10, 6))  # Book-friendly dimensions

# Turn off axis
ax.axis('off')

# Define colors
observe_color = "#4285F4"  # Google Blue
think_color = "#FBBC05"    # Google Yellow
act_color = "#34A853"      # Google Green
bg_color = "#F8F9FA"       # Light gray background
arrow_color = "#5F6368"    # Dark gray for arrows

# Set background color
ax.set_facecolor(bg_color)
fig.patch.set_facecolor(bg_color)

# Define node positions
center = np.array([5, 3])
radius = 2
angles = np.array([90, 210, 330]) * np.pi / 180  # in radians
positions = {
    'Observe': center + radius * np.array([np.cos(angles[0]), np.sin(angles[0])]),
    'Think': center + radius * np.array([np.cos(angles[1]), np.sin(angles[1])]),
    'Act': center + radius * np.array([np.cos(angles[2]), np.sin(angles[2])])
}

# Draw the three main components
node_radius = 0.8
for label, pos in positions.items():
    color = observe_color if label == 'Observe' else think_color if label == 'Think' else act_color
    circle = plt.Circle(pos, node_radius, color=color, alpha=0.8, zorder=10)
    ax.add_patch(circle)
    ax.text(pos[0], pos[1], label, fontsize=14, ha='center', va='center',
            color='white', fontweight='bold', zorder=11)

# Draw curved arrows connecting the components
arrow_properties = {
    'width': 0.1,
    'head_width': 0.3,
    'head_length': 0.3,
    'fc': arrow_color,
    'ec': arrow_color,
    'zorder': 5
}

# Helper function to compute control points for curved arrows
def get_control_points(start, end):
    mid = (start + end) / 2
    vec = end - start
    perp = np.array([-vec[1], vec[0]])  # Perpendicular vector
    ctrl = mid + 0.5 * perp / np.linalg.norm(perp)
    return ctrl

# Draw arrows connecting the main components
component_pairs = [
    ('Observe', 'Think'),
    ('Think', 'Act'),
    ('Act', 'Observe')
]

for start_label, end_label in component_pairs:
    start_pos = positions[start_label]
    end_pos = positions[end_label]

    # Adjust start and end points to be on the edge of circles
    dir_vec = end_pos - start_pos
    dir_vec = dir_vec / np.linalg.norm(dir_vec)

    start_adj = start_pos + dir_vec * node_radius
    end_adj = end_pos - dir_vec * node_radius

    # Create curved path using control point
    ctrl_point = get_control_points(start_adj, end_adj)

    # Create curved path using Bezier curve
    t = np.linspace(0, 1, 100)
    bezier_x = (1-t)**2 * start_adj[0] + 2*(1-t)*t*ctrl_point[0] + t**2 * end_adj[0]
    bezier_y = (1-t)**2 * start_adj[1] + 2*(1-t)*t*ctrl_point[1] + t**2 * end_adj[1]

    # Plot the path
    ax.plot(bezier_x, bezier_y, color=arrow_color, linewidth=2, zorder=5)

    # Add arrowhead
    arrow_idx = 80  # Position along the curve for arrowhead (0-99)
    arrow_dir = np.array([bezier_x[arrow_idx+1] - bezier_x[arrow_idx-1],
                          bezier_y[arrow_idx+1] - bezier_y[arrow_idx-1]])
    arrow_dir = arrow_dir / np.linalg.norm(arrow_dir)

    ax.arrow(bezier_x[arrow_idx], bezier_y[arrow_idx],
             arrow_dir[0]*0.2, arrow_dir[1]*0.2, **arrow_properties)

# Add subcomponents
subcomponents = {
    'Observe': ['User Input', 'Environment State'],
    'Think': ['Reasoning', 'Planning'],
    'Act': ['Execute Tool', 'Generate Response']
}

for main_comp, sub_comps in subcomponents.items():
    main_pos = positions[main_comp]

    # Draw a box around the subcomponents
    box_width, box_height = 2.8, 1.2
    box_x = main_pos[0] - box_width/2
    box_y = main_pos[1] - 2.2  # Position below main component

    rect = patches.Rectangle((box_x, box_y), box_width, box_height,
                            linewidth=1, edgecolor='gray', facecolor='white',
                            alpha=0.8, zorder=1)
    ax.add_patch(rect)

    # Add label for the subcomponent group
    ax.text(main_pos[0], box_y + box_height + 0.1, f"{main_comp} Components",
            fontsize=10, ha='center', va='bottom', color='gray')

    # Add subcomponents within the box
    for i, sub_comp in enumerate(sub_comps):
        sub_x = box_x + (i+0.5) * (box_width / len(sub_comps))
        sub_y = box_y + box_height/2

        # Draw subcomponent
        main_color = observe_color if main_comp == 'Observe' else think_color if main_comp == 'Think' else act_color
        sub_circle = plt.Circle((sub_x, sub_y), 0.3, color=main_color, alpha=0.4, zorder=2)
        ax.add_patch(sub_circle)

        # Add subcomponent label
        ax.text(sub_x, sub_y, sub_comp, fontsize=8, ha='center', va='center', zorder=3)

    # Draw a line connecting the main component to its subcomponents
    ax.plot([main_pos[0], main_pos[0]], [main_pos[1]-node_radius, box_y+box_height],
            color='gray', linestyle='--', alpha=0.8, zorder=0)

# Set equal aspect ratio to ensure circles look round
ax.set_aspect('equal')

# Ensure the diagram fits well in the figure
plt.tight_layout()

# Save the image
output_path = output_dir / 'agent_loop_diagram.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Image saved to {output_path}")

# Display the image (comment out when not needed)
# plt.show()