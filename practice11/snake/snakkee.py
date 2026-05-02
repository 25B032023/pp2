
import pygame
import sys
import random

pygame.init()

width = 400
height = 600
shag = 20

ecran = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
speed = 4

a = True

snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

food = (200, 200)

score = 0
level = 0
font = pygame.font.SysFont("Verdana", 20)

while a:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление змейкой
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # текущая голова змейки
    head_x, head_y = snake[0]

    # движение головы
    if direction == "RIGHT":
        head_x += shag
    if direction == "LEFT":
        head_x -= shag
    if direction == "UP":
        head_y -= shag
    if direction == "DOWN":
        head_y += shag

    
    # проверка стены
    if head_x < 0:
        head_x = width - shag
    elif head_x >= width:
        head_x = 0
    
    if head_y < 0:
        head_y = height - shag
    elif head_y >= height:
        head_y = 0
    
    new_head = (head_x, head_y)
    

    # проверка столкновения с собой
    if new_head in snake[1:]:
        ecran.fill((255, 0, 0))
        text = font.render("Game Over", True, (0, 0, 0))
        ecran.blit(text, (130, 280))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # добавляем новую голову
    snake.insert(0, new_head)

    # если съела еду
    if new_head == food:
        score += 1
        food = (random.randrange(0, width, shag), random.randrange(0, height, shag))
        if score % 3 == 0:
            level +=1
            speed += 2
    else:
        snake.pop()

    # рисуем фон
    ecran.fill((0, 0, 0))

    # рисуем змейку
    for part in snake:
        pygame.draw.rect(ecran, (0, 255, 0), (part[0], part[1], shag, shag))

    # рисуем еду
    pygame.draw.rect(ecran, (255, 0, 0), (food[0], food[1], shag, shag))

    # рисуем счет
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    ecran.blit(text, (10, 10))
    #рисуем уровень 
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    ecran.blit(level_text, (10, 35))


    pygame.display.update()
    clock.tick(speed)
