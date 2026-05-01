import pygame
import os
from datetime import datetime


def calculate_rect(x1, y1, x2, y2):
    # Creates correct rectangle even if mouse is dragged left/up
    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )


def calculate_square(x1, y1, x2, y2):
    # Square must have equal width and height
    side = min(abs(x2 - x1), abs(y2 - y1))

    # Detect drag direction
    if x2 < x1:
        x = x1 - side
    else:
        x = x1

    if y2 < y1:
        y = y1 - side
    else:
        y = y1

    return pygame.Rect(x, y, side, side)


def calculate_circle_radius(x1, y1, x2, y2):
    # Radius is distance between start point and current mouse point
    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)


def calculate_right_triangle(x1, y1, x2, y2):
    # Right triangle inside dragged rectangle
    return [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]


def calculate_equilateral_triangle(x1, y1, x2, y2):
    # Equilateral triangle: all sides are equal
    side = abs(x2 - x1)
    height = int(side * (3 ** 0.5) / 2)

    # If mouse is dragged upward, triangle goes up
    if y2 < y1:
        height = -height

    return [
        (x1, y1),
        (x2, y1),
        ((x1 + x2) // 2, y1 + height)
    ]


def calculate_rhombus(x1, y1, x2, y2):
    # Rhombus/diamond is built inside dragged rectangle
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    return [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]


def flood_fill(surface, start_pos, new_color):
    # Simple bucket fill tool.
    # It changes connected pixels with the same starting color.
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


def save_canvas(surface, folder="saved"):
    # Create saved folder if it does not exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create unique filename with timestamp
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join("TSIS","TSIS2",folder, f"paint_{time}.png")

    # Save only canvas/base_layer, not UI
    pygame.image.save(surface, filename)

    return filename