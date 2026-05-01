import pygame


def draw_text(screen, text, font, color, x, y):
    # Draw text at exact position
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_center(screen, text, font, color, y):
    # Draw text centered horizontally
    img = font.render(text, True, color)
    rect = img.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(img, rect)


def draw_menu(screen, font_big, font_small):
    # Main menu screen
    screen.fill((20, 20, 20))

    draw_center(screen, "RACER TSIS3", font_big, (255, 255, 255), 120)
    draw_center(screen, "1 - Play", font_small, (255, 255, 255), 230)
    draw_center(screen, "2 - Leaderboard", font_small, (255, 255, 255), 270)
    draw_center(screen, "3 - Settings", font_small, (255, 255, 255), 310)
    draw_center(screen, "4 - Quit", font_small, (255, 255, 255), 350)


def draw_username_screen(screen, font_big, font_small, username):
    # Username input screen
    screen.fill((20, 20, 20))

    draw_center(screen, "Enter Username", font_big, (255, 255, 255), 180)
    draw_center(screen, username, font_small, (255, 255, 0), 260)
    draw_center(screen, "Press ENTER to start", font_small, (255, 255, 255), 330)


def draw_settings(screen, font_big, font_small, settings):
    # Settings screen
    screen.fill((20, 20, 20))

    draw_center(screen, "SETTINGS", font_big, (255, 255, 255), 100)
    draw_center(screen, f"S - Sound: {settings['sound']}", font_small, (255, 255, 255), 200)
    draw_center(screen, f"C - Car color: {settings['car_color']}", font_small, (255, 255, 255), 245)
    draw_center(screen, f"D - Difficulty: {settings['difficulty']}", font_small, (255, 255, 255), 290)
    draw_center(screen, "ESC - Save and return", font_small, (255, 255, 0), 380)


def draw_leaderboard(screen, font_big, font_small, leaderboard):
    # Top 10 leaderboard screen
    screen.fill((20, 20, 20))

    draw_center(screen, "TOP 10 LEADERBOARD", font_big, (255, 255, 255), 60)

    if not leaderboard:
        draw_center(screen, "No results yet", font_small, (255, 255, 255), 180)
    else:
        y = 120

        for i, item in enumerate(leaderboard, start=1):
            line = f"{i}. {item['name']} | Score: {item['score']} | Distance: {item['distance']} | Coins: {item['coins']}"
            draw_text(screen, line, font_small, (255, 255, 255), 25, y)
            y += 35

    draw_center(screen, "ESC - Back", font_small, (255, 255, 0), 560)


def draw_game_over(screen, font_big, font_small, result):
    # Game over screen
    screen.fill((20, 20, 20))

    draw_center(screen, "GAME OVER", font_big, (255, 0, 0), 140)
    draw_center(screen, f"Score: {result['score']}", font_small, (255, 255, 255), 230)
    draw_center(screen, f"Distance: {result['distance']}", font_small, (255, 255, 255), 270)
    draw_center(screen, f"Coins: {result['coins']}", font_small, (255, 255, 255), 310)

    draw_center(screen, "1 - Play again", font_small, (255, 255, 255), 400)
    draw_center(screen, "2 - Main menu", font_small, (255, 255, 255), 440)