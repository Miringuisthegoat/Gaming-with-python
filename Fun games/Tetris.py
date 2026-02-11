import pygame, sys, random

pygame.init()

# Screen settings
CELL_SIZE = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL_SIZE * COLS, CELL_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Python")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),  # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),  # S
    (128, 0, 128),  # T
    (255, 0, 0)  # Z
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]]  # Z
]

# Grid
grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]


# Current block
class Block:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        # Rotate clockwise
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))][::-1] for x in range(len(self.shape[0]))]


def valid_move(block, dx, dy):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = block.x + x + dx
                ny = block.y + y + dy
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and grid[ny][nx] != BLACK:
                    return False
    return True


def place_block(block):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                if block.y + y >= 0:
                    grid[block.y + y][block.x + x] = block.color


def clear_lines():
    global grid, score
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    lines_cleared = ROWS - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [BLACK for _ in range(COLS)])
    grid = new_grid
    score += lines_cleared * 100


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


# Game variables
current_block = Block(random.choice(SHAPES))
fall_time = 0
normal_fall_speed = 500  # milliseconds
fast_fall_speed = 50
fall_speed = normal_fall_speed
score = 0
down_pressed = False  # Track if DOWN key is held

# Main loop
while True:
    screen.fill(BLACK)
    fall_time += clock.get_time()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_move(current_block, -1, 0):
                current_block.x -= 1
            if event.key == pygame.K_RIGHT and valid_move(current_block, 1, 0):
                current_block.x += 1
            if event.key == pygame.K_DOWN:
                down_pressed = True
            if event.key == pygame.K_UP:
                current_block.rotate()
                if not valid_move(current_block, 0, 0):
                    for _ in range(3): current_block.rotate()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                down_pressed = False

    # Update fall speed dynamically
    fall_speed = fast_fall_speed if down_pressed else normal_fall_speed

    # Block falling
    if fall_time > fall_speed:
        fall_time = 0
        if valid_move(current_block, 0, 1):
            current_block.y += 1
        else:
            place_block(current_block)
            clear_lines()
            current_block = Block(random.choice(SHAPES))
            if not valid_move(current_block, 0, 0):
                # Game over
                pygame.quit()
                print("Game Over! Score:", score)
                sys.exit()

    # Draw
    draw_grid()
    for y, row in enumerate(current_block.shape):
        for x, cell in enumerate(row):
            if cell and current_block.y + y >= 0:
                pygame.draw.rect(screen, current_block.color,
                                 ((current_block.x + x) * CELL_SIZE, (current_block.y + y) * CELL_SIZE, CELL_SIZE,
                                  CELL_SIZE))
                pygame.draw.rect(screen, WHITE,
                                 ((current_block.x + x) * CELL_SIZE, (current_block.y + y) * CELL_SIZE, CELL_SIZE,
                                  CELL_SIZE), 1)

    # Draw score
    font = pygame.font.SysFont("Arial", 24)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

    pygame.display.update()
    clock.tick(60)
