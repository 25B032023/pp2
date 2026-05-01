import pygame
import random
import sys
import json
import os

from snake import sn, Food, PowerUp, WIDTH, HEIGHT, CELL
from db import create_tables, save_game, get_best_score, get_leaderboard


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 32)
BIG_FONT = pygame.font.SysFont("arial", 55)

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "snake_color": [255, 0, 0],
            "grid": True,
            "sound": False
        }

        with open(SETTINGS_FILE, "w") as file:
            json.dump(default_settings, file, indent=4)

        return default_settings

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


def draw_text(text, x, y, font=FONT, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(text, rect, color=(60, 60, 60)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    text_img = FONT.render(text, True, (255, 255, 255))
    text_rect = text_img.get_rect(center=rect.center)
    screen.blit(text_img, text_rect)


def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (35, 120, 35), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (35, 120, 35), (0, y), (WIDTH, y))


def make_obstacles(snake_body, foods):
    obstacles = []

    food_positions = []
    for food in foods:
        food_positions.append([food.x, food.y])

    head = snake_body[0]

    # Бас жақты қоршап тастамау үшін head айналасындағы орындарды бос қалдырамыз
    safe_zone = [
        head,
        [head[0] + CELL, head[1]],
        [head[0] - CELL, head[1]],
        [head[0], head[1] + CELL],
        [head[0], head[1] - CELL]
    ]

    while len(obstacles) < 20:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        block = [x, y]

        if block not in snake_body and block not in food_positions and block not in safe_zone and block not in obstacles:
            obstacles.append(block)

    return obstacles


def draw_obstacles(obstacles):
    for block in obstacles:
        pygame.draw.rect(screen, (70, 70, 70), (block[0], block[1], CELL, CELL))


def username_screen():
    username = ""

    while True:
        screen.fill((20, 20, 20))

        draw_text("Enter username:", 520, 300, BIG_FONT)
        draw_text(username, 520, 380, BIG_FONT, (0, 255, 0))
        draw_text("Press ENTER to continue", 520, 470)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        return username.strip()

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 15:
                        username += event.unicode


def main_menu(username):
    play_btn = pygame.Rect(610, 260, 300, 70)
    leader_btn = pygame.Rect(610, 350, 300, 70)
    settings_btn = pygame.Rect(610, 440, 300, 70)
    exit_btn = pygame.Rect(610, 530, 300, 70)

    while True:
        screen.fill((20, 20, 20))

        draw_text("SNAKE GAME", 580, 130, BIG_FONT)
        draw_text(f"Player: {username}", 610, 200)

        draw_button("Play", play_btn)
        draw_button("Leaderboard", leader_btn)
        draw_button("Settings", settings_btn)
        draw_button("Exit", exit_btn)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if play_btn.collidepoint(mouse):
                    game(username)

                elif leader_btn.collidepoint(mouse):
                    leaderboard_screen()

                elif settings_btn.collidepoint(mouse):
                    settings_screen()

                elif exit_btn.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()


def game_over_screen(username, score, level, best):
    save_game(username, score, level)

    retry_btn = pygame.Rect(610, 450, 300, 70)
    menu_btn = pygame.Rect(610, 540, 300, 70)

    while True:
        screen.fill((20, 20, 20))

        draw_text("GAME OVER", 590, 180, BIG_FONT, (255, 0, 0))
        draw_text(f"Score: {score}", 650, 280)
        draw_text(f"Level: {level}", 650, 330)
        draw_text(f"Best score: {max(best, score)}", 650, 380)

        draw_button("Retry", retry_btn)
        draw_button("Main Menu", menu_btn)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if retry_btn.collidepoint(mouse):
                    game(username)

                elif menu_btn.collidepoint(mouse):
                    return


def leaderboard_screen():
    back_btn = pygame.Rect(610, 720, 300, 70)

    try:
        rows = get_leaderboard()
    except Exception:
        rows = []

    while True:
        screen.fill((20, 20, 20))

        draw_text("LEADERBOARD TOP 10", 500, 70, BIG_FONT)

        draw_text("Rank", 230, 160)
        draw_text("Username", 350, 160)
        draw_text("Score", 600, 160)
        draw_text("Level", 750, 160)
        draw_text("Date", 900, 160)

        y = 220
        rank = 1

        for row in rows:
            username, score, level, date = row

            draw_text(str(rank), 250, y)
            draw_text(str(username), 350, y)
            draw_text(str(score), 600, y)
            draw_text(str(level), 750, y)
            draw_text(str(date)[:19], 900, y)

            y += 45
            rank += 1

        draw_button("Back", back_btn)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if back_btn.collidepoint(mouse):
                    return


def settings_screen():
    global settings

    colors = [
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [255, 255, 0],
        [255, 255, 255]
    ]

    color_index = 0

    grid_btn = pygame.Rect(550, 260, 420, 60)
    sound_btn = pygame.Rect(550, 340, 420, 60)
    color_btn = pygame.Rect(550, 420, 420, 60)
    save_btn = pygame.Rect(550, 540, 420, 70)

    while True:
        screen.fill((20, 20, 20))

        draw_text("SETTINGS", 630, 120, BIG_FONT)

        draw_button(f"Grid: {settings['grid']}", grid_btn)
        draw_button(f"Sound: {settings['sound']}", sound_btn)
        draw_button("Change snake color", color_btn)
        draw_button("Save and Back", save_btn)

        pygame.draw.rect(screen, settings["snake_color"], (1000, 430, 50, 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if grid_btn.collidepoint(mouse):
                    settings["grid"] = not settings["grid"]

                elif sound_btn.collidepoint(mouse):
                    settings["sound"] = not settings["sound"]

                elif color_btn.collidepoint(mouse):
                    color_index += 1
                    if color_index >= len(colors):
                        color_index = 0

                    settings["snake_color"] = colors[color_index]

                elif save_btn.collidepoint(mouse):
                    save_settings(settings)
                    return


def game(username):
    try:
        best = get_best_score(username)
    except Exception:
        best = 0

    snake = sn(WIDTH // 2, HEIGHT // 2, settings["snake_color"])

    foods = []
    normal_food = Food("normal")
    normal_food.gen(snake.element, [])
    foods.append(normal_food)

    poison = Food("poison")
    poison.gen(snake.element, [])
    foods.append(poison)

    power = None
    active_power = None
    power_start = 0
    shield = False

    score = 0
    level = 1
    old_level = 1
    speed = 8

    obstacles = []

    running = True

    while running:
        now = pygame.time.get_ticks()

        # Power-up актив уақытын тексеру
        if active_power is not None:
            if now - power_start > 5000:
                active_power = None

        # Power-up field-те 8 секундтан көп тұрса жоғалады
        if power is not None:
            if power.expired():
                power = None

        # Кейде жаңа power-up шығарамыз
        if power is None and random.randint(1, 120) == 1:
            power = PowerUp()
            power.gen(snake.element, obstacles, foods)

        # Food timer
        for food in foods:
            if food.expired():
                food.gen(snake.element, obstacles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.dy != CELL:
                    snake.dx, snake.dy = 0, -CELL

                elif event.key == pygame.K_DOWN and snake.dy != -CELL:
                    snake.dx, snake.dy = 0, CELL

                elif event.key == pygame.K_RIGHT and snake.dx != -CELL:
                    snake.dx, snake.dy = CELL, 0

                elif event.key == pygame.K_LEFT and snake.dx != CELL:
                    snake.dx, snake.dy = -CELL, 0

        snake.move()
        head = snake.element[0]

        # Wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            if shield:
                shield = False

                if head[0] < 0:
                    head[0] = WIDTH - CELL
                elif head[0] >= WIDTH:
                    head[0] = 0
                elif head[1] < 0:
                    head[1] = HEIGHT - CELL
                elif head[1] >= HEIGHT:
                    head[1] = 0
            else:
                game_over_screen(username, score, level, best)
                return

        # Self collision
        if snake.self_collision():
            if shield:
                shield = False
            else:
                game_over_screen(username, score, level, best)
                return

        # Obstacle collision
        if head in obstacles:
            game_over_screen(username, score, level, best)
            return

        # Eat food
        for food in foods[:]:
            if snake.eat(food.x, food.y):
                if food.kind == "poison":
                    snake.cut(2)

                    if len(snake.element) <= 1:
                        game_over_screen(username, score, level, best)
                        return

                    food.gen(snake.element, obstacles)

                else:
                    score += food.weight
                    snake.grow = True

                    level = score // 5 + 1
                    speed = 8 + level

                    food.gen(snake.element, obstacles)

                break

        # Eat power-up
        if power is not None:
            if snake.eat(power.x, power.y):
                if power.type == "shield":
                    shield = True
                else:
                    active_power = power.type
                    power_start = now

                power = None

        # Level 3-тен бастап obstacle шығады
        if level >= 3 and level != old_level:
            obstacles = make_obstacles(snake.element, foods)
            old_level = level

        # Speed effect
        current_speed = speed

        if active_power == "speed":
            current_speed += 5

        elif active_power == "slow":
            current_speed = max(4, current_speed - 5)

        screen.fill((0, 90, 0))

        if settings["grid"]:
            draw_grid()

        for food in foods:
            food.draw(screen)

        if power is not None:
            power.draw(screen)

        draw_obstacles(obstacles)
        snake.draw(screen)

        draw_text(f"Score: {score}", 20, 20)
        draw_text(f"Level: {level}", 20, 60)
        draw_text(f"Best: {best}", 20, 100)

        if shield:
            draw_text("Shield: ON", 20, 140, FONT, (0, 255, 0))

        if active_power is not None:
            draw_text(f"Power: {active_power}", 20, 180, FONT, (255, 255, 0))

        pygame.display.update()
        clock.tick(current_speed)


try:
    create_tables()
except Exception as error:
    print("Database error:", error)

username = username_screen()
main_menu(username)

pygame.quit()
sys.exit()