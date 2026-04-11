import pygame
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24)

player = MusicPlayer("music")

running = True
while running:
    screen.fill("black")

    title = font.render("Music Player", True, "white")
    track_text = font.render(f"Current track: {player.current_track()}", True, "white")
    controls1 = font.render("P = Play/Unpause", True, "white")
    controls2 = font.render("S = Stop", True, "white")
    controls3 = font.render("N = Next", True, "white")
    controls4 = font.render("B = Previous", True, "white")
    controls5 = font.render("SPACE = Pause", True, "white")
    controls6 = font.render("Q = Quit", True, "white")

    screen.blit(title, (260, 40))
    screen.blit(track_text, (50, 120))
    screen.blit(controls1, (50, 180))
    screen.blit(controls2, (50, 210))
    screen.blit(controls3, (50, 240))
    screen.blit(controls4, (50, 270))
    screen.blit(controls5, (50, 300))
    screen.blit(controls6, (50, 330))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_SPACE:
                player.pause()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()