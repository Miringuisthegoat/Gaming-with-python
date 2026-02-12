import pygame
import sys

# --- Configuration ---
WIDTH, HEIGHT = 800, 400
FPS = 60
GROUND_Y = HEIGHT - 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GOLD = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Duel")
clock = pygame.time.Clock()


class Fighter:
    def __init__(self, x, color, name, controls, flip):
        self.name = name
        self.rect = pygame.Rect(x, GROUND_Y - 80, 40, 80)
        self.color = color
        self.controls = controls
        self.flip = flip  # True if facing left

        # Physics & Stats
        self.vel_y = 0
        self.health = 100
        self.is_jumping = False

        # Combat State
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_type = None  # 0: Punch, 1: Kick

    def move(self, target):
        speed = 6
        gravity = 1
        dx = 0

        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if not self.attacking:
            if keys[self.controls['left']]:
                dx = -speed
                self.flip = True
            if keys[self.controls['right']]:
                dx = speed
                self.flip = False

            # Jump
            if keys[self.controls['up']] and not self.is_jumping:
                self.vel_y = -16
                self.is_jumping = True

        # Apply Gravity
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # Floor/Screen Collision
        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False

        self.rect.x += dx
        self.rect.clamp_ip(screen.get_rect())

    def update_attack(self, target):
        keys = pygame.key.get_pressed()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking = False

        if not self.attacking:
            if keys[self.controls['punch']]:
                self.perform_attack(target, damage=5, range_val=50, type_idx=0)
            elif keys[self.controls['kick']]:
                self.perform_attack(target, damage=12, range_val=70, type_idx=1)

    def perform_attack(self, target, damage, range_val, type_idx):
        self.attacking = True
        self.attack_type = type_idx
        self.attack_cooldown = 15  # frames of animation

        # Hitbox calculation
        atk_rect = pygame.Rect(self.rect.centerx - (range_val if self.flip else 0),
                               self.rect.y, range_val, self.rect.height)

        if atk_rect.colliderect(target.rect):
            target.health -= damage

    def draw(self, surface):
        x, y = self.rect.centerx, self.rect.y
        # Draw Head
        pygame.draw.circle(surface, self.color, (x, y + 10), 10, 2)
        # Body
        pygame.draw.line(surface, self.color, (x, y + 20), (x, y + 50), 2)

        # Arms/Legs logic changes if attacking
        arm_end = x - 30 if self.flip else x + 30
        leg_end = x - 20 if self.flip else x + 20

        if self.attacking and self.attack_type == 0:  # Punch
            pygame.draw.line(surface, WHITE, (x, y + 25), (arm_end, y + 25), 3)
        else:
            pygame.draw.line(surface, self.color, (x, y + 25), (x - 15, y + 40), 2)
            pygame.draw.line(surface, self.color, (x, y + 25), (x + 15, y + 40), 2)

        if self.attacking and self.attack_type == 1:  # Kick
            pygame.draw.line(surface, GOLD, (x, y + 50), (leg_end, y + 40), 3)
        else:
            pygame.draw.line(surface, self.color, (x, y + 50), (x - 15, y + 75), 2)
            pygame.draw.line(surface, self.color, (x, y + 50), (x + 15, y + 75), 2)

        # Health Bar
        bar_x = self.rect.x
        pygame.draw.rect(surface, RED, (bar_x, y - 20, 40, 5))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, y - 20, 40 * (max(0, self.health) / 100), 5))


# --- Setup Players ---
p1_keys = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'punch': pygame.K_f, 'kick': pygame.K_g}
p2_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'punch': pygame.K_k, 'kick': pygame.K_l}

player1 = Fighter(200, BLUE, "P1", p1_keys, False)
player2 = Fighter(600, RED, "P2", p2_keys, True)

# --- Main Loop ---
while True:
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    if player1.health > 0 and player2.health > 0:
        player1.move(player2)
        player2.move(player1)
        player1.update_attack(player2)
        player2.update_attack(player1)

    # Draw
    player1.draw(screen)
    player2.draw(screen)

    if player1.health <= 0:
        print("Player 2 Wins!")
        break
    if player2.health <= 0:
        print("Player 1 Wins!")
        break

    pygame.display.flip()
    clock.tick(FPS)