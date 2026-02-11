import pygame, sys, random, math

pygame.init()

# Screen
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = 28, 31
SCREEN_WIDTH, SCREEN_HEIGHT = CELL_SIZE*GRID_WIDTH, CELL_SIZE*GRID_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Classic Clone")
clock = pygame.time.Clock()

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
PINK = (255,184,255)
CYAN = (0,255,255)
ORANGE = (255,184,82)
BLUE = (0,0,255)

# Maze layout (0=empty,1=wall,2=pellet,3=power pellet)
maze = [[0]*GRID_WIDTH for _ in range(GRID_HEIGHT)]
for r in range(GRID_HEIGHT):
    for c in range(GRID_WIDTH):
        if r==0 or r==GRID_HEIGHT-1 or c==0 or c==GRID_WIDTH-1:
            maze[r][c]=1  # outer walls
        elif (r%2==0 and c%2==0):
            maze[r][c]=1  # inner walls
        else:
            maze[r][c]=2  # pellets
maze[1][1]=3
maze[1][GRID_WIDTH-2]=3
maze[GRID_HEIGHT-2][1]=3
maze[GRID_HEIGHT-2][GRID_WIDTH-2]=3

# Player
pacman = pygame.Rect(14*CELL_SIZE,23*CELL_SIZE,CELL_SIZE,CELL_SIZE)
pacman_dx, pacman_dy = 0,0
next_dx, next_dy = 0,0
speed = 4
lives = 3

# Ghosts
ghost_colors = [RED, PINK, CYAN, ORANGE]
ghosts=[]
start_positions = [(13,11),(14,11),(13,12),(14,12)]
for i,pos in enumerate(start_positions):
    ghosts.append({"rect": pygame.Rect(pos[0]*CELL_SIZE,pos[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE),
                   "color": ghost_colors[i],
                   "dx":speed, "dy":0,
                   "edible":False,
                   "target":(0,0)})

# Power pellet timer
power_time = 0
power_duration = 7000

score = 0

font = pygame.font.SysFont("Arial",24)

# Functions
def draw_maze():
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            x, y = c*CELL_SIZE, r*CELL_SIZE
            if maze[r][c]==1:
                pygame.draw.rect(screen, BLUE, (x,y,CELL_SIZE,CELL_SIZE))
            elif maze[r][c]==2:
                pygame.draw.circle(screen, WHITE, (x+CELL_SIZE//2, y+CELL_SIZE//2),4)
            elif maze[r][c]==3:
                pygame.draw.circle(screen, WHITE, (x+CELL_SIZE//2, y+CELL_SIZE//2),8)

def move_rect(rect, dx, dy):
    new_rect = rect.move(dx, dy)
    # Wrap around tunnels
    if new_rect.right < 0: new_rect.left = SCREEN_WIDTH
    if new_rect.left > SCREEN_WIDTH: new_rect.right = 0
    row_top = new_rect.top//CELL_SIZE
    row_bottom = (new_rect.bottom-1)//CELL_SIZE
    col_left = new_rect.left//CELL_SIZE
    col_right = (new_rect.right-1)//CELL_SIZE
    for r in range(row_top,row_bottom+1):
        for c in range(col_left,col_right+1):
            if 0<=r<GRID_HEIGHT and 0<=c<GRID_WIDTH:
                if maze[r][c]==1:
                    return rect
    return new_rect

def check_pellets():
    global score, power_time
    row = pacman.centery//CELL_SIZE
    col = pacman.centerx//CELL_SIZE
    if 0<=row<GRID_HEIGHT and 0<=col<GRID_WIDTH:
        if maze[row][col]==2:
            maze[row][col]=0
            score+=10
        elif maze[row][col]==3:
            maze[row][col]=0
            score+=50
            power_time = pygame.time.get_ticks()
            for g in ghosts: g["edible"]=True

def move_ghosts():
    for g in ghosts:
        # Simple AI: move randomly but avoid walls
        g["rect"] = move_rect(g["rect"], g["dx"], g["dy"])
        if random.random()<0.02:
            g["dx"], g["dy"] = random.choice([(speed,0),(-speed,0),(0,speed),(0,-speed)])

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT: next_dx=-speed; next_dy=0
            if event.key==pygame.K_RIGHT: next_dx=speed; next_dy=0
            if event.key==pygame.K_UP: next_dx=0; next_dy=-speed
            if event.key==pygame.K_DOWN: next_dx=0; next_dy=speed

    # Try to move in the next direction if possible
    pacman_temp = move_rect(pacman, next_dx, next_dy)
    if pacman_temp!=pacman:
        pacman_dx, pacman_dy = next_dx, next_dy
    pacman = move_rect(pacman, pacman_dx, pacman_dy)

    check_pellets()
    move_ghosts()

    # Power pellet effect ends
    if power_time>0 and pygame.time.get_ticks()-power_time>power_duration:
        for g in ghosts:
            g["edible"]=False
        power_time=0

    draw_maze()
    pygame.draw.circle(screen,YELLOW,(pacman.centerx,pacman.centery),CELL_SIZE//2)

    for g in ghosts:
        color = BLUE if g["edible"] else g["color"]
        pygame.draw.rect(screen,color,g["rect"])

    # Collision with ghosts
    for g in ghosts:
        if pacman.colliderect(g["rect"]):
            if g["edible"]:
                g["rect"].x = start_positions[ghosts.index(g)][0]*CELL_SIZE
                g["rect"].y = start_positions[ghosts.index(g)][1]*CELL_SIZE
                g["edible"]=False
                score+=200
            else:
                lives-=1
                pacman.x, pacman.y = 14*CELL_SIZE,23*CELL_SIZE
                pacman_dx, pacman_dy = 0,0
                if lives<=0:
                    screen.fill(BLACK)
                    screen.blit(font.render("GAME OVER",True,RED),(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2-30))
                    screen.blit(font.render(f"Score: {score}",True,WHITE),(SCREEN_WIDTH//2-60, SCREEN_HEIGHT//2+20))
                    pygame.display.update()
                    pygame.time.wait(4000)
                    pygame.quit(); sys.exit()

    # Draw UI
    screen.blit(font.render(f"Score: {score}",True,WHITE),(10,10))
    screen.blit(font.render(f"Lives: {lives}",True,YELLOW),(10,40))

    pygame.display.update()
