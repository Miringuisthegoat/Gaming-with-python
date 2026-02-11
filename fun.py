import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge The Blocks - Power Up Edition")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLACK = (0, 0, 0)

# Player
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 7
health = 3

# Enemy
enemy_size = 50
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = -50
enemy_speed = 5

# Power-up
power_size = 40
power_x = random.randint(0, WIDTH - power_size)
power_y = -200
power_speed = 4
shield_active = False
shield_timer = 0
shield_duration = 5000  # 5 seconds

# Score
score = 0
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

clock = pygame.time.Clock()


def detect_collision(px, py, psize, ox, oy, osize):
    return (px < ox + osize and
            px + psize > ox and
            py < oy + osize and
            py + psize > oy)


running = True
game_over = False

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Enemy movement
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -50
            enemy_x = random.randint(0, WIDTH - enemy_size)
            score += 1
            enemy_speed += 0.3

        # Power-up movement
        power_y += power_speed
        if power_y > HEIGHT:
            power_y = -random.randint(300, 800)
            power_x = random.randint(0, WIDTH - power_size)

        # Collision with enemy
        if detect_collision(player_x, player_y, player_size,
                            enemy_x, enemy_y, enemy_size):
            if not shield_active:
                health -= 1
                enemy_y = -50
                enemy_x = random.randint(0, WIDTH - enemy_size)

                if health <= 0:
                    game_over = True

        # Collision with power-up
        if detect_collision(player_x, player_y, player_size,
                            power_x, power_y, power_size):
            shield_active = True
            shield_timer = pygame.time.get_ticks()
            power_y = -random.randint(300, 800)
            power_x = random.randint(0, WIDTH - power_size)

        # Shield timer check
        if shield_active:
            if pygame.time.get_ticks() - shield_timer > shield_duration:
                shield_active = False

        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # Draw shield effect
        if shield_active:
            pygame.draw.circle(screen, GREEN,
                               (player_x + player_size // 2,
                                player_y + player_size // 2),
                               player_size)

        # Draw enemy & power-up
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_size, enemy_size))
        pygame.draw.rect(screen, GREEN, (power_x, power_y, power_size, power_size))

        # Draw score & health
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        health_text = font.render(f"Health: {health}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

    else:
        over_text = big_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {int(score)}", True, BLACK)
        restart_text = font.render("Close window to exit", True, BLACK)

        screen.blit(over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 80))
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - 140, HEIGHT // 2 + 50))

    pygame.display.update()
