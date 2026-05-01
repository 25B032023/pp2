import pygame
import sys

from racer import run_racer
from persistence import load_settings, save_settings, add_score, get_top10
from ui import (
    draw_menu,
    draw_username_screen,
    draw_settings,
    draw_leaderboard,
    draw_game_over
)


pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Menu")

clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Verdana", 36)
font_small = pygame.font.SysFont("Verdana", 22)

MENU = "menu"
USERNAME = "username"
SETTINGS = "settings"
LEADERBOARD = "leaderboard"
GAME_OVER = "game_over"

state = MENU
username = ""
settings = load_settings()

last_result = {
    "score": 0,
    "distance": 0,
    "coins": 0
}


def change_car_color(settings):
    # Change car color setting
    colors = ["blue", "red", "green", "yellow"]

    if settings["car_color"] not in colors:
        settings["car_color"] = "blue"
        return

    index = colors.index(settings["car_color"])
    settings["car_color"] = colors[(index + 1) % len(colors)]


def change_difficulty(settings):
    # Change difficulty setting
    levels = ["easy", "normal", "hard"]

    if settings["difficulty"] not in levels:
        settings["difficulty"] = "normal"
        return

    index = levels.index(settings["difficulty"])
    settings["difficulty"] = levels[(index + 1) % len(levels)]


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Main menu
            if state == MENU:
                if event.key == pygame.K_1:
                    username = ""
                    state = USERNAME

                elif event.key == pygame.K_2:
                    state = LEADERBOARD

                elif event.key == pygame.K_3:
                    settings = load_settings()
                    state = SETTINGS

                elif event.key == pygame.K_4:
                    running = False

            # Username input
            elif state == USERNAME:
                if event.key == pygame.K_RETURN and username.strip():
                    last_result = run_racer(username.strip(), settings)

                    add_score(
                        username.strip(),
                        last_result["score"],
                        last_result["distance"],
                        last_result["coins"]
                    )

                    state = GAME_OVER

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    username += event.unicode

            # Settings
            elif state == SETTINGS:
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                elif event.key == pygame.K_c:
                    change_car_color(settings)

                elif event.key == pygame.K_d:
                    change_difficulty(settings)

                elif event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    state = MENU

            # Leaderboard
            elif state == LEADERBOARD:
                if event.key == pygame.K_ESCAPE:
                    state = MENU

            # Game over
            elif state == GAME_OVER:
                if event.key == pygame.K_1:
                    username = ""
                    state = USERNAME

                elif event.key == pygame.K_2:
                    state = MENU

    # Draw current screen
    if state == MENU:
        draw_menu(screen, font_big, font_small)

    elif state == USERNAME:
        draw_username_screen(screen, font_big, font_small, username)

    elif state == SETTINGS:
        draw_settings(screen, font_big, font_small, settings)

    elif state == LEADERBOARD:
        draw_leaderboard(screen, font_big, font_small, get_top10())

    elif state == GAME_OVER:
        draw_game_over(screen, font_big, font_small, last_result)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()