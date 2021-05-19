import pygame
import random


### Settings ###
width = 900
height = 900
FPS = 30

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTBLUE = (0, 155, 155)

pygame.init()

### Primary Definitions ###
background = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
pygame.display.set_caption("Turn-based battle")
font_name = pygame.font.match_font('Monospace')

### Functions and Sprites ###
def draw_text(font_size, text, x, y):
    font = pygame.font.Font(font_name, font_size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    background.blit(text_surface, text_rect)

def health_bar(x, y, w, hp):
    if hp < 0:
        hp = 0
    fill = (hp/100) * w
    outline_rect = pygame.Rect(x, y, w, 10)
    filled_rect = pygame.Rect(x+1, y+1, fill-2, 8)
    pygame.draw.rect(background, WHITE, outline_rect, 1)
    pygame.draw.rect(background, GREEN, filled_rect)

def turn(character):
    character.turn = True
    if character in enemies:
        target = random.choice([player, player2])
        character.attack(target)
    else:
        idle = True
        while idle:
            button.able = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.rect.collidepoint(event.pos):
                        character.attack(enemy)
                        button.image.fill(GRAY)
                        idle = False
                        button.able = False
                
            #print(random.randint(1, 1000))
            background.fill(BLACK)
            all_sprites.draw(background)
            all_sprites.update()
            pygame.display.flip()

# Sprites ###
class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.image = pygame.Surface((100, 40))
        self.rect = self.image.get_rect()
        self.image.fill(GRAY)
        self.rect.centerx = width / 2
        self.rect.centery = 3 * height / 4
        self.text = 'Attack'
        self.font = pygame.font.Font(font_name, 16)
        self.image.blit(self.font.render(self.text, True, WHITE), (20, 10))
        self.able = False
    
    def update(self):
        self.image.fill(GRAY)
        if self.able:
            self.image.fill(GREEN)
        self.image.blit(self.font.render(self.text, True, WHITE), (20, 10))
        #pass

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, COL, speed):
        pygame.sprite.Sprite.__init__(self, all_sprites, characters, heroes)
        self.image = pygame.Surface([30, 30])
        self.image.fill(COL)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.max_hp = 100
        self.hp = 100
        self.strength = 10
        self.speed = speed
        self.turn = False
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp)

    def attack(self, target):
        if self.turn:
            hit = int(random.randrange(0.8 * self.strength, 1.2 * self.strength))
            rng = random.randint(1, 101)
            if rng <= 20:
                hit *= 2
                target.hp -= hit
                Value(hit, target, WHITE)
            else:
                target.hp -= hit
                Value(hit, target, RED)
            self.turn = False
            sortedbyspeed.remove(self)
            sortedbyspeed.append(self)

    def update(self):
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp)
        if self.hp <= 0:
            self.kill()
        if sortedbyspeed.index(self) == 0:
            self.turn = True

class Red_box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, all_sprites, characters, enemies)
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.max_hp = 100
        self.hp = 100
        self.strength = 20
        self.speed = 25
        self.turn = False
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp)

    def attack(self, target):
        if self.turn:
            hit = int(random.randrange(0.8 * self.strength, 1.2 * self.strength))
            rng = random.randint(1, 101)
            if rng <= 20:
                hit *= 2
                target.hp -= hit
                Value(hit, target, WHITE)
            else:
                target.hp -= hit
                Value(hit, target, RED)
            self.turn = False
            print(target.hp)
            sortedbyspeed.remove(self)
            sortedbyspeed.append(self)
    
    def update(self):
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp)
        if self.hp <= 0:
            self.kill()
        if sortedbyspeed.index(self) == 0:
            self.turn = True

    
class Value(pygame.sprite.Sprite):
    def __init__(self, value, target, color):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.font = pygame.font.Font(font_name, 24)
        self.image = self.font.render(str(value), True, color)
        self.rect = self.image.get_rect()
        self.owner = target
        self.rect.bottomright = target.rect.topleft
    
    def update(self):
        self.rect.y -= 1
        if self.owner.rect.y - self.rect.y >= 75:
            self.kill()

### Creating Sprites ###
all_sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
heroes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player(width / 4, height / 2, YELLOW, 15)
player2 = Player(width/4 - 50, height/2, LIGHTBLUE, 15)
enemy = Red_box(3 * width / 4, height / 2)
button = Button()

### Time-related stuff ###
cooldown = 1000
last_turn = 0

### Background music ###
pygame.mixer.music.load('battle.wav')
pygame.mixer.music.play(-1)

### Main Loop ###
sortedbyspeed = sorted(characters, key=lambda x: x.speed, reverse=True)
while len(heroes) > 0 and len(enemies) > 0:
    clock.tick(60)
    countdown = pygame.time.get_ticks()
    if countdown - last_turn > cooldown:
        turn(sortedbyspeed[0])
        last_turn = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    #print(random.randint(1, 1000))
    background.fill(BLACK)
    all_sprites.draw(background)
    all_sprites.update()
    pygame.display.update()

pygame.quit()