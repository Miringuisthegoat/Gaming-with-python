import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5
        self.health = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
        # Keep inside screen
        self.rect.clamp_ip(screen.get_rect())


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.Vector2(dir_x, dir_y).normalize() * 10

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if not screen.get_rect().colliderect(self.rect):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((random.randint(50,255), 0, 0))
        self.rect = self.image.get_rect(
            center=(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        )
        self.speed = 2

    def update(self, player):
        direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed


player = Player()
player_group = pygame.sprite.Group(player)
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

SPAWNENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMY, 2000)  # spawn every 2 sec

score = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWNENEMY:
            enemy_group.add(Enemy())
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dir_vector = pygame.Vector2(mx - player.rect.centerx, my - player.rect.centery)
            bullet_group.add(Bullet(player.rect.centerx, player.rect.centery, dir_vector.x, dir_vector.y))

    # Update
    player_group.update()
    bullet_group.update()
    enemy_group.update(player)

    # Collision
    for bullet in pygame.sprite.groupcollide(bullet_group, enemy_group, True, True):
        score += 1
    if pygame.sprite.spritecollide(player, enemy_group, True):
        player.health -= 1
        if player.health <= 0:
            print("Game Over! Score:", score)
            pygame.quit()
            sys.exit()

    # Draw
    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)

    # UI
    score_text = font.render(f"Score: {score}  Health: {player.health}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()


