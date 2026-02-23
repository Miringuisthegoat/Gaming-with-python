import pygame, sys, random

import pygame
import random
import sys
import os

pygame.init()

# ======================
# CONFIG
# ======================
CELL_SIZE = 30
COLS, ROWS = 10, 20
SIDE_PANEL = 150

WIDTH = CELL_SIZE * COLS + SIDE_PANEL
HEIGHT = CELL_SIZE * ROWS

NORMAL_FALL_SPEED = 500
FAST_FALL_SPEED = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 0, 0)
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

# ======================
# BLOCK
# ======================
class Block:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))][::-1]
                      for x in range(len(self.shape[0]))]


# ======================
# TETRIS GAME
# ======================
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris - Advanced")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 40)

        self.load_high_score()
        self.reset()

    # ------------------
    # HIGH SCORE
    # ------------------
    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        else:
            self.high_score = 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    # ------------------
    def reset(self):
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_block = Block(random.choice(SHAPES))
        self.next_block = Block(random.choice(SHAPES))

        self.score = 0
        self.fall_time = 0
        self.paused = False
        self.game_over = False
        self.down_pressed = False

    # ------------------
    # LOGIC
    # ------------------
    def valid_move(self, block, dx, dy):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = block.x + x + dx
                    ny = block.y + y + dy
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return False
                    if ny >= 0 and self.grid[ny][nx] != BLACK:
                        return False
        return True

    def place_block(self):
        for y, row in enumerate(self.current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_block.y + y][self.current_block.x + x] = self.current_block.color

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines = ROWS - len(new_grid)
        for _ in range(lines):
            new_grid.insert(0, [BLACK for _ in range(COLS)])
        self.grid = new_grid
        self.score += lines * 100

    # ------------------
    # DRAWING
    # ------------------
    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(self.screen, self.grid[y][x],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, WHITE,
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_block(self):
        for y, row in enumerate(self.current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.current_block.color,
                        ((self.current_block.x + x) * CELL_SIZE,
                         (self.current_block.y + y) * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        ((self.current_block.x + x) * CELL_SIZE,
                         (self.current_block.y + y) * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE), 1
                    )

    def draw_next_piece(self):
        panel_x = COLS * CELL_SIZE + 20
        panel_y = 80

        label = self.font.render("Next:", True, WHITE)
        self.screen.blit(label, (panel_x, 40))

        for y, row in enumerate(self.next_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.next_block.color,
                        (panel_x + x * CELL_SIZE,
                         panel_y + y * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (panel_x + x * CELL_SIZE,
                         panel_y + y * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE), 1
                    )

    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        high_text = self.font.render(f"High: {self.high_score}", True, WHITE)

        self.screen.blit(score_text, (COLS * CELL_SIZE + 20, 200))
        self.screen.blit(high_text, (COLS * CELL_SIZE + 20, 230))

        if self.paused:
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        if self.game_over:
            over_text = self.big_font.render("GAME OVER", True, WHITE)
            self.screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))

    # ------------------
    # MAIN LOOP
    # ------------------
    def run(self):
        while True:
            self.screen.fill(GRAY)
            self.fall_time += self.clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if event.key == pygame.K_r:
                        self.reset()

                    if not self.paused and not self.game_over:
                        if event.key == pygame.K_LEFT and self.valid_move(self.current_block, -1, 0):
                            self.current_block.x -= 1
                        if event.key == pygame.K_RIGHT and self.valid_move(self.current_block, 1, 0):
                            self.current_block.x += 1
                        if event.key == pygame.K_DOWN:
                            self.down_pressed = True
                        if event.key == pygame.K_UP:
                            self.current_block.rotate()
                            if not self.valid_move(self.current_block, 0, 0):
                                for _ in range(3):
                                    self.current_block.rotate()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.down_pressed = False

            # Falling
            if not self.paused and not self.game_over:
                speed = FAST_FALL_SPEED if self.down_pressed else NORMAL_FALL_SPEED

                if self.fall_time > speed:
                    self.fall_time = 0
                    if self.valid_move(self.current_block, 0, 1):
                        self.current_block.y += 1
                    else:
                        self.place_block()
                        self.clear_lines()

                        self.current_block = self.next_block
                        self.next_block = Block(random.choice(SHAPES))

                        if not self.valid_move(self.current_block, 0, 0):
                            self.game_over = True
                            if self.score > self.high_score:
                                self.high_score = self.score
                                self.save_high_score()

            # Draw
            self.draw_grid()
            if not self.game_over:
                self.draw_block()
            self.draw_next_piece()
            self.draw_ui()

            pygame.display.update()
            self.clock.tick(60)


# START
if __name__ == "__main__":
    Tetris().run()