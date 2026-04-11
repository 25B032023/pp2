import pygame
from clock import get_current_time, draw_clock

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

clock = pygame.time.Clock()

# images
background = pygame.image.load("images/clock.png")
left_arm = pygame.image.load("images/leftarm.png")
right_arm = pygame.image.load("images/rightarm.png")

# фонды экран өлшеміне келтіреміз
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# сағаттың ортасы
center = (WIDTH // 2, HEIGHT // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    minutes, seconds = get_current_time()

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    draw_clock(screen, left_arm, right_arm, center, minutes, seconds)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()