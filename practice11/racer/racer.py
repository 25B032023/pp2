import pygame
import sys 
import random

# запускаем pygame
pygame.init() 

# размеры окна
height = 800
width = 600

# создаем окно
ecran = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer ")

# переменная для игрового цикла
a = True

# загружаем фон
fon = pygame.image.load("images/AnimatedStreet.png")
fon = pygame.transform.scale(fon, (width, height))

# загружаем машину игрока
player = pygame.image.load("images/Player.png")
player = pygame.transform.scale(player, (50, 100))
player_x = 200
player_y = 650

# загружаем машину врага
enemy = pygame.image.load("images/Enemy.png")
enemy = pygame.transform.scale(enemy, (50, 100))
enemy_x = random.randint(50, width-50)
enemy_y = -100
enemy_shag = 1
score = 0


# загружаем монету
coin = pygame.image.load("images/Coin.png")
coin = pygame.transform.scale(coin, (60, 60))
coin_x = random.randint(60, width-60)
coin_y = -60
coin_shag = 1
point = 0

point_coin = 15
move = 1

# создаем шрифты
font = pygame.font.SysFont("Verdana", 80)
font_small = pygame.font.SysFont("Verdana", 20)

# главный цикл игры
while a:
    # двигаем врага и монету вниз
    enemy_y += enemy_shag + move
    coin_y += coin_shag


    # создаем области для проверки столкновений
    player_rect = player.get_rect(topleft=(player_x, player_y))
    enemy_rect = enemy.get_rect(topleft=(enemy_x, enemy_y))
    coin_rect = coin.get_rect(topleft=(coin_x, coin_y))
   
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # проверяем нажатые клавиши
    keys = pygame.key.get_pressed()
    
    # если враг ушел вниз, возвращаем его наверх
    if enemy_y > height:
        score += 1
        enemy_y = -100
        enemy_x = random.randint(50, width-50)
    

    # если монета ушла вниз, возвращаем ее наверх
    if coin_y > height:
        coin_y = -60
        coin_x = random.randint(60, width-60)

    # создаем текст очков
    text = font_small.render(f"SCORE: {score}", True, (0, 0, 0))
    text2 = font_small.render(f"POINT: {point}", True, (0, 0, 0))

    # движение игрока влево и вправо
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 2
    if keys[pygame.K_RIGHT] and player_x < width - 70:
        player_x += 2

    # проверка столкновения с врагом
    if player_rect.colliderect(enemy_rect):
        ecran.fill((255, 0, 0))
        text = font.render("Game Over", True, (0, 0, 0))
        ecran.blit(text, (10, 250))

        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
    
    # проверка сбора монеты
    if player_rect.colliderect(coin_rect):
        point += random.randint(1,6)
        coin_y = -60
        coin_x = random.randint(60, width-60)

    
    if point >= point_coin:
        move += 1
        point_coin += 15

    # рисуем фон
    ecran.blit(fon, (0, 0))

    # рисуем счетчики
    ecran.blit(text, (7, 5))
    ecran.blit(text2, (470, 5))

    # рисуем игрока, врага и монету
    ecran.blit(player, (player_x, player_y))
    ecran.blit(enemy, (enemy_x, enemy_y))
    ecran.blit(coin, (coin_x, coin_y))
    
    
    # обновляем экран
    pygame.display.update()