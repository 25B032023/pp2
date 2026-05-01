import pygame
import random
import os


def run_racer(username, settings):
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 400, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS3 Racer")

    clock = pygame.time.Clock()
    FPS = 60

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 120, 255)
    RED = (220, 0, 0)
    GREEN = (0, 200, 0)
    YELLOW = (255, 255, 0)

    small_font = pygame.font.SysFont("Verdana", 14)

    # Asset folders
    image_path = os.path.join("assets", "images")
    sound_path = os.path.join("assets", "sounds")

    # Basic images from practice
    background = pygame.image.load(os.path.join(image_path, "AnimatedStreet.png")).convert()
    player_img = pygame.image.load(os.path.join(image_path, "Player.png")).convert_alpha()
    enemy_img = pygame.image.load(os.path.join(image_path, "Enemy.png")).convert_alpha()
    coin_img = pygame.image.load(os.path.join(image_path, "coin.png")).convert_alpha()

    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    player_img = pygame.transform.scale(player_img, (50, 90))
    enemy_img = pygame.transform.scale(enemy_img, (50, 90))
    coin_img = pygame.transform.scale(coin_img, (35, 35))

    # New TSIS3 images
    oil_img = pygame.image.load(os.path.join(image_path, "oil.png")).convert_alpha()
    barrier_img = pygame.image.load(os.path.join(image_path, "barrier.png")).convert_alpha()
    slow_img = pygame.image.load(os.path.join(image_path, "slow_zone.png")).convert_alpha()
    speed_bump_img = pygame.image.load(os.path.join(image_path, "speed_bump.png")).convert_alpha()
    nitro_strip_img = pygame.image.load(os.path.join(image_path, "nitro_strip.png")).convert_alpha()
    shield_img = pygame.image.load(os.path.join(image_path, "shield.png")).convert_alpha()
    repair_img = pygame.image.load(os.path.join(image_path, "repair.png")).convert_alpha()

    oil_img = pygame.transform.scale(oil_img, (60, 35))
    barrier_img = pygame.transform.scale(barrier_img, (80, 45))
    slow_img = pygame.transform.scale(slow_img, (55, 55))
    speed_bump_img = pygame.transform.scale(speed_bump_img, (85, 35))
    nitro_strip_img = pygame.transform.scale(nitro_strip_img, (60, 60))
    shield_img = pygame.transform.scale(shield_img, (40, 40))
    repair_img = pygame.transform.scale(repair_img, (40, 40))

    # Music
    if settings["sound"]:
        music_file = os.path.join(sound_path, "background.wav")

        if not os.path.exists(music_file):
            music_file = os.path.join(sound_path, "background.mp3")

        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)

    # Difficulty
    if settings["difficulty"] == "easy":
        enemy_speed = 4
        extra_enemy_distance = 900
    elif settings["difficulty"] == "hard":
        enemy_speed = 7
        extra_enemy_distance = 450
    else:
        enemy_speed = 5
        extra_enemy_distance = 650

    # Player
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 110, 50, 90)

    car_colors = {
        "blue": BLUE,
        "red": RED,
        "green": GREEN,
        "yellow": YELLOW
    }

    player_color = car_colors.get(settings["car_color"], BLUE)

    # Game variables
    score = 0
    coins = 0
    distance = 0

    shield = False
    active_power = None
    power_start = 0

    enemies = []
    coin_list = []
    hazards = []
    road_events = []
    power_up = None

    def safe_x(width):
        # Random x position inside road
        return random.randint(35, WIDTH - width - 35)

    def spawn_enemy():
        # Enemy car
        return pygame.Rect(safe_x(50), random.randint(-700, -100), 50, 90)

    def spawn_coin():
        # Coin with different weight
        weight = random.choice([1, 1, 1, 2, 2, 3])
        rect = pygame.Rect(safe_x(35), random.randint(-600, -50), 35, 35)
        return {"rect": rect, "weight": weight}

    def spawn_hazard():
        # Lane hazards: oil, slow zone, barrier
        kind = random.choice(["oil", "slow", "barrier"])

        if kind == "barrier":
            size = (80, 45)
        elif kind == "slow":
            size = (55, 55)
        else:
            size = (60, 35)

        rect = pygame.Rect(safe_x(size[0]), random.randint(-950, -100), size[0], size[1])
        return {"rect": rect, "kind": kind}

    def spawn_road_event():
        # Dynamic road events
        kind = random.choice(["moving_barrier", "speed_bump", "nitro_strip"])

        if kind == "speed_bump":
            size = (85, 35)
        elif kind == "nitro_strip":
            size = (60, 60)
        else:
            size = (80, 45)

        rect = pygame.Rect(safe_x(size[0]), random.randint(-1100, -150), size[0], size[1])
        direction = random.choice([-2, 2])

        return {"rect": rect, "kind": kind, "direction": direction}

    def spawn_power_up():
        # Power-ups: nitro, shield, repair
        kind = random.choice(["nitro", "shield", "repair"])
        rect = pygame.Rect(safe_x(40), random.randint(-900, -150), 40, 40)

        return {
            "rect": rect,
            "kind": kind,
            "time": pygame.time.get_ticks()
        }

    def draw_text(text, x, y, color=WHITE):
        img = small_font.render(text, True, color)
        screen.blit(img, (x, y))

    def get_hazard_image(kind):
        # Return correct image for hazard
        if kind == "oil":
            return oil_img
        if kind == "slow":
            return slow_img
        return barrier_img

    def get_road_event_image(kind):
        # Return correct image for road event
        if kind == "speed_bump":
            return speed_bump_img
        if kind == "nitro_strip":
            return nitro_strip_img
        return barrier_img

    def get_power_image(kind):
        # Return correct image for power-up
        if kind == "shield":
            return shield_img
        if kind == "repair":
            return repair_img
        return nitro_strip_img

    # Initial objects
    enemies.append(spawn_enemy())

    for _ in range(3):
        coin_list.append(spawn_coin())

    for _ in range(2):
        hazards.append(spawn_hazard())

    road_events.append(spawn_road_event())

    running = True

    while running:
        now = pygame.time.get_ticks()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()

        player_speed = 5

        if active_power == "nitro":
            player_speed = 8

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        if keys[pygame.K_UP] and player.top > 0:
            player.y -= player_speed

        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += player_speed

        # Power timer
        if active_power == "nitro" and now - power_start > 5000:
            active_power = None

        # Distance and score
        distance += 1
        score = distance // 10 + coins * 10

        # Speed scales by distance
        current_speed = enemy_speed + distance // 700

        # Add more enemy cars by distance
        if distance > extra_enemy_distance and len(enemies) < 2:
            enemies.append(spawn_enemy())

        if distance > extra_enemy_distance * 2 and len(enemies) < 3:
            enemies.append(spawn_enemy())

        # Enemies
        for enemy in enemies:
            enemy.y += current_speed

            if enemy.top > HEIGHT:
                enemy.x = safe_x(50)
                enemy.y = random.randint(-700, -100)

            if player.colliderect(enemy):
                if shield:
                    shield = False
                    enemy.y = random.randint(-700, -100)
                else:
                    running = False

        # Coins
        for coin in coin_list[:]:
            coin["rect"].y += current_speed

            if coin["rect"].top > HEIGHT:
                coin_list.remove(coin)
                coin_list.append(spawn_coin())
                continue

            if player.colliderect(coin["rect"]):
                coins += coin["weight"]
                coin_list.remove(coin)
                coin_list.append(spawn_coin())

        # Hazards
        for hazard in hazards[:]:
            hazard["rect"].y += current_speed

            if hazard["rect"].top > HEIGHT:
                hazards.remove(hazard)
                hazards.append(spawn_hazard())
                continue

            if player.colliderect(hazard["rect"]):
                if hazard["kind"] == "barrier":
                    if shield:
                        shield = False
                        hazard["rect"].y = random.randint(-900, -100)
                    else:
                        running = False

                elif hazard["kind"] == "slow":
                    player.y += 10

                elif hazard["kind"] == "oil":
                    player.x += random.choice([-25, 25])
                    player.x = max(0, min(WIDTH - player.width, player.x))

        # Road events
        for event_obj in road_events[:]:
            event_obj["rect"].y += current_speed

            if event_obj["kind"] == "moving_barrier":
                event_obj["rect"].x += event_obj["direction"]

                if event_obj["rect"].left < 0 or event_obj["rect"].right > WIDTH:
                    event_obj["direction"] *= -1

            if event_obj["rect"].top > HEIGHT:
                road_events.remove(event_obj)
                road_events.append(spawn_road_event())
                continue

            if player.colliderect(event_obj["rect"]):
                if event_obj["kind"] == "moving_barrier":
                    if shield:
                        shield = False
                        event_obj["rect"].y = random.randint(-900, -100)
                    else:
                        running = False

                elif event_obj["kind"] == "speed_bump":
                    player.y += 20

                elif event_obj["kind"] == "nitro_strip":
                    active_power = "nitro"
                    power_start = now
                    event_obj["rect"].y = random.randint(-1000, -150)

        # Power-up
        if power_up is None and random.randint(1, 180) == 1:
            power_up = spawn_power_up()

        if power_up:
            power_up["rect"].y += current_speed

            # Power-up disappears after 8 seconds
            if now - power_up["time"] > 8000 or power_up["rect"].top > HEIGHT:
                power_up = None

            elif player.colliderect(power_up["rect"]):
                if power_up["kind"] == "nitro":
                    active_power = "nitro"
                    power_start = now

                elif power_up["kind"] == "shield":
                    shield = True

                elif power_up["kind"] == "repair":
                    coins += 2

                power_up = None

        # Draw
        screen.blit(background, (0, 0))

        for coin in coin_list:
            screen.blit(coin_img, coin["rect"])
            draw_text(f"+{coin['weight']}", coin["rect"].x, coin["rect"].y - 15, YELLOW)

        for hazard in hazards:
            img = get_hazard_image(hazard["kind"])
            screen.blit(img, hazard["rect"])

        for event_obj in road_events:
            img = get_road_event_image(event_obj["kind"])
            screen.blit(img, event_obj["rect"])

        if power_up:
            img = get_power_image(power_up["kind"])
            screen.blit(img, power_up["rect"])

        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        # Draw player color under player image
        pygame.draw.rect(screen, player_color, player)
        screen.blit(player_img, player)

        # UI
        draw_text(f"Player: {username}", 10, 10)
        draw_text(f"Score: {score}", 10, 30)
        draw_text(f"Distance: {distance}", 10, 50)
        draw_text(f"Coins: {coins}", 10, 70)

        if shield:
            draw_text("Shield: ON", 10, 90, BLUE)

        if active_power:
            draw_text(f"Power: {active_power}", 10, 110, YELLOW)

        pygame.display.update()
        clock.tick(FPS)

    if settings["sound"]:
        pygame.mixer.music.stop()

    return {
        "score": score,
        "distance": distance,
        "coins": coins
    }