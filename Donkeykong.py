import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Donkey Kong")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BLUE = (50, 100, 255)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)

font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 60)

# Player
player = pygame.Rect(100, 600, 40, 60)
player_vel_y = 0
gravity = 0.8
jump_power = -15
player_speed = 5
on_ground = False
climbing = False

# Donkey & Princess
donkey = pygame.Rect(50, 50, 80, 80)
princess = pygame.Rect(750, 70, 40, 60)

# Platforms
platforms = [
    pygame.Rect(0, 650, 900, 50),
    pygame.Rect(0, 550, 750, 20),
    pygame.Rect(150, 450, 750, 20),
    pygame.Rect(0, 350, 750, 20),
    pygame.Rect(150, 250, 750, 20),
    pygame.Rect(0, 150, 750, 20),
]

# Ladders
ladders = [
    pygame.Rect(200, 550, 40, 100),
    pygame.Rect(600, 450, 40, 100),
    pygame.Rect(200, 350, 40, 100),
    pygame.Rect(600, 250, 40, 100),
    pygame.Rect(350, 150, 40, 100),
]

# Barrels
barrels = []
barrel_timer = 0

score = 0
lives = 3
game_over = False
win = False


def spawn_barrel():
    return pygame.Rect(donkey.x + 60, donkey.y + 60, 30, 30)


def reset_player():
    player.x = 100
    player.y = 600


running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not win:

        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        # Jump
        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = jump_power

        # Ladder detection
        climbing = False
        for ladder in ladders:
            if player.colliderect(ladder):
                climbing = True
                if keys[pygame.K_UP]:
                    player.y -= player_speed
                if keys[pygame.K_DOWN]:
                    player.y += player_speed

        # Gravity
        if not climbing:
            player_vel_y += gravity
            player.y += player_vel_y

        # Platform collision
        on_ground = False
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
            barrel.x += 4
            barrel.y += gravity

            # Barrel platform collision
            for platform in platforms:
                if barrel.colliderect(platform):
                    barrel.bottom = platform.top

        # Remove off-screen barrels
        barrels = [b for b in barrels if b.y < HEIGHT]

        # Barrel collision
        for barrel in barrels:
            if player.colliderect(barrel):
                lives -= 1
                reset_player()
                barrels.clear()
                if lives <= 0:
                    game_over = True

        # Win condition
        if player.colliderect(princess):
            win = True

        score += 0.02

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

    # Draw ladders
    for ladder in ladders:
        pygame.draw.rect(screen, YELLOW, ladder)

    # Draw characters
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, donkey)
    pygame.draw.rect(screen, PINK, princess)

    # Draw barrels
    for barrel in barrels:
        pygame.draw.rect(screen, WHITE, barrel)

    # UI
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))

    if win:
        win_text = big_font.render("YOU SAVED THE PRINCESS!", True, YELLOW)
        screen.blit(win_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))

    pygame.display.update()
