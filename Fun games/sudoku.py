import pygame, sys

pygame.init()

# Screen
WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (200,200,200)
BLUE = (0,0,255)
RED = (255,0,0)

# Font
font = pygame.font.SysFont("Arial", 40)

# Example Sudoku puzzle (0=empty)
board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

selected = None

def draw_grid():
    # Draw cells
    for i in range(9):
        for j in range(9):
            rect = pygame.Rect(j*60, i*60, 60, 60)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j*60 + 20, i*60 + 10))
    # Bold lines
    for i in range(10):
        thickness = 3 if i%3==0 else 1
        pygame.draw.line(screen, BLACK, (0,i*60),(540,i*60), thickness)
        pygame.draw.line(screen, BLACK, (i*60,0),(i*60,540), thickness)

def highlight_cell():
    if selected:
        pygame.draw.rect(screen, BLUE, (selected[1]*60, selected[0]*60, 60, 60), 3)

def is_valid(num, row, col):
    # Row check
    if num in board[row]:
        return False
    # Column check
    for i in range(9):
        if board[i][col]==num:
            return False
    # 3x3 square check
    start_row, start_col = 3*(row//3),3*(col//3)
    for i in range(start_row,start_row+3):
        for j in range(start_col,start_col+3):
            if board[i][j]==num:
                return False
    return True

running = True
while running:
    clock.tick(60)
    screen.fill(GRAY)
    draw_grid()
    highlight_cell()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            selected = (y//60, x//60)
        if event.type==pygame.KEYDOWN and selected:
            row, col = selected
            if event.key==pygame.K_1: num = 1
            elif event.key==pygame.K_2: num = 2
            elif event.key==pygame.K_3: num = 3
            elif event.key==pygame.K_4: num = 4
            elif event.key==pygame.K_5: num = 5
            elif event.key==pygame.K_6: num = 6
            elif event.key==pygame.K_7: num = 7
            elif event.key==pygame.K_8: num = 8
            elif event.key==pygame.K_9: num = 9
            elif event.key==pygame.K_BACKSPACE or event.key==pygame.K_DELETE:
                board[row][col]=0
                num = None
            else:
                num = None
            if num:
                if is_valid(num,row,col):
                    board[row][col] = num
                else:
                    # Optional: flash red if invalid
                    pygame.draw.rect(screen, RED, (col*60,row*60,60,60), 3)

    pygame.display.update()
