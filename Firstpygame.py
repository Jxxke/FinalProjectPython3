import pygame
import math
import random
pygame.init()
pygame.mixer.init()
parry = pygame.mixer.Sound('ding-101377.mp3')
pygame.mixer.music.load('the-cradle-of-your-soul-15700.mp3')
pygame.mixer.music.play(loops = 100, start = 0)

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 382

#loading background, etc.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Martian Run!")
bg = pygame.image.load("Bg_for_pygame 2.jpg").convert()
bg_width = bg.get_width()


#define game variables
parry_mod = 0
enemy_speed = 15
phase = 1
shieldshow = 0
wins = 1
ud = True
forwardback = True
game_over = False
boss_hp = 5
shield_time = 0
floor = 250
ready = False
#define font
font_small = pygame.font.SysFont('Lucida Sans', 30)
font_big = pygame.font.SysFont('Lucida Sans', 75)
#scroll
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
scroll = 0
#jump
jumping = False
jump_height = 20
velocity = jump_height
gravity = 1

class object(pygame.sprite.Sprite):
    def __init__(self, speed, x, y, xsize, ysize, degree, img):
        #trying to integrate sprites to fix flickering
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.xsize = xsize
        self.ysize = ysize
        self.x = x
        self.y = y
        self.degree = degree
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.xsize, self.ysize))
        self.image = pygame.transform.rotate(self.image, self.degree)
        self.rect = pygame.Rect((self.x, self.y, self.xsize, self.ysize))
    def auto(self):
        self.rect.move_ip(-self.speed, 0)
        self.x -= self.speed
        if self.x <= 0:
            spawn = random.randint(800, 2000)
            self.x += spawn
            self.rect.move_ip(spawn, 0)
        self.rect
    def draw(self):
        screen.blit(self.image, self.rect)
        

enemy1 = object(15, 1000, floor, 50, 50, 0, 'rocket.png')
player = object(15, 200, floor, 50, 46, 0, 'martian.png')
boss1 = object(15, 500, 75, 300, 300, 0, 'head.png')

#function to output text to screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

flag = True
while flag:
    clock.tick(FPS)
    if ready == False:
        screen.fill("white")
        draw_text(f"INSTRUCTIONS", font_big, (0, 0, 0), 200, 100)
        draw_text("Jump with SPACE, spawn shield with RIGHT SHIFT.\n   Shield only works when blue bar is on screen.\n                              press C to start.", font_small, (0, 0, 0), 150, 175)
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            ready = True
    if game_over == False and ready == True and boss_hp > 0:
        #scrolling background=
        for i in range(0, tiles):
            screen.blit(bg, (i*bg_width + scroll, 0))
        #scroll background
        scroll -= 5
        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0

        #event handler
        player.draw()
        boss1.draw()
        enemy1.draw()
        #show shield level
        pygame.draw.rect(screen, (0, 255, 255), (10, 15, shieldshow*10, 10))
        pygame.display.flip()
        key = pygame.key.get_pressed()
    #jumping + checking floor
        if player.y > floor:
            player.rect.move_ip(0, (player.y - floor))
            player.y = floor
        if key[pygame.K_SPACE]:
            jumping = True
        
        if jumping:
            player.rect.move_ip(0, -velocity)
            player.y -= velocity
            velocity -= gravity
            if velocity < -jump_height:
                jumping = False
                velocity = jump_height

        if key[pygame.K_RSHIFT] and shield_time > 0:
            shieldrect = pygame.Rect(300, player.y - 50, 5, 150)
            shieldimg = pygame.image.load('shield.png').convert_alpha()
            shieldimg = pygame.transform.scale(shieldimg, (40, 150))
            screen.blit(shieldimg, shieldrect)
            shield_time -= 1
            shieldshow -= 1
            if shieldrect.colliderect(enemy1.rect):
                parry.play()
                enemy1.speed = -25
                enemy1.image = pygame.transform.flip(enemy1.image, flip_x=True, flip_y=False)
        spawn = random.randint(1001, 2000)
        if enemy1.x >= spawn:
            if enemy1.speed < 0:
                enemy1.image = pygame.transform.flip(enemy1.image, flip_x=True, flip_y=False)
            enemy1.speed = random.randint(5, 12+(wins*2))

    #boss hover
        if ud:
            boss1.rect.move_ip(0, -1)
            enemy1.rect.move_ip(0, -1)
            boss1.y -= 1
            if boss1.y <= 65:
                ud = False
        elif ud == False:
            boss1.rect.move_ip(0, 1)
            enemy1.rect.move_ip(0, 1)
            boss1.y += 1
            if boss1.y >= 95: 
                ud = True
    #boss hp shower
        for i in range(boss_hp):
            pygame.draw.rect(screen, (255, 10, 10), (700-(i*30), 15, 25, 25))
    #enemy move
        enemy1.auto()
    #Collision
        if player.rect.colliderect(enemy1.rect):
            game_over = True
        elif enemy1.x >= 240 and enemy1.x < 255:
            shield_time = 20-parry_mod
            shieldshow = shield_time
        #boss damage
        if enemy1.x <= boss1.x+12 and enemy1.x > boss1.x-13 and enemy1.speed < 0:
            boss_hp -= 1

    elif game_over == True:
        draw_text(f"GAME OVER! You won {wins-1} times!", font_big, (255, 255, 255), 20, 100)
        draw_text("To play again, press C", font_small, (255, 255, 255), 275, 175)
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            game_over = False
            jumping = False
            jump_height = 20
            velocity = jump_height
            boss_hp = 5
            wins = 1
            parry_mod = 0
            enemy1 = object(15, 1000, floor, 50, 50, 0, 'rocket.png')
            player = object(15, 200, floor, 50, 46, 0, 'martian.png')
            boss1 = object(15, 500, 75, 300, 300, 0, 'head.png')
            shieldshow = 0
    elif boss_hp == 0:
        screen.fill("white")
        draw_text(f"YOU WON! Wins = {wins}", font_big, (0, 0, 0), 150, 100)
        draw_text("To play again, press C", font_small, (0, 0, 0), 275, 175)
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            boss_hp = 5
            wins += 1
            enemy1 = object(15, 1000, floor, 50, 50, 0, 'rocket.png')
            player = object(15, 200, floor, 50, 46, 0, 'martian.png')
            boss1 = object(15, 500, 75, 300, 300, 0, 'head.png')
            shieldshow = 0
            if wins < 10:
                parry_mod += 2


#quitter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    pygame.display.update()

pygame.quit()