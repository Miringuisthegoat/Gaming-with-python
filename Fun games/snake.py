import pygame
import sys
import random

# Initialize
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
BLOCK = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Snake setup
snake = [(300, 300)]
direction = (BLOCK, 0)

# Food setup
food = (random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK))

score = 0


def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK, BLOCK))


def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK, BLOCK))


def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


running = True
while running:
    clock.tick(10)  # Snake speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, BLOCK):
                direction = (0, -BLOCK)
            if event.key == pygame.K_DOWN and direction != (0, -BLOCK):
                direction = (0, BLOCK)
            if event.key == pygame.K_LEFT and direction != (BLOCK, 0):
                direction = (-BLOCK, 0)
            if event.key == pygame.K_RIGHT and direction != (-BLOCK, 0):
                direction = (BLOCK, 0)

    # Move snake
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]
    new_head = (head_x, head_y)

    # Check wall collision
    if (head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT):
        break

    # Check self collision
    if new_head in snake:
        break

    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, BLOCK),
                random.randrange(0, HEIGHT, BLOCK))
    else:
        snake.pop()

    # Drawing
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    show_score()

    pygame.display.update()

# Game Over screen
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, RED)
score_text = font.render(f"Final Score: {score}", True, WHITE)

screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))
screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.update()

pygame.time.wait(3000)
pygame.quit()
