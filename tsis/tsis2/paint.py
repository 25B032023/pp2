import pygame
import sys

from tools import (
    calculate_rect,
    calculate_square,
    calculate_circle_radius,
    calculate_right_triangle,
    calculate_equilateral_triangle,
    calculate_rhombus,
    flood_fill,
    save_canvas
)


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

clock = pygame.time.Clock()


# --------------------------------------------------
# CANVAS LAYER
# --------------------------------------------------
# base_layer stores permanent drawing.
# screen is used to show base_layer + temporary preview + UI.
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill("black")


# --------------------------------------------------
# COLORS
# --------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)

COLORS = {
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "yellow": YELLOW,
    "purple": PURPLE,
    "white": WHITE,
    "black": BLACK
}


# --------------------------------------------------
# FONTS
# --------------------------------------------------
font = pygame.font.SysFont("Verdana", 18)
small_font = pygame.font.SysFont("Verdana", 15)


# --------------------------------------------------
# VARIABLES
# --------------------------------------------------
current_tool = "pencil"
current_color = RED
brush_size = 5

drawing = False

start_x = start_y = 0
curr_x = curr_y = 0
prev_x = prev_y = 0

# Text tool variables
text_mode = False
text_value = ""
text_pos = (0, 0)

# Message after saving
message = ""


# --------------------------------------------------
# DRAW UI
# --------------------------------------------------
def draw_ui():
    # UI is drawn only on screen, not on base_layer.
    info_1 = "P-Pencil  L-Line  R-Rect  O-Circle  S-Square  T-RightTri  Q-EqTri  H-Rhombus"
    info_2 = "E-Eraser  F-Fill  X-Text  C-Clear  Ctrl+S-Save"
    info_3 = "1-2px  2-5px  3-10px | 4-Red 5-Green 6-Blue 7-Yellow 8-Purple 9-White"

    tool_text = small_font.render(f"Tool: {current_tool} | Size: {brush_size}", True, WHITE)
    color_text = small_font.render(f"Color: {current_color}", True, WHITE)
    help_1 = small_font.render(info_1, True, WHITE)
    help_2 = small_font.render(info_2, True, WHITE)
    help_3 = small_font.render(info_3, True, WHITE)
    msg_text = small_font.render(message, True, YELLOW)

    screen.blit(tool_text, (10, 10))
    screen.blit(color_text, (10, 30))
    screen.blit(help_1, (10, 55))
    screen.blit(help_2, (10, 75))
    screen.blit(help_3, (10, 95))

    if message:
        screen.blit(msg_text, (10, 120))


# --------------------------------------------------
# DRAW SHAPES
# --------------------------------------------------
def draw_shape(surface):
    # This function draws selected shape on given surface.
    # For preview, surface is screen.
    # For final drawing, surface is base_layer.

    if current_tool == "line":
        pygame.draw.line(
            surface,
            current_color,
            (start_x, start_y),
            (curr_x, curr_y),
            brush_size
        )

    elif current_tool == "rect":
        pygame.draw.rect(
            surface,
            current_color,
            calculate_rect(start_x, start_y, curr_x, curr_y),
            brush_size
        )

    elif current_tool == "circle":
        radius = calculate_circle_radius(start_x, start_y, curr_x, curr_y)
        pygame.draw.circle(
            surface,
            current_color,
            (start_x, start_y),
            radius,
            brush_size
        )

    elif current_tool == "square":
        pygame.draw.rect(
            surface,
            current_color,
            calculate_square(start_x, start_y, curr_x, curr_y),
            brush_size
        )

    elif current_tool == "right_triangle":
        pygame.draw.polygon(
            surface,
            current_color,
            calculate_right_triangle(start_x, start_y, curr_x, curr_y),
            brush_size
        )

    elif current_tool == "equilateral_triangle":
        pygame.draw.polygon(
            surface,
            current_color,
            calculate_equilateral_triangle(start_x, start_y, curr_x, curr_y),
            brush_size
        )

    elif current_tool == "rhombus":
        pygame.draw.polygon(
            surface,
            current_color,
            calculate_rhombus(start_x, start_y, curr_x, curr_y),
            brush_size
        )


def is_preview_tool():
    # These tools need live preview while dragging mouse.
    return current_tool in [
        "line",
        "rect",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ]


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
running = True

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        # -------------------------------
        # QUIT
        # -------------------------------
        if event.type == pygame.QUIT:
            running = False

        # -------------------------------
        # KEYBOARD EVENTS
        # -------------------------------
        if event.type == pygame.KEYDOWN:

            # If text mode is active, keyboard writes text.
            if text_mode:
                if event.key == pygame.K_RETURN:
                    # Save text to base_layer
                    text_surface = font.render(text_value, True, current_color)
                    base_layer.blit(text_surface, text_pos)

                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    # Cancel text writing
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    # Delete last character
                    text_value = text_value[:-1]

                else:
                    # Add typed character
                    text_value += event.unicode

            else:
                # Tool selection
                if event.key == pygame.K_p:
                    current_tool = "pencil"

                elif event.key == pygame.K_l:
                    current_tool = "line"

                elif event.key == pygame.K_r:
                    current_tool = "rect"

                elif event.key == pygame.K_o:
                    current_tool = "circle"

                elif event.key == pygame.K_s:
                    # Ctrl+S saves canvas, normal S selects square
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        filename = save_canvas(base_layer)
                        message = f"Saved: {filename}"
                    else:
                        current_tool = "square"

                elif event.key == pygame.K_t:
                    current_tool = "right_triangle"

                elif event.key == pygame.K_q:
                    current_tool = "equilateral_triangle"

                elif event.key == pygame.K_h:
                    current_tool = "rhombus"

                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                elif event.key == pygame.K_f:
                    current_tool = "fill"

                elif event.key == pygame.K_x:
                    current_tool = "text"

                elif event.key == pygame.K_c:
                    # Clear canvas
                    base_layer.fill(BLACK)

                # Brush sizes required by TSIS2
                elif event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

                # Color selection
                elif event.key == pygame.K_4:
                    current_color = RED

                elif event.key == pygame.K_5:
                    current_color = GREEN

                elif event.key == pygame.K_6:
                    current_color = BLUE

                elif event.key == pygame.K_7:
                    current_color = YELLOW

                elif event.key == pygame.K_8:
                    current_color = PURPLE

                elif event.key == pygame.K_9:
                    current_color = WHITE

        # -------------------------------
        # MOUSE BUTTON DOWN
        # -------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_x, start_y = event.pos
            curr_x, curr_y = event.pos
            prev_x, prev_y = event.pos

            # Fill tool works on click
            if current_tool == "fill":
                flood_fill(base_layer, event.pos, current_color)

            # Text tool starts text mode on click
            elif current_tool == "text":
                text_mode = True
                text_value = ""
                text_pos = event.pos

            else:
                drawing = True

        # -------------------------------
        # MOUSE MOTION
        # -------------------------------
        if event.type == pygame.MOUSEMOTION:
            curr_x, curr_y = event.pos

            if drawing:
                # Pencil draws immediately on base_layer
                if current_tool == "pencil":
                    pygame.draw.line(
                        base_layer,
                        current_color,
                        (prev_x, prev_y),
                        (curr_x, curr_y),
                        brush_size
                    )

                # Eraser draws black line on base_layer
                elif current_tool == "eraser":
                    pygame.draw.line(
                        base_layer,
                        BLACK,
                        (prev_x, prev_y),
                        (curr_x, curr_y),
                        brush_size
                    )

                # Preview tools are not drawn permanently here
                # They are shown later in the draw section.

                prev_x, prev_y = curr_x, curr_y

        # -------------------------------
        # MOUSE BUTTON UP
        # -------------------------------
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            curr_x, curr_y = event.pos

            # When mouse is released, draw final shape on base_layer
            if drawing and is_preview_tool():
                draw_shape(base_layer)

            drawing = False

    # --------------------------------------------------
    # DRAW FRAME
    # --------------------------------------------------

    # Draw saved canvas
    screen.blit(base_layer, (0, 0))

    # Draw temporary preview shape while mouse is pressed
    if drawing and is_preview_tool():
        draw_shape(screen)

    # Draw temporary text while typing
    if text_mode:
        preview_text = font.render(text_value, True, current_color)
        screen.blit(preview_text, text_pos)

    # Draw UI over everything
    draw_ui()

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()