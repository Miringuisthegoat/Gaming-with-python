import pygame, sys, random, math
pygame.init()

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D GTA Pro Extreme Deluxe")
clock = pygame.time.Clock()

# Colors
WHITE=(255,255,255); BLACK=(0,0,0); RED=(200,50,50); BLUE=(50,100,255)
YELLOW=(255,215,0); GREEN=(34,177,76); ORANGE=(255,140,0); GRAY=(100,100,100)
CYAN=(0,255,255); PURPLE=(200,0,200)

font=pygame.font.SysFont("arial",24)

# World
WORLD_WIDTH, WORLD_HEIGHT = 2000, 2000

# Player
player = pygame.Rect(1000,1000,30,30)
player_speed = 5
player_health = 100
cash = 0
player_gun = "pistol"

# Weapons
weapons = {
    "pistol":{"damage":20,"speed":12,"color":WHITE,"fire_rate":500},
    "shotgun":{"damage":50,"speed":8,"color":ORANGE,"fire_rate":1000},
    "mg":{"damage":10,"speed":15,"color":YELLOW,"fire_rate":100}
}
last_shot_time = 0

# Assets, hideouts, shops, barrels
assets=[pygame.Rect(500,1200,20,20), pygame.Rect(800,600,20,20)]
hideouts=[pygame.Rect(200,1800,40,40), pygame.Rect(1800,200,40,40)]
shops=[pygame.Rect(300,500,50,50), pygame.Rect(1600,1600,50,50)]
barrels=[pygame.Rect(600,600,20,20), pygame.Rect(1400,1400,20,20)]

# NPCs
npcs=[pygame.Rect(random.randint(50,WORLD_WIDTH-50), random.randint(50,WORLD_HEIGHT-50),25,25) for _ in range(15)]

# Police
police_units=[]
special_police_units=[]  # SWAT cars
helicopters=[]

# Bullets
bullets=[]

# Missions
class Mission:
    def __init__(self,type,start,end,target,reward):
        self.type=type
        self.start=start
        self.end=end
        self.target=target
        self.completed=False
        self.stage=0
        self.reward=reward
missions=[Mission("advanced",pygame.Rect(400,400,20,20),pygame.Rect(800,800,20,20),pygame.Rect(900,900,25,25),500)]

# Explosions
class Explosion:
    def __init__(self,x,y,radius,duration):
        self.x=x; self.y=y; self.radius=radius; self.timer=pygame.time.get_ticks(); self.duration=duration
    def draw(self,camera_x,camera_y):
        elapsed = pygame.time.get_ticks()-self.timer
        if elapsed < self.duration:
            pygame.draw.circle(screen,RED,(int(self.x-camera_x),int(self.y-camera_y)),self.radius)
            return True
        return False
explosions=[]

# Camera
camera_x,camera_y=0,0

# Wanted
wanted_level=0
wanted_timer=0

def draw_text(text,x,y,color=WHITE):
    screen.blit(font.render(text,True,color),(x,y))

def spawn_police():
    side=random.choice(["top","bottom","left","right"])
    if side=="top": return pygame.Rect(random.randint(0,WORLD_WIDTH),0,30,30)
    if side=="bottom": return pygame.Rect(random.randint(0,WORLD_WIDTH),WORLD_HEIGHT,30,30)
    if side=="left": return pygame.Rect(0,random.randint(0,WORLD_HEIGHT),30,30)
    if side=="right": return pygame.Rect(WORLD_WIDTH,random.randint(0,WORLD_HEIGHT),30,30)
def spawn_swat():
    side=random.choice(["top","bottom","left","right"])
    if side=="top": return pygame.Rect(random.randint(0,WORLD_WIDTH),0,40,40)
    if side=="bottom": return pygame.Rect(random.randint(0,WORLD_WIDTH),WORLD_HEIGHT,40,40)
    if side=="left": return pygame.Rect(0,random.randint(0,WORLD_HEIGHT),40,40)
    if side=="right": return pygame.Rect(WORLD_WIDTH,random.randint(0,WORLD_HEIGHT),40,40)
def spawn_helicopter():
    return pygame.Rect(random.randint(0,WORLD_WIDTH),0,50,50)  # always spawn from top

# Game loop
running=True
while running:
    dt=clock.tick(60)
    screen.fill(GREEN)
    keys=pygame.key.get_pressed()

    # Events
    for event in pygame.event.get():
        if event.type==pygame.QUIT: pygame.quit(); sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_1: player_gun="pistol"
            if event.key==pygame.K_2: player_gun="shotgun"
            if event.key==pygame.K_3: player_gun="mg"

    # Movement
    if keys[pygame.K_w]: player.y-=player_speed
    if keys[pygame.K_s]: player.y+=player_speed
    if keys[pygame.K_a]: player.x-=player_speed
    if keys[pygame.K_d]: player.x+=player_speed

    # Shooting
    if keys[pygame.K_SPACE]:
        now=pygame.time.get_ticks()
        if now-last_shot_time>weapons[player_gun]["fire_rate"]:
            mx,my=pygame.mouse.get_pos()
            dx=mx-SCREEN_WIDTH//2
            dy=my-SCREEN_HEIGHT//2
            dist=math.hypot(dx,dy)
            if dist!=0: dx,dy=dx/dist,dy/dist
            bullets.append([player.centerx,player.centery,dx*weapons[player_gun]["speed"],dy*weapons[player_gun]["speed"],weapons[player_gun]["damage"],weapons[player_gun]["color"]])
            last_shot_time=now

    # NPC random movement
    for npc in npcs:
        npc.x+=random.choice([-1,0,1])
        npc.y+=random.choice([-1,0,1])

    # Bullet movement & collision
    for bullet in bullets:
        bullet[0]+=bullet[2]; bullet[1]+=bullet[3]
    bullets=[b for b in bullets if 0<b[0]<WORLD_WIDTH and 0<b[1]<WORLD_HEIGHT]

    for bullet in bullets[:]:
        for npc in npcs[:]:
            if npc.collidepoint(bullet[0],bullet[1]):
                bullets.remove(bullet); npcs.remove(npc); cash+=100; wanted_level=min(5,wanted_level+1); wanted_timer=pygame.time.get_ticks()
                break
        for barrel in barrels[:]:
            if barrel.collidepoint(bullet[0],bullet[1]):
                bullets.remove(bullet); explosions.append(Explosion(barrel.x,barrel.y,50,500)); barrels.remove(barrel)
                break

    # Police spawn based on wanted
    if wanted_level>0:
        if len(police_units)<wanted_level*2: police_units.append(spawn_police())
        if wanted_level>=4 and len(special_police_units)<wanted_level-3: special_police_units.append(spawn_swat())
        if wanted_level>=5 and len(helicopters)<1: helicopters.append(spawn_helicopter())

    # Police AI
    for cop in police_units+special_police_units:
        dx=player.x-cop.x; dy=player.y-cop.y; dist=math.hypot(dx,dy)
        if dist!=0:
            speed=2+(2 if cop in special_police_units else 0)
            cop.x+=(dx/dist)*speed; cop.y+=(dy/dist)*speed
        if player.colliderect(cop): player_health-=0.5

    # Helicopter AI
    for heli in helicopters:
        dx=player.x-heli.x; dy=player.y-heli.y; dist=math.hypot(dx,dy)
        if dist!=0: heli.x+=(dx/dist)*1.5; heli.y+=(dy/dist)*1.5
        # simulate damage zone
        if math.hypot(player.x-heli.x, player.y-heli.y)<100: player_health-=0.2

    # Wanted decay
    if wanted_level>0 and pygame.time.get_ticks()-wanted_timer>8000:
        wanted_level-=1; wanted_timer=pygame.time.get_ticks()

    # Player collect assets
    for asset in assets[:]:
        if player.colliderect(asset): cash+=50; assets.remove(asset)
    for hideout in hideouts:
        if player.colliderect(hideout): wanted_level=0

    # Camera
    camera_x=player.x-SCREEN_WIDTH//2; camera_y=player.y-SCREEN_HEIGHT//2

    # Draw world
    pygame.draw.rect(screen,GRAY,(-camera_x,-camera_y,WORLD_WIDTH,WORLD_HEIGHT))
    for barrel in barrels: pygame.draw.rect(screen,ORANGE,(barrel.x-camera_x,barrel.y-camera_y,barrel.width,barrel.height))
    for asset in assets: pygame.draw.rect(screen,GREEN,(asset.x-camera_x,asset.y-camera_y,asset.width,asset.height))
    for hideout in hideouts: pygame.draw.rect(screen,YELLOW,(hideout.x-camera_x,hideout.y-camera_y,hideout.width,hideout.height))
    for shop in shops: pygame.draw.rect(screen,BLUE,(shop.x-camera_x,shop.y-camera_y,shop.width,shop.height))
    for npc in npcs: pygame.draw.rect(screen,RED,(npc.x-camera_x,npc.y-camera_y,npc.width,npc.height))
    for cop in police_units: pygame.draw.rect(screen,BLUE,(cop.x-camera_x,cop.y-camera_y,cop.width,cop.height))
    for swat in special_police_units: pygame.draw.rect(screen,PURPLE,(swat.x-camera_x,swat.y-camera_y,swat.width,swat.height))
    for heli in helicopters: pygame.draw.rect(screen,CYAN,(heli.x-camera_x,heli.y-camera_y,heli.width,heli.height))

    for bullet in bullets: pygame.draw.circle(screen,bullet[5],(int(bullet[0]-camera_x),int(bullet[1]-camera_y)),4)
    for exp in explosions[:]:
        if not exp.draw(camera_x,camera_y): explosions.remove(exp)
    pygame.draw.rect(screen,WHITE,(player.x-camera_x,player.y-camera_y,player.width,player.height))

    # Mini-map
    minimap=pygame.Surface((200,150)); minimap.fill(BLACK)
    scale_x=200/WORLD_WIDTH; scale_y=150/WORLD_HEIGHT
    pygame.draw.rect(minimap,WHITE,(player.x*scale_x,player.y*scale_y,5,5))
    for cop in police_units: pygame.draw.rect(minimap,BLUE,(cop.x*scale_x,cop.y*scale_y,5,5))
    for swat in special_police_units: pygame.draw.rect(minimap,PURPLE,(swat.x*scale_x,swat.y*scale_y,5,5))
    for heli in helicopters: pygame.draw.rect(minimap,CYAN,(heli.x*scale_x,heli.y*scale_y,5,5))
    for hideout in hideouts: pygame.draw.rect(minimap,YELLOW,(hideout.x*scale_x,hideout.y*scale_y,5,5))
    for asset in assets: pygame.draw.rect(minimap,GREEN,(asset.x*scale_x,asset.y*scale_y,5,5))
    for shop in shops: pygame.draw.rect(minimap,BLUE,(shop.x*scale_x,shop.y*scale_y,5,5))
    screen.blit(minimap,(SCREEN_WIDTH-210,10))

    # Shops
    for shop in shops:
        if player.colliderect(shop):
            draw_text("Press B to Buy Health/Ammo ($100)",SCREEN_WIDTH//2-150,SCREEN_HEIGHT-50)
            if keys[pygame.K_b]:
                if cash>=100: cash-=100; player_health=min(100,player_health+50)

    # Missions
    for m in missions:
        if not m.completed:
            if m.stage==0:
                pygame.draw.rect(screen,ORANGE,(m.start.x-camera_x,m.start.y-camera_y,m.start.width,m.start.height))
                if player.colliderect(m.start): m.stage=1
            elif m.stage==1:
                pygame.draw.rect(screen,ORANGE,(m.end.x-camera_x,m.end.y-camera_y,m.end.width,m.end.height))
                if player.colliderect(m.end): m.stage=2
            elif m.stage==2:
                pygame.draw.rect(screen,RED,(m.target.x-camera_x,m.target.y-camera_y,m.target.width,m.target.height))
                if player.colliderect(m.target): m.completed=True; cash+=m.reward; draw_text(f"Mission Complete +${m.reward}",SCREEN_WIDTH//2-100,SCREEN_HEIGHT-50)

    # UI
    draw_text(f"Health: {int(player_health)}",10,10)
    draw_text(f"Cash: ${cash}",10,35)
    draw_text("Wanted: "+"★"*wanted_level,10,60,YELLOW)
    draw_text(f"Gun: {player_gun}",10,85)

    # Game Over
    if player_health<=0:
        screen.fill(BLACK)
        draw_text("YOU DIED",SCREEN_WIDTH//2-60,SCREEN_HEIGHT//2,RED)
        draw_text(f"Cash Collected: ${cash}",SCREEN_WIDTH//2-100,SCREEN_HEIGHT//2+40)
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    pygame.display.update()
