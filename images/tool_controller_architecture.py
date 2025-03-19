#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Set up the image dimensions
WIDTH = 1200
HEIGHT = 800
PADDING = 60
BOX_HEIGHT = 100
BOX_WIDTH = 250
ARROW_WIDTH = 2
ARROW_HEAD_SIZE = 12
BOX_SPACING = 40

# Colors
PRIMARY_COLOR = (75, 0, 130)  # Deep Purple
SECONDARY_COLOR = (147, 112, 219)  # Medium Purple
HIGHLIGHT_COLOR = (255, 99, 71)  # Tomato
TEXT_COLOR = (255, 255, 255)  # White
BG_COLOR = (255, 255, 255)  # White
BORDER_COLOR = (124, 3, 120)  # Darker Purple

def create_rounded_rectangle(draw, xy, radius=10, fill=None, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.ellipse((x1, y1, x1 + radius * 2, y1 + radius * 2), fill=fill, outline=outline)
    draw.ellipse((x2 - radius * 2, y1, x2, y1 + radius * 2), fill=fill, outline=outline)
    draw.ellipse((x1, y2 - radius * 2, x1 + radius * 2, y2), fill=fill, outline=outline)
    draw.ellipse((x2 - radius * 2, y2 - radius * 2, x2, y2), fill=fill, outline=outline)
    draw.rectangle((x1 + radius, y1, x2 - radius, y2), fill=fill, outline=None)
    draw.rectangle((x1, y1 + radius, x2, y2 - radius), fill=fill, outline=None)
    if outline:
        draw.arc((x1, y1, x1 + radius * 2, y1 + radius * 2), 180, 270, fill=outline)
        draw.arc((x2 - radius * 2, y1, x2, y1 + radius * 2), 270, 360, fill=outline)
        draw.arc((x1, y2 - radius * 2, x1 + radius * 2, y2), 90, 180, fill=outline)
        draw.arc((x2 - radius * 2, y2 - radius * 2, x2, y2), 0, 90, fill=outline)
        draw.line((x1 + radius, y1, x2 - radius, y1), fill=outline, width=width)
        draw.line((x1 + radius, y2, x2 - radius, y2), fill=outline, width=width)
        draw.line((x1, y1 + radius, x1, y2 - radius), fill=outline, width=width)
        draw.line((x2, y1 + radius, x2, y2 - radius), fill=outline, width=width)

def draw_arrow(draw, start, end, width=ARROW_WIDTH, color=BORDER_COLOR, head_size=ARROW_HEAD_SIZE):
    """Draw an arrow from start to end points"""
    # Draw the line
    draw.line([start, end], fill=color, width=width)

    # Calculate the arrow head
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = np.sqrt(dx**2 + dy**2)
    dx, dy = dx / length, dy / length

    # Calculate perpendicular vector
    px, py = -dy, dx

    # Calculate the three points of the arrow head
    p1 = (end[0] - head_size * dx, end[1] - head_size * dy)
    p2 = (p1[0] + head_size * px, p1[1] + head_size * py)
    p3 = (p1[0] - head_size * px, p1[1] - head_size * py)

    # Draw the arrow head
    draw.polygon([end, p2, p3], fill=color)

def draw_text_centered(draw, position, text, font, fill=TEXT_COLOR):
    """Draw text centered at position"""
    text_width, text_height = draw.textlength(text, font=font), font.size
    draw.text((position[0] - text_width // 2, position[1] - text_height // 2), text, fill=fill, font=font)

def draw_multi_line_text(draw, position, text, font, fill=TEXT_COLOR, line_spacing=5, max_width=None):
    """Draw text with multiple lines if needed"""
    x, y = position
    if not max_width:
        draw.text((x, y), text, fill=fill, font=font)
        return

    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        test_width = draw.textlength(test_line, font=font)
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    text_height = font.size
    total_height = len(lines) * (text_height + line_spacing)

    current_y = y - total_height // 2
    for line in lines:
        line_width = draw.textlength(line, font=font)
        draw.text((x - line_width // 2, current_y), line, fill=fill, font=font)
        current_y += text_height + line_spacing

def main():
    # Create the image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    try:
        # Attempt to load fonts
        title_font = ImageFont.truetype("Arial Bold.ttf", 36)
        header_font = ImageFont.truetype("Arial Bold.ttf", 24)
        text_font = ImageFont.truetype("Arial.ttf", 18)
    except IOError:
        # Fallback to default font
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Draw title
    title = "Tool Controller Architecture"
    draw_text_centered(draw, (WIDTH//2, PADDING), title, title_font, fill=PRIMARY_COLOR)

    # Define the main components
    components = [
        {
            "title": "Tool Discovery",
            "description": "Finds and catalogs available tools",
            "color": SECONDARY_COLOR
        },
        {
            "title": "Tool Selection",
            "description": "Chooses appropriate tools for user requests",
            "color": SECONDARY_COLOR
        },
        {
            "title": "Tool Execution",
            "description": "Safely runs tools and processes results",
            "color": HIGHLIGHT_COLOR
        }
    ]

    # Calculate positions
    center_y = HEIGHT // 2
    total_width = len(components) * BOX_WIDTH + (len(components) - 1) * BOX_SPACING
    start_x = (WIDTH - total_width) // 2

    # Draw controller container
    container_padding = 60
    container_x1 = start_x - container_padding
    container_y1 = center_y - BOX_HEIGHT * 1.5 - container_padding
    container_x2 = start_x + total_width + container_padding
    container_y2 = center_y + BOX_HEIGHT * 1.5 + container_padding

    # Draw a subtle background for the container
    container_bg = (247, 243, 255)  # Very light purple
    create_rounded_rectangle(draw, (container_x1, container_y1, container_x2, container_y2),
                           radius=20, fill=container_bg, outline=BORDER_COLOR, width=3)

    # Draw controller label
    controller_label = "Tool Controller"
    draw_text_centered(draw, (WIDTH//2, container_y1 - 20), controller_label, header_font, fill=PRIMARY_COLOR)

    # Draw main components
    for i, component in enumerate(components):
        x = start_x + i * (BOX_WIDTH + BOX_SPACING)

        # Draw component box
        box = (x, center_y - BOX_HEIGHT//2, x + BOX_WIDTH, center_y + BOX_HEIGHT//2)
        create_rounded_rectangle(draw, box, fill=component["color"], outline=BORDER_COLOR, width=2)

        # Draw title and description
        draw_text_centered(draw, (x + BOX_WIDTH//2, center_y - BOX_HEIGHT//5), component["title"], header_font)
        draw_multi_line_text(draw, (x + BOX_WIDTH//2, center_y + BOX_HEIGHT//5),
                          component["description"], text_font, max_width=BOX_WIDTH-20)

        # Draw arrow to next component if not the last
        if i < len(components) - 1:
            arrow_start = (x + BOX_WIDTH, center_y)
            arrow_end = (x + BOX_WIDTH + BOX_SPACING, center_y)
            draw_arrow(draw, arrow_start, arrow_end, width=3)

    # Define external elements
    external_elements = {
        "top": {
            "title": "Agent System",
            "description": "Orchestrates tool interactions",
            "y_offset": -250
        },
        "bottom": {
            "title": "External Tools & APIs",
            "description": "Provide specialized capabilities",
            "y_offset": 250
        }
    }

    # Draw external elements
    for position, element in external_elements.items():
        y = center_y + element["y_offset"]

        # Draw element box
        box = (WIDTH//2 - BOX_WIDTH//2, y - BOX_HEIGHT//2, WIDTH//2 + BOX_WIDTH//2, y + BOX_HEIGHT//2)
        create_rounded_rectangle(draw, box, fill=PRIMARY_COLOR, outline=BORDER_COLOR, width=2)

        # Draw title and description
        draw_text_centered(draw, (WIDTH//2, y - BOX_HEIGHT//5), element["title"], header_font)
        draw_multi_line_text(draw, (WIDTH//2, y + BOX_HEIGHT//5),
                          element["description"], text_font, max_width=BOX_WIDTH-20)

    # Draw connection arrows
    # Top to controller
    draw_arrow(draw, (WIDTH//2, center_y - BOX_HEIGHT//2 - container_padding),
              (WIDTH//2, external_elements["top"]["y_offset"] + BOX_HEIGHT//2), width=3)

    # Controller to bottom
    draw_arrow(draw, (WIDTH//2, center_y + BOX_HEIGHT//2 + container_padding),
              (WIDTH//2, external_elements["bottom"]["y_offset"] - BOX_HEIGHT//2), width=3)

    # Bottom to controller (bidirectional)
    draw_arrow(draw, (WIDTH//2 + 30, external_elements["bottom"]["y_offset"] - BOX_HEIGHT//2),
              (WIDTH//2 + 30, center_y + BOX_HEIGHT//2 + container_padding), width=3)

    # Save the image
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated", "tool_controller_architecture.png")
    img.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    main()