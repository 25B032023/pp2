import pygame
import math

pygame.init()

width = 1000
height = 800
ecran = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 180, 0)
blue = (0, 100, 255)

ecran.fill(white)

font = pygame.font.SysFont("Arial", 18)

current_color = black
tool = "brush"
drawing = False
start_pos = None

a = True

while a:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"

            # новые фигуры
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_t:
                tool = "right_triangle"
            elif event.key == pygame.K_y:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_d:
                tool = "diamond"

            elif event.key == pygame.K_1:
                current_color = black
            elif event.key == pygame.K_2:
                current_color = red
            elif event.key == pygame.K_3:
                current_color = green
            elif event.key == pygame.K_4:
                current_color = blue
            elif event.key == pygame.K_SPACE:
                ecran.fill(white)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x = min(start_pos[0], end_pos[0])
            y = min(start_pos[1], end_pos[1])
            w = abs(start_pos[0] - end_pos[0])
            h = abs(start_pos[1] - end_pos[1])

            if tool == "rectangle":
                pygame.draw.rect(ecran, current_color, (x, y, w, h), 3)

            elif tool == "circle":
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(ecran, current_color, start_pos, radius, 3)

            elif tool == "square":
                side = min(w, h)
                pygame.draw.rect(ecran, current_color, (x, y, side, side), 3)

            elif tool == "right_triangle":
                points = [
                    start_pos,
                    (start_pos[0], end_pos[1]),
                    end_pos
                ]
                pygame.draw.polygon(ecran, current_color, points, 3)

            elif tool == "equilateral_triangle":
                side = min(w, h)
                p1 = (x + side // 2, y)
                p2 = (x, y + int(side * math.sqrt(3) / 2))
                p3 = (x + side, y + int(side * math.sqrt(3) / 2))
                pygame.draw.polygon(ecran, current_color, [p1, p2, p3], 3)

            elif tool == "diamond":
                cx = (start_pos[0] + end_pos[0]) // 2
                cy = (start_pos[1] + end_pos[1]) // 2
                points = [
                    (cx, y),
                    (x + w, cy),
                    (cx, y + h),
                    (x, cy)
                ]
                pygame.draw.polygon(ecran, current_color, points, 3)

    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if tool == "brush":
            pygame.draw.line(ecran, current_color, start_pos, mouse_pos, 5)
            start_pos = mouse_pos

        elif tool == "eraser":
            pygame.draw.line(ecran, white, start_pos, mouse_pos, 20)
            start_pos = mouse_pos

    pygame.draw.rect(ecran, white, (0, 0, width, 55))
    info = font.render(
        "B Brush | R Rect | C Circle | S Square | T Right Tri | Y Equal Tri | D Diamond | E Eraser | Space Clear",
        True,
        black
    )
    ecran.blit(info, (10, 15))
    info2 = font.render(
    "1 Black | 2 Red | 3 Green | 4 Blue | Space Clear",
    True,
    black
    )
    ecran.blit(info2, (10, 35))

    pygame.display.update()
    clock.tick(60)

pygame.quit()