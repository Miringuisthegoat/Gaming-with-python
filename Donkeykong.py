import pygame
import sys
import random

pygame.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Donkey Kong")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (200, 50, 50)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 40)

# Player
player = pygame.Rect(100, 500, 40, 60)
player_vel_y = 0
gravity = 0.8
jump_power = -15
player_speed = 5
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(100, 450, 600, 20),
    pygame.Rect(0, 350, 600, 20),
    pygame.Rect(200, 250, 600, 20),
    pygame.Rect(0, 150, 600, 20),
]

# Barrels
barrels = []
barrel_timer = 0

score = 0
game_over = False


def spawn_barrel():
    return pygame.Rect(750, 120, 30, 30)


running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = jump_power

        # Gravity
        player_vel_y += gravity
        player.y += player_vel_y
        on_ground = False

        # Platform collision
        for platform in platforms:
            if player.colliderect(platform) and player_vel_y >= 0:
                player.bottom = platform.top
                player_vel_y = 0
                on_ground = True

        # Spawn barrels
        barrel_timer += 1
        if barrel_timer > 120:
            barrels.append(spawn_barrel())
            barrel_timer = 0

        # Move barrels
        for barrel in barrels:
            barrel.x -= 4

        # Remove off-screen barrels
        barrels = [b for b in barrels if b.x > -50]

        # Collision detection
        for barrel in barrels:
            if player.colliderect(barrel):
                game_over = True

        # Increase score
        score += 0.05

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, BROWN, platform)

        # Draw player
        pygame.draw.rect(screen, BLUE, player)

        # Draw barrels
        for barrel in barrels:
            pygame.draw.rect(screen, RED, barrel)

        # Draw score
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else:
        over_text = font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {int(score)}", True, BLACK)
        restart_text = font.render("Close window to exit", True, BLACK)

        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - 140, HEIGHT // 2 + 40))

    pygame.display.update()
