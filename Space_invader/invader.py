import pygame
import os
import time
import random

from pygame.constants import HIDDEN
pygame.font.init()

WIDTH, HEIGHT =750,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter")

#load images
RED_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
YELLOW_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

class Ship:
    def __init__(self,x,y,health=100):
        self.x =x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img =None
        self.lasers=[]
        self.cool_down_counter = 0
    
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))

    #to get width and height of the space ship image
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

#player
class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img=YELLOW_SHIP
        self.laser_img=YELLOW_LASER
        #pixel perfect collision -> mask()
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

#enemy
class Enemy(Ship):
    COLOR_MAP = {
            "red":(RED_SHIP,RED_LASER),
            "green":(GREEN_SHIP,GREEN_LASER),
            "blue":(BLUE_SHIP,BLUE_LASER)
        }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img,self.laser_img =self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self,vel):
        self.y += vel

def main():
    run=True 
    FPS = 60 #Frames per second
    level = 0
    lives = 6
    player_vel = 5
    main_font = pygame.font.SysFont("Garamond",35)
    lost_font = pygame.font.SysFont("Garamond",55)

    enemies =[]
    wave_length = 5
    enemy_vel= 1

    player = Player(300,650)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0))
        #draw text
        level_label = main_font.render(f"Level: {level}",1,(255, 223, 211))
        lives_label = main_font.render(f"Lives: {lives}",1,(255, 223, 211))

        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))

        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!",1,(255, 223, 211))
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,350))

        pygame.display.update()

    
    while run:
        clock.tick(FPS)
        redraw_window() 

        #for lives
        if lives <= 0 or player.health<=0 :
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies)== 0:
            level += 1
            wave_length +=5
            for i in range(wave_length):
                 enemy = Enemy(random.randrange(50,WIDTH-100),random.randrange(-1500 ,-100),random.choice(["red","blue","green"]))
                 enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        
        #to move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x-player_vel>0: #left
            player.x -=player_vel
        if keys[pygame.K_d] and player.x+player_vel+player.get_width()<WIDTH: #right
            player.x += player_vel
        if keys[pygame.K_w] and player.y-player_vel >0: #up
            player.y -=player_vel
        if keys[pygame.K_s] and player.y+player_vel+player.get_height() < HEIGHT: #down
            player.y +=player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -=1
                enemies.remove(enemy)

  
main()
